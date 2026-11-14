"""HL7 Message Normalizer. Synthetic portfolio demonstration."""
def normalize(message):
    segments = {}
    for line in message.replace('\r','\n').splitlines():
        fields = line.split('|')
        if fields[0] in ('MSH','PID','PV1'):
            if fields[0] in segments:
                raise ValueError('Repeated supported segment')
            segments[fields[0]] = fields
    msh,pid,pv1 = segments['MSH'],segments['PID'],segments['PV1']
    if msh[11] != '2.5' or not pid[3]:
        raise ValueError('Requires HL7 2.5 and PID-3')
    return {'message_id':msh[9],'message_type':msh[8],
            'patient_id':pid[3].split('^')[0],'patient_class':pv1[2],'location':pv1[3]}

def run(data):
    accepted,rejected = [],[]
    for index,message in enumerate(data['messages']):
        try:
            accepted.append(normalize(message))
        except (KeyError,IndexError,ValueError) as error:
            rejected.append({'index':index,'reason':str(error)})
    return {'accepted':accepted,'rejected':rejected}



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
