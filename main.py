from argparse import ArgumentParser

from src.decorators import log
from src.model import db, flight_model, user_model
from src.view import messager, ui
from src.controller import controller

def setup_parser() -> ArgumentParser:
	parser = ArgumentParser()
	parser.add_argument('--backend', '-b', default=False, action='store_true', help='Load the backend API server')
	parser.add_argument('--frontend', '-f', default=False, action='store_true', help='Loads the app frontend.')
	return parser

def main(
	user_interface: ui.UserInterface,
	messager: messager.Messager,

	controller: controller.Controller,

	flight_model: flight_model.FlightModel,
	user_model: user_model.UserModel,
	data_base: db.DataBase
	) -> None:


	bot = controller(
		port=5000,
		user_interface=user_interface(
			port=5500,
			backend_endpoint="http://127.0.0.1:5000"
		),
		messager=messager(),
		flight_model=flight_model(
			data_base=data_base(
				db_name="flight_data"
				)
			),
		user_model=user_model(
			data_base=data_base(
				db_name="user_data"
				)
			),
		)

	
	parser = setup_parser()
	arguments = vars(parser.parse_args())

	if arguments["backend"]:
		bot.load_backend()
	elif arguments["frontend"]:
		bot.load_ui()
	

if __name__ == "__main__":
	main(
		controller=controller.FlaskAPIController,
		user_interface=ui.FlaskUserInterface,
		messager=messager.TerminalMessager,
		flight_model=flight_model.TequilaFlightModel,
		user_model=user_model.TerminalUserModel,
		data_base=db.CSVDB
		)