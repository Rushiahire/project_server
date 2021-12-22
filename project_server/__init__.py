import firebase_admin
from firebase_admin import credentials


creds = credentials.Certificate('serviceAccountKey.json')

firebase_admin.initialize_app(creds)
