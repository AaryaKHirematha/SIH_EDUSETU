# GATE 3: Validation Plan Summary

## 1. Motivation
The Gate 2C Automated Benchmark proved that while the base IndicTrans2 model struggles significantly with formulas and terminology (especially geometry/algebra hallucinations in Kannada), the Protected Pipeline completely resolves formula dropping and term hallucination. However, the automated benchmark concluded with a **PASS WITH CONDITIONS** because the morphology handling in Kannada is rule-based and produced some edge cases. Gate 3 transitions the pipeline to Human Validation to obtain ground-truth assessments of morphology, grammar, and semantic safety that AI-proxies cannot guarantee.

## 2. Validation Package Scope
- **Number of Selected Cases:** 114 items (from the original 120-item dataset).
- **Domain Distribution:** Physics, Mathematics, Chemistry, Biology, and Computer Science are all heavily represented.
- **Hindi/Kannada Distribution:** All 114 items require validation in *both* Hindi and Kannada.
- **Content:** Each record exposes the Raw model output, Protected output, and Protected+Morphology output, juxtaposed with the AI-Reference translation.

## 3. Selection Methodology
The 114 validation cases were programmatically filtered to capture the highest-risk scenarios based on Gate 2C data:
- Every instance where a formula, technical identifier, or critical terminology token failed in the Raw model.
- Every known high-risk terminology token from the core syllabus (`mass`, `force`, `acceleration`, `quadratic equation`, `derivative`, etc.).
- A sampling of flawless baseline runs to act as experimental controls for the human reviewers.

## 4. Reviewer Instructions & Constraints
Reviewers must act independently. The provided AI references are explicitly marked as automated baselines, not human ground-truth. Reviewers are forbidden from accepting translations based purely on surface fluency. The primary assessment is **Educational Integrity** (scientific exactness, unflattened formulas, correct mathematical term mappings). Detailed instructions are provided in `gate3_human_review_guide.md`.

## 5. Acceptance Criteria
The EduSetu translation architecture will achieve a final **PASS** (cleared for production) if:
- The human reviewers validate that the Protected Pipeline (Config B for Hindi, Config C for Kannada) eliminates all semantic Critical Failures.
- The Kannada morphology rules are deemed sufficiently natural for educational reading, or the edge cases are documented for a final code-fix.

## 6. Limitations
Human validation is slow and subjective. While reviewers are given strict pass/fail rubrics, minor stylistic disagreements on "natural fluency" may occur. The focus must remain steadfastly on educational safety (i.e., avoiding hallucinations and concept alterations).
