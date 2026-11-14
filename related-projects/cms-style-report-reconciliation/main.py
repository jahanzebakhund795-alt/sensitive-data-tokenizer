"""CMS Style Report Reconciliation. Synthetic portfolio demonstration."""
def index(rows):
    result = {}
    for row in rows:
        key = (row['member'],row['month'])
        if key in result:
            raise ValueError('Duplicate member-month')
        result[key] = row
    return result

def run(data):
    enrollment,risk,payments = (index(data[k]) for k in ('enrollment','risk','payments'))
    exceptions,ready = [],[]
    for key in sorted(enrollment):
        missing = [name for name,table in [('risk',risk),('payment',payments)] if key not in table]
        if missing:
            exceptions.append({'member':key[0],'month':key[1],'missing':missing})
        else:
            ready.append({'member':key[0],'month':key[1],'score':risk[key]['score'],
                          'payment_cents':payments[key]['cents']})
    orphans = [list(k) for k in sorted((set(payments)|set(risk))-set(enrollment))]
    return {'ready':ready,'exceptions':exceptions,'orphan_member_months':orphans}



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
