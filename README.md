# MysqlExercises
### Initial env configuration (DB setup)
`PYTHONPATH=. python src/db.py`
### Functional requirements
* Adding to Product table 2 new columns: UnitPriceUSD, UnitPriceEuro.
<br>`Covered by Initial Db setup: PYTHONPATH=. python src/db.py`
* Connecting with NbpAPI, downloading current USD/Euro rates and then updating mydb.Product.{UnitPriceUSD|UnitPriceEuro} currency rates.
<br>`python app.py update-currency-rates`

### Run tests
`PYTHONPATH=. pytest -s -vv tests/`
