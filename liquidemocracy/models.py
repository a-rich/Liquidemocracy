from flask_mongoengine import MongoEngine
import dateutil
import datetime

db = MongoEngine()

class Comment(db.EmbeddedDocument):
    user_id = db.ObjectIdField(required=True)
    parent = db.ReferenceField('self', default='top-level', required=True)
    children = db.ListField(db.ReferenceField('self'), required=True)
    date = db.DateTimeField(default=datetime.datetime.now, required=True)
    text = db.StringField(required=True)

class VoteInfo(db.EmbeddedDocument):
    yay = db.IntField(default=0, required=True)
    nay = db.IntField(default=0, required=True)
    voter_count = db.IntField(default=0, required=True)

class Location(db.EmbeddedDocument):
    city = db.StringField(default='', required=True)
    county = db.StringField(default='', required=True)
    state = db.StringField(default='', required=True)

class Bill(db.Document):
    title = db.StringField(required=True)
    category = db.StringField(required=True)
    date = db.DateTimeField(required=True)
    authors = db.StringField()
    text = db.StringField(required=True)
    source = db.StringField(required=True)
    comments = db.ListField(db.EmbeddedDocumentField(Comment))
    vote_info = db.EmbeddedDocumentField(VoteInfo, required=True)
    location = db.EmbeddedDocumentField(Location, required=True)
    level = db.StringField(required=True)

class DelegatedBill(db.EmbeddedDocument):
    bill = db.ReferenceField(Bill, required=True)
    vote = db.StringField(default='None', required=True)

class InterestVector(db.EmbeddedDocument):
    taxation = db.IntField(default=0, required=True)
    health = db.IntField(default=0, required=True)
    armed_forces_and_national_security = db.IntField(default=0, required=True)
    foreign_trade_and_international_finance = db.IntField(default=0, required=True)
    international_affairs = db.IntField(default=0, required=True)
    crime_and_law_enforcement = db.IntField(default=0, required=True)
    transportation_and_public_works = db.IntField(default=0, required=True)
    education = db.IntField(default=0, required=True)
    energy = db.IntField(default=0, required=True)
    agriculture_and_food = db.IntField(default=0, required=True)
    economics_and_public_finance = db.IntField(default=0, required=True)
    labor_and_employment = db.IntField(default=0, required=True)
    environmental_protection = db.IntField(default=0, required=True)
    science_technology_communications = db.IntField(default=0, required=True)
    immigration = db.IntField(default=0, required=True)
    other = db.IntField(default=0, required=True)

class Residence(db.EmbeddedDocument):
    location = db.EmbeddedDocumentField(Location, required=True)
    last_update = db.DateTimeField(required=True)

class Delegate(db.EmbeddedDocument):
    user_id = db.ObjectIdField(required=True)
    name = db.StringField(required=True)
    bills = db.ListField(db.EmbeddedDocumentField(DelegatedBill))
    categories = db.ListField(db.StringField())

class User(db.Document):
    email = db.EmailField(required=True)
    password = db.StringField(required=True)
    name = db.StringField(required=True)
    residence = db.EmbeddedDocumentField(Residence, required=True)
    interest_vector = db.EmbeddedDocumentField(InterestVector, required=True)
    delegates = db.ListField(db.EmbeddedDocumentField(Delegate))

    @staticmethod
    def exists(email):
        return User.objects(email=email)
