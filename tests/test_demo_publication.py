import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.publish_demo import check_demo
from scripts.publish_model import check as check_real_release

class DemoPublicationTests(unittest.TestCase):
    def test_demo_preflight_preserves_config_and_publishable_false(self):
        before=(ROOT/'model/config.json').read_bytes()
        c=check_demo()
        self.assertEqual(c['version'],'0.1.0-demo')
        self.assertEqual(c['data_source'],'sentetik')
        self.assertIs(c['publishable'],False)
        self.assertEqual((ROOT/'model/config.json').read_bytes(),before)

    def test_real_publication_gate_still_rejects_demo(self):
        with self.assertRaisesRegex(ValueError,'Nihai yayın reddedildi'):
            check_real_release()

    def test_demo_command_cannot_publish_real_source(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            folder=Path(tmp)
            (folder/'model').mkdir()
            shutil.copy2(ROOT/'model/config.schema.json',folder/'model/config.schema.json')
            c=json.loads((ROOT/'model/config.json').read_text(encoding='utf-8'))
            c.update(version='2.0.0',data_source='gerçek')
            (folder/'model/config.json').write_text(json.dumps(c),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'yalnız publishable=false, sentetik'):
                check_demo(folder)

if __name__=='__main__':unittest.main()
