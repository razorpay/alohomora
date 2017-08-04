from __future__ import absolute_import
from razorpay.alohomora import Alohomora
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import io
from io import open
import pytest


class TestAlohomora(object):
    """Alohomora cast and other tests"""

    def read_generated_config(self, file):
        ini_contents = open('test/files/' + file).read()
        string_config = '[default]\n' + ini_contents

        config = configparser.ConfigParser(allow_no_value=True)
        config.readfp(io.StringIO(string_config))

        return config

    def cast_and_read(self, spell):
        spell.cast(open('test/files/birdie.j2'))

        return self.read_generated_config('birdie')

    def test_multi_target_cast(self):
        spell = Alohomora('prod', 'birdie', mock=True)
        res = spell.cast(open('test/files/birdie.j2'),
                         open('test/files/birdie2.j2'))

        config1 = self.read_generated_config('birdie')
        config2 = self.read_generated_config('birdie2')

        assert 'fake_app_key' == config1.get('default', 'APP_KEY')
        assert 'fake_app_key' == config2.get('default', 'APP_KEY')

    def test_lookup(self):
        spell = Alohomora('prod', 'birdie', mock=True)
        config = self.cast_and_read(spell)
        assert 'prod-common.db.website.vpc' == config.get('default', 'DB_HOST')
        assert 'fake_app_key' == config.get('default', 'APP_KEY')
        assert 'fake_db_password' == config.get('default', 'DB_PASSWORD')
        assert 'fake_secret' == config.get('default', 'APP_SECRET')

    def test_lookup_failure(self):
        spell = Alohomora('prod', 'birdie', mock=True)
        with pytest.raises(Exception,
                           message='Lookup failed: app_key_non_existent'):
            spell.cast(open('test/files/birdie_fail.j2'))

    def test_canonical(self):
        spell = Alohomora('prod', 'birdie', mock=True)
        assert 'prod' == spell.canonical_env('Production')
        assert 'prod' == spell.canonical_env('Production-API')
        assert 'prod' == spell.canonical_env('prod-birdie')
        assert 'beta' == spell.canonical_env('beta-birdie')
        assert 'beta' == spell.canonical_env('beta')
