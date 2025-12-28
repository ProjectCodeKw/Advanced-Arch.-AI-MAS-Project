#!/usr/bin/env python3
"""
Runner script for Orchestrator
"""

import uuid
from orchestrator import Orchestrator
import time
from independant_prompts import EASY_PROMPTS
from dependant_prompts import DEPENDANT_PROMPTS

# Configuration
BROKER_HOST = "192.168.1.84"
BROKER_PORT = 1883
MODEL_PATH = "/home/ai-mas/arch-ai-mas/Advanced-Arch.-AI-MAS-Project/Benchmark/model/phi3-5/Phi-3.5-mini-instruct-Q4_K_M.gguf"


def print_result(result):
    """Callback to print task completion results"""
    print("\n" + "=" * 70)
    print(f"TASK COMPLETED: {result['task_id']}")
    print(f"Task Type: {result.get('task_type', 'unknown').upper()}")
    print(f"Difficulty: {result.get('difficulty', 'unknown')}")
    print("=" * 70)
    print(f"Prompt: {result['prompt'][:60]}...")
    print(f"Decomposition Time: {result['decomposition_time_s']:.2f}s")
    print("-" * 70)
    
    for st in result["subtasks"]:
        print(f"\n  Subtask {st['subtask_id']} ({st['type']})")
        print(f"    Chain Execution: {st['chain_execution_s']:.3f}s")
        
        for agent in st.get("agents_in_chain", []):
            print(f"      -> {agent['agent_id']}: {agent['execution_time_s']:.3f}s")
    
    print("-" * 70)
    totals = result["totals"]
    print(f"TOTALS:")
    print(f"  Agent Execution:  {totals['agent_execution_s']:.3f}s (sum of all agents)")
    if "max_parallel_execution_s" in totals:
        print(f"  Max Parallel:     {totals['max_parallel_execution_s']:.3f}s (bottleneck)")
    print(f"  Network Overhead: {totals['network_overhead_s']:.3f}s")
    print(f"  Round Trip:       {totals['round_trip_s']:.3f}s")
    
    # Print reputation updates
    rep_updates = result.get("reputation_updates", [])
    if rep_updates:
        print("-" * 70)
        print("REPUTATION UPDATES:")
        for update in rep_updates:
            delta_str = f"+{update['delta']:.4f}" if update['delta'] >= 0 else f"{update['delta']:.4f}"
            print(f"  {update['agent_id']}: {update['old_score']:.4f} -> {update['new_score']:.4f} ({delta_str})")
    
    print("=" * 70 + "\n")


def main():
    print("Starting Orchestrator...")
    
    indp_prompts = EASY_PROMPTS()
    
    orch = Orchestrator(
        broker_host=BROKER_HOST,
        model_path=MODEL_PATH,
        broker_port=BROKER_PORT
    )
    
    # Set callback for results
    orch.on_task_complete = print_result

    orch.initialize_agents_with_scores({
        "code": [
            ("code_agent_1", 0.35),
            ("code_agent_2", 0.2)
        ],
        "text": [
            ("text_agent_1", 0.35)
        ],
        "math": [
            ("math_agent_1", 0.35)
        ],
        "translate": [
            ("translate_agent_1", 0.35)
        ]
    })
    
    orch.start()
    print("Orchestrator connected. Waiting 2s...")
    time.sleep(2)
    
    try:
        total_prompts = sum(len(prompts) for prompts in indp_prompts.values())
        prompt_counter = 0
        
        for category, prompts in indp_prompts.items():
            print(f"\n### CATEGORY: {category.upper()} ({len(prompts)} prompts) ###\n")
            
            for i, prompt in enumerate(prompts, 1):
                prompt_counter += 1
                
                print(f"[{prompt_counter}/{total_prompts}] {prompt[:50]}...")
                
                task_id = f"{category}_{i}_{str(uuid.uuid4())[:6]}"
                orch.process_prompt(prompt, task_id, difficulty=category)
                
                if prompt_counter < total_prompts:
                    time.sleep(20)
                else:
                    time.sleep(30)
        
        print("\nBenchmark complete!")
        
    except KeyboardInterrupt:
        print("\nInterrupted.")

    orch.stop()
    print("Orchestrator stopped.")


if __name__ == "__main__":
    main()