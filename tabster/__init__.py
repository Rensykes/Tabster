'''In Python, a sub-directory that includes a __init__.py file is considered a package, and can be imported.
When you import a package, the __init__.py executes and defines what symbols the package exposes to the outside world.'''

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from flask_whooshalchemy as wa
from elasticsearch import Elasticsearch
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)



from tabster import views, models, errors

