# Contributing to CDSA-ATM

Thank you for your interest in contributing to CDSA-ATM. This document
provides guidelines for contributing to the project.

## Project Maintainer

**Mete Cantekin** (metecantekin@gmail.com)
PhD Candidate, Istanbul Beykent University

## Scope of Contributions

CDSA-ATM is currently maintained as a single-author academic research
project. The repository accompanies a doctoral dissertation, a CEAS
Aeronautical Journal submission, an arXiv preprint, and a planned
TÜBİTAK 1001 research project.

Contributions that align with the academic scope of the project are
welcome, particularly:

- Bug reports and reproducibility issues
- Documentation improvements
- Extensions of the 15-class ATS occurrence typology with additional
  ESARR 2 or MITRE ATT&CK cross-mappings
- Federated learning algorithm variants (e.g., FedNova, SCAFFOLD)
- Additional ANSP simulation configurations
- OpenSky Network data ingestion improvements

## How to Contribute

1. **Open an issue first.** Discuss the proposed change before
   submitting a pull request. This helps avoid duplicated work and
   ensures alignment with the academic scope.
2. **Fork the repository** and create a feature branch:
   `git checkout -b feature/your-feature-name`
3. **Write clear commit messages** describing the academic or
   technical motivation.
4. **Update the documentation** in `docs/` for any new functionality.
5. **Add or update tests** in `tests/`.
6. **Submit a pull request** with a clear description and references
   to the relevant issue.

## Code Style

- Python 3.10+
- PEP 8 compliant
- Type hints encouraged
- Docstrings in English (Google or NumPy style)

## Academic Citation

If your contribution leads to a publication, please cite CDSA-ATM
using the metadata in `CITATION.cff`. If your work substantially
extends CDSA-ATM, we encourage you to publish your extension as a
separate academic work.

## Licence

By contributing, you agree that your contributions will be licensed
under the MIT Licence (code) and CC-BY 4.0 (data/documentation).

## Code of Conduct

This project follows the principles of respectful, evidence-based
academic discourse. Personal attacks, harassment, or unprofessional
conduct will not be tolerated.
