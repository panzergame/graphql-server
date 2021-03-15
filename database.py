import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("tp-info802-graphql-server-firebase-adminsdk-snehc-d6f5b0cd40.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

clients_ref = db.collection('clients')
