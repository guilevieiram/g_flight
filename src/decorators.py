import json
import datetime

def log(name: str):
	def logger(function):
		def wrapper(*args, **kwargs):

			result = function(*args, **kwargs)	

			if isinstance(result, dict):
				printable_result: str = json.dumps(result, indent=4)
			else:
				printable_result: str = result

			try:
				with open(f"logs/{name}.txt", "a") as log_file:
					log_file.write(
						f"{datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}\n\n" + \
						f"{function.__name__}\n\n{printable_result}\n------------------------------\n"
						)	
			except FileNotFoundError:
				with open(f"logs/{name}.txt", "w+") as log_file:
					log_file.write(
						f"{datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}\n\n" + \
						f"{function.__name__}\n\n{printable_result}\n------------------------------\n"
						)	

			return result		
		return wrapper
	return logger

def terminal_action(message: str, sleep_time: int = 1):
	def logger(function):
		def wrapper(*args, **kwargs):
			print(message)
			result = function(*args, **kwargs)
			print(result)
			time.sleep(sleep_time)
			return result		
		return wrapper
	return logger