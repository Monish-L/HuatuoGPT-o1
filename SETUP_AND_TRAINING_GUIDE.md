# Complete Setup and Training Guide for HuatuoGPT-o1 Stage 1

This guide will walk you through **every step** needed to set up your environment and run Stage 1 training using the FreedomIntelligence/medical-o1-reasoning-SFT dataset.

---

## 📋 Prerequisites

### System Requirements
- **GPU**: NVIDIA GPU with at least 24GB VRAM (preferably A100, A6000, or RTX 4090)
  - For multi-GPU: 8x GPUs recommended (as per original training setup)
  - For single GPU: You'll need to adjust batch sizes
- **RAM**: At least 64GB system RAM
- **Storage**: At least 100GB free space for model, dataset, and checkpoints
- **OS**: Linux (Ubuntu 20.04+ recommended)
- **CUDA**: CUDA 11.8 or higher
- **Python**: Python 3.8 - 3.11

### Check Your GPU
```bash
# Check if you have NVIDIA GPU
nvidia-smi

# You should see your GPU(s) listed with memory info
```

---

## 🚀 Step 1: Set Up Python Environment

### Option A: Using Conda (Recommended)

```bash
# 1. Install Miniconda if you don't have it
# Download from: https://docs.conda.io/en/latest/miniconda.html
# Or use:
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# 2. Create a new conda environment
conda create -n huatuogpt python=3.10 -y

# 3. Activate the environment
conda activate huatuogpt

# 4. Install PyTorch (adjust based on your CUDA version)
# For CUDA 11.8:
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1:
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121

# 5. Verify PyTorch can see your GPU
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU count: {torch.cuda.device_count()}')"
```

### Option B: Using venv

```bash
# 1. Create virtual environment
python3 -m venv huatuogpt-env

# 2. Activate it
source huatuogpt-env/bin/activate

# 3. Install PyTorch (follow same instructions as conda above)
```

---

## 📦 Step 2: Install Dependencies

```bash
# Make sure you're in the project directory
cd /home/user/HuatuoGPT-o1

# Install all required packages
pip install -r requirements.txt

# Install additional required packages for dataset download
pip install datasets huggingface_hub

# If you encounter any issues with deepspeed, install it separately:
pip install deepspeed==0.15.4 --no-build-isolation
```

### Verify Installation

```bash
# Check key packages
python -c "import torch; import transformers; import accelerate; import deepspeed; print('✓ All packages installed successfully!')"
```

---

## 📥 Step 3: Download the Dataset

We'll use the FreedomIntelligence/medical-o1-reasoning-SFT dataset.

```bash
# Run the dataset download script
python download_and_prepare_dataset.py --subset en --output_dir ./data

# This will:
# 1. Download the English dataset (~19.7k samples)
# 2. Convert it to the required JSON format
# 3. Save it to ./data/medical_o1_sft_en_data.json

# For Chinese dataset, use:
# python download_and_prepare_dataset.py --subset zh --output_dir ./data
```

**What this does:**
- Downloads the dataset from HuggingFace
- Converts it to JSON format with fields: Question, Complex_CoT, Response
- Saves to `./data/medical_o1_sft_en_data.json`

**Expected output:**
```
✓ Successfully loaded 19700 samples!
✓ Dataset preparation complete!
📊 Total samples: 19700
📁 Saved to: ./data/medical_o1_sft_en_data.json
💾 File size: ~500 MB
```

---

## 🤖 Step 4: Download the Base Model

You'll need a base model to fine-tune. HuatuoGPT-o1 uses LLaMA or Qwen models.

### Option 1: Using Hugging Face CLI (Recommended)

```bash
# Login to Hugging Face (you'll need an account)
huggingface-cli login

# Enter your Hugging Face token when prompted
# Get your token from: https://huggingface.co/settings/tokens

# Download LLaMA 3.1 8B Instruct (you'll need to accept Meta's license first)
# Go to: https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
# Click "Agree and access repository"

# The model will be automatically downloaded during training
# Or pre-download it:
python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('meta-llama/Llama-3.1-8B-Instruct')"
```

