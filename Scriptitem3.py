import hashlib
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()
        
with app.app_context():
    db.create_all()

    integrantes = [
        {"username": "PedroCharalamby", "password": "ped123"},
        {"username": "AlvaroOrmazabal", "password": "alv123"},
        {"username": "KevinTapia", "password": "kev123"},
        {"username": "CamiloMundaca", "password": "cam123"},
        # Agrega los nombres de usuario y contraseñas de los integrantes restantes
    ]

    for integrante in integrantes:
        user = User(integrante["username"], integrante["password"])
        db.session.add(user)

    db.session.commit()

@app.route('/')
def home():
    return "Sitio web creado correctamente"

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = hashlib.sha256(request.form['password'].encode()).hexdigest()

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return "Inicio de sesión exitoso"
    else:
        return "Nombre de usuario o contraseña incorrectos"

if __name__ == '__main__':
    app.run(port=4850)
