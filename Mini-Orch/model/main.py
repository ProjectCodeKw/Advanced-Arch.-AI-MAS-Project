"""
Orchestrator Model Benchmarking Script
Benchmarks microsoft/Phi-3.5-mini-instruct on 100 task decomposition prompts
Categorizes by decomposition complexity: Easy, Medium, Hard, Very Hard
(based on prompt clarity, not task complexity)
"""

import torch
import time
import json
import re
import statistics
from datetime import datetime
import os
from llama_cpp import Llama

# Define available agents and their capabilities
AGENT_CAPABILITIES = """
Available Agents in the System:
1. Text & Definitions Agent (tasks/text):
   - Text summarization
   - Definitions and explanations
   - Content writing
   - Language translation
   
2. Code Agent (tasks/code):
   - Python code generation
   - Multi-language code (JavaScript, SQL, etc.)
   - Code debugging and conversion
   - Script writing and API integration
   
4. Math Agent (tasks/math):
   - Mathematical calculations
   - Statistical analysis
   - Formula derivation
   
5. Image Generator Agent (tasks/image):
   - Image generation from text descriptions
   - Visual content creation
"""

# Prompts categorized by DECOMPOSITION complexity (clarity/structure)
PROMPTS = {
    "easy": [
        # Clear, well-structured prompts
        "Search for AI news and summarize it",
        "Generate Python code to calculate factorial",
        "Define machine learning in simple terms",
        "Calculate 25% of 840",
        "Create an image of a sunset over mountains",
        "Write a function to reverse a string",
        "Explain what is a neural network",
        "Generate code to read a CSV file",
        "Calculate the average of 10, 20, 30, 40",
        "Summarize this article about climate change",
        "Create a simple SQL query to select all users",
        "Define what blockchain technology is",
        "Generate an image of a futuristic city",
        "Write Python code to sort a list",
        "Calculate 15 * 23 + 45",
        "Explain the concept of recursion",
        "Generate Python code for finding the median in a list",
        "What is the derivative of x squared?",
        "Create an image of a robot in a garden",
        "Write a summary of quantum computing",
        "Generate code to connect to MySQL database",
        "Calculate the area of circle with radius 7",
        "Define artificial intelligence",
        "Create an image of abstract geometric shapes",
        "Write Python code for bubble sort algorithm"
    ],
    
    "medium": [
    # Mix of independent and dependent multi-agent tasks
    # Independent tasks (parallel execution)
    "Define machine learning and generate Python code to implement linear regression",
    "Calculate 25% of 840 and create an image showing the percentage visually",
    "Write JavaScript code for form validation and explain what is input sanitization",
    "Generate SQL query to select all users and define what is database normalization",
    "Calculate the derivative of x squared and write Python code to compute it",
    
    # Dependent tasks (sequential execution)
    "Calculate the factorial of 5 then explain the mathematical concept behind factorials",
    "Generate Python code to sort a list then calculate the time complexity",
    "Define neural networks then write code to implement a simple perceptron",
    "Calculate the area of circle with radius 7 then explain the history of pi",
    "Write code to reverse a string then explain the algorithm complexity",
    
    # More independent tasks
    "Create an image of a sunset and define what causes sunset colors",
    "Generate code to read CSV file and calculate average of numeric columns",
    "Define blockchain technology and write code to create a simple hash function",
    "Calculate fibonacci sequence up to 10 and create visualization image",
    "Write JavaScript validation code and define what is XSS attack",
    
    # More dependent tasks
    "Solve equation 2x + 5 = 13 then explain the algebraic method used",
    "Generate code for bubble sort then calculate its Big O notation",
    "Calculate mean of numbers 10, 20, 30, 40 then explain statistical significance",
    "Write code to connect to MySQL database then define connection pooling",
    "Calculate binomial coefficient then explain its applications in probability",
    
    # Mixed complexity
    "Define recursion and generate code showing recursive factorial",
    "Calculate square root of 144 and explain the Babylonian method",
    "Write Python code for matrix multiplication and define what is linear algebra",
    "Generate image of geometric shapes and calculate their areas",
    "Define API and write code to make HTTP GET request"
]
    
    
}

