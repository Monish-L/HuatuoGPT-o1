# ReasonMed vs HuatuoGPT-o1: Comprehensive Comparison

## Overview

This document analyzes the ReasonMed appendix (Appendix H) and compares it with HuatuoGPT-o1's approach to medical reasoning.

---

## 1. FUNDAMENTAL DIFFERENCES

### Paper Type & Focus

**ReasonMed:**
- **Type:** Dataset paper ("A 370K Multi-Agent Generated Dataset")
- **Focus:** Creating diverse medical reasoning datasets using multiple agent types
- **Goal:** Provide training data for medical QA systems

**HuatuoGPT-o1:**
- **Type:** Model/Method paper
- **Focus:** Advanced medical reasoning with LLMs through verifier-guided search
- **Goal:** Build models that can identify mistakes, explore alternatives, and refine answers

---

## 2. STRUCTURE OF THE REASONMED APPENDIX

### What the Appendix Shows

The appendix (H) demonstrates:

1. **Transparency Declaration**
   - Explicitly states outputs are "single-run, non-cherry-picked examples"
   - Acknowledges variability as a problem, not a feature
   - Mentions future RL development to address inconsistency

2. **Three Model Variants**
   - **ReasonMed:** Primary reasoning model with detailed step-by-step analysis
   - **CoTMed:** Chain-of-Thought specialized model
   - **ResponseMed:** More concise response model

3. **Temperature Variation Testing**
   - Each model tested at temperatures: 0.4, 0.5, 0.6
   - Shows how same model gives different (often contradictory) answers

4. **The Example Problem**
   ```
   Question: Which of the following is not true about glomerular capillaries?
   A. Oncotic pressure of fluid leaving < fluid entering
   B. Glucose concentration same in capillaries and filtrate
   C. Afferent arteriole constriction decreases blood flow
   D. Hematocrit of fluid leaving < fluid entering
   ```

---

## 3. KEY FINDING: VARIABILITY & INCONSISTENCY

### Answer Distribution Across Models/Temperatures

| Model | Temp 0.4 | Temp 0.5 | Temp 0.6 |
|-------|----------|----------|----------|
| **ReasonMed** | B (glucose) | B (glucose) | D (hematocrit) |
| **CoTMed** | A (oncotic) | B (glucose) | B (glucose) |
| **ResponseMed** | A (oncotic) | A (oncotic) | D (hematocrit) |

### Critical Observation

**The same model gives different answers at different temperatures!** This reveals:

1. **Reasoning Instability:** Models aren't converging to consistent logic
2. **Temperature Sensitivity:** Small sampling changes produce contradictory conclusions
3. **Knowledge Uncertainty:** Models may not have robust medical understanding

### Correct Answer Analysis

The question has multiple interpretation issues:
- **Statement A** is technically incorrect (oncotic pressure increases, not decreases)
- **Statement B** is true (glucose freely filtered initially)
- **Statement D** could be interpreted differently based on what "fluid" means

The variability suggests models are struggling with:
- Precise medical terminology interpretation
- Distinguishing between glomerular filtrate vs. capillary blood
- Understanding temporal aspects (initial filtration vs. post-reabsorption)

---

## 4. REASONMED'S REASONING STRUCTURE

### 6-Step Format

All ReasonMed variants use this structured approach:

```
1. Restate the question
   → Clarify what's being asked

2. Key clinical details and background
   → Establish domain knowledge context

3. Evaluate each candidate answer
   → Systematically analyze all options

4. Rule out options that don't align
   → Eliminate clearly incorrect choices

5. Compare remaining choices
   → Detailed comparison of viable options

6. Final answer
   → Conclusion with justification
```

### Example (ReasonMed @ 0.4):

```
1. Restate: "Identify which statement about glomerular capillaries is incorrect"

2. Key details:
   - Glomerular capillaries filter blood
   - Oncotic pressure from proteins
   - Glucose actively reabsorbed in proximal tubule
   - Afferent arterioles supply blood

3. Evaluate:
   - Option A: True (proteins filtered out, reducing oncotic pressure)
   - Option B: FALSE (glucose reabsorbed, so lower in filtrate)
   - Option C: True (constriction reduces flow)
   - Option D: True (proteins filtered out, reducing hematocrit)

4-5. Rule out A, C, D as true statements

6. Final Answer: B (glucose concentration statement is false)
```

