# GATE 2: Educational Translation Benchmark Specification (EduSetu)

## 1. OBJECTIVE
Measure whether the proposed EduSetu translation architecture (ai4bharat/indictrans2-en-indic-dist-200M + Protected-content extraction/restoration + Educational terminology glossary + Kannada morphological post-processing) is reliable, safe, and accurate enough for real-world educational content deployment.

## 2. LANGUAGES
- **Source:** English
- **Target:** Hindi
- **Target:** Kannada

## 3. DOMAINS
The benchmark evaluates content across the following core STEM domains:
- Physics
- Mathematics
- Chemistry
- Biology
- Computer Science
- General STEM education

## 4. DATASET DESIGN
The evaluation dataset must be representative of real educational material. It will consist of:
- Short sentences (e.g., direct facts, axioms)
- Medium sentences (e.g., multi-clause explanations)
- Long paragraphs (e.g., conceptual introductions, textbook excerpts)
- Definitions (e.g., glossary terms)
- Explanations (e.g., step-by-step logic)
- Formulas (inline and standalone)
- Units of measurement
- Tables or structured text (where applicable)
- Technical terminology heavily embedded in natural language

*Note:* Automated metrics will rely on curated reference translations, but no fake, machine-generated "ground truth" translations will be used or presented as human ground truth. 
Clear distinctions will be maintained between:
- **Reference translations:** Curated target-language text.
- **Model outputs:** Raw and protected outputs from the pipeline.
- **Automated metrics:** Algorithmic scores (e.g., BLEU, term matching).
- **Human evaluation:** Native-speaker assessment of semantic fidelity and grammar.

## 5. TERMINOLOGY TEST SET
A curated list of high-risk educational terms that must be explicitly evaluated.
*Validation Status: Pending Native Speaker Review*

| Domain | English Term | Expected Hindi | Expected Kannada |
|---|---|---|---|
| Physics | mass | द्रव्यमान | ದ್ರವ್ಯರಾಶಿ |
| Physics | force | बल | ಬಲ |
| Physics | acceleration | त्वरण | ವೇಗವರ್ಧನೆ |
| Physics | velocity | वेग | ವೇಗ |
| Physics | momentum | संवेग / गति | ಆವೇಗ |
| Physics | gravity | गुरुत्वाकर्षण | ಗುರುತ್ವಾಕರ್ಷಣೆ |
| Mathematics | quadratic equation | द्विघात समीकरण | ವರ್ಗ ಸಮೀಕರಣ |
| Mathematics | polynomial | बहुपद | ಬಹುಪದ |
| Mathematics | derivative | अवकलज / व्युत्पन्न | ವ್ಯುತ್ಪನ್ನ |
| Mathematics | integration | समाकलन | ಅನುಕಲನ |
| Mathematics | coefficient | गुणांक | ಗುಣಾಂಕ |
| Mathematics | matrix | आव्यूह / मैट्रिक्स | ಮಾತೃಕೆ / ಮ್ಯಾಟ್ರಿಕ್ಸ್ |
| Chemistry | molecule | अणु | ಅಣು |
| Chemistry | atom | परमाणु | ಪರಮಾಣು |
| Chemistry | chemical formula | रासायनिक सूत्र | ರಾಸಾಯನಿಕ ಸೂತ್ರ |
| Biology | photosynthesis | प्रकाश संश्लेषण | ದ್ಯುತಿಸಂಶ್ಲೇಷಣೆ |
| CompSci | algorithm | एल्गोरिदम | ಅಲ್ಗಾರಿದಮ್ |
| CompSci | database | डेटाबेस | ದತ್ತಸಂಚಯ |

## 6. FORMULA TEST SET
Explicit testing of mathematical and scientific notation preservation, specifically focusing on superscripts, subscripts, and symbols:
- `F = ma`
- `E = mc²`
- `H₂O`
- `CO₂`
- `9.8 m/s²`
- `x²`
- `a₁`
- Standard algebraic and trigonometric notation (e.g., `sin(θ)`)

## 7. TECHNICAL CONTENT
Testing the preservation of technical identifiers, software names, and web standards. These must remain intact (untranslated and optionally untransliterated depending on context):
- `Python`
- `NumPy`
- `HTML`
- `CSS`
- `TensorFlow`
- `API`
- `database`
- `algorithm`
- `variable`
- `function`

## 8. KANNADA MORPHOLOGY
Specialized test cases to evaluate the morphological safety of the placeholder-restoration pipeline in Kannada. Cases include terminology followed by grammatical suffixes:
- Case markers (accusative, dative, genitive, instrumental, locative)
- Postpositions
- Common noun endings (e.g., ending in 'i', 'a', 'u')

*Measurement Focus:*
- Detached suffixes (e.g., `ಪದ ಅನ್ನು`)
- Incorrect suffixes (e.g., applying `ರ` when `ದ` is required)
- Incorrect joining (e.g., `xದ` instead of `xನ`)
- Meaning changes resulting from morphological errors

## 9. EVALUATION CATEGORIES
Every translation output will be evaluated across the following dimensions:
1. **Semantic fidelity:** Does the translation mean exactly the same thing as the source?
2. **Terminology correctness:** Are the specific educational terms mapped correctly?
3. **Mathematical correctness:** Is the math logically sound in the target language?
4. **Scientific correctness:** Are scientific facts preserved?
5. **Formula preservation:** Are equations exactly preserved without Unicode flattening?
6. **Technical identifier preservation:** Are code/software terms preserved?
7. **Kannada grammatical correctness:** Morphological fluency and syntax.
8. **Hindi grammatical correctness:** Gender, case, and syntax.
9. **Hallucination:** Was any unprompted information added?
10. **Omission:** Was any critical information dropped?
11. **Addition:** Were unnecessary clarifying words added (if not hallucinated)?
12. **Fluency:** Does the sentence read naturally to a native student?

