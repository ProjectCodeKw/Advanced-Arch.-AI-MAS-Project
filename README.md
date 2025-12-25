# Advanced Arch. AI MAS Project

A lightweight workspace focused on benchmarking a local translation model (Helsinki-NLP `opus-mt-en-ar`) and organizing related artifacts. It also includes utilities for model downloads and format conversion.

## Project Structure

```
Advanced-Arch.-AI-MAS-Project/
├── requirements.txt                # Python dependencies
├── model/
│   ├── main.py                     # Translation agent benchmarking (EN → AR)
│   ├── download_model.py           # Example script to fetch a Diffusers model
│   ├── quan.py                     # GGUF conversion workflow (llama.cpp)
│   ├── benchmark/                  # Generated benchmark outputs and stats
│   │   ├── accuracy.json
│   │   ├── benchmark_results.txt
│   │   ├── translation_agent_benchmark_*.json
│   │   ├── translation_agent_responses_*.txt
│   │   └── translation_agent_stats_*.json
│   └── opus-mt-en-ar/              # Local HF model assets (EN→AR)
│       ├── config.json
│       ├── generation_config.json
│       ├── metadata.json
│       ├── pytorch_model.bin
│       ├── rust_model.ot
│       ├── source.spm
│       ├── target.spm
│       ├── tf_model.h5
│       ├── tokenizer_config.json
│       └── vocab.json
```

Note: Image artifacts (e.g., any `image_agent_outputs_*` folders) are present but intentionally not documented here per request.

## Requirements

- Python 3.10+
- CPU-only environment supported (no GPU required for the translation benchmark).

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Components

### Translation Benchmark (`model/main.py`)
- Loads the local `opus-mt-en-ar` model from `model/opus-mt-en-ar/` using `transformers`.
- Translates 50 English prompts (categorized as Easy/Medium) into Arabic.
- Records per-prompt timings and writes outputs to `model/benchmark/`:
  - `translation_agent_responses_*.txt`: human-readable translations and timings
  - `translation_agent_benchmark_*.json`: raw per-prompt results
  - `translation_agent_stats_*.json`: aggregate stats
  - `benchmark_results.txt`: appended summary of each run

Run the benchmark:

```bash
cd model
python main.py
```

If the model folder is missing, place Hugging Face assets for `Helsinki-NLP/opus-mt-en-ar` inside `model/opus-mt-en-ar/`. The script uses `local_files_only=True` and will not attempt downloads.

### Diffusers Model Sample (`model/download_model.py`)
- Demonstrates fetching `runwayml/stable-diffusion-v1-5` via `diffusers`.
- This sample disables the safety checker explicitly.

Run the sample:

```bash
cd model
python download_model.py
```

Note: This script only initializes the pipeline. Additional code is needed to generate outputs, and any image outputs are out of scope here.

### GGUF Conversion Utility (`model/quan.py`)
- Converts a `tiny_starcoder_py` model to GGUF using `llama.cpp` tools.
- Expects a local `llama.cpp` checkout and a `tiny_starcoder_py` directory.

Example steps (adjust paths as needed):

```bash
# Ensure the model and llama.cpp exist
ls tiny_starcoder_py
ls llama.cpp

# Run conversion and quantization
cd model
python quan.py
```

Outputs are written to `tiny_starcoder_py_gguf/` as FP16 and Q4_K_M variants.

## Benchmark Outputs

The benchmark data in `model/benchmark/` includes:
- `accuracy.json`: summary or placeholder for accuracy metrics.
- `benchmark_results.txt`: cumulative human-readable summaries of multiple runs.
- Time-stamped JSON/TXT files capturing responses, per-prompt timings, category stats, and overall stats.

## Tips & Troubleshooting

- Ensure `model/opus-mt-en-ar/` contains all required HF files (tokenizer, vocab, configs, and weights). The script will exit if files are missing.
- CPU runs may be slow for larger models; consider reducing prompt counts or categories in `PROMPTS` within `model/main.py`.
- For GGUF conversion, verify `llama.cpp` tools (`convert.py`, `quantize`) are compiled and available.

## License & Attribution

- Model files under `model/opus-mt-en-ar/` originate from Hugging Face (`Helsinki-NLP/opus-mt-en-ar`) and are subject to their respective licenses.
- This repository’s code is provided as-is; please review and comply with dependent libraries’ licenses.
