import requests
import datetime

from abc import ABC, abstractmethod

from src.decorators import log
from src.model import db, flight_model, user_model
from src.view import messager, ui
from src.controller import controller

from src.model.flight_model import Flight
from src.model.user_model import User


class Controller(ABC):
	"""Controller abstract class to control the main flow of the aplication"""

	@abstractmethod
	def __init__(self,	
		user_interface: ui.UserInterface,
		messager: messager.Messager,
		flight_model: flight_model.FlightModel,
		user_model: user_model.UserModel
		) -> None:
		"""Initializes the controller with all the components it needs."""
		pass

	@abstractmethod
	def send_cheapest_flights(self) -> None:
		"""For every user in the user_model, find the cheap flight prices using the flight_model.
		Then, send that flight information to the user."""
		pass

	@abstractmethod
	def load_ui(self) -> None:
		"""Load the main ui screen via user_interface."""
		pass

	@abstractmethod
	def contact_user(self, user: User, flight: Flight) -> None:
		"""Sends the message with flight information to the user via messager."""
		pass

	@abstractmethod
	def add_user(self) -> None:
		"""Get a new user info via the ui and passes that info to user_model via the User dataclass."""
		pass


class FlightBotController(Controller):
	"""Implementation for the Controller abstract class. More info on that class."""

	def __init__(self,	
		user_interface: ui.UserInterface,
		messager: messager.Messager,
		flight_model: flight_model.FlightModel,
		user_model: user_model.UserModel
		) -> None:

		self.user_interface = user_interface
		self.messager = messager
		self.flight_model = flight_model
		self.user_model = user_model


	def send_cheapest_flights(self) -> None:
		all_users: list[User] = self.user_model.get_all_users()
		for user in all_users:		
			cheap_flights = self.flight_model.check_cheap_prices(from_city=user.city)
			if cheap_flights:
				self.contact_user(user=user, flights=cheap_flights)

	def update_flight_prices(self) -> None:
		all_users: list[User] = self.user_model.get_all_users()
		for user in all_users:		
			cheap_flights = self.flight_model.update_flight_prices(from_city=user.city)

	def load_ui(self) -> None:
		self.user_interface.get_actions(
			cont_add_user=self.add_user,
			cont_delete_user=self.delete_user,
			cont_update_user=self.update_user,
			cont_find_user=self.find_user,
			cont_send_cheapest_flights=self.send_cheapest_flights,
			cont_update_flight_prices=self.update_flight_prices
			)
		self.user_interface.start()

	def contact_user(self, user: User, flights: list[Flight]) -> None:
		print("contacting user")
		message = f"\nHello {user.first_name}! We have found some good cheap flights that might interest you!\n"

		for flight in flights:
			message +=	f"\nFly from {flight.from_city}-{flight.from_airport} to {flight.to_city}-{flight.to_airport} "
			message += 	f"leaving on {flight.departure_date.strftime('%d/%m/%y')} "
			message += 	f"and returning on {flight.return_date.strftime('%d/%m/%y')}.\n"
			message += 	f"For only {flight.price} euros !\n"

			if flight.stops:
				message += f"\nThis flight has {len(flight.stops)} stops at {', '.join(flight.stops)}\n"

		self.messager.send_message(
			destination=user.e_mail,
			subject="Flight Deal Alert!!!",
			message=message
			)

	def add_user(self) -> str:
		user_attributes: list[str] = list(User().__dict__.keys())
		user_data: dict = self.user_interface.accquire_info(information_needed=user_attributes, message="Enter the following info: ")
		try:
			self.user_model.add_user(user=User().set(user_data))
			return "User added."
		except Exception as e:
			return f"Could not add user\n{e}"

	def delete_user(self) -> str:
		user_data: dict = self.user_interface.accquire_info(information_needed=["e_mail"], message="User e-mail:")
		try:
			user: User = self.user_model.find_user(attribute=user_data)
			self.user_model.delete_user(user=user)
			return "User deleted"
		except Exception as e:
			return f"Could not delete user: \n{e}"

	def update_user(self) -> str:
		user_data: dict = self.user_interface.accquire_info(information_needed=["e_mail"], message="User e-mail:")
		try:
			user: User = self.user_model.find_user(attribute=user_data)
		except Exception as e:
			return f"Could not find user: \n{e}"
		else:
			user_attributes: list[str] = list(User().__dict__.keys())
			attribute_name: dict = self.user_interface.accquire_info(information_needed=["attribute"],
				message=f"What would you like to change\nChoose from {', '.join(user_attributes)}")
			attribute_value: dict = self.user_interface.accquire_info(information_needed=[attribute_name["attribute"]])
			attribute: dict = {attribute_name["attribute"]: attribute_value[attribute_name["attribute"]]}
			self.user_model.edit_user(user=user, attribute=attribute)
			return "User updated."

	def find_user(self) -> str:
		user_data: dict = self.user_interface.accquire_info(information_needed=["e_mail"], message="User e-mail:")
		try:
			user: User = self.user_model.find_user(attribute=user_data)
			return user.print()
		except Exception as e:
			return f"Could not find user: \n{e}"		