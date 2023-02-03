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
from models import db, User, Ejercicio, Ficha 
# from models import Person
import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import chilean_rut
from sqlalchemy.dialects.postgresql import ENUM

app = Flask(__name__)
CORS(app)
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
def login():
    body = request.get_json()
    if "email" not in body:
        return {"msg":"falta ingresar tu email",
                "token":"",
                "status": 400}
    elif "password" not in body:
        return {"msg":"falta tu password",
                "token":"",
                "status": 400}
    else:
        user = User.query.filter_by(
        email=body['email'], password=body['password']).first()

    if (user):

        expira = datetime.timedelta(minutes=4320)
        access = create_access_token(identity=user.serialize(), expires_delta=expira)
        data = {
            "msg": "logeado",
            "token": access,
            "status": 200,
        }
        return jsonify(data),200

    else:
        return {"msg": "datos invalidos",
                "token":"",
                "status": 404}


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
         {"msg":"falta tu password",
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
            userid = User.query.filter_by( rut=body['rut']).first()

        expira = datetime.timedelta(minutes=4320)
        access = create_access_token(identity=userid.serialize(), expires_delta=expira)

        return jsonify({"msg": "Usuario registrado",
                        "token": access,
                        "status":200
                        })

@app.route('/token', methods=['POST'])
@jwt_required()
def token_validation():
    
    return jsonify({
        "msg":"token valido"
    })


# PRIVATE POR AHORA NO LO UTILIZAMOS
# @app.route('/private', methods=['GET']) #que persona pidio permiso para esta ruta privada
# @jwt_required()
# def privada():
#    identidad = get_jwt_identity()
#    return identidad

@app.route('/user', methods=['POST'])
@jwt_required()
def get_user():
     body = request.get_json()
     all = User.query.filter_by( rol=body['rol'])
    
     all = list(map(lambda user: user.serialize(), all))

     return jsonify({
         "user": all
     }), 200


@app.route('/register', methods=['GET'])
def get_user_register():

    all_Register = User.query.all()

    all_Register = list(
        map(lambda register: register.serialize(), all_Register))

    return jsonify({
        "user": all_Register
    }), 200


@app.route('/ficha', methods=['POST'])
@jwt_required()
def user_ficha():
    body = request.get_json()  
    user = User.query.filter_by(id=body["id_usuario"]).first()

    if (user):
        
        busqueda_ficha = Ficha.query.filter_by(id_usuario=body["id_usuario"]).first()
    
        if (busqueda_ficha):
           
            busqueda_ficha.peso = int(body['peso'])    
            busqueda_ficha.porcentaje_grasa = int(body['porcentaje_grasa'])
            busqueda_ficha.porcentaje_musculo = int(body['porcentaje_musculo'])
            busqueda_ficha.nivel = int(body['nivel'])
            busqueda_ficha.id_usuario = int(body['id_usuario'])
            
            db.session.commit()

            return jsonify({"msg": "ficha actualizada",
                             "status":200})
        else:
            ficha = Ficha() 
            ficha.peso = int(body['peso'])    
            ficha.porcentaje_grasa = int(body['porcentaje_grasa'])
            ficha.porcentaje_musculo = int(body['porcentaje_musculo'])
            ficha.nivel = int(body['nivel'])
            ficha.id_usuario = int(body['id_usuario'])

            db.session.add(ficha)
            db.session.commit()
            return jsonify({"msg": "ficha guardada",
                             "status":200})

                               
    else:
        return jsonify({
            "msj":"solicitud rechazada",
            "status":400
        })



    # ficha = Ficha()
    # ficha.peso = int(body['peso'])    
    # ficha.porcentaje_grasa = int(body['porcentaje_grasa'])
    # ficha.porcentaje_musculo = int(body['porcentaje_musculo'])
    # ficha.nivel = int(body['nivel'])
    # ficha.user_id = int(body['user_id'])

    # ficha = Ficha(peso=int(body['peso']), porcentaje_grasa=int(
    #     body['porcentaje_grasa']), porcentaje_musculo=int(body['porcentaje_musculo']), nivel=int(body['nivel']), user_id = int(body['user_id']))
    
    # db.session.add(ficha)
    # db.session.commit()

    # return {"msg": "ficha guardada"}, 200


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
        ['series']), repeticiones=int(['repeticiones']), peso=int(['peso']), nivel=int(['nivel']))
    
    db.session.add(ejercicio)
    db.session.commit()

    return {"msg": "Ejercicio guardado"}, 200


@app.route('/ficha/<int:userID>', methods=['GET'])
@jwt_required()
def get_ficha(userID):
    print(userID)
    ficha1 = Ficha.query.filter_by(
        id_usuario=userID).first()
    ficha= ficha1.serialize()
    print(ficha)
    if (ficha):  
        return jsonify({
        "msg":"tienes acceso a tu ficha",
        "status":200,
        "ficha": ficha
    }) 
    else:
        return jsonify({
        "msg":"no puedes acceder a id",
        "status":400,
        "ficha":"" 
        })

@app.route('/ejercicio', methods=['GET'])
def get_ejercicio():

    all_ejercicio = Ejercicio.query.all()

    all_ejercicio = list(
        map(lambda ejercicio: ejercicio.serialize(), all_ejercicio))

    return jsonify(all_ejercicio), 200



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
