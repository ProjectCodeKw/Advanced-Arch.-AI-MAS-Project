# Code1

## Overview
Benchmarking system for `bigcode/tiny_starcoder_py` model on Python code generation tasks.

## Structure
- `model/main.py` - Main benchmarking script for code generation prompts
- `model/quan.py` - Model conversion script (HuggingFace to GGUF format)
- `model/download_model.py` - Model download utility
- `model/benchmark/` - Benchmark results and metrics

## Usage
Run benchmarks: `python model/main.py`


# Code2

## Overview
Deployment folder for the quantized `tiny_starcoder_py` model.

## Structure
- `model/tiny_starcoder_py_fp16.gguf` - Quantized model file (FP16 format)
- `model/benchmark/` - Benchmark results and performance metrics

## Usage
Load the GGUF model using llama-cpp-python or compatible inference engines.
