from __future__ import with_statement
from __future__ import absolute_import
from jinja2 import Environment, select_autoescape
import json
import credstash
import click
import botocore.exceptions
import os.path
import re
from io import open

GLOBALS = {
    'alohomora_managed': "This file is managed by Alohomora",
}


class MockStash(object):
    """Credstash mock class"""

    def listSecrets(self, table='credential-store',
                    region=credstash.DEFAULT_REGION):
        return {
            'app_key': 'fake_app_key',
            'db_password': 'fake_db_password',
            'secret': 'fake_secret'
        }


class CredStash(object):
    """Actual Credstash class wrapper"""

    def listSecrets(self, table='credential-store',
                    region=credstash.DEFAULT_REGION):
        return credstash.getAllSecrets(
            table=table,
            region=region
        )


class Alohomora(object):
    """Alohomora unlocks secrets"""

    def __init__(self, env, app, region=credstash.DEFAULT_REGION, mock=False):
        self.env = self.canonical_env(env)
        self.app = self.canonical_app(app)
        if mock:
            self.stash = MockStash()
        else:
            self.stash = CredStash()
        self.region = region
        self.secrets = None

    def canonical_env(self, env):
        pattern = re.compile('^(\w+).*$')
        env = pattern.findall(env)[0]
        if env == 'Production':
            env = 'prod'
        return env.lower()

    def canonical_app(self, app):
        return app.lower()

    def cache_secrets(self):
        if self.secrets == None:
            self.secrets = self.stash.listSecrets(
                self.make_table_name(),
                region=self.region)

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
        vault_file = self.make_vault_file_name(file.name)
        variables = GLOBALS
        variables['env'] = self.env
        variables['lookup'] = self.lookup
        # This is the template variable
        contents = Environment().from_string(
            source=file.read(), globals=variables
        ).render()

        if os.path.isfile(vault_file):
            """TODO: The file exists, we will output diff"""
            msg = vault_file + " updated"
            pass
        else:
            msg = vault_file + " created"

        with open(vault_file, 'w') as f:
            f.write(contents)

        return(msg)

    def make_vault_file_name(self, file):
        if file[-3:] != '.j2':
            raise Exception('File must be a valid j2 template')

        return file[0:-3]

    def render(self, file):
        return self.cast(file)
