# Advanced Architecture AI Multi-Agent System (AI-MAS) Project

## Overview
This workspace contains a Math Agent benchmarking system that evaluates the performance of quantized language models on mathematical reasoning tasks. The project focuses on testing DeepSeek-R1-Distill-Qwen-1.5B model in GGUF format for mathematical computations.

## Project Structure

```
arch-ai-mas/
├── Advanced-Arch.-AI-MAS-Project/
│   └── model/
│       ├── main.py                 # Main benchmarking script
│       ├── quan.py                 # GGUF conversion utilities
│       ├── download_model.py       # Model download script
│       └── benchmark/              # Benchmark results and statistics
│           ├── accuracy.json
│           ├── benchmark_results.txt
│           └── math_agent_stats_*.json
├── venv/                           # Python virtual environment
└── requirements.txt                # Python dependencies
```

## Features

- **Math Agent Benchmarking**: Tests language models on 50 mathematical prompts across two difficulty categories:
  - **Easy**: Basic arithmetic, factorials, percentages, simple calculations
  - **Medium**: Statistics, geometry, probability, multi-step problems

- **Model Support**:
  - DeepSeek-R1-Distill-Qwen-1.5B (GGUF Q4_K_M quantized format)
  - GGUF conversion tools for model quantization

- **Performance Metrics**:
  - Execution time per prompt
  - Statistical analysis (average, median, min, max, standard deviation)
  - Category-based performance comparison
  - Success/failure tracking

## Requirements

- Python 3.10+
- PyTorch (CPU version)
- Transformers >= 4.30.0
- llama-cpp-python
- Additional dependencies in [requirements.txt](requirements.txt)

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the model (if needed) or convert your own using [quan.py](Advanced-Arch.-AI-MAS-Project/model/quan.py)

## Usage

Run the math agent benchmark:
```bash
cd Advanced-Arch.-AI-MAS-Project/model
python main.py
```

Results will be saved in the [benchmark/](Advanced-Arch.-AI-MAS-Project/model/benchmark/) directory with timestamped files containing:
- Individual responses
- JSON formatted results
- Statistical summaries

## Output Files

- `math_agent_responses_*.txt`: Detailed responses for each prompt
- `math_agent_benchmark_*.json`: Complete benchmark results in JSON format
- `math_agent_stats_*.json`: Statistical summary of performance
- `benchmark_results.txt`: Aggregated results across runs

## Notes

- The system uses CPU-based inference with 2 threads
- Model runs with low temperature (0.1) for deterministic mathematical outputs
- Context window: 2048 tokens
- Maximum output: 256 tokens per response
