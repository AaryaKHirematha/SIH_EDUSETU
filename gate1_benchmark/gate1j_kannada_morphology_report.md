# GATE 1J: Kannada Morphological Safety Report

## 1. Objective
To determine whether the grammatical artifacts (detached suffixes) introduced by terminology placeholders in Kannada can be reliably and deterministically corrected using post-translation morphological rules, without damaging educational correctness or altering meaning.

## 2. Gate 1I Failure Analysis
In Gate 1I, using numeric placeholders successfully preserved terminology and formulas (e.g., fixing the "quadrilateral" hallucination). However, because Kannada is agglutinative, the translation model attached case suffixes directly to the numeric placeholders (e.g., `99901ರ`, `99901 ಅನ್ನು`). When restored naively, this created grammatically detached or morphologically incorrect suffixes (e.g., `ಕಾರ್ಯ ರ` instead of `ಕಾರ್ಯದ`), severely degrading sentence fluency.

## 3. Tested Morphology Strategies
Three strategies were tested for the placeholder restoration:
- **Strategy A (Raw Placeholder):** Naive string replacement.
- **Strategy B (Quoted Placeholder):** Wrapping the placeholder in quotes (`"99901"`) to prevent the model from attaching suffixes.
- **Strategy C (Morphological Restoration):** Detecting attached/detached suffixes using Regex, mapping them through a basic Kannada morph-joiner (Sandhi rules), and dynamically attaching them to the restored target word.

## 4. Before/After Examples & Assessment

### Case 1: Accusative Suffix Join
- **English:** Solve the quadratic equation using the quadratic formula.
- **Strategy A (Raw):** ವರ್ಗ ಸೂತ್ರ ಅನ್ನು ಬಳಸಿಕೊಂಡು ವರ್ಗ ಸಮೀಕರಣ ಅನ್ನು ಪರಿಹರಿಸಿ. *(Detached)*
- **Strategy C (Morph):** ವರ್ಗ ಸೂತ್ರವನ್ನು ಬಳಸಿಕೊಂಡು ವರ್ಗ ಸಮೀಕರಣವನ್ನು ಪರಿಹರಿಸಿ.
- **Grammar Assessment:** **Perfect.** The script successfully identified the detached `ಅನ್ನು` markers and correctly applied Kannada Sandhi rules to produce `ಸೂತ್ರವನ್ನು` and `ಸಮೀಕರಣವನ್ನು`.

### Case 2: Genitive Suffix Join
- **English:** The equation E = mc² describes the relationship between energy and mass.
- **Strategy A (Raw):** ಸಮೀಕರಣ E = mc² ಶಕ್ತಿ ಮತ್ತು ದ್ರವ್ಯರಾಶಿ ರ ನಡುವಿನ ಸಂಬಂಧ ಅನ್ನು ವಿವರಿಸುತ್ತದೆ.
- **Strategy C (Morph):** ಸಮೀಕರಣ E = mc² ಶಕ್ತಿ ಮತ್ತು ದ್ರವ್ಯರಾಶಿಯ ನಡುವಿನ ಸಂಬಂಧವನ್ನು ವಿವರಿಸುತ್ತದೆ.
- **Grammar Assessment:** **Perfect.** The script converted the raw model's attached `ರ` (`99905ರ`) into the correct Kannada genitive `ಯ` for words ending in 'i' (`ದ್ರವ್ಯರಾಶಿಯ`).

### Case 3: The Failure of Strategy B (Quotes)
- **English:** The equation E = mc² describes the relationship between energy and mass.
- **Strategy B (Quotes):** ಸಮೀಕರಣ E = mc² "" ಶಕ್ತಿ "ಮತ್ತು" ದ್ರವ್ಯರಾಶಿ "ನಡುವಿನ" ಸಂಬಂಧ "ಅನ್ನು ವಿವರಿಸುತ್ತದೆ".
- **Grammar Assessment:** **Catastrophic Failure.** The quotes severely confused the MT model, causing it to inject random quote marks around native Kannada conjunctions and postpositions.

## 5. Terminology and Formula Preservation
- **Preserved:** All terminology (ವರ್ಗ ಸಮೀಕರಣ, ದ್ರವ್ಯರಾಶಿ), formulas (E = mc², H₂O), and identifiers (x) were perfectly preserved across Strategy C without any corruption or hallucination.

## 6. Failure Cases in Strategy C
While Strategy C was overwhelmingly successful, its naive rule-set missed some edge cases:
- **Case:** "The coefficient of x in the equation is 5."
- **Output:** ಸಮೀಕರಣ ರಲ್ಲಿ xದ ಗುಣಾಂಕ 5 ಆಗಿದೆ.
- **Issue:** It failed to properly join `ಸಮೀಕರಣ` + `ರಲ್ಲಿ`, leaving it detached. It also joined `x` + `ರ` into `xದ` instead of the more natural `xನ`. This does not alter the mathematical meaning, but it indicates that a more comprehensive rule set is required.

## 7. Complexity Assessment & Production Risk
- **Complexity:** Moderate. The required regex detection is simple and deterministic. The complexity lies solely in defining a complete matrix of Kannada vowel/consonant ending rules (Sandhi) for the ~10 common case markers.
- **Risk:** Low. Because the restoration is deterministic and rule-based, it poses **zero risk of hallucinating educational content**, unlike the raw MT model. If a rule fails, the fallback is a detached suffix, which is cosmetically awkward but factually safe.

## 8. Recommendation & Verdict
**Verdict: PASS WITH CONDITIONS**

Morphological correction using controlled placeholder parsing and Sandhi-rule application is highly effective and solves the primary obstacle from Gate 1I. It perfectly restores natural Kannada grammar for standard cases without damaging formulas or terminology.

**Recommendation:** Proceed with Strategy C (Numeric Placeholders + Morphological Post-Processor). To move to production, the basic rule set must be expanded into a robust Kannada Sandhi dictionary, or validated by a native speaker to ensure all noun endings are handled smoothly.
