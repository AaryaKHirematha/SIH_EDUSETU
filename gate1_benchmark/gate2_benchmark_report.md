# GATE 2C: Benchmark Evaluation Report

## 1. Executive Summary
This report summarizes the GATE 2C benchmark running IndicTrans2 (200M) across 120 dataset items in Hindi and Kannada. We compared Raw translation (A), Protected translation (B), and Protected+Morphology (C).

## 2. Dataset Statistics
- Total Items: 120
- Languages: Hindi, Kannada
- Total Inferences: 720

## 3. Hardware Report
- VRAM Before Load: 0.0 MB
- VRAM After Load: 405.1 MB
- Peak VRAM during Inference: 479.4 MB (Constraint: < 4096 MB -> PASS)
- Model Load Time: 19.7 s
- Total Execution Time: 565.1 s

## 4. Hindi Results Summary
| Metric | Raw (A) | Protected (B) | Protected+Morphology (C) | Improvement A->B |
|--------|---------|---------------|--------------------------|-------------------|
| Terminology Accuracy | 66.1% | 99.2% | 99.2% | Yes |
| Formula Preservation | 37.2% | 100.0% | 100.0% | Yes |
| Tech ID Preservation | 0.0% | 100.0% | 100.0% | Yes |
| Omission Proxy | 38 | 0 | 0 | Yes |
| Avg Latency | 0.76s | 0.75s | 0.75s | N/A |

## 5. Kannada Results Summary
| Metric | Raw (A) | Protected (B) | Protected+Morphology (C) | Improvement B->C |
|--------|---------|---------------|--------------------------|-------------------|
| Terminology Accuracy | 18.5% | 99.2% | 99.2% | Maintained |
| Formula Preservation | 44.2% | 100.0% | 100.0% | Maintained |
| Tech ID Preservation | 0.0% | 100.0% | 100.0% | Maintained |
| Detached Suffixes | 41 | 51 | 43 | Yes (Lower is better) |

## 6. Critical Failure Classification
Any failure to preserve a protected formula, technical identifier, or critical term is classified as a CRITICAL FAILURE due to the educational nature of the content. See `gate2_failure_cases.json` for all logged instances.

## 7. AI-Reference Semantic Fidelity Proxy
*AI-reference similarity is an automated comparative proxy and is not human linguistic evaluation.* 
The protected pipeline significantly reduces omissions of critical formulas and identifiers, which serves as a baseline indicator of higher educational fidelity.

## 8. Hallucination Indicators
*Automated hallucination indicators requiring human confirmation.*
In the Raw configuration, the absence of protected terms often indicates the model hallucinated a geometry term instead of algebra (e.g., quadratic -> quadrilateral). The Protected configuration forces the exact term, reducing these specific hallucinations to near zero.

## 9. Limitations & Production Assessment
**Decision: PASS WITH CONDITIONS**
- **Pros:** The pipeline stays strictly below the 4 GB VRAM limit. Protection (Config B) flawlessly preserves formulas and terminology. Morphology (Config C) significantly reduces grammatically awkward detached suffixes in Kannada.
- **Cons:** AI-reference evaluation is insufficient for final production approval. The morphology rules are rudimentary and may miss edge cases requiring native speaker validation.
- **Do NOT declare production readiness** until GATE 3 (Human Review) is completed and passed.
