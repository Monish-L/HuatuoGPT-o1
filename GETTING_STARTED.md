# 🏥 Getting Started with HuatuoGPT-o1 Stage 1 Training

Welcome! This guide will help you train HuatuoGPT-o1 using the **FreedomIntelligence/medical-o1-reasoning-SFT** dataset.

---

## 📁 What's Included

I've created several helpful files for you:

| File | Purpose |
|------|---------|
| `download_and_prepare_dataset.py` | Downloads and prepares the FreedomIntelligence dataset |
| `train_stage1.sh` | Easy-to-use training script with configuration |
| `QUICKSTART.md` | Quick reference guide (5-minute read) |
| `SETUP_AND_TRAINING_GUIDE.md` | Detailed step-by-step guide (complete tutorial) |
| `requirements-complete.txt` | All dependencies including dataset tools |

---

## 🎯 Three Ways to Get Started

### 1️⃣ Ultra-Quick Start (For Experienced Users)

```bash
# Setup
conda create -n huatuogpt python=3.10 -y
conda activate huatuogpt
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements-complete.txt

# Download dataset
python download_and_prepare_dataset.py --subset en

# Login to HuggingFace (needed for LLaMA models)
huggingface-cli login

# Train
./train_stage1.sh
```

### 2️⃣ Quick Start (Recommended)

Read the **[QUICKSTART.md](QUICKSTART.md)** file - it's a condensed guide that covers:
- Environment setup (5 minutes)
- Dataset download (10 minutes)
- Training launch (1 command)
- Basic troubleshooting

**Time to start training: ~15-20 minutes**

### 3️⃣ Complete Tutorial (For Beginners)

Read the **[SETUP_AND_TRAINING_GUIDE.md](SETUP_AND_TRAINING_GUIDE.md)** file - it's a comprehensive tutorial that covers:
- Detailed system requirements
- Step-by-step environment setup
- Dataset preparation with explanations
- Training configuration explained
- Complete troubleshooting guide
- Tips for success

**Time to start training: ~30-45 minutes**

---

## 📚 Documentation Overview

### File Details

#### 1. `download_and_prepare_dataset.py`
**Purpose**: Downloads the medical reasoning dataset from HuggingFace

**Usage**:
```bash
# Download English dataset (19.7k samples)
python download_and_prepare_dataset.py --subset en --output_dir ./data

# Download Chinese dataset
python download_and_prepare_dataset.py --subset zh --output_dir ./data

# Preview first sample only
python download_and_prepare_dataset.py --subset en --output_dir ./data --preview
```

**What it does**:
- Downloads FreedomIntelligence/medical-o1-reasoning-SFT from HuggingFace
- Converts to JSON format: `{"Question": "...", "Complex_CoT": "...", "Response": "..."}`
- Saves to `./data/medical_o1_sft_{subset}_data.json`
- Shows progress and sample data

---

#### 2. `train_stage1.sh`
**Purpose**: Easy-to-use bash script that launches training

**Features**:
- ✅ Pre-flight checks (GPU, dependencies, data)
- ✅ Configurable parameters (edit at top of file)
- ✅ Multi-GPU and single-GPU support
- ✅ Colored output and progress indicators
- ✅ Post-training summary

**Usage**:
```bash
# Option 1: Use defaults
./train_stage1.sh

# Option 2: Edit configuration first
nano train_stage1.sh
# (Edit MODEL_PATH, DATA_PATH, NUM_GPUS, etc.)
./train_stage1.sh
```

**Key Configuration Variables** (edit in the script):
```bash
MODEL_PATH="meta-llama/Llama-3.1-8B-Instruct"  # Base model
DATA_PATH="./data/medical_o1_sft_en_data.json"  # Training data
NUM_GPUS=8                                       # Number of GPUs
TRAIN_BSZ_PER_GPU=2                              # Batch size per GPU
N_EPOCHS=3                                       # Training epochs
```

---

