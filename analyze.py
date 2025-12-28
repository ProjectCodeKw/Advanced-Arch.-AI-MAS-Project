#!/usr/bin/env python3
"""
Combine MQTT broker timing logs with orchestrator results
to get accurate network overhead measurements.

Network overhead = sum of all (request → claim) times
This represents the time subtasks spend waiting in MQTT channels
before being claimed by agents.

For sequential: orch→A1 + A1→A2 + A2→A3 ...
For parallel: sum of all request→claim (they happen simultaneously)
"""

import json
from collections import defaultdict

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)


def calculate_network_overhead(broker_task):
    """
    Calculate network overhead as sum of (request → claim) times.
    
    This is the time subtasks spend in MQTT channels waiting to be claimed.
    """
    if not broker_task:
        return 0, []
    
    broker_subtasks = broker_task.get("subtasks", {})
    
    total_overhead = 0
    subtask_details = []
    
    # Sort subtasks by request time for proper ordering
    sorted_subtasks = sorted(
        broker_subtasks.items(),
        key=lambda x: (x[1].get("request_time") or 0) if x[1] else 0
    )
    
    for subtask_id, subtask_data in sorted_subtasks:
        if not subtask_data:
            continue
        
        request_time = subtask_data.get("request_time")
        claim_time = subtask_data.get("claim_time")
        
        if request_time and claim_time:
            req_to_claim = claim_time - request_time
            
            # Handle clock sync issues (negative values)
            if req_to_claim < 0:
                req_to_claim = 0
            
            total_overhead += req_to_claim
            
            subtask_details.append({
                "subtask_id": subtask_id,
                "request_time": round(request_time, 3),
                "claim_time": round(claim_time, 3),
                "request_to_claim_s": round(req_to_claim, 3),
                "claim_agent": subtask_data.get("claim_agent")
            })
    
    return round(total_overhead, 3), subtask_details


def process_reputation_data(reputation_data):
    """Process reputation data to add job_count and TCR percentage."""
    processed = {}
    
    for agent_type, agents in reputation_data.items():
        processed[agent_type] = {}
        
        for agent_id, data in agents.items():
            tcr_list = data.get("TCR", [])
            job_count = len(tcr_list)
            
            if job_count > 0:
                completed_count = sum(1 for entry in tcr_list if entry.get("completed", False))
                tcr_percentage = round(completed_count / job_count, 3)
            else:
                tcr_percentage = 0.0
            
            processed[agent_type][agent_id] = {
                "score": round(data.get("score", 0), 3),
                "job_count": job_count,
                "tcr_percentage": tcr_percentage
            }
    
    return processed


def combine_results(mqtt_log_path, orchestrator_results_path, reputation_path, output_path):
    """Combine all data sources into clean results."""
    
    mqtt_log = load_json(mqtt_log_path)
    orch_results = load_json(orchestrator_results_path)
    reputation_data = load_json(reputation_path)
    
    # Get tasks from broker format
    broker_tasks = mqtt_log.get("tasks", {})
    
    # Process reputation data
    processed_reputation = process_reputation_data(reputation_data)
    
    combined = {
        "metadata": {
            "run_id": "",
            "run_timestamp": "",
            "total_tasks": 0
        },
        "tasks": [],
        "summary": {
            "by_task_type": {},
            "by_agent_type": {},
            "by_difficulty": {}
        },
        "reputation_final": processed_reputation
    }
    
    # Process each task
    for task in orch_results.get("tasks", []):
        task_id = task.get("task_id")
        task_type = task.get("task_type", "unknown")
        task_status = task.get("status", "completed")
        
        # Get broker data for this task
        broker_task = broker_tasks.get(task_id, {})
        
        # Skip tasks with no MQTT data (not captured by monitor)
        if not broker_task or not broker_task.get("subtasks"):
            print(f"Skipping {task_id} - no MQTT data")
            continue
        
        # Calculate network overhead as sum of request→claim times
        network_overhead, overhead_breakdown = calculate_network_overhead(broker_task)
        
        # Get broker round trip (first_request to last_completed)
        broker_round_trip = broker_task.get("total_broker_round_trip_s")
        if broker_round_trip is None:
            # Fallback to orchestrator's round_trip if broker data missing
            broker_round_trip = task.get("totals", {}).get("round_trip_s", 0) or 0
        
        # Extract timing values
        decomposition_time = task.get("decomposition_time_s") or 0
        agent_execution = task.get("totals", {}).get("agent_execution_s") or 0
        
        # Build agents list
        agents_list = []
        for subtask in task.get("subtasks", []):
            for agent in subtask.get("agents_in_chain", []):
                exec_time = agent.get("execution_time_s")
                agents_list.append({
                    "agent_id": agent["agent_id"],
                    "execution_time_s": round(exec_time, 3) if exec_time is not None else None,
                    "status": agent.get("status", "completed")
                })
        
        # Build clean task output
        clean_task = {
            "task_id": task_id,
            "prompt": task.get("prompt"),
            "difficulty": task.get("difficulty"),
            "task_type": task_type,
            "status": task_status,
            "num_agents": task.get("num_agents_total"),
            
            # Timing summary
            "timing": {
                "decomposition_s": round(decomposition_time, 3),
                "agent_execution_s": round(agent_execution, 3),
                "network_overhead_s": network_overhead,
                "broker_round_trip_s": round(broker_round_trip, 3),
                "total_time_s": round(decomposition_time + broker_round_trip, 3)
            },
            
            # Network overhead breakdown (request→claim per subtask)
            "network_overhead_breakdown": overhead_breakdown,
            
            # Agent chain details
            "agents": agents_list,
            
            # Reputation changes
            "reputation_updates": [
                {
                    "agent_id": update.get("agent_id"),
                    "agent_type": update.get("agent_type"),
                    "old_score": round(update.get("old_score") or 0, 3),
                    "new_score": round(update.get("new_score") or 0, 3),
                    "delta": round(update.get("delta") or 0, 3)
                }
                for update in task.get("reputation_updates", [])
            ]
        }
        
        # Add failure reason if present
        if task.get("failure_reason"):
            clean_task["failure_reason"] = task.get("failure_reason")
        
        combined["tasks"].append(clean_task)
        
        # Update metadata
        if not combined["metadata"]["run_id"]:
            combined["metadata"]["run_id"] = task.get("run_id", "")
            combined["metadata"]["run_timestamp"] = task.get("run_timestamp", "")
    
    combined["metadata"]["total_tasks"] = len(combined["tasks"])
    
    # Calculate summaries
    combined["summary"] = calculate_summaries(combined["tasks"])
    
    # Save
    with open(output_path, 'w') as f:
        json.dump(combined, f, indent=2)
    
    print(f"Combined results saved to {output_path}")
    print(f"Total tasks: {len(combined['tasks'])}")
    
    return combined


