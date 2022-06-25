from xlsxwriter import Workbook

from src.db import DbWrapper
from src.helpers import get_credentials


class ExcelReport:
    """One Page/Worksheet Excel report."""

    def __init__(self, name: str = "report.xlsx"):
        self._name = name
        self._bold = None

    def __enter__(self):
        self._workbook = Workbook(self._name)
        self._worksheet = self._workbook.add_worksheet()
        self._bold = self._workbook.add_format({'bold': True})
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._workbook.close()

    @property
    def name(self):
        return self._name

    def fill_header_row(self, header_row: tuple[str, ...]) -> None:
        self._worksheet.write_row("A1", header_row, self._bold)

    def fill_worksheet_rows(self, rows: list[tuple[str, ...], ...]) -> None:
        for row_id, row in enumerate(rows, start=2):
            self._worksheet.write_row(f"A{row_id}", row)


def generate_product_report() -> str:
    product_table_columns = ("ProductID", "DepartmentID", "Category", "IDSKU", "ProductName", "Quantity", "UnitPrice", "UnitPriceUSD", "UnitPriceEuro", "Ranking", "ProductDesc", "UnitsInStock", "UnitsInOrder")
    columns = ", ".join(["p." + column for column in product_table_columns])
    product_query = f"select {columns} from mydb.Product p order by p.ProductID asc;"
    with DbWrapper(**get_credentials()) as db_, ExcelReport() as report:
        report.fill_header_row(product_table_columns)
        fetched_items = db_.execute_query(product_query)
        report.fill_worksheet_rows(fetched_items)
        return report.name
