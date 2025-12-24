"""
Code Agent Benchmarking Script
Benchmarks bigcode/tiny_starcoder_py GGUF on 50 Python code generation prompts
Categorizes by code complexity: Easy, Medium
"""

import time
import json
import statistics
from datetime import datetime
import os
from llama_cpp import Llama

# Prompts categorized by CODE complexity
PROMPTS = {
    "easy": [
        # Simple, single-function tasks
        "Write a Python function to calculate factorial of a number",
        "Create a function to reverse a string",
        "Write code to check if a number is prime",
        "Generate a function to find the maximum in a list",
        "Write a function to calculate the sum of all elements in a list",
        "Create code to convert Celsius to Fahrenheit",
        "Write a function to check if a string is a palindrome",
        "Generate code to count vowels in a string",
        "Write a function to remove duplicates from a list",
        "Create code to find the length of a string without using len()",
        "Write a function to calculate the average of numbers in a list",
        "Generate code to swap two variables",
        "Write a function to check if a number is even or odd",
        "Create code to find the minimum element in a list",
        "Write a function to capitalize first letter of each word",
        "Generate code to check if a list is empty",
        "Write a function to multiply all elements in a list",
        "Create code to convert a string to uppercase",
        "Write a function to calculate the power of a number",
        "Generate code to find the index of an element in a list",
        "Write a function to check if a year is a leap year",
        "Create code to concatenate two strings",
        "Write a function to count occurrences of a character in a string",
        "Generate code to create a list of even numbers from 1 to 20",
        "Write a function to calculate the absolute value of a number"
    ],
    
    "medium": [
        # More complex tasks requiring multiple operations or data structures
        "Write a function to implement bubble sort algorithm",
        "Create code to find the second largest number in a list",
        "Write a function to merge two sorted lists",
        "Generate code to implement a stack using a list",
        "Write a function to find all prime numbers up to n",
        "Create code to reverse words in a sentence",
        "Write a function to check if two strings are anagrams",
        "Generate code to implement binary search",
        "Write a function to find common elements in two lists",
        "Create code to rotate a list by n positions",
        "Write a function to flatten a nested list",
        "Generate code to implement a queue using two stacks",
        "Write a function to find the longest word in a sentence",
        "Create code to remove all whitespace from a string",
        "Write a function to check if parentheses are balanced",
        "Generate code to find the intersection of two sets",
        "Write a function to calculate Fibonacci sequence up to n terms",
        "Create code to sort a dictionary by values",
        "Write a function to remove all non-alphanumeric characters",
        "Generate code to find the mode of a list",
        "Write a function to convert a decimal number to binary",
        "Create code to implement selection sort",
        "Write a function to find all substrings of a string",
        "Generate code to transpose a matrix",
        "Write a function to find the GCD of two numbers using Euclidean algorithm"
    ]
}

def load_model():
    """Load tiny_starcoder_py GGUF model"""
    MODEL_PATH = "tiny_starcoder_py_fp16.gguf"  # or tiny_starcoder_py_Q4_K_M.gguf if you quantized it

    print(f"Loading bigcode/tiny_starcoder_py GGUF from {MODEL_PATH}...")
    print("=" * 70)

    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=2,  # Use 2 CPU threads for code agent
        n_gpu_layers=0,
        verbose=False
    )

    print("✓ Model loaded successfully")
    print("=" * 70)
    return llm

