"""
tests for src.helpers module
"""
import os
from logging import RootLogger
from pathlib import Path

import pytest

from src.helpers import get_credentials, transaction_reader, get_file_content, get_timestamp, LogProvider


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


class TestGetFileContent:
    EXPECTED_TEXT = "Exampled file\nUnit test artefact\n"

    def test_get_file_content_path_obj_input(self):
        text = get_file_content(file_path=Path("tests/static/example.txt"))
        assert text == self.EXPECTED_TEXT

    def test_get_file_content_str_obj_input(self):
        text = get_file_content(file_path="tests/static/example.txt")
        assert text == self.EXPECTED_TEXT

    def test_get_file_content_file_doesnt_exist(self):
        with pytest.raises(FileNotFoundError):
            get_file_content(file_path="tests/static/file_doesnt_exist.txt")


class TestBuildTransaction:
    """ tests for src.helpers.build_transaction"""
    pass


class TestBuildUpdateCurrencyTransaction:
    """ tests for src.helpers.build_update_currency_transaction"""
    pass


class TestGetTimestamp:
    """ tests for src.helpers.get_timestamp"""

    def test_get_timestamp(self):
        timestamp_ = get_timestamp()
        assert isinstance(timestamp_, str)
        assert len(timestamp_) == 15

    @pytest.mark.questionable
    def test_get_timestamp_detailed(self):
        pass


@pytest.mark.questionable
class TestLogProvider:
    """ tests for src.helpers.LogProvider"""

    def test_log_provider(self):
        logger = LogProvider()
        assert isinstance(logger, RootLogger)

    def test_log_directory_creation(self):
        pass

    def test_log_file_creation(self):
        pass


@pytest.mark.questionable
def test_get_root_dir():
    pass
