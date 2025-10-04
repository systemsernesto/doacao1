from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os

app = Flask(__name__)

# Configurações do banco de dados
app.secret_key = 'your_secret_key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'doacoes_db'

mysql = MySQL(app)

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE email = %s AND senha = %s', (email, password))
        account = cursor.fetchone()
        
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['nome'] = account['nome']
            session['email'] = account['email']
            return redirect(url_for('busca_instituicoes'))
        else:
            return render_template('login.html', msg='Credenciais inválidas!')
    
    return render_template('login.html')

# Rota para cadastro de usuário
@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        email = request.form['email']
        cpf = request.form['cpf']
        senha = request.form['senha']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Verificar se o email já existe
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        account = cursor.fetchone()
        
        if account:
            return render_template('cadastro_usuario.html', msg='Email já cadastrado!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return render_template('cadastro_usuario.html', msg='Email inválido!')
        elif not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            return render_template('cadastro_usuario.html', msg='CPF inválido!')
        else:
            cursor.execute('INSERT INTO usuarios (nome, endereco, telefone, email, cpf, senha) VALUES (%s, %s, %s, %s, %s, %s)',
                           (nome, endereco, telefone, email, cpf, senha))
            mysql.connection.commit()
            return render_template('login.html', msg='Cadastro realizado com sucesso!')
    
    return render_template('cadastro_usuario.html')

# Rota para cadastro de instituição
@app.route('/cadastro_instituicao', methods=['GET', 'POST'])
def cadastro_instituicao():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        url_doacao = request.form['url_doacao']
        cnpj = request.form['cnpj']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO instituicoes (nome, endereco, telefone, url_doacao, cnpj) VALUES (%s, %s, %s, %s, %s)',
                       (nome, endereco, telefone, url_doacao, cnpj))
        mysql.connection.commit()
        return render_template('busca_instituicoes.html', msg='Instituição cadastrada com sucesso!')
    
    return render_template('cadastro_instituicao.html')

# Rota para busca de instituições
@app.route('/busca_instituicoes')
def busca_instituicoes():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM instituicoes')
    instituicoes = cursor.fetchall()
    
    return render_template('busca_instituicoes.html', instituicoes=instituicoes, usuario_nome=session['nome'])

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('nome', None)
    session.pop('email', None)
    return redirect(url_for('index'))

# Rota para API de busca de instituições próximas
@app.route('/api/instituicoes_proximas', methods=['GET'])
def instituicoes_proximas():
    if 'loggedin' not in session:
        return jsonify({'error': 'Acesso não autorizado'}), 401
    
    localizacao = request.args.get('localizacao', '')
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM instituicoes')
    instituicoes = cursor.fetchall()
    
    # Simular cálculo de distância
    for inst in instituicoes:
        inst['distancia'] = round(1 + (inst['id'] * 2.5), 1)  # Distância simulada
    
    return jsonify(instituicoes)

if __name__ == '__main__':
    app.run(debug=True)