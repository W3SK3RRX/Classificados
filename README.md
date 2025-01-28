# Classificados Web

Este é um projeto de classificados online desenvolvido utilizando Django para o backend e Docker para orquestração dos containers. O sistema permite que profissionais e empresas anunciem seus serviços em uma plataforma de fácil acesso.

## Tecnologias Utilizadas

- **Backend**: Django (Django REST Framework)
- **Banco de Dados**: PostgreSQL
- **Orquestração de Containers**: Docker
- **Frontend**: React (caso aplicável)

## Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas em seu ambiente de desenvolvimento:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.12 ou superior](https://www.python.org/downloads/)
- [Pipenv ou Poetry](https://pipenv.pypa.io/en/latest/) (caso esteja usando um ambiente virtual)

## Como Executar o Projeto

Siga os passos abaixo para rodar o projeto em seu ambiente local:

### 1. **Clonar o Repositório**

Clone o repositório e acesse a pasta do projeto:

```bash
git clone https://github.com/seu_usuario/classificados.git
cd classificados
```

### 2. **Configuração do Docker**

O projeto utiliza o Docker e o Docker Compose para facilitar a execução dos containers. Para rodar o projeto no Docker, basta usar o comando:

```bash
docker-compose up -d
```

Esse comando irá:

Criar os containers para o banco de dados (PostgreSQL) e o backend (Django).

Rodar o servidor Django no container classificados-web e o banco de dados no container classificados-db.

### 3. **Acessar o Container do Django**

Depois que os containers estiverem em execução, entre no container do Django para rodar as migrações e comandos do Django:

```bash
docker exec -it classificados-classificados-web-1
```

### 4. **Executar as Migrações do Banco de Dados**

Dentro do container, execute as migrações para configurar o banco de dados:

```bash
python manage.py migrate
````

### 5. **Criar um Superusuário (opcional)**

Para acessar o admin do Django, você pode criar um superusuário com o comando:

```bash
python manage.py createsuperuser
```

### 6. **Rodar o Servidor de Desenvolvimento**

O servidor do Django já estará sendo executado dentro do container na porta 8000. Você pode acessá-lo no navegador usando o seguinte endereço:

```bash
http://localhost:8000
```

Caso precise rodar o servidor manualmente (caso tenha feito alterações), execute o comando:

```bash
python manage.py runserver 0.0.0.0:8000
```

### 7. **Verificar Logs do Docker (opcional)**

Se você deseja acompanhar os logs do seu container para verificar a execução, use o comando:

```bash
docker logs -f classificados-classificados-web-1
```

Isso exibirá os logs do container do Django em tempo real.

### 8. **Variáveis de Ambiente**

As variáveis de ambiente são configuradas através do arquivo .env. Certifique-se de que as seguintes variáveis estejam configuradas corretamente:

```bash
.env
# Django Settings
SECRET_KEY=django-insecure-necfb3tggkjed^4j7wn@rhmn2375$h7r^wv(tg7xpux5d71%co
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database
DB_NAME=Classificados
DB_USER=Classificados_user
DB_PASSWORD=T4Mhj,pyEt*$Q.tl
DB_HOST=classificados-db
DB_PORT=5432

# D4Sign API (se aplicável)
D4SIGN_API_URL=https://sandbox.d4sign.com.br/api/v1
D4SIGN_API_KEY=sua_api_key_aqui
D4SIGN_CRYPTO_KEY=sua_crypto_key_aqui
```

### 9. **Comandos Úteis**

Verificar o status do banco de dados (PostgreSQL):

```bash
docker-compose logs classificados-db
```

Parar e remover os containers:
```bash
docker-compose down
```

Reiniciar o projeto (containers e volumes):

```bash
docker-compose down -v
docker-compose up -d
```

### 10. **Contribuindo**

Contribuições são sempre bem-vindas! Para contribuir com o projeto:

Faça um fork do repositório.
Crie uma nova branch (git checkout -b feature/nome-da-sua-feature).
Faça as alterações necessárias.
Faça o commit das suas alterações (git commit -am 'Adiciona nova feature').
Envie para o seu repositório (git push origin feature/nome-da-sua-feature).
Abra um Pull Request para o repositório original.


### 11. **Licença**

Este projeto está licenciado sob a Licença MIT.
