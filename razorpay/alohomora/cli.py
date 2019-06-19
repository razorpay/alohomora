#!/usr/bin/env python

from __future__ import absolute_import
from credstash import createDdbTable, putSecretAction
from razorpay.alohomora import Alohomora
import click


@click.group()
def cli():
    """Alohomora is a secret distribution tool"""


@click.option('--region', default='us-east-1', help='AWS region')
@click.option('--env', default='prod',
              help='environment for the application, used for namespacing')
@click.argument('app')
@cli.command('create',
             short_help='Create a credstash database for an application')
def create(region, env, app):
    spell = Alohomora(env, app, region)
    spell.create_table()


@click.option('--region', default='us-east-1', help='AWS region')
@click.option('--env', default='prod',
              help='environment for the application, used for namespacing')
@click.argument('secret')
@click.argument('key')
@click.argument('app')
@cli.command('store', short_help='Store a secret for an application')
def store(region, env, secret, key, app):
    spell = Alohomora(env, app, region)
    click.echo(spell.store(key, secret))


@click.option('--region', default='eu-west-1', help='AWS region')
@click.option('--app', help='application name, used for table name as well')
@click.option('--env', default='prod',
              help='environment for the application, used for namespacing')
@click.option('--output', default=None,
              help='Output file name of the vault file')
@click.option('--mock', default=False,
              help='To mock all calls to credstash.')
@click.argument('files', type=click.File('rb'), nargs=-1)
@cli.command('cast', short_help='Render a ansible jinja template file')
def cast(app, env, region, output, files, mock):
    is_mock = False

    if isinstance(mock, bool):
        is_mock = mock
    elif isinstance(mock, basestring) and mock.lower() == "true":
        is_mock = True

    spell = Alohomora(env, app, region, mock=is_mock)
    for msg in spell.cast(*files, filename=output):
        click.echo(msg)


if __name__ == '__main__':
    cli()
