"""
Results Analysis Script for Masters Thesis
Compares Solution Guidance model against baselines on MedQA
"""

import json
import os
import glob
from collections import defaultdict


def load_results(file_path):
    """Load results from JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)


def extract_medqa_score(results):
    """Extract MedQA accuracy from results"""
    if isinstance(results, dict):
        for key in results.keys():
            if 'MedQA' in key or 'medqa' in key.lower():
                score_data = results[key]
                if isinstance(score_data, list) and len(score_data) >= 3:
                    # Format: [best_score, head_match, total_count, tail_match]
                    accuracy = score_data[0] * 100  # Convert to percentage
                    count = score_data[2]
                    return accuracy, count
    return None, None


def calculate_improvement(baseline, model):
    """Calculate improvement percentage"""
    if baseline and model:
        absolute_improvement = model - baseline
        relative_improvement = (absolute_improvement / baseline) * 100
        return absolute_improvement, relative_improvement
    return None, None


def find_result_files():
    """Find all result JSON files"""
    result_files = glob.glob("result_*.json")
    return result_files


def identify_model_type(filename):
    """Identify which model based on filename"""
    filename_lower = filename.lower()

    if 'solution' in filename_lower or 'llama-3.1-8b' in filename_lower:
        # Check if it's from checkpoint (your trained model)
        if 'checkpoint' in filename_lower or 'ckpt' in filename_lower:
            return 'Your Model (Llama3 + Solution Guidance)'
        # Or if it's the base model
        elif 'instruct' in filename_lower:
            return 'Baseline (Llama3-8B-Instruct)'

    if 'biomistral' in filename_lower or 'bio' in filename_lower:
        return 'BioMistral-7B'

    if 'llama' in filename_lower and 'instruct' in filename_lower:
        return 'Baseline (Llama3-8B-Instruct)'

    return filename  # Return filename if can't identify


def main():
    print("=" * 70)
    print("MASTERS THESIS - RESULTS ANALYSIS")
    print("Solution Guidance for Medical Reasoning")
    print("=" * 70)
    print()

    # Find all result files
    result_files = find_result_files()

    if not result_files:
        print("ERROR: No result files found!")
        print("Please run evaluations first.")
        return

    print(f"Found {len(result_files)} result file(s):")
    for f in result_files:
        print(f"  - {f}")
    print()

    # Load and organize results
    results = {}
    for file_path in result_files:
        model_name = identify_model_type(file_path)
        data = load_results(file_path)
        accuracy, count = extract_medqa_score(data)

        if accuracy is not None:
            results[model_name] = {
                'accuracy': accuracy,
                'count': count,
                'file': file_path
            }

    if not results:
        print("ERROR: Could not extract MedQA scores from result files!")
        return

    # Display results
    print("=" * 70)
    print("MEDQA EVALUATION RESULTS")
    print("=" * 70)
    print()

    # Sort by accuracy
    sorted_results = sorted(results.items(), key=lambda x: x[1]['accuracy'], reverse=True)

    for rank, (model_name, data) in enumerate(sorted_results, 1):
        print(f"{rank}. {model_name}")
        print(f"   Accuracy: {data['accuracy']:.2f}%")
        print(f"   Dataset size: {data['count']} questions")
        print(f"   Source file: {data['file']}")
        print()

    # Calculate improvements if we have baseline
    baseline_models = [name for name in results.keys() if 'Baseline' in name]
    your_models = [name for name in results.keys() if 'Your Model' in name or 'Solution Guidance' in name]

    if baseline_models and your_models:
        baseline_name = baseline_models[0]
        your_model_name = your_models[0]

        baseline_acc = results[baseline_name]['accuracy']
        your_acc = results[your_model_name]['accuracy']

        abs_imp, rel_imp = calculate_improvement(baseline_acc, your_acc)

        print("=" * 70)
        print("IMPROVEMENT ANALYSIS")
        print("=" * 70)
        print()
        print(f"Baseline ({baseline_name}):")
        print(f"  {baseline_acc:.2f}%")
        print()
        print(f"Your Model ({your_model_name}):")
        print(f"  {your_acc:.2f}%")
        print()
        print(f"Absolute Improvement: +{abs_imp:.2f} percentage points")
        print(f"Relative Improvement: +{rel_imp:.2f}%")
        print()

        if abs_imp >= 10:
            print("✅ SUCCESS! You achieved the 10% improvement target!")
        elif abs_imp >= 5:
            print("⚠️  GOOD! You achieved {:.1f}% improvement (target was 10%)".format(abs_imp))
        else:
            print("⚠️  Below target. Consider:")
            print("   - Training for more epochs")
            print("   - Using more training data")
            print("   - Adjusting learning rate")
        print()

    # Compare with BioMistral if available
    biomistral_models = [name for name in results.keys() if 'BioMistral' in name]
    if biomistral_models and your_models:
        biomistral_name = biomistral_models[0]
        your_model_name = your_models[0]

        biomistral_acc = results[biomistral_name]['accuracy']
        your_acc = results[your_model_name]['accuracy']

        print("=" * 70)
        print("COMPARISON WITH BIOMISTRAL-7B")
        print("=" * 70)
        print()
        print(f"BioMistral-7B: {biomistral_acc:.2f}%")
        print(f"Your Model:    {your_acc:.2f}%")
        print()

        if your_acc > biomistral_acc:
            diff = your_acc - biomistral_acc
            print(f"✅ Your model outperforms BioMistral by +{diff:.2f}%!")
        elif your_acc > biomistral_acc - 2:
            print("✅ Your model is competitive with BioMistral!")
        else:
            diff = biomistral_acc - your_acc
            print(f"⚠️  BioMistral is ahead by +{diff:.2f}%")
        print()

    # Generate LaTeX table for thesis
    print("=" * 70)
    print("LATEX TABLE FOR THESIS")
    print("=" * 70)
    print()
    print(r"\begin{table}[h]")
    print(r"\centering")
    print(r"\caption{Performance Comparison on MedQA Dataset}")
    print(r"\begin{tabular}{lc}")
    print(r"\hline")
    print(r"Model & Accuracy (\%) \\")
    print(r"\hline")

    for model_name, data in sorted_results:
        # Clean up model name for LaTeX
        clean_name = model_name.replace('_', r'\_')
        print(f"{clean_name} & {data['accuracy']:.2f} \\\\")

    print(r"\hline")
    print(r"\end{tabular}")
    print(r"\label{tab:results}")
    print(r"\end{table}")
    print()

    # Save summary to file
    summary_file = "THESIS_RESULTS_SUMMARY.txt"
    with open(summary_file, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("MASTERS THESIS - RESULTS SUMMARY\n")
        f.write("Solution Guidance for Medical Reasoning\n")
        f.write("=" * 70 + "\n\n")

        f.write("MEDQA EVALUATION RESULTS\n")
        f.write("-" * 70 + "\n")
        for rank, (model_name, data) in enumerate(sorted_results, 1):
            f.write(f"{rank}. {model_name}: {data['accuracy']:.2f}%\n")

        if baseline_models and your_models:
            f.write("\nIMPROVEMENT OVER BASELINE\n")
            f.write("-" * 70 + "\n")
            f.write(f"Baseline: {baseline_acc:.2f}%\n")
            f.write(f"Your Model: {your_acc:.2f}%\n")
            f.write(f"Absolute Improvement: +{abs_imp:.2f} percentage points\n")
            f.write(f"Relative Improvement: +{rel_imp:.2f}%\n")

        if biomistral_models and your_models:
            f.write("\nCOMPARISON WITH BIOMISTRAL-7B\n")
            f.write("-" * 70 + "\n")
            f.write(f"BioMistral-7B: {biomistral_acc:.2f}%\n")
            f.write(f"Your Model: {your_acc:.2f}%\n")
            f.write(f"Difference: {your_acc - biomistral_acc:+.2f}%\n")

    print(f"Summary saved to: {summary_file}")
    print()
    print("=" * 70)
    print("ANALYSIS COMPLETE!")
    print("Use these results for your thesis writeup.")
    print("=" * 70)


if __name__ == "__main__":
    main()
