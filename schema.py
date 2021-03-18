from graphene import ObjectType, String, Schema, List, NonNull, Field, Mutation

import database


def db_resolver(attname, default_value, root, info, **args):
	return root.doc.get(attname)


class DbObjectType(ObjectType):
	id = String()

	def __init__(self, doc):
		self.doc = doc

	def resolve_id(self, info):
		return self.doc.id

class Client(DbObjectType):
	username = String()
	email = String()
	password = String()

	class Meta:
		default_resolver = db_resolver

class Product(DbObjectType):
	title = String()
	description = String()
	cost = String()
	weight = String()

	class Meta:
		default_resolver = db_resolver


class Query(ObjectType):
	clients = List(Client)
	client = Field(Client, id=String())
	products = List(Product)
	product = Field(Product, id=String())

	def resolve_client(self, info, id):
		client_ref = database.clients_ref.document(id)
		return Client(client_ref.get())

	def resolve_clients(self, info):
		clients = database.clients_ref.stream()

		return map(lambda client: Client(client), clients)

	def resolve_product(self, info, id):
		product_ref = database.products_ref.document(id)
		return Product(product_ref.get())

	def resolve_products(self, info):
		products = database.products_ref.stream()

		return map(lambda product: Product(product), products)


class RegisterClient(Mutation):
	class Arguments:
		username = String()
		email = String()
		password = String()

	Output = Client

	def mutate(self, info, username, email, password):
		_, doc = database.clients_ref.add({
			'username': username,
			'email': email,
			'password': password
		})

		client = Client(doc.get())

		return client


class Mutation(ObjectType):
	registerClient = RegisterClient.Field()


schema = Schema(query=Query, mutation=Mutation)
