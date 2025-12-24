"""
Download Phi-3.5-mini-instruct model to local model/ folder
"""
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

# Set local models directory
MODELS_DIR = "model/Phi-3.5-mini-instruct"

print("Downloading microsoft/Phi-3.5-mini-instruct model to model/ folder...")
print("=" * 70)
print("WARNING: This will download ~7.5GB of data. Make sure you have enough space!")
print("=" * 70)

# Remove existing corrupted files
if os.path.exists(MODELS_DIR):
    print(f"Removing existing directory: {MODELS_DIR}")
    import shutil
    shutil.rmtree(MODELS_DIR)

os.makedirs(MODELS_DIR, exist_ok=True)

# Download tokenizer
print("\nDownloading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3.5-mini-instruct")
tokenizer.save_pretrained(MODELS_DIR)
print(f"✓ Tokenizer downloaded and saved to {MODELS_DIR}")

# Download model
print("\nDownloading model (this will take several minutes)...")
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3.5-mini-instruct",
    trust_remote_code=True,
    attn_implementation="eager"
)
model.save_pretrained(MODELS_DIR)
print(f"✓ Model downloaded and saved to {MODELS_DIR}")

print("=" * 70)
print(f"Model and tokenizer are now saved in: {MODELS_DIR}")
print("=" * 70)
