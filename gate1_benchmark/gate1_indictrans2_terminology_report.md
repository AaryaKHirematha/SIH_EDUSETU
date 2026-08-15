# IndicTrans2 200M Terminology & Educational Suitability Report

## 1. Executive Summary
This report evaluates the `ai4bharat/indictrans2-en-indic-dist-200M` model for its suitability in the EduSetu project, specifically focusing on English → Hindi and English → Kannada translations of scientific and mathematical educational content.

While the model handles basic scientific vocabulary in Hindi much better than previously tested models (e.g., NLLB), it exhibits severe, deal-breaking failures in formula preservation, mathematical symbol handling, and Kannada algebraic terminology. Most notably, it suffers from the exact same class of semantic hallucination for "quadratic" in Kannada that NLLB suffered from in Hindi, translating it as "quadrilateral" (a geometry term). Furthermore, it aggressively transliterates English formulas (e.g., `F = ma` becomes `एफ = मा`), rendering physics equations useless.

**Verdict: FAIL**

## 2. Hardware/Performance Results
The model was run under strict memory constraints on a WSL environment with an RTX 3050 GPU (4GB VRAM). By strictly enforcing `inference_mode` and keeping the model directly on CUDA without intermediate CPU caching, OOM errors were successfully avoided.

- **Model:** `ai4bharat/indictrans2-en-indic-dist-200M`
- **Device:** CUDA (dtype: float16)
- **Model Load Time:** ~10.77 s
- **Cold Inference Latency:** ~24.79 s (includes initialization overhead)
- **Warm Inference Latency:** ~0.35 s - 1.47 s per sentence
- **Peak VRAM:** 514.08 MB
- **Peak Process RAM:** 1831.82 MB

## 3. Complete Hindi Results
1. Force is equal to mass times acceleration.
   - **HI:** बल द्रव्यमान गुणा त्वरण के बराबर होता है।
2. The mass of the object is exactly 5 kg.
   - **HI:** वस्तु का द्रव्यमान ठीक 5 किलोग्राम है।
3. The velocity of an object changes when a force is applied.
   - **HI:** जब कोई बल लगाया जाता है तो किसी वस्तु का वेग बदल जाता है।
4. Momentum is equal to mass times velocity.
   - **HI:** गति द्रव्यमान गुणा वेग के बराबर होती है।
5. The quadratic equation can be solved using the quadratic formula.
   - **HI:** द्विघात समीकरण को द्विघात सूत्र का उपयोग करके हल किया जा सकता है।
6. A polynomial is an algebraic expression consisting of variables and coefficients.
   - **HI:** बहुपद एक बीजगणितीय अभिव्यक्ति है जिसमें चर और गुणांक होते हैं।
7. The derivative of a function represents its rate of change.
   - **HI:** किसी फलन का व्युत्पन्न उसके परिवर्तन की दर को दर्शाता है।
8. Integration is used to calculate area under a curve.
   - **HI:** एकीकरण का उपयोग वक्र के नीचे क्षेत्र की गणना करने के लिए किया जाता है।
9. A matrix is a rectangular arrangement of numbers.
   - **HI:** एक मैट्रिक्स संख्याओं की एक आयताकार व्यवस्था है।
10. The coefficient of x in the equation is 5.
    - **HI:** समीकरण में x का गुणांक 5 है।
11. A molecule of water is formed by two hydrogen atoms and one oxygen atom.
    - **HI:** पानी का एक अणु दो हाइड्रोजन परमाणुओं और एक ऑक्सीजन परमाणु से बनता है।
12. The chemical formula for water is H₂O and for carbon dioxide is CO₂.
    - **HI:** पानी का रासायनिक सूत्र H2O है और कार्बन डाइऑक्साइड का रासायनिक सूत्र CO2 है।
13. An atom consists of a nucleus surrounded by electrons.
    - **HI:** परमाणु में एक नाभिक होता है जो इलेक्ट्रॉनों से घिरा होता है।
14. An algorithm is a step-by-step procedure for solving a problem.
    - **HI:** एक एल्गोरिथ्म एक समस्या को हल करने के लिए एक चरण-दर-चरण प्रक्रिया है।
15. Python and NumPy are used for matrix multiplication.
    - **HI:** पायथन और नुमपाई का उपयोग मैट्रिक्स गुणन के लिए किया जाता है।
