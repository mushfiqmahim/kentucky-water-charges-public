# Data dictionary

The statistical unit is a water district. Utility IDs are strings. Accounts are utility-reported residential connections, not people or occupied households. Dollar fields are nominal monthly charges unless expressly identified otherwise. Empty CSV fields and JSON `null` mean unavailable or not applicable in the recorded context, not zero. Literal qualifications remain part of the data.

## Files and roles

| File | Rows/unit | Role |
| --- | --- | --- |
| analysis_inputs_v4.csv | 96 district–consumption rows; 32 districts; 44 columns | Compiled analytical input. Three consumption scenarios per district |
| Source_Verification_Register_v4.csv | 40 district–year endpoints | Coded tariff schedules for the 20 primary districts |
| Endpoint_Account_Source_Check.csv | 40 district–year endpoints | Primary account source pages and hashes |
| Benchmark_Comparability_Register.csv | 20 districts | Literal tariff category, meter, territory and comparability decisions |
| Supplier_Register.csv | 40 district–year records | Incomplete vendor evidence; not a supplier exposure matrix |
| selection_frame_34.csv | 34 selected districts | Original strata, account screen and inherited dispositions; current decisions are in results/Selected_34_Disposition_v4.csv |
| stage2_district_screen.csv | 97 candidates | Original screening frame, before the separate Daviess correction |
| residential_customer_panel_2019_2024.csv | 736 utility–year rows | Inherited six-year account extraction supporting continuity review; larger than the selected sample |
| customer_continuity_flags.csv | 70 utility–year rows | Broad continuity-review flags, not the final exclusion list |
| merger_screening.csv | 118 utility records | Reported merger-history text and in-window mention flags |
| tariff_feasibility_sample.csv | 34 districts | Original tariff draw and directory matching |
| surcharges.json | Six recurring-charge records | Documentary input, including billing/collection qualifications |

## Compiled analysis fields

| Field or family | Definition |
| --- | --- |
| utility_id; utility_name | PSC identifier and recorded district name |
| gallons | Fixed monthly volume: 2,000, 4,000 or 6,000; not an additional independent observation |
| price_status | `supported`, `conditional`, or legacy `regional`; Garrison's regional code is displayed as conditional in the readable disposition |
| base_bill_2019; base_bill_2024 | Reconstructed base charge in dollars, before separate recurring extras |
| charge_inclusive_bill_or_scenario_2019; _2024 | Base plus coded recurring extras; scenario validity depends on price_status |
| 2019; 2024 | Reported year-end residential accounts, PSC account 461.1 |
| customer_change_pct | 100 × (N2024/N2019 − 1), ordinary percent |
| district_name_flag | Inherited district-name candidate flag; not a legal-entity audit |
| counties_reported; counties_reported_2019; _2024 | Literal reported served-county sets; the unsuffixed field is inherited endpoint metadata |
| operating_margin_pct_2019; _2024 | 100 × (operating revenue − full operating expenses)/operating revenue; inherited descriptive financial fields |
| operating_revenue_2019; _2024 | Reported annual operating revenue, nominal dollars; not benchmark charge revenue |
| full_operating_expenses_2019; _2024 | Reported annual full operating expenses, nominal dollars |
| arc_group_2019; _2024 | ARC classification of reported county sets; not customer-weighted service areas |
| county_set_changed | Whether the reported endpoint county sets differ |
| documented_in_window_merger | Inherited documented 2020–2024 merger flag; blank history alone does not prove no transfer |
| screening_status | Inherited textual candidate/screen qualification |
| margin_change_pp | 2024 minus 2019 operating margin, percentage points |
| material_customer_flag | Original material continuity flag: absolute annual end-account change >10% or start/prior-end discrepancy >1% |
| years_observed | Count of observed annual reports across 2019–2024 |
| conservative_screen_pass | Six observed years, unchanged reported counties, no documented in-window merger and no material customer flag |
| x | 100 × ln(N2024/N2019), log points |
| ln_n19 | Natural logarithm of 2019 accounts |
| declining | Negative endpoint residential-account change; distinct from diagnostic neutral bands |
| ln_bill19 | Natural logarithm of 2019 full benchmark charge, not raw initial dollars |
| y_base; y_full | 100 × ln(B2024/B2019), using base-only or full charges |
| full_pct_change | 100 × (B2024/B2019 − 1), ordinary nominal percent |
| bill_change_dollars | Full 2024 charge minus full 2019 charge, nominal dollars |
| arc_all; arc_mixed | Indicators for all-ARC and mixed reported county sets |
| main_eligible | Current primary inclusion: supported benchmark plus unchanged account screen; Knott is included |
| design_weight | Original draw weight: 1 for initial decliners, 80/17 for sampled nondecliners; does not repair later exclusions |
| real_pct_change | 100 × [(B2024/B2019)/(315.605/256.974) − 1]; BLS December CPI-U CUUR0000SA0 |
| main_eligible_v2 | Legacy inclusion flag retained for provenance; not current primary membership |