### Strengths of This Format

✅ **Systematic:** Forces comprehensive evaluation
✅ **Transparent:** Shows reasoning process
✅ **Educational:** Each step has pedagogical value
✅ **Auditable:** Easy to identify where reasoning went wrong

### Weaknesses

❌ **No self-verification:** Doesn't check its own conclusion
❌ **No backtracking:** Can't revise earlier wrong assumptions
❌ **Linear:** Doesn't explore alternative reasoning paths
❌ **No external validation:** Relies solely on model's internal knowledge

---

## 5. HUATUOGPT-O1'S APPROACH

### Core Innovation: Verifier-Guided Search

HuatuoGPT-o1 solves the variability problem through:

1. **Tree Search with Verification**
   - Explores multiple reasoning paths (not just one linear path)
   - Uses a medical verifier to check conclusions
   - Backtracks when verification fails

2. **Three Action Types**
   ```json
   {
     "CoT": [
       {"action": "Inner Thinking", "title": "...", "content": "..."},
       {"action": "Final Conclusion", "content": "..."},
       {"action": "Verification", "content": "..."}
     ]
   }
   ```

3. **Iterative Refinement**
   - If verification fails → backtrack to "Inner Thinking"
   - Generate alternative reasoning paths
   - Re-verify until correct answer found

### Key Differences from ReasonMed

| Aspect | ReasonMed | HuatuoGPT-o1 |
|--------|-----------|--------------|
| **Search Strategy** | Single linear path | Tree search with backtracking |
| **Verification** | None (implicit in final step) | Explicit verifier model |
| **Error Recovery** | None (one-shot generation) | Backtracking when wrong |
| **Training Data** | Pre-generated reasoning samples | Complex paths from search process |
| **RL Integration** | Mentioned as future work | Core component (Stage 2 PPO) |
| **Output Format** | Natural language steps | JSON-structured actions |

---

## 6. TRAINING METHODOLOGY COMPARISON

### ReasonMed (Inferred from Appendix)

```
1. Generate diverse reasoning examples using GPT-4o
2. Create 370K samples with different:
   - Model variants (ReasonMed, CoTMed, ResponseMed)
   - Temperature settings
   - Reasoning styles
3. Train models on this dataset (supervised learning)
4. [Future] Use RL to improve consistency
```

**Strengths:**
- Large-scale dataset diversity
- Multiple reasoning styles
- Shows realistic model behavior

**Weaknesses:**
- Training on inconsistent data may learn inconsistency
- No explicit mechanism to prefer correct reasoning paths
- Variability is documented but not solved

### HuatuoGPT-o1

```
Stage 1: Supervised Fine-Tuning (SFT)
├─ Input: Verifiable medical problems (with ground truth)
├─ Process: Search for complex reasoning paths using GPT-4o
│  ├─ Generate initial CoT
│  ├─ Verify with verifier model
│  ├─ If wrong: backtrack and try alternative reasoning
│  └─ Keep only successful reasoning paths
└─ Output: High-quality complex CoT + Response pairs

Stage 2: Reinforcement Learning (PPO)
├─ Policy Model: HuatuoGPT-o1 (from Stage 1)
├─ Reward Model: Medical verifier (3B model)
├─ Value Model: LLaMA-3.2-3B
├─ Process:
│  ├─ Generate reasoning for medical problems
│  ├─ Verifier scores correctness
│  ├─ PPO optimizes for higher verifier scores
│  └─ Model learns to consistently reach correct answers
└─ Output: Refined model with improved consistency
```

**Key Innovations:**

1. **Verifiable Problems:**
   - Only uses problems with definitive ground truth
   - Enables objective verification

2. **Search Process:**
   - Actively explores reasoning space
   - Only keeps paths that lead to correct answers
   - Creates training data from successful searches

3. **Verifier-Based Rewards:**
   - Medical verifier provides objective feedback
   - RL optimizes for correctness, not just fluency
   - Reduces hallucination through grounded rewards

---

## 7. OUTPUT FORMAT COMPARISON

### ReasonMed Format

```
## Thinking
To answer this question, let's break down the components step-by-step:

1. Restate the question: ...
2. Key clinical details and relevant background information: ...
3. Evaluate each candidate answer: ...
4. Rule out options that do not align with the clinical context: ...
5. Compare any remaining choices: ...
6. Final answer: ...

[Summary paragraph]
```

