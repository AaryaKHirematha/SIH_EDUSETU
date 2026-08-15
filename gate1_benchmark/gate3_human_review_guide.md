# GATE 3: EduSetu Human Review Guide

## 1. Objective
You are a native speaker acting as a final human validator for the EduSetu educational translation pipeline. Your task is to evaluate the provided Hindi and Kannada translations and assign definitive **PASS / FAIL / UNCERTAIN** judgments across several distinct categories.

## 2. Review Methodology
Do not evaluate translation quality based solely on surface fluency or grammatical correctness. An educationally dangerous translation that reads fluently must still **FAIL**.

### Evaluating Formulas
- Check character-for-character exactness.
- Examples: `E = mc²`, `H₂O`, `F = ma`, `9.8 m/s²`.
- **FAIL** if sub/superscripts are flattened (e.g., `mc2` instead of `mc²`).
- **CRITICAL FAIL** if the formula is semantically altered or translated out of its symbolic form.

### Evaluating Technical Identifiers
- Check for exact preservation of Latin-script code and standards.
- Examples: `Python`, `HTML`, `CSS`, `API`.
- **FAIL** if they are transliterated or translated, altering their specific technical meaning.

### Evaluating Educational Terminology
- Check the precise scientific or mathematical mapping of the word.
- **CRITICAL FAIL** if "quadratic" is mapped to a geometry concept (like quadrilateral) instead of algebra (*वर्ग* / *द्विघात*).
- **CRITICAL FAIL** if "mass" is mapped to general weight rather than the specific physical quantity (*द्रव्यमान* / *ದ್ರವ್ಯರಾಶಿ*).

### Evaluating Grammar and Morphology
- **Hindi:** Judge gender, case, and syntax.
- **Kannada Morphology:** Carefully assess how case markers (`ಅನ್ನು`, `ನಲ್ಲಿ`, `ಗೆ`, `ರ`, etc.) attach to the root terminology. 
- **FAIL (Grammar)** if a suffix is awkwardly detached (e.g., `ಸಮೀಕರಣ ಅನ್ನು`) or malformed, *even if the terminology itself is correct*. However, note this separately from "Semantic Correctness".

### Evaluating Semantic Correctness
- **PASS** if the underlying scientific concept is perfectly conveyed.
- **IMPORTANT RULE:** A translation that preserves scientific meaning perfectly but has an awkward Kannada suffix should **FAIL** the "Grammar/Morphology" check but **PASS** the "Semantic Correctness" check. Do not intertwine grammar and science.

### Evaluating Hallucinations / Omissions / Additions
- **Hallucination (FAIL):** The model invented a concept, term, or formula not present in the English source.
- **Omission (FAIL):** The model dropped a critical fact, formula, or clause.
- **Addition (FAIL/UNCERTAIN):** The model added unnecessary explanatory words that were not in the source text.

### Evaluating Natural Fluency
- **PASS** if the sentence reads like high-quality textbook prose, rather than a direct, clunky machine translation.

## 3. How to Fill the Template
For each record in the JSON or CSV, leave the respective verdict fields (`human_hi_verdict`, `human_kn_verdict`, etc.) as **PASS**, **FAIL**, or **UNCERTAIN**. Use the `notes` field to explain any failures, specifically identifying which token or rule failed.
