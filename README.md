# Customer Base Change and Approved Water Charges in Kentucky, 2019–2024

MD. Mushfiquzzaman Mahim · Berea College  
Working paper revised October 2, 2026

How are changes in residential water accounts associated with changes in approved water charges? This study links Kentucky Public Service Commission annual reports, historical tariffs and regulatory orders for 2019–2024. It compares charges at a common consumption level and reconstructs the rate decisions behind the endpoint changes. Customer losses may put pressure on a utility's revenue, but investment, purchased-water costs and regulatory timing can also change its charges.

Read the [paper (PDF)](paper/KEA_Manuscript_v4.pdf), [editable paper (Word)](paper/KEA_Manuscript_v4.docx) and [supplement (PDF)](paper/Supplement_v4.pdf). The authored sources are [manuscript.md](paper/manuscript.md), [supplement.md](paper/supplement.md) and the supplement's [source notes](paper/Source_Followup_v4.md).

## Findings and limitations

The primary sample contains 20 districts: nine with declining residential accounts and eleven with growing accounts. At 4,000 gallons per month, median nominal charge growth is 34.69% for declining districts and 24.24% for growing districts. Controlling for initial account-base size, the account-growth coefficient is −1.23, with a 95% HC3 confidence interval of [−2.79, 0.33]. The estimate is imprecise; the data do not identify a causal effect. [Model outputs](results/models_v4.csv) retain full precision.

The regulatory reconstruction distinguishes base-rate changes, recurring extras, amendments and superseded approvals. Across one standardized connection in each primary district, changes sum to $207.14 in base charges and $7.33 in extras, totaling $214.47. These sums describe hypothetical monthly charges, not utility revenue or household spending.

The tariff review deliberately oversampled districts with account declines. The final sample is small and selected, and district-wide account counts may cover customers outside the designated tariff category. HC3 intervals do not resolve supplier dependence. Approved charges do not establish actual invoices, affordability or a complete billing history. [Evidence notes](docs/evidence.md) explain the sample screens, source qualifications and assistance used in preparing the research.

## Files

| Location | Contents |
| --- | --- |
| [paper/](paper/) | Paper, supplement, editable sources and reading copies |
| [data/](data/README.md) | Compiled inputs, documentary coding and source registers |
| [src/](src/) | Analysis, reconstruction, document builders and validation |
| [results/](results/) | Models, diagnostics, district tables and figures |
| [sources/](sources/README.md) | Source catalogue, original-host links and retained evidence |
| [docs/reproduction.md](docs/reproduction.md) | Commands, dependencies, tolerances and verification scope |

## Use

Use Python 3.12 and the pinned dependencies. Run overwrite-producing commands in a disposable copy.

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`. From a disposable copy, freshly calculate the results and build both documents:

```sh
python src/analyze_v4.py
python src/build_synthesis_v4.py
python src/build_manuscript_v4.py
python src/build_supplement_v4.py
python src/validate_v4.py
```

Numerical reproduction uses the distributed compiled inputs and coded evidence. Fixed input identities, schemas, sample membership and reference outputs are checked. See [docs/reproduction.md](docs/reproduction.md) for tolerances and optional PDF conversion.

Original-source verification is a separate command:

```sh
python src/verify_sources.py
```

It verifies 54 bundled PSC orders and reports incomplete coverage of the 213 expected originals. Another 158 documents are supplied through original-host references, and one archived index has an unresolved original URL. [sources/access.csv](sources/access.csv) records every path, expected hash, URL and analytical role. Numerical reproduction uses compiled inputs and does not require these original files. Complete source verification requires all 213 exact originals in a private disposable copy.

The distributed numerical workflow passed fresh reproduction for all 13 models and 41 coefficient records, figures, reconstruction and document tables. Numerical agreement and source-file identity do not independently validate documentary interpretations or reconstruct the original collection and screening process. Reviewed paper and supplement files are preserved.

## Cite

Mahim, MD. Mushfiquzzaman. 2026. *Customer Base Change and Approved Water Charges in Kentucky, 2019–2024*. Working paper, Berea College, revised October 2. See [CITATION.cff](CITATION.cff). Cite original documents through the source catalogue.

## Reuse terms

Project-authored code and configuration are licensed under MIT. Original writing, figures, tables, explanatory documentation and compiled-data contributions are licensed under CC BY 4.0, limited to rights held by MD. Mushfiquzzaman Mahim. Third-party sources, quotations and dependencies are excluded; underlying facts and public-domain material are not newly restricted. See [LICENSE.md](LICENSE.md) for scope and license references.

Repository: [kentucky-water-charges-public](https://github.com/mushfiqmahim/kentucky-water-charges-public).
