from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Profesor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True, nullable=False)
    apellido = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    segundopassword = db.Column(db.String(80), unique=False, nullable=False)
    telefono = db.Column(db.Integer, unique=False, nullable=False)
    rut = db.Column(db.String(20), unique=False, nullable=False)
    rol = db.Column(db.Boolean(), unique=False, nullable=False)


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True, nullable=False)
    apellido = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    segundopassword = db.Column(db.String(80), unique=False, nullable=False)
    telefono = db.Column(db.Integer, unique=False, nullable=False)
    rut = db.Column(db.String(20), unique=False, nullable=False)
    rol = db.Column(db.Boolean(), unique=True, nullable=True)


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Ejercicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_de_ejercicio = db.Column(db.String(120), unique=True, nullable=False)
    series = db.Column(db.String(80), unique=False, nullable=False)
    repeticiones = db.Column(db.String(20), unique=False, nullable=False)
    peso = db.Column(db.String(20), unique=False, nullable=False)
    descanso = db.Column(db.String(20), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    id_cliente = db.Column(db.Integer, primary_key=True)
    id_profesor = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Ficha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('Estudiantes.id'))
    peso = db.Column(interger(120), unique=True, nullable=False)
    estatura = db.Column(interger(120), unique=True, nullable=False)
    porcentaje_grasa = db.Column(interger(120), unique=True, nullable=False)
    porcentaje_musculo = db.Column(interger(120), unique=True, nullable=False)
   


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
