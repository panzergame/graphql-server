from flask import Flask
from flask_graphql import GraphQLView

import database
from schema import schema

import os

app = Flask(__name__)
app.config.from_pyfile(os.environ.get('GRAPHQL_CONFIG') or 'config/default.cfg')

database.init_db(app)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))

if __name__ == '__main__':
	app.run(debug=True)
