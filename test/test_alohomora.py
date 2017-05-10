from __future__ import absolute_import
from razorpay.alohomora import Alohomora
import ConfigParser
import StringIO
from io import open


class TestAlohomora(object):
    """Alohomora cast and other tests"""

    def cast_and_read(self, spell):
        spell.cast(file('test/files/birdie.j2'))

        ini_contents = open('test/files/birdie').read()
        string_config = '[default]\n' + ini_contents

        config = ConfigParser.ConfigParser(allow_no_value=True)
        config.readfp(StringIO.StringIO(string_config))

        return config

    def test_lookup(self):
        spell = Alohomora('prod', 'birdie', mock=True)
        config = self.cast_and_read(spell)
        assert 'prod-common.db.website.vpc' == config.get('default', 'DB_HOST')
        assert 'fake_app_key' == config.get('default', 'APP_KEY')
        assert 'fake_db_password' == config.get('default', 'DB_PASSWORD')
        assert 'fake_secret' == config.get('default', 'APP_SECRET')

    def test_canonical(self):
        spell = Alohomora('prod', 'birdie', mock=True)
        assert 'prod' == spell.canonical_env('Production')
        assert 'prod' == spell.canonical_env('Production-API')
        assert 'prod' == spell.canonical_env('prod-birdie')
        assert 'beta' == spell.canonical_env('beta-birdie')
        assert 'beta' == spell.canonical_env('beta')
