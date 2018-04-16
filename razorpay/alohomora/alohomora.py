from __future__ import with_statement
from __future__ import absolute_import
from jinja2 import Environment, select_autoescape
import json
import credstash
import click
import botocore.exceptions
import os
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
        self.failed_lookups = []
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
            self.failed_lookups.append(key)

    def __cast_one_file(self, file, context, filename=None):
        self.validate_j2(file.name)

        if filename:
            vault_file = filename
        else:
            vault_file = file.name[0:-3]

        contents = str(file.read())

        # re-initialize the failed_lookups
        self.failed_lookups = []
        # This is the template variable
        contents = Environment().from_string(
            source=contents, globals=context
        ).render()

        if self.failed_lookups:
            msg = "Lookup failed: {}".format(", ".join(self.failed_lookups))
            raise Exception(msg)

        if os.path.isfile(vault_file):
            """TODO: The file exists, we will output diff"""
            msg = vault_file + " updated"
        else:
            msg = vault_file + " created"

        with open(vault_file, 'w') as f:
            f.write(contents)

        return msg

    def cast(self, *files, **kwargs):
        filename = kwargs.get('filename')
        if len(files) > 2 and filename:
            raise Exception('Output name given for multiple files')

        variables = GLOBALS
        variables['env'] = self.env
        variables['ENV'] = os.environ
        variables['lookup'] = self.lookup

        msgs = []

        # If a single j2 file is given and an output name,
        # Cast the j2 file with that output file name
        if len(files) == 1 and filename:
            file = files[0]
            msgs.append(self.__cast_one_file(file, variables, filename=filename))
        else:
            for file in files:
                msgs.append(self.__cast_one_file(file, variables))

        return msgs

    def validate_j2(self, file):
        if file[-3:] != '.j2':
            raise Exception('File must be a valid j2 template')

    def render(self, *files):
        return self.cast(*files)
