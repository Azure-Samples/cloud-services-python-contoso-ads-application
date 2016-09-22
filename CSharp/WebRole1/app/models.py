from datetime import datetime
from app import db

CategoryList = ['Cars', 'Real Estate', 'Free Stuff']

class Ad(db.Document):
    title = db.StringField(max_length=100)
    price = db.IntField()
    description = db.StringField(max_length=1000)
    imageURL = db.StringField(max_length=2083)
    thumbnailURL = db.StringField(max_length=2083)
    postedDate = db.DateTimeField(default=datetime.now)
    category = db.StringField(max_length=1000)
    phone = db.StringField(max_length=12)