def calculate_summaries(tasks):
    """Calculate summary statistics."""
    
    summaries = {
        "by_task_type": {},
        "by_agent_type": {},
        "by_difficulty": {}
    }
    
    # Group by task type
    task_type_data = defaultdict(list)
    for task in tasks:
        task_type = task.get("task_type", "unknown")
        task_type_data[task_type].append(task)
    
    for task_type, task_list in task_type_data.items():
        n = len(task_list)
        summaries["by_task_type"][task_type] = {
            "count": n,
            "avg_decomposition_s": round(sum(t["timing"]["decomposition_s"] or 0 for t in task_list) / n, 3),
            "avg_execution_s": round(sum(t["timing"]["agent_execution_s"] or 0 for t in task_list) / n, 3),
            "avg_network_overhead_s": round(sum(t["timing"]["network_overhead_s"] or 0 for t in task_list) / n, 3),
            "avg_broker_round_trip_s": round(sum(t["timing"]["broker_round_trip_s"] or 0 for t in task_list) / n, 3),
            "avg_total_time_s": round(sum(t["timing"]["total_time_s"] or 0 for t in task_list) / n, 3)
        }
    
    # Group by agent type
    agent_data = defaultdict(list)
    for task in tasks:
        for agent in task.get("agents", []):
            agent_id = agent["agent_id"]
            exec_time = agent.get("execution_time_s")
            
            # Skip agents with no execution time (failed)
            if exec_time is None:
                continue
                
            if "_agent_" in agent_id:
                agent_type = agent_id.split("_agent_")[0]
            elif "_agent" in agent_id:
                agent_type = agent_id.split("_agent")[0]
            else:
                agent_type = "unknown"
            agent_data[agent_type].append(exec_time)
    
    for agent_type, exec_times in agent_data.items():
        if len(exec_times) > 0:
            summaries["by_agent_type"][agent_type] = {
                "tasks_handled": len(exec_times),
                "total_execution_s": round(sum(exec_times), 3),
                "avg_execution_s": round(sum(exec_times) / len(exec_times), 3)
            }
    
    # Group by difficulty
    difficulty_data = defaultdict(list)
    for task in tasks:
        diff = task.get("difficulty", "unknown")
        difficulty_data[diff].append(task)
    
    for diff, task_list in difficulty_data.items():
        n = len(task_list)
        summaries["by_difficulty"][diff] = {
            "count": n,
            "avg_decomposition_s": round(sum(t["timing"]["decomposition_s"] or 0 for t in task_list) / n, 3),
            "avg_execution_s": round(sum(t["timing"]["agent_execution_s"] or 0 for t in task_list) / n, 3),
            "avg_network_overhead_s": round(sum(t["timing"]["network_overhead_s"] or 0 for t in task_list) / n, 3),
            "avg_broker_round_trip_s": round(sum(t["timing"]["broker_round_trip_s"] or 0 for t in task_list) / n, 3),
            "avg_total_time_s": round(sum(t["timing"]["total_time_s"] or 0 for t in task_list) / n, 3)
        }
    
    return summaries
 

if __name__ == "__main__":
    
    mqtt_log_path = "IndependantResults\\mqtt_timing_log.json"
    orch_results_path = "IndependantResults\\benchmark_results.json"
    reputation_path = "IndependantResults\\reputation_tables.json"
    output_path = "IndependantResults\\combined_results.json"
    
    combine_results(mqtt_log_path, orch_results_path, reputation_path, output_path)