from alohomora import Alohomora
from configparser import ConfigParser


class TestAlohomora:

    def test_lookup(self):
        spell = Alohomora('prod', 'birdie', mock=True)
        string_config = '[default]\n' + spell.cast('test/files/birdie.j2')

        config = ConfigParser(allow_no_value=True)
        config.read_string(string_config)

        assert 'prod-common.db.website.vpc' == config.get('default', 'DB_HOST')
        assert 'fake_app_key' == config.get('default', 'APP_KEY')
        assert 'fake_db_password' == config.get('default', 'DB_PASSWORD')
        assert 'fake_secret' == config.get('default', 'APP_SECRET')

    def test_actual_lookup(self):
        spell = Alohomora('prod', 'birdie')
        string_config = '[default]\n' + spell.cast('test/files/birdie.j2')

        config = ConfigParser(allow_no_value=True)
        config.read_string(string_config)

        assert 'prod-common.db.website.vpc' == config.get('default', 'DB_HOST')
        assert 'fake_app_key' == config.get('default', 'APP_KEY')
        assert 'fake_db_password' == config.get('default', 'DB_PASSWORD')
        assert 'fake_secret' == config.get('default', 'APP_SECRET')
