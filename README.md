# MysqlExercises
### Initial env configuration (DB setup)
`python app.py db-setup`
### Functional requirements
* Adding to Product table 2 new columns: UnitPriceUSD, UnitPriceEuro.
<br>`Covered by Initial Db setup: python app.py db-setup`
* Connecting with NbpAPI, downloading current USD/Euro rates and then updating mydb.Product.{UnitPriceUSD|UnitPriceEuro} currency rates.
<br>`python app.py update-currency-rates`

### Run tests
* All tests:<br>
`PYTHONPATH=. pytest -p no:logging -s -vv tests/ `<br>
* All tests (apart from logging related items):<br>
`PYTHONPATH=. pytest -s -vv tests/`<br>
* All tests (apart from tests marked as questionable):<br>
`PYTHONPATH=. pytest -p no:logging -s -vv tests/ -m "not questionable"`