def load_model():
    """Load Phi-3.5-mini-instruct GGUF model"""
    MODEL_PATH = "model/phi3-5/Phi-3.5-mini-instruct-Q4_K_M.gguf"

    print(f"Loading Phi-3.5-mini-instruct from {MODEL_PATH}...")
    print("=" * 70)

    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=4096,           # Phi-3.5 supports 4k context
        n_threads=4,          # Use 4 CPU threads
        n_gpu_layers=0,       # CPU only
        chat_format="chatml", # Phi-3 uses ChatML format
        verbose=False
    )

    print("✓ Model loaded successfully")
    print("=" * 70)
    return llm

def extract_json(text):
    """
    Extract JSON from text that may contain markdown code blocks or extra content.
    Returns the parsed JSON dict or None if no valid JSON found.
    """
    # Try to find JSON in markdown code blocks first
    json_block_pattern = r'```json\s*(\{.*?\})\s*```'
    match = re.search(json_block_pattern, text, re.DOTALL)

    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # If no markdown block, try to find raw JSON
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    match = re.search(json_pattern, text, re.DOTALL)

    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return None

def run_inference(llm, prompt, category, prompt_num, responses_file):
    """Run single inference and measure execution time"""

    # Simplified, more direct prompt
    messages = [
        {
            "role": "system", 
            "content": "You are a task decomposition assistant. Break user requests into subtasks (if task is breakable) and assign them to agents: tasks/text, tasks/code, tasks/math, tasks/image"
        },
        {
    "role": "user", 
    "content": f"""Task: {prompt}

Available agents:
- tasks/text: summaries, definitions, explanations
- tasks/code: code generation (Python, JavaScript, SQL)
- tasks/math: calculations, formulas
- tasks/image: image generation

IMPORTANT RULES FOR DEPENDENCIES:
1. If a subtask uses the OUTPUT of another subtask, it MUST list that subtask in "depends_on"
2. If subtasks can run in parallel (no data dependency), set "depends_on" to []
3. Examples:
   - "Calculate X then explain Y" → subtask 2 depends on subtask 1
   - "Define X and generate code Y" → both have "depends_on": []

Output format (JSON):
{{"subtasks": [
  {{"id": 1, "channel": "tasks/math", "task": "Calculate factorial of 5", "depends_on": []}},
  {{"id": 2, "channel": "tasks/text", "task": "Explain factorial concept using result from subtask 1", "depends_on": [1]}}
]}}

Decomposition:"""
}
    ]

    start_time = time.time()

    try:
        output = llm.create_chat_completion(
            messages=messages,
            max_tokens=256,  # Reduced
            temperature=0.1,  # Very low
            top_p=0.9,
            stop=None # Remove stop tokens - might be cutting off response
        )

        result = output['choices'][0]['message']['content'].strip()
        execution_time = time.time() - start_time

        if not result:
            result = "[ERROR: Model returned empty response]"

        # Extract JSON from response
        extracted_json = extract_json(result)
        json_status = "✓ Valid JSON extracted" if extracted_json else "✗ No valid JSON found"

        # Print and save the response
        print(f"\n{'='*70}")
        print(f"RESPONSE #{prompt_num} ({category})")
        print(f"{'='*70}")
        print(f"Prompt: {prompt}")
        print(f"{'-'*70}")
        print(f"Response:\n{result}")
        print(f"{'-'*70}")
        print(f"Extracted JSON ({json_status}):")
        if extracted_json:
            print(json.dumps(extracted_json, indent=2))
        else:
            print("None")
        print(f"{'='*70}")
        print(f"Execution time: {execution_time:.3f}s\n")

        # Append to responses file
        with open(responses_file, 'a') as f:
            f.write(f"\n{'='*70}\n")
            f.write(f"RESPONSE #{prompt_num} ({category})\n")
            f.write(f"{'='*70}\n")
            f.write(f"Prompt: {prompt}\n")
            f.write(f"{'-'*70}\n")
            f.write(f"Response:\n{result}\n")
            f.write(f"{'-'*70}\n")
            f.write(f"Extracted JSON ({json_status}):\n")
            if extracted_json:
                f.write(json.dumps(extracted_json, indent=2) + "\n")
            else:
                f.write("None\n")
            f.write(f"{'='*70}\n")
            f.write(f"Execution time: {execution_time:.3f}s\n\n")

        return {
            "prompt_num": prompt_num,
            "category": category,
            "prompt": prompt,
            "execution_time": execution_time,
            "output_length": len(result),
            "response": result,
            "extracted_json": extracted_json,
            "json_valid": extracted_json is not None,
            "status": "success"
        }

    except Exception as e:
        execution_time = time.time() - start_time
        print(f"✗ Failed on prompt {prompt_num}: {str(e)}")
        return {
            "prompt_num": prompt_num,
            "category": category,
            "prompt": prompt,
            "execution_time": execution_time,
            "output_length": 0,
            "response": "",
            "status": f"failed: {str(e)}"
        }

