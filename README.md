# **Projeto Cloud**

**Autor: Felipe Maia**

Bem-vindo ao **Projeto Cloud**, uma API desenvolvida com o framework Flask em Python. Esta aplicação permite que os usuários realizem operações de registro e autenticação com JWT, além de consultar dados de temperatura de São Paulo em tempo real. A aplicação está totalmente dockerizada e pronta para ser implantada em Kubernetes.

**Acesse a Aplicação:**  
[**http://a7756f3f934ce47d9b783c0b601c1774-2104210423.us-east-1.elb.amazonaws.com**](http://a7756f3f934ce47d9b783c0b601c1774-2104210423.us-east-1.elb.amazonaws.com)  

**Vídeo Demonstrativo:**  
[**https://youtu.be/uopwnFodgPs**](https://youtu.be/uopwnFodgPs)

---

## **Índice**

1. [Descrição do Projeto](#descrição-do-projeto)  
2. [Funcionalidades](#funcionalidades)  
3. [Estrutura do Projeto](#estrutura-do-projeto)  
4. [Pré-requisitos](#pré-requisitos)  
5. [Instalação e Execução](#instalação-e-execução)  
6. [Testando a Aplicação](#testando-a-aplicação)  
7. [Publicação no Docker Hub](#publicação-no-docker-hub)  
8. [Link do Vídeo Demonstrativo](#link-do-vídeo-demonstrativo)  

---

## **Descrição do Projeto**

O **Projeto Cloud** é uma aplicação desenvolvida para demonstrar funcionalidades básicas de autenticação e consulta de dados externos. Ele combina a simplicidade de Flask com a robustez do PostgreSQL, sendo capaz de:

- Gerenciar usuários com segurança.
- Fornecer informações de temperatura de São Paulo utilizando integração com API externa.
- Ser implantado em contêineres Docker e gerenciado com Kubernetes.

---

## **Funcionalidades**

- **Registro de Usuários**: Cadastro seguro de usuários no banco de dados.
- **Login com JWT**: Geração de tokens para autenticação.
- **Consulta de Temperatura**: Integração com API para obter temperatura de São Paulo.
- **Totalmente Dockerizado**: Configuração pronta para execução em contêineres.

---

## **Estrutura do Projeto**

```plaintext
ProjetoCloud/
├── app/
│   ├── Dockerfile
│   ├── __init__.py
│   ├── models.py
│   ├── run.py
│   ├── routes.py
│   ├── requirements.txt
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── style.css
│       └── script.js
├── migrations/
│   ├── ...
├── compose.yaml
├── README.md

```

**Diretórios principais:**

- **app/**: Contém o código da aplicação (Flask).  
- **migrations/**: Scripts de migração gerados pelo Flask-Migrate.  
- **compose.yaml**: Arquivo Docker Compose para orquestração local.  
- **run.py**: Arquivo principal que inicializa a aplicação.  

---

## **Pré-requisitos**

Certifique-se de ter as seguintes ferramentas instaladas:

- **Docker**  
- **Docker Compose**  
- **Python 3.7+**  

---

## **Instalação e Execução**

### **1. Executar Localmente com Docker Compose**

1. Clone o repositório:

   ```bash
   git clone https://github.com/Fdemaiaar/ProjetoCloud.git
   cd ProjetoCloud
   ```

2. Inicie os contêineres:

   ```bash
   docker compose up --build
   ```

3. Acesse a aplicação em:  
   [http://localhost:5000](http://localhost:5000)

4. Execute migrações:

   ```bash
   docker compose exec app flask db upgrade
   ```

---

## **Testando a Aplicação**

### **Endpoints Disponíveis**

1. **Registro de Usuário**
   - **Método:** `POST`  
   - **URL:** `/registrar`  
   - **Body:**
     ```json
     {
         "nome": "Fulano",
         "email": "fulano@gmail.com",
         "senha": "senha"
     }
     ```

2. **Login**
   - **Método:** `POST`  
   - **URL:** `/login`  
   - **Body:**
     ```json
     {
         "email": "fulano@gmail.com",
         "senha": "senha"
     }
     ```

3. **Consulta de Temperatura**
   - **Método:** `GET`  
   - **URL:** `/consultar`  
   - **Headers:**  
     `Authorization: Bearer <seu_token_jwt>`  

---

## **Publicação no Docker Hub**

A imagem da aplicação foi publicada no Docker Hub:  
[**https://hub.docker.com/repository/docker/fdemaiaar/cloud-felipe-maia**](https://hub.docker.com/repository/docker/fdemaiaar/cloud-felipe-maia)

Para atualizar a imagem no Docker Hub:

1. Gere uma nova imagem:
   ```bash
   docker build -t fdemaiaar/cloud-felipe-maia:latest .
   ```

2. Faça login no Docker Hub:
   ```bash
   docker login
   ```

3. Envie a imagem:
   ```bash
   docker push fdemaiaar/cloud-felipe-maia:latest
   ```

---

## **Link do Vídeo Demonstrativo**

Assista ao vídeo demonstrativo do projeto:  
[**https://youtu.be/uopwnFodgPs**](https://youtu.be/uopwnFodgPs)

---

Kubernetes: Para este projeto, os arquivos YAML de configuração para o Kubernetes foram criados, permitindo implantação em AWS EKS, mas **não estão incluídos no repositório do GitHub**.
