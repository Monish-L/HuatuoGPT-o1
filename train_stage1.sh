#!/bin/bash

################################################################################
# HuatuoGPT-o1 Stage 1 Training Script
#
# This script runs Stage 1 Supervised Fine-Tuning (SFT) using the
# FreedomIntelligence/medical-o1-reasoning-SFT dataset
#
# Usage:
#   ./train_stage1.sh
#
# Before running:
#   1. Make sure you've downloaded the dataset (run download_and_prepare_dataset.py)
#   2. Ensure you have GPU access (check with: nvidia-smi)
#   3. Activate your Python environment (conda activate huatuogpt)
################################################################################

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================================================"
echo "                  HuatuoGPT-o1 Stage 1 Training"
echo "================================================================================"
echo ""

# ============================================================================
# CONFIGURATION - EDIT THESE SETTINGS
# ============================================================================

# Model Configuration
MODEL_PATH="meta-llama/Llama-3.1-8B-Instruct"  # Can be a HuggingFace model name or local path
# Alternative models you can try:
# MODEL_PATH="meta-llama/Llama-3.1-70B-Instruct"  # Larger model (requires more GPUs)
# MODEL_PATH="Qwen/Qwen2.5-7B-Instruct"          # Qwen model

# Data Configuration
DATA_PATH="./data/medical_o1_sft_en_data.json"  # Path to your training data

# Training Configuration
OUTPUT_DIR="./ckpts/sft_stage1"                 # Where to save checkpoints
MAX_SEQ_LEN=8192                                 # Maximum sequence length
TRAIN_BSZ_PER_GPU=2                              # Batch size per GPU (reduce if OOM)
GRADIENT_ACCUMULATION_STEPS=8                    # Gradient accumulation steps
LEARNING_RATE=5e-6                               # Learning rate
N_EPOCHS=3                                       # Number of training epochs
MAX_CKPTS=2                                      # Maximum checkpoints to keep
EXPERIMENT_NAME="sft_stage1_medical_o1"          # Experiment name for logging

# Multi-GPU Configuration
NUM_GPUS=8                                       # Number of GPUs to use
NUM_MACHINES=1                                   # Number of machines
MACHINE_RANK=0                                   # Machine rank (0 for single machine)

# Advanced Configuration (usually don't need to change)
WEIGHT_DECAY=0.1                                 # Weight decay
WARMUP_RATES=0.05                                # Warmup ratio
LOG_DIR="./train_logs"                           # Log directory

# ============================================================================
# PRE-FLIGHT CHECKS
# ============================================================================

