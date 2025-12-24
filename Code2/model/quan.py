"""
Convert tiny_starcoder_py to GGUF format
Requires: llama.cpp repository
"""
# (venv) ai-mas@code1:~/arch-ai-mas/model$ python convert_hf_to_gguf.py tiny_starcoder_py --outfile tiny_starcoder_py_fp16.gguf --outtype f16

import os
import subprocess

# Paths
MODEL_DIR = "tiny_starcoder_py"  # Your existing model folder
OUTPUT_DIR = "tiny_starcoder_py_gguf"
LLAMA_CPP_DIR = "llama.cpp"  # You'll need to clone llama.cpp repo

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Converting tiny_starcoder_py to GGUF format...")
print("=" * 70)

# Step 1: Convert to FP16 GGUF
print("\nStep 1: Converting to FP16 GGUF...")
convert_cmd = [
    "python3",
    f"{LLAMA_CPP_DIR}/convert.py",
    MODEL_DIR,
    "--outfile", f"{OUTPUT_DIR}/tiny_starcoder_py_fp16.gguf",
    "--outtype", "f16"
]

subprocess.run(convert_cmd, check=True)

# Step 2: Quantize to Q4_K_M (4-bit)
print("\nStep 2: Quantizing to Q4_K_M...")
quantize_cmd = [
    f"{LLAMA_CPP_DIR}/quantize",
    f"{OUTPUT_DIR}/tiny_starcoder_py_fp16.gguf",
    f"{OUTPUT_DIR}/tiny_starcoder_py_Q4_K_M.gguf",
    "Q4_K_M"
]

subprocess.run(quantize_cmd, check=True)

print("\n" + "=" * 70)
print("✓ Conversion complete!")
print(f"✓ Output: {OUTPUT_DIR}/tiny_starcoder_py_Q4_K_M.gguf")
print("=" * 70)