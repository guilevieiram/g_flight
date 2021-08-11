from src.decorators import log
from abc import ABC, abstractmethod
import os
import smtplib

from typing import Optional


class Messager(ABC):
	"""Messager class, responsible for communicating with a given destination"""

	@abstractmethod
	def send_message(self, destination: str, message: str, subject: str) -> None:
		"""Sends a message with a subject to the destination (email, phone, ...)"""
		pass


class TerminalMessager(Messager):
	"""Terminal implementation. Used for debuggin mainly."""

	@log("messager_log")
	def send_message(self, destination: str, message: str, subject: str) -> None:
		content = "\n-------------------------------------------------------------------"
		content += f"\nMessage to {destination}\nSubject: {subject}\n\n{message}"
		content += "\n-------------------------------------------------------------------\n"
		print(content)
		return content


class EmailMessager(Messager):
	"""Email implementation of the messager, using smtp."""

	def __init__(self, 
				user: str = os.environ.get("EMAIL_USER"),
				password: str = os.environ.get("EMAIL_PASSWORD_PYTHON"),
				server: str = "smtp.gmail.com",
				port: int = 587) -> None:

		"""Initializes the credentials. Uses my values as default but that can be changed if you want."""

		self.user: str = user
		self.password: str = password
		self.server: str = server
		self.port: int = port

	@log("mail_log")
	def connect_to_server(self) -> Optional[str]:
		"""Connect to smtp server and tls secures the connection"""
		self.connection = smtplib.SMTP(self.server, self.port)
		self.connection.starttls() 

	@log("mail_log")
	def login(self) -> None:
		"""Logs in on the initialized account."""
		self.connection.login(user=self.user, password=self.password)

	@log("mail_log")
	def logout(self) -> None:
		"""Logs out, closing the connection (a good practice)"""
		self.connection.close()

	@log("mail_log")
	def send_message(self, destination: str, message: str, subject: str) -> Optional[str]:
		"""Connects, logs in, sends a formatted message and logs out."""
		self.connect_to_server()
		self.login()
		self.connection.sendmail(
			from_addr=self.user,
			to_addrs=destination,
			msg=f"Subject:{subject}\n\n{message}"
			)
		self.logout()