16. TensorFlow is an open-source machine learning framework.
    - **HI:** टेंसरफ्लो एक ओपन-सोर्स मशीन लर्निंग फ्रेमवर्क है।
17. The web page is styled using HTML and CSS.
    - **HI:** वेब पेज को एच. टी. एम. एल. और सी. एस. एस. का उपयोग करके स्टाइल किया गया है।
18. A database stores and retrieves structured information.
    - **HI:** एक डेटाबेस संरचित जानकारी को संग्रहीत और पुनर्प्राप्त करता है।
19. The famous equation is E = mc².
    - **HI:** प्रसिद्ध समीकरण E = mc2 है।
20. Gravity on Earth is approximately 9.8 m/s².
    - **HI:** पृथ्वी पर गुरुत्वाकर्षण लगभग 9.8 मीटर/सेकंड है।
21. F = ma.
    - **HI:** एफ = मा।
22. Photosynthesis paragraph...
    - **HI:** प्रकाश संश्लेषण एक ऐसी प्रक्रिया है जिसका उपयोग...

## 4. Complete Kannada Results
1. Force is equal to mass times acceleration.
   - **KN:** ಬಲವು ದ್ರವ್ಯರಾಶಿಯ ಬಾರಿ ವೇಗವರ್ಧನೆಗೆ ಸಮಾನವಾಗಿರುತ್ತದೆ.
2. The mass of the object is exactly 5 kg.
   - **KN:** ವಸ್ತುವಿನ ದ್ರವ್ಯರಾಶಿಯು ನಿಖರವಾಗಿ 5 ಕೆ. ಜಿ. ಆಗಿದೆ.
3. The velocity of an object changes when a force is applied.
   - **KN:** ಬಲವನ್ನು ಅನ್ವಯಿಸಿದಾಗ ವಸ್ತುವಿನ ವೇಗವು ಬದಲಾಗುತ್ತದೆ.
4. Momentum is equal to mass times velocity.
   - **KN:** ಆವೇಗವು ದ್ರವ್ಯರಾಶಿಯ ವೇಗಕ್ಕೆ ಸಮನಾಗಿರುತ್ತದೆ.
5. The quadratic equation can be solved using the quadratic formula.
   - **KN:** ಚತುರ್ಭುಜ ಸೂತ್ರವನ್ನು ಬಳಸಿಕೊಂಡು ಚತುರ್ಭುಜ ಸಮೀಕರಣವನ್ನು ಪರಿಹರಿಸಬಹುದು.
6. A polynomial is an algebraic expression consisting of variables and coefficients.
   - **KN:** ಬಹುಪದವು ಅಸ್ಥಿರಗಳು ಮತ್ತು ಗುಣಾಂಕಗಳನ್ನು ಒಳಗೊಂಡಿರುವ ಬೀಜಗಣಿತದ ಅಭಿವ್ಯಕ್ತಿಯಾಗಿದೆ.
7. The derivative of a function represents its rate of change.
   - **KN:** ಒಂದು ಕಾರ್ಯದ ವ್ಯುತ್ಪನ್ನವು ಅದರ ಬದಲಾವಣೆಯ ದರವನ್ನು ಪ್ರತಿನಿಧಿಸುತ್ತದೆ.
8. Integration is used to calculate area under a curve.
   - **KN:** ಒಂದು ವಕ್ರರೇಖೆಯ ಕೆಳಗಿರುವ ಪ್ರದೇಶವನ್ನು ಲೆಕ್ಕ ಹಾಕಲು ಏಕೀಕರಣವನ್ನು ಬಳಸಲಾಗುತ್ತದೆ.
9. A matrix is a rectangular arrangement of numbers.
   - **KN:** ಮ್ಯಾಟ್ರಿಕ್ಸ್ ಎಂಬುದು ಸಂಖ್ಯೆಗಳ ಆಯತಾಕಾರದ ಜೋಡಣೆಯಾಗಿದೆ.
10. The coefficient of x in the equation is 5.
    - **KN:** ಸಮೀಕರಣದಲ್ಲಿ x ನ ಗುಣಾಂಕವು 5 ಆಗಿದೆ.
11. A molecule of water is formed by two hydrogen atoms and one oxygen atom.
    - **KN:** ಎರಡು ಹೈಡ್ರೋಜನ್ ಪರಮಾಣುಗಳು ಮತ್ತು ಒಂದು ಆಮ್ಲಜನಕದ ಪರಮಾಣುಗಳಿಂದ ನೀರಿನ ಅಣುವು ರೂಪುಗೊಳ್ಳುತ್ತದೆ.
