import click

from src.rest_api import NbpClient
from src.db import DbWrapper
from src.helpers import get_credentials, build_update_currency_transaction


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
def update_currency_rates(config) -> None:
    """Command updates current currency rates for USD and Euro."""
    nbp_client = NbpClient()
    click.secho(message=" ... Downloading current currency rate for USD.", fg="blue", bold=True)
    usd_rate = nbp_client.get_mid_currency_rate("usd")
    click.secho(message=" ... Downloading current currency rate for Euro.", fg="blue", bold=True)
    euro_rate = nbp_client.get_mid_currency_rate("eur")
    with DbWrapper(**get_credentials()) as db:
        click.secho(message=" ... Updating mydb.Product.UnitPriceUSD column with current USD rate.", fg="blue", bold=True)
        db.execute_query(build_update_currency_transaction(currency="USD", value=usd_rate))
    with DbWrapper(**get_credentials()) as db:
        click.secho(message=" ... Updating mydb.Product.UnitPriceEuro column with current Euro rate.", fg="blue", bold=True)
        db.execute_query(build_update_currency_transaction(currency="Euro", value=euro_rate))


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
      j. Ranking"""
    click.secho(message="Hi, from generate_report command context!", fg="blue", bold=True)


if __name__ == "__main__":
    cli()
