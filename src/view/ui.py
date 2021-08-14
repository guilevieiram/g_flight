from abc import ABC, abstractmethod
from enum import Enum, auto
from dataclasses import dataclass
import os
import time
import sys
import requests
import json

from flask import Flask, render_template

from src.decorators import terminal_action

# preventing __pycache__ files ofbeing created
sys.dont_write_bytecode = True

# Menu enumerator classes
class Menu(Enum):
	pass

class MainMenu(Menu):
	EXIT = 0
	MANAGE_USERS = auto()
	SEND_FLIGHTS = auto()
	UPDATE_FLIGHTS = auto()
	GET_FLIGHTS = auto()

	def name() -> str:
		return "Main menu"

class UserMenu(Menu):
	EXIT = 0
	ADD_USER = auto()
	SEE_USERS = auto()
	DELETE_USER = auto()
	UPDATE_USER = auto()

	def name() -> str:
		return "User menu"

# Abstract user interface class
class UserInterface(ABC):
	"""User interface class. Responsible for showing and retrieving information from the user"""

	@abstractmethod
	def start(self) -> None:
		"""A starter, to initiate the interface."""
		pass

class FlaskUserInterface(UserInterface):
	"""
	User interface implementation. Responsible for showing and retrieving information from the user
	Lauches our web files on a flask server.
	"""

	app: Flask = Flask(__name__)

	def __init__(self, backend_endpoint: str) -> None:
		self.endpoint: str = backend_endpoint

	def start(self) -> None:
		"""A starter, to initiate the interface."""
		self.app.run(debug=True)

	@app.route("/")
	def home():
		"""Endpoint to the index page"""
		return render_template("index.html")
	
	@app.route("/about")
	def about():
		"""Endpoint to the about page"""
		return render_template("about.html")

	@app.route("/view-flights")
	def view_flights():
		"""Endpoint to the view-flights page"""
		return render_template("view-flights.html")