12. The chemical formula for water is H₂O and for carbon dioxide is CO₂.
    - **KN:** ನೀರಿನ ರಾಸಾಯನಿಕ ಸೂತ್ರವು H2O ಮತ್ತು ಇಂಗಾಲದ ಡೈಆಕ್ಸೈಡ್ಗೆ CO2 ಆಗಿದೆ.
13. An atom consists of a nucleus surrounded by electrons.
    - **KN:** ಪರಮಾಣು ಎಲೆಕ್ಟ್ರಾನ್ಗಳಿಂದ ಸುತ್ತುವರೆದಿರುವ ನ್ಯೂಕ್ಲಿಯಸ್ ಅನ್ನು ಹೊಂದಿರುತ್ತದೆ.
14. An algorithm is a step-by-step procedure for solving a problem.
    - **KN:** ಅಲ್ಗಾರಿದಮ್ ಎನ್ನುವುದು ಸಮಸ್ಯೆಯನ್ನು ಪರಿಹರಿಸುವ ಹಂತ-ಹಂತದ ಕಾರ್ಯವಿಧಾನವಾಗಿದೆ.
15. Python and NumPy are used for matrix multiplication.
    - **KN:** ಪೈಥಾನ್ ಮತ್ತು ನಮ್ಪೈಗಳನ್ನು ಮ್ಯಾಟ್ರಿಕ್ಸ್ ಗುಣಾಕಾರಕ್ಕಾಗಿ ಬಳಸಲಾಗುತ್ತದೆ.
16. TensorFlow is an open-source machine learning framework.
    - **KN:** ಟೆನ್ಸಾರ್ಫ್ಲೋ ಒಂದು ಮುಕ್ತ-ಮೂಲ ಯಂತ್ರ ಕಲಿಕೆಯ ಚೌಕಟ್ಟಾಗಿದೆ.
17. The web page is styled using HTML and CSS.
    - **KN:** ವೆಬ್ ಪುಟವನ್ನು ಎಚ್. ಟಿ. ಎಂ. ಎಲ್ ಮತ್ತು ಸಿ. ಎಸ್. ಎಸ್ ಬಳಸಿ ವಿನ್ಯಾಸಗೊಳಿಸಲಾಗಿದೆ.
18. A database stores and retrieves structured information.
    - **KN:** ದತ್ತಸಂಚಯವು ರಚನಾತ್ಮಕ ಮಾಹಿತಿಯನ್ನು ಸಂಗ್ರಹಿಸುತ್ತದೆ ಮತ್ತು ಹಿಂಪಡೆಯುತ್ತದೆ.
19. The famous equation is E = mc².
    - **KN:** ಪ್ರಸಿದ್ಧ ಸಮೀಕರಣವೆಂದರೆ E = mc2.
20. Gravity on Earth is approximately 9.8 m/s².
    - **KN:** ಭೂಮಿಯ ಮೇಲಿನ ಗುರುತ್ವಾಕರ್ಷಣೆಯು ಸುಮಾರು 9.8 ಮೀ/ಸೆ2 ಆಗಿದೆ.
21. F = ma.
    - **KN:** ಎಫ್ = ಮಾ.
22. Photosynthesis paragraph...
    - **KN:** ದ್ಯುತಿಸಂಶ್ಲೇಷಣೆಯು ಸಸ್ಯಗಳು ಮತ್ತು ಇತರ ಜೀವಿಗಳು...

## 5. Mathematical Terminology Audit
- **Hindi:**
  - quadratic: द्विघात (dvighat) -> **PASS**. Fixes NLLB's error.
  - polynomial: बहुपद -> **PASS**.
  - derivative: व्युत्पन्न -> **PASS** (Acceptable equivalent).
  - integration: एकीकरण -> **MINOR ISSUE** (General "unification" instead of calculus "समाकलन", but acceptable in some contexts).
  - matrix: मैट्रिक्स -> **PASS** (Transliteration, acceptable).
  - coefficient: गुणांक -> **PASS**.
