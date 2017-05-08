from jinja2 import Environment, select_autoescape
import json
import credstash
import click
import botocore.exceptions

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

    def __init__(self, env, app, region=credstash.DEFAULT_REGION, mock=False):
        self.env = env
        self.app = app
        if mock:
            self.stash = MockStash()
        else:
            self.stash = CredStash()
        self.region = region
        self.secrets = None

    def cache_secrets(self):
        if self.secrets == None:
            self.secrets = self.stash.listSecrets(
                self.make_table_name())

    def make_table_name(self):
        return "credstash-{self.env}-{self.app}".format(**locals())

    def create_table(self):
        credstash.createDdbTable(
            table=self.make_table_name(), region=self.region)

    def store(self, key, secret):
        msg = ''
        try:
            credstash.putSecret(table=self.make_table_name(),
                                region=self.region,
                                name=key,
                                secret=secret,
                                )
            msg = "secret saved"
        except Exception as e:
            if (e.response["Error"]["Code"]
                    == "ConditionalCheckFailedException"):
                msg = ("store command failed\n"
                       "Please try the command: credstash -r {0}"
                       " -t {1} put -a {2} [secret]"
                       ).format(self.region, self.make_table_name(), key)
        finally:
            return msg

    def lookup(self, key):
        self.cache_secrets()
        if key in self.secrets:
            return self.secrets[key]
        else:
            raise Exception('Lookup failed')

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
