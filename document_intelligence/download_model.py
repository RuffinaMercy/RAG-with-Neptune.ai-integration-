# download_working.py
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

print("="*60)
print("DOWNLOADING PHI-3 MODEL")
print("="*60)

MODEL_NAME = "microsoft/phi-3-mini-4k-instruct"
SAVE_DIR = "models/phi-3"

# Create directory
os.makedirs(SAVE_DIR, exist_ok=True)

try:
    print("\n1. Downloading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True
    )
    tokenizer.save_pretrained(SAVE_DIR)
    print("   ✅ Tokenizer saved")
    
    print("\n2. Downloading model...")
    
    # Try different approaches
    try:
        # First try with eager attention
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True,
            attn_implementation="eager",
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        print("   ✅ Downloaded with eager attention")
        
    except Exception as e1:
        print(f"   ⚠️ First attempt failed: {e1}")
        
        # Try without any special parameters
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True
        )
        print("   ✅ Downloaded with default settings")
    
    # Save the model
    model.save_pretrained(SAVE_DIR)
    print("   ✅ Model saved")
    
    # Verify files
    print(f"\n3. Verifying download...")
    files = os.listdir(SAVE_DIR)
    print(f"   Found {len(files)} files:")
    for file in files:
        size = os.path.getsize(os.path.join(SAVE_DIR, file))
        print(f"   - {file} ({size/1024/1024:.1f} MB)")
    
    print("\n" + "="*60)
    print("🎉 SUCCESS! Model is ready to use.")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\n💡 Solutions:")
    print("1. Update transformers: pip install --upgrade transformers")
    print("2. Install flash-attention: pip install flash-attn --no-build-isolation")
    print("3. Or download manually from huggingface.co/microsoft/phi-3-mini-4k-instruct")