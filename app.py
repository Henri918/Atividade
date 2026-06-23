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

    cursor.execute(
        "SELECT * FROM usuario WHERE email=%s AND senha=%s",
        (email,senha)
    )

    usuario = cursor.fetchone()

    print("Email:", email)
    print("Senha:", senha)
    print("Usuario encontrado:", usuario)

    if usuario:

        tipo = usuario[3]

        if tipo == "admin":
            return redirect('/adm')

        return redirect('/dps')

    return "Email ou senha incorretos"

@app.route('/cadastrarproduto', methods=['POST'])
def cadastrarproduto():

    nome = request.form['nome']
    categoria = request.form['categoria']
    quantidade = request.form['quantidade']

    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO produtos
        (nome,categoria,quantidade_estoque,estoque_minimo,preco)
        VALUES (%s,%s,%s,%s,%s)
        """,
        (nome,categoria,quantidade_estoque,0,0)
    )

    conexao.commit()

    return redirect('/adm')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():

        email = request.form['email']
        senha = request.form['senha']

        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO usuario (email, senha, tipo)
            VALUES (%s, %s, %s)
            """,
            (email, senha, 'usuario')
        )

        conexao.commit()

        return redirect('/dps')

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
@app.route('/retirar/<int:id>/<int:qtd>')
def retirar(id,qtd):

    cursor = conexao.cursor()

    cursor.execute(
        "SELECT quantidade FROM produtos WHERE id=%s",
        (id,)
    )

    resultado = cursor.fetchone()

    print("ID recebido:", id)
    print("Resultado:", resultado)

    if resultado is None:
        return "Produto não encontrado"

    atual = resultado[0]

    nova = atual - qtd

    cursor.execute(
        """
        UPDATE produtos
        SET quantidade=%s
        WHERE id=%s
        """,
        (nova,id)
    )

    conexao.commit()

    return redirect('/dps')

@app.route('/dps')
def dps():

    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM produtos"
    )

    produtos = cursor.fetchall()

    return render_template(
        'dps.html',
        produtos=produtos
    )

@app.route('/editarquantidade/<int:id>/<int:qtd>')
def editarquantidade(id,qtd):

    cursor = conexao.cursor() 

    cursor.execute(
        """
        UPDATE produtos
        SET quantidade=%s
        WHERE id=%s
        """,
        (qtd,id)
    )

    conexao.commit()

    return redirect('/adm')

@app.route('/deletar/<int:id>')
def deletar(id):

    cursor = conexao.cursor()

    cursor.execute(
        """
        DELETE FROM produtos
        WHERE id=%s
        """,
        (id,)
    )

    conexao.commit()

    return redirect('/adm')

app.run(debug=True)