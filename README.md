# Antibiotic-aware Adaptive Feature Fusion for *Salmonella* Antimicrobial Resistance Prediction

Genome-based prediction of antimicrobial resistance (AMR) in *Salmonella*, built around an
**antibiotic-aware adaptive feature-fusion** model and a **reliability-checking protocol** that
audits every prediction for the three failure modes most machine-learning AMR papers ignore:
class imbalance, test-set configuration selection, and leakage from population structure.

> Undergraduate thesis project. Baseline reference: You et al., *Engineering* **48**(5):174–184, 2025
> (DOI [10.1016/j.eng.2025.01.013](https://doi.org/10.1016/j.eng.2025.01.013)).

---

## Overview

Existing AMR studies typically train on genomic features with random splits and report high
accuracy, but rarely control for the risks above. This project keeps predictive performance
competitive while putting **reliability at the centre**:

- **Data.** 1,167 *Salmonella* genomes with five original antibiotics, extended by external
  validation on [BV-BRC](https://www.bv-brc.org/) for five further drugs.
- **Signal.** The **accessory genome** (18,125 genes) is the dominant predictive signal and
  clearly outperforms core SNPs.
- **Adaptive fusion.** Each antibiotic selects its own best feature module × model, reaching
  **F1 0.886–0.971**. Raw F1 improves on 4/5 drugs over the strong expert-marker baseline, but the
  gain is **not statistically significant after Holm correction (0/5 drugs)** — the honest reading
  is *parity with, and competitive against,* the expert-marker baseline, with the value coming from
  antibiotic-specific representation, not a blanket accuracy win.
- **Reliability.** Repeated-CV paired t-tests, lineage-aware splits (core-SNP internally, MLST
  externally), probability calibration + decision-curve analysis, and real QRDR mutation calling.

### Key findings

| Question | Result |
|---|---|
| Which signal dominates? | Accessory genome ≫ core SNPs |
| Does adaptive fusion beat the expert-marker baseline? | Competitive / at parity — 0/5 drugs significant after Holm |
| Which drugs are mechanism-driven & lineage-robust? | **AXO, FOX, TET** (small drop under blocked CV) |
| Which drugs are lineage-confounded? | **AMP, AUG, CHL** and **CIP, NAL, GEN** (collapse toward ~0.5 under lineage/MLST split) |
| Are models deployable for screening? | Yes — isotonic calibration ECE ≈ 0.005–0.01; NPV 0.98–0.998; positive net benefit |
| Quinolone mechanism features? | QRDR mutations (gyrA, parC) strongly associate with resistance and stay robust across lineages |

> ⚠️ The dataset is ~97–99% one clonal lineage (by core SNP), so lineage-aware evaluation is
> essential — several drugs that look strong under random CV are largely explained by population
> structure. See `results/LINEAGE_AWARE_SUMMARY.md`.

---

## Architecture

The pipeline has two cooperating layers. Editable diagram source:
[`report/architecture.drawio`](report/architecture.drawio) (three pages — Pipeline, Feature Modules,
Reliability Layer; exported to `report/figures/arch_*.png`).

**Prediction layer** — turns genomic matrices into a per-antibiotic resistance decision:

- Feature construction on the accessory genome (18,125 genes) via several modules:
  - Paper-ready expert markers (50D)
  - Accessory chi² selection (top-200)
  - Ensemble selector (chi² + L1-logistic + random-forest importances, top-200)
  - Sample-similarity graph (Jaccard kNN → 7 statistics)
  - Gene-graph embedding (correlation adjacency → truncated SVD, 17D)
- Adaptive selection of the best module × model **per antibiotic**.
- Classifier: Logistic Regression / Random Forest / XGBoost (class-weight balanced) with an F1-tuned
  decision threshold τ.

**Reliability layer** (main contribution) — audits each configuration:

- **Statistical testing** — per-fold F1 differences over repeated CV (n = 25), paired t-test with
  Nadeau–Bengio correction, Wilcoxon, and bootstrap CIs, Holm-corrected across drugs.
- **Lineage-aware split** — pairwise SNP (Hamming) distance clustered (Ward) into sub-lineages that
  define `GroupKFold`; MLST groups for external data.
- **Negative control** — label shuffling collapses balanced accuracy to ~0.5.
- **Mutation validation** — real QRDR calling (gyrA 83/87, parC 80/84) as mechanism-based features.
- **Deployability** — isotonic calibration, operating points, decision-curve net benefit.

---

## Repository structure

```
.
├── code/           # 26 analysis notebooks (01–26), one per research "direction"
├── report/         # LaTeX thesis (main.tex → main.pdf) + architecture.drawio
├── results/        # Frozen result tables (CSV) + per-direction Markdown summaries
├── figures/        # Figures used in the report
├── data_doc_figs/  # Data-documentation figures (accessory, SNP, labels, ...)
├── slides/         # Presentation material
├── scripts/        # Helper scripts (e.g. project inventory)
├── archive/        # Earlier drafts / superseded material
└── requirements.txt
```

### Notebooks (`code/`)

| Group | Notebooks | Purpose |
|---|---|---|
| Baseline & signal | `01_baseline` · `02_stability` · `03_signal_source` · `04_temporal` | Baseline models, stability, accessory-vs-SNP signal source |
| Biology & imbalance | `05_bio_interp` · `06_imbalance` · `07_phylogeny` · `08_functional` · `09_network` | Interpretation, class imbalance, phylogeny, functional/network views |
| Feature modules | `10_ensemble_select` · `11_sample_graph` · `12_marker_hybrid` · `13_gene_embed` | The four fusion feature modules |
| Adaptive fusion | `14_adaptive_fusion` · `15_antibiotic_aware` · `16_new_drug` | Per-antibiotic module × model selection |
| External validation | `17_external_tet` · `18_external_multi` · `19_external_robust` · `25_external_mlst` | BV-BRC external drugs, MLST group-aware split |
| Reliability | `20_stat_test` · `21_stat_test_fusion` · `23_calibration` · `24_lineage` | Statistical tests, calibration, lineage-aware validity |
| Mechanism | `22_annotation` · `26_mutation` | Gene annotation, QRDR mutation calling |

Each notebook corresponds to a "Direction" whose frozen outputs and a written summary live in
`results/` (see `results/README.md`).

---

## Getting started

```bash
# 1. Clone
git clone <repo-url>
cd salmonella

# 2. Environment (Python 3.10+)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Run the notebooks
jupyter lab   # open code/01_baseline.ipynb and work through 01 → 26
```

**Dependencies** (`requirements.txt`): pandas, numpy, scipy, scikit-learn, xgboost, matplotlib,
networkx, biopython, requests, openpyxl, jupyter, nbformat.

### Data

The genomic inputs are **not committed to this repo**. They come from the original 2025 study's
public repository:

**https://github.com/347251369/Antimicrobial-resistance-prediction-in-Salmonella**

Download it and place the files under a local `data/` directory. It provides, for each of the five
original antibiotics:

- 50 "paper-ready" expert markers (per-genome gene table),
- the accessory gene matrix (1167 × 18125 binary, from Roary),
- the core-SNP matrix (126,087 positions × 1167 genomes),
- and the S/R labels (strongly imbalanced, resistance rate 6.1%–17.1%).

All three sources are aligned by genome accession (verified to match 100%). The notebooks document
the exact CSV/TSV formats. The **external** validation genomes are queried programmatically from
[BV-BRC](https://www.bv-brc.org/) inside the external-validation notebooks (S/R labels, functional
gene-family features, and MLST type via the API — no raw reads required).

### Reproducing the report

```bash
cd report
latexmk -pdf main.tex     # or: pdflatex main.tex (×2) + biber
```

The compiled thesis is `report/main.pdf`.

---

## Results

Frozen result tables and readable summaries are in `results/`:

- `ROBUSTNESS_SUMMARY.md` — adaptive fusion vs expert markers (statistical parity).
- `LINEAGE_AWARE_SUMMARY.md` — the central validity check (population-structure confounding).
- `EXTERNAL_VALIDITY_SUMMARY.md` — BV-BRC real-prevalence + MLST group-split.
- `DEPLOYABILITY_SUMMARY.md` — calibration & screening operating points.
- `MUTATION_QRDR_SUMMARY.md` — quinolone QRDR mutation evidence.
- `BIOLOGICAL_INTERPRETATION_SUMMARY.md` — gene-level interpretation & limitations.
- `claim_evidence_limitations.csv` — every claim paired with its evidence and caveat.

> These are a manual snapshot of already-run notebook outputs, curated for writing the report — not
> a fresh automated pipeline run. Re-running the notebooks reproduces them.

---

## Citation

If you use this work, please cite the thesis and the baseline paper:

```bibtex
@mastersthesis{loan2025salmonella,
  title  = {Antibiotic-aware Adaptive Feature Fusion for Salmonella
            Antimicrobial Resistance Prediction},
  author = {Nguyen, Bich Loan},
  year   = {2025}
}

@article{you2025amr,
  title     = {Developing a Predictive Platform for Salmonella Antimicrobial
               Resistance Based on a Large Language Model and Quantum Computing},
  author    = {You, Yujie and Tan, Kan and Jiang, Zekun and Zhang, Le},
  journal   = {Engineering},
  volume    = {48},
  number    = {5},
  pages     = {174--184},
  year      = {2025},
  doi       = {10.1016/j.eng.2025.01.013},
  publisher = {Elsevier}
}
```

## Author

**Nguyen Bich Loan** — thesis author.

## License

No license file is currently included; all rights reserved by the author unless stated otherwise.
Add a `LICENSE` file if you intend to permit reuse.
