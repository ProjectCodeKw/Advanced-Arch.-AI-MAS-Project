"""
Text Agent Benchmarking Script
Benchmarks TinyLlama-1.1B-Chat GGUF on 50 text processing and reasoning prompts
Categorizes by reasoning complexity: Easy, Medium
"""

import time
import json
import statistics
from datetime import datetime
import os
from llama_cpp import Llama

# Prompts categorized by REASONING complexity
PROMPTS = {
    "easy": [
        # Simple text processing and basic reasoning tasks
        "Summarize this sentence in 5 words: The quick brown fox jumps over the lazy dog",
        "What is the main topic of this text: Climate change affects global weather patterns",
        "Identify the sentiment: I absolutely loved the movie, it was amazing!",
        "Count the words in this sentence: Artificial intelligence is transforming technology",
        "What emotion does this express: I'm so frustrated with this situation",
        "Is this statement positive or negative: The service was terrible and slow",
        "Extract the key verb: The scientists discovered a new species in the rainforest",
        "What is the tone: Please consider my request at your earliest convenience",
        "Identify the subject: The ancient pyramids stand as monuments to human achievement",
        "Classify this as fact or opinion: The Earth orbits around the Sun",
        "What is the purpose: Click here to subscribe to our newsletter",
        "Detect the language style: Yo, what's up? Let's hang out later",
        "Is this formal or informal: I hope this email finds you well",
        "What is the main idea: Regular exercise improves both physical and mental health",
        "Identify the audience: This bedtime story features talking animals and magic",
        "Extract the location mentioned: We visited the Eiffel Tower in Paris last summer",
        "What is the intent: Could you please help me with this problem?",
        "Classify the genre: Once upon a time in a faraway kingdom",
        "Identify the tense: She will travel to Japan next month",
        "What is the mood: The dark clouds gathered ominously over the horizon",
        "Extract the time reference: The meeting is scheduled for 3 PM tomorrow",
        "Is this a question or statement: Where are my keys",
        "Identify the writing style: Furthermore, the data suggests a significant correlation",
        "What is the context: Add salt and pepper to taste, then simmer for 20 minutes",
        "Classify the message type: URGENT: Your account will be suspended unless you act now"
    ],
    
    "medium": [
        # More complex reasoning, inference, and multi-step text analysis
        "Compare and contrast: Democracy vs. Autocracy in terms of citizen participation",
        "Explain the logical flaw: If it rains, the ground is wet. The ground is wet, therefore it rained",
        "Infer the relationship: John gave Mary the book. What can you conclude about ownership?",
        "Identify the implicit assumption: We should hire more staff because we're too busy",
        "Analyze the argument structure: Smoking causes cancer. Cancer is deadly. Therefore, smoking is deadly",
        "What is the underlying message: Actions speak louder than words",
        "Determine cause and effect: The plant died after I forgot to water it for two weeks",
        "Identify the bias: Our product is clearly superior to all competitors in every way",
        "Resolve the ambiguity: I saw the man with the telescope. Who has the telescope?",
        "Infer missing information: She scored 95%, 87%, and 92% on her first three tests. Predict her final grade",
        "Analyze perspective: From a teacher's viewpoint, describe homework. Now from a student's viewpoint",
        "Identify the paradox: This statement is false",
        "Determine credibility: An anonymous blog claims a miracle cure. Should you trust it?",
        "Explain the analogy: Finding a job is like fishing. Explain the comparison",
        "Detect circular reasoning: The Bible is true because it says so in the Bible",
        "Infer character motivation: Despite being offered money, she refused. What does this suggest?",
        "Analyze tone shift: I appreciate your concern. However, this matter is closed",
        "Identify the fallacy: Everyone is buying this phone, so it must be the best",
        "Determine implications: If all A are B, and all B are C, what can we conclude about A and C?",
        "Reconstruct the argument: Here's the conclusion: We need change. What might the premises be?",
        "Evaluate evidence strength: One study shows X, but five studies show Y. What's stronger?",
        "Identify the metaphor and explain: Time is money",
        "Analyze the dilemma: Save one person you love or five strangers. What are the ethical considerations?",
        "Determine intent vs. impact: She meant well, but her words hurt. Analyze this",
        "Synthesize information: Given these facts, what pattern emerges? Fact 1: Sales drop in winter. Fact 2: It's a seasonal product. Fact 3: Competitors face the same issue"
    ]
}

