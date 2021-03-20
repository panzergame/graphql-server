from graphene import ObjectType, String, Decimal, Schema, List, NonNull, Field, Mutation

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
	cost = Decimal()
	weight = Decimal()

	class Meta:
		default_resolver = db_resolver


class Query(ObjectType):
	clients = List(Client)
	client_by_id = Field(Client, id=String())
	client_by_credential = Field(Client, email=String(), password=String())
	products = List(Product)
	product_by_id = Field(Product, id=String())

	def resolve_client_by_id(self, info, id):
		client_ref = database.clients_ref.document(id)
		return Client(client_ref.get())

	def resolve_client_by_credential(self, info, email, password):
		client_ref = database.clients_ref \
			.where('email', '==', email) \
			.where('password', '==', password)

		return Client(client_ref.get()[0])

	def resolve_clients(self, info):
		clients = database.clients_ref.stream()

		return map(lambda client: Client(client), clients)

	def resolve_product_by_id(self, info, id):
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
