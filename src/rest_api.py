from src.helpers import LogProvider

from requests import Session


class RestApiClient:

    def __init__(self, headers: dict = None):
        self.logger = LogProvider()
        self.sesion = Session()
        self.sesion.headers.update(headers or {})


class NbpClient(RestApiClient):

    SUPPORTED_CURRENCIES = ["usd", "eur"]

    USD_URL = "https://api.nbp.pl/api/exchangerates/rates/a/usd/?format=json"
    EUR_URL = "https://api.nbp.pl/api/exchangerates/rates/a/eur/?format=json"

    def get_mid_currency_rate(self, currency: str, /) -> float:
        """
        response_content example:
        {'table': 'A', 'currency': 'dolar amerykański', 'code': 'USD', 'rates': [{'no': '121/A/NBP/2022', 'effectiveDate': '2022-06-24', 'mid': 4.4656}]}
        """
        url_ = self.currency_exchange_url(currency)
        reponse_content = self.sesion.get(url_).json()
        return float(reponse_content.get("rates")[0].get("mid"))

    @classmethod
    def currency_exchange_url(cls, currency: str) -> str:
        if not isinstance(currency, str) or len(currency) != 3:
            raise TypeError("Currency should be str of length three.")
        if currency not in cls.SUPPORTED_CURRENCIES:
            raise ValueError(f"Currently {currency} is not supported.")
        return f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/?format=json"
