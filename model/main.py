"""
Translation Agent Benchmarking Script
Benchmarks Helsinki-NLP/opus-mt-en-ar on 50 English to Arabic translations
Categorizes by sentence complexity: Easy, Medium
"""

import time
import json
import statistics
from datetime import datetime
import os
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Prompts categorized by SENTENCE complexity
PROMPTS = {
    "easy": [
        # Simple, short sentences with common vocabulary
        "Hello, how are you?",
        "My name is Ahmed.",
        "The weather is nice today.",
        "I like to read books.",
        "She is a good student.",
        "We live in a big city.",
        "The food is delicious.",
        "Thank you very much.",
        "I am learning Arabic.",
        "He works in a hospital.",
        "The car is red.",
        "I have two brothers.",
        "The school is closed today.",
        "She speaks English well.",
        "Water is very important.",
        "The sun is shining.",
        "I need help with homework.",
        "They are playing football.",
        "The book is on the table.",
        "I love my family.",
        "Coffee is ready.",
        "The door is open.",
        "He has a new phone.",
        "The children are happy.",
        "Good morning everyone."
    ],
    
    "medium": [
        # Longer, more complex sentences with varied vocabulary
        "The government announced new policies to improve the education system.",
        "Scientists have discovered a potential cure for the disease.",
        "Climate change is affecting global weather patterns significantly.",
        "The company's revenue increased by twenty percent this quarter.",
        "Technology has transformed the way we communicate with each other.",
        "The conference will discuss sustainable development and environmental issues.",
        "Students must complete their assignments before the deadline.",
        "The research team published their findings in a prestigious journal.",
        "Economic growth depends on investment in infrastructure and innovation.",
        "The hospital introduced advanced medical equipment for better diagnosis.",
        "International cooperation is essential for addressing global challenges.",
        "The museum exhibits artifacts from ancient civilizations.",
        "Renewable energy sources are becoming more cost-effective.",
        "The software update includes several security improvements.",
        "Cultural diversity enriches our society and promotes understanding.",
        "The project requires careful planning and coordination.",
        "Financial markets responded positively to the central bank's decision.",
        "Online learning platforms have expanded access to education.",
        "The investigation revealed significant corruption in the department.",
        "Urban planning should prioritize public transportation and green spaces.",
        "The treaty aims to strengthen diplomatic relations between nations.",
        "Cybersecurity threats are evolving and becoming more sophisticated.",
        "The pharmaceutical industry is developing new treatments for chronic diseases.",
        "Social media has revolutionized marketing and customer engagement.",
        "Environmental regulations are necessary to protect natural resources."
    ]
}

def load_model():
    """Load Helsinki-NLP English to Arabic translation model"""
    MODEL_PATH = "./opus-mt-en-ar"  # Local folder
    
    print(f"Loading translation model from {MODEL_PATH}...")
    print("=" * 70)
    
    # Load model and tokenizer from local folder
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_PATH,
        local_files_only=True  # Don't download
    )
    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_PATH,
        local_files_only=True  # Don't download
    )
    
    # Create pipeline
    translator = pipeline(
        "translation",
        model=model,
        tokenizer=tokenizer,
        device=-1  # CPU
    )
    
    print("✓ Model loaded successfully")
    print("=" * 70)
    return translator

