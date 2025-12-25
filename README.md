# Advanced Architecture AI-MAS Project

## Overview
This project is an **Advanced Architecture AI-MAS** (Multi-Agent System) implementation that focuses on benchmarking and evaluating the **TinyLlama-1.1B-Chat** language model in GGUF (GPT-Generated Unified Format) for text processing and reasoning tasks.

## Project Structure

```
Advanced-Arch.-AI-MAS-Project/
├── model/                          # Main model directory
│   ├── main.py                     # Primary benchmarking script
│   ├── download_model.py           # Model download utility
│   ├── quan.py                     # Model quantization script
│   ├── tinyllama-1.1b-chat-v1.0.Q3_K_M.gguf  # Quantized TinyLlama model
│   └── benchmark/                  # Benchmark results and metrics
│       ├── benchmark_results.txt
│       ├── text_agent_benchmark_20251224_185213.json
│       ├── text_agent_responses_20251224_185213.txt
│       └── text_agent_stats_20251224_185213.json
├── .gitignore                      # Git ignore file
└── README.md                       # This file
```

## Component Descriptions

### 1. **main.py** - Text Agent Benchmarking Script
- **Purpose**: Benchmarks the TinyLlama-1.1B-Chat GGUF model on 50 text processing and reasoning prompts
- **Features**:
  - Categorizes prompts by reasoning complexity (Easy, Medium)
  - Easy tasks: Sentiment analysis, text summarization, keyword extraction, tone detection
  - Medium tasks: Complex reasoning, inference, logical analysis, multi-step text analysis
  - Measures performance metrics:
    - Response time per prompt
    - Token generation speed
    - Statistical analysis (mean, median, standard deviation)
- **Output**: JSON and text reports with detailed benchmark statistics

### 2. **download_model.py** - Model Download Utility
- **Purpose**: Downloads the TinyLlama or other language models from Hugging Face
- **Functionality**:
  - Fetches pre-trained models using the `transformers` library
  - Saves model and tokenizer locally for offline use
  - Target model: `bigcode/tiny_starcoder_py` (or similar lightweight models)
- **Usage**: Run before model benchmarking to ensure model is available locally

### 3. **quan.py** - Model Quantization Script
- **Purpose**: Converts Hugging Face models to GGUF format with quantization
- **Process**:
  1. Takes a HuggingFace model directory
  2. Converts to FP16 GGUF format for efficiency
  3. Applies quantization (Q3_K_M in the current setup)
  4. Outputs optimized GGUF files for faster inference
- **Benefits**: 
  - Reduced model size
  - Faster inference on CPU/low-resource devices
  - Maintained model accuracy with minimal loss

### 4. **tinyllama-1.1b-chat-v1.0.Q3_K_M.gguf**
- **Type**: Quantized language model in GGUF format
- **Model**: TinyLlama 1.1B Chat
- **Quantization**: Q3_K_M (3-bit quantization with K-quants)
- **Size**: Significantly reduced from full precision
- **Use**: Used for inference in benchmarking tasks

### 5. **benchmark/** - Benchmark Results Directory
Contains evaluation results from the latest benchmark run (December 24, 2025):

- **benchmark_results.txt**: Human-readable summary of benchmark performance
- **text_agent_benchmark_*.json**: Detailed JSON data with all prompt responses and metrics
- **text_agent_responses_*.txt**: Raw model responses to all benchmark prompts
- **text_agent_stats_*.json**: Statistical analysis (latency, throughput, token speeds)

## Dependencies

The project uses the following libraries:
- `llama-cpp-python`: Python bindings for llama.cpp (GGUF model inference)
- `transformers`: Hugging Face transformers library for model handling
- Standard libraries: `json`, `time`, `statistics`, `datetime`, `os`

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps
```bash
# Clone the repository
git clone <repo-url>
cd Advanced-Arch.-AI-MAS-Project

# Install dependencies
pip install transformers llama-cpp-python

# (Optional) Download model
cd model
python download_model.py

# (Optional) Quantize model to GGUF
python quan.py
```

## Usage

### Running Benchmarks
```bash
cd model
python main.py
```

This will:
1. Load the TinyLlama GGUF model
2. Execute 50 benchmark prompts (25 easy, 25 medium complexity)
3. Measure performance metrics
4. Generate JSON and text reports with results

### Expected Output
- Console logs with real-time progress
- Benchmark JSON with detailed metrics
- Statistics file with performance analysis
- Response file with all model outputs

## Performance Metrics

The benchmark measures:
- **Latency**: Time taken per prompt (milliseconds)
- **Throughput**: Tokens generated per second
- **Success Rate**: Percentage of successful responses
- **Statistical Summary**: Mean, median, std deviation of metrics

## Benchmark Categories

### Easy Prompts (25 tasks)
- Sentiment analysis
- Text summarization
- Keyword extraction
- Tone and style detection
- Subject identification
- Simple fact/opinion classification

### Medium Prompts (25 tasks)
- Logical reasoning and inference
- Relationship analysis
- Assumption identification
- Context comprehension
- Multi-step analysis
- Complex problem-solving

## Git Configuration
The project uses git for version control. Check [.gitignore](.gitignore) for excluded files.

## Key Features of TinyLlama-1.1B
- **Lightweight**: Only 1.1 billion parameters
- **Fast**: Suitable for CPU inference
- **Quantized**: Q3_K_M quantization reduces size further
- **Chat-Optimized**: Fine-tuned for conversational tasks
- **Offline**: Can run completely offline after model download

## Future Enhancements
- Add more reasoning complexity levels (Hard, Expert)
- Implement multi-turn conversation benchmarks
- Support for additional model architectures
- API endpoint deployment
- Performance comparison with other lightweight models
- Integration with FastAPI for production serving

## Notes
- This is an advanced architecture project focusing on efficient AI inference
- The MAS (Multi-Agent System) aspect can be extended for collaborative agent benchmarking
- All benchmarks are conducted on the quantized model for efficient execution

## License
[Add appropriate license information]

## Contact
For questions or contributions, please refer to the project repository.

---

**Last Updated**: December 24, 2025
**Project Status**: Active Development
