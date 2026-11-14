"""Sensitive Data Tokenizer. Synthetic portfolio demonstration."""
import hashlib
import hmac
import os

def run(data):
    secret = os.environ.get('TOKEN_KEY','local-demo-key-not-for-production').encode()
    if not secret:
        raise ValueError('TOKEN_KEY cannot be empty')
    output = []
    for row in data['records']:
        token = hmac.new(secret, str(row['patient_id']).encode(), hashlib.sha256).hexdigest()
        output.append({'patient_token':token,'diagnosis':row['diagnosis']})
    return {'records':output,'mode':'pseudonymization; not anonymization'}



if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path(__file__).with_name('sample.json'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run(json.loads(args.input.read_text()))
    serialized = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)
    if args.output:
        args.output.write_text(serialized + '\n')
    else:
        print(serialized)
