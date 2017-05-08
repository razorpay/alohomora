from alohomora import Alohomora
from configparser import ConfigParser


class TestAlohomora:
    """Alohomora cast and other tests"""

    def cast_and_read(self, spell):
        spell.cast('test/files/birdie.j2')

        ini_contents = open('test/files/birdie').read()
        string_config = '[default]\n' + ini_contents

        config = ConfigParser(allow_no_value=True)
        config.read_string(string_config)

        return config

    def test_lookup(self):
        spell = Alohomora('prod', 'birdie', mock=True)
        config = self.cast_and_read(spell)
        assert 'prod-common.db.website.vpc' == config.get('default', 'DB_HOST')
        assert 'fake_app_key' == config.get('default', 'APP_KEY')
        assert 'fake_db_password' == config.get('default', 'DB_PASSWORD')
        assert 'fake_secret' == config.get('default', 'APP_SECRET')

    def test_actual_lookup(self):
        spell = Alohomora('prod', 'birdie')
        config = self.cast_and_read(spell)

        assert 'prod-common.db.website.vpc' == config.get('default', 'DB_HOST')
        assert 'fake_app_key' == config.get('default', 'APP_KEY')
        assert 'fake_db_password' == config.get('default', 'DB_PASSWORD')
        assert 'fake_secret' == config.get('default', 'APP_SECRET')
