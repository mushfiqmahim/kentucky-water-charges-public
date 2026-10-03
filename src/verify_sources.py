"""Verify every expected original. Missing originals never count as verified."""
from pathlib import Path
import hashlib
import json
from check_inputs import source_catalog

def main():
    root = Path(__file__).resolve().parents[1]
    output = root / 'results/source_verification.json'
    output.parent.mkdir(exist_ok=True)
    try:
        catalog = source_catalog(root)
    except (AssertionError, ValueError, KeyError, FileNotFoundError) as error:
        result = {'status':'failed','scope':'original source-file verification',
                  'reference_validation':'failed','error':str(error)}
        output.write_text(json.dumps(result,indent=2))
        print(json.dumps(result,indent=2))
        return 1
    checks = []
    for path, expected in sorted(catalog.items()):
        file = root / path
        item = {'path':path,'expected_sha256':expected['sha256'],
                'expected_git_blob':expected['git_blob'],'expected_bytes':int(expected['bytes'])}
        if not file.is_file():
            item['status'] = 'missing'
        else:
            content = file.read_bytes()
            item.update(observed_sha256=hashlib.sha256(content).hexdigest(),
                        observed_git_blob=hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest(),
                        observed_bytes=len(content))
            item['status'] = 'verified' if all(item['observed_'+key] == item['expected_'+key]
                for key in ['sha256','git_blob','bytes']) else 'incorrect_identity'
        checks.append(item)
    missing = [x['path'] for x in checks if x['status']=='missing']
    incorrect = [x['path'] for x in checks if x['status']=='incorrect_identity']
    result = {'status':'failed' if incorrect else 'incomplete' if missing else 'passed',
              'scope':'original source-file verification; not independent validation of interpretations',
              'expected_documents':213,'verified_documents':sum(x['status']=='verified' for x in checks),
              'missing_documents':missing,'incorrect_identity_documents':incorrect,
              'source_references':'catalogue and compiled reference identities checked','documents':checks}
    output.write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='documents'},indent=2))
    return 1 if incorrect else 2 if missing else 0

if __name__ == '__main__':
    raise SystemExit(main())
