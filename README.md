# Projeto Cloud

**Autor: Felipe Maia**

Bem-vindo ao **Projeto Cloud**, uma API desenvolvida com o framework Flask em Python. Esta aplicação permite que os usuários realizem um registro em um banco de dados PostgreSQL, com autenticação segura utilizando JWT (JSON Web Tokens). A aplicação está totalmente dockerizada, facilitando sua implantação e gerenciamento em diferentes ambientes.

**PARA TESTAR VÁ DIRETO PARA: Como Executar a Aplicação**
http://a7756f3f934ce47d9b783c0b601c1774-2104210423.us-east-1.elb.amazonaws.com

## Índice
1. [Descrição do Projeto](#descrição-do-projeto)
2. [Funcionalidades](#funcionalidades)
3. [Pré-requisitos](#pré-requisitos)
4. [Instalação](#instalação)
5. [Configuração](#configuração)
6. [Como Executar a Aplicação](#como-executar-a-aplicação)
7. [Link do DockerHub do Projeto](#link-do-dockerhub-do-projeto)
8. [Link do Video demonstrativo](#link-do-video-demonstrativo)

## Descrição do Projeto

O **Projeto Cloud** é uma API robusta que oferece funcionalidades de gerenciamento de usuários e consulta de dados de temperatura em tempo real. As principais características incluem:

- **Autenticação de Usuários**: Registro, login e logout com segurança aprimorada utilizando JWT.
- **Integração com API Externa**: Consulta de dados de temperatura em tempo real através de uma API externa.
- **Dockerização Completa**: Facilita a implantação e escalabilidade da aplicação em diferentes ambientes.
- **Boas Práticas de Segurança**: Uso de variáveis de ambiente para gerenciamento de credenciais e proteção de rotas sensíveis.

## Funcionalidades

- **Registro de Usuários**: Permite que novos usuários se registrem fornecendo nome, email e senha.
- **Login de Usuários**: Autentica usuários registrados e gera tokens JWT para acesso seguro.
- **Consulta de Temperatura**: Fornece dados de temperatura, integrando-se com uma API externa para obter informações em tempo real.

## Pré-requisitos

Antes de começar, certifique-se de ter os seguintes itens instalados em seu ambiente:

- **Python 3.7 ou superior**
- **pip** (gerenciador de pacotes do Python)
- **Docker**: Para containerização da aplicação.
- **Docker Compose**: Para orquestrar os contêineres.
- **Git**: (Opcional, para clonar o repositório).

## Instalação

### 1. Clone o Repositório
```bash
git clone [(https://github.com/Fdemaiaar/ProjetoCloud.git)]
cd ProjetoCloud
```

### 2. Crie e Ative o Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Para Linux/Mac
venv\Scripts\activate  # Para Windows
```

### 3. Instale as Dependências
```bash
pip install -r app/requirements.txt
```

### 4. Configurar as Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
DATABASE_URL=postgresql://meuprojeto:S3cr3t@db:5432/superprojeto
JWT_SECRET_KEY=seu_segredo_jwt
FLASK_APP = run.py
FLASK_ENV=development
```

**Nota**: Se não criar o arquivo `.env`, os valores padrões definidos no `docker-compose.yaml` serão utilizados.

## Como Executar a Aplicação

### 1. Iniciar os Contêineres com Docker Compose
```bash
docker compose up --build
```

### 2. Verificar os Contêineres
```bash
docker compose ps
```

**Saída Esperada:**
```bash
NAME           SERVICE       STATUS     PORTS
app            app           Up         0.0.0.0:5000->5000/tcp
database       db            Up         0.0.0.0:5432->5432/tcp
```

### 3. Executar os comando abaixo para garantir as Migrações do Banco de Dados
```bash
docker compose exec app flask db upgrade
```

### 4. Testar os Endpoints da API

- **Registrar um Novo Usuário:**
```bash
curl -X POST http://localhost:5000/registrar -H "Content-Type: application/json" -d '{"nome":"Fulano","email":"fulano@example.com","senha":"senha123"}'
```

- **Fazer Login:**
```bash
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"email":"fulano@example.com","senha":"senha123"}'
```

- **Consultar Temperatura:**
```bash
curl -X GET http://localhost:5000/consultar_temperatura -H "Authorization: Bearer seu_token_jwt"
```


## Link do DockerHub do Projeto
[Clique aqui para acessar](https://hub.docker.com/repository/docker/fdemaiaar/cloud-felipe-maia/general)


## Link do Video demonstrativo
[Clique aqui para acessar](URL)
