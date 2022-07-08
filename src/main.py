"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, Characters, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_serialized = [user.serialize()for user in users]

    return jsonify(users_serialized), 200

@app.route('/people', methods=['GET'])
def get_all_characters():
    characters = Characters.query.all()
    characters_serialized = [character.serialize()for character in characters]

    return jsonify(characters_serialized), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    character = Characters.query.filter_by(id=people_id).first()
    

    return jsonify(character.serialize()), 200

@app.route('/people', methods=['POST'])
def create_characters():
    data = request.get_json()
    for item in data:
        character = Characters(name = item["name"], height = item["height"], hair_color = item["hair_color"], eye_color = item["eye_color"])
        db.session.add(character)
        db.session.commit()

    return jsonify("characters added"), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planets.query.all()
    planets_serialized = [planet.serialize()for planet in planets]

    return jsonify(planets_serialized), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.filter_by(id=planet_id).first()
    

    return jsonify(planet.serialize()), 200

@app.route('/planets', methods=['POST'])
def create_planets():
    data = request.get_json()
    for item in data:
        planet = Planets(name = item["name"], rotation_period = item["rotation_period"], orbital_period = item["orbital_period"], terrain = item["terrain"])
        db.session.add(planet)
        db.session.commit()

    return jsonify("planets added"), 200

@app.route('/favorites/<int:id>', methods=['GET'])
def get_user_favorites(id):
    favorites = Favorites.query.filter_by(user_id=id)
    favorites_serialized = [favorite.serialize()for favorite in favorites]

    return jsonify(favorites_serialized), 200

@app.route('/users/<int:user_id>/favorites', methods=['POST'])
def create_user_favorite(user_id):
    data = request.get_json()
    
    favorite = Favorites(name = data["name"], user_id = user_id)
    db.session.add(favorite)
    db.session.commit()
    favorites = Favorites.query.filter_by(user_id=user_id)
    favorites_serialized = [favorite.serialize()for favorite in favorites]

    return jsonify(favorites_serialized), 200

@app.route('/users/<int:user_id>/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_user_favorite(user_id, favorite_id):

    favorite = Favorites.query.filter_by(user_id=user_id, id=favorite_id).first()
    db.session.delete(favorite)
    db.session.commit()
    favorites = Favorites.query.filter_by(user_id=user_id)
    favorites_serialized = [favorite.serialize()for favorite in favorites]

    return jsonify(favorites_serialized), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
