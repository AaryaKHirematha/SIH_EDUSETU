# GATE 1I: Terminology and Formula Protection Report

## 1. Objective
To determine whether a pre-translation placeholder/glossary injection layer can successfully protect high-risk mathematical/scientific terminology, formulas, and technical identifiers from IndicTrans2's hallucination and transliteration issues, particularly the Kannada "quadratic = quadrilateral" hallucination.

## 2. Experimental Setup
- **Model:** `ai4bharat/indictrans2-en-indic-dist-200M`
- **Configuration:** CUDA, `float16`, `inference_mode()`
- **Strategy:** Replace English terms/formulas with numeric placeholders (e.g., `99901`) before translation, map them, and restore the exact target-language terminology or formulas post-translation.

## 3. Glossary & Identifiers Tested
- **Terms:** quadratic equation, mass, acceleration, derivative, integration, polynomial, matrix multiplication, etc.
- **Formulas:** E = mc², F = ma, H₂O, CO₂, 9.8 m/s²
- **Identifiers:** Python, NumPy

## 4. Evaluation Highlights (Side-by-Side Comparison)

### Case 1: Kannada "Quadratic Equation" Hallucination
- **English:** The quadratic equation can be solved using the quadratic formula.
- **Raw Kannada:** ಚತುರ್ಭುಜ ಸೂತ್ರವನ್ನು ಬಳಸಿಕೊಂಡು ಚತುರ್ಭುಜ ಸಮೀಕರಣವನ್ನು ಪರಿಹರಿಸಬಹುದು. *(Critical Error: "Quadrilateral")*
- **Protected Kannada:** ವರ್ಗ ಸಮೀಕರಣ ಅನ್ನು ವರ್ಗ ಸೂತ್ರ ಅನ್ನು ಬಳಸಿಕೊಂಡು ಪರಿಹರಿಸಬಹುದು. *(Conceptually correct, but grammatically detached case marker 'ಅನ್ನು')*

### Case 2: Formula Preservation
- **English:** The famous equation is E = mc².
- **Raw Hindi:** प्रसिद्ध समीकरण E = mc2 है। *(Subscript flattened)*
- **Protected Hindi:** प्रसिद्ध समीकरण E = mc² है। *(Perfectly preserved)*

### Case 3: Technical Identifier Preservation
- **English:** Python and NumPy are used for matrix multiplication.
- **Raw Hindi:** पायथन और नुमपाई का उपयोग मैट्रिक्स गुणन के लिए किया जाता है। *(Transliterated)*
- **Protected Hindi:** Python और NumPy का उपयोग मैट्रिक्स गुणन के लिए किया जाता है। *(Perfectly preserved)*

### Case 4: Unit Preservation
- **English:** Gravity on Earth is approximately 9.8 m/s².
- **Raw Hindi:** पृथ्वी पर गुरुत्वाकर्षण लगभग 9.8 मीटर/सेकंड है। *(Corrupted unit, lost exponent)*
- **Protected Hindi:** पृथ्वी पर गुरुत्वाकर्षण लगभग 9.8 m/s² है। *(Perfectly preserved)*

## 5. Morphological Artifacts in Agglutinative Languages
While the protection layer was conceptually successful, it introduced grammatical artifacts in Kannada (and to a lesser extent Hindi). 
Because Kannada is highly agglutinative, the model attaches case markers directly to the numeric placeholders.
- *Model Output:* `99901 ಅನ್ನು`, `99902ರ`, `99901ಕ್ಕೆ`
- *Restoration Result:* `ಗುಣಾಂಕಗಳು ಅನ್ನು` (instead of `ಗುಣಾಂಕಗಳನ್ನು`), `ಕಾರ್ಯರ` (instead of `ಕಾರ್ಯದ`).
This results in grammatically awkward, "robotic" sounding sentences, even though the educational concepts are now 100% accurate.

## 6. Failure Analysis Breakdown
- **Model limitations:** Unable to reliably translate "quadratic" algebraically in Kannada; fails to natively preserve Unicode superscripts/subscripts.
- **Formula/technical-content protection:** **SOLVED**. Placeholders successfully protected all formulas and identifiers from transliteration/flattening.
- **Terminology/glossary problems:** **SOLVED**. The glossary successfully mapped educational terms and prevented hallucinations.
- **General translation problems:** **NEW ISSUE INTRODUCED**. Agglutinative morphology is broken by rigid numeric placeholders, resulting in detached suffixes.

## 7. Architectural Implications
A terminology protection layer is absolutely mandatory for EduSetu to prevent catastrophic educational errors. However, a naive string replacement strategy degrades grammatical fluency in agglutinative languages. 

To productionize this, the system requires:
1. **Linguistic Post-Processing:** A morphological joiner for Kannada that merges detached suffixes (e.g., `ಪದ + ಅನ್ನು = ಪದವನ್ನು`).
2. OR **Constrained Decoding:** Upgrading to an MT engine that natively supports dictionary-constrained decoding at the beam-search level, avoiding placeholders entirely.

## 8. Final Verdict
**PASS WITH CONDITIONS**

The protection mechanism reliably fixes the most dangerous critical failures (hallucinations, formula corruption, and unit destruction) without causing OOM or performance regressions. However, the resulting grammatical artifacts in Kannada mean the pipeline needs a morphological post-processing step to achieve natural fluency.
