import pytest

from src.helpers import get_credentials, transaction_reader


class TestGetCredentials:

    def test_get_credentials_env_setuped(self, mock_env_creds):
        creds = get_credentials()
        assert isinstance(creds, dict)
        assert creds == mock_env_creds

    def test_get_credentials_env_not_setuped(self, mock_env_creds_not_setuped):
        with pytest.raises(OSError):
            get_credentials()


class TestTransactionReader:

    def test_transaction_reader(self):
        exp_transaction = "START TRANSACTION;\nUSE `mydb`;\n" \
                      "INSERT INTO `mydb`.`Payment_Giftcard` " \
                      "(`GiftcardID`, `PaymentID`, `GiftCardNumber`, `GiftcardExpMM`, `GiftcardExpYYYY`) " \
                      "VALUES ('G764', 'P7836', '4556 8598 9698', '12', '2020');" \
                      "\n\nCOMMIT;"
        transaction_reader_gen = transaction_reader(transactions_path="tests/static/population_fixture.sql")
        for transaction in transaction_reader_gen:
            assert transaction == exp_transaction
