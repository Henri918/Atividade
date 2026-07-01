from flask import Flask, render_template, request, redirect, session
import mysql.connector
import bcrypt

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
        """
        SELECT * FROM usuario
        WHERE email=%s
        """,
        (email,)
    )

    usuario = cursor.fetchone()

    if usuario is None:
        return "Email ou senha incorretos"

    senha_hash = usuario[2]

    if not bcrypt.checkpw(
        senha.encode('utf-8'),
        senha_hash.encode('utf-8')
    ):
        return "Email ou senha incorretos"

    session['email'] = usuario[1]
    session['tipo'] = usuario[3]

    if usuario[3] == "admin":
        return redirect('/adm')

    return redirect('/dps')

@app.route('/cadastrarproduto', methods=['POST'])
def cadastrarproduto():

    nome = request.form['nome']
    categoria = request.form['categoria']
    quantidade = request.form['quantidade']
    foto2 = request.form['foto2']

    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO produtos
        (nome, categoria, quantidade, estoque_minimo, preco, foto2)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nome, categoria, quantidade, 0, 0, foto2))

    cursor.execute(
    """
    INSERT INTO movimentacoes
    (produto_id, produto, tipo, quantidade, usuario)
    VALUES (%s,%s,%s,%s,%s)
    """,
    (
        cursor.lastrowid,
        nome,
        "Entrada",
        quantidade,
        session['email']
    )
    )

    conexao.commit()

    return redirect('/adm')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():

    email = request.form['email']
    senha = request.form['senha']

    senha_hash = bcrypt.hashpw(
        senha.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO usuario(email, senha, tipo)
        VALUES (%s,%s,%s)
        """,
        (email, senha_hash, "usuario")
    )

    conexao.commit()

    return redirect('/')

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
def retirar(id, qtd):

    if 'email' not in session:
        return redirect('/')

    cursor = conexao.cursor()

 
    cursor.execute(
    """
    SELECT nome, quantidade
    FROM produtos
    WHERE id=%s
    """,
    (id,)
    )
    resultado = cursor.fetchone()

    if resultado is None:
        cursor.close()
        return "Produto não encontrado"

    produto_nome = resultado[0]
    quantidade_atual = resultado[1]


    if qtd > quantidade_atual:
        cursor.close()
        return "Quantidade indisponível no estoque"

    nova_quantidade = quantidade_atual - qtd

    cursor.execute(
    """
    UPDATE produtos
    SET quantidade=%s
    WHERE id=%s
    """,
    (nova_quantidade, id)
    )
    cursor.execute(
        """
        INSERT INTO movimentacoes
        (produto_id, produto, tipo, quantidade, usuario)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            id,
            produto_nome,
            "Retirada",
            qtd,
            session['email']
        )
    )

    conexao.commit()
    cursor.close()

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

    cursor.execute(
    "SELECT nome FROM produtos WHERE id=%s",
    (id,)
)

    produto = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO movimentacoes
        (produto_id, produto, tipo, quantidade, usuario)
        VALUES (%s,%s,%s,%s,%s)
        """,
        (
            id,
            produto,
            "Edição",
            qtd,
            session['email']
        )
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


@app.route('/movimentacos')
def movimentacos():

    if 'tipo' not in session:
        return redirect('/')

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM movimentacoes
        ORDER BY data_hora DESC
    """)

    movimentacoes = cursor.fetchall()

    return render_template(
        "movimentacos.html",
        movimentacoes=movimentacoes
    )

@app.route('/usuarios')
def usuarios():

    if 'tipo' not in session:
        return redirect('/')

    if session['tipo'] != 'admin':
        return redirect('/dps')

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id,email,tipo
        FROM usuario
    """)

    usuarios = cursor.fetchall()

    return render_template(
        "usuarios.html",
        usuarios=usuarios
    )

@app.route('/cadastrarusuario', methods=['POST'])
def cadastrarusuario():

    email = request.form['email']
    senha = request.form['senha']
    senha_hash = bcrypt.hashpw(
        senha.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    tipo = request.form['tipo']

    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO usuario(email, senha, tipo)
        VALUES (%s,%s,%s)
        """,
        (email, senha_hash, tipo)
    )

    conexao.commit()

    return redirect('/usuarios')

app.run(debug=True)