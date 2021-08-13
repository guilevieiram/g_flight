import requests
if __name__ == "__main__":
	response = requests.post(url = "http://127.0.0.1:5000/current_flights", 
		data = {
			"city": "Belo Horizonte"
		}
	)

	print(response)