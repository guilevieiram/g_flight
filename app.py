from src.decorators import log
from src.model import db, flight_model, user_model
from src.view import messager, ui
from src.controller import controller

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
		user="postmaster@sandbox5c725b2cd6e14cacbb1cf89697024fa1.mailgun.org",
		password="b3744b23ca9cd21f013da1449dbac525-9ad3eb61-40edec17"
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
