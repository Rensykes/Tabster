import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
   #WHOOSH_BASE = 'whoosh'
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    UPLOAD_FOLDER = "/Users/chiccolacriola/Documents/Tabs"
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', '.gpx', '.gp5'])


    '''The SECRET_KEY configuration variable that I added as the only configuration item is an important part
    in most Flask applications. Flask and some of its extensions use the value of the secret key as a cryptographic key,
    useful to generate signatures or tokens. The Flask-WTF extension uses it to protect web forms against a nasty attack
    called Cross-Site Request Forgery or CSRF (pronounced "seasurf"). As its name implies, the secret key is supposed to be secret,
    as the strength of the tokens and signatures generated with it depends on no person outside of the trusted maintainers of the
    application knowing it.
    The value of the secret key is set as an expression with two terms, joined by the or operator.
    The first term looks for the value of an environment variable, also called SECRET_KEY.
    The second term, is just a hardcoded string.



    The Flask-SQLAlchemy extension takes the location of the application's database from the SQLALCHEMY_DATABASE_URI configuration variable.
    As you recall from Chapter 3, it is in general a good practice to set configuration from environment variables,
    and provide a fallback value when the environment does not define the variable. In this case I'm taking the database URL
    from the DATABASE_URL environment variable, and if that isn't defined, I'm configuring a database named app.db located in the
    main directory of the application, which is stored in the basedir variable.

	The SQLALCHEMY_TRACK_MODIFICATIONS configuration option is set to False to disable a feature of Flask-SQLAlchemy that I do
	not need, which is to signal the application every time a change is about to be made in the database.



	The database is going to be represented in the application by the database instance.
	The database migration engine will also have an instance.'''
