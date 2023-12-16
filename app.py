from flask import Flask, render_template, redirect, request, session, jsonify, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/proyecto"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.secret_key = "password1234"
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    password = request.form['password']

    usuario_db = Usuario.query.filter_by(usuario=usuario).first()

    if usuario_db and usuario_db.password == password:
        session['logueado'] = True
        session['id'] = usuario_db.id
        session['usuario'] = usuario
        return redirect(url_for('ver'))
    else:
        return render_template('index.html')

@app.route('/ver')
def ver():
    if "logueado" in session and session["logueado"]:
        user_id = session.get("id")
        if user_id is not None:
            usuario = Usuario.query.get(user_id).usuario
            return redirect(url_for('lista', usuario=usuario))

    return render_template('lista')

@app.route('/registros')
def registro():
    return render_template('registros.html')

@app.route('/crear-registro', methods=["POST"])
def crear_registro():
    usuario = request.form['usuario']
    password = request.form['password']

    try:
        nuevo_usuario = Usuario(usuario=usuario, password=password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error al insertar en la base de datos: {e}")
        return render_template("index.html")

@app.route('/lista')
def lista():
    return render_template('listar_usuarios.html')

@app.route('/listar_usuarios', methods=["GET"])
def listar_usuarios():
    usuarios = Usuario.query.all()
    users_json = [{"id": user.id, "usuario": user.usuario} for user in usuarios]
    return jsonify(users_json)
    
@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')






if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=False, port=5000, threaded=True)

    
    


