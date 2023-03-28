from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, ForeignKey
import enum

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorites = db.relationship("Favorites", backref="user", lazy=True)
    

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
      
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),  nullable=False)
    height = db.Column(db.String(120),  nullable=False)
    eye_color = db.Column(db.String(120),  nullable=False)
    hair_color = db.Column(db.String(120),  nullable=False)

    def __repr__(self):
        return f'<People ${self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color
            # do not serialize the password, its a security breach
        }

    

class Planets(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False )
    gravity = db.Column(db.String(120), nullable=False )
    population = db.Column(db.String(120), nullable=False)
    climate = db.Column(db.String(120), nullable=False)

    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate
            # do not serialize the password, its a security breach
        }


class Nature(enum.Enum):
    planets = "planets"
    people = "people"

class Favorites(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    nature_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    nature = db.Column("nature",Enum(Nature))

    def __repr__(self):
        return f'<Favorites {self.nature} {self.nature_id}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "nature_id":self.nature_id,
            "user_id": self.user_id,
            "nature": self.nature.value

            # do not serialize the password, its a security breach
        }
