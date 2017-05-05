from jinja2 import Environment, select_autoescape
import json
import credstash

GLOBALS = {
    'alohomora_managed': "This file is managed by Alohomora",
}


class MockStash:
    """Credstash mock class"""

    def listSecrets(self, table='credential-store'):
        return {
            'app_key': 'fake_app_key',
            'db_password': 'fake_db_password',
            'secret': 'fake_secret'
        }


class CredStash:
    """Actual Credstash class wrapper"""

    def listSecrets(self, table='credential-store'):
        return credstash.getAllSecrets(
            table=table
        )


class Alohomora:
    """Alohomora unlocks secrets"""

    def __init__(self, env, app, mock=False):
        self.env = env
        self.app = app
        if mock:
            self.stash = MockStash()
        else:
            self.stash = CredStash()

        self.secrets = self.stash.listSecrets(
            self.make_table_name())

    def make_table_name(self):
        return f"credstash-{self.env}-{self.app}"

    def lookup(self, key):
        if key in self.secrets:
            return self.secrets[key]
        else:
            return 'NO_SECRET'

    def cast(self, file):
        variables = GLOBALS
        variables['env'] = self.env
        variables['lookup'] = self.lookup
        # This is the template variable
        return Environment().from_string(
            source=open(file).read(), globals=variables
        ).render()

    def render(self, file):
        return self.cast(file)
