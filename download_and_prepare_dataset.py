#!/usr/bin/env python3
"""
Download and prepare the FreedomIntelligence/medical-o1-reasoning-SFT dataset for Stage 1 training.

This script:
1. Downloads the dataset from HuggingFace
2. Converts it to the required JSON format
3. Saves it to the data directory
"""

import json
import os
from datasets import load_dataset
from tqdm import tqdm
import argparse


def download_and_prepare_dataset(output_dir='./data', subset='en', split='train'):
    """
    Download and prepare the medical-o1-reasoning-SFT dataset.

    Args:
        output_dir: Directory to save the processed dataset
        subset: Dataset subset - 'en' for English or 'zh' for Chinese
        split: Dataset split (default: 'train')
    """
    print("=" * 80)
    print("Downloading FreedomIntelligence/medical-o1-reasoning-SFT dataset...")
    print("=" * 80)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Download the dataset from HuggingFace
    print(f"\n📥 Loading dataset subset '{subset}' (split: {split})...")
    print("This may take a few minutes depending on your internet connection.\n")

    try:
        dataset = load_dataset(
            "FreedomIntelligence/medical-o1-reasoning-SFT",
            subset,
            split=split
        )
        print(f"✓ Successfully loaded {len(dataset)} samples!\n")
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have an internet connection")
        print("2. Install datasets library: pip install datasets")
        print("3. Try running: huggingface-cli login (if authentication is needed)")
        return None

    # Convert to the required format
    print("=" * 80)
    print("Converting to training format...")
    print("=" * 80)

    processed_data = []

    for idx, sample in enumerate(tqdm(dataset, desc="Processing samples")):
        # The dataset has fields: Question, Complex_CoT, Response
        # We keep them as-is since SFT_stage1.py supports both formats
        processed_sample = {
            "Question": sample["Question"],
            "Complex_CoT": sample["Complex_CoT"],
            "Response": sample["Response"]
        }
        processed_data.append(processed_sample)

    # Save the processed dataset
    output_filename = f"medical_o1_sft_{subset}_data.json"
    output_path = os.path.join(output_dir, output_filename)

    print(f"\n💾 Saving processed dataset to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("✓ Dataset preparation complete!")
    print("=" * 80)
    print(f"📊 Total samples: {len(processed_data)}")
    print(f"📁 Saved to: {output_path}")
    print(f"💾 File size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")
    print("=" * 80)

    # Show a sample
    print("\n📝 Sample data (first entry):")
    print("-" * 80)
    print(f"Question: {processed_data[0]['Question'][:200]}...")
    print(f"\nComplex_CoT: {processed_data[0]['Complex_CoT'][:200]}...")
    print(f"\nResponse: {processed_data[0]['Response'][:200]}...")
    print("-" * 80)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Download and prepare medical-o1-reasoning-SFT dataset'
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        default='./data',
        help='Output directory for processed dataset (default: ./data)'
    )
    parser.add_argument(
        '--subset',
        type=str,
        default='en',
        choices=['en', 'zh'],
        help='Dataset subset: "en" for English, "zh" for Chinese (default: en)'
    )
    parser.add_argument(
        '--split',
        type=str,
        default='train',
        help='Dataset split to download (default: train)'
    )

    args = parser.parse_args()

    download_and_prepare_dataset(
        output_dir=args.output_dir,
        subset=args.subset,
        split=args.split
    )


if __name__ == '__main__':
    main()