echo -e "${YELLOW}Running pre-flight checks...${NC}"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Error: Python not found. Please install Python 3.8+${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Python found: $(python --version)"

# Check if NVIDIA GPU is available
if ! command -v nvidia-smi &> /dev/null; then
    echo -e "${RED}❌ Error: nvidia-smi not found. Please ensure NVIDIA drivers are installed.${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} NVIDIA GPU found:"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader | nl

# Check if data file exists
if [ ! -f "$DATA_PATH" ]; then
    echo -e "${RED}❌ Error: Data file not found at $DATA_PATH${NC}"
    echo -e "${YELLOW}Please run: python download_and_prepare_dataset.py${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Data file found: $DATA_PATH"

# Check if SFT script exists
if [ ! -f "SFT_stage1.py" ]; then
    echo -e "${RED}❌ Error: SFT_stage1.py not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Training script found: SFT_stage1.py"

# Check if accelerate is installed
if ! python -c "import accelerate" &> /dev/null; then
    echo -e "${RED}❌ Error: accelerate not installed. Please run: pip install -r requirements.txt${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Accelerate library found"

# Check if transformers is installed
if ! python -c "import transformers" &> /dev/null; then
    echo -e "${RED}❌ Error: transformers not installed. Please run: pip install -r requirements.txt${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Transformers library found"

# Create output directories
mkdir -p "$OUTPUT_DIR"
mkdir -p "$LOG_DIR"
echo -e "${GREEN}✓${NC} Output directories created"

echo ""
echo "================================================================================"
echo "                         Training Configuration"
echo "================================================================================"
echo "Model:                    $MODEL_PATH"
echo "Data:                     $DATA_PATH"
echo "Output Directory:         $OUTPUT_DIR"
echo "Number of GPUs:           $NUM_GPUS"
echo "Batch Size per GPU:       $TRAIN_BSZ_PER_GPU"
echo "Gradient Accumulation:    $GRADIENT_ACCUMULATION_STEPS"
echo "Effective Batch Size:     $((TRAIN_BSZ_PER_GPU * GRADIENT_ACCUMULATION_STEPS * NUM_GPUS))"
echo "Learning Rate:            $LEARNING_RATE"
echo "Number of Epochs:         $N_EPOCHS"
echo "Max Sequence Length:      $MAX_SEQ_LEN"
echo "================================================================================"
echo ""

# Ask for confirmation
read -p "$(echo -e ${YELLOW}Ready to start training? This may take many hours. Continue? [y/N]: ${NC})" -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Training cancelled."
    exit 0
fi

# ============================================================================
# LAUNCH TRAINING
# ============================================================================

echo ""
echo "================================================================================"
echo "                         Starting Training"
echo "================================================================================"
echo ""

# Determine which accelerate config to use
if [ $NUM_GPUS -gt 1 ]; then
    echo "Using multi-GPU configuration with DeepSpeed ZeRO-3"
    ACCELERATE_CONFIG="./configs/deepspeed_zero3.yaml"

    accelerate launch \
        --config_file "$ACCELERATE_CONFIG" \
        --num_processes "$NUM_GPUS" \
        --num_machines "$NUM_MACHINES" \
        --machine_rank "$MACHINE_RANK" \
        --deepspeed_multinode_launcher standard \
        SFT_stage1.py \
        --experiment_name "$EXPERIMENT_NAME" \
        --model_path "$MODEL_PATH" \
        --data_path "$DATA_PATH" \
        --output_dir "$OUTPUT_DIR" \
        --log_dir "$LOG_DIR" \
        --max_seq_len "$MAX_SEQ_LEN" \
        --train_bsz_per_gpu "$TRAIN_BSZ_PER_GPU" \
        --gradient_accumulation_steps "$GRADIENT_ACCUMULATION_STEPS" \
        --learning_rate "$LEARNING_RATE" \
        --n_epochs "$N_EPOCHS" \
        --max_ckpts "$MAX_CKPTS" \
        --weight_decay "$WEIGHT_DECAY" \
        --warmup_rates "$WARMUP_RATES"
else
    echo "Using single-GPU configuration"

    accelerate launch \
        --num_processes 1 \
        --mixed_precision bf16 \
        SFT_stage1.py \
        --experiment_name "$EXPERIMENT_NAME" \
        --model_path "$MODEL_PATH" \
        --data_path "$DATA_PATH" \
        --output_dir "$OUTPUT_DIR" \
        --log_dir "$LOG_DIR" \
        --max_seq_len "$MAX_SEQ_LEN" \
        --train_bsz_per_gpu "$TRAIN_BSZ_PER_GPU" \
        --gradient_accumulation_steps "$GRADIENT_ACCUMULATION_STEPS" \
        --learning_rate "$LEARNING_RATE" \
        --n_epochs "$N_EPOCHS" \
        --max_ckpts "$MAX_CKPTS" \
        --weight_decay "$WEIGHT_DECAY" \
        --warmup_rates "$WARMUP_RATES"
fi

# ============================================================================
# POST-TRAINING
# ============================================================================

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================================================"
    echo -e "${GREEN}✓ Training completed successfully!${NC}"
    echo "================================================================================"
    echo ""
    echo "Your trained model checkpoints are saved in: $OUTPUT_DIR"
    echo ""
    echo "To find your latest checkpoint:"
    echo "  ls -lt $OUTPUT_DIR/"
    echo ""
    echo "Next steps:"
    echo "  1. Test your model with inference"
    echo "  2. Evaluate on test datasets"
    echo "  3. Proceed to Stage 2 (RL training) if desired"
    echo ""
    echo "================================================================================"
else
    echo ""
    echo "================================================================================"
    echo -e "${RED}❌ Training failed. Please check the error messages above.${NC}"
    echo "================================================================================"
    echo ""
    echo "Common issues:"
    echo "  - CUDA out of memory: Reduce --train_bsz_per_gpu or --max_seq_len"
    echo "  - Model not found: Check HuggingFace access and login (huggingface-cli login)"
    echo "  - Data format error: Verify your data file format"
    echo ""
    exit 1
fi