The active analysis recalculates primary tariff arithmetic from the 40-row register, overwrites the matching compiled prices, then recomputes transformations. The other reconstructed pairs remain compiled inputs. It does not freshly transcribe every source document. `account_pct` in the generated panel is the recomputed ordinary account change; `customer_change_pct` is inherited.

## Tariff and account registers

Tariff keys are `utility_id` and `year`. `base_schedule_effective_date` applies to the selected base schedule; `component_date_note` preserves separate timing. `minimum` is dollars; `included_gallons` is the allowance; `applicable_blocks_per_1000` is JSON containing incremental gallon widths and dollars per 1,000 gallons, with `null` for an unlimited final block. `applied_extra` is dollars per month; `extra_per_1000` is dollars per 1,000 gallons. `base_2000/4000/6000` and `total_2000/4000/6000` are cent-rounded coded calculations. Final tariff amounts use decimal half-up rounding.

`meter_size`, `customer_category`, and `territory` retain literal distinctions. `surcharge_evidence`, `verification`, `notes`, `correction`, `component_date_note` and `printed_extra_note` distinguish selected components, corrections and uncertainty. A zero extra is benchmark coding, not proof that no household paid another charge. `source_file` is now edition-root relative; `source_url`, `pdf_page` and `source_sha256` retain original provenance.

The account register uses `residential_start`/`residential_end` from the named `row` (account 461.1), with `source_file`, `pdf_page` and `sha256`. In the six-year panel, `previous_end`/`previous_year` refer to the prior observation, `consecutive` flags adjacent years, `start_previous_end_gap` is a signed account difference, and `annual_end_change_pct` is ordinary percentage change between consecutive year-end counts. The review flag file includes gaps exceeding one account; that rule is broader than the primary screen's 1% threshold.

The comparability register records `population`, `meter_category`, `tariff_customer_category`, `tariff_territory`, `benchmark_comparability`, `shares`, `coverage_class`, `decision` and `qualification`. Year-specific account/tariff source and page fields identify the evidence; `county_page_2019/2024` identifies the service-county page. Unknown shares are not imputed weights. The supplier register's `vendor_literal` is reported text, `status` qualifies it, and `supplier_volumes` remains unattributed where unavailable.

In selection records, `original_stratum` precedes tariff review. `max_abs_annual_pct` and `max_abs_gap_pct` summarize available comparisons; `years` lists observed years. `decision_reasons` and inherited `main_eligible` describe their recorded stage. Only the current panel's `main_eligible` selects the v4 primary sample. In feasibility records, `folder_name`, `folder_url` and `name_match_score` describe tariff-directory matching. `merger_history_reported` is literal report text; `mentions_2020_2024` is a screening aid, not a complete legal history.

## Documentary records and generated outputs

`results/events_v4.json` has 76 schedule/amendment records keyed by `event_id`. `district_id`, `district`, `case` and `record_type` identify context. `schedule_parameters` and `base_bill_4000` describe coded arithmetic. `document_date`, `approval_date`, `event_date`, `service_effective_date`, `date_basis`, `first_billing_month`, `amends_event_id` and `superseded_by_event_id` must not be treated as interchangeable. Some inherited approval dates refer to parent orders. `legal_status`, `billing_evidence_status`, `evidence_status` and `notes` preserve qualifications; `resolved_sources` links IDs/pages/URLs/hashes to canonical files. E057 retains its former label and the v4 correction note. The current authored ledger is `data/events_current.json`; synthesis writes its corresponding current result.

