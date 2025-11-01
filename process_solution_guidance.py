#!/usr/bin/env python3
"""
Process the medical-o1-reasoning-SFT dataset to convert Complex_CoT to Solution_Guidance format.
This script:
1. Removes informal/bloat language
2. Segments reasoning into logical steps
3. Numbers the steps
4. Maintains medical accuracy while improving clarity
"""

import json
import re
from typing import Dict, List
import argparse


class SolutionGuidanceProcessor:
    """Processes Complex CoT into cleaner Solution Guidance format"""

    # Handle both ASCII apostrophe (') and Unicode right single quotation mark (')
    APOS = r"['\u2019]"

    # Bloat words/phrases to remove or replace
    BLOAT_PATTERNS = [
        # Complete phrase removals at sentence start (most specific first)
        (rf'^\s*Alright,?\s+let{APOS}s start by looking at\s+', 'Looking at ', re.IGNORECASE),
        (rf'^\s*Okay,?\s+let{APOS}s think about\s+', '', re.IGNORECASE),
        (rf'^\s*Now,?\s+let{APOS}s consider\s+', 'Considering ', re.IGNORECASE),

        # Starting phrases (at beginning of sentence/paragraph)
        (r'^\s*Alright,?\s+', ''),
        (r'^\s*Okay,?\s+', ''),
        (r'^\s*So,?\s+', ''),
        (r'^\s*Now,?\s+', ''),
        (r'^\s*Well,?\s+', ''),

        # After periods (new sentence starters)
        (r'\.\s+Alright,?\s+', '. '),
        (r'\.\s+Okay,?\s+', '. '),
        (rf'\.\s+So,?\s+I{APOS}d say,?\s+considering\s+', '. Considering '),
        (rf'\.\s+So,?\s+I{APOS}d say,?\s+', '. '),
        (r'\.\s+So,?\s+considering\s+', '. Considering '),
        (r'\.\s+So,?\s+', '. '),
        (r'\.\s+Now,?\s+', '. '),
        (r'\.\s+Well,?\s+', '. '),
        (r'\.\s+But wait,?\s+', '. But '),

        # Specific phrase patterns before general removals
        (r'[Hh]mm,?\s+this makes me reconsider\.\s*', 'Reconsidering this: ', re.IGNORECASE),
        (r'this makes me reconsider\.\s*', 'Reconsidering: ', re.IGNORECASE),
        (r'makes me think the problem\s+', 'suggests the problem ', re.IGNORECASE),
        (r'makes me think\s+that\s+', 'suggests ', re.IGNORECASE),
        (r'makes me think\s+the\s+', 'suggests the ', re.IGNORECASE),
        (r'makes me think\s+', 'suggests ', re.IGNORECASE),

        # Thinking phrases (case insensitive)
        (rf"let{APOS}s see,?\s+", '', re.IGNORECASE),
        (rf"let{APOS}s think\s+about\s+possible\s+scenarios\.\s+", 'Possible scenarios: ', re.IGNORECASE),
        (rf"let{APOS}s think\s+about\s+possible\s+", 'Possible ', re.IGNORECASE),
        (rf"let{APOS}s think\s+about\s+", '', re.IGNORECASE),
        (rf"let{APOS}s start\s+by\s+looking at\s+", 'Looking at ', re.IGNORECASE),
        (rf"let{APOS}s figure this out\.?\s*", '', re.IGNORECASE),
        (rf"let{APOS}s dive into\s+", '', re.IGNORECASE),
        (rf"let{APOS}s consider\s+some\s+", 'Considering ', re.IGNORECASE),
        (rf"let{APOS}s consider\s+", 'Considering ', re.IGNORECASE),

        # I-statements
        (r"\bI think\s+that\s+", '', re.IGNORECASE),
        (r"\bI think\s+", '', re.IGNORECASE),
        (rf"\bI{APOS}d say,?\s+considering\s+everything,?\s+", 'Considering everything, ', re.IGNORECASE),
        (rf"\bI{APOS}d say,?\s+considering\s+", 'Considering ', re.IGNORECASE),
        (rf"\bI{APOS}d say,?\s+", '', re.IGNORECASE),

        # Interjections
        (r'[Hh]mm,?\s+', ''),
        (r'[Oo]h,?\s+and\s+', 'Additionally, '),
        (r'[Oo]h,?\s+', ''),
        (r'[Ww]ait,?\s+', ''),
        (r'\bBut wait,\s+', 'But ', re.IGNORECASE),

        # Mid-sentence fillers
        (r'\s+kind of\s+', ' '),
        (r'\s+really\s+', ' '),
        (r'\s+pretty\s+', ' '),
        (r'\s+quite\s+', ' '),
        (r'\s+very\s+', ' '),
        (r'\s+definitely\s+', ' '),
        (r'\s+actually\s+', ' '),

        # Weak modal verbs - be conservative
        (r'\bcould be\s+', 'may be '),
        (r'\bmight be\s+', 'may be '),

        # Clean up extra spaces (do this last)
        (r'\s+', ' '),
        (r'^\s+', ''),
        (r'\s+$', ''),
    ]

    # Sentence starters that indicate new logical steps
    STEP_INDICATORS = [
        'looking at', 'considering', 'given', 'now', 'next',
        'the', 'this', 'these', 'moving on', 'turning to',
        'to calculate', 'to determine', 'to understand',
        'based on', 'in', 'for', 'when', 'if', 'however',
        'but', 'so', 'therefore', 'thus', 'hence',
    ]

    def __init__(self, min_step_length: int = 50):
        """
        Args:
            min_step_length: Minimum character length for a reasoning step
        """
        self.min_step_length = min_step_length

    def remove_bloat(self, text: str) -> str:
        """Remove bloat words and phrases from text"""
        # Split into paragraphs to clean each one
        paragraphs = re.split(r'\n\s*\n', text)

        cleaned_paragraphs = []
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # Apply bloat pattern replacements to each paragraph
            cleaned = para
            for pattern_tuple in self.BLOAT_PATTERNS:
                if len(pattern_tuple) == 3:
                    pattern, replacement, flags = pattern_tuple
                    cleaned = re.sub(pattern, replacement, cleaned, flags=flags)
                else:
                    pattern, replacement = pattern_tuple
                    cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)

            cleaned = cleaned.strip()
            if cleaned:
                cleaned_paragraphs.append(cleaned)

        # Join paragraphs back with double newlines
        result = '\n\n'.join(cleaned_paragraphs)
        return result

    def segment_into_steps(self, text: str) -> List[str]:
        """
        Segment reasoning text into logical steps.
        Uses paragraph breaks as primary delimiter - each paragraph = one step.
        This preserves coherent reasoning blocks.
        """
        # Split by paragraph breaks (double newlines or single newlines)
        # Medical reasoning often uses paragraph breaks to separate logical units
        paragraphs = re.split(r'\n\s*\n', text)

        steps = []
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # If paragraph is very short, merge with previous step
            if len(para) < self.min_step_length and steps:
                steps[-1] += ' ' + para
            else:
                steps.append(para)

        # Clean up steps
        steps = [s.strip() for s in steps if s.strip()]

        return steps

    def capitalize_first_letter(self, text: str) -> str:
        """Ensure first letter is capitalized"""
        if not text:
            return text
        return text[0].upper() + text[1:]

    def fix_sentence_capitalization(self, text: str) -> str:
        """Capitalize the first letter after sentence-ending punctuation"""
        # Find patterns like ". word" or "? word" or "! word" and capitalize
        import re

        def capitalize_match(match):
            punct = match.group(1)
            space = match.group(2)
            letter = match.group(3)
            rest = match.group(4)
            return punct + space + letter.upper() + rest

        # Pattern: (sentence-ending punct) + (spaces) + (lowercase letter) + (rest of word)
        text = re.sub(r'([.!?])(\s+)([a-z])(\w*)', capitalize_match, text)

        return text

    def process_complex_cot(self, complex_cot: str) -> str:
        """
        Main processing function: Convert Complex_CoT to Solution_Guidance

        Args:
            complex_cot: Original Complex CoT reasoning text

        Returns:
            Processed Solution Guidance text with numbered steps
        """
        # Step 1: Remove bloat language
        cleaned_text = self.remove_bloat(complex_cot)

        # Step 2: Fix sentence capitalization after bloat removal
        cleaned_text = self.fix_sentence_capitalization(cleaned_text)

        # Step 3: Segment into logical steps
        steps = self.segment_into_steps(cleaned_text)

        # Step 4: Format with step numbers
        formatted_steps = []
        for i, step in enumerate(steps, 1):
            # Ensure first letter is capitalized
            step = self.capitalize_first_letter(step)
            formatted_steps.append(f"Step {i}: {step}")

        # Join with double newlines for readability
        solution_guidance = '\n\n'.join(formatted_steps)

        return solution_guidance

    def process_dataset(self, input_path: str, output_path: str, limit: int = None):
        """
        Process entire dataset

        Args:
            input_path: Path to input JSON file
            output_path: Path to output JSON file
            limit: Optional limit on number of records to process
        """
        print(f"Loading dataset from {input_path}...")
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if limit:
            data = data[:limit]
            print(f"Processing {limit} records (limited)...")
        else:
            print(f"Processing {len(data)} records...")

        processed_data = []
        for i, record in enumerate(data):
            if (i + 1) % 10 == 0:
                print(f"  Processed {i + 1}/{len(data)} records...")

            # Create new record with Solution_Guidance
            new_record = record.copy()

            # Process Complex_CoT to Solution_Guidance
            if 'Complex_CoT' in record:
                solution_guidance = self.process_complex_cot(record['Complex_CoT'])
                new_record['Solution_Guidance'] = solution_guidance

                # Optionally keep original for comparison
                # new_record['Complex_CoT_Original'] = record['Complex_CoT']

                # Remove Complex_CoT (replaced with Solution_Guidance)
                del new_record['Complex_CoT']

            processed_data.append(new_record)

        # Save processed dataset
        print(f"\nSaving processed dataset to {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)

        print(f"✓ Processing complete! Saved {len(processed_data)} records.")

        return processed_data

    def compare_samples(self, original: str, processed: str):
        """Print comparison of original vs processed"""
        print("\n" + "="*80)
        print("ORIGINAL COMPLEX_COT:")
        print("="*80)
        print(original[:800] + "...\n")

        print("="*80)
        print("PROCESSED SOLUTION_GUIDANCE:")
        print("="*80)
        print(processed[:800] + "...\n")

        print("="*80)
        print(f"Length: {len(original)} → {len(processed)} chars "
              f"({(len(processed)/len(original)*100):.1f}%)")
        print("="*80)


def main():
    parser = argparse.ArgumentParser(
        description='Process medical reasoning dataset to Solution Guidance format'
    )
    parser.add_argument(
        '--input',
        type=str,
        default='./data/demo_data.json',
        help='Input JSON file path'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='./data/solution_guidance_data.json',
        help='Output JSON file path'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit number of records to process (for testing)'
    )
    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview transformation on first sample only'
    )
    parser.add_argument(
        '--min-step-length',
        type=int,
        default=50,
        help='Minimum character length for a reasoning step'
    )

    args = parser.parse_args()

    processor = SolutionGuidanceProcessor(min_step_length=args.min_step_length)

    if args.preview:
        # Preview mode: show transformation on first sample
        print("PREVIEW MODE: Showing transformation on first sample\n")
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)

        sample = data[0]
        original = sample['Complex_CoT']
        processed = processor.process_complex_cot(original)

        processor.compare_samples(original, processed)
    else:
        # Full processing mode
        processor.process_dataset(args.input, args.output, limit=args.limit)


if __name__ == '__main__':
    main()
