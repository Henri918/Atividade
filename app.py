from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="usuarios"
)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    senha = request.form['senha']

    cursor = conexao.cursor()

    comando = """
    SELECT *
    FROM Usuarios
    WHERE email=%s
    AND senha=%s
    """

    cursor.execute(comando,(email,senha))

    usuario = cursor.fetchone()

    if usuario:

        tipo = usuario[3]

        if tipo == "admin":
            return redirect('/adm')

        else:
            return redirect('/dps')

    return "Email ou senha incorretos"

@app.route('/dps')
def cadastro():
    return render_template('dps.html')

@app.route('/login', methods=['POST'])
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

@app.route('/adm')
def adm():

    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM produtos"
    )

    produtos = cursor.fetchall()

    return render_template(
        'adm.html',
        produtos=produtos
    )
@app.route('/cadastrarproduto', methods=['POST'])
def cadastrarproduto():

    produto = request.form['produto']
    categoria = request.form['categoria']
    quantidade = request.form['quantidade']

    cursor = conexao.cursor()

    comando = """
    INSERT INTO produtos(
        produto,
        categoria,
        quantidade
    )
    VALUES(%s,%s,%s)
    """

    cursor.execute(
        comando,
        (produto,categoria,quantidade)
    )

    conexao.commit()

    return redirect('/adm')

app.run(debug=True)