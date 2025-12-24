"""
Download Phi-2 model and tokenizer to local model/ folder
"""
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

# Set local models directory
MODELS_DIR = "model/phi-2-model"
os.makedirs(MODELS_DIR, exist_ok=True)

print("Downloading microsoft/phi-2 model to model/ folder...")
print("=" * 70)

# Download tokenizer
print("Downloading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
tokenizer.save_pretrained(MODELS_DIR)
print(f"✓ Tokenizer downloaded and saved to {MODELS_DIR}")

# Download model
print("\nDownloading model (this may take a while)...")
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", trust_remote_code=True)
model.save_pretrained(MODELS_DIR)
print(f"✓ Model downloaded and saved to {MODELS_DIR}")

print("=" * 70)
print(f"Model and tokenizer are now saved in: {MODELS_DIR}")
print("=" * 70)
