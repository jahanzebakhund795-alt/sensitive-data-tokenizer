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
        self.assertEqual(len(result['ready']),1)
        self.assertEqual(result['exceptions'][0]['missing'],['risk','payment'])
        self.assertEqual(result['orphan_member_months'],[['S3','2025-01']])
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        data['enrollment'].append(copy.deepcopy(data['enrollment'][0]))
        with self.assertRaises(ValueError):
            run(data)
        self.assertEqual(run({'enrollment':[],'risk':[],'payments':[]})['ready'], [])


if __name__ == '__main__':
    unittest.main()
