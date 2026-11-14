"""Healthcare Claims Analytics. Synthetic portfolio demonstration."""
def run(data):
    seen,providers = {},{}
    for claim in data['claims']:
        if claim['status'] not in ('paid','denied') or type(claim['paid_cents']) is not int or claim['paid_cents'] < 0:
            raise ValueError('Invalid claim status or payment')
        if claim['status']=='denied' and claim['paid_cents'] != 0:
            raise ValueError('Denied claim must have zero payment')
        if claim['id'] in seen:
            if seen[claim['id']] != claim:
                raise ValueError('Conflicting duplicate claim')
            continue
        seen[claim['id']] = claim
        summary = providers.setdefault(claim['provider'],{'claims':0,'denied':0,'paid_cents':0})
        summary['claims'] += 1
        summary['denied'] += claim['status']=='denied'
        summary['paid_cents'] += claim['paid_cents']
    for summary in providers.values():
        summary['denial_rate'] = summary['denied']/summary['claims']
    return {'providers':providers,'unique_claims':len(seen)}



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
