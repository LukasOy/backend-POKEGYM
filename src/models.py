from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Profesor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=False, nullable=False)
    apellido = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    telefono = db.Column(db.Integer, unique=False, nullable=False)
    rut = db.Column(db.String(20), unique=True, nullable=False)
    rol_profesor = db.Column(db.Boolean(), unique=False, nullable=False) 

    def __repr__(self):
        return '<Profesor %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,   
            "apellido":self.apellido,       
            "email": self.email,
            "password": self.password,
            "telefono": self.telefono,
            "rut":self.rut,
            "rol_profesor":self.rol_profesor
            # do not serialize the password, its a security breach
        }


class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True, nullable=False)
    apellido = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    telefono = db.Column(db.Integer, unique=False, nullable=False)
    rut = db.Column(db.String(20), unique=False, nullable=False)
    comentario = db.Column(db.String(500), unique=True, nullable=False)
    id_profesor = db.Column(db.Integer, db.ForeignKey("profesor.id"))
    rel_p = db.relationship('Profesor')
  

    def __repr__(self):
        return '<Estudiante %r>' % self.email

    def serialize(self):
        return {
           "id": self.id,
            "nombre": self.nombre,
            "apellido": apellido.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "rut":self.telefono,
            "comentario":self.comentario,
            "idProfesor":self.id_profesor
            # do not serialize the password, its a security breach
        }

class Ejercicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_de_ejercicio = db.Column(db.String(120), unique=True, nullable=False)
    series = db.Column(db.String(80), unique=False, nullable=False)
    repeticiones = db.Column(db.String(20), unique=False, nullable=False)
    peso = db.Column(db.String(20), unique=False, nullable=False)
    descanso = db.Column(db.String(20), unique=False, nullable=False)
    id_estudiante = db.Column(db.Integer, db.ForeignKey ('estudiante.id'))
    id_profesor = db.Column(db.Integer, db.ForeignKey ('profesor.id'))
    rel_p = db.relationship('Profesor')
    rel_e= db.relationship('Estudiante')
    


    def __repr__(self):
        return '<Ejercicio %r>' % self.tipo_de_ejercicio

    def serialize(self):
        return {
            "id": self.id,
            "ejercicio" : self.tipo_de_ejercicio,
            "series" : self.series,
            "repeticiones" : self.repeticiones,
            "peso" : self.peso,
            "descanso" : self.descanso,
            "id_estudiante" : self.id_estudiante,
            "id_profesor" : self.id_profesor
            # do not serialize the password, its a security breach
        }

class Ficha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id'))
    peso = db.Column(db.Integer, unique=True, nullable=False)
    estatura = db.Column(db.Integer, unique=True, nullable=False)
    porcentaje_grasa = db.Column(db.Integer, unique=True, nullable=False)
    porcentaje_musculo = db.Column(db.Integer, unique=True, nullable=False)
    rel_e= db.relationship('Estudiante')
    
   
    
    def __repr__(self):
        return '<Ficha %r>' % self.id_estudiante

    def serialize(self):
        return {
            "id": self.id,
            "id_estudiante" : self.id_estudiante,
            "peso" : self.peso,
            "estatura" : self.estatura,
            "porcentaje_grasa" : self.porcentaje_grasa,
            "porcentaje_musculo" : self.porcentaje_musculo,

            # do not serialize the password, its a security breach
        }

class Reto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_profesor = db.Column(db.Integer, db.ForeignKey('profesor.id'))
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id'))
    ejercicio = db.Column(db.String(120), unique=True, nullable=False)
    rel_p = db.relationship('Profesor')
    rel_e= db.relationship('Estudiante')


    def __repr__(self):
        return '<Ficha %r>' % self.id_ejercicio

    def serialize(self):
        return {
            "id": self.id,
            "ejercicio": self.ejercicio
            # do not serialize the password, its a security breach
        }
