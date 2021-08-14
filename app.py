from src.decorators import log
from src.model import db, flight_model, user_model
from src.view import messager, ui
from src.controller import controller
from main import main

def app (environ, start_response):
	_controller = controller.FlaskAPIController
	_user_interface = ui.FlaskUserInterface
	_messager = messager.TerminalMessager
	_flight_model = flight_model.TequilaFlightModel
	_user_model = user_model.TerminalUserModel
	_data_base = db.PostgresqlDataBase


	bot = _controller(
		port=5000,
		user_interface=_user_interface(
			port=4000,
			backend_endpoint="http://127.0.0.1:5000"
		),
		messager=_messager(),
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
		)

	return bot.app

if __name__ == "__main__":
    app().run()