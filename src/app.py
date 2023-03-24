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
from models import db, User, People, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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
def handle_user():
    if request.method == "GET":
        users = User.query.all()
        users_list =[]
        for user in users:
            users_list.append(user.serialize())
            
            return jsonify(users_list), 200
        
@app.route('/user/favorites', methods=['GET'])
def handleuser_favorites():
    if request.method == 'GET':
        search_favoritebyuser = Favorites.query.all()
        # favoritebyuser =[]
        # for favorite in search_favoritebyuser:
        #     favoritebyuser.append(favorite.serialize())
        return (list(map(lambda favorite:favorite.serialize(),search_favoritebyuser)))

@app.route('/people', methods=["GET"])
def getpeople():
    if request.method =="GET":
        people = People.query.all()
        person_list= []  
        for person in people:
            person_list.append(person.serialize())
        
        return jsonify(person_list),200

@app.route('/planets', methods=["GET"])
def getplanets():
    if request.method == "GET":
        planets = Planets.query.all()
        planets_list =[]
        for planet in planets:
            planets_list.append(planet.serialize())

        return jsonify(planets_list), 200

@app.route('/people/<int:people_id>', methods=["GET"])
def getpeople_id(people_id=None):
    if request.method == "GET":
        person_id = People.query.filter_by(id=people_id).first()
        if person_id is None:
            return jsonify({"Message":"There's no person with that ID"}),404
        else:
            return jsonify(person_id.serialize()),200
        
@app.route('/planets/<int:planets_id>', methods=["GET"])
def planets_id(planets_id=None):
    if request.method == "GET":
        planets_id = Planets.query.filter_by(id=planets_id).first()
        if planets_id is None:
            return jsonify({"Message":"There's no person with that ID"}),404
        else:
            return jsonify(planets_id.serialize()),200

@app.route('/favorites/people/<int:nature_id>',methods=['POST'])
def getfavorites_people(nature_id=None):
    if People.query.filter_by(id=nature_id).first():
        search_favorite = Favorites.query.filter_by(user_id=1, nature_id=nature_id).first()
        if search_favorite:
            return jsonify({"Message":"Favorite already exist"}),400
        else:
            if request.method == 'POST':
                favorite = Favorites(user_id=1, nature='people', nature_id=nature_id)
                db.session.add(favorite)
                db.session.commit()
            return jsonify({"Message":"Favorite has been added to the user"}),201
    else:
        return jsonify({"Message":"People don't exist"}),400    

@app.route('/favorites/planets/<int:nature_id>', methods=['POST'])
def getfavorites_planets(nature_id=None):
    if Planets.query.filter_by(id=nature_id).first():
        search_favorite= Favorites.query.filter_by(user_id=1, nature_id=nature_id).first()
        if search_favorite:
            return jsonify({'Message':'Favorite already exist'}), 400
        else:
            if request.method == 'POST':
                favorite= Favorites(user_id=1, nature='planets', nature_id=nature_id)
                db.session.add(favorite)
                db.session.commit()
            return jsonify({'Message':'Favorite has been added to user'}),201
    else:
        return jsonify({'Message':'Planet doesnt exist'}),400

@app.route('/favorites/planets/<int:nature_id>', methods=['DELETE'])
def delete_planets(nature_id=None):
    search_favorite= Favorites.query.filter_by(user_id=1, nature='planets', nature_id=nature_id).first()
    if search_favorite:
        db.session.delete(search_favorite)
        db.session.commit()
        return jsonify({'Message':'Favorite has been deleted successfully'}),201
    else:
        return jsonify({'Message':'Favorite that want to be deleted doesnt exist'}),400

@app.route('/favorites/people/<int:nature_id>', methods=['DELETE'])
def delete_people(nature_id=None):
    search_favorite = Favorites.query.filter_by(user_id=1, nature="people", nature_id=nature_id).first()
    if search_favorite:
        db.session.delete(search_favorite)
        db.session.commit()
        return jsonify({'Message':'Favorite has been deleted successfully'})
    else:
        return jsonify({'Message':'Favorite that would like to be deleted doesnt exist'})


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)