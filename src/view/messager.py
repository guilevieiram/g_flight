from src.decorators import log
from abc import ABC, abstractmethod
import os
import smtplib
import sys
import requests
import json
from email.mime.text import MIMEText

from typing import Optional

# preventing __pycache__ files ofbeing created
sys.dont_write_bytecode = True

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


class TrustifiMessager(Messager):
	"""
	Messager class implementation for intended use on heroku deployment.
	Uses the Trustifi API to complete the request
	"""
	def __init__(self) -> None:
		self.endpoint: str = "https://be.trustifi.com/api/i/v1/email"

		# needs to be implemented as env variables
		self.key: str = "fff4a63b544f6dc658b86bba0d1e4310c663a4c3cbc2ed4d"
		self.secret: str = "b0f3d23c21ce4b55fc53e8c05c1a09d3"

	def send_message(self, destination: str, message: str, subject: str) -> None:
		"""Sends a message with a subject to the destination (email, phone, ...)"""
		# debuger		
		content = "\n-------------------------------------------------------------------"
		content += f"\nMessage to {destination}\nSubject: {subject}\n\n{message}"
		content += "\n-------------------------------------------------------------------\n"
		print(content)
		# debuger

		data = {
			"recipients": [{
				"email": destination,
				"name": "",
				"phone": {"country_code": "+1","phone_number": "1111111111"}
			}],
			"lists": [],
			"contacts": [],
			"attachments": [],
			"title": subject,
			"html": message,
			"methods": {
				"postmark": False,
				"secureSend": False,
				"encryptContent": False,
				"secureReply": False
  			} 
		}
		self.make_request(data=data)
		
	def make_request(self, data: dict) -> None:
		"""Given the payload, dumps and makes the request"""
		headers = {
			"x-trustifi-key": self.key,
			"x-trustifi-secret": self.secret,
			"Content-Type": "application/json"
		}
		response = requests.request(
			"POST",
			self.endpoint,
			headers=headers,
			data=json.dumps(data)
		)
		print(response.text)


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
		self.connection.quit()

	@log("mail_log")
	def send_message(self, destination: str, message: str, subject: str) -> Optional[str]:
		"""Connects, logs in, sends a formatted message and logs out."""
		self.connect_to_server()
		self.login()
		self.connection.sendmail(
			from_addr=self.user,
			to_addrs=destination,
			msg=MIMEText(f"Subject:{subject}\n\n{message}").as_string()
			)
		self.logout()
