from __future__ import absolute_import
from razorpay.alohomora import Alohomora
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import io
from io import open
import pytest
import contextlib
import os
import unittest


class TestAlohomora(unittest.TestCase):

    '''
        Picked up from
        https://stackoverflow.com/a/34333710/368328
    '''
    @contextlib.contextmanager
    def modified_environ(self, *remove, **update):
        """
        Temporarily updates the ``os.environ`` dictionary in-place.

        The ``os.environ`` dictionary is updated in-place so that the modification
        is sure to work in all situations.

        :param remove: Environment variables to remove.
        :param update: Dictionary of environment variables and values to add/update.
        """
        env = os.environ
        update = update or {}
        remove = remove or []

        # List of environment variables being updated or removed.
        stomped = (set(update.keys()) | set(remove)) & set(env.keys())
        # Environment variables and values to restore on exit.
        update_after = {k: env[k] for k in stomped}
        # Environment variables and values to remove on exit.
        remove_after = frozenset(k for k in update if k not in env)

        try:
            env.update(update)
            [env.pop(k, None) for k in remove]
            yield
        finally:
            env.update(update_after)
            [env.pop(k) for k in remove_after]
    """Alohomora cast and other tests"""

    def tearDown(self):
        files = [
            'tests/files/birdie',
            'tests/files/birdie_env',
            'tests/files/birdie2',
            'tests/files/env.birdie.vault',
        ]

        for test_file in files:
            if os.path.isfile(test_file):
                os.remove(test_file)

    def read_generated_config(self, file, filename=None):
        if filename:
            vault_file = filename
            f = open(vault_file)
        else:
            vault_file = file
            f = open('tests/files/' + vault_file)
        string_config = '[default]\n' + f.read()
        f.close()

        config = configparser.ConfigParser(allow_no_value=True)
        config.read_file(io.StringIO(string_config))

        return config

    def cast_and_read(self, spell, filename=None):
        fd = open('tests/files/birdie.j2')
        spell.cast(fd, filename=filename)
        fd.close()

        return self.read_generated_config('birdie', filename=filename)

    def test_multi_target_cast(self):
        spell = Alohomora('prod', 'birdie', mock=True)
        with open('tests/files/birdie.j2') as f1, open('tests/files/birdie2.j2') as f2:
            res = spell.cast(f1,f2)

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

    def test_output_file_name(self):
        spell = Alohomora('prod', 'birdie', mock=True)
        vault_file = 'tests/files/env.birdie.vault'
        config = self.cast_and_read(spell, filename=vault_file)
        assert os.path.isfile('tests/files/env.birdie.vault')
        assert 'fake_secret' == config.get('default', 'APP_SECRET')

    def test_lookup_failure(self):
        spell = Alohomora('prod', 'birdie', mock=True)
        msg = r'Lookup failed: alohomora_app_key_non_existent'
        with pytest.raises(Exception,
                           match=msg):
            with open('tests/files/birdie_fail.j2') as f:
                spell.cast(f)

    def test_canonical(self):
        spell = Alohomora('prod', 'birdie', mock=True)
        assert 'prod' == spell.canonical_env('Production')
        assert 'prod' == spell.canonical_env('Production-API')
        assert 'prod' == spell.canonical_env('prod-birdie')
        assert 'beta' == spell.canonical_env('beta-birdie')
        assert 'beta' == spell.canonical_env('beta')

    def test_multi_lookup_failure(self):
        spell = Alohomora('prod', 'birdie', mock=True)
        msg = r'Lookup failed: alohomora_app_key_non_existent, alohomora_app_fake_key'
        with pytest.raises(Exception,
                           match=msg) as excinfo:
            with open('tests/files/birdie_fail_multiple.j2') as f:
                spell.cast(f)
        assert excinfo.value.args[0] == msg

    def test_environment(self):
        with self.modified_environ(README='VALUE'):
            spell = Alohomora('prod', 'birdie', mock=True)
            with open('tests/files/birdie_env.j2') as f:
                spell.cast(f)

            conf = self.read_generated_config('birdie_env')
            assert 'VALUE' == conf.get('default', 'ENV_TEST')
