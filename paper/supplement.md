# Supplement: Customer Base Change and Approved Water Charges in Kentucky 2019 to 2024

October 2, 2026. The accompanying CSV files preserve district identifiers, source references, and full numerical precision. Inputs are in data/ and generated results in results/. This supplement gives the complete sample disposition, diagnostics, and documentary qualifications.

## 1 Complete sample disposition

Table S1 reports the price and account decisions for every selected district. “Decline” and “Nondecline” are original sampling strata, assigned before tariff reconstruction. “Supported” and “Conditional” both indicate a reconstructed endpoint pair; “No pair” means none accepted. “Pass” means passing the stated six-year reporting screen; it does not certify stable physical boundaries or perfect category continuity. Price support is assessed separately. The account screen uses annual end-count changes above 10%, opening/prior-closing discrepancies above 1%, report completeness, reported county sets and documented mergers. These thresholds are pragmatic, not externally validated optimal cutoffs.

{{S1}}

The table reconciles to 34 selected districts, 32 reconstructed pairs, 27 supported pairs and 20 primary observations. Five reconstructed pairs are displayed as conditional; Garrison retains the original “regional” code in the underlying panel. Bullock Pen and Southern Water & Sewer lack accepted reconstructed pairs. Bullock Pen is not excluded by a universal rule against geographic supplements: a completed supported non-extension pair is unavailable in the retained work. If such evidence is obtained, its price eligibility must be reconsidered consistently.

Among the 27 supported pairs, the seven account exclusions are East Pendleton, Trimble, North Hopkins, Webster, Henry #2, Barkley and Caldwell. Their detailed decisions and original page references remain in docs/evidence.md and sources/catalog.csv. Retention is 20/34 = 58.8%, 9/17 = 52.9% among initial decliners and 11/17 = 64.7% among sampled nondecliners; these retention rates do not determine the direction of selection bias.

Knott remains included: cancelled southwest usage rates do not establish an alternative ordinary endpoint category. Estill remains an explicitly non-Cobhill benchmark, with whole-district accounts and unknown shares; its sub-threshold swing is unexplained. Powell's three-county service is supported by both reports and its 2024 order. Garrison's ordinary non-extension benchmark does not resolve the separate $1.73 component ambiguity or account opening discrepancy. The full comparability decisions are preserved in docs/evidence.md.

## 2 Full-sample documentary synthesis

Manuscript Appendix B contains the readable arithmetic table and companion documentary table for all 20 primary districts, in the same order as Appendix A. results/Reconstruction_Summary_20_v4.csv supplies their full-precision data and references. Eighteen have higher endpoint base charges; two have unchanged benchmarks. Four have positive net endpoint extras. The sums $207.14 base + $7.33 extras = $214.47 are unweighted hypothetical-charge identities, not utility revenue or causal shares. Hyden's $1.53 temporary surcharge is absent at both endpoints. Estill's $3.54 is present at both. In either case, a zero endpoint difference in extras does not mean that no surcharge was billed during the interval.

Proceeding labels describe regulatory routes; economic interpretations require actual documentary support. Unknown intermediate reasons remain unknown. Pendleton E057's generic v3 rate-review label is corrected to wholesale special-contract amendment, based on the October 28, 2020 order in 2020-00158, p1. The ordinary residential base stays unchanged. This is a documentary classification correction only.

## 3 Current exploratory diagnostics

Account change is c = 100 × (N2024/N2019 − 1). For band b, decline is c < −b, growth is c > b, and neutral is |c| ≤ b. Bands are ordinary percentage units, not proportions or log points. Neutral observations are excluded only from these median comparisons; primary regression membership and continuity screening are unchanged.

{{S2}}

The current declining-versus-growing median growth gap is 10.44 percentage points. It incorporates Knott’s inclusion after review of its cancelled tariff and Muhlenberg’s corrected endpoint. The consequential source corrections are documented in docs/evidence.md. Group mean charges are $36.89→$49.77 for decline and $42.70→$51.66 for growth, with mean dollar changes $12.89 and $8.95. Different percentage denominators do not establish convergence or delayed adjustment.

{{S3}}

Omitting Powell, alone or with Estill, produces an interval below zero, but source evidence supports their designated benchmarks. These exploratory omissions are not eligibility tests. Leave-one-out slopes run from −1.633053 (omit Powell) to −0.885785 (omit Cumberland Falls Highway); Hyden has the largest Cook's distance, and its omission gives −0.921579. The incomplete supplier audit identifies South Anderson→North Mercer and Knott→Letcher, not a complete dependence network. HC3 does not account for supplier or regional dependence.

