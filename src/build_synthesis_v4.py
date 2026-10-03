from pathlib import Path
from decimal import Decimal
import json,pandas as pd
from check_inputs import validate_inputs
validate_inputs()
R=Path(__file__).resolve().parents[1];O=R/'results'
p=pd.read_csv(R/'results/analysis_panel_v4.csv',dtype={'utility_id':str});primary=p[p.gallons.eq(4000)&p.main_eligible].sort_values('utility_name');bridge=pd.read_csv(R/'results/price_bridge_v4.csv',dtype={'utility_id':str}).set_index('utility_id')
e=json.loads((R/'data/events_current.json').read_text())
coding=json.loads((R/'data/documentary_judgments.json').read_text())
D=coding['reconstruction']
assert set(D)==set(primary.utility_id)
rows=[]
for x in primary.itertuples():
 b=bridge.loc[x.utility_id];d=lambda z:Decimal(str(z)).quantize(Decimal('.01'));a=d(b.base_bill_2019);c=d(b.base_bill_2024);t19=d(b.charge_inclusive_bill_or_scenario_2019);t24=d(b.charge_inclusive_bill_or_scenario_2024)
 proc,why,limit,ref=D[x.utility_id]
 rows.append(dict(utility_id=x.utility_id,utility_name=x.utility_name,base_2019=float(a),extra_2019=float(t19-a),base_2024=float(c),extra_2024=float(t24-c),total_2019=float(t19),total_2024=float(t24),delta_base=float(c-a),delta_extra=float((t24-c)-(t19-a)),delta_total=float(t24-t19),documented_proceedings=proc,document_supported_interpretation=why,material_limit=limit,evidence_reference=ref,temporary_extra_absent_both_endpoints=coding['temporary_extra'][x.utility_id],component_scope=coding['component_scope']))
r=pd.DataFrame(rows);assert r.utility_id.nunique()==20
assert [round(r[c].sum(),2) for c in ['delta_base','delta_extra','delta_total']]==[207.14,7.33,214.47]
r.to_csv(R/'results/Reconstruction_Summary_20_v4.csv',index=False)
# Original selection record supplies stratum and screen; current panel supplies price/eligibility.
s=pd.read_csv(R/'data/selection_frame_34.csv',dtype={'utility_id':str});q=p[p.gallons.eq(4000)].set_index('utility_id');assert len(s)==34
excluded=coding['excluded']
disp=[]
for x in s.sort_values('utility_name').itertuples():
 uid=x.utility_id;present=uid in q.index;z=q.loc[uid] if present else None;included=bool(z.main_eligible) if present else False
 status=('Supported' if z.price_status=='supported' else 'Conditional') if present else 'Not reconstructed'
 reason,ref=excluded.get(uid,coding['default_disposition'])
 if uid in coding['included_overrides']:reason,ref=coding['included_overrides'][uid]
 disp.append(dict(utility_id=uid,utility_name=x.utility_name,original_stratum=x.original_stratum,endpoint_pair_reconstructed=present,price_classification=status,legacy_price_status=z.price_status if present else x.price_status,account_screen_pass=bool(x.conservative_screen_pass),primary=included,decision_reason=reason,evidence_reference=ref))
d=pd.DataFrame(disp);assert len(d)==34 and d.endpoint_pair_reconstructed.sum()==32 and d.price_classification.eq('Supported').sum()==27 and d.primary.sum()==20
assert d[d.primary].original_stratum.value_counts().to_dict()=={'nondeclining':11,'declining':9}
d.to_csv(R/'results/Selected_34_Disposition_v4.csv',index=False)
# Preserve event totals while correcting the single proceeding label.
(O/'events_v4.json').write_text(json.dumps(e,indent=2))
ledger=pd.read_csv(R/'data/event_classification_current.csv');ledger['regulatory_category']=[next(x.get('regulatory_category') for x in e if x['event_id']==id) for id in ledger.event_id];ledger.to_csv(R/'results/Event_Ledger_Classification_v4.csv',index=False)
schedules=ledger[~ledger.record_type.eq('amending_order')]
surcharges=json.loads((R/'data/surcharges.json').read_text());cases=sorted({x['case'] for x in e+surcharges if x.get('case')})
first=sum(bool(x.get('verified_first_billing_month') or x.get('assessment_reported_first_billing_month')) for x in surcharges)
collection=sum(bool(x.get('assessment_reported_collection_start_month')) and not bool(x.get('verified_first_billing_month') or x.get('assessment_reported_first_billing_month')) for x in surcharges)
counts=dict(event_rows=len(e),schedule_authorization_rows=len(schedules),baseline_anchors=int(ledger.record_type.eq('baseline_anchor').sum()),subsequent_schedule_authorization_rows=int((~schedules.record_type.eq('baseline_anchor')).sum()),arithmetic_price_change_rows=int(ledger.base_price_changed_4000.eq(True).sum()),zero_base_change_rows=int(ledger.base_price_changed_4000.eq(False).sum()),amendment_rows=int(ledger.record_type.eq('amending_order').sum()),superseded_schedule_rows=int(ledger.record_type.eq('superseded_schedule').sum()),separate_recurring_charge_records=len(surcharges),combined_logical_records=len(e)+len(surcharges),distinct_recorded_case_ids=len(cases),case_ids=cases,schedule_rows_without_case_id=int(schedules['case'].isna().sum()),unique_resolved_pdf_hashes=len({x['sha256'] for v in e for x in v['resolved_sources']}),unresolved_source_references=[],legally_operative_period_count=None,unique_implemented_price_change_count=None,billing_or_collection_start_reported_districts=first+collection,first_billing_month_supported_districts=first,collection_start_only_districts=collection)
(O/'ledger_counts_v4.json').write_text(json.dumps(counts,indent=2))
summary={'primary':20,'selected':34,'reconstructed':32,'supported':27,'conditional_including_legacy_regional':5,'not_reconstructed':2,'retention_pct':100*20/34,'retained_declining':9,'selected_declining':17,'retained_nondeclining':11,'selected_nondeclining':17,'base_increase_districts':int((r.delta_base>0).sum()),'zero_endpoint_change_districts':int((r.delta_total==0).sum()),'positive_net_extra_districts':int((r.delta_extra>0).sum()),'base_total':207.14,'extra_total':7.33,'total_change':214.47,'documentary_classification_change':'E057 retail-review label corrected to wholesale special-contract amendment; numerical fields unchanged'}
(O/'synthesis_checks_v4.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
