
# Projeto Cloud

## Nome do Aluno
**Felipe Maia**

## Explicação do Projeto
Este projeto consiste em uma API desenvolvida com Flask que permite realizar operações de CRUD (Create, Read, Update, Delete) em um banco de dados PostgreSQL. A API inclui funcionalidades de autenticação utilizando JWT (JSON Web Tokens) para garantir a segurança dos endpoints. Além disso, a aplicação está totalmente dockerizada, facilitando sua implantação e gerenciamento em diferentes ambientes.

### Funcionalidades Implementadas:
- **Registro de Usuários:** Permite que novos usuários se registrem fornecendo nome, email e senha.
- **Login de Usuários:** Autentica usuários registrados e gera tokens JWT para acesso seguro.
- **Consulta de Temperatura:** Fornece dados de temperatura, integrando-se com uma API externa para obter informações em tempo real.
- **Autenticação e Autorização:** Protege rotas sensíveis, garantindo que apenas usuários autenticados possam acessá-las.
- **Dockerização:** A aplicação está containerizada utilizando Docker, facilitando o deployment e a escalabilidade.
- **Gerenciamento de Migrações:** Utiliza Flask-Migrate para gerenciar mudanças no banco de dados de forma eficiente.

## Estrutura do Projeto
📁 app  
├── 📄 Dockerfile  
├── 📄 run.py  
├── 📄 requirements.txt  
├── 📄 init.py  
├── 📄 models.py  
├── 📄 routes.py  
├── 📄 entrypoint.sh  
└── 📄 migrations/  
📄 docker-compose.yaml  
📄 .env  
📄 README.md  

## Como Executar a Aplicação

### Pré-requisitos
- Docker instalado na máquina
- Conta no Docker Hub

### Passo a Passo

1. **Clonar o Repositório:**
   ```bash
   git clone https://github.com/seu_usuario/seu_repositorio.git
   cd seu_repositorio
   ```

2. **Configurar as Variáveis de Ambiente:**

Opcionalmente, crie um arquivo .env com as seguintes variáveis:

```makefile
POSTGRES_DB=superprojeto
POSTGRES_USER=meuprojeto
POSTGRES_PASSWORD=S3cr3t
DATABASE_URL=postgresql://meuprojeto:S3cr3t@db:5432/superprojeto
JWT_SECRET_KEY=seu_segredo_jwt
OPENWEATHERMAP_API_KEY=sua_api_key  # Se aplicável
```

Nota: Se não criar o arquivo .env, os valores padrões definidos no docker-compose.yaml serão utilizados.

3. **Executar a Aplicação com Docker Compose:**

```bash
docker-compose up -d
```

4. **Verificar os Contêineres:**

```bash
docker-compose ps
```

Saída Esperada:

```bash
NAME           SERVICE       STATUS     PORTS
app            app           Up         0.0.0.0:5000->5000/tcp
database       db            Up         0.0.0.0:5432->5432/tcp
```

5. **Testar os Endpoints da API:**

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

## Documentação dos Endpoints da API

### 1. Registrar um Novo Usuário
- **URL:** `/registrar`
- **Método:** POST
- **Payload:**
```json
{
    "nome": "Fulano",
    "email": "fulano@example.com",
    "senha": "senha123"
}
```
- **Resposta:**
```json
{
    "jwt": "seu_token_jwt"
}
```

### 2. Fazer Login
- **URL:** `/login`
- **Método:** POST
- **Payload:**
```json
{
    "email": "fulano@example.com",
    "senha": "senha123"
}
```
- **Resposta:**
```json
{
    "jwt": "seu_token_jwt"
}
```

### 3. Consultar Temperatura
- **URL:** `/consultar_temperatura`
- **Método:** GET
- **Headers:**
```makefile
Authorization: Bearer seu_token_jwt
```
- **Resposta:**
```json
{
    "temperatura": "25°C"
}
```

## Considerações Finais
- **Segurança:** As credenciais sensíveis são gerenciadas através de variáveis de ambiente, garantindo que não sejam expostas no código ou no repositório.
- **Dockerização Completa:** A aplicação está totalmente dockerizada e pode ser executada facilmente em qualquer ambiente que suporte Docker.
- **Documentação Completa:** Este README fornece todas as informações necessárias para entender, executar e testar a aplicação.
