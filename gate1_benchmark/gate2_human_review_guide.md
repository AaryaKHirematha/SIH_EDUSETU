# GATE 2: EduSetu Human Review Guide

This guide is for native-speaker educational reviewers tasked with validating translations for the EduSetu platform. Your primary responsibility is to ensure that the educational, mathematical, and scientific integrity of the content is preserved in Hindi and Kannada.

## Core Evaluation Dimensions

Please evaluate each translation across the following 12 dimensions:

1. **Semantic Fidelity:** Does the translated sentence mean exactly the same thing as the English source? Are the core educational concepts accurately represented?
2. **Mathematical Terminology:** Are mathematical concepts correctly translated?
3. **Scientific Terminology:** Are physics, chemistry, and biology concepts correctly translated?
4. **Formula Preservation:** Are equations (e.g., `F = ma`, `E = mc²`) preserved flawlessly? Look for flattened subscripts/superscripts.
5. **Units:** Are measurement units (e.g., `m/s²`, `kg`) preserved or correctly localized without losing physical meaning?
6. **Technical Identifiers:** Are programming languages, web standards, and software names (e.g., `Python`, `HTML`, `TensorFlow`) preserved exactly as written in English when required?
7. **Hindi Grammar:** Does the Hindi sentence use correct gender, number, and case markers?
8. **Kannada Grammar:** Does the Kannada sentence use correct syntax and morphological endings?
9. **Kannada Morphology:** Pay special attention to case markers and suffixes. Ensure that suffixes are naturally joined to the root words according to Kannada Sandhi rules, not awkwardly detached.
10. **Hallucinations:** Has the translation model invented any words, concepts, or symbols that are not present in the source text?
11. **Omissions:** Has the translation model dropped any critical facts, symbols, or clauses?
12. **Fluency:** Does the sentence read naturally to a student? Does it sound like high-quality textbook language rather than a robotic translation?

---

## 🚨 EXPLICIT WARNINGS FOR REVIEWERS 🚨

- **Grammar ≠ Science:** A grammatically fluent translation can still be scientifically WRONG. Do not pass a translation just because it reads smoothly.
- **Mathematical Specificity:** "Quadratic" must be evaluated as an algebraic concept (e.g., *ವರ್ಗ* / *द्विघात*), not by superficial or geometric similarity (e.g., *quadrilateral*).
- **Physical Quantities:** Physics terms like "mass" must be evaluated strictly as the physical quantity (*द्रव्यमान* / *ದ್ರವ್ಯರಾಶಿ*), not loosely as "weight".
- **Character-by-Character Formula Checks:** Equations must be checked character-by-character. `mc2` is not an acceptable substitute for `mc²`.
- **Chemical Integrity:** Chemical formulas (`H₂O`, `CO₂`) must not be altered, flattened, or transliterated.
- **Do Not Transliterate Code:** Identifiers like `Python`, `NumPy`, `HTML`, `CSS`, and `TensorFlow` should be preserved in the Latin script (English) unless local curriculum explicitly demands transliteration.
- **Holistic Morphology:** Kannada case markers and suffixes must be judged as part of the complete word and sentence context. A grammatically detached suffix (e.g., `ಪದ ಅನ್ನು`) is an error.

*Note: Do NOT prescribe a particular translation if you are acting as the independent creator of the reference text. Generate the most natural, accurate translation based on your pedagogical expertise.*

---

## Severity Scale

When logging errors or notes, classify the severity using the following scale:

- **CRITICAL:** Changes the educational, scientific, or mathematical meaning. The translation is unsafe for students.
- **MAJOR:** Significantly damages correctness, readability, or formatting (e.g., flattened equations, missing units), though the general concept might still be guessable.
- **MINOR:** A stylistic issue, slightly awkward phrasing, or minor grammatical error that does not change the meaning.
- **NONE:** The translation is completely correct and natural.

---

## Reviewer Checklist

Before marking an item as `VALIDATED`, ensure you have:
- [ ] Confirmed the core scientific/mathematical meaning is 100% accurate.
- [ ] Verified that formulas, equations, and units are perfectly intact.
- [ ] Checked that all required technical identifiers (like `HTML`) are preserved.
- [ ] Read the sentence aloud to verify natural fluency and correct grammar (especially Kannada morphology).
- [ ] Ensured no extra information was added (hallucination) and no source information was lost (omission).
- [ ] Filled out any necessary terminology notes in the JSON template.
