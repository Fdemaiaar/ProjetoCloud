# app/routes.py

from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from .models import User
from . import db
import logging
import requests
import openmeteo_requests
from retry_requests import retry
import requests_cache

main = Blueprint('main', __name__)

# Configuração de Logging
logger = logging.getLogger(__name__)

# Configuração do cliente Open-Meteo com cache e retry
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo_client = openmeteo_requests.Client(session=retry_session)

# Rotas e lógica da aplicação

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/registrar', methods=['POST'])
def registrar():
    try:
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
    except Exception as e:
        logger.error(f"Erro no registro: {str(e)}")
        return jsonify({'msg': 'Erro interno no servidor'}), 500

@main.route('/login', methods=['POST'])
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

@main.route('/consultar_temperatura')
@jwt_required()
def consultar_temperatura():
    return render_template('consultar.html')

@main.route('/consultar', methods=['GET'])
@jwt_required()
def consultar():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    logger.info(f"Consulta de temperatura solicitada para latitude: {latitude}, longitude: {longitude}")

    if not latitude or not longitude:
        logger.warning("Parâmetros latitude e longitude são obrigatórios")
        return jsonify({'msg': 'Parâmetros latitude e longitude são obrigatórios'}), 400

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        logger.warning("Parâmetros latitude e longitude devem ser números válidos")
        return jsonify({'msg': 'Parâmetros latitude e longitude devem ser números válidos'}), 400

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "timezone": "UTC"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        times = data['hourly']['time']
        temperatures = data['hourly']['temperature_2m']

        resultados = []
        for time, temp in zip(times, temperatures):
            resultados.append({
                'date': time,  # Já no formato ISO 8601
                'temperature_2m': temp
            })

        resultados = resultados[-10:]

        logger.info("Retornando dados de temperatura")
        return jsonify(resultados), 200

    except Exception as e:
        logger.error(f"Erro ao buscar dados de temperatura: {str(e)}")
        return jsonify({'msg': 'Erro ao buscar dados de temperatura', 'error': str(e)}), 500

# Tratadores de erro
@main.app_errorhandler(400)
def bad_request(e):
    return jsonify({'msg': 'Bad Request'}), 400

@main.app_errorhandler(404)
def not_found(e):
    return jsonify({'msg': 'Not Found'}), 404

@main.app_errorhandler(500)
def internal_error(e):
    return jsonify({'msg': 'Internal Server Error'}), 500
