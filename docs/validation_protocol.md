# Validation Protocol

CDSA-ATM employs a triple cross-validation framework:

1. **ESARR 2 cross-alignment** — typology mapped to EUROCONTROL
   severity classification.
2. **Statistical distribution testing** — synthetic occurrence
   distributions validated via Chi-square goodness-of-fit and
   Kolmogorov-Smirnov tests against ESARR 2 statistical averages.
3. **Peer review** — submission to CEAS Aeronautical Journal
   (Springer, Q2) and arXiv preprint.

## 1. ESARR 2 Alignment

Each of the 15 occurrence classes is mapped to ESARR 2 severity
(A/B/C) as detailed in `ats_occurrence_taxonomy.md`. The proportion
of high-severity (A) occurrences in the synthetic dataset is
constrained to align with ESARR 2 aggregate statistics across
European ANSPs.

## 2. Statistical Distribution Testing

The synthetic occurrence engine produces distributions across:
- Class frequency (multinomial)
- Severity proportion (ordinal)
- Inter-arrival time (exponential, λ derived from ESARR 2)
- Sector geographic distribution (mixture of Gaussians per ANSP)

Validation tests:
- **Chi-square goodness-of-fit**: synthetic class frequency vs ESARR
  2 distribution.
- **Kolmogorov-Smirnov**: inter-arrival time distribution against
  expected exponential.

Results are reported in `data/validation_report.md` (added in v1.1
after Phase 3 platform deployment).

## 3. Peer Review

Two peer review channels:
- **CEAS Aeronautical Journal** (Springer, Q2, IF 1.6) — target
  submission 30 June 2026.
- **arXiv preprint** (cs.LG primary, cs.CR secondary, cs.SY
  cross-list) — open-access companion.

A third Q1 peer review channel is planned via Safety Science
(Elsevier, IF 6.1) for the cross-pillar paradigm-defining paper
combining CDSA-MRO and CDSA-ATM results.
