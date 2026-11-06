import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock,patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts import hf_login_safe

class SafeLoginTests(unittest.TestCase):
    def test_name_instead_of_token_is_rejected_without_network(self):
        with patch.object(hf_login_safe.getpass,'getpass',return_value='primer-demo'),patch.object(hf_login_safe.requests,'get') as request:
            with self.assertRaises(SystemExit) as result:hf_login_safe.main()
            self.assertNotIn('primer-demo',str(result.exception))
            request.assert_not_called()

    def test_failed_auth_is_not_saved_or_echoed(self):
        secret='hf_FAKE_UNIT_TEST_NOT_A_REAL_TOKEN'
        with patch.object(hf_login_safe.getpass,'getpass',return_value=secret),patch.object(hf_login_safe.requests,'get',return_value=Mock(status_code=400)),patch.object(hf_login_safe.HfFolder,'save_token') as save:
            with self.assertRaises(SystemExit) as result:hf_login_safe.main()
            self.assertIn('HTTP 400',str(result.exception))
            self.assertNotIn(secret,str(result.exception))
            save.assert_not_called()

    def test_valid_auth_saved_without_printing_token(self):
        secret='hf_FAKE_UNIT_TEST_NOT_A_REAL_TOKEN'
        response=Mock(status_code=200)
        response.json.return_value={'name':'test-account','auth':{'accessToken':{'role':'write'}}}
        output=io.StringIO()
        with patch.object(hf_login_safe.getpass,'getpass',return_value=secret),patch.object(hf_login_safe.requests,'get',return_value=response),patch.object(hf_login_safe.HfFolder,'save_token') as save,contextlib.redirect_stdout(output):
            hf_login_safe.main()
            save.assert_called_once_with(secret)
        self.assertNotIn(secret,output.getvalue())
        self.assertIn('test-account',output.getvalue())

if __name__=='__main__':unittest.main()
