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
from models import db, User, Ejercicio, Ficha, Reto
# from models import Person
import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import chilean_rut
from sqlalchemy.dialects.postgresql import ENUM

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


@app.route('/login', methods=['POST'])
def loginprof():
    body = request.get_json()
    if "email" not in body:
        return "falta email", 400
    if "password" not in body:
        return "falta password", 400
#    if "rut" not in body:
#        return "falta rut"
#    if (chilean_rut.is_valid(body['rut'])==False):
#        return "falta rut"

    user = User.query.filter_by(
        email=body['email'], password=body['password']).first()

    if (user):

        expira = datetime.timedelta(minutes=3)
        access = create_access_token(identity=body, expires_delta=expira)
        data = {
            "user": user.serialize(),
            "token": access,
            "expires": expira.total_seconds(),
            "status": 200,
        }
        return (jsonify(data))

    else:
        return {"msg": "datos invalidos"}, 404


@app.route('/register', methods=['POST'])
def registerinfo():
    body = request.get_json()

    if "nombre" not in body:
        return {"msg":"falta ingresar tu nombre de usuario",
                "token":"",
                "status": 400}
    elif "email" not in body:
        return  {"msg":"falta ingresar tu email",
                "token":"",
                "status": 400}
    elif "password" not in body:
         {"msg":"falta tu",
                "token":"",
                "status": 400}
    elif "rut" not in body:
         {"msg":"falta ingresar tu rut",
                "token":"",
                "status": 400}
    elif "telefono" not in body:
         {"msg":"falta ingresar tu telefono",
                "token":"",
                "status": 400}
    elif (chilean_rut.is_valid(body['rut']) == False):
        return  {"msg":"rut no valido",
                "token":"",
                "status": 400}
    elif "rol" not in body:
        return  {"msg":"falta ingresar tu rol",
                "token":"",
                "status": 400}
    else:
        userdb = User.query.filter_by(nombre=body['nombre'], apellido=body['apellido'], email=body['email'],
                                      password=body['password'], telefono=body['telefono'], rut=body['rut'], rol=body['rol']).first()
        if (userdb):
            return {"msg": "el usuario ya existe",
                    "token": "",
                    "status": 400}
        usermail = User.query.filter_by( email=body['email']).first()
        if(usermail):
         return {"msg": "email ya registrado",
                    "token": "",
                    "status":400}
        userrut = User.query.filter_by( rut=body['rut']).first()
        if(userrut):
         return {"msg": "rut ya registrado",
                    "token": "",
                    "status":400}
        else:
            user = User()
            user.nombre = body["nombre"]
            user.apellido = body["apellido"]
            user.email = body["email"]
            user.password = body["password"]
            user.rut = body["rut"]
            user.telefono = body["telefono"]
            user.rol = body["rol"]
            db.session.add(user)
            db.session.commit()

        expira = datetime.timedelta(minutes=354353)
        access = create_access_token(identity=body, expires_delta=expira)

        return jsonify({"msg": "Usuario registrado",
                        "token": access,
                        "status":200
                        })


# PRIVATE POR AHORA NO LO UTILIZAMOS
# @app.route('/private', methods=['GET']) #que persona pidio permiso para esta ruta privada
# @jwt_required()
# def privada():
#    identidad = get_jwt_identity()
#    return identidad

@app.route('/login', methods=['GET'])
def get_user_login():
    all_Users = User.query.all()

    all_Users = list(map(lambda login: login.serialize(), all_Users))

    return jsonify({
        "user": all_Users[0]
    }), 200


@app.route('/register', methods=['GET'])
def get_user_register():

    all_Register = User.query.all()

    all_Register = list(
        map(lambda register: register.serialize(), all_Register))

    return jsonify({
        "user": all_Register[0]
    }), 200


@app.route('/ficha', methods=['POST'])
def ficha():
    body = request.get_json()

    ficha = Ficha()

    ficha.peso = int(body['peso'])
    ficha.porcentaje_grasa = int(body['porcentaje_grasa'])
    ficha.porcentaje_musculo = int(body['porcentaje_musculo'])
    ficha.nivel = int(body['nivel'])

    ficha = Ficha(peso=int(body['peso']), porcentaje_grasa=int(
        body['porcentaje_grasa']), porcentaje_musculo=int(body['porcentaje_musculo']), nivel=int(body['nivel']))
    db.session.add(ficha)
    db.session.commit()

    return {"msg": "ficha guardada"}, 200


@app.route('/reto', methods=['POST'])
def reto():
    body = request.get_json()

    reto = Reto()

    reto.ejercicio = body['ejercicio']

    reto = Reto(ejercicio=body['ejercicio'])
    db.session.add(reto)
    db.session.commit()

    return {"msg": "Reto guardado"}, 200


@app.route('/ejercicio', methods=['POST'])
def ejercicio():
    body = request.get_json()

    ejercicio = Ejercicio()

    ejercicio.tipo_de_ejercicio = body['tipo_de_ejercicio']
    ejercicio.series = int(body['series'])
    ejercicio.repeticiones = int(body['repeticiones'])
    ejercicio.peso = int(body['peso'])
    ejercicio.nivel = int(body['nivel'])

    ejercicio = Ejercicio(tipo_de_ejercicio=['tipo_de_ejercicio'], series=int(
        ['series']), repeticiones=int(['repeticiones']), peso=int(['peso']), nivel=int(body['nivel']))
    db.session.add(ejercicio)
    db.session.commit()

    return {"msg": "Ejercicio guardado"}, 200


@app.route('/ficha', methods=['GET'])
def get_ficha():

    all_fichas = Ficha.query.all()

    all_fichas = list(map(lambda fichas: fichas.serialize(), all_fichas))

    return jsonify(all_fichas), 200


@app.route('/ejercicio', methods=['GET'])
def get_ejercicio():

    all_ejercicio = Ejercicio.query.all()

    all_ejercicio = list(
        map(lambda ejercicio: ejercicio.serialize(), all_ejercicio))

    return jsonify(all_ejercicio), 200


@app.route('/reto', methods=['GET'])
def get_reto():

    all_reto = Reto.query.all()

    all_reto = list(map(lambda reto: reto.serialize(), all_reto))

    return jsonify(all_reto), 200

# @app.route('/nivel/<int:userID>', methods= ['PATCH'])
# def editar(userID):
#     body = request.get_json()

#     user= User.query.get(userID)
#     user.nivel = body['nivel']

#     return "nocachonada"


# id_profesor id_estudiante ejercicio

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
