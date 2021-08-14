import requests
import datetime
import os
import sys

from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Union, Optional, Any

from src.decorators import log
from src.model.db import DataBase

# preventing __pycache__ files ofbeing created
sys.dont_write_bytecode = True

# Data classes
@dataclass
class Flight:
	"""
	Dataclass representing a flight
	The only necessary value to initialization is the price for a flight.
	"""
	price: float 

	departure_date: Optional[datetime.datetime] = datetime.datetime.now()
	return_date: Optional[datetime.datetime] = datetime.datetime.now()

	from_city: Optional[str] = None
	to_city: Optional[str] = None 

	from_code: str = ""
	to_code: str = ""

	from_airport: str = ""
	to_airport: str = ""

	stops: Optional[list] = None 

	_id: Optional[int] = None


@dataclass
class FlightComparisson:
	"""Flight comparisson dataclass. Used to store and compare flights in a simple way"""
	initial: Flight
	found: Flight

	def is_found_better(self) -> bool:
		return self.found.price < self.initial.price


# Abstract model
class FlightModel(ABC):
	"""
	Flight Model abstract class.
	It is responsible for analyzing and operating with all the flight data.
	It has a direct connection with the given data_base
	"""

	@abstractmethod
	def __init__(self, data_base: DataBase) -> None:
		"""Initializes the class with a flights database connection."""
		pass

	@abstractmethod
	def check_cheap_prices(self, from_city: str) -> list[Flight]:
		"""
		Given a city of departure: from_city (e.g. Paris) 
		Must return a list of flights leaving that city.
		This flights have a destination stored in the database and 
		must be returned only if the found price is lower than the stored price.
		"""
		pass

	@abstractmethod
	def update_flight_prices(self, from_city: str) -> None:
		"""
		Gets the found flights and the stored flight destinations
		Updates the flight prices with the average between the stored and the found price.
		With time this should reflect the average price for a flight.
		"""
		pass

	@abstractmethod
	def set_flight_prices(self, from_city: str) -> None:
		"""
		Gets all the wanted destinations from a city
		Sets all the flight prices with the price found that day.
		Used as an initializer for newly created tables
		"""
		pass
	
	@abstractmethod
	def get_wanted_destinations(self, from_city: str) -> list[Flight]:
		"""
		Given a departure city, should check the data base to get all the flights leaving that city.
		If a table of that city does not exists, must create one from the template and update 
		the prices with the current up to date value.		
		"""
		pass

	@abstractmethod
	def close_connection(self) -> None:
		"""Closes the model connection with its data base and terminates processes"""
		pass

# Model implementation

class TequilaFlightModel(FlightModel):
	"""
	Flight model implemented using the Kiwi Tequila Flights API. 
	It uses an helper class 'TequilaFlightApi' as a search engine to handle the requests.
	"""

	def __init__(self, data_base: DataBase, months_window: int = 6, minimum_stay: int = 2, maximum_stay: int = 20) -> None:
		"""Initializes the model with the API helper class and some mutable settings for the flight search"""
		self.data_base: DataBase = data_base
		self.flight_search_engine = TequilaFlightApi()

		self.months_window: int = months_window
		self.minimum_stay: int = minimum_stay
		self.maximum_stay: int = maximum_stay

	def check_cheap_prices(self, from_city: str) -> list[Flight]:
		"""
		Compares all the found flights with the stored flight destinations using the FlightComparisson class.
		If the found flight is better, it appends that new flight to a list that is then returned.
		"""
		
		comparissons: List[FlightComparisson] = []
		for destination in self.get_wanted_destinations(from_city=from_city):
			initial_flight = destination
			try:
				found_flight = self.get_cheapest_flight(destination)
			except KeyError as e:
				found_flight = Flight(price=100_000)
			comparissons.append(FlightComparisson(initial=initial_flight, found=found_flight))

		flights_data: list[Flight] = []
		for comparisson in comparissons:
			if comparisson.is_found_better():
				flights_data.append(comparisson.found)

		return flights_data

	def update_flight_prices(self, from_city: str) -> None:
		"""
		Gets the found flights and the stored flight destinations
		Updates the flight prices with the average between the stored and the found price.
		With time this should reflect the average price for a flight.
		"""
		for destination in self.get_wanted_destinations(from_city=from_city):
			try:
				flight: Flight = self.get_cheapest_flight(destination)
			except Exception as e:
				print("error while update_flight_prices: ", e)
			else:
				self.update_data(
					destination=destination,
					new_price= (destination.price + flight.price) / 2
					)

	def set_flight_prices(self, from_city: str) -> None:
		"""
		Gets all the wanted destinations from a city
		Sets all the flight prices with the price found that day.
		Used as an initializer for newly created tables
		"""
		for destination in self.get_wanted_destinations(from_city=from_city):
			try:
				flight: Flight = self.get_cheapest_flight(destination)
				self.update_data(
					destination=destination,
					new_price=flight.price
					)
			except KeyError:
				self.data_base.delete_table(table=self.table_name(city_name=from_city))
				raise KeyError("from_city not valid")
				
	def get_cheapest_flight(self, destination: Flight) -> Flight:
		"""
		Uses the search engine to find flights given a destination. 
		If any meaningful data is returned from the engine the method returns a Flight type object.
		"""
		data = self.flight_search_engine.search_flights(
			from_code=destination.from_code,
			to_code=destination.to_code,
			months_window=self.months_window,
			minimum_stay=self.minimum_stay,
			maximum_stay=self.maximum_stay
			)
		if not data:
			raise KeyError("No Flights found for destination: ", destination)

		return Flight(
			price=data["price"],
			departure_date=self.flight_search_engine.decode_dates(data["utc_departure"]),
			return_date=self.flight_search_engine.decode_dates(data["utc_departure"], day_delta = data["nightsInDest"]),
			from_city=data["cityFrom"],
			to_city=data["cityTo"],
			from_code=data["cityCodeFrom"],
			to_code=data["cityCodeTo"],
			from_airport=data["flyFrom"],
			to_airport=data["flyTo"],
			stops=[route["flyFrom"] for route in self.flight_search_engine.get_routes(routes=data["route"])]
			)


	def update_data(self, destination: Flight, new_price: float) -> None:
		"""
		Updates the destination data in the database with a new price.
		This new price is given by new lowest price.
		"""
		table_name: str = self.table_name(city_name=destination.from_city)
		try:
			self.data_base.update_data(
				table=table_name,
				key=destination._id,
				key_values=[{
					"price": new_price
				}]
				)
		except KeyError:
			self.data_base.create_table_from_template(new_table_name=table_name, parent_table_name="flights")
			self.data_base.update_data(
				table=table_name,
				key=destination._id,
				key_values=[{
					"price": new_price
				}]
				)

	def get_wanted_destinations(self, from_city: str) -> list[Flight]:
		"""
		Given a departure city, should check the data base to get all the flights leaving that city.
		If a table of that city does not exists, must create one from the template and update 
		the prices with the current up to date value.		
		"""
		table_name: str = self.table_name(city_name=from_city)
		try:
			data: list[dict] = self.data_base.get_data(table=table_name)
		except KeyError:
			self.create_flights_table(table_name=table_name, from_city=from_city)
			data: list[dict] = self.data_base.get_data(table=table_name)
		return [
			Flight(
				_id=point["id"],
				to_city=point["city"],
				to_code=self.flight_search_engine.get_IATA_code(point["city"]),
				price=point["price"],
				from_city=from_city,
				from_code=self.flight_search_engine.get_IATA_code(from_city)
				) for point in data
			] 

	def close_connection(self) -> None:
		"""Closes the model connection with its data base and terminates processes"""
		self.data_base.close()

	def create_flights_table (self, table_name: str, from_city: str) -> None:
		"""Creates a flights table with a certain table name, excluding desinations equals to the 'from_city'."""
		self.data_base.create_table_from_template(new_table_name=table_name, parent_table_name="flights")
		try:
			city_key = self.data_base.get_data(table=table_name, key_value = {"city": from_city})[0]["id"]
		except IndexError:
			print("City not included in desired table")
		else:
			self.data_base.delete_data(table=table_name, key=city_key)
		finally:
			self.set_flight_prices(from_city=from_city)


	@staticmethod
	def table_name(city_name: str) -> str:
		return city_name.replace(" ", "").lower()