### Option 2: Use Local Model Path

If you have a model downloaded locally, you can specify the path directly in the training command.

**Important:** For LLaMA models, you need to:
1. Create a HuggingFace account: https://huggingface.co/join
2. Request access to LLaMA models: https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
3. Wait for approval (usually instant)

---

## ⚙️ Step 5: Configure Training Parameters

### Understanding the Training Script

The `SFT_stage1.py` script accepts these key parameters:

| Parameter | Description | Default | Recommended |
|-----------|-------------|---------|-------------|
| `--model_path` | Path or name of base model | Required | `meta-llama/Llama-3.1-8B-Instruct` |
| `--data_path` | Path to training data JSON | Required | `./data/medical_o1_sft_en_data.json` |
| `--output_dir` | Where to save checkpoints | `./ckpts` | `./ckpts/sft_stage1` |
| `--max_seq_len` | Maximum sequence length | 8192 | 8192 |
| `--train_bsz_per_gpu` | Batch size per GPU | 2 | 1-2 (adjust based on VRAM) |
| `--gradient_accumulation_steps` | Gradient accumulation | 8 | 8-16 |
| `--learning_rate` | Learning rate | 5e-6 | 5e-6 |
| `--n_epochs` | Number of training epochs | 3 | 3 |
| `--max_ckpts` | Max checkpoints to keep | 2 | 2 |

### Memory Requirements

**Approximate VRAM usage:**
- 8B model with batch_size=1: ~18-20GB per GPU
- 8B model with batch_size=2: ~22-24GB per GPU

If you have limited VRAM:
- Reduce `--train_bsz_per_gpu` to 1
- Increase `--gradient_accumulation_steps` to maintain effective batch size

---

## 🎯 Step 6: Run Stage 1 Training

### For Multi-GPU Setup (8 GPUs - Recommended)

```bash
# Make sure you're in the project directory
cd /home/user/HuatuoGPT-o1

# Run training with accelerate
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
    --n_epochs 3 \
    --max_ckpts 2
```

### For Single GPU Setup

```bash
# For single GPU, use a simpler config
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
    --n_epochs 3 \
    --max_ckpts 2
```

### Using the Training Script (Easiest)

We've created a simple script for you:

```bash
# Make it executable
chmod +x train_stage1.sh

# Edit the script to set your preferences (optional)
nano train_stage1.sh

# Run training
./train_stage1.sh
```

---

## 📊 Step 7: Monitor Training

### What to Expect

During training, you'll see output like:

```
Loading dataset...
✓ Successfully loaded 19700 samples
Training...
Epoch 0: 100%|████████| 1234/1234 [1:23:45<00:00, loss=2.345, acc=0.567, lr=5e-6]
✓ Checkpoint checkpoint-0-1234 is saved...
```

### Key Metrics

- **Loss**: Should decrease over time (start ~3.0, end ~1.5)
- **Accuracy**: Should increase (start ~0.3, end ~0.6-0.7)
- **Learning Rate**: Will follow cosine schedule with warmup

### Checkpoints

Checkpoints are saved after each epoch to:
```
./ckpts/sft_stage1/checkpoint-{epoch}-{step}/tfmr/
```

Each checkpoint contains:
- Model weights
- Tokenizer
- Configuration files

### Training Time Estimates

- **8x A100 GPUs**: ~12-18 hours for 3 epochs
- **Single A100**: ~4-6 days for 3 epochs
- **4x RTX 4090**: ~1-2 days for 3 epochs

---

## 🔍 Step 8: Resume Training (If Interrupted)

If training stops, you can resume from the latest checkpoint:

```bash
# Find the latest checkpoint
ls -lt ./ckpts/sft_stage1/

# Note: The current training script doesn't have automatic resume
# You would need to modify the script or restart training
# The script will save checkpoints, but resuming requires code modification
```

---

## ✅ Step 9: Verify Your Trained Model

After training completes:

