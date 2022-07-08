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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Characters.query.all()
    characters_serialized = [character.serialize()for character in characters]

    return jsonify(characters_serialized), 200

@app.route('/characters', methods=['POST'])
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

@app.route('/planets', methods=['POST'])
def create_planets():
    data = request.get_json()
    for item in data:
        planet = Planets(name = item["name"], rotation_period = item["rotation_period"], orbital_period = item["orbital_period"], terrain = item["terrain"])
        db.session.add(planet)
        db.session.commit()

    return jsonify("planets added"), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
