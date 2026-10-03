"""Validate compiled inputs and declared source identities without opening originals."""
from pathlib import Path
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_SHA256 = '3dea12b82c15ad525bd370b4435a17a1c4e9346b248452c279abb7c9c113b4fe'

def load_reference(root=ROOT):
    path = root / 'data/reference/current_reference.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == REFERENCE_SHA256, 'fixed reference changed'
    return json.loads(path.read_text())

def csv_rows(path, required, keys, count):
    with path.open(newline='') as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames
        assert fields and len(fields) == len(set(fields)), ('duplicate/missing fields', path.name)
        assert set(required).issubset(fields), ('required fields', path.name, required)
        rows = list(reader)
    assert len(rows) == count, ('row count', path.name, len(rows), count)
    assert all(None not in r and all(v is not None for v in r.values()) for r in rows), ('row schema', path.name)
    if keys:
        identities = [tuple(r[k] for k in keys) for r in rows]
        assert all(all(v for v in key) for key in identities), ('empty key', path.name)
        assert len(set(identities)) == len(rows), ('duplicate key', path.name, keys)
    return rows

def source_catalog(root=ROOT):
    reference = load_reference(root)
    rows = csv_rows(root / 'sources/catalog.csv',
                    ['path','sha256','git_blob','bytes','source_ids'], ['path'], 213)
    catalog = {r['path']:r for r in rows}
    assert catalog.keys() == reference['sources'].keys(), 'fixed source coverage'
    for path, row in catalog.items():
        assert path.startswith('sources/files/') and '..' not in Path(path).parts, ('source path',path)
        fixed = reference['sources'][path]
        assert all(row[k] == fixed[k] for k in ['sha256','git_blob']), ('fixed source identity',path)
        assert int(row['bytes']) == int(fixed['bytes']), ('fixed source size',path)
    ids = [sid for r in rows for sid in json.loads(r['source_ids'])]
    assert len(ids) == len(set(ids)), 'duplicate source ID'

    def references(value):
        if isinstance(value, dict):
            if 'source_id' in value:
                assert value['source_id'] in ids, ('source ID',value['source_id'])
            for key in ['path','source_file']:
                path = value.get(key)
                if isinstance(path,str) and path.startswith('sources/'):
                    assert path in catalog, ('uncatalogued source',path)
                    for digest_key in ['sha256','source_sha256']:
                        if value.get(digest_key):
                            assert value[digest_key] == catalog[path]['sha256'], ('declared source hash',path)
            for child in value.values(): references(child)
        elif isinstance(value,list):
            for child in value: references(child)
        elif isinstance(value,str) and value.startswith('sources/'):
            assert value in catalog, ('uncatalogued source',value)

    for f in (root / 'data').glob('*.json'):
        references(json.loads(f.read_text()))
    for f in (root / 'data').glob('*.csv'):
        with f.open(newline='') as stream:
            for row in csv.DictReader(stream): references(row)
    with (root / 'sources/cited_works.csv').open(newline='') as stream:
        for row in csv.DictReader(stream):
            for path in json.loads(row['local_evidence']):
                assert path in catalog or path == 'sources/catalog.csv', ('bibliography source',path)
    return catalog

def validate_inputs(root=ROOT):
    reference = load_reference(root)
    for path, digest in reference['inputs_sha256'].items():
        assert hashlib.sha256((root / path).read_bytes()).hexdigest() == digest, ('compiled input changed',path)
    # Fixed byte identities protect every field; these contracts also explain keys and required fields.
    contracts = {
        'analysis_inputs_v4.csv': (96, ['utility_id','gallons'],
            ['price_status','2019','2024','main_eligible','design_weight','arc_all','arc_mixed',
             'base_bill_2019','base_bill_2024','charge_inclusive_bill_or_scenario_2019',
             'charge_inclusive_bill_or_scenario_2024']),
        'Source_Verification_Register_v4.csv': (40, ['utility_id','year'],
            ['minimum','included_gallons','applicable_blocks_per_1000','applied_extra','extra_per_1000',
             'source_file','source_sha256','base_2000','total_2000','base_4000','total_4000','base_6000','total_6000']),
        'Endpoint_Account_Source_Check.csv': (40, ['utility_id','year'], ['residential_end','source_file','sha256']),
        'Benchmark_Comparability_Register.csv': (20, ['utility_id'], ['decision','qualification']),
        'Supplier_Register.csv': (40, ['utility_id','year'], ['vendor_literal','status','source_file']),
        'selection_frame_34.csv': (34, ['utility_id'], ['original_stratum','conservative_screen_pass']),
        'stage2_district_screen.csv': (97, ['utility_id'], ['2019','2024','conservative_screen_pass']),
        'residential_customer_panel_2019_2024.csv': (736, ['utility_id','year'], ['residential_start','residential_end']),
        'customer_continuity_flags.csv': (70, ['utility_id','year'], ['residential_start','residential_end']),
        'merger_screening.csv': (118, ['utility_id'], ['merger_history_reported']),
        'tariff_feasibility_sample.csv': (34, ['utility_id'], ['folder_url']),
        'event_classification_current.csv': (76, ['event_id'], ['district_id','record_type','base_bill_4000'])
    }
    for name, (count, keys, fields) in contracts.items():
        csv_rows(root / 'data' / name, keys + fields, keys, count)
    events = json.loads((root / 'data/events_current.json').read_text())
    assert len(events) == 76 and len({x['event_id'] for x in events}) == 76, 'event keys'
    for event in events:
        assert {'event_id','district_id','record_type','resolved_sources'}.issubset(event), 'event schema'
    extras = json.loads((root / 'data/surcharges.json').read_text())
    assert len(extras) == 6 and len({x['record_id'] for x in extras}) == 6, 'recurring-charge keys'
    for extra in extras:
        assert {'record_id','district_id','monthly_charge','classification'}.issubset(extra), 'recurring-charge schema'
    return source_catalog(root)
