from src.model.db import CSVDB

if __name__ == "__main__":

	db = CSVDB(db_name="data")

	data = {"city": "Berlin", "price": 1000}

	db.create_table_from_template("london", "flights_test")

	db.add_data("saopaulo", data = [data])