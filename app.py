import click

from src.reports import generate_product_report
from src.rest_api import NbpClient
from src.db import DbWrapper
from src.helpers import get_credentials, build_update_currency_transaction, transaction_reader, get_file_content


class Config:
    """Configuration class will be used across click module context for handling configuration details"""
    def __init__(self):
        self.version = "0.1"


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@pass_config
def cli(config):
    """Hello in the app!"""
    pass


@cli.command()
@pass_config
def db_setup(config) -> None:
    """Command runs full db setup.

    \b
    For previously installed MySQL DB:
      - delete mydb database if already exists
      - imports DB schema (src/static/dbschema.sql) and creates mydb database
      - imports test data  (src/static/population.sql)
      - adds 2 new columns: UnitPriceUSD, UnitPriceEuro (Product table)"""
    creds: dict = get_credentials()
    with DbWrapper(**creds) as db:
        click.secho(message=" ... Initializing fresh mydb instance.", fg="blue", bold=False)
        db.initiate_db()
    click.secho(message=" ... Inserting all test data.", fg="blue", bold=False)
    for transaction in transaction_reader():
        with DbWrapper(**get_credentials()) as db:
            db.execute_query(transaction)
    with DbWrapper(**creds) as db:
        click.secho(message=" ... Adding 2 new columns to Product table (UnitPriceUSD, UnitPriceEuro).", fg="blue", bold=False)
        db.execute_query(get_file_content("src/static/extend_product_table.sql"))


@cli.command()
@pass_config
def generate_report(config):
    """Command generates Excel report with all products in database.

    \b
    Report will contain the following columns:
      a. ProductID,
      b. DepartmentID,
      c. Category,
      d. IDSKU,
      e. ProductName,
      f. Quantity,
      g. UnitPrice,
      h. UnitPriceUSD,
      i. UnitPriceEuro,
      j. Ranking
      k. ProductDesc
      l. UnitsInStock
      m. UnitsInOrder"""
    click.secho(message=" ... Generating Product report.", fg="blue")
    with DbWrapper(**get_credentials()) as db:
        report_name = generate_product_report()(db)
    click.secho(message=f" ... Product report {report_name!r} was generated.", fg="blue")


@cli.command()
@pass_config
def update_currency_rates(config) -> None:
    """Command updates current currency rates for USD and Euro."""
    nbp_client = NbpClient()
    click.secho(message=" ... Downloading current currency rate for USD.", fg="blue", bold=False)
    usd_rate = nbp_client.get_mid_currency_rate("usd")
    click.secho(message=" ... Downloading current currency rate for Euro.", fg="blue", bold=False)
    euro_rate = nbp_client.get_mid_currency_rate("eur")
    with DbWrapper(**get_credentials()) as db:
        click.secho(message=" ... Updating mydb.Product.UnitPriceUSD column with current USD rate.", fg="blue", bold=False)
        db.execute_query(build_update_currency_transaction(currency="USD", value=usd_rate))
    with DbWrapper(**get_credentials()) as db:
        click.secho(message=" ... Updating mydb.Product.UnitPriceEuro column with current Euro rate.", fg="blue", bold=False)
        db.execute_query(build_update_currency_transaction(currency="Euro", value=euro_rate))


if __name__ == "__main__":
    cli()
