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
from models import db, Profesor,Estudiante,Ejercicio, Ficha, Reto
#from models import Person
import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import chilean_rut

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

jwt = JWTManager(app)
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/login/profesor', methods=['POST'])
def loginprof():
    body = request.get_json()
    if "email" not in body:
        return "falta email"
    if "password" not in body:
        return "falta password"
    if "rut" not in body:
        return "falta rut"
    if (chilean_rut.is_valid(body['rut'])==False):
        return "falta rut"
    
 
    user = Profesor.query.filter_by(email = body['email'], password = body['password'], rut = body['rut']).first()
    if(user):

        expira = datetime.timedelta(minutes=1)
        access = create_access_token(identity=body, expires_delta=expira)

        return jsonify({
            "token":access
        })
    else:
        return "datos incorrectos"

@app.route('/login/estudiantes', methods=['POST'])
def loginest():
    body = request.get_json()
    if "email" not in body:
        return "falta email"
    if "password" not in body:
        return "falta password"
    if "rut" not in body:
        return "falta rut"
    if (chilean_rut.is_valid(body['rut'])==False):
        return "falta rut"
    
 
    user = Profesor.query.filter_by(email = body['email'], password = body['password'], rut = body['rut']).first()
    if(user):

        expira = datetime.timedelta(minutes=1)
        access = create_access_token(identity=body, expires_delta=expira)

        return jsonify({
            "token":access
        })
    else:
        return "datos incorrectos"

@app.route('/private', methods=['GET']) #que persona pidio permiso para esta ruta privada
@jwt_required()
def privada():
    identidad = get_jwt_identity()
    return identidad

@app.route('/estudiante', methods=['GET'])
@jwt_required()
def estudiante():
    identidadCliente = get_jwt_identity()
    return identidadEstudiante


@app.route('/profesor', methods=['GET'])
def get_profesores():
        
        
    all_profesores = Profesor.query.all()

    all_profesores= list(map(lambda profesores: profesores.serialize() ,all_profesores))
   
    return jsonify(all_profesores),200
           
         
    #identidadCliente = get_jwt_identity()
    #return identidadProfesor

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
