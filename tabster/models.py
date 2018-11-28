from tabster import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)    

class Tabs(db.Model): #inherits from a basic db model provided by sql alchemy and creates a table called Tabs were we will store our tabs objects 
    title = db.Column(db.String(80), unique=False, nullable=False, primary_key=False) #create a column named title that consist of a String of at most 80characters, that can store two tabs with the same name, the tab must have a title and is not a primary key
    author = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    url = db.Column(db.String(200), unique=True, nullable=False, primary_key=True)    
    typology = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    capo = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
    tuning = db.Column(db.String(80), unique=False, nullable=True, primary_key=False)


    def __repr__(self): #representation of our book object as a string (like toString)
        return "<Title: {}>".format(self.title) 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


'''The model class created in the previous section defines the initial database structure (or schema) for this application. But as the application continues to grow, there is going to be a need change that structure, very likely to add new things, but sometimes also to modify or remove items. Alembic (the migration framework used by Flask-Migrate) will make these schema changes in a way that does not require the database to be recreated from scratch.

To accomplish this seemingly difficult task, Alembic maintains a migration repository, which is a directory in which it stores its migration scripts. Each time a change is made to the database schema, a migration script is added to the repository with the details of the change. To apply the migrations to a database, these migration scripts are executed in the sequence they were created.

Flask-Migrate exposes its commands through the flask command. You have already seen flask run, which is a sub-command that is native to Flask. The flask db sub-command is added by Flask-Migrate to manage everything related to database migrations. So let's create the migration repository for microblog by running flask db init:


flask db migrate -m "users table"
With the migration repository in place, it is time to create the first database migration, which will include the users table that maps to the User database model. There are two ways to create a database migration: manually or automatically. To generate a migration automatically, Alembic compares the database schema as defined by the database models, against the actual database schema currently used in the database. 
It then populates the migration script with the changes necessary to make the database schema match the application models. In this case, since there is no previous database, the automatic migration will add the entire User model to the migration script. The flask db migrate sub-command generates these automatic migrations:

The flask db migrate command does not make any changes to the database, it just generates the migration script. To apply the changes to the database, the flask db upgrade command must be used.


Because this application uses SQLite, the upgrade command will detect that a database does not exist and will create it (you will notice a file named app.db is added after this command finishes, that is the SQLite database). When working with database servers such as MySQL and PostgreSQL, you have to create the database in the database server before running upgrade.

The application is in its infancy at this point, but it does not hurt to discuss what is going to be the database migration strategy going forward. Imagine that you have your application on your development machine, and also have a copy deployed to a production server that is online and in use.

Let's say that for the next release of your app you have to introduce a change to your models, for example a new table needs to be added. Without migrations you would need to figure out how to change the schema of your database, both in your development machine and then again in your server, and this could be a lot of work.

But with database migration support, after you modify the models in your application you generate a new migration script (flask db migrate), you probably review it to make sure the automatic generation did the right thing, and then apply the changes to your development database (flask db upgrade). You will add the migration script to source control and commit it.

When you are ready to release the new version of the application to your production server, all you need to do is grab the updated version of your application, which will include the new migration script, and run flask db upgrade. Alembic will detect that the production database is not updated to the latest revision of the schema, and run all the new migration scripts that were created after the previous release.

As I mentioned earlier, you also have a flask db downgrade command, which undoes the last migration. While you will be unlikely to need this option on a production system, you may find it very useful during development. You may have generated a migration script and applied it, only to find that the changes that you made are not exactly what you need. In this case, you can downgrade the database, delete the migration script, and then generate a new one to replace it.

'''