#### 3. `QUICKSTART.md`
**Purpose**: Quick reference guide for getting started

**Best for**:
- Users who want to start quickly
- Users familiar with ML training
- Quick reference during setup

**Contains**:
- Minimal setup commands
- Essential configuration options
- Quick troubleshooting tips
- Training time estimates

---

#### 4. `SETUP_AND_TRAINING_GUIDE.md`
**Purpose**: Comprehensive tutorial with detailed explanations

**Best for**:
- First-time users
- Users unfamiliar with distributed training
- Users who want to understand each step
- Troubleshooting difficult issues

**Contains**:
- System requirements explained
- Step-by-step environment setup
- Dataset details and format
- Training parameter explanations
- Complete troubleshooting section
- Tips and best practices
- Next steps after training

---

#### 5. `requirements-complete.txt`
**Purpose**: Complete list of dependencies

**Usage**:
```bash
pip install -r requirements-complete.txt
```

**Includes**:
- Original dependencies from `requirements.txt`
- Additional packages for dataset download (`datasets`, `huggingface_hub`)
- Useful utilities (`wandb`, `jupyter`, `pandas`)

---

## 🚦 Recommended Workflow

### Step 1: Choose Your Guide
- **Experienced?** → Start with QUICKSTART.md
- **New to this?** → Start with SETUP_AND_TRAINING_GUIDE.md

### Step 2: Environment Setup
```bash
# Create environment
conda create -n huatuogpt python=3.10 -y
conda activate huatuogpt

# Install dependencies
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements-complete.txt
```

### Step 3: Download Dataset
```bash
# Login to HuggingFace (first time only)
huggingface-cli login

# Download dataset
python download_and_prepare_dataset.py --subset en
```

### Step 4: Configure Training
```bash
# Edit the training script
nano train_stage1.sh

# Key settings to check:
# - MODEL_PATH: Which model to use
# - NUM_GPUS: How many GPUs you have
# - TRAIN_BSZ_PER_GPU: Adjust if you get OOM errors
```

### Step 5: Launch Training
```bash
# Start training
./train_stage1.sh

# Monitor GPU usage in another terminal
watch -n 1 nvidia-smi
```

### Step 6: Monitor Progress
Training will show:
```
Epoch 0: 100%|████| 1234/1234 [1:23:45<00:00, loss=2.345, acc=0.567]
✓ Checkpoint checkpoint-0-1234 is saved...
```

### Step 7: Use Your Model
After training, your model will be in:
```
./ckpts/sft_stage1/checkpoint-{epoch}-{step}/tfmr/
```

---

## ⚡ Quick Tips

### Before You Start
1. ✅ Check GPU availability: `nvidia-smi`
2. ✅ Verify you have 100GB+ free space: `df -h`
3. ✅ Create HuggingFace account: https://huggingface.co/join
4. ✅ Request LLaMA access: https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct

