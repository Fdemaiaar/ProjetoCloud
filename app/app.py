# app/app.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import numpy as np
import logging

# Configuração de Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurações do banco de dados e JWT
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Certifique-se de que esta chave esteja no .env

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Modelo de Usuário
class User(db.Model):
    __tablename__ = 'users'  # Nome da tabela
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.senha_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha_hash, password)

# Endpoint para registrar usuário
@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('senha'):
        logger.warning("Dados insuficientes para registro")
        return jsonify({'msg': 'Dados insuficientes'}), 400

    if User.query.filter_by(email=data['email']).first():
        logger.warning(f"E-mail já registrado: {data['email']}")
        return jsonify({'msg': 'E-mail já registrado'}), 409

    novo_usuario = User(
        nome=data.get('nome'),
        email=data['email']
    )
    novo_usuario.set_password(data['senha'])

    db.session.add(novo_usuario)
    db.session.commit()

    access_token = create_access_token(identity=novo_usuario.id)
    logger.info(f"Usuário registrado: {data['email']}")
    return jsonify({'jwt': access_token}), 201

# Endpoint para login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('senha'):
        logger.warning("Dados insuficientes para login")
        return jsonify({'msg': 'Dados insuficientes'}), 400

    usuario = User.query.filter_by(email=data['email']).first()

    if not usuario or not usuario.check_password(data['senha']):
        logger.warning(f"Credenciais inválidas para email: {data.get('email')}")
        return jsonify({'msg': 'Credenciais inválidas'}), 401

    access_token = create_access_token(identity=usuario.id)
    logger.info(f"Usuário autenticado: {data['email']}")
    return jsonify({'jwt': access_token}), 200

# Configuração do cliente Open-Meteo com cache e retry
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo_client = openmeteo_requests.Client(session=retry_session)

# Endpoint para consultar dados de temperatura
@app.route('/consultar', methods=['GET'])
@jwt_required()
def consultar():
    """
    Este endpoint retorna os dados de temperatura para uma localização especificada.
    Parâmetros de query:
        - latitude: Latitude da localização (obrigatório)
        - longitude: Longitude da localização (obrigatório)
    """
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    logger.info(f"Consulta de temperatura solicitada para latitude: {latitude}, longitude: {longitude}")

    if not latitude or not longitude:
        logger.warning("Parâmetros latitude e longitude são obrigatórios")
        return jsonify({'msg': 'Parâmetros latitude e longitude são obrigatórios'}), 400

    try:
        # Converter parâmetros para float
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        logger.warning("Parâmetros latitude e longitude devem ser números válidos")
        return jsonify({'msg': 'Parâmetros latitude e longitude devem ser números válidos'}), 400

    # Definir os parâmetros para a API Open-Meteo
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "timezone": "UTC"
    }

    try:
        # Fazer a requisição para a API Open-Meteo
        responses = openmeteo_client.weather_api(url, params=params)

        if not responses:
            logger.error("Nenhuma resposta recebida da API de clima")
            return jsonify({'msg': 'Nenhuma resposta recebida da API de clima'}), 500

        response = responses[0]

        # Verificar se os dados necessários estão presentes
        if not response.Hourly() or not response.Hourly().Variables():
            logger.error("Dados de temperatura não disponíveis na resposta da API")
            return jsonify({'msg': 'Dados de temperatura não disponíveis'}), 500

        # Extrair dados de temperatura
        hourly = response.Hourly()
        temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        times = pd.to_datetime(hourly.Time(), unit='s', utc=True)

        # Criar DataFrame
        hourly_data = {
            "date": times,
            "temperature_2m": temperature_2m
        }
        hourly_dataframe = pd.DataFrame(data=hourly_data)

        # Obter os últimos 10 registros
        hourly_dataframe = hourly_dataframe.tail(10)

        # Converter DataFrame para JSON ou CSV baseado no header 'Accept'
        accept_header = request.headers.get('Accept', 'application/json')
        if 'text/csv' in accept_header:
            # Converter para CSV
            csv_data = hourly_dataframe.to_csv(index=False)
            logger.info("Retornando dados em formato CSV")
            return (csv_data, 200, {
                'Content-Type': 'text/csv',
                'Content-Disposition': 'attachment; filename="temperatura.csv"'
            })
        else:
            # Retornar JSON por padrão
            # Converter datetime para string para serialização JSON
            hourly_dataframe['date'] = hourly_dataframe['date'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            logger.info("Retornando dados em formato JSON")
            return jsonify(hourly_dataframe.to_dict(orient='records')), 200

    except Exception as e:
        logger.error(f"Erro ao buscar dados de temperatura: {str(e)}")
        return jsonify({'msg': 'Erro ao buscar dados de temperatura', 'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8080)
