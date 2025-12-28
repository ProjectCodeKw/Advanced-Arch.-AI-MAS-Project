import paho.mqtt.client as mqtt
import json
import time
import uuid

# MQTT Broker Configuration
BROKER_HOST = "192.168.1.84"
BROKER_PORT = 1883

# MQTT Topics (all channels)
TOPIC_CODE = "tasks/code"
TOPIC_TEXT = "tasks/text"
TOPIC_MATH = "tasks/math"
TOPIC_TRANSLATE = "tasks/translate"
TOPIC_COMPLETED = "tasks/completed"

# Track active tasks: {task_id: {prompt, subtasks, results}}
active_tasks = {}

# Callback when connected to broker
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"[OK] Connected to MQTT broker at {BROKER_HOST}:{BROKER_PORT}")
        client.subscribe(TOPIC_COMPLETED)
        print(f"[OK] Subscribed to {TOPIC_COMPLETED}")
    else:
        print(f"[ERROR] Connection failed with code {reason_code}")

# Callback when message received on tasks/completed
def on_message(client, userdata, msg):
    print(f"\n[RECEIVED] Result on {msg.topic}:")
    payload = json.loads(msg.payload.decode())
    print(json.dumps(payload, indent=2))
    
    # Extract task_id from result
    task_id = payload.get("task_id")
    
    if task_id in active_tasks:
        # Store the result
        active_tasks[task_id]["results"].append(payload)
        
        print(f"\n[MATCH] Found task {task_id}")
        print(f"Original prompt: {active_tasks[task_id]['prompt']}")
        print(f"Agent result: {payload.get('result', 'N/A')}")
        
        # Check if all subtasks completed
        total_subtasks = active_tasks[task_id]["total_subtasks"]
        completed = len(active_tasks[task_id]["results"])
        
        if completed == total_subtasks:
            print(f"\n[COMPLETE] All subtasks for task {task_id} finished!")
            print("="*60)
            reconstruct_response(task_id)
            # Clean up
            del active_tasks[task_id]
    else:
        print(f"[WARNING] Unknown task_id: {task_id}")

def reconstruct_response(task_id):
    """Combine all subtask results into final response"""
    task_info = active_tasks[task_id]
    print(f"\n[FINAL RESPONSE] Task: {task_id}")
    print(f"Original Prompt: {task_info['prompt']}")
    print("-" * 60)
    
    # Sort results by subtask_id
    results = sorted(task_info["results"], key=lambda x: x.get("subtask_id", 0))
    
    for result in results:
        print(f"\nSubtask {result['subtask_id']} ({result['type']}):")
        print(f"  Agent: {result.get('agent_id', 'unknown')}")
        print(f"  Execution Time: {result.get('execution_time_ms', 0):.2f} ms")
        print(f"  Result: {result.get('result', 'N/A')[:200]}...")  # First 200 chars
    
    print("="*60)
    # Here you would send this back to the client/user

# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="orchestrator_test")
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker
print(f"Connecting to broker at {BROKER_HOST}:{BROKER_PORT}...")
client.connect(BROKER_HOST, BROKER_PORT, 60)
client.loop_start()

# Wait for connection
time.sleep(2)

# Simulate client request
print("\n" + "="*60)
print("CLIENT REQUEST: Write a Python function to calculate factorial")
print("="*60)

task_id = str(uuid.uuid4())[:8]

# Track this task
active_tasks[task_id] = {
    "prompt": "Write a Python function to calculate factorial",
    "total_subtasks": 1,  # Only 1 subtask for this test
    "results": []
}

# Create and publish subtask
subtask = {
    "task_id": task_id,
    "subtask_id": 1,
    "type": "code",
    "data": "Write a Python function to calculate factorial",
    "next": None,
    "timestamp": time.time()
}

print(f"\n[PUBLISH] Sending to {TOPIC_CODE}:")
print(json.dumps(subtask, indent=2))
client.publish(TOPIC_CODE, json.dumps(subtask))

print("\n[OK] Subtask published!")
print(f"[TRACKING] Task {task_id} added to active_tasks")
print("Waiting for Code Agent response... (Ctrl+C to exit)")

# Keep running to receive response
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\nShutting down...")
    client.loop_stop()
    client.disconnect()