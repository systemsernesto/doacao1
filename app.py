import os
import math
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}
"""
def get_coordinates(address):
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': address,
            'format': 'json',
            'limit': 1
        }
        # O User-Agent é obrigatório na API do Nominatim
        headers = {'User-Agent': 'DoacoesApp/1.0 (contato@doacoes.local)'}
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()  # Levanta exceção para códigos HTTP de erro
        data = response.json()
        
        # Verifica se há pelo menos um resultado
        if data and len(data) > 0:
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            print(f"Nenhum resultado encontrado para o endereço: {address}")
            return None, None
            
    except Exception as e:
        print(f"Erro ao geocodificar '{address}': {e}")
        return None, None

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        email = request.form['email']
        cpf = request.form['cpf']
        senha = request.form['senha']

        lat, lon = get_coordinates(endereco)
        hashed_senha = generate_password_hash(senha)

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO usuarios (nome, endereco, telefone, email, cpf, senha, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (nome, endereco, telefone, email, cpf, hashed_senha, lat, lon))
            conn.commit()
            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('login'))
        except Error as e:
            flash('Erro ao cadastrar. Verifique e-mail ou CPF duplicados.', 'danger')
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    return render_template('register_user.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user and check_password_hash(user['senha'], senha):
                session['user_id'] = user['id_usuario']
                session['user_name'] = user['nome']
                return redirect(url_for('register_org'))
            else:
                flash('E-mail ou senha inválidos.', 'danger')
        except Error as e:
            flash('Erro no login.', 'danger')
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/register_org', methods=['GET', 'POST'])
def register_org():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        url_doacao = request.form['url_doacao']
        cnpj = request.form['cnpj']

        lat, lon = get_coordinates(endereco)

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO instituicoes (nome, endereco, telefone, url_doacao, cnpj, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nome, endereco, telefone, url_doacao, cnpj, lat, lon))
            conn.commit()
            flash('Instituição cadastrada com sucesso!', 'success')
            return redirect(url_for('search'))
        except Error as e:
            flash('Erro ao cadastrar instituição. CNPJ pode estar duplicado.', 'danger')
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    return render_template('register_org.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    instituicoes = []
    user_lat, user_lon = None, None

    if request.method == 'POST':
        endereco = request.form['endereco']
        user_lat, user_lon = get_coordinates(endereco)
        if user_lat is None:
            flash('Endereço não encontrado. Tente novamente.', 'warning')
            return render_template('search.html')

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM instituicoes")
        instituicoes = cursor.fetchall()

        for inst in instituicoes:
            if user_lat is not None and inst['latitude'] is not None:
                dist = haversine(user_lat, user_lon, float(inst['latitude']), float(inst['longitude']))
                inst['distancia_km'] = round(dist, 2)
            else:
                inst['distancia_km'] = None

        instituicoes.sort(key=lambda x: x['distancia_km'] if x['distancia_km'] is not None else float('inf'))

    except Error as e:
        flash('Erro ao buscar instituições.', 'danger')
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    return render_template('search.html', instituicoes=instituicoes, user_lat=user_lat, user_lon=user_lon)

if __name__ == '__main__':
    app.run(debug=True)