def load_model():
    """Load TinyLlama-1.1B-Chat GGUF model"""
    MODEL_PATH = "tinyllama-1.1b-chat-v1.0.Q3_K_M.gguf"

    print(f"Loading TinyLlama-1.1B-Chat Q3_K_M from {MODEL_PATH}...")
    print("=" * 70)

    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=2,  # Use 2 CPU threads for text agent
        n_gpu_layers=0,
        verbose=False
    )

    print("✓ Model loaded successfully")
    print("=" * 70)
    return llm

def run_inference(llm, prompt, category, prompt_num, responses_file):
    """Run single inference and measure execution time"""

    # Format prompt for chat model
    formatted_prompt = f"""<|system|>
You are a helpful AI assistant specialized in text analysis and reasoning.</s>
<|user|>
{prompt}</s>
<|assistant|>
"""

    start_time = time.time()

    try:
        output = llm(
            formatted_prompt,
            max_tokens=200,
            temperature=0.3,
            top_p=0.9,
            stop=["</s>", "<|user|>", "<|system|>"],
            echo=False
        )

        generated_response = output['choices'][0]['text'].strip()
        execution_time = time.time() - start_time

        # Print and save the response
        print(f"\n{'='*70}")
        print(f"RESPONSE #{prompt_num} ({category})")
        print(f"{'='*70}")
        print(f"Prompt: {prompt}")
        print(f"{'-'*70}")
        print(f"Response:\n{generated_response}")
        print(f"{'='*70}")
        print(f"Execution time: {execution_time:.3f}s\n")

        # Append to responses file
        with open(responses_file, 'a') as f:
            f.write(f"\n{'='*70}\n")
            f.write(f"RESPONSE #{prompt_num} ({category})\n")
            f.write(f"{'='*70}\n")
            f.write(f"Prompt: {prompt}\n")
            f.write(f"{'-'*70}\n")
            f.write(f"Response:\n{generated_response}\n")
            f.write(f"{'='*70}\n")
            f.write(f"Execution time: {execution_time:.3f}s\n\n")

        return {
            "prompt_num": prompt_num,
            "category": category,
            "prompt": prompt,
            "execution_time": execution_time,
            "output_length": len(generated_response),
            "generated_response": generated_response,
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
            "generated_response": "",
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
    print("TEXT AGENT BENCHMARKING")
    print("Model: TinyLlama-1.1B-Chat (Q3_K_M GGUF)")
    print("Total Prompts: 50")
    print("Categories: Easy, Medium (based on reasoning complexity)")
    print("=" * 70)

    # Create benchmark directory
    benchmark_dir = "benchmark"
    os.makedirs(benchmark_dir, exist_ok=True)

    # Create responses file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    responses_file = os.path.join(benchmark_dir, f"text_agent_responses_{timestamp}.txt")

    # Initialize responses file
    with open(responses_file, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("TEXT AGENT RESPONSES\n")
        f.write("Model: TinyLlama-1.1B-Chat (Q3_K_M GGUF)\n")
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
    filename = os.path.join(benchmark_dir, f"text_agent_benchmark_{timestamp}.json")

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
        "model": "TinyLlama-1.1B-Chat Q3_K_M GGUF",
        "total_prompts": len(results),
        "successful": len([r for r in results if r["status"] == "success"]),
        "failed": len([r for r in results if r["status"] != "success"]),
        "categories": {
            category: calculate_statistics(results, category)
            for category in PROMPTS.keys()
        },
        "overall": overall_stats
    }
    
    stats_filename = os.path.join(benchmark_dir, f"text_agent_stats_{timestamp}.json")
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
TEXT AGENT BENCHMARK RUN - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
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