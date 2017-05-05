from jinja2 import Environment, select_autoescape
import json
from credstash import listSecrets, DEFAULT_REGION

GLOBALS = {
    'ansible_managed': "This file is managed by Ansible",
}


class MockStash:
    """Credstash mock class"""
    def listSecrets(table='credential-store'):
        return {
            'app_key': 'fake_app_key',
            'db_password': 'fake_db_password',
            'secret': 'fake_secret'
        }


class Alohomora:
    """Alohomora unlocks secrets"""

    def __init__(self, env, app, mock=False):
        self.env = env
        if mock:
            self.stash = MockStash()
        else:
            self.stash = Credstash()

        self.secrets = self.stash.listSecrets(
            table=self.make_table_name())

    def make_table_name():
        return f"credstash-{self.env}-{self.app}"

    def lookup(self, method, key, **args):
        self.setup_secret_cache()
        secrets = self.stash.listSecrets()
        if method == 'credstash':
            # We have a table set in the lookup,
            # it must match the table we are using
            if 'table' in args:
                if args['table'] == self.make_table_name():
                    if key in self.secrets:
                        return self.secrets[key]
                    else:
                        return 'alohomora'
                    pass
                else:
                    # We really don't have a fallback here
                    return 'alohomora_untouched'
                    pass
        elif method == = 'alohomora':
            # TODO: Define a stricter alohomora lookup
            pass

    def render(self, file):
        variables = GLOBALS
        variables['env'] = self.env
        variables['lookup'] = self.lookup
        template = Environment().from_string(
            source=open(file).read(), globals=variables
        )
        return template.render()