# Helper Classes
class TequilaFlightApi:
	"""
	Helper class responsible for doing all the Kiwi Tequila API requests
	This class finds cheap flights given a to and a from places and
	finds the IATA code for a given city.

	The api requires a login and a private key, not given here
	"""

	endpoint: str = "https://tequila-api.kiwi.com"
	api_key: str = os.environ.get("FLIGHT_API")

	@log(name='flight_search')
	def search_flights(self, from_code: str, to_code: str, months_window: int, minimum_stay: int, maximum_stay: int) -> Optional[dict]:
		"""Returns the data for the cheapest flight given two places (to and from) and a set of parameters"""
		date_from, date_to = self.get_dates(months=months_window)
		try:
			response = requests.get(
				url=f"{self.endpoint}/v2/search",
				headers={
						"apikey": self.api_key
					},
				params={
						"fly_from": from_code,
						"fly_to": to_code,
						"dateFrom": date_from,
						"dateTo": date_to,
						"nights_in_dst_from": minimum_stay,
						"nights_in_dst_to": maximum_stay,
					}
				)
			return response.json()["data"][0]
		except Exception as e:
			print("Error while searching flights: ", e)

	def get_IATA_code(self, city_name: str) -> str:
		"""Returns the IATA code for a given city name. If no code is found returns 'XXX'. """
		try:
			response = requests.get(
				url=f"{self.endpoint}/locations/query",
				headers={
						"apikey": self.api_key
					},
				params={
						"term": city_name,
					}
				)
			return response.json()["locations"][0]["code"]
		except Exception as e:
			print("Error while getting IATA code:", e)
			return "XXX"


	@staticmethod
	def get_dates(months: int) -> tuple[str]:
		"""
		Auxiliary method that returns a tuple of dates (datetime.datetime objects) for today and 
		a given amount of months from now.
		Used for calculating the time window to search for flights in.
		"""
		date_from = datetime.datetime.now().strftime("%d/%m/%Y")
		date_to = (datetime.datetime.now() + datetime.timedelta(months*30)).strftime("%d/%m/%Y")
		return date_from, date_to

	@staticmethod
	def decode_dates(date: str, day_delta: int = 0) -> datetime.datetime:
		"""
		Decodes the string date returned in the api to a datetime.datetime object.
		It can add a certain time delta in days.
		"""
		return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.000Z") + datetime.timedelta(days=day_delta)

	@staticmethod	
	def get_routes(routes: list[dict]) -> list[dict]:
		"""Get the list of routes on the from-to trip. Excluding the first flight."""
		first_hand_routes = routes[0 : len(routes)//2]
		first_hand_routes = first_hand_routes[1:] # Slicing of the first departure
		return first_hand_routes


