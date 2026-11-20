# Generative vs. Discriminative Models for POS Tagging

Comparing **HMM** (generative) with **MaxEnt / MEMM** and **CRF** (discriminative) for part-of-speech tagging
on Vietnamese and English, using [Universal Dependencies](https://universaldependencies.org/) treebanks
with the 17-tag UPOS tagset.

Machine Learning course project (CO3117), HCMUT. Vietnamese version: [README.vi.md](README.vi.md).

## Research questions

| | Question | Experiment |
|---|---|---|
| RQ1 | How does training-set size affect generative vs. discriminative models? (Ng & Jordan, 2002) | Learning curves on 5% → 100% of train |
| RQ2 | Which model handles unseen (OOV) words better, and why? | OOV accuracy; HMM UNK strategies; error analysis |
| RQ3 | Which features help, and is it language-dependent? | CRF feature-group ablation (vi, en); genetic algorithm |
| RQ4 | Does modelling the whole sequence beat per-token classification? | MaxEnt vs. MEMM vs. CRF with identical features (label bias) |

## Results (development phase)

All hyperparameters are chosen by 3-fold cross-validation **on train** (`scripts/tune.py`); the test set is
used only once, at the end. Models are compared on **5-fold cross-validation on train for Vietnamese** and
on **dev for English**. The VTB dev set is distributed differently from train and test: a third of its
sentences are longer than 25 words, while train and test have none
([docs/notes/GHI_CHU.md](docs/notes/GHI_CHU.md), section 2). The full VTB dev set is kept only for a side
experiment on sentence length ([analysis_vi_dev.md](results/tables/analysis_vi_dev.md)).
Full tables: [results_cv.md](results/tables/results_cv.md) (vi), [results_dev.md](results/tables/results_dev.md).

| Model | vi token acc (CV) | vi OOV acc (CV) | en token acc (dev) | en OOV acc (dev) |
|---|---|---|---|---|
| Most-frequent-tag baseline | 86.07% | 37.96% | 86.13% | 29.56% |
| HMM (add-α, single UNK) | 83.62% | 13.25% | 87.47% | 25.68% |
| HMM (signature UNK, tuned) | 85.15% | 48.61% | 90.74% | 64.25% |
| MaxEnt (per token) | 90.37% | 66.14% | 94.41% | 78.97% |
| MEMM | 90.60% | 67.65% | 94.52% | 79.11% |
| **CRF** | **90.45%** | **67.28%** | **94.78%** | **79.44%** |

Vietnamese numbers are means over 5 folds (fold-to-fold standard deviation 0.6–0.9 points). They are higher
than dev or test accuracy because sentences from the same article can end up on both sides of a fold, so
compare models within a column, not across columns.

Key findings:

- **RQ1** – CRF beats HMM at *every* training size, including 5% of train (on Vietnamese, in every fold);
  we do not observe the crossover predicted by Ng & Jordan. On Vietnamese the gap narrows from 11.4 points
  at 5% of train to 5.3 points at 100% ([learning_curve_vi.png](results/figures/learning_curve_vi.png),
  [learning_curve_en.png](results/figures/learning_curve_en.png)).
- **RQ2** – OOV handling dominates the HMM's performance: signature-based UNK classes raise HMM OOV
  accuracy from 13% to 49% (vi) and 26% to 64% (en). CRF still leads the HMM on OOV by 19 (vi) and
  15 (en) points thanks to affix/shape features. On Vietnamese, the tuned HMM is 0.92 points *below* the baseline
  (p < 0.001). The loss comes from words seen once in training: the HMM maps them to UNK classes during
  training, so it tags them correctly only 49% of the time against 91% for the baseline. On OOV and
  ambiguous words the HMM beats the baseline ([analysis_vi_cv.md](results/tables/analysis_vi_cv.md)).
- **RQ3** – Vietnamese: every group except ±2 context lowers accuracy when removed, in 5 of 5 folds. The
  largest drops come from ±1 context (−0.61), affixes (−0.52) and shape (−0.43); these are within 0.2 points
  of each other, so their order is not reliable. The VTB dev set had suggested that shape mattered most and
  affixes hardly at all. English: *±1 context* and *affixes*. ±2 context does not help in either language;
  the genetic algorithm independently drops it ([ablation_vi.md](results/tables/ablation_vi.md),
  [ablation_en.md](results/tables/ablation_en.md), [ga_vi.md](results/tables/ga_vi.md)).
- **RQ4** – With identical features, MaxEnt, MEMM and CRF are within 0.4 points; the feature set matters far
  more than the sequence model on these data.

## Data

| Language | Treebank |
|---|---|
| Vietnamese | [UD_Vietnamese-VTB](https://github.com/UniversalDependencies/UD_Vietnamese-VTB) |
| English | [UD_English-EWT](https://github.com/UniversalDependencies/UD_English-EWT) |

Data is not included; download with `scripts/download_data.py` (UD `master` branch, retrieved 2026-10-24).
Each treebank has its own license.

## Layout

```
src/
  data.py             CoNLL-U reader
  baseline.py         most-frequent-tag baseline
  hmm.py              bigram HMM + Viterbi (numpy), UNK strategies
  features.py         named CRF/MaxEnt feature groups
  crf.py              CRF (sklearn-crfsuite)
  memm.py             MaxEnt and MEMM (+ Viterbi)
  evaluate.py         predict_all / metrics(mask) / save & load predictions
  model_selection.py  sentence-level k-fold, grid search, subsampling
  stats.py            paired bootstrap, McNemar
  ga.py               genetic algorithm over feature groups
scripts/              download_data, eda, tune, run_experiments, learning_curve, analyze, ablation
configs/              best_params.json (generated by tune.py)
results/tables, results/figures   committed tables and figures
tests/                pytest (no UD data required)
```

## Quick start

Python 3.11.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

make all          # data, tests, EDA, tuning, dev results, learning curve, ablation, analysis
make final        # evaluate on TEST — run only once
```

Or with Docker: `docker build -t pos-tagging . && docker run --rm -v "$PWD/results:/app/results" pos-tagging`.

## Citation

Data: Universal Dependencies (Nivre et al., 2020); UD_Vietnamese-VTB; UD_English-EWT (Silveira et al., 2014).

## License

Code: MIT ([LICENSE](LICENSE)). Data: see each UD treebank.