# User interface terminal implementation
class TerminalUserInterface(UserInterface):
	"""Simple terminal user interface"""

	def __init__(self, backend_endpoint: str) -> None:
		self.endpoint: str = backend_endpoint

	def start(self) -> None:
		"""Start screen and main loop"""
		print("Welcome to FlightBot!\n")
		time.sleep(1)
		self.main_loop()

	def main_loop(self) -> None:
		"""Main action loop"""
		while True:
			user_action: Menu = self.show_menu(MainMenu)
			self.do_menu_actions(action=user_action)

	def show_menu(self, menu: Menu) -> Menu:
		"""Shows a given menu, subclass of Menu, and executes the action given."""
		self.clear_screen()
		print(f"{menu.name()}: \n")
		for name, member in menu.__members__.items():
			print(f"{member.value}: {self.to_title_case(name)}")
		return self.get_input(menu=menu)

	def get_input(self, menu: Menu) -> Menu:
		"""Getting user input and mapping into a menu item"""
		try:
			action_number = int(input("\n>>> "))
			return menu(action_number)
		except Exception as e:
			print(e)
			return self.show_menu(menu)

	def do_menu_actions(self, action: Menu) -> None:
		"""Executing of all the menu actions"""
		if isinstance(action, MainMenu):
			self.main_menu_actions(action=action)
		elif isinstance(action, UserMenu):
			self.user_menu_actions(action=action)
	
	def main_menu_actions(self, action: Menu) -> None:
		"""Mapping the main menu actions"""
		if action == MainMenu.EXIT or action == UserMenu.EXIT:
			self.exit()
		elif action == MainMenu.MANAGE_USERS:
			self.do_menu_actions(self.show_menu(UserMenu))
		elif action == MainMenu.SEND_FLIGHTS:
			self.send_cheapest_flights()
		elif action == MainMenu.UPDATE_FLIGHTS:
			self.update_flights()
		elif action == MainMenu.GET_FLIGHTS:
			self.get_flights()

	def user_menu_actions(self, action: Menu) -> None:
		"""Mapping the user menu actions"""
		if action == UserMenu.ADD_USER:
			self.add_user()
		elif action == UserMenu.SEE_USERS:
			self.see_users()
		elif action == UserMenu.DELETE_USER:
			self.delete_user()
		elif action == UserMenu.UPDATE_USER:
			self.update_user()

	# user action methods
	def send_cheapest_flights(self) -> None:
		print("Sending out the best flights...\n")
		requests.get(self.endpoint + "/send_flights")
		print("Fights sent!")
		input("\nPress any key to continue ...")

	def update_flights(self) -> None:
		print("Updating flight prices...\n")
		requests.get(self.endpoint + "/update_flights")
		print("Flight prices updated!")
		input("\nPress any key to continue ...")

	def get_flights(self) -> None:
		print("Getting flights\n")
		print("Please enter the:")
		data= {
				"city": input("\tCity: ")
			}
		data_bytes = json.dumps(data).encode("utf-8")
		response = requests.post(
			url = self.endpoint + "/current_flights",
			data = data_bytes
		)		
		print(response.json())
		input("\nPress any key to continue ...")

	def add_user(self) -> None: 
		print("Adding user\n")
		print("Please enter the user information:")
		data= {
				"first_name": input("\tFirst name: "),
				"last_name": input("\tLast name: "),
				"e_mail": input("\tE-mail: "),
				"phone": "0",
				"city": input("\tCity: ")
			}
		data_bytes = json.dumps(data).encode("utf-8")
		response = requests.post(
			url = self.endpoint + "/users",
			data = data_bytes
		)
		response_code = response.json()["code"]
		if response_code == -1:
			print("User already exists...")
			self.add_user()
		elif response_code == 1:
			print("User added!")
			input("\nPress any key to continue ...")
		else:
			print("Looks like our server are down...\nTry again later")
			input("\nPress any key to continue ...")

	def see_users(self) -> None:
		print("Here are all the users in our data base:")	
		response = requests.get(url = self.endpoint + "/users")
		print(response.json())
		input("\nPress any key to continue ...")

	def delete_user(self) -> None: 
		print("Deleting user\n")
		print("Please enter the user email:")
		data= {
				"e_mail": input("\tE-mail: "),
			}
		data_bytes = json.dumps(data).encode("utf-8")
		response = requests.delete(
			url = self.endpoint + "/users",
			data = data_bytes
		)
		response_code = response.json()["code"]
		if response_code == -1:
			print("User not found in the database...")
			self.delete_user()
		elif response_code == 1:
			print("User deleted!")
			input("\nPress any key to continue ...")
		else:
			print("Looks like our server are down...\nTry again later")
			input("\nPress any key to continue ...")

	def update_user(self) -> None: 
		print("Updating user\n")
		print("Please enter the user email:")
		user_data = {
			"e_mail": input("\tE-mail: ")
		}

		attribute = self.get_atribute()
		new_value = input("Enter the new value: ")
		new_user_data = {
			attribute: new_value
		}

		data = {
			"user_data": user_data,
			"new_user_data": new_user_data
		}
		data_bytes = json.dumps(data).encode("utf-8")
		response = requests.put(
			url = self.endpoint + "/users",
			data = data_bytes
		)
		response_code = response.json()["code"]
		if response_code == -1:
			print("User not found in the database...")
			self.update_user()
		elif response_code == 1:
			print("User atribute changed!")
			input("\nPress any key to continue ...")
		else:
			print("Looks like our server are down...\nTry again later")
			input("\nPress any key to continue ...")

	# helper methods
	@staticmethod
	def exit() -> None:
		"""Exits the program terminating the script"""
		exit()

	def get_atribute(self) -> bool:
		possible_attributes = ["e_mail", "first_name", "last_name", "phone", "city"]
		attribute: str = input(f"Choose one atribute from:\n{', '.join(possible_attributes)}:  ")
		if not attribute in possible_attributes:
			self.get_atribute()
		else: 
			return attribute

	@staticmethod
	def to_title_case(string_snake_case: str) -> str:
		"""
		Auxiliary method for formating strings passed to the ui.
		'turn_this_into_that' -> 'Turn This Into That'
		"""
		splited: list[str] = string_snake_case.split("_")
		splited = [word.lower() for word in splited]
		splited[0] = splited[0].title()
		return " ".join(splited)

	@staticmethod
	def to_regular_case(string_snake_case: str) -> str:
		"""
		Auxiliary method for formating strings passed to the ui.
		'turn_this_into_that' -> 'turn this into that'
		"""	
		splited: list[str] = string_snake_case.split("_")
		splited = [word.lower() for word in splited]
		return " ".join(splited)

	@staticmethod
	def clear_screen() -> None:
		"""Method for clearing the terminal screen. Works for mac, win and linux"""
		os.system('cls' if os.name == 'nt' else 'clear')