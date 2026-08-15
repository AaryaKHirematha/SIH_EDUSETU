# GATE 3A: Critical Review Subset Audit

## Selection Statistics
- **original cases:** 114
- **selected cases:** 48
- **Hindi cases:** 48
- **Kannada cases:** 48

## Priority Breakdown
- **CRITICAL:** 48
- **HIGH:** 0
- **CONTROL:** 0

## Domains Represented
- **Physics**: 10 cases
- **Mathematics**: 10 cases
- **Chemistry**: 10 cases
- **Biology**: 9 cases
- **Computer Science**: 9 cases

## Selection Rationale
Cases were selected based strictly on the priority order, distributing across all 5 domains round-robin within each priority tier up to ~48 cases.
The priorities evaluated were:
1. Human-critical terminology failures detected by Gate 2.
2. Formula preservation failures.
3. Technical identifier failures.
4. Kannada quadratic-equation terminology failures.
5. Kannada morphology failures remaining after Config C.
6. Hallucination indicators.
7. Omission/addition failures.
8. Cases containing high-risk STEM terminology.
9. Representative successful cases as controls.

## Validation Confirmations
- every selected ID exists in Gate 2
- no source text changed
- no translation output changed
- no human judgments were generated
- all judgment fields are empty
- all cases are marked PENDING_HUMAN_REVIEW