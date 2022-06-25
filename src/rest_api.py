from requests import (Session, RequestException)

from src.helpers import LogProvider


class RestApiClient:

    def __init__(self, headers: dict = None):
        self._logger = LogProvider()
        self._sesion = Session()
        self._sesion.headers.update(headers or {})


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
        self._logger.debug(f"Connecting with NbpAPI ({url_}) to get currency rate for {currency}")
        try:
            reponse_content = self._sesion.get(url_).json()
            self._logger.debug(f"Response body:  {reponse_content}")
        except RequestException as err:
            self._logger.exception(f"Connecting with NbpAPI ({url_}) was not possible due to: {err}")
            raise RequestException from err
        return float(reponse_content.get("rates")[0].get("mid"))

    @classmethod
    def currency_exchange_url(cls, currency: str) -> str:
        if not isinstance(currency, str) or len(currency) != 3:
            raise TypeError("Currency should be str of length three.")
        if currency not in cls.SUPPORTED_CURRENCIES:
            raise ValueError(f"Currently {currency} is not supported.")
        return f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/?format=json"
