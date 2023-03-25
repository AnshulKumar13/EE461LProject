from flask_mongoengine import MongoEngine

db = MongoEngine()


class User(db.Document):
    """User for our site. Data used to log into and manage
    resources for the site
    Fields:
        first_name: user's first name
        last_name: user's last name
        email: user's email (unique identifier)
        password: user's hashed password
    """
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)


class Projects(db.Document):
    """Projects for our site. The Data that is associated with the
    projects
    Field:
        name: the name of the project
        hardware: list of hardware sets associated with this project
        description: description of the project
    """
    name = db.StringField(required=True, min_length=1, max_length=20)
    description = db.StringField(required=True, min_length=5)
    hardware = db.ListField(db.DictField())
    creator_id = db.ObjectIdField(required=True)
    project_id = db.StringField(required=True, unique=True)


class HardwareSet(db.Document):
    """Hardware Set for checkout
    Fields:
        name: the name of the Hardware Set
        capacity: hardware set capacity (how many we own)
        available: hardware set availability (how many are not currently checked out)
        price: hardware set price per hour
    """
    name = db.StringField(required=True, unique=True, min_length=1)
    capacity = db.IntField(required=True, min_value=0)
    available = db.IntField(required=True, min_value=0)
    price = db.FloatField(required=True, min_value=0)
