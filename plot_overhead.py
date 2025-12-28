#!/usr/bin/env python3
"""
Plot network overhead and reputation for PARALLEL task simulation.
Stacked layout (top/bottom) like the sequential plot.
Skips sequential task_type results.
FILTERS OUT first encounter per channel (anomalous timing bug).
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
with open('C:\\Users\\User\\OneDrive\\Desktop\\Advanced Arch\\IndependantResults\\combined_results.json', 'r') as f:
    data = json.load(f)

# Track first encounter per channel to filter them out
first_encounter_seen = {
    'code': False,
    'text': False,
    'math': False,
    'translate': False
}

def is_first_encounter(task):
    """Check if this task contains a first encounter for any channel"""
    agents = task.get('agents', [])
    for agent in agents:
        agent_id = agent.get('agent_id', '')
        for channel in first_encounter_seen.keys():
            if agent_id.startswith(channel):
                if not first_encounter_seen[channel]:
                    first_encounter_seen[channel] = True
                    return True
    return False

# Extract tasks with network overhead, grouped by difficulty
# SKIP sequential task_type AND first encounters
difficulty_data = {}
task_counter = 0
filtered_count = 0

for task in data['tasks']:
    # Skip sequential tasks
    if task.get('task_type') == 'sequential':
        continue
    
    # Skip first encounter per channel
    if is_first_encounter(task):
        filtered_count += 1
        continue
    
    overhead = task.get('timing', {}).get('network_overhead_s', 0)
    if overhead > 0:
        task_counter += 1
        diff = task.get('difficulty', 'unknown')
        if diff not in difficulty_data:
            difficulty_data[diff] = {'x': [], 'y': []}
        difficulty_data[diff]['x'].append(task_counter)
        difficulty_data[diff]['y'].append(overhead)

print(f"Filtered out {filtered_count} first-encounter tasks")
print(f"Total tasks after filtering: {task_counter}")
print(f"Difficulties: {list(difficulty_data.keys())}")

# Print averages per difficulty
print("\n=== AVERAGE NETWORK OVERHEAD (excluding first encounters) ===")
for diff, vals in sorted(difficulty_data.items()):
    avg = sum(vals['y']) / len(vals['y']) if vals['y'] else 0
    print(f"{diff}: {avg:.3f}s (n={len(vals['y'])})")

# Color map for difficulties
colors = {
    'single_task': '#1f77b4',
    'two_tasks': '#ff7f0e', 
    'four_tasks': '#2ca02c',
    'five_tasks': '#d62728'
}

markers = {
    'single_task': 'o',
    'two_tasks': 's', 
    'four_tasks': '^',
    'five_tasks': 'D'
}

# Setup figure - STACKED (top/bottom)
sns.set_style("whitegrid")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Plot 1: Network Overhead - LINES with markers
for diff, vals in difficulty_data.items():
    color = colors.get(diff, 'gray')
    marker = markers.get(diff, 'o')
    label = diff.replace('_', ' ').title()
    ax1.plot(vals['x'], vals['y'], '-', color=color, marker=marker, 
             label=label, markersize=4, linewidth=1.5, alpha=0.8)

ax1.set_ylabel('Network Overhead (s)', fontsize=11)
ax1.set_title('Network Overhead per Task by Difficulty Category (First Encounters Excluded)', fontsize=12)
ax1.legend(loc='upper right', fontsize=9)

# Plot 2: Reputation Over Time
# Reset first encounter tracking for reputation plot
first_encounter_seen_rep = {
    'code': False,
    'text': False,
    'math': False,
    'translate': False
}

# Start with baseline reputation at task 0
rep_history = {
    'code_agent_1': {'x': [0], 'y': [0.35]},
    'code_agent_2': {'x': [0], 'y': [0.2]},
    'text_agent_1': {'x': [0], 'y': [0.35]},
    'math_agent_1': {'x': [0], 'y': [0.35]},
    'translate_agent_1': {'x': [0], 'y': [0.35]}
}

task_idx = 0
for task in data['tasks']:
    # Skip sequential tasks
    if task.get('task_type') == 'sequential':
        continue
    
    # Check if first encounter (for filtering)
    is_first = False
    for agent in task.get('agents', []):
        agent_id = agent.get('agent_id', '')
        for channel in first_encounter_seen_rep.keys():
            if agent_id.startswith(channel) and not first_encounter_seen_rep[channel]:
                first_encounter_seen_rep[channel] = True
                is_first = True
    
    if is_first:
        continue
    
    task_idx += 1
    for update in task.get('reputation_updates', []):
        agent_id = update.get('agent_id')
        new_score = update.get('new_score')
        if agent_id and new_score:
            if agent_id not in rep_history:
                rep_history[agent_id] = {'x': [0], 'y': [0.35]}
            rep_history[agent_id]['x'].append(task_idx)
            rep_history[agent_id]['y'].append(new_score)

# Agent colors
agent_colors = {
    'code_agent_1': '#d62728',
    'code_agent_2': '#ff9896',
    'text_agent_1': '#1f77b4',
    'math_agent_1': '#2ca02c',
    'translate_agent_1': '#ff7f0e'
}

for agent_id, history in rep_history.items():
    color = agent_colors.get(agent_id, 'gray')
    label = agent_id.replace('_', ' ').replace('agent ', 'Agent ')
    
    # Check if agent was unused (only has baseline point)
    if len(history['x']) == 1:
        ax2.axhline(y=history['y'][0], color=color, linestyle='--', label=label + ' (unused)', alpha=0.7)
    else:
        ax2.plot(history['x'], history['y'], '-o', color=color, label=label, markersize=3, linewidth=1.5)

ax2.set_xlabel('Task Number', fontsize=11)
ax2.set_ylabel('Reputation Score', fontsize=11)
ax2.set_title('Agent Reputation Over Time (First Encounters Excluded)', fontsize=12)
ax2.legend(loc='lower right', fontsize=9)
ax2.set_ylim(0.1, 1.05)

# Set x-axis ticks
max_task = max(task_counter, max(max(h['x']) for h in rep_history.values() if h['x']))
ax2.set_xticks(range(0, max_task + 1, 5))
ax2.set_xlim(0, max_task + 1)

plt.tight_layout()
plt.savefig('parallel_network_overhead_filtered.png', dpi=150, bbox_inches='tight')
print("\nSaved to parallel_network_overhead_filtered.png")
plt.show()