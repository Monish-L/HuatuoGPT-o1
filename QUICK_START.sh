#!/bin/bash
################################################################################
# QUICK START SCRIPT FOR MASTERS THESIS
# Solution Guidance for Medical Reasoning
################################################################################

set -e  # Exit on error

echo "=================================="
echo "SOLUTION GUIDANCE TRAINING"
echo "Masters Thesis Quick Start"
echo "=================================="
echo ""

# Check if running in correct directory
if [ ! -f "SFT_solution_guidance.py" ]; then
    echo "ERROR: Please run this script from the HuatuoGPT-o1 directory"
    exit 1
fi

# Function to check GPU
check_gpu() {
    echo "Checking GPU availability..."
    if ! command -v nvidia-smi &> /dev/null; then
        echo "ERROR: nvidia-smi not found. GPU required for training!"
        exit 1
    fi
    nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv
    echo ""
}

# Function to install dependencies
install_deps() {
    echo "Installing dependencies..."
    pip install -r requirements.txt
    pip install datasets wandb
    pip install sglang  # For inference
    echo "Dependencies installed!"
    echo ""
}

# Function to prepare training data
prepare_data() {
    echo "Preparing training data..."

    # Option 1: Use demo data (198 samples - FAST for testing)
    if [ -f "data/demo_data.json" ]; then
        echo "Using demo_data.json (198 samples)"
        TRAIN_DATA="data/demo_data.json"
    else
        echo "ERROR: data/demo_data.json not found!"
        exit 1
    fi

    # Option 2: Create a subset (uncomment if you want to download full dataset)
    # python3 -c "
    # from datasets import load_dataset
    # import json
    # print('Downloading full dataset...')
    # ds = load_dataset('FreedomIntelligence/medical-o1-reasoning-SFT', split='train')
    # print(f'Loaded {len(ds)} samples')
    # # Use 3000 samples for faster training
    # subset = ds.select(range(min(3000, len(ds))))
    # data = [item for item in subset]
    # with open('data/training_subset_3k.json', 'w') as f:
    #     json.dump(data, f, indent=2)
    # print('Created data/training_subset_3k.json')
    # "
    # TRAIN_DATA="data/training_subset_3k.json"

    echo "Training data: $TRAIN_DATA"
    echo ""
}

# Main menu
show_menu() {
    echo ""
    echo "What would you like to do?"
    echo "1. Check GPU and install dependencies"
    echo "2. Train model (1 GPU - takes 8-10 hours)"
    echo "3. Train model (8 GPUs - takes 2-3 hours)"
    echo "4. Evaluate trained model on MedQA"
    echo "5. Evaluate baseline (Llama3-8B-Instruct)"
    echo "6. Evaluate BioMistral-7B"
    echo "7. Full pipeline (train + evaluate all)"
    echo "8. Exit"
    echo ""
    read -p "Enter choice [1-8]: " choice
}

# Training functions
train_1gpu() {
    echo "Starting training on 1 GPU..."
    echo "This will take approximately 8-10 hours"
    echo "You can run this overnight!"
    echo ""

    check_gpu
    prepare_data

    CUDA_VISIBLE_DEVICES=0 python SFT_solution_guidance.py \
        --model_path meta-llama/Llama-3.1-8B-Instruct \
        --data_path ${TRAIN_DATA:-data/demo_data.json} \
        --output_dir ./ckpts \
        --experiment_name solution_guidance_medical \
        --n_epochs 2 \
        --train_bsz_per_gpu 1 \
        --gradient_accumulation_steps 16 \
        --learning_rate 2e-5 \
        --max_seq_len 2048 \
        2>&1 | tee training_log.txt

    echo ""
    echo "Training complete! Model saved in ./ckpts/solution_guidance_medical/"
}

train_8gpu() {
    echo "Starting training on 8 GPUs..."
    echo "This will take approximately 2-3 hours"
    echo ""

    check_gpu
    prepare_data

    accelerate launch --config_file ./configs/deepspeed_zero3.yaml \
        --num_processes 8 \
        --num_machines 1 \
        --machine_rank 0 \
        --deepspeed_multinode_launcher standard SFT_solution_guidance.py \
        --model_path meta-llama/Llama-3.1-8B-Instruct \
        --data_path ${TRAIN_DATA:-data/demo_data.json} \
        --output_dir ./ckpts \
        --experiment_name solution_guidance_medical \
        --n_epochs 3 \
        --train_bsz_per_gpu 1 \
        --gradient_accumulation_steps 16 \
        --learning_rate 5e-6 \
        2>&1 | tee training_log.txt

    echo ""
    echo "Training complete! Model saved in ./ckpts/solution_guidance_medical/"
}