## 10. SAFETY CRITERIA
A **CRITICAL FAILURE** occurs when a translation compromises the educational integrity of the text. A single catastrophic educational error will be flagged separately and can fail the entire pipeline, regardless of high BLEU/chrF scores.

*Examples of Critical Failures:*
- Incorrect scientific concept (e.g., confusing velocity with acceleration).
- Incorrect mathematical concept (e.g., translating "quadratic" to "quadrilateral").
- Changed equation (e.g., flattening `mc²` to `mc2`).
- Changed unit (e.g., `m/s²` becoming `m/s`).
- Hallucinated information.
- Omitted critical fact.
- Translation of a protected technical identifier resulting in a changed meaning.

## 11. METRICS
Reliance on BLEU/chrF is insufficient for educational text. The benchmark will utilize:
- **Terminology Accuracy:** % of protected terms correctly restored.
- **Formula Preservation Rate:** % of formulas perfectly matching the source string.
- **Technical Identifier Preservation Rate:** % of technical terms preserved.
- **Semantic Accuracy:** Human-graded (or LLM-assisted) binary score of meaning preservation.
- **Hallucination Rate:** Frequency of hallucinated outputs.
- **Omission Rate:** Frequency of dropped facts.
- **Hindi Grammatical Score:** Qualitative fluency score (1-5).
- **Kannada Grammatical Score:** Qualitative fluency score (1-5), emphasizing morphology.
- **Overall Educational Safety Score:** Aggregate pass/fail rate based on the absence of CRITICAL FAILURES.

## 12. PERFORMANCE
The benchmark will log hardware and system performance:
- Model load time (seconds)
- Cold latency (seconds for the first inference)
- Warm latency (seconds per inference after initialization)
- Peak VRAM (MB)
- Peak RAM (MB)
- Throughput (tokens/second or sentences/second)
- Failure/OOM rate

## 13. BASELINES
To contextualize the performance, the benchmark will reference the existing Gate 1 evidence (no reruns required):
- **NLLB 600M** (Known issues: severe Hindi geometric hallucination, Unicode flattening)
- **NLLB 1.3B** (Known issues: hallucination, instability)
- **M2M100 418M** (Known issues: terminology instability)
- **Raw IndicTrans2 200M** (Known issues: Kannada geometric hallucination, equation transliteration)
- **Protected IndicTrans2 200M** (Proposed architecture)

## 14. HUMAN VALIDATION
Automated metrics cannot cover all nuances. Native Hindi and Kannada reviewers are explicitly required to validate:
- **Kannada morphology:** Ensuring Sandhi rules in the post-processor yield natural text.
- **Mathematical terminology:** Confirming the target terms are actually used in standard regional curriculums.
- **Scientific terminology:** Validating the contextual appropriateness of biology/chemistry terms.
- **Fluency:** Ensuring the text sounds like a textbook, not a robot.

## 15. PASS/FAIL THRESHOLDS
*(Proposed Engineering Thresholds - Subject to adjustment based on human feedback)*
- **Formula Preservation Rate:** 100%
- **Terminology Accuracy:** >98%
- **Critical Failure Rate:** 0% on benchmark set
- **Hallucination Rate:** 0% on benchmark set
- **OOM Rate:** 0% on target hardware (4GB VRAM)
- **Grammar/Fluency Score:** >4.0/5.0 average (Human validated)

## 16. REPRODUCIBILITY
- **Model Revision:** `ai4bharat/indictrans2-en-indic-dist-200M`
- **Python Version:** 3.x
- **PyTorch Version:** (To be logged during run)
- **Transformers Version:** (To be logged during run)
- **CUDA Version:** (To be logged during run)
- **GPU:** NVIDIA RTX 3050 Laptop GPU (4GB VRAM) / Target Hardware
- **Random Seeds:** Fixed (e.g., 42) for deterministic generation if applicable.
- **Preprocessing Version:** `IndicTransToolkit`
- **Terminology Glossary Version:** v1.0 (Gate 1 Output)
- **Morphology-Rule Version:** v1.0 (Gate 1J Output)

## 17. DATA LEAKAGE / BIAS
Risk documentation to be monitored during the benchmark:
- **Training-data overlap:** AI4Bharat models are trained on standard datasets (Samanantar, BPCC); we must ensure our evaluation sentences are sufficiently distinct to test generalization.
- **Machine-generated references:** We must strictly avoid evaluating the model against references generated by another MT system (e.g., Google Translate), as this introduces translationese bias.
- **Domain imbalance:** The dataset must be balanced across Physics, Math, Chemistry, Biology, and CS.
- **Hindi/Kannada imbalance:** Ensure both languages receive equal stress testing, particularly regarding morphological complexity in Kannada.
- **Terminology coverage bias:** The glossary must cover edge cases, not just common terms.

## 18. GATE 2 DECISION
Based on the benchmark results, the final decision will be:
- **PASS:** The architecture meets all proposed thresholds and is ready for production integration.
- **PASS WITH CONDITIONS:** The architecture is fundamentally sound but requires specific tweaks (e.g., expanding the morphology dictionary, tweaking prompt/padding settings) before deployment.
- **FAIL:** The architecture fails critical safety thresholds (e.g., persistent hallucinations, unsolvable morphology, or OOM errors) and requires a fundamentally different approach.
