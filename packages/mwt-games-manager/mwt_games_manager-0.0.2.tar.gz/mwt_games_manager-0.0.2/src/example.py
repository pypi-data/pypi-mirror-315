import firebase_admin
from firebase_admin import credentials, firestore, get_app

client = None
if get_app("games-manager"):
    client = firestore.client(get_app("games-manager"))


def setup_firebase(database_credentials):
    global client
    firestore_app = firebase_admin.initialize_app(database_credentials)
    client = firestore.client(firestore_app)
    print(client)