### During Training
1. 📊 Monitor GPU usage: `watch -n 1 nvidia-smi`
2. 💾 Keep checkpoints safe (they're auto-saved after each epoch)
3. 📝 Save logs: `./train_stage1.sh 2>&1 | tee training.log`
4. ⏱️ Be patient - training takes 12-18 hours on 8x A100 GPUs

### If Something Goes Wrong
1. **CUDA Out of Memory**
   - Reduce `TRAIN_BSZ_PER_GPU` to 1
   - Reduce `MAX_SEQ_LEN` to 4096
   - Increase `GRADIENT_ACCUMULATION_STEPS` to 16

2. **Dataset Not Found**
   - Re-run: `python download_and_prepare_dataset.py --subset en`
   - Check file exists: `ls -lh ./data/`

3. **Model Download Failed**
   - Login: `huggingface-cli login`
   - Check LLaMA access approved
   - Try downloading manually first

---

## 📊 What to Expect

### Dataset
- **Size**: 19,700 medical reasoning samples (English subset)
- **Format**: Question + Complex Chain-of-Thought + Response
- **Topics**: Medical diagnosis, treatment, physiology, pathology
- **File size**: ~500 MB

### Training
- **Time**: 12-18 hours (8x A100) to 4-6 days (1x A100)
- **Checkpoints**: Saved after each epoch (~50-70 GB each)
- **GPU VRAM**: ~20-24 GB per GPU (with default settings)
- **Metrics**: Loss should decrease from ~3.0 to ~1.5, Accuracy increases to ~0.6-0.7

### Output
- **Location**: `./ckpts/sft_stage1/checkpoint-{epoch}-{step}/tfmr/`
- **Contents**: Model weights, tokenizer, config files
- **Size**: ~14-16 GB per checkpoint (for 8B model)
- **Format**: Standard HuggingFace Transformers format

---

## 🎓 Learning Resources

### Understanding the Training Process
1. **Stage 1 (SFT)**: Supervised Fine-Tuning on reasoning trajectories
2. **What you're training**: Teaching the model to think step-by-step
3. **Why Complex CoT**: Helps model break down complex medical reasoning
4. **Next**: Stage 2 uses Reinforcement Learning to improve further

### Key Concepts
- **Gradient Accumulation**: Simulates larger batch sizes with limited memory
- **DeepSpeed ZeRO-3**: Distributes model parameters across GPUs
- **Mixed Precision (bf16)**: Faster training with lower memory usage
- **Effective Batch Size**: `batch_size_per_gpu × num_gpus × gradient_accumulation_steps`

---

## 🆘 Getting Help

### If You're Stuck

1. **Check the guides**:
   - QUICKSTART.md for quick answers
   - SETUP_AND_TRAINING_GUIDE.md for detailed help

2. **Common issues**:
   - Out of memory → Reduce batch size or sequence length
   - Model not found → Check HuggingFace login and access
   - Training too slow → Check GPU utilization with `nvidia-smi`

3. **Verify your setup**:
   ```bash
   # Check CUDA
   python -c "import torch; print(torch.cuda.is_available())"

   # Check packages
   python -c "import transformers, accelerate, datasets; print('✓ OK')"

   # Check data
   ls -lh ./data/medical_o1_sft_en_data.json
   ```

4. **Still stuck?**
   - Open an issue on GitHub
   - Include error messages and system info
   - Share relevant log outputs

---

## 📖 Additional Resources

- **Paper**: [HuatuoGPT-o1](https://arxiv.org/pdf/2412.18925)
- **Dataset**: [medical-o1-reasoning-SFT](https://huggingface.co/datasets/FreedomIntelligence/medical-o1-reasoning-SFT)
- **Models**: [HuatuoGPT-o1 on HuggingFace](https://huggingface.co/FreedomIntelligence)
- **DeepSpeed Docs**: https://www.deepspeed.ai/
- **Accelerate Docs**: https://huggingface.co/docs/accelerate

---

## ✨ Summary

You now have everything you need to train HuatuoGPT-o1 Stage 1:

- ✅ Dataset download script
- ✅ Training launch script
- ✅ Quick start guide
- ✅ Detailed tutorial
- ✅ Complete requirements
- ✅ Troubleshooting help

**Next step**: Open either QUICKSTART.md or SETUP_AND_TRAINING_GUIDE.md and follow along!

Good luck with your training! 🚀🏥

---

## 📝 Checklist Before Starting

- [ ] GPU available (`nvidia-smi` works)
- [ ] Python 3.8-3.11 installed
- [ ] Created conda/venv environment
- [ ] Installed all dependencies (`pip install -r requirements-complete.txt`)
- [ ] Downloaded dataset (`python download_and_prepare_dataset.py`)
- [ ] HuggingFace account created and logged in
- [ ] LLaMA model access approved (if using LLaMA)
- [ ] 100GB+ free disk space
- [ ] Reviewed training configuration in `train_stage1.sh`
- [ ] Ready to commit to 12+ hours of training

If all checked ✅, you're ready to run `./train_stage1.sh`!
