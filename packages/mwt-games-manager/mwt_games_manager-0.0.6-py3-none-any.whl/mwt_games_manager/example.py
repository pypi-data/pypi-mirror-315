import firebase_admin
from firebase_admin import credentials, firestore, get_app

client = None
try:
    client = firestore.client(get_app("games-manager"))
except Exception as e:
    pass


def setup_firebase(database_credentials):
    global client
    firestore_app = firebase_admin.initialize_app(database_credentials)
    client = firestore.client(firestore_app)
    print(client)

