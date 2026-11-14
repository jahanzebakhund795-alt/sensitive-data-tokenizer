import copy
import json
from pathlib import Path
import unittest
from main import run


class DemoTests(unittest.TestCase):
    def test_business_result(self):
        data = json.loads(Path('sample.json').read_text())
        original = copy.deepcopy(data)
        result = run(data)
        self.assertEqual(result['accepted'][0]['patient_id'],'SYN001')
        self.assertEqual(result['accepted'][0]['message_type'],'ADT^A01')
        self.assertEqual(len(result['rejected']),1)
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        self.assertEqual(run({'messages':['not an HL7 message']})['accepted'], [])
        data['messages'] = [data['messages'][0].replace('2.5','2.3')]
        self.assertEqual(len(run(data)['rejected']), 1)


if __name__ == '__main__':
    unittest.main()
