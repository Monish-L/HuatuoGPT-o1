# 🚀 Quick Reference Card - HuatuoGPT-o1 Training

One-page reference for common commands and workflows.

---

## 📋 Essential Commands

### Environment Setup
```bash
# Create environment (one time)
conda create -n huatuogpt python=3.10 -y

# Activate environment (every time)
conda activate huatuogpt

# Install PyTorch (one time)
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu118

# Install dependencies (one time)
pip install -r requirements-complete.txt

# Login to HuggingFace (one time)
huggingface-cli login
```

### Check System
```bash
# Check GPU
nvidia-smi

# Check CUDA available in PyTorch
python -c "import torch; print(torch.cuda.is_available())"

# Check GPU count
python -c "import torch; print(torch.cuda.device_count())"

# Check packages installed
python -c "import transformers, accelerate, datasets; print('OK')"

# Check disk space
df -h
```

### Dataset
```bash
# Download dataset
python download_and_prepare_dataset.py --subset en --output_dir ./data

# Verify dataset
ls -lh ./data/
python -c "import json; print(len(json.load(open('./data/medical_o1_sft_en_data.json'))))"
```

### Training
```bash
# Make script executable (one time)
chmod +x train_stage1.sh

# Start training
./train_stage1.sh

# Stop training
Ctrl + C
```

### Monitoring
```bash
# Watch GPU usage (in separate terminal)
watch -n 1 nvidia-smi

# Check checkpoints
ls -lh ./ckpts/sft_stage1/

# View logs
tail -f ./train_logs/sft_stage1_medical_o1/wandb/latest-run/logs/debug.log

# Check disk space
df -h
```

---

## 🎯 Quick Workflows

### Complete Setup (First Time)
```bash
# 1. Environment
conda create -n huatuogpt python=3.10 -y
conda activate huatuogpt

# 2. Dependencies
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements-complete.txt

# 3. Login
huggingface-cli login

# 4. Download dataset
python download_and_prepare_dataset.py --subset en

# 5. Train
./train_stage1.sh
```

### Daily Workflow (Resume Training)
```bash
# 1. Open VS Code
code /home/user/HuatuoGPT-o1

# 2. Open terminal (Ctrl + `)

# 3. Activate environment
conda activate huatuogpt

# 4. Start/resume training
./train_stage1.sh
```

### Check Training Progress
```bash
# Terminal 1: Watch training output
./train_stage1.sh

# Terminal 2: Monitor GPUs
watch -n 1 nvidia-smi

# Terminal 3: Check checkpoints
ls -lht ./ckpts/sft_stage1/
```

---

## 🔧 Quick Fixes

### Out of Memory
Edit `train_stage1.sh`:
```bash
TRAIN_BSZ_PER_GPU=1                    # Reduce from 2
GRADIENT_ACCUMULATION_STEPS=16         # Increase from 8
MAX_SEQ_LEN=4096                        # Reduce from 8192
```

### Dataset Missing
```bash
python download_and_prepare_dataset.py --subset en --output_dir ./data
```

### Package Not Found
```bash
conda activate huatuogpt
pip install -r requirements-complete.txt
```

### Model Access Denied
```bash
huggingface-cli login
# Then visit: https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
# Click: "Agree and access repository"
```

---

## 📊 What to Expect

### Training Progress
```
Epoch 0: XX%|████ | 285/1234 [1:23:45<4:32:10, loss=2.345, acc=0.456]
```
- **loss**: Should decrease (3.0 → 1.5)
- **acc**: Should increase (0.3 → 0.7)
- **Time**: 12-18 hours on 8x A100

### Checkpoints
```
./ckpts/sft_stage1/
  ├── checkpoint-0-1234/tfmr/    # After epoch 0
  ├── checkpoint-1-2468/tfmr/    # After epoch 1
  └── checkpoint-2-3702/tfmr/    # After epoch 2 (final)
```

### GPU Usage (nvidia-smi)
- **GPU-Util**: Should be 90-100%
- **Memory**: Near maximum
- **Temp**: Below 85°C

---

## ⌨️ VS Code Shortcuts

### Essential
- `` Ctrl + ` ``: Toggle terminal
- `Ctrl + P`: Quick file open
- `Ctrl + Shift + P`: Command palette
- `Ctrl + B`: Toggle sidebar
- `Ctrl + F`: Find in file
- `Ctrl + C` (in terminal): Stop process

### Terminal
- `Ctrl + Shift + 5`: Split terminal
- `Ctrl + Shift + \``: New terminal
- `Ctrl + L`: Clear terminal
- `Ctrl + C`: Stop current process
- `↑ / ↓`: Previous/next command

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `download_and_prepare_dataset.py` | Download dataset |
| `train_stage1.sh` | Start training |
| `VSCODE_SETUP_GUIDE.md` | Complete VS Code tutorial |
| `SETUP_AND_TRAINING_GUIDE.md` | Detailed training guide |
| `QUICKSTART.md` | Quick start guide |
| `requirements-complete.txt` | All dependencies |

---

## 🎓 Key Concepts

**Effective Batch Size** = `batch_size_per_gpu × num_gpus × gradient_accumulation_steps`
- Example: `2 × 8 × 8 = 128`

**Epochs**: Full passes through dataset
- We train for 3 epochs
- Each epoch ~4-6 hours on 8x A100

**Checkpoints**: Saved after each epoch
- Used to resume training
- Each ~15 GB for 8B model

**Learning Rate**: How fast model learns
- Starts at 5e-6
- Follows cosine schedule with warmup

---

## 📞 Getting Help

**In order:**
1. Check troubleshooting section in `VSCODE_SETUP_GUIDE.md`
2. Review error message carefully
3. Check `SETUP_AND_TRAINING_GUIDE.md`
4. Google the error
5. Ask on GitHub issues

---

## ✅ Pre-Training Checklist

- [ ] Conda environment created and activated
- [ ] PyTorch installed with CUDA support
- [ ] All dependencies installed
- [ ] HuggingFace logged in
- [ ] LLaMA access approved (if using LLaMA)
- [ ] Dataset downloaded (~500 MB)
- [ ] GPU available and detected
- [ ] 100GB+ free disk space
- [ ] `train_stage1.sh` configured
- [ ] Ready for 12+ hours of training

---

## 🎯 Quick Test

Run this to verify everything is ready:
```bash
# Test environment
conda activate huatuogpt
python -c "import torch, transformers, accelerate, datasets; assert torch.cuda.is_available(); print('✓ All systems ready!')"

# Test dataset
python -c "import json; data=json.load(open('./data/medical_o1_sft_en_data.json')); print(f'✓ Dataset ready: {len(data)} samples')"

# Test GPU
nvidia-smi

# If all pass, you're ready to train!
./train_stage1.sh
```

---

## 📖 Documentation Map

```
Start Here
    ↓
GETTING_STARTED.md ──→ Choose your path:
    ↓                   ├─→ Experienced: QUICKSTART.md
    ↓                   └─→ Beginner: SETUP_AND_TRAINING_GUIDE.md
    ↓
VSCODE_SETUP_GUIDE.md ──→ Complete VS Code tutorial
    ↓
QUICK_REFERENCE.md ──→ This file (you are here!)
    ↓
Start training! 🚀
```

---

**Print this page and keep it handy!** 📄

Good luck! 🍀