# Evaluation functions
evaluate_trained() {
    echo "Evaluating YOUR trained model on MedQA..."

    # Find the latest checkpoint
    CHECKPOINT_DIR=$(ls -td ./ckpts/solution_guidance_medical/checkpoint-*/tfmr 2>/dev/null | head -1)

    if [ -z "$CHECKPOINT_DIR" ]; then
        echo "ERROR: No trained checkpoint found!"
        echo "Please train the model first (option 2 or 3)"
        exit 1
    fi

    echo "Using checkpoint: $CHECKPOINT_DIR"

    # Deploy model
    echo "Deploying model with sglang..."
    CUDA_VISIBLE_DEVICES=0 python -m sglang.launch_server \
        --model-path $CHECKPOINT_DIR \
        --port 28035 \
        --mem-fraction-static 0.8 \
        --dp 1 --tp 1 > sglang_trained.log 2>&1 &

    SERVER_PID=$!
    echo "Server starting... PID: $SERVER_PID"
    echo "Waiting for server to be ready (this may take 2-5 minutes)..."
    sleep 120

    # Run evaluation
    python evaluation/eval.py \
        --model_name $CHECKPOINT_DIR \
        --eval_file evaluation/data/eval_data.json \
        --port 28035

    # Kill server
    kill $SERVER_PID 2>/dev/null || true
    bash evaluation/kill_sglang_server.sh 2>/dev/null || true

    echo "Results saved! Check result_* files"
}

evaluate_baseline() {
    echo "Evaluating baseline Llama3-8B-Instruct on MedQA..."

    # Deploy model
    echo "Deploying baseline model..."
    CUDA_VISIBLE_DEVICES=0 python -m sglang.launch_server \
        --model-path meta-llama/Llama-3.1-8B-Instruct \
        --port 28035 \
        --mem-fraction-static 0.8 \
        --dp 1 --tp 1 > sglang_baseline.log 2>&1 &

    SERVER_PID=$!
    echo "Server starting... PID: $SERVER_PID"
    echo "Waiting for server to be ready..."
    sleep 120

    # Run evaluation
    python evaluation/eval.py \
        --model_name meta-llama/Llama-3.1-8B-Instruct \
        --eval_file evaluation/data/eval_data.json \
        --port 28035

    # Kill server
    kill $SERVER_PID 2>/dev/null || true
    bash evaluation/kill_sglang_server.sh 2>/dev/null || true

    echo "Baseline results saved!"
}

evaluate_biomistral() {
    echo "Evaluating BioMistral-7B on MedQA..."

    # Deploy model
    echo "Deploying BioMistral..."
    CUDA_VISIBLE_DEVICES=0 python -m sglang.launch_server \
        --model-path BioMistral/BioMistral-7B \
        --port 28035 \
        --mem-fraction-static 0.8 \
        --dp 1 --tp 1 > sglang_biomistral.log 2>&1 &

    SERVER_PID=$!
    echo "Server starting... PID: $SERVER_PID"
    echo "Waiting for server to be ready..."
    sleep 120

    # Run evaluation
    python evaluation/eval.py \
        --model_name BioMistral/BioMistral-7B \
        --eval_file evaluation/data/eval_data.json \
        --port 28035

    # Kill server
    kill $SERVER_PID 2>/dev/null || true
    bash evaluation/kill_sglang_server.sh 2>/dev/null || true

    echo "BioMistral results saved!"
}

full_pipeline() {
    echo "Running FULL PIPELINE..."
    echo "This will:"
    echo "1. Train your model (8-10 hours on 1 GPU)"
    echo "2. Evaluate your model"
    echo "3. Evaluate baseline"
    echo "4. Evaluate BioMistral"
    echo "5. Generate comparison report"
    echo ""
    read -p "Continue? This will take ~12-14 hours total [y/N]: " confirm

    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "Cancelled."
        return
    fi

    # Step 1: Train
    train_1gpu

    # Step 2: Evaluate all models
    evaluate_trained
    evaluate_baseline
    evaluate_biomistral

    # Step 3: Generate report
    echo ""
    echo "=================================="
    echo "ALL EVALUATIONS COMPLETE!"
    echo "=================================="
    echo ""
    echo "Your results are in:"
    ls -lh result_*.json
    echo ""
    echo "Now create comparison tables for your thesis!"
}

# Main loop
while true; do
    show_menu
    case $choice in
        1)
            check_gpu
            install_deps
            ;;
        2)
            train_1gpu
            ;;
        3)
            train_8gpu
            ;;
        4)
            evaluate_trained
            ;;
        5)
            evaluate_baseline
            ;;
        6)
            evaluate_biomistral
            ;;
        7)
            full_pipeline
            ;;
        8)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac

    read -p "Press Enter to continue..."
done
