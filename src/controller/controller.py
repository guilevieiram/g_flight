import requests
import datetime
import json
import sys

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS

from abc import ABC, abstractmethod

from src.decorators import log
from src.model import db, flight_model, user_model
from src.view import messager, ui
from src.controller import controller

from src.model.flight_model import Flight
from src.model.user_model import User

# preventing __pycache__ files ofbeing created
sys.dont_write_bytecode = True

# Helper functions
def get_payload() -> dict:
	payload_string = request.data.decode('utf8')
	return json.loads(payload_string)

class Controller(ABC):
	"""Controller abstract class to control the main flow of the aplication"""

	@abstractmethod
	def __init__(self,
		port: int,	
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
	def update_flight_prices(self) -> None:
		"""
		Update all the flight prices comparing the lowest available prices with the day's lowest price.
		"""
		pass

	@abstractmethod
	def get_wanted_destinations(self) -> None:
		"""
		Returns the present data for the lowest prices for a given city.
		"""
		pass
	@abstractmethod
	def load_ui(self) -> None:
		"""Load the main ui screen via user_interface."""
		pass

	@abstractmethod
	def load_backend(self) -> None:
		"""Load the server API backend"""
		pass

	@abstractmethod
	def close_backend(self) -> None:
		"""Closes the connection with the backend/ terminate services"""
		pass

	@abstractmethod
	def contact_user(self, user: User, flights: list[Flight]) -> None:
		"""Sends the message with flight information to the user via messager."""
		pass

	@abstractmethod
	def user(self) -> None:
		"""CRUD user operations info via the ui and passes that info to user_model via the User dataclass."""
		pass

class FlaskAPIController(Controller):
	"""Implementation for the controller using a flask rest API."""
	
	def __init__(self,	
		port: int,
		user_interface: ui.UserInterface,
		messager: messager.Messager,
		flight_model: flight_model.FlightModel,
		user_model: user_model.UserModel
		) -> None:
		"""Initializes the controller with all the components it needs."""
		self.user_interface = user_interface
		self.messager = messager
		self.flight_model = flight_model
		self.user_model = user_model

		self.app: Flask = Flask(__name__)
		CORS(self.app)
		self.api: Api = Api(self.app)

		self.api.add_resource(self.user(), '/users')
		self.api.add_resource(self.send_cheapest_flights(), '/send_flights')
		self.api.add_resource(self.update_flight_prices(), '/update_flights')
		self.api.add_resource(self.get_wanted_destinations(), '/current_flights')

	def send_cheapest_flights(self) -> None:
		"""
		For every user in the user_model, find the cheap flight prices using the flight_model.
		Then, send that flight information to the user.
		This action is triggered via a GET request.
		"""
		user_model = self.user_model
		flight_model = self.flight_model
		contact_user = self.contact_user

		class _send_cheapest_flights(Resource):
			def get(self):
				all_users: list[User] = user_model.get_all_users()
				for user in all_users:		
					cheap_flights = flight_model.check_cheap_prices(from_city=user.city)
					if cheap_flights:
						contact_user(user=user, flights=cheap_flights)
				return {'message': 'flights sent to all users'}
		return _send_cheapest_flights

	def update_flight_prices(self) -> None:
		"""
		Update all the flight prices comparing the lowest available prices with the day's lowest price.
		This action is triggered via a GET request.
		"""
		user_model = self.user_model
		flight_model = self.flight_model
		contact_user = self.contact_user

		class _update_flight_prices(Resource):
			def get(self):
				all_users: list[User] = user_model.get_all_users()
				for user in all_users:		
					flight_model.update_flight_prices(from_city=user.city)
				return {'message': 'flights updated.'}
		return _update_flight_prices
	
	def get_wanted_destinations(self) -> None:
		"""
		Returns the present data for the lowest prices for a given city.
		"""
		flight_model = self.flight_model
		class _get_wanted_destinations(Resource):
			def post(self):
				city: dict = get_payload()["city"]
				try:
					flights: List[Flight] = flight_model.get_wanted_destinations(from_city=city)
					flights_list = [{
						"city": flight.to_city,
						"price": flight.price 
					} for flight in flights]
					return {"code": 1, "flights": flights_list}
				except KeyError:
					return {"code": -1, "message": "location invalid"}
				
		return _get_wanted_destinations

	def load_ui(self) -> None:
		"""Load the main ui screen via user_interface by lauching the API on the server"""
		try:
			self.user_interface.start()
		except Exception as e:
			print("error while loading ui", e)
		finally:
			print("closing backend")
			self.close_backend()


	def load_backend(self) -> None:
		"""Load the flask restful api to be accessed by the frontend"""
		try:
			self.app.run(debug=True)
		except Exception as e:
			print(e)
		finally:
			print("closing backend")
			self.close_backend()

	def close_backend(self) -> None:
		"""Closes the connection with the backend/ terminate services"""
		self.flight_model.close_connection()
		self.user_model.close_connection()

	def contact_user(self, user: User, flights: list[Flight]) -> None:
		"""Sends the message with flight information to the user via messager."""
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
			subject="G-Flight good deal alert!",
			message=message
			)

	def user(self) -> None:
		"""Get a new user info via the ui and passes that info to user_model via the User dataclass."""
		user_model = self.user_model
		class _Users(Resource):
			def get(self):
				users = user_model.get_all_users()
				return jsonify(users)
			def post(self):
				user_data = get_payload()
				try:
					user_model.add_user(user=User().set(user_data))
				except NameError:
					return {'message': 'User already exists', 'code': -1}
				else: 
					return {'code': 1, **user_data}
			def delete(self):
				user_data = get_payload()
				try:
					user = user_model.find_user(attribute=user_data)
				except KeyError:
					return {'message': 'User not found in database', 'code': -1}
				else:
					user_model.delete_user(user=user)
					return {'message': 'User deleted successfully', 'code': 1}

			def put(self):
				user_data = get_payload()
				try:
					user = user_model.find_user(attribute=user_data["user_data"])
				except KeyError:
					return {'message': 'User not found in database', 'code': -1}
				else:
					user_model.edit_user(user=user, attribute=user_data["new_user_data"])
					return {'message': 'User updated successfully', 'code': 1}
					
		return _Users