{{S4}}

Table S4 reports all 13 specifications, using the current data and eligibility rules. The dollar-change row has dollars as its outcome; other rows use 100 times a log charge ratio. No added regression was selected for significance. The raw-initial-charge adjustment and log-initial-charge adjustment are explicitly distinct. Original sampling weights do not repair later exclusions.

## 4 Documentary counting units

The ledger contains 68 schedule/authorization records, including 20 baseline anchors and 48 subsequent entries. Forty-five subsequent entries change the benchmark arithmetic and three do not. One is a superseded same-effective-date approval. Eight amendment/clarification and six recurring-charge records are coded separately: 82 logical records in total, carrying 43 distinct non-null case IDs. Twenty-four schedule rows lack a linked case ID. These are not counts of independent proceedings, implemented price changes or invoice periods. Legally operative period and distinct implemented-change totals remain unknown.

All 20 base-price paths reconcile arithmetically. That cannot exclude missing intermediate reversals. Three surcharge records support a first billing month (Hyden, Mountain and reported Henderson); Western Fleming supports a reported collection start only. Powell's first invoice and Estill's complete billing spell are unavailable. The detailed count reconciliation is preserved in docs/evidence.md. Its numerical counts remain current; the one proceeding-label correction is recorded above and in results/events_v4.json.

## 5 Financial definitions and source qualifications

{{SOURCE_FOLLOWUP}}

## 6 Literature and evidence boundaries

The Pennsylvania predecessor is Bash, Grimshaw, Horan, Stanmyer, Warren and Patterson (2020), Addressing Financial Sustainability of Drinking Water Systems with Declining Populations: Lessons from Pennsylvania. Duke's institutional record establishes authorship and the 16-system/four-case scope: https://scholars.duke.edu/publication/1565546. Exact report full text remains unavailable through the checked publisher/repository routes; no claim is made that it lacks an equivalent regression or tariff appendix. The literature search is targeted, not exhaustive.

The October 2026 review inspected the Kentucky affordability report’s methods, rate-case examples, and ratemaking appendix in full text. That report already uses fixed-consumption charges and surcharges; this paper’s addition is the 2019–2024 linkage to accounts and a common reconstruction for the primary sample. Full-text sections of Allaire and Dinar (2022), Patterson and Doyle (2021), and Patterson, Bryson, and Doyle (2023) were accessible. For Cardoso and Wichman (2022), the author-hosted February 2022 working paper’s introduction and methods were inspected alongside the published bibliographic record. It is not treated as proof of identical wording in the published article.

Bash et al. (2020), Doyle et al. (2020), August et al. (2023), Mahmood and Lane (2026), and Ormsbee et al. (2026) were checked through accessible institutional, author-hosted, or publisher summaries and metadata where complete articles were unavailable. Search-index excerpts from the Pennsylvania PDF were also available, but do not constitute inspection of the complete report. sources/cited_works.csv records source-specific coverage and URLs.

The 40 endpoint tariff records were previously checked against original pages; this edition reuses that coding. Machine checks verify hashes and arithmetic, not human double coding. Research preparation, coding, source review, and document revision used AI assistance. The present review does not constitute independent human double coding or completed faculty review. docs/evidence.md describes documentary limits, and docs/reproduction.md reports execution and comparison results.

Mountain's refund installment and calendar-duration conflicts, Hyden's earlier phase-two first billing, and Powell's first surcharge invoice remain unresolved. These are within-period limits rather than new endpoint corrections. Seven account exclusions, category shares and physical territory continuity can affect the meaning or composition of the sample. The prior source memos distinguish those issues without imputed account reallocations or invoices.

## 7 Research files and execution

The analytical observations, eligibility rules, and specifications remain those of the v4 analysis. README.md identifies the files and execution commands; docs/reproduction.md gives the tested workflow and its scope. Current validation uses fixed references in data/reference/ and requires no historical directory. Sources retain their identities and qualifications. Execution from compiled inputs does not reconstruct the original collection and screening process; availability of the source files does not establish redistribution permission.

The paper and supporting files are provided in this private working edition. No public release URL or DOI has been assigned. Paths in this supplement are relative to the edition directory unless stated otherwise.
