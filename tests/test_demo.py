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
        self.assertEqual(result['records'][0]['patient_token'],result['records'][1]['patient_token'])
        self.assertNotIn('email',result['records'][0])
        self.assertNotIn('patient_id',result['records'][0])
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        import os
        from unittest.mock import patch
        with patch.dict(os.environ, {'TOKEN_KEY':'test-one'}):
            first = run(data)['records'][0]['patient_token']
        with patch.dict(os.environ, {'TOKEN_KEY':'test-two'}):
            second = run(data)['records'][0]['patient_token']
        self.assertNotEqual(first, second)
        self.assertEqual(set(run(data)['records'][0]), {'patient_token','diagnosis'})


if __name__ == '__main__':
    unittest.main()
