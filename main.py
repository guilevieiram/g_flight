from src.decorators import log
from src.model import db, flight_model, user_model
from src.view import messager, ui
from src.controller import controller

def main(
	user_interface: ui.UserInterface,
	messager: messager.Messager,

	controller: controller.Controller,

	flight_model: flight_model.FlightModel,
	user_model: user_model.UserModel,
	data_base: db.DataBase
	) -> None:

	bot = controller(
		user_interface=user_interface(),
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

	bot.load_ui()


if __name__ == "__main__":
	main(
		controller=controller.FlaskAPIController,
		user_interface=ui.TerminalUserInteface,
		messager=messager.TerminalMessager,
		flight_model=flight_model.TequilaFlightModel,
		user_model=user_model.TerminalUserModel,
		data_base=db.CSVDB
		)