# Final Failure & Resolution History

This document traces the significant pipeline failures encountered during validation and the isolated experiments used to resolve them.

## 1. Hardware Resource Exhaustion (OOM)
- **Gate Discovered:** Gate 2 / Gate 4A
- **Symptoms:** The pipeline crashed when processing multiple translations sequentially on the 4 GB VRAM limit.
- **Root Cause:** Pytorch CUDA cache and Python garbage collection were holding onto stale tensors between sequential inference calls.
- **Resolution:** Implementation of a strict sequential loop utilizing `torch.inference_mode()`, explicit `gc.collect()`, and `torch.cuda.empty_cache()` between iterations.
- **Result:** Peak VRAM stabilized at exactly 475.4 MB across all subsequent Gate 4 evaluations.

## 2. Kannada Morphology Detached Suffixes
- **Gate Discovered:** Gate 1
- **Symptoms:** Hard string replacement caused Kannada case markers (e.g., `ಅನ್ನು`, `ಗೆ`) to detach grammatically from protected English words.
- **Resolution:** Gate 1J introduced Kannada Sandhi heuristics (`kannada_morph_join`) to dynamically reattach suffixes based on the phonetic ending of the protected term.

## 3. The 33% "False Positive" Morphology Failure
- **Gate Discovered:** Gate 3A
- **Symptoms:** An automated AI-review script flagged a 33.33% failure rate for detached Kannada suffixes under Config C.
- **Root Cause:** Deep analysis in Gate 3B revealed that standard Python regular expressions (`\b`) treat Kannada virama characters (halant) as word boundaries. The heuristic was falsely classifying securely attached suffixes as "detached."
- **Resolution:** The heuristic was corrected to use physical whitespace/punctuation bounding rather than `\b`.
- **Result:** The failure rate dropped to 0%, proving the Sandhi logic was actually functioning perfectly.

## 4. The MAT_028 Source Corruption Bug
- **Gate Discovered:** Gate 4B
- **Symptoms:** Terminology protection failed completely for the phrase "limits of integration" in item `MAT_028` ("The limits of integration are from a to b.").
- **Root Cause:** Single-character technical identifiers ("a" and "b") were blindly replaced using `.replace()`. The letter "a" inside the word "integration" was corrupted into a placeholder (`integr[99901]tion`). The terminology regex subsequently failed to match the corrupted source.
- **Resolution:** Gate 4C introduced a dynamic `safe_replace` boundary check utilizing negative lookbehinds/lookaheads (`(?<![a-zA-Z0-9_])`) to prevent alphanumeric identifiers from overwriting letters inside existing words, while safely handling formulas with non-word symbols like `(x+y)`.
- **Result:** The fix was proven in Gate 4C (245/245 cases passed) and safely migrated into production during Gate 4D. No regressions were introduced in Gate 4E.
