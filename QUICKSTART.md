# 🚀 Quick Start Guide - Stage 1 Training

This is a simplified quick-start guide. For detailed instructions, see [SETUP_AND_TRAINING_GUIDE.md](SETUP_AND_TRAINING_GUIDE.md).

---

## Prerequisites

- NVIDIA GPU(s) with CUDA installed
- Python 3.8-3.11
- 100GB+ free disk space

---

## Step 1: Set Up Environment

```bash
# Create conda environment
conda create -n huatuogpt python=3.10 -y
conda activate huatuogpt

# Install PyTorch (adjust for your CUDA version)
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu118

# Install dependencies
cd /home/user/HuatuoGPT-o1
pip install -r requirements.txt
pip install datasets huggingface_hub

# Verify installation
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

---

## Step 2: Download Dataset

```bash
# Download the FreedomIntelligence dataset (English)
python download_and_prepare_dataset.py --subset en --output_dir ./data

# This downloads ~19.7k medical reasoning samples
# Output: ./data/medical_o1_sft_en_data.json
```

---

## Step 3: Set Up Model Access

```bash
# Login to HuggingFace
huggingface-cli login
# Enter your token from: https://huggingface.co/settings/tokens

# Request LLaMA access (if using LLaMA models):
# 1. Go to: https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
# 2. Click "Agree and access repository"
# 3. Wait for approval (usually instant)
```

---

## Step 4: Run Training

### Easy Way (Recommended)

```bash
# Edit configuration if needed
nano train_stage1.sh

# Run training
./train_stage1.sh
```

### Manual Way

**For 8 GPUs:**
```bash
accelerate launch \
    --config_file ./configs/deepspeed_zero3.yaml \
    --num_processes 8 \
    --num_machines 1 \
    --machine_rank 0 \
    --deepspeed_multinode_launcher standard \
    SFT_stage1.py \
    --model_path meta-llama/Llama-3.1-8B-Instruct \
    --data_path ./data/medical_o1_sft_en_data.json \
    --output_dir ./ckpts/sft_stage1 \
    --max_seq_len 8192 \
    --train_bsz_per_gpu 2 \
    --gradient_accumulation_steps 8 \
    --learning_rate 5e-6 \
    --n_epochs 3
```

**For Single GPU:**
```bash
accelerate launch \
    --num_processes 1 \
    --mixed_precision bf16 \
    SFT_stage1.py \
    --model_path meta-llama/Llama-3.1-8B-Instruct \
    --data_path ./data/medical_o1_sft_en_data.json \
    --output_dir ./ckpts/sft_stage1 \
    --max_seq_len 4096 \
    --train_bsz_per_gpu 1 \
    --gradient_accumulation_steps 16 \
    --learning_rate 5e-6 \
    --n_epochs 3
```

---

## Expected Training Time

- **8x A100 (80GB)**: 12-18 hours
- **4x A100 (40GB)**: 24-36 hours
- **Single A100**: 4-6 days
- **4x RTX 4090**: 1-2 days

---

## Monitoring Training

Training progress will show:
```
Epoch 0: 100%|████████| 1234/1234 [1:23:45<00:00, loss=2.345, acc=0.567]
✓ Checkpoint checkpoint-0-1234 is saved...
```

Check GPU usage:
```bash
watch -n 1 nvidia-smi
```

---

## Output

Trained models saved to:
```
./ckpts/sft_stage1/checkpoint-{epoch}-{step}/tfmr/
```

Each checkpoint contains:
- Model weights
- Tokenizer
- Config files

---

## Troubleshooting

### CUDA Out of Memory
```bash
# Reduce batch size in train_stage1.sh:
TRAIN_BSZ_PER_GPU=1

# Or reduce sequence length:
MAX_SEQ_LEN=4096
```

### Dataset Not Found
```bash
# Re-download dataset
python download_and_prepare_dataset.py --subset en --output_dir ./data
```

### Model Download Failed
```bash
# Make sure you're logged in
huggingface-cli login

# Check you have LLaMA access approved
```

---

## Testing Your Trained Model

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load your model
model_path = "./ckpts/sft_stage1/checkpoint-2-XXXX/tfmr"
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Test inference
question = "What are the symptoms of diabetes?"
messages = [{"role": "user", "content": question}]
inputs = tokenizer.apply_chat_template(messages, return_tensors="pt", add_generation_prompt=True)
outputs = model.generate(inputs.to(model.device), max_new_tokens=512)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

---

## Next Steps

1. ✅ Evaluate your model on test datasets
2. ✅ Try inference on medical questions
3. ✅ Proceed to Stage 2 (RL training) - see README.md

---

## Configuration Options

| Parameter | Description | Default | Adjust If |
|-----------|-------------|---------|-----------|
| `--train_bsz_per_gpu` | Batch size per GPU | 2 | OOM error → reduce to 1 |
| `--max_seq_len` | Max sequence length | 8192 | OOM error → reduce to 4096 |
| `--gradient_accumulation_steps` | Gradient accumulation | 8 | Smaller batch → increase |
| `--learning_rate` | Learning rate | 5e-6 | Adjust for convergence |
| `--n_epochs` | Training epochs | 3 | More/less training |

---

## Full Documentation

See [SETUP_AND_TRAINING_GUIDE.md](SETUP_AND_TRAINING_GUIDE.md) for:
- Detailed setup instructions
- System requirements
- Advanced configuration
- Complete troubleshooting guide
- Tips and best practices

---

## Help & Support

- **GitHub Issues**: Open an issue on the repository
- **Paper**: https://arxiv.org/pdf/2412.18925
- **Dataset**: https://huggingface.co/datasets/FreedomIntelligence/medical-o1-reasoning-SFT

Good luck! 🎉
