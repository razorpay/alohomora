from credstash import createDdbTable, putSecretAction
import click

@click.group()
def cli():
    """A simple command line tool."""

@click.option('--region', default='us-east-1', help='AWS region')
@click.option('--env', default='prod', help='environment for the application, used for namespacing')
@click.option('--default-table', default='credential-store', help='Default table to use')
@click.argument('app')
@cli.command('create', short_help='Create a credstash database for an application')
def create(region, env, default_table, app):
    table_name = f"credstash-{env}-{app}"
    createDdbTable(region=region, table=table_name)

@click.option('--region', default='us-east-1', help='AWS region')
@click.option('--env', default='prod', help='environment for the application, used for namespacing')
@click.argument('key')
@click.argument('app')
@cli.command('store', short_help='Store a secret for an application')
def store(region, env, app, key):
    table_name = f"credstash-{env}-{app}"
    click.echo("Please run the following command")
    # This is a hack because credstash does not allow us to easily autoversion
    # TODO: Use putSecret and echo the CLI version if that fails
    click.echo(f"credstash -r {region} -t {table_name} put -a {key} [secret]")

@click.option('--region', default='eu-west-1', help='AWS region')
@click.option('--app', help='application name, used for table name as well')
@click.option('--env', default='prod', help='environment for the application, used for namespacing')
@click.option('--default-table', default='credential-store', help='Default table to use')
@click.argument('file', type=click.File('rb'))
@cli.command('render', short_help='Render a ansible jinja template file')
def render():
    pass

if __name__ == '__main__':
    cli()