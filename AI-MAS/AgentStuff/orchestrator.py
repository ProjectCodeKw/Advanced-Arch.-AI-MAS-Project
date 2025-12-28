#!/usr/bin/env python3
"""
Mini-Orchestrator with Phi-3.5 Decomposition and Credibility Layer
Simple duration-based timing - no clock sync needed
"""

import paho.mqtt.client as mqtt
import json
import time
from llama_cpp import Llama


class Orchestrator:
    
    def __init__(self, broker_host, model_path, broker_port=1883):
        self.broker_host = broker_host
        self.broker_port = broker_port
        
        self.llm = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_threads=4,
            n_gpu_layers=0,
            verbose=False
        )
        
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="orchestrator")
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        
        self.active_tasks = {}
        
        self.reputation_tables = {
            "code": {},
            "text": {},
            "math": {},
            "translate": {}
        }
        
        self._load_reputation_tables()
        
        self.W_FEEDBACK = 0.3
        self.W_EFFICIENCY = 0.4
        self.W_TCR = 0.3
        self.ALPHA = 0.15
        self.BETA = 0.85
        self.NEW_AGENT_BASELINE = 0.35
        
        self.HISTORY_WINDOW = 20
        
        # Callback
        self.on_task_complete = None
        
        # Results log file - in execution_logs directory
        self.results_log = "execution_logs/benchmark_results.json"
        self._init_results_log()
    
    def _load_reputation_tables(self):
        try:
            with open("reputation_data/reputation_tables.json", "r") as f:
                self.reputation_tables = json.load(f)
        except FileNotFoundError:
            pass
    
    def _save_reputation_tables(self):
        import os
        os.makedirs("reputation_data", exist_ok=True)
        with open("reputation_data/reputation_tables.json", "w") as f:
            json.dump(self.reputation_tables, f, indent=2)
    
    def _init_results_log(self):
        """Initialize or load existing results log"""
        import os
        os.makedirs("execution_logs", exist_ok=True)
        
        if os.path.exists(self.results_log):
            try:
                with open(self.results_log, "r") as f:
                    self.all_results = json.load(f)
            except:
                self.all_results = {"tasks": [], "summary": {}}
        else:
            self.all_results = {"tasks": [], "summary": {}}
        
        # Log this run's start time
        self.run_start_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.run_id = time.strftime("%Y%m%d_%H%M%S")    
    def _save_result(self, result_summary):
        """Save task result to JSON log"""
        # Add run metadata to result
        result_summary["run_id"] = self.run_id
        result_summary["run_timestamp"] = self.run_start_time
        
        self.all_results["tasks"].append(result_summary)
        
        # Update summary stats
        tasks = self.all_results["tasks"]
        total = len(tasks)
        
        # Categorize tasks by task_type field
        single_tasks = [t for t in tasks if t.get("task_type") == "single_agent"]
        sequential_tasks = [t for t in tasks if t.get("task_type") == "sequential"]
        parallel_tasks = [t for t in tasks if t.get("task_type") == "parallel"]
        
        def avg(lst, key):
            if not lst:
                return 0
            return round(sum(t["totals"][key] for t in lst) / len(lst), 3)

        def avg_decomp(lst):
            if not lst:
                return 0
            return round(sum(t["decomposition_time_s"] for t in lst) / len(lst), 3)
        
        self.all_results["summary"] = {
            "total_tasks": total,
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "single_agent_tasks": {
                "count": len(single_tasks),
                "avg_decomposition_s": avg_decomp(single_tasks),
                "avg_execution_s": avg(single_tasks, "agent_execution_s"),
                "avg_network_overhead_s": avg(single_tasks, "network_overhead_s"),
                "avg_round_trip_s": avg(single_tasks, "round_trip_s")
            },
            "sequential_tasks": {
                "count": len(sequential_tasks),
                "avg_decomposition_s": avg_decomp(sequential_tasks),
                "avg_execution_s": avg(sequential_tasks, "agent_execution_s"),
                "avg_network_overhead_s": avg(sequential_tasks, "network_overhead_s"),
                "avg_round_trip_s": avg(sequential_tasks, "round_trip_s")
            },
            "parallel_tasks": {
                "count": len(parallel_tasks),
                "avg_decomposition_s": avg_decomp(parallel_tasks),
                "avg_execution_s": avg(parallel_tasks, "agent_execution_s"),
                "avg_network_overhead_s": avg(parallel_tasks, "network_overhead_s"),
                "avg_round_trip_s": avg(parallel_tasks, "round_trip_s")
            }
        }
        
        with open(self.results_log, "w") as f:
            json.dump(self.all_results, f, indent=2)
    
    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            client.subscribe("tasks/completed")
    
    def _on_message(self, client, userdata, msg):
        if msg.topic == "tasks/completed":
            self._handle_completion(msg)
    
    def decompose_task(self, prompt):
        """
        Use Phi-3.5 to decompose prompt into subtasks
        
        Args:
            prompt: User's task description
            
        Returns:
            dict: {"subtasks": [{id, channel, task, depends_on}, ...]}
        """
        
        system_prompt = """You are a task decomposition assistant. Your job is to identify ALL tasks in the user's prompt and assign each one to the appropriate agent.

    CRITICAL: If the user mentions MULTIPLE different tasks (like "do X and Y"), you MUST create separate subtasks for each one."""

        user_message = f"""Task: {prompt}

    Available agents:
    - tasks/text: summaries, definitions, explanations, descriptions
    - tasks/code: code generation (Python, JavaScript, SQL, any programming)
    - tasks/math: calculations, formulas, equations
    - tasks/translate: English-Arabic translation

    RULES:
    1. Carefully read the ENTIRE prompt - look for words like "and", "also", "then"
    2. Each distinct task mentioned gets its own subtask
    3. Match each subtask to the correct agent type
    4. Copy the user's EXACT wording for each task - DO NOT add examples or values
    5. If one task needs the output of another, use depends_on with the prerequisite's id

    Examples (using placeholders):

    Input: "Define TOPIC_X and write PROGRAMMING_TASK_Y"
    Output: {{"subtasks": [
    {{"id": 1, "channel": "tasks/text", "sub-task": "Define TOPIC_X", "depends_on": []}},
    {{"id": 2, "channel": "tasks/code", "sub-task": "Write PROGRAMMING_TASK_Y", "depends_on": []}}
    ]}}

    Input: "Calculate MATH_OPERATION then explain CONCEPT"
    Output: {{"subtasks": [
    {{"id": 1, "channel": "tasks/math", "sub-task": "Calculate MATH_OPERATION", "depends_on": []}},
    {{"id": 2, "channel": "tasks/text", "sub-task": "Explain CONCEPT", "depends_on": [1]}}
    ]}}

    Input: "Write code for TASK_X"
    Output: {{"subtasks": [
    {{"id": 1, "channel": "tasks/code", "sub-task": "Write code for TASK_X", "depends_on": []}}
    ]}}

    Now decompose this task (use the EXACT words from the user's prompt, do NOT substitute with examples):
    {prompt}

    Output ONLY valid JSON:"""

        full_prompt = f"<|system|>{system_prompt}<|end|><|user|>{user_message}<|end|><|assistant|>"
        
        response = self.llm(
            full_prompt,
            max_tokens=1024,
            temperature=0.1,
            stop=["<|end|>", "<|user|>"],
            echo=False
        )
        
        raw_output = response["choices"][0]["text"].strip()
        
        try:
            if "```json" in raw_output:
                raw_output = raw_output.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_output:
                raw_output = raw_output.split("```")[1].split("```")[0].strip()
            
            decomposition = json.loads(raw_output)
            return decomposition
            
        except json.JSONDecodeError:
            start = raw_output.find("{")
            end = raw_output.rfind("}") + 1
            
            if start != -1 and end != 0:
                json_str = raw_output[start:end]
                try:
                    decomposition = json.loads(json_str)
                    return decomposition
                except:
                    pass
            
            return {
                "subtasks": [{
                    "id": 1,
                    "channel": "tasks/text",
                    "sub-task": prompt,
                    "depends_on": []
                }]
            }
    
    def restructure_dependencies(self, decomposition, task_id):
        subtasks = decomposition.get("subtasks", [])
        
        initial_subtasks = [st for st in subtasks if not st.get("depends_on")]
        
        structured_subtasks = []
        
        def build_chain(subtask_id):
            dependents = [
                st for st in subtasks
                if subtask_id in st.get("depends_on", [])
            ]
            
            if not dependents:
                return None
            
            next_subtask = dependents[0]
            next_id = next_subtask["id"]
            
            next_channel = next_subtask["channel"]
            if next_channel.startswith("tasks/"):
                next_type = next_channel.split("/")[1]
            else:
                next_type = next_channel
            
            return {
                "subtask_id": next_id,
                "channel": f"tasks/{next_type}",
                "sub-task": next_subtask["sub-task"],
                "next": build_chain(next_id)
            }
        
        for subtask in initial_subtasks:
            st_id = subtask["id"]
            
            channel = subtask["channel"]
            if channel.startswith("tasks/"):
                st_type = channel.split("/")[1]
            else:
                st_type = channel
            
            next_chain = build_chain(st_id)
            
            structured_subtask = {
                "task_id": task_id,
                "subtask_id": st_id,
                "type": st_type,
                "data": subtask["sub-task"],
                "next": next_chain
            }
            
            structured_subtasks.append(structured_subtask)
        
        return structured_subtasks
    
    def publish_subtasks(self, subtasks):
        for subtask in subtasks:
            channel = f"tasks/{subtask['type']}/request"
            self.client.publish(channel, json.dumps(subtask))
    
    def process_prompt(self, prompt, task_id, difficulty="unknown"):
        # Decomposition timing (local)
        decomp_start = time.time()
        decomposition = self.decompose_task(prompt)
        decomp_time_s = time.time() - decomp_start
        
        structured_subtasks = self.restructure_dependencies(decomposition, task_id)
        
        def count_final(subtasks):
            count = 0
            for st in subtasks:
                if st.get("next") is None:
                    count += 1
            return count
        
        # Start round-trip timer AFTER decomposition, RIGHT BEFORE publishing
        round_trip_start = time.time()
        
        self.active_tasks[task_id] = {
            "round_trip_start": round_trip_start,
            "decomposition_time_s": decomp_time_s,
            "prompt": prompt,
            "difficulty": difficulty,
            "subtasks": structured_subtasks,
            "completed_subtasks": [],
            "expected_completions": count_final(structured_subtasks)
        }
        
        self.publish_subtasks(structured_subtasks)
        
        return {
            "task_id": task_id,
            "subtask_count": len(decomposition.get("subtasks", [])),
            "decomposition_time_s": decomp_time_s
        }
    
    def _handle_completion(self, msg):
        receive_time = time.time()  # Stop timer immediately
        
        try:
            result = json.loads(msg.payload.decode())
            task_id = result.get("task_id")
            
            if task_id not in self.active_tasks:
                return
            
            task_info = self.active_tasks[task_id]
            
            # Store receive time for this completion
            if "receive_times" not in task_info:
                task_info["receive_times"] = []
            task_info["receive_times"].append(receive_time)
            
            self._update_reputation(result, task_info)
            
            task_info["completed_subtasks"].append(result)
            
            completed_count = len(task_info["completed_subtasks"])
            expected_count = task_info["expected_completions"]
            
            if completed_count >= expected_count:
                self._finalize_task(task_id)
        
        except:
            pass
    
    def _update_reputation(self, result, task_info):
        agent_times = result.get("agent_times", [])
        if not agent_times:
            return
        
        # Track reputation updates for this task
        if "reputation_updates" not in task_info:
            task_info["reputation_updates"] = []
        
        # Update reputation for each agent in the chain
        for agent_entry in agent_times:
            agent_id = agent_entry.get("agent_id")
            execution_time_s = agent_entry.get("execution_time_s", 0)
            execution_time_ms = execution_time_s * 1000
            
            # Determine agent type from agent_id (e.g., "code_agent_1" -> "code", "text_agent_1" -> "text")
            if "_agent_" in agent_id:
                agent_type = agent_id.split("_agent_")[0]
            else:
                agent_type = result.get("type")
            
            if agent_type not in self.reputation_tables:
                continue
            
            if agent_id not in self.reputation_tables[agent_type]:
                self.reputation_tables[agent_type][agent_id] = {
                    "score": self.NEW_AGENT_BASELINE,
                    "TCR": []
                }
            
            agent_data = self.reputation_tables[agent_type][agent_id]
            
            # Handle old format (history) -> new format (TCR)
            if "history" in agent_data and "TCR" not in agent_data:
                agent_data["TCR"] = agent_data.pop("history")
            elif "TCR" not in agent_data:
                agent_data["TCR"] = []
            
            old_score = agent_data["score"]
            
            q_feedback = 0.5
            
            
            EXPECTED_TIMES_MS = {
                "code": 16000,      # avg of code_agent_1 (15.71s) and code_agent_2 (16.65s) ≈ 16s
                "text": 12500,      # 12.41s → 12.5s
                "math": 6000,       # 5.78s → 6s
                "translate": 350    # 0.34s → 350ms
            }
            expected_time_ms = EXPECTED_TIMES_MS.get(agent_type, 10000)
            r = expected_time_ms / max(execution_time_ms, 1)
            r_capped = min(r, 2.0)
            s_efficiency = (r_capped - 0.5) / 1.5
            
            agent_data["TCR"].append({"completed": True})
            if len(agent_data["TCR"]) > self.HISTORY_WINDOW:
                agent_data["TCR"] = agent_data["TCR"][-self.HISTORY_WINDOW:]
            
            completed_count = sum(1 for h in agent_data["TCR"] if h.get("completed"))
            tcr = completed_count / len(agent_data["TCR"])
            
            delta = (self.W_FEEDBACK * q_feedback + 
                    self.W_EFFICIENCY * s_efficiency + 
                    self.W_TCR * tcr)
            
            if delta > 0:
                new_score = old_score + self.ALPHA * delta * (1 - old_score)
            else:
                new_score = old_score * (1 + self.BETA * delta)
            
            new_score = max(0.0, min(1.0, new_score))
            agent_data["score"] = round(new_score, 3)
            
            # Store the reputation update
            task_info["reputation_updates"].append({
                "agent_id": agent_id,
                "agent_type": agent_type,
                "old_score": round(old_score, 4),
                "new_score": round(new_score, 4),
                "delta": round(new_score - old_score, 4)
            })
            
            self._publish_reputation_table(agent_type)
        
        self._save_reputation_tables()
    
    def _publish_reputation_table(self, channel):
        topic = f"tasks/{channel}/reputation"
        
        reputations = [
            {"agent_id": agent_id, "score": data["score"]}
            for agent_id, data in self.reputation_tables[channel].items()
        ]
        
        message = {
            "channel": f"tasks/{channel}",
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "reputations": reputations
        }
        
        self.client.publish(topic, json.dumps(message), retain=True)
    
    def _finalize_task(self, task_id):
        task_info = self.active_tasks[task_id]
        
        # Use the last receive time (when final completion arrived)
        round_trip_end = task_info["receive_times"][-1]
        round_trip_s = round_trip_end - task_info["round_trip_start"]
        
        result_summary = {
            "task_id": task_id,
            "prompt": task_info["prompt"],
            "difficulty": task_info.get("difficulty", "unknown"),
            "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "decomposition_time_s": task_info.get("decomposition_time_s", 0),
            "round_trip_s": round_trip_s,
            "subtasks": []
        }
        
        # Collect all agent execution times
        total_agent_execution_s = 0
        total_agents_in_chains = 0
        num_subtasks = len(task_info["completed_subtasks"])
        
        for result in task_info["completed_subtasks"]:
            agent_times = result.get("agent_times", [])
            
            subtask_exec_s = 0
            agents_in_chain = []
            
            for at in agent_times:
                exec_s = at.get("execution_time_s", 0)
                subtask_exec_s += exec_s
                agents_in_chain.append({
                    "agent_id": at.get("agent_id"),
                    "execution_time_s": exec_s
                })
            
            total_agent_execution_s += subtask_exec_s
            total_agents_in_chains += len(agents_in_chain)
            
            subtask_result = {
                "subtask_id": result.get("subtask_id"),
                "final_agent": result.get("agent_id"),
                "type": result.get("type"),
                "result": result.get("result"),
                "agents_in_chain": agents_in_chain,
                "chain_execution_s": subtask_exec_s
            }
            
            result_summary["subtasks"].append(subtask_result)
        
        # Determine task type
        if num_subtasks == 1 and total_agents_in_chains == 1:
            task_type = "single_agent"
        elif num_subtasks == 1 and total_agents_in_chains > 1:
            task_type = "sequential"
        elif num_subtasks > 1:
            task_type = "parallel"
        else:
            task_type = "unknown"
        
        result_summary["task_type"] = task_type
        result_summary["num_subtasks"] = num_subtasks
        result_summary["num_agents_total"] = total_agents_in_chains
        
        # Calculate network overhead based on task type
        if task_type == "parallel":
            max_chain_execution = max(st["chain_execution_s"] for st in result_summary["subtasks"])
            network_overhead_s = round_trip_s - max_chain_execution
            print(f"[DEBUG] Parallel: round_trip={round_trip_s:.3f}, max_exec={max_chain_execution:.3f}, network={network_overhead_s:.3f}")
        else:
            network_overhead_s = round_trip_s - total_agent_execution_s
            print(f"[DEBUG] Sequential: round_trip={round_trip_s:.3f}, total_exec={total_agent_execution_s:.3f}, network={network_overhead_s:.3f}")
        
        if network_overhead_s < 0:
            network_overhead_s = 0
        
        result_summary["totals"] = {
            "agent_execution_s": total_agent_execution_s,
            "network_overhead_s": network_overhead_s,
            "round_trip_s": round_trip_s
        }
        
        if task_type == "parallel":
            result_summary["totals"]["max_parallel_execution_s"] = max_chain_execution
        
        result_summary["reputation_updates"] = task_info.get("reputation_updates", [])
        
        task_info["final_result"] = result_summary
        
        self._save_result(result_summary)
        
        if self.on_task_complete:
            self.on_task_complete(result_summary)
        
        del self.active_tasks[task_id]
        
        return result_summary
    
    def get_reputation_tables(self):
        return self.reputation_tables
    
    def initialize_agents_with_scores(self, agent_configs):
        for channel, agents in agent_configs.items():
            if channel not in self.reputation_tables:
                continue
            
            for agent_id, score in agents:
                self.reputation_tables[channel][agent_id] = {
                    "score": score,
                    "TCR": []
                }
        
        self._save_reputation_tables()
        
        for channel in agent_configs.keys():
            if channel in self.reputation_tables:
                self._publish_reputation_table(channel)
    
    def start(self):
        self.client.connect(self.broker_host, self.broker_port, 60)
        self.client.loop_start()
    
    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()