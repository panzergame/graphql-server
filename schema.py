from graphene import ObjectType, String, Schema, List, NonNull, Field, Mutation

import database


def db_resolver(attname, default_value, root, info, **args):
	return root.doc.get(attname)


class DbObjectType(ObjectType):
	def __init__(self, doc):
		self.doc = doc


class Client(DbObjectType):
	firstname = String()
	lastname = String()
	id = String()

	class Meta:
		default_resolver = db_resolver

	def resolve_id(self, info):
		return self.doc.id


class Query(ObjectType):
	clients = List(Client)
	client = Field(Client, id=String())

	def resolve_client(self, info, id):
		client_ref = database.clients_ref.document(id)
		return Client(client_ref.get())

	def resolve_clients(self, info):
		clients = database.clients_ref.stream()

		return map(lambda client: Client(client), clients)


class RegisterClient(Mutation):
	class Arguments:
		firstname = String()
		lastname = String()

	Output = Client

	def mutate(self, info, firstname, lastname):
		_, doc = database.clients_ref.add({
			"firstname": firstname,
			"lastname": lastname
		})

		client = Client(doc.get())

		return client


class Mutation(ObjectType):
	registerClient = RegisterClient.Field()


schema = Schema(query=Query, mutation=Mutation)