def calculate_statistics(results, category=None):
    """Calculate statistics for execution times"""
    if category:
        times = [r["execution_time"] for r in results if r["category"] == category and r["status"] == "success"]
    else:
        times = [r["execution_time"] for r in results if r["status"] == "success"]
    
    if not times:
        return {"avg": 0, "min": 0, "max": 0, "count": 0, "median": 0, "stdev": 0}
    
    return {
        "avg": statistics.mean(times),
        "min": min(times),
        "max": max(times),
        "median": statistics.median(times),
        "stdev": statistics.stdev(times) if len(times) > 1 else 0,
        "count": len(times)
    }

def print_statistics(stats, category_name):
    """Print statistics in formatted way"""
    print(f"\n{category_name}:")
    print(f"  Count:   {stats['count']}")
    print(f"  Average: {stats['avg']:.3f}s")
    print(f"  Median:  {stats['median']:.3f}s")
    print(f"  Min:     {stats['min']:.3f}s")
    print(f"  Max:     {stats['max']:.3f}s")
    print(f"  StdDev:  {stats['stdev']:.3f}s")

def main():
    print("\n" + "=" * 70)
    print("ORCHESTRATOR MODEL BENCHMARKING")
    print("Model: microsoft/Phi-3.5-mini-instruct")
    print("Total Prompts: 100")
    print("Categories: Easy, Medium, Hard, Very Hard (based on decomposition complexity)")
    print("=" * 70)

    # Create benchmark directory
    benchmark_dir = "model/benchmark"
    os.makedirs(benchmark_dir, exist_ok=True)

    # Create responses file inside benchmark folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    responses_file = os.path.join(benchmark_dir, f"model_responses_{timestamp}.txt")
    json_file = os.path.join(benchmark_dir, f"extracted_jsons_{timestamp}.jsonl")

    # Initialize responses file
    with open(responses_file, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("ORCHESTRATOR MODEL RESPONSES\n")
        f.write("Model: microsoft/Phi-3.5-mini-instruct\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n")

    print(f"\nResponses will be saved to: {responses_file}\n")

    # Load model
    llm = load_model()

    # Run benchmarks
    results = []
    prompt_num = 1

    for category, prompts in PROMPTS.items():
        print(f"\n{'=' * 70}")
        print(f"Testing Category: {category.upper()} ({len(prompts)} prompts)")
        print(f"{'=' * 70}")

        for prompt in prompts:
            print(f"[{prompt_num}/100] {category}: ", end="", flush=True)

            result = run_inference(llm, prompt, category, prompt_num, responses_file)
            results.append(result)

            # Append extracted JSON to JSONL file
            if result["status"] == "success" and result.get("extracted_json"):
                with open(json_file, 'a') as jf:
                    json_entry = {
                        "prompt_num": prompt_num,
                        "category": category,
                        "prompt": prompt,
                        "extracted_json": result["extracted_json"]
                    }
                    jf.write(json.dumps(json_entry) + "\n")

            if result["status"] == "success":
                print(f"✓ {result['execution_time']:.3f}s")
            else:
                print(f"✗ Failed")

            prompt_num += 1

    # Save results to JSON inside benchmark folder
    filename = os.path.join(benchmark_dir, f"orchestrator_benchmark_{timestamp}.json")

    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n{'=' * 70}")
    print(f"Results saved to: {filename}")
    print(f"{'=' * 70}")
    
    # Calculate and print statistics
    print(f"\n{'=' * 70}")
    print("BENCHMARK STATISTICS")
    print(f"{'=' * 70}")
    
    # Per-category statistics
    for category in PROMPTS.keys():
        stats = calculate_statistics(results, category)
        print_statistics(stats, f"{category.upper()} Category")
    
    # Overall statistics
    overall_stats = calculate_statistics(results)
    print(f"\n{'=' * 70}")
    print_statistics(overall_stats, "OVERALL")
    print(f"{'=' * 70}\n")
    
    # Calculate JSON extraction success rate
    json_valid_count = len([r for r in results if r.get("json_valid", False)])
    json_success_rate = (json_valid_count / len(results)) * 100 if results else 0

    # Save statistics summary
    stats_summary = {
        "timestamp": timestamp,
        "model": "microsoft/Phi-3.5-mini-instruct",
        "total_prompts": len(results),
        "successful": len([r for r in results if r["status"] == "success"]),
        "failed": len([r for r in results if r["status"] != "success"]),
        "json_valid": json_valid_count,
        "json_success_rate": f"{json_success_rate:.1f}%",
        "categories": {
            category: calculate_statistics(results, category)
            for category in PROMPTS.keys()
        },
        "overall": overall_stats
    }

    print(f"\nJSON Extraction: {json_valid_count}/{len(results)} ({json_success_rate:.1f}%)")
    print(f"Extracted JSONs saved to: {json_file}")
    
    stats_filename = os.path.join(benchmark_dir, f"orchestrator_stats_{timestamp}.json")
    with open(stats_filename, 'w') as f:
        json.dump(stats_summary, f, indent=2)

    print(f"Statistics saved to: {stats_filename}\n")

    # Append results to benchmark text file
    append_to_benchmark_file(stats_summary, timestamp)

def append_to_benchmark_file(stats_summary, timestamp):
    """Append benchmark results to a text file in benchmark directory"""
    # Create benchmark directory if it doesn't exist
    benchmark_dir = "benchmark"
    os.makedirs(benchmark_dir, exist_ok=True)

    # Path to the results file
    results_file = os.path.join(benchmark_dir, "benchmark_results.txt")

    # Format the results as human-readable text
    result_text = f"""
{'=' * 80}
BENCHMARK RUN - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
{'=' * 80}
Model: {stats_summary['model']}
Total Prompts: {stats_summary['total_prompts']}
Successful: {stats_summary['successful']}
Failed: {stats_summary['failed']}

{'─' * 80}
CATEGORY STATISTICS
{'─' * 80}
"""

    # Add per-category statistics
    for category, stats in stats_summary['categories'].items():
        result_text += f"""
{category.upper()} Category:
  Count:           {stats['count']} prompts
  Average Time:    {stats['avg']:.3f}s
  Median Time:     {stats['median']:.3f}s
  Min Time:        {stats['min']:.3f}s
  Max Time:        {stats['max']:.3f}s
  Std Deviation:   {stats['stdev']:.3f}s
"""

    # Add overall statistics
    overall = stats_summary['overall']
    result_text += f"""
{'─' * 80}
OVERALL STATISTICS
{'─' * 80}
  Total Successful: {overall['count']} prompts
  Average Time:     {overall['avg']:.3f}s
  Median Time:      {overall['median']:.3f}s
  Min Time:         {overall['min']:.3f}s
  Max Time:         {overall['max']:.3f}s
  Std Deviation:    {overall['stdev']:.3f}s

{'=' * 80}

"""

    # Append to file
    with open(results_file, 'a') as f:
        f.write(result_text)

    print(f"{'=' * 70}")
    print(f"Results appended to: {results_file}")
    print(f"{'=' * 70}\n")

if __name__ == "__main__":
    main()