`surcharges.json` uses `record_id` S01–S06, `monthly_charge`, `approval_date`, `case`, `collection_cap` and `maximum_months`. `verified_*` retains the earlier coding designation; `assessment_reported_*` distinguishes reported first billing from collection starts. Neither implies a new human audit. Nested sources and update evidence retain page references and caveats. Missing billing months remain unknown.

`results/Event_Ledger_Classification_v4.csv` is generated from the coded ledger. It describes logical records, not a census of implemented price changes. `ledger_counts_v4.json` contains counting units and explicit unknown legally operative periods. District interpretations and exclusion reasons are authored in `data/documentary_judgments.json` and read by `src/build_synthesis_v4.py`. `results/Reconstruction_Summary_20_v4.csv` supplies endpoint components, differences, proceeding interpretations and limitations. `results/Selected_34_Disposition_v4.csv` separates price classification, account screen and primary membership.

`models_v4.json` retains all 13 specifications and all 41 coefficient records with estimates, HC3 SEs and 95% t intervals. `models_v4.csv` summarizes the account-growth slope, sample size, residual degrees of freedom, p-value and R-squared. The dollar-change model has a dollar outcome; the other growth outcomes use log points. Diagnostic CSVs in results contain current v4 rows only. `leave_one_out_v4.csv` and `influence_v4.csv` describe sensitivity and conventional OLS influence, not evidence that an observation is wrong. `manuscript_tables.json` and `supplement_tables_v4.json` are generated display text; underlying data retain precision. Figure PNG/PDF pairs are reading formats of the same two research figures.

Source IDs, document roles and all original path aliases resolve through [the source catalogue](../sources/catalog.csv). Page references refer to the retained PDF's page sequence unless explicitly identified otherwise. See [evidence.md](../docs/evidence.md) for sample and documentary limitations.

## Current documentary inputs and fixed references

| File | Unit and fields | Role |
| --- | --- | --- |
| `documentary_judgments.json` | District-ID keys. `reconstruction` tuples contain proceeding description, supported interpretation, limitation, and evidence reference, in that order. `excluded` and `included_overrides` pairs contain decision reason and supporting reference. `temporary_extra` preserves the district-specific billing qualification. | Authored interpretations previously embedded in synthesis code; read without reinterpretation. Utility IDs are strings; missing evidence is stated, not imputed. |
| `events_current.json` | 76 event records, keyed by `event_id`; `district_id`, document/service dates, record type, 4,000-gallon base dollars, decimal-string tariff blocks, preceding change, linked case, source IDs/pages and resolved paths/hashes, legal/billing qualifications. Null dates mean unestablished, not zero. | Current coded schedules and amendments. `regulatory_category_v3` and `v4_classification_note` preserve the consequential E057 correction. |
| `event_classification_current.csv` | One row per event, 76 rows. `record_type` determines counting unit; `base_price_changed_4000` is a Boolean for schedule changes and blank for anchors/amendments. Source and date meanings follow the event JSON. | Current classification ledger used by synthesis; no historical directory required. |
| `coding_provenance.json` | E057 prior and corrected classification, complete retained source references and prior-value provenance. | Documentary correction record; neither monetary values nor dates change. Other consequential corrections are in the tariff/comparability registers and `docs/evidence.md`. |
| `reference/current_reference.json` | Fixed input SHA-256 values, current CSV/JSON values and figure hashes captured from Stage 1 before execution; explicit statistical tolerances. | Regression-test expectations, not newly authored observations. Never generated by analysis or validation. Future scientific changes require a documented comparison before intentionally revising this reference. |

Dates are ISO dates where established; prose qualifiers must not be parsed as exact billing dates. `sources/catalog.csv` resolves source IDs to expected canonical paths and retains URLs, original paths, dates, page references, qualifications and current event-input references. `sources/access.csv` distinguishes 54 bundled orders, 158 reference-only originals and one held index with an unresolved original URL; fixed source identities remain unchanged. A source link records provenance, not proof of its interpretation or present availability. Generated outputs are in `results/`; authored manuscript/supplement prose is in `paper/manuscript.md`, `paper/supplement.md` and `paper/Source_Followup_v4.md`.