**Characteristics:**
- Natural language throughout
- Pedagogical structure
- Human-readable
- Not easily parseable by machines

### HuatuoGPT-o1 Format

```json
{
  "CoT": [
    {
      "action": "Inner Thinking",
      "title": "Understanding glomerular filtration basics",
      "content": "The glomerulus filters blood through three layers..."
    },
    {
      "action": "Inner Thinking",
      "title": "Analyzing oncotic pressure changes",
      "content": "As plasma proteins are too large to filter..."
    },
    {
      "action": "Final Conclusion",
      "content": "The incorrect statement is A because oncotic pressure increases, not decreases"
    },
    {
      "action": "Verification",
      "content": "Checking: Oncotic pressure is determined by protein concentration. As water and small molecules filter out, protein concentration in remaining blood increases. Therefore oncotic pressure of fluid leaving capillaries > entering. Statement A claims the opposite. Verification: CORRECT"
    }
  ]
}
```

Then rendered as:

```
## Thinking
[Inner Thinking steps with titles]
...

## Final Response
[Extracted from Final Conclusion]
```

**Characteristics:**
- Structured JSON internally
- Machine-parseable
- Clear action types
- Explicit verification step
- Human-readable rendering

---

## 8. THE VERIFICATION PROBLEM

### ReasonMed's Implicit Verification

Looking at the examples, ReasonMed models make critical errors:

**ReasonMed @ 0.4 (Answer: B - glucose)**
```
"Glucose concentration in the capillaries is the same as that in glomerular
filtrate": This is false. Glucose is actively reabsorbed in the proximal
tubule, so its concentration in the filtrate is lower than in the capillaries.
```

**Error:** Confuses initial filtration with post-reabsorption. At the point of glomerular filtration, glucose concentration IS the same (freely filtered). Reabsorption happens AFTER in the proximal tubule.

**ResponseMed @ 0.4 (Answer: A - oncotic)**
```
"The oncotic pressure of the fluid leaving the capillaries is less than that
of fluid entering it": This is incorrect because the oncotic pressure
increases as proteins are retained in the capillaries.
```

**Correct reasoning!** As fluid filters out, protein concentration in blood increases, raising oncotic pressure.

### HuatuoGPT-o1's Explicit Verification

From `search_for_complex_reasoning_path.py`:

```python
verify_prompt = """<Model Response>
{}
</Model Response>

<Reference Answer>
{}
</Reference Answer>

You are provided with a model-generated response and a reference answer.
Compare the model response with the reference answer and determine its
correctness. Your task is to simply output "True" if the response is
correct, and "False" otherwise."""
```

**Verification Process:**
1. Model generates reasoning + answer
2. Extract answer from response
3. Compare with ground truth
4. If False → trigger backtracking
5. If True → accept this reasoning path

**Backtracking Prompt:**
```python
gen_prompt_rethink_Backtracking = """
<previous reasoning>
{}
</previous reasoning>

Your task is to continue from the current 'Verification' step. I have
manually reviewed the reasoning and determined that the **Final Conclusion**
is false. Your 'Verification' results must align with mine. Proceed to
refine the reasoning using **backtracking** to revisit earlier points of
reasoning and construct a new Final Conclusion.
"""
```

This creates a **self-correcting loop** that ReasonMed lacks.

---

## 9. PRACTICAL IMPLICATIONS

### When ReasonMed Approach is Useful

✅ **Dataset Creation:** Generating diverse reasoning examples for training
✅ **Exploration:** Understanding different reasoning styles and approaches
✅ **Benchmarking:** Testing model robustness across temperatures
✅ **Analysis:** Identifying common reasoning patterns and failure modes

### When HuatuoGPT-o1 Approach is Superior

✅ **Production Deployment:** Need consistent, reliable medical answers
✅ **High-Stakes Decisions:** Medical advice where correctness is critical
✅ **Complex Reasoning:** Multi-step problems requiring verification
✅ **Iterative Refinement:** When you can afford search/verification cost

### Cost-Benefit Tradeoff

