import firebase_admin
from firebase_admin import credentials, firestore, get_app
from models.game_history import GameHistory
from models.general_game_data import GeneralGameData
from models.user import User
from flask_bcrypt import check_password_hash


client = None
try:
    client = firestore.client(get_app("games-manager"))
except Exception as e:
    pass

default_game_name = ""


def setup_module(database_credentials, game_name):
    global client, default_game_name
    firestore_app = firebase_admin.initialize_app(database_credentials)
    client = firestore.client(firestore_app)
    default_game_name = game_name
    print(client)


def is_user_first_game(username, game_name=default_game_name):
    global client
    if not client:
        raise Exception("module has not been setup properly")

    game_data = client.collection("users").document(username).collection("game-data").document(game_name).get().exists
    return not game_data


def setup_user_game_data(username, game_data=GeneralGameData(), game_name=default_game_name):
    global client
    if not client:
        raise Exception("module has not been setup properly")

    game_data.game_name = game_name
    client.collection("users").document(username).collection("game-data").document(game_name).set(game_data.__dict__)


def _initial_check(username, game_name=default_game_name):
    global client
    if not client:
        raise Exception("module has not been setup properly")

    if is_user_first_game(username, game_name=game_name):
        setup_user_game_data(username, game_name=game_name)


def add_game_history(username, game_history, game_name=default_game_name):
    _initial_check(username, game_name)
    client.collection("users").document(username).collection("game-data").document(game_name).collection(
        "history").document(game_history.game_id).set(game_history.__dict__)


def update_game_history(username, game_history, game_name=default_game_name):
    _initial_check(username, game_name)
    client.collection("users").document(username).collection("game-data").document(game_name).collection(
        "history").document(game_history.game_id).set(game_history.__dict__)


def delete_game_history(username, game_id, game_name=default_game_name):
    _initial_check(username, game_name)
    client.collection("users").document(username).collection("game-data").document(game_name).collection(
        "history").document(game_id).delete()


def get_game_history(username, game_id, game_name=default_game_name):
    _initial_check(username, game_name)
    game_history = client.collection("users").document(username).collection("game-data").document(game_name).collection(
        "history").document(game_id).get()

    game_history = GameHistory(**game_history.to_dict())
    return game_history


def validate_user(username, password, game_name=default_game_name):
    _initial_check(username, game_name)
    user = client.collection("users").document(username).get()
    if not user.exists:
        return False

    user = User(**user.to_dict())

    return check_password_hash(user.password, password)
