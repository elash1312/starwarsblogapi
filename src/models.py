from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorites')

    def __repr__(self):
        return f'<User {self.email}>'
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')

    def __repr__(self):
        return f"<Favorites {self.id}>"
    
    def serialize(self):
        return {
            "id": self.id,
            'name': self.name
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    height = db.Column(db.String(80))
    hair_color = db.Column(db.String(80))
    eye_color = db.Column(db.String(80))

    def __repr__(self):
        return f"<Characters {self.id}>"
    
    def serialize(self):
        return {
        "id": self.id,
        "name": self.name,
        "height": self.height,
        "hair color": self.hair_color,
        "eye color": self.eye_color
        }

class Planets(db.Model):
    __tablename__ = 'Planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    rotation_period = db.Column(db.String(80))
    orbital_period = db.Column(db.String(80))
    terrain = db.Column(db.String(80))

    def __repr__(self):
        return f"<Planets {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation period": self.rotation_period,
            "orbital period": self.orbital_period,
            "terrain": self.terrain
        }