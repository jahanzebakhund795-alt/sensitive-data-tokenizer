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
        self.assertEqual(result['unique_claims'],3)
        self.assertEqual(result['providers']['p1']['denial_rate'],0.5)
        self.assertEqual(result['providers']['p1']['paid_cents'],12000)
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        data['claims'].append({'id':'x1','provider':'p1','status':'paid','paid_cents':1})
        with self.assertRaises(ValueError):
            run(data)
        with self.assertRaises(ValueError):
            run({'claims':[{'id':'x','provider':'p','status':'denied','paid_cents':100}]})


if __name__ == '__main__':
    unittest.main()