| Method | Inference Cost | Consistency | Accuracy | Use Case |
|--------|---------------|-------------|----------|----------|
| **ReasonMed** | Low (single pass) | Low (varies with temp) | Variable | Dataset generation, exploration |
| **HuatuoGPT-o1** | High (tree search + verification) | High | High | Production, high-stakes medical QA |

---

## 10. THE NUANCES YOU ASKED ABOUT

### Nuance 1: Transparency vs. Performance

**ReasonMed:**
- Shows "warts and all" - real model behavior including failures
- Acknowledges: "This practice supports scientific reproducibility and honest appraisal"
- Values: Transparency > Perfect results

**HuatuoGPT-o1:**
- Filters through search to find correct paths
- Shows: What the model CAN achieve with proper guidance
- Values: Correctness > Showing all attempts

### Nuance 2: The Role of Temperature

**ReasonMed's Discovery:**
Temperature affects not just creativity but **logical consistency**:
- 0.4: More conservative, but can still be wrong
- 0.5: Middle ground, but introduces more variability
- 0.6: More exploration, but less reliable conclusions

**HuatuoGPT-o1's Approach:**
Uses temperature strategically during search:
- Higher temperature for exploring alternative reasoning paths
- Verification filters out incorrect explorations
- Keeps diversity in "how to think" while ensuring correctness in "what to conclude"

### Nuance 3: What "Reasoning" Means

**ReasonMed:**
Reasoning = Structured articulation of thought process
- Focus on FORM (6-step structure)
- Pedagogical value (good for humans to follow)
- But form doesn't guarantee correctness

**HuatuoGPT-o1:**
Reasoning = Verified path to correct answer
- Focus on OUTCOME (correct answer via sound logic)
- Iterative refinement (more like human expert problem-solving)
- Form serves verification, not just presentation

### Nuance 4: The Medical Knowledge Gap

Both papers reveal a fundamental challenge:

**The Problem:**
Medical questions often require:
1. Precise terminology understanding
2. Temporal reasoning (what happens when)
3. Multi-level system knowledge (molecular → organ → systemic)
4. Distinguishing similar but different concepts

**Example from the glomerular capillaries question:**
- "Fluid leaving capillaries" could mean:
  - Glomerular filtrate entering Bowman's capsule
  - Blood leaving via efferent arteriole
  - Fluid after tubular processing

Models struggle with this ambiguity.

**ReasonMed's Response:**
Show the variability, document the problem

**HuatuoGPT-o1's Response:**
Use verifier to ground answers in medical correctness

### Nuance 5: Future Convergence

ReasonMed states:
> "To mitigate this variability and improve reasoning consistency, we are
> developing a reinforcement learning approach tailored to medical QA that
> guides models toward more convergent, clinically accurate reasoning paths."

This is essentially **converging toward HuatuoGPT-o1's approach!**

Both teams recognize:
1. Supervised learning alone → inconsistent reasoning
2. Need for verification/rewards
3. RL as solution for convergence

---

## 11. TECHNICAL ARCHITECTURE COMPARISON

### ReasonMed (Inferred)

```
┌─────────────────────────────────────────────┐
│         Medical Question                    │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│    Model Selection (ReasonMed/CoT/Response) │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│    Generate Single Reasoning Path           │
│    (6-step structured format)               │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│    Extract Final Answer                     │
└─────────────────────────────────────────────┘

✗ No verification
✗ No backtracking
✗ No alternative path exploration
```

### HuatuoGPT-o1

```
┌─────────────────────────────────────────────┐
│      Verifiable Medical Problem             │
│      (with ground truth answer)             │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         SEARCH PROCESS (Training)           │
│  ┌─────────────────────────────────────┐   │
│  │ 1. Generate CoT reasoning           │   │
│  │ 2. Extract answer                   │   │
│  │ 3. Verify with ground truth         │   │
│  │ 4. If wrong → backtrack + rethink   │   │
│  │ 5. Repeat until correct             │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         STAGE 1: SFT                        │
│    Train on successful reasoning paths      │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         STAGE 2: PPO + Verifier             │
│  ┌─────────────────────────────────────┐   │
│  │ Policy: Generate reasoning          │   │
│  │ Reward: Verifier scores correctness │   │
│  │ Update: Optimize for high scores    │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│     INFERENCE (thinks-before-answers)       │
│     ## Thinking                             │
│     [Complex reasoning]                     │
│     ## Final Response                       │
│     [Answer]                                │
└─────────────────────────────────────────────┘

✓ Verification loop
✓ Backtracking capability
✓ Multi-path exploration
✓ Reward-guided optimization
```