def run_inference(translator, prompt, category, prompt_num, responses_file):
    """Run single inference and measure execution time"""
    
    start_time = time.time()
    
    try:
        # Translate
        result = translator(prompt, max_length=512)
        translation = result[0]['translation_text']
        
        execution_time = time.time() - start_time
        
        # Print and save the response
        print(f"\n{'='*70}")
        print(f"TRANSLATION #{prompt_num} ({category})")
        print(f"{'='*70}")
        print(f"English:  {prompt}")
        print(f"{'-'*70}")
        print(f"Arabic:   {translation}")
        print(f"{'='*70}")
        print(f"Execution time: {execution_time:.3f}s\n")
        
        # Append to responses file
        with open(responses_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*70}\n")
            f.write(f"TRANSLATION #{prompt_num} ({category})\n")
            f.write(f"{'='*70}\n")
            f.write(f"English:  {prompt}\n")
            f.write(f"{'-'*70}\n")
            f.write(f"Arabic:   {translation}\n")
            f.write(f"{'='*70}\n")
            f.write(f"Execution time: {execution_time:.3f}s\n\n")
        
        return {
            "prompt_num": prompt_num,
            "category": category,
            "english": prompt,
            "execution_time": execution_time,
            "translation": translation,
            "translation_length": len(translation),
            "status": "success"
        }
        
    except Exception as e:
        execution_time = time.time() - start_time
        print(f"✗ Failed on prompt {prompt_num}: {str(e)}")
        return {
            "prompt_num": prompt_num,
            "category": category,
            "english": prompt,
            "execution_time": execution_time,
            "translation": "",
            "translation_length": 0,
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
    print("TRANSLATION AGENT BENCHMARKING")
    print("Model: Helsinki-NLP/opus-mt-en-ar (~300 MB)")
    print("Task: English to Arabic Translation")
    print("Device: CPU (1GB RAM, 2 cores)")
    print("Total Prompts: 50")
    print("Categories: Easy, Medium (based on sentence complexity)")
    print("=" * 70)
    
    # Create benchmark directory
    benchmark_dir = "benchmark"
    os.makedirs(benchmark_dir, exist_ok=True)
    
    # Create responses file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    responses_file = os.path.join(benchmark_dir, f"translation_agent_responses_{timestamp}.txt")
    
    # Initialize responses file
    with open(responses_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("TRANSLATION AGENT RESPONSES\n")
        f.write("Model: Helsinki-NLP/opus-mt-en-ar\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n")
    
    print(f"\nResponses will be saved to: {responses_file}\n")
    
    # Load model
    translator = load_model()
    
    # Run benchmarks
    results = []
    prompt_num = 1
    
    for category, prompts in PROMPTS.items():
        print(f"\n{'=' * 70}")
        print(f"Testing Category: {category.upper()} ({len(prompts)} prompts)")
        print(f"{'=' * 70}")
        
        for prompt in prompts:
            print(f"[{prompt_num}/50] {category}: ", end="", flush=True)
            
            result = run_inference(translator, prompt, category, prompt_num, responses_file)
            results.append(result)
            
            if result["status"] == "success":
                print(f"✓ {result['execution_time']:.3f}s")
            else:
                print(f"✗ Failed")
            
            prompt_num += 1
    
    # Save results to JSON
    filename = os.path.join(benchmark_dir, f"translation_agent_benchmark_{timestamp}.json")
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
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
        "model": "Helsinki-NLP/opus-mt-en-ar",
        "task": "English to Arabic Translation",
        "device": "CPU (1GB RAM, 2 cores)",
        "total_prompts": len(results),
        "successful": len([r for r in results if r["status"] == "success"]),
        "failed": len([r for r in results if r["status"] != "success"]),
        "categories": {
            category: calculate_statistics(results, category)
            for category in PROMPTS.keys()
        },
        "overall": overall_stats
    }
    
    stats_filename = os.path.join(benchmark_dir, f"translation_agent_stats_{timestamp}.json")
    with open(stats_filename, 'w', encoding='utf-8') as f:
        json.dump(stats_summary, f, indent=2, ensure_ascii=False)
    
    print(f"Statistics saved to: {stats_filename}\n")
    append_to_benchmark_file(stats_summary, timestamp)

def append_to_benchmark_file(stats_summary, timestamp):
    """Append benchmark results to a text file in benchmark directory"""
    benchmark_dir = "benchmark"
    os.makedirs(benchmark_dir, exist_ok=True)
    results_file = os.path.join(benchmark_dir, "benchmark_results.txt")
    
    result_text = f"""
{'=' * 80}
TRANSLATION AGENT BENCHMARK RUN - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
{'=' * 80}
Model: {stats_summary['model']}
Task: {stats_summary['task']}
Device: {stats_summary['device']}
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
    
    with open(results_file, 'a', encoding='utf-8') as f:
        f.write(result_text)
    
    print(f"{'=' * 70}")
    print(f"Results appended to: {results_file}")
    print(f"{'=' * 70}\n")

if __name__ == "__main__":
    main()