def run_inference(llm, prompt, category, prompt_num, responses_file):
    """Run single inference and measure execution time"""

    # Format prompt for code generation
    formatted_prompt = f"""# Task: {prompt}
# Python code:
"""

    start_time = time.time()

    try:
        output = llm(
            formatted_prompt,
            max_tokens=256,
            temperature=0.2,
            top_p=0.95,
            stop=["# Task:", "\n\n\n"],
            echo=False
        )

        generated_code = output['choices'][0]['text'].strip()
        execution_time = time.time() - start_time

        # Print and save the response
        print(f"\n{'='*70}")
        print(f"RESPONSE #{prompt_num} ({category})")
        print(f"{'='*70}")
        print(f"Prompt: {prompt}")
        print(f"{'-'*70}")
        print(f"Generated Code:\n{generated_code}")
        print(f"{'='*70}")
        print(f"Execution time: {execution_time:.3f}s\n")

        # Append to responses file
        with open(responses_file, 'a') as f:
            f.write(f"\n{'='*70}\n")
            f.write(f"RESPONSE #{prompt_num} ({category})\n")
            f.write(f"{'='*70}\n")
            f.write(f"Prompt: {prompt}\n")
            f.write(f"{'-'*70}\n")
            f.write(f"Generated Code:\n{generated_code}\n")
            f.write(f"{'='*70}\n")
            f.write(f"Execution time: {execution_time:.3f}s\n\n")

        return {
            "prompt_num": prompt_num,
            "category": category,
            "prompt": prompt,
            "execution_time": execution_time,
            "output_length": len(generated_code),
            "generated_code": generated_code,
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
            "generated_code": "",
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
    print("CODE AGENT BENCHMARKING")
    print("Model: bigcode/tiny_starcoder_py (GGUF)")
    print("Total Prompts: 50")
    print("Categories: Easy, Medium (based on code complexity)")
    print("=" * 70)

    # Create benchmark directory
    benchmark_dir = "benchmark"
    os.makedirs(benchmark_dir, exist_ok=True)

    # Create responses file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    responses_file = os.path.join(benchmark_dir, f"code_agent_responses_{timestamp}.txt")

    # Initialize responses file
    with open(responses_file, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("CODE AGENT RESPONSES\n")
        f.write("Model: bigcode/tiny_starcoder_py (GGUF)\n")
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
            print(f"[{prompt_num}/50] {category}: ", end="", flush=True)

            result = run_inference(llm, prompt, category, prompt_num, responses_file)
            results.append(result)

            if result["status"] == "success":
                print(f"✓ {result['execution_time']:.3f}s")
            else:
                print(f"✗ Failed")

            prompt_num += 1

    # Save results to JSON
    filename = os.path.join(benchmark_dir, f"code_agent_benchmark_{timestamp}.json")

    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n{'=' * 70}")
    print(f"Results saved to: {filename}")
    print(f"{'=' * 70}")
    
    # Calculate and print statistics
    print(f"\n{'=' * 70}")
    print("BENCHMARK STATISTICS")
    print(f"{'=' * 70}")
    
    for category in PROMPTS.keys():
        stats = calculate_statistics(results, category)
        print_statistics(stats, f"{category.upper()} Category")
    
    overall_stats = calculate_statistics(results)
    print(f"\n{'=' * 70}")
    print_statistics(overall_stats, "OVERALL")
    print(f"{'=' * 70}\n")
    
    # Save statistics summary
    stats_summary = {
        "timestamp": timestamp,
        "model": "bigcode/tiny_starcoder_py (GGUF)",
        "total_prompts": len(results),
        "successful": len([r for r in results if r["status"] == "success"]),
        "failed": len([r for r in results if r["status"] != "success"]),
        "categories": {
            category: calculate_statistics(results, category)
            for category in PROMPTS.keys()
        },
        "overall": overall_stats
    }
    
    stats_filename = os.path.join(benchmark_dir, f"code_agent_stats_{timestamp}.json")
    with open(stats_filename, 'w') as f:
        json.dump(stats_summary, f, indent=2)

    print(f"Statistics saved to: {stats_filename}\n")
    append_to_benchmark_file(stats_summary, timestamp)

def append_to_benchmark_file(stats_summary, timestamp):
    """Append benchmark results to a text file in benchmark directory"""
    benchmark_dir = "benchmark"
    os.makedirs(benchmark_dir, exist_ok=True)
    results_file = os.path.join(benchmark_dir, "benchmark_results.txt")

    result_text = f"""
{'=' * 80}
CODE AGENT BENCHMARK RUN - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
{'=' * 80}
Model: {stats_summary['model']}
Total Prompts: {stats_summary['total_prompts']}
Successful: {stats_summary['successful']}
Failed: {stats_summary['failed']}

{'─' * 80}
CATEGORY STATISTICS
{'─' * 80}
"""

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

    with open(results_file, 'a') as f:
        f.write(result_text)

    print(f"{'=' * 70}")
    print(f"Results appended to: {results_file}")
    print(f"{'=' * 70}\n")

if __name__ == "__main__":
    main()