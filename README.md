# MysqlExercises
### Initial env configuration (DB setup)
`python3 -m venv <env_name>`<br>
`source <env_name>/bin/activate`<br>
`pip install -r requirements.txt`<br>
<p><em>Comment: Exercise was developed with Ubuntu 20.04 / Python 3.9.13</em></p>

### DB setup
`python app.py db-setup`
### Functional requirements
* Adding to Product table 2 new columns: UnitPriceUSD, UnitPriceEuro.<br>Covered by DB setup: `python app.py db-setup`
* Connecting with NbpAPI, downloading current USD/Euro rates and then updating mydb.Product.{UnitPriceUSD|UnitPriceEuro} currency rates.
<br>`python app.py update-currency-rates`
* Generating excel report with list of all product
<br>`python app.py generate-report`

### Run tests
* All tests:<br>
`PYTHONPATH=. pytest -p no:logging -s -vv tests/ `<br>
* All tests (apart from logging related items):<br>
`PYTHONPATH=. pytest -s -vv tests/`<br>
* All tests (apart from tests marked as questionable):<br>
`PYTHONPATH=. pytest -p no:logging -s -vv tests/ -m "not questionable"`
