from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "senai2026"

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
        (email, senha)
    )

    usuario = cursor.fetchone()

    if usuario is None:
        return "Email ou senha incorretos"

    session['email'] = usuario[1]
    session['tipo'] = usuario[3]

    tipo = usuario[3]

    if tipo == 'admin':
        return redirect('/adm')

    return redirect('/dps')

@app.route('/cadastrarproduto', methods=['POST'])
def cadastrarproduto():

    nome = request.form['nome']
    categoria = request.form['categoria']
    quantidade = request.form['quantidade_estoque']
    foto2 = request.form['foto2']

    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO produtos
        (nome, categoria, quantidade_estoque, estoque_minimo, preco, foto2)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nome, categoria, quantidade, 0, 0, foto2))

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
    if 'tipo' not in session:
        return redirect('/')

    if session['tipo'] != 'admin':
        return redirect('/dps')

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
        "SELECT quantidade_estoque FROM produtos WHERE id=%s",
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
        SET quantidade_estoque=%s
        WHERE id=%s
        """,
        (nova,id)
    )

    conexao.commit()

    return redirect('/dps')

@app.route('/dps')
def dps():

    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM produtos")

    produtos = cursor.fetchall()

    print(produtos)   

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

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

@app.route('/usuarios')
def usuarios():

    if 'tipo' not in session:
        return redirect('/')

    if session['tipo'] != 'admin':
        return redirect('/dps')

    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM usuario")

    usuarios = cursor.fetchall()

    return render_template(
        'usuarios.html',
        usuarios=usuarios
    )

@app.route('/movimentacos')
def movimentacos():

    if 'tipo' not in session:
        return redirect('/')

    if session['tipo'] != 'admin':
        return redirect('/dps')

    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM usuario")

    moveimentacos = cursor.fetchall()

    return render_template(
        'movimentacos.html',
        movimentacos=movimentacos
    )
app.run(debug=True)