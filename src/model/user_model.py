from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Union, Optional, Any

from src.decorators import log
from src.model.db import DataBase

@dataclass
class User:
	"""Dataclass to encode a user."""
	first_name: str = ""
	last_name: str = ""
	e_mail: str = ""
	phone: str = ""
	city: str = ""

	def set(self, data: dict):
		"""
		Method for setting a user if the data is in a dictionary format.
		Use as 'user = User().set(data)'.
		"""
		self.__dict__.update(**data)
		return self

	def print(self):
		"""Method for printing user info in a user-friendly way"""
		return "\n".join([f"{key}: {value}" for key, value in self.__dict__.items()])


class UserModel(ABC):
	"""
	User model responsible for dealing with all the operations related to the users of the aplication.
	It lacks a verification and a login method as those are not yet necessary
	"""

	@abstractmethod
	def __init__(self, data_base: DataBase) -> None:
		"""
		Initializes the object giving it the user data base.
		This data base must have the same atributes as the User dataclass.
		"""
		pass

	@abstractmethod
	def add_user(self, user: User) -> None:
		"""Adds a user to the data base"""
		pass

	@abstractmethod
	def delete_user(self, user: User) -> None:
		"""Deletes a given user (via user object) to the data base"""
		pass

	@abstractmethod
	def find_user(self, attribute: dict[str, Any]) -> User:
		"""
		Finds a user given one of its attributes as a dict (e.g.: {'first_name': 'user1'})
		If many users share this attribute return the first/oldest one.
		"""
		pass

	@abstractmethod
	def get_all_users(self) -> list[User]:
		"""Returns all the users in the data base in a list."""
		pass

	@abstractmethod
	def edit_user(self, user: User, attribute: dict[str, Any]) -> None:
		"""
		Edits a user, setting a new attribute, given as a dictionary.
		The dictionary key must be an atribute of the User dataclass
		"""
		pass


class TerminalUserModel(UserModel):
	"""Implementation of the User Model, loging executions on the terminal."""

	def __init__(self, data_base: DataBase) -> None:
		self.data_base: DataBase = data_base

	def add_user(self, user: User) -> None:
		all_emails = [u.e_mail for u in self.get_all_users()]
		if not user.e_mail in all_emails:
			self.data_base.add_data(table="users", data=[user.__dict__])
		else:
			print("User already exists.")

	def delete_user(self, user: User) -> None:
		user_id: int = self.data_base.get_data(table="users", key_value={"e_mail": user.e_mail})[0]["id"]
		self.data_base.delete_data(table="users", key=user_id)

	def find_user(self, attribute: dict[str, Any]) -> User:
		user_list = self.data_base.get_data(table="users", key_value=attribute)
		if not user_list:
			raise KeyError("User not found on the data base.")
		return self.convert_attributes_user(attributes=user_list[0])

	def get_all_users(self) -> list[User]:
		return [self.convert_attributes_user(attributes=attributes)
				for attributes in self.data_base.get_data(table="users")]

	def edit_user(self, user: User, attribute: dict[str, Any]) -> None:
		user_id: int = self.data_base.get_data(table="users", key_value={"e_mail": user.e_mail})[0]["id"]
		self.data_base.update_data(table="users", key=user_id, key_values=[attribute])

	@staticmethod
	def convert_attributes_user(attributes: dict[str, Any]) -> User:
		"""Converts a dict of attributes to a user object"""
		attributes.pop("id")
		return User().set(attributes)