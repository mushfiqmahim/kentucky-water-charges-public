# Reproduction

## Environment

Use Python 3.12 and `requirements.txt`: numpy 2.3.5, pandas 2.2.3, scipy 1.17.0, matplotlib 3.10.8 and python-docx 1.2.0. The tested environment used Python 3.12.14. LibreOffice is optional for DOCX-to-PDF conversion.

Two separate workflows distinguish numerical reproduction from original-source integrity. Neither independently validates documentary interpretations or reconstructs the complete original collection and screening process.

## Numerical reproduction

Run from the project root in a disposable copy; commands overwrite generated outputs. No private originals, historical fixtures, network access or saved model results are needed as calculation inputs.

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/analyze_v4.py
python src/build_synthesis_v4.py
python src/build_manuscript_v4.py
python src/build_supplement_v4.py
python src/validate_v4.py
```

On Windows PowerShell use `.venv\Scripts\Activate.ps1` to activate.

`check_inputs.py` checks all 16 fixed compiled-input hashes, the unchanged reference identity, CSV schemas and unique keys, event/recurring-charge keys and declared source identities. Missing or altered required compiled inputs fail. No command regenerates reference expectations.

`analyze_v4.py` recalculates the 40 primary tariff endpoints at 2,000, 4,000 and 6,000 gallons from coded blocks, minimums and recurring extras. It estimates all 13 models from the 96-row compiled panel, recomputes diagnostics and draws both figures. Other reconstructed districts' prices remain compiled inputs. The second algebraic HC3 implementation is a numerical cross-check, not independent human review.

`build_synthesis_v4.py` recomputes district reconstructions, dispositions and ledger counts from current event, surcharge, selection and documentary-decision inputs. The E057 classification correction remains in `data/coding_provenance.json`. The builders combine fresh results with `paper/manuscript.md`, `paper/supplement.md` and `paper/Source_Followup_v4.md` to generate DOCX, complete Markdown and table JSON.

`validate_v4.py` compares fresh results with fixed `data/reference/current_reference.json`, checks all 13 models and 41 coefficient records, exact membership and sample counts (20 primary, 27 supported, 32 reconstructed, 34 selected), account linkage, cent identities, reconstruction totals, event counts, diagnostics, figure PNGs and all 12 document tables. It writes only `results/numerical_validation_v4.json`; it does not verify original bytes or issue a source-completeness receipt.

Statistical comparisons retain absolute tolerance 1e-9 with relative tolerance zero; selected descriptive checks use 1e-7. Categories, IDs, counts and cents are exact. Tariff arithmetic retains the 1e-8-dollar tolerance alongside cent and fixed-input checks.

## Original-source verification

Run separately:

```sh
python src/verify_sources.py
```

The command checks catalogue coverage, declared references and all 213 expected original sizes, SHA-256 values and Git blob identities. It writes `results/source_verification.json` with a per-document status. Exit code 0 means all originals match; 2 means coverage is incomplete because files are missing; 1 means an incorrect identity or invalid source reference. Incorrect bytes and absent files are reported separately. No documents are downloaded automatically.

This distribution verifies 54 bundled PSC orders and reports 159 missing originals: 158 are available by recorded original-host reference, and one archived annual-report index has no verified original URL. [sources/access.csv](../sources/access.csv) records each expected path, identity, analytical role and access qualification.

The Knott named-customer tariff compilation, Western Fleming monitoring filing with bank identifiers and Kentucky affordability report remain excluded. Other nonbundled originals are utility filings, financial statements, staff correspondence and institutional HTML whose republication basis is unresolved. Retained administrative orders are a distinct document class; Kentucky state works are not treated as federal-government works.

For complete verification, supply exact originals at their catalogue paths only in a private disposable copy. The ignore rules allow only the 54 selected originals to enter a fresh public history. Do not commit restored reference-only files. A changed live-host file is not the recorded source. Numerical success cannot establish complete source-file coverage.

## Documents and checked results

The numerical workflow was tested before the source-distribution changes in a fresh ZIP extraction after removing regenerable results and DOCX/complete-Markdown outputs. The present edition retains byte-identical code, numerical inputs, fixed references, results and paper files; focused input/reference and source-verification checks were repeated after the access changes. All five commands passed without originals. All numerical CSV/JSON results and figure PNGs agreed with the preserved baseline; figure PDFs agreed in text and rendered pixels. Both DOCX builders reproduced identical internal document members, and all 12 tables passed validation. The primary result remains N=20, slope −1.2310921377721913, HC3 interval [−2.7937591248238163, 0.3315748492794337], and $207.14 + $7.33 = $214.47.

Before this distribution change, separate source verification reported 210 verified and three missing originals; a private copy with all 213 exact originals passed. The present distribution was checked separately: 54 verified, 159 missing, none incorrect (exit code 2). The earlier complete-source result is not a receipt for this distribution. Negative checks rejected altered/missing compiled inputs and incorrect source bytes. These scopes remain distinct from source interpretation.

The reviewed paper and supplement are unchanged reading copies, with the earlier 30- and 11-page visual inspection retained. Their builders and tables were compared; no new PDF export was necessary. To make new PDFs after an authorized revision, with LibreOffice on PATH:

```sh
mkdir pdf_rebuild
libreoffice --headless --convert-to pdf --outdir pdf_rebuild paper/KEA_Manuscript_v4.docx paper/Supplement_v4.docx
```

Inspect new exports before replacing reading copies. Fonts, conversion settings and metadata can affect layout. [Evidence notes](evidence.md) retain the scientific qualifications and assistance/review scope.