---

## 12. KEY TAKEAWAYS

### What ReasonMed Teaches Us

1. **Raw model behavior is inconsistent** - even structured prompting doesn't guarantee reliability
2. **Temperature matters more than expected** - affects logical consistency, not just creativity
3. **Multiple reasoning styles exist** - ReasonMed/CoT/Response represent different approaches
4. **Transparency is valuable** - showing failures helps the field understand limitations

### What HuatuoGPT-o1 Teaches Us

1. **Verification is essential** - external grounding prevents hallucination
2. **Search > Single-pass** - exploring reasoning space finds better paths
3. **RL enables convergence** - rewards guide models toward consistent correctness
4. **Medical domain needs specialized tools** - general LLMs aren't enough

### The Papers Are Complementary

**ReasonMed:**
- Provides the DATA (370K examples showing diverse reasoning)
- Documents the PROBLEM (variability and inconsistency)
- Offers RESOURCES for training other models

**HuatuoGPT-o1:**
- Provides the METHOD (how to achieve consistent reasoning)
- Implements the SOLUTION (verifier + search + RL)
- Delivers MODELS ready for deployment

---

## 13. ANSWERING YOUR SPECIFIC QUESTION

> "How is it different from HuatuoGPT-o1 paper in comparison?"

### Core Differences Summary

| Dimension | ReasonMed | HuatuoGPT-o1 |
|-----------|-----------|--------------|
| **Paper Type** | Dataset paper | Model/method paper |
| **Main Contribution** | 370K reasoning examples | Verifier-guided reasoning method |
| **Reasoning Format** | 6-step natural language | JSON with Inner Thinking/Conclusion/Verification |
| **Verification** | None (implicit) | Explicit verifier model |
| **Training** | Supervised on diverse examples | SFT + RL with verifier rewards |
| **Error Handling** | Shows variability | Backtracking and correction |
| **Temperature Approach** | Documents instability | Uses strategically in search |
| **Consistency** | Variable (acknowledged problem) | High (through verification) |
| **Inference** | Single-pass generation | Can include self-verification |
| **Output Philosophy** | Show realistic model behavior | Show refined, correct reasoning |
| **Use Case** | Research, dataset creation | Production medical QA |
| **Transparency** | Explicit about failures | Filtered for correctness |
| **Future Direction** | Moving toward RL | Already implements RL |

### Philosophical Difference

**ReasonMed:** "Here's what happens when you ask models to reason - sometimes they get it right, sometimes wrong, and it varies with temperature. We're documenting this honestly."

**HuatuoGPT-o1:** "Here's how to make models reason consistently correctly - use verification to guide search and RL to learn from rewards."

---

## 14. VISUAL CONCEPTUAL MAP

```
MEDICAL REASONING LANDSCAPE

Raw LLM
   │
   ├─→ ReasonMed Approach
   │      ├─ Structured prompting (6 steps)
   │      ├─ Multiple model variants
   │      ├─ Temperature exploration
   │      └─ Result: Variable accuracy ❌
   │
   └─→ HuatuoGPT-o1 Approach
          ├─ Verifiable problems
          ├─ Search with verification
          ├─ Backtracking on errors
          ├─ SFT on successful paths
          ├─ RL with verifier rewards
          └─ Result: Consistent accuracy ✓

Both approaches recognize the same fundamental problem:
└─→ LLMs alone are inconsistent in complex medical reasoning

ReasonMed: Documents and quantifies the problem
HuatuoGPT-o1: Solves the problem through verification
```

---

## CONCLUSION

The ReasonMed appendix you shared is remarkably honest about model limitations, showing real variability across temperatures and model types. This transparency is valuable for understanding where current approaches fall short.

HuatuoGPT-o1 represents a solution to the exact problem ReasonMed documents: using verification and search to achieve consistent, correct medical reasoning despite the underlying model's potential for inconsistency.

**ReasonMed asks:** "What does medical reasoning look like in LLMs?"
**HuatuoGPT-o1 asks:** "How do we make medical reasoning reliable?"

Both are essential contributions to medical AI, approaching from complementary angles: documentation vs. solution, exploration vs. optimization, transparency vs. reliability.
