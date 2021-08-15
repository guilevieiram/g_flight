from src.decorators import log
from src.model import db, flight_model, user_model
from src.view import messager, ui
from src.controller import controller

import os

"""
This file servs only to start the flask app on heroku.
It is not the most organized but its the only way I could get gunicorn to work.
"""

_controller = controller.FlaskAPIController
_user_interface = ui.FlaskUserInterface
_messager = messager.EmailMessager
_flight_model = flight_model.TequilaFlightModel
_user_model = user_model.TerminalUserModel
_data_base = db.PostgresqlDataBase


app = _controller(
	port=5000,
	user_interface=_user_interface(
		backend_endpoint="https://g-flights-backend.herokuapp.com"
	),
	# embed in evironment vars
	messager=_messager(
		server="smtp.mailgun.org",
		port=587,
		user=os.environ.get("MAILGUN_SMTP_LOGIN"),
		password=os.environ.get("MAILGUN_SMTP_PASSWORD")
	),
	flight_model=_flight_model(
		data_base=_data_base(
			db_name="flight_data"
			)
		),
	user_model=_user_model(
		data_base=_data_base(
			db_name="user_data"
			)
		),
	).app
