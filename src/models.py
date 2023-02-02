from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ENUM

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=False, nullable=False)
    apellido = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    telefono = db.Column(db.String(20), unique=False, nullable=False)
    rut = db.Column(db.String(20), unique=True, nullable=False)
    rol = db.Column(db.Boolean(), unique=False, nullable=False) 

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,   
            "apellido":self.apellido,       
            "email": self.email,
            "password": self.password,
            "telefono": self.telefono,
            "rut":self.rut,
            "rol":self.rol
            # do not serialize the password, its a security breach
        } 
   

class Ejercicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_de_ejercicio = db.Column(db.String(120), unique=True, nullable=False)
    series = db.Column(db.Integer, unique=False, nullable=False)
    repeticiones = db.Column(db.Integer, unique=False, nullable=False)
    peso = db.Column(db.Integer, unique=False, nullable=False)
    nivel = db.Column(db.Integer, unique=True, nullable=False)


    def __repr__(self):
        return '<Ejercicio %r>' % self.tipo_de_ejercicio

    def serialize(self):
        return {
            "id": self.id,
            "tipo_de_ejercicio" : self.tipo_de_ejercicio,
            "series" : self.series,
            "repeticiones" : self.repeticiones,
            "peso" : self.peso,
            "nivel": self.nivel
            # do not serialize the password, its a security breach
        }

class Ficha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('user.id'))
    peso = db.Column(db.Integer, unique=True, nullable=False)
    porcentaje_grasa = db.Column(db.Integer, unique=True, nullable=False)
    porcentaje_musculo = db.Column(db.Integer, unique=True, nullable=False)
    nivel = db.Column(db.Integer, unique=True, nullable=False)
   
     
    def __repr__(self):
        return '<Ficha %r>' % self.id_usuario

    def serialize(self):
        return {
            "id": self.id,
            "id_usuario" : self.id_usuario,
            "peso" : self.peso,          
            "porcentaje_grasa" : self.porcentaje_grasa,
            "porcentaje_musculo" : self.porcentaje_musculo,
            "nivel": self.nivel

            # do not serialize the password, its a security breach
        }

