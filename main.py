from argparse import ArgumentParser

from src.decorators import log
from src.model import db, flight_model, user_model
from src.view import messager, ui
from src.controller import controller

def setup_parser() -> ArgumentParser:
	parser = ArgumentParser()
	parser.add_argument('--backend', '-b', default=True, action='store_true', help='Load the backend API server')
	parser.add_argument('--frontend', '-f', default=False, action='store_true', help='Loads the app frontend.')
	return parser

def main() -> None:

	_controller = controller.FlaskAPIController
	_user_interface = ui.TerminalUserInterface
	_messager = messager.TerminalMessager
	_flight_model = flight_model.TequilaFlightModel
	_user_model = user_model.TerminalUserModel
	_data_base = db.PostgresqlDataBase


	bot = _controller(
		port=5000,
		user_interface=_user_interface(
			# backend_endpoint="https://g-flights-backend.herokuapp.com"
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
	
	parser = setup_parser()
	arguments = vars(parser.parse_args())

	if arguments["frontend"]:
		bot.load_ui()
	elif arguments["backend"]:
		bot.load_backend()

if __name__ == "__main__":
	main()