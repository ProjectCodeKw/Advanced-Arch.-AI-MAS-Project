# Decentralized, SLM-Based Orchestration for Resource-Constrained AI Multi Agent Systems

## Overview

This repository implements a decentralized multi-agent system (MAS) architecture that uses Small Language Models (SLMs) for orchestration. The system is designed to operate efficiently on resource-constrained environments, distributing AI workloads across multiple specialized agents.

## Repository Structure

Each branch contains the code for a specific agent's virtual machine. The main components are:

### Branches

- **main**: Primary branch with shared resources and documentation
- **mini-orch**: Contains the Mini Orchestrator implementation

### Mini-Orch (Orchestrator Agent)

Located in `Mini-Orch/`, this is the central orchestration component that:

- **Model**: Uses Microsoft Phi-3.5-mini-instruct (quantized Q4_K_M GGUF format) for efficient inference
- **Task Decomposition**: Routes incoming prompts to appropriate specialized agents based on task type
- **Benchmarking**: Includes evaluation tools for measuring orchestration accuracy across different complexity levels

#### Directory Structure

```
Mini-Orch/
├── model/
│   ├── main.py              # Orchestrator benchmarking script
│   ├── download_model.py    # Model download utilities
│   ├── download_phi35.py    # Phi-3.5 specific downloader
│   ├── phi3-5/              # Model weights directory
│   └── benchmark/           # Benchmark results and test data
├── requirements.txt         # Python dependencies
└── venv/                    # Python virtual environment
```

#### Available Agents

The orchestrator routes tasks to the following specialized agents:

1. **Text and Definitions Agent** (`tasks/text`): Text summarization, explanations, content writing, translation
2. **Code Agent** (`tasks/code`): Code generation (Python, JavaScript, SQL), debugging, API integration
3. **Math Agent** (`tasks/math`): Mathematical calculations, statistical analysis, formula derivation
4. **Image Generator Agent** (`tasks/image`): Image generation from text descriptions

## Dependencies

Key Python packages used:

- `llama-cpp-python`: For running GGUF quantized models
- `transformers`: Hugging Face transformers library
- `torch`: PyTorch (CPU version)
- `accelerate`: Model acceleration utilities
- `huggingface-hub`: Model downloading and management

## Getting Started

1. Clone the repository and checkout the desired branch
2. Navigate to the agent directory (e.g., `Mini-Orch/`)
3. Create and activate the virtual environment
4. Install dependencies: `pip install -r requirements.txt`
5. Download the model using the provided scripts
6. Run the orchestrator or benchmarks

## Benchmarking

The orchestrator includes a comprehensive benchmark suite that tests task decomposition across four complexity levels:

- **Easy**: Clear, single-task prompts
- **Medium**: Multi-task prompts with both independent and dependent operations
- **Hard**: Complex prompts requiring careful task sequencing
- **Very Hard**: Ambiguous or challenging decomposition scenarios

Benchmark results are stored in `Mini-Orch/model/benchmark/`. 