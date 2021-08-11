import requests
from werkzeug.wrappers import response

if __name__ == "__main__":


	# response = requests.put(
	# 	url = 'http://127.0.0.1:5000/users',
	# 	data={
	# 		'first_name': 'test name',
	# 		'e_mail': 'gui@test.com'
	# 	}
	# )

	response = requests.put(url = 'http://127.0.0.1:5000/users',
		data= {
			'first_name': 'gui',
			'last_name': 'vieira',
			'e_mail': 'gui@test.com',
			'city': 'Belo Horizonte'
		}
	)
	print(response.json())
