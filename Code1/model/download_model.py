from transformers import AutoModelForCausalLM, AutoTokenizer

# Download and save to a local directory
model_name = "bigcode/tiny_starcoder_py"
local_dir = "./models/tiny_starcoder_py"

# Download model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Save locally
tokenizer.save_pretrained(local_dir)
model.save_pretrained(local_dir)

print(f"Model saved to {local_dir}")