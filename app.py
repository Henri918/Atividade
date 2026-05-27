from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="login"
)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    senha = request.form['senha']

    cursor = conexao.cursor()

    comando = "SELECT * FROM Usuarios WHERE email=%s AND senha=%s"
    valores = (email, senha)

    cursor.execute(comando, valores)

    usuario = cursor.fetchone()

    if usuario:
        return redirect('/dps')

    return "Email ou senha incorretos"

@app.route('/dps')
def cadastro():
    return render_template('dps.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():

    email = request.form['email']
    senha = request.form['senha']

    cursor = conexao.cursor()

    comando = """
    INSERT INTO Usuarios(email, senha)
    VALUES (%s,%s)
    """

    valores = (email, senha)

    cursor.execute(comando, valores)
    conexao.commit()

    return redirect('/antesdodps')

@app.route('/antesdodps')
def pag():
    return render_template('antesdodps.html')

app.run(debug=True)