```bash
# List checkpoints
ls ./ckpts/sft_stage1/

# Test the model with a simple inference script
python -c "
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load your trained model
model_path = './ckpts/sft_stage1/checkpoint-2-XXXX/tfmr'
model = AutoModelForCausalLM.from_pretrained(model_path, device_map='auto')
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Test with a medical question
question = 'What are the symptoms of diabetes?'
messages = [{'role': 'user', 'content': question}]
inputs = tokenizer.apply_chat_template(messages, return_tensors='pt', add_generation_prompt=True)
outputs = model.generate(inputs.to(model.device), max_new_tokens=512)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
"
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. CUDA Out of Memory

**Error:** `RuntimeError: CUDA out of memory`

**Solutions:**
```bash
# Reduce batch size
--train_bsz_per_gpu 1

# Increase gradient accumulation to maintain effective batch size
--gradient_accumulation_steps 16

# Reduce sequence length
--max_seq_len 4096
```

#### 2. Dataset Not Found

**Error:** `FileNotFoundError: [Errno 2] No such file or directory: './data/...'`

**Solution:**
```bash
# Re-run the dataset download script
python download_and_prepare_dataset.py --subset en --output_dir ./data
```

#### 3. Model Download Fails

**Error:** `403 Forbidden` or `Repository not found`

**Solution:**
```bash
# Login to Hugging Face
huggingface-cli login

# Accept LLaMA license at:
# https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
```

#### 4. DeepSpeed Issues

**Error:** `No module named 'deepspeed'` or DeepSpeed compilation errors

**Solution:**
```bash
# Reinstall DeepSpeed
pip uninstall deepspeed -y
pip install deepspeed==0.15.4 --no-build-isolation

# If still fails, install build dependencies
sudo apt-get install libaio-dev
```

#### 5. Slow Training

**Solutions:**
- Enable gradient checkpointing (already enabled in script)
- Use mixed precision training (already enabled with bf16)
- Ensure you're using the DeepSpeed config for multi-GPU
- Check GPU utilization: `nvidia-smi -l 1`

---

## 📈 Next Steps: Stage 2 (Reinforcement Learning)

After Stage 1 completes, you can proceed to Stage 2 (PPO training):

1. Your Stage 1 checkpoint will be used as the starting point
2. You'll need the medical verifier model
3. See the main README.md for Stage 2 instructions

---

## 🔗 Useful Resources

- **HuatuoGPT-o1 Paper**: https://arxiv.org/pdf/2412.18925
- **Dataset**: https://huggingface.co/datasets/FreedomIntelligence/medical-o1-reasoning-SFT
- **Pre-trained Models**: https://huggingface.co/FreedomIntelligence
- **DeepSpeed Documentation**: https://www.deepspeed.ai/
- **Accelerate Documentation**: https://huggingface.co/docs/accelerate

---

## 💡 Tips for Success

1. **Start Small**: Test with a small subset first (use `--limit` parameter in dataset script)
2. **Monitor GPU**: Use `watch -n 1 nvidia-smi` to monitor GPU usage
3. **Save Logs**: Redirect output to a log file: `./train_stage1.sh 2>&1 | tee training.log`
4. **Backup Checkpoints**: Copy important checkpoints to a safe location
5. **Use WandB**: The script supports Weights & Biases for tracking (logs saved offline)

---

## ❓ Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review the error message carefully
3. Check GPU memory: `nvidia-smi`
4. Verify all files exist: `ls -la ./data/`
5. Open an issue on the GitHub repository

---

## 📝 Summary Checklist

Before starting training, make sure you have:

- [ ] Python environment set up (conda/venv)
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] GPU accessible (check with `nvidia-smi`)
- [ ] Dataset downloaded (check `./data/medical_o1_sft_en_data.json`)
- [ ] HuggingFace account created and logged in
- [ ] LLaMA model access granted (if using LLaMA)
- [ ] Sufficient disk space (~100GB free)
- [ ] Training script configured (check parameters)
- [ ] Ready to monitor training (terminal multiplexer like `tmux` recommended)

Good luck with your training! 🚀
