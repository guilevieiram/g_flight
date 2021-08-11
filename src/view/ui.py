from abc import ABC, abstractmethod
from enum import Enum, auto
from dataclasses import dataclass
import os
import time

from src.decorators import terminal_action

# Menu enumerator classes
class Menu(Enum):
	pass

class MainMenu(Menu):
	EXIT = 0
	MANAGE_USERS = auto()
	SEND_FLIGHTS = auto()
	UPDATE_FLIGHTS = auto()

	def name() -> str:
		return "Main menu"

class UserMenu(Menu):
	EXIT = 0
	ADD_USER = auto()
	DELETE_USER = auto()
	UPDATE_USER = auto()
	FIND_USER = auto()

	def name() -> str:
		return "User menu"


# Abstract user interface class
class UserInterface(ABC):
	"""User interface class. Responsible for showing and retrieving information from the user"""

	@abstractmethod
	def start(self) -> None:
		"""A starter, to initiate the interface."""
		pass

	@abstractmethod
	def get_actions(self, **actions) -> None:
		"""
		Should get all the necessary actions from the controller
		to associate them to commands on the ui
		"""
		pass

	@abstractmethod
	def accquire_info(self, information_needed: list, message: str) -> dict:
		"""Acquire a new user info, with a list of desired information"""
		pass

# User interface implementation
class TerminalUserInteface(UserInterface):
	"""Simple terminal user interface"""

	def start(self) -> None:
		"""Start screen and main loop"""
		print("Welcome to FlightBot!\n")
		time.sleep(1)
		self.main_loop()

	def main_loop(self) -> None:
		"""Main action loop"""
		while True:
			user_action: Menu = self.show_menu(MainMenu)
			self.do_action(action=user_action)

	def get_actions(self, **actions) -> None:
		"""Updates the class methods with methods provided by the controller."""
		self.__dict__.update(actions)

	def accquire_info(self, information_needed: list, message: str = "") -> dict:
		"""Method to be used by the controller to get information from the user."""
		print(message)
		information: dict = {}
		for item in information_needed:
			# Could use formatting
			information[item] = input(f"\t{self.to_title_case(item)}: ")
		return information

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

	def do_action(self, action: Menu) -> None:
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
			self.do_action(self.show_menu(UserMenu))
		elif action == MainMenu.SEND_FLIGHTS:
			print("Sending out the best flights...\n")
			self.cont_send_cheapest_flights()
			input("\nPress any key to continue ...")
		elif action == MainMenu.UPDATE_FLIGHTS:
			print("Updating flight prices...\n")
			self.cont_update_flight_prices()
			input("\nPress any key to continue ...")

	def user_menu_actions(self, action: Menu) -> None:
		"""Mapping the user menu actions"""
		if action == UserMenu.ADD_USER:
			print("Adding user\n")
			print(self.cont_add_user())
			input("\nPress any key to continue ...")
		elif action == UserMenu.DELETE_USER:
			print("Deleting user\n")
			print(self.cont_delete_user())
			input("\nPress any key to continue ...")
		elif action == UserMenu.UPDATE_USER:
			print("Updating user\n")
			print(self.cont_update_user())
			input("\nPress any key to continue ...")
		elif action == UserMenu.FIND_USER:
			print("Finding user\n")
			print(self.cont_find_user())
			input("\nPress any key to continue ...")


	@staticmethod
	def exit() -> None:
		"""Exits the program terminating the script"""
		exit()

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