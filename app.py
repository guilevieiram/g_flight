from src.decorators import log
from src.model import db, flight_model, user_model
from src.view import messager, ui
from src.controller import controller
from main import main as app

if __name__ == "__main__":
    app()