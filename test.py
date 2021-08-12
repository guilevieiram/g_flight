from src.model.db import PostgresqlDataBase

if __name__ == "__main__":
	db = PostgresqlDataBase(db_name='name')

	data = [
		{
			'city': 'Belo Horizonte',
			'price': 1000
		},
		{
			'city': 'London',
			'price': 1000
		}
	]
	print(db.get_data('flights'))
	db.create_table_from_template('bh', 'flights')
	print(db.get_data('bh'))
