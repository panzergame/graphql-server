import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

db = None
clients_ref = None
products_ref = None

def init_db(app):
	global db
	global clients_ref
	global products_ref

	cred = credentials.Certificate(app.config['FIREBASE_CERTIFICATE'])
	firebase_admin.initialize_app(cred)

	db = firestore.client()
	clients_ref = db.collection('clients')
	products_ref = db.collection('products')