- **Kannada:**
  - quadratic equation: ಚತುರ್ಭುಜ ಸಮೀಕರಣ (Chaturbhuja) -> **CRITICAL FAIL**. "ಚತುರ್ಭುಜ" means "quadrilateral" (geometry). The model made the exact same error in Kannada that NLLB made in Hindi.
  - polynomial: ಬಹುಪದ -> **PASS**.
  - derivative: ವ್ಯುತ್ಪನ್ನ -> **PASS**.
  - integration: ಏಕೀಕರಣ -> **MINOR ISSUE** (General unification instead of calculus).
  - matrix: ಮ್ಯಾಟ್ರಿಕ್ಸ್ -> **PASS** (Transliteration).
  - coefficient: ಗುಣಾಂಕ -> **PASS**.

## 6. Physics Terminology Audit
- **Hindi:**
  - mass: द्रव्यमान -> **PASS**.
  - force: बल -> **PASS**.
  - acceleration: त्वरण -> **PASS**.
- **Kannada:**
  - mass: ದ್ರವ್ಯರಾಶಿ -> **PASS**. (Fixes NLLB's error).
  - force: ಬಲ -> **PASS**.
  - acceleration: ವೇಗವರ್ಧನೆ -> **PASS**.

## 7. Chemistry Terminology Audit
Both languages successfully used correct terms for atom, molecule, nucleus, and electrons.
- **PASS** for pure text terminology.

## 8. Computer Science Terminology Audit
Both languages successfully handled computer science terms (algorithm, database, framework).
- **PASS**.

## 9. Formula Preservation Audit
- **H₂O and CO₂:** Subscripts are flattened to H2O and CO2 in both languages. -> **MINOR FORMAT LOSS**.
- **E = mc²:** Superscript is flattened to E = mc2 in both languages. -> **MINOR FORMAT LOSS**.
- **9.8 m/s²:**
  - **Hindi:** "9.8 मीटर/सेकंड" (Lost the squared completely, changing acceleration to velocity). -> **SEMANTICALLY CHANGED**.
  - **Kannada:** "9.8 ಮೀ/ಸೆ2" -> **MINOR FORMAT LOSS**.
- **F = ma:**
  - **Hindi:** "एफ = मा" (Transliterated variables into Hindi script). -> **CORRUPTED**.
  - **Kannada:** "ಎಫ್ = ಮಾ" (Transliterated variables into Kannada script). -> **CORRUPTED**.

## 10. Medium-Text Evaluation
The paragraph about photosynthesis was translated faithfully in both languages. No obvious hallucinations were present, and technical concepts (cellular respiration, carbohydrate molecules) were translated understandably. -> **PASS**.

## 11. Hallucination Analysis
While the model did not introduce random external concepts into the medium text, its handling of formulas and specific mathematical terms acts as a semantic hallucination. "ಚತುರ್ಭುಜ" (quadrilateral) for quadratic is a direct conceptual hallucination caused by token/embedding misalignment in Kannada mathematics. Translating `F = ma` to `एफ = मा` is a hallucination of script application where verbatim ASCII retention is required.

## 12. Comparison with NLLB 600M and NLLB 1.3B
- **Did IndicTrans2 avoid NLLB failures?**
  - **NLLB Hindi quadratic (चतुर्भुज):** Yes, IndicTrans2 correctly outputs द्विघात.
  - **NLLB Kannada mass:** Yes, IndicTrans2 correctly outputs ದ್ರವ್ಯರಾಶಿ.
  - **NLLB Unicode flattening:** No. IndicTrans2 flattens superscripts/subscripts just like NLLB.
- **New Issues Introduced:**
  - It shifted the "quadratic = quadrilateral" hallucination from Hindi to Kannada.
  - It aggressively transliterates Latin mathematical variables (F = ma -> एफ = मा), which completely breaks physics equations.

## 13. Critical Educational Risk Assessment
Using this model for an educational application without a robust pre/post-processing pipeline (e.g., regex protection for equations) is highly dangerous.
1. Equations will be destroyed by transliteration (F=ma becoming एफ=मा).
2. Units will be semantically corrupted (m/s² becoming m/s).
3. Algebra students in Kannada will be taught that quadratic equations are "quadrilateral equations".

## 14. Final Verdict
**FAIL**

While the core scientific terminology in Hindi shows promise, the catastrophic failure in Kannada algebraic terminology, combined with the aggressive transliteration of formulas and equations, makes it unsuitable as an out-of-the-box educational translation model.
