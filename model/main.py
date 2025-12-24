"""
Math Agent Benchmarking Script
Benchmarks DeepSeek-R1-Distill-Qwen-1.5B (GGUF Q4_K_M) on 50 mathematical calculation prompts
Categorizes by math complexity: Easy, Medium
"""

import time
import json
import statistics
from datetime import datetime
import os
from llama_cpp import Llama

# Prompts categorized by MATH complexity
PROMPTS = {
    "easy": [
        # Basic arithmetic and simple calculations
        "Calculate 25% of 840",
        "What is 15 times 23 plus 45",
        "Find the average of 10, 20, 30, and 40",
        "Calculate the area of a circle with radius 7",
        "What is 2 to the power of 8",
        "Calculate the factorial of 5",
        "Find the square root of 144",
        "What is 100 divided by 4",
        "Calculate 50% of 200",
        "What is the cube of 4",
        "Calculate 3.14 times 5 squared",
        "Find the remainder when 17 is divided by 5",
        "What is the absolute value of -25",
        "Calculate 7 factorial",
        "What is 12 squared",
        "Find 20% of 500",
        "Calculate 8 divided by 2 times 4",
        "What is 99 plus 1",
        "Find the sum of 1 through 10",
        "Calculate 16 to the power of 0.5",
        "What is 45 minus 23",
        "Calculate 6 times 7",
        "Find half of 86",
        "What is 1000 divided by 25",
        "Calculate 9 squared"
    ],
    
    "medium": [
        # More complex calculations and multi-step problems
        "Calculate the variance of the numbers 2, 4, 6, 8, 10",
        "Find the standard deviation of 5, 10, 15, 20, 25",
        "Calculate the median of 3, 7, 2, 9, 5, 1, 8",
        "Find the mode of 2, 3, 3, 4, 4, 4, 5",
        "Calculate the range of 12, 45, 23, 67, 34",
        "What is the greatest common divisor of 48 and 18",
        "Find the least common multiple of 12 and 15",
        "Calculate the slope between points (2,3) and (5,9)",
        "Find the distance between points (0,0) and (3,4)",
        "Calculate the midpoint between (2,5) and (8,13)",
        "What is 5 factorial divided by 3 factorial",
        "Calculate the sum of squares from 1 to 5",
        "Find the geometric mean of 4 and 9",
        "Calculate compound interest: principal 1000, rate 5%, time 2 years",
        "What is the perimeter of a rectangle with length 12 and width 8",
        "Find the volume of a cube with side length 5",
        "Calculate the surface area of a sphere with radius 3",
        "What is sin(30 degrees) in decimal form",
        "Find the hypotenuse of a right triangle with sides 3 and 4",
        "Calculate the discriminant of equation x^2 + 5x + 6 = 0",
        "What is the sum of the arithmetic sequence 2, 5, 8, 11, 14",
        "Find the 10th term in the sequence 3, 6, 12, 24",
        "Calculate the probability of rolling a sum of 7 with two dice",
        "What is 15 choose 3 (combinations)",
        "Find the permutations of 5 items taken 2 at a time"
    ]
}

def load_model():
    """Load DeepSeek-R1-Distill-Qwen-1.5B GGUF Q4_K_M model"""
    MODEL_PATH = "DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf"
    
    print(f"Loading DeepSeek-R1-Distill-Qwen-1.5B (GGUF Q4_K_M) from {MODEL_PATH}...")
    print("=" * 70)
    
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=2,  # Use 2 CPU threads for math agent
        n_gpu_layers=0,
        verbose=False
    )
    
    print("✓ Model loaded successfully")
    print("=" * 70)
    return llm

def run_inference(llm, prompt, category, prompt_num, responses_file):
    """Run single inference and measure execution time"""

    # Format prompt for math calculation - DeepSeek-R1 uses simple Q&A format
    formatted_prompt = f"Question: {prompt}\nAnswer:"

    start_time = time.time()

    try:
        output = llm(
            formatted_prompt,
            max_tokens=256,
            temperature=0.1,  # Very low temperature for deterministic math
            top_p=0.9,
            stop=["Question:", "\n\n"],
            echo=False
        )

        answer = output['choices'][0]['text'].strip()
        execution_time = time.time() - start_time

        # Print and save the response
        print(f"\n{'='*70}")
        print(f"RESPONSE #{prompt_num} ({category})")
        print(f"{'='*70}")
        print(f"Prompt: {prompt}")
        print(f"{'-'*70}")
        print(f"Answer: {answer}")
        print(f"{'='*70}")
        print(f"Execution time: {execution_time:.3f}s\n")

        # Append to responses file
        with open(responses_file, 'a') as f:
            f.write(f"\n{'='*70}\n")
            f.write(f"RESPONSE #{prompt_num} ({category})\n")
            f.write(f"{'='*70}\n")
            f.write(f"Prompt: {prompt}\n")
            f.write(f"{'-'*70}\n")
            f.write(f"Answer: {answer}\n")
            f.write(f"{'='*70}\n")
            f.write(f"Execution time: {execution_time:.3f}s\n\n")

        return {
            "prompt_num": prompt_num,
            "category": category,
            "prompt": prompt,
            "execution_time": execution_time,
            "output_length": len(answer),
            "answer": answer,
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
            "answer": "",
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
    print("MATH AGENT BENCHMARKING")
    print("Model: DeepSeek-R1-Distill-Qwen-1.5B (GGUF Q4_K_M)")
    print("Total Prompts: 50")
    print("Categories: Easy, Medium (based on math complexity)")
    print("=" * 70)

    # Create benchmark directory
    benchmark_dir = "benchmark"
    os.makedirs(benchmark_dir, exist_ok=True)

    # Create responses file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    responses_file = os.path.join(benchmark_dir, f"math_agent_responses_{timestamp}.txt")

    # Initialize responses file
    with open(responses_file, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("MATH AGENT RESPONSES\n")
        f.write("Model: DeepSeek-R1-Distill-Qwen-1.5B (GGUF Q4_K_M)\n")
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
    filename = os.path.join(benchmark_dir, f"math_agent_benchmark_{timestamp}.json")

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
        "model": "DeepSeek-R1-Distill-Qwen-1.5B (GGUF Q4_K_M)",
        "total_prompts": len(results),
        "successful": len([r for r in results if r["status"] == "success"]),
        "failed": len([r for r in results if r["status"] != "success"]),
        "categories": {
            category: calculate_statistics(results, category)
            for category in PROMPTS.keys()
        },
        "overall": overall_stats
    }
    
    stats_filename = os.path.join(benchmark_dir, f"math_agent_stats_{timestamp}.json")
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
MATH AGENT BENCHMARK RUN - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
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