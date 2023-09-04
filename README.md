# README

## Desafio Técnico Python - MAISTODOS LTDA

### Introdução

Este repositório contém o código-fonte de uma API REST para cadastro de cartões de crédito. A API foi desenvolvida usando o framework Django e o Django Rest Framework. O banco de dados usado é o PostgreSQL. O projeto inclui um arquivo `docker-compose.yaml` para facilitar a execução do projeto em diferentes ambientes. O projeto também inclui um arquivo `Pipfile` para gerenciamento de dependências usando o Pipenv.

### Requisitos

- O código deve estar em inglês.
- Utilizar Git e instalar os Git Hooks com `pre-commit install`.
- Fazer micro commits.
- Documentar detalhadamente quaisquer referências/ferramentas pesquisadas.
- Criar um repositório público e compartilhar o link para acompanhamento do desenvolvimento.
- Implementar testes automatizados (unitários e de integração).

### Configuração Inicial

1. Clone o repositório.
2. Copie o arquivo `.env.example` e renomeie a cópia para `.env`.
3. Instale os Git Hooks:

   ```
   pre-commit install
   ```

## Executando via Docker

Se você não tem o Docker ou o Docker Compose instalados, siga os guias oficiais para instalação:

- [Instalar Docker](https://docs.docker.com/get-docker/)
- [Instalar Docker Compose](https://docs.docker.com/compose/install/)

Depois de instalados, você pode usar os comandos abaixo para construir e executar o projeto.

### Construindo a Imagem

Para construir a imagem Docker do projeto:

```bash
docker-compose build
```

### Iniciando os Serviços

Para iniciar os serviços definidos no `docker-compose.yaml`:

```bash
docker-compose up
```

### Parando os Serviços

Para parar os serviços:

```bash
docker-compose down
```

### Acessando o Container

Se você precisar acessar o container diretamente para executar comandos ou inspecionar algo, use:

```bash
docker exec -it maistodos_creditcard_backend_web-1 /bin/bash
```

Este comando abre um shell Bash no container `maistodos_creditcard_backend_web_1`, permitindo que você interaja diretamente com o ambiente do container. Para sair do shell, digite `exit`. Note que o nome do container pode ser diferente, dependendo do seu sistema operacional.

### Executando Localmente

Se preferir executar o projeto localmente:

1. Instale o Pipenv:

   ```
   pip install pipenv
   ```

2. Instale as dependências de desenvolvimento:

   ```
   pipenv install --dev
   ```

3. Instale o PostgreSQL e configure-o de acordo com as instruções do seu sistema operacional.
4. Ative o ambiente virtual:

   ```
   pipenv shell
   ```

5. Execute as migrações:

   ```
   python manage.py migrate
   ```

6. Inicie o servidor:

   ```
   python manage.py runserver
   ```

### IMPORTANTE - Criação das Tabelas de Autenticação

Para que o sistema funcione corretamente, é necessário criar as tabelas de autenticação do Django. Para isso, execute o comando abaixo:

```
python manage.py migrate authtoken
```

Você só precisa executar este comando uma vez, e este passo precisa ser executado tanto na versão Docker quanto na versão local.

### Endpoints da API

#### Cartões de Crédito

- `GET /api/creditcards/` - Listar os cartões de crédito.
- `GET /api/creditcards/<pk>/` - Detalhe do cartão de crédito.
- `POST /api/creditcards/` - Cadastrar um novo cartão de crédito.
- `GET /api/creditcards/<pk>.<format>/` - Detalhe do cartão de crédito com formato específico.
- `GET /api/creditcards/.<format>/` - Listar os cartões de crédito com formato específico.

#### Usuários

- `POST /api/users/create/` - Criar um novo usuário.
- `GET /api/users/me/` - Obter informações do usuário autenticado.
- `POST /api/users/token/` - Obter token para autenticação.

#### Documentação

- `GET /api/docs/` - Documentação Swagger da API, incluindo exemplos de requisições.
- `GET /api/schema/` - Esquema da API.

### Autenticação

O acesso à API é aberto ao mundo, mas requer autenticação e autorização, que é feita usando o pacote authtoken do Django Rest Framework. Para obter um token, faça uma requisição POST para `/api/users/token/` com o email e a senha do usuário. O token será retornado no corpo da resposta. Para usar o token, inclua-o no cabeçalho `Authorization` da requisição, precedido pela palavra `Token` e um espaço em branco. Por exemplo:

```http
curl -X 'GET' \
  'http://localhost:8000/api/creditcards/' \
  -H 'accept: application/json' \
  -H 'Authorization: Token 9fad7d50928868c40315a215f3'
```

### Fluxo da Aplicação

O fluxo da aplicação é o seguinte:

1. O usuário cria uma conta usando o endpoint `/api/users/create/`.
2. O usuário obtém um token de autenticação usando o endpoint `/api/users/token/`.
3. O usuário usa o token para acessar os endpoints protegidos da API.
4. O usuário cadastra um cartão de crédito usando o endpoint `/api/creditcards/`.
5. O usuário obtém os detalhes do cartão de crédito usando o endpoint `/api/creditcards/<pk>/`.
6. O usuário obtém uma lista de cartões de crédito usando o endpoint `/api/creditcards/`.

### Validações de Campos

O sistema realiza várias validações para garantir a qualidade dos dados. Abaixo estão as validações detalhadas:

#### Data de Expiração (`exp_date`)

- O formato deve ser MM/YYYY.
- A data não pode ser anterior à data atual.
- O ano da data de expiração deve ser no máximo 10 anos à frente do ano atual.
- O mês deve ser um valor entre 01 e 12.
- O ano deve ter 4 dígitos e o mês 2 dígitos.

#### CVV

- Deve ser numérico.
- Deve ter entre 3 e 4 dígitos.

#### Número do Cartão (`number`)

- Deve ser numérico.
- Deve ter entre 13 e 16 dígitos.
- O número do cartão deve ser válido de acordo com a biblioteca `creditcard`.
- O número do cartão deve ser criptografado antes de ser persistido.

#### Nome do Titular (`holder`)

- Deve ter pelo menos 2 caracteres.

#### Bandeira do Cartão (`brand`)

- A bandeira do cartão é determinada automaticamente usando a biblioteca `creditcard`.
- Se a bandeira não for suportada ou não puder ser determinada, uma exceção é lançada.

#### Geração de Data Válida

- Para persistência, a data de expiração é convertida para o formato YYYY-MM-DD, onde DD é o último dia do mês especificado.

### Testes

Este repositório inclui testes para a API de cartão de crédito e a API de usuário. Para executar os testes, use dentro ou fora do container:

```
python manage.py test
```

Para executar os testes com cobertura de código, use:

```
coverage run manage.py test && coverage report
```

### Motivação

A escolha da arquitetura e das tecnologias foi baseada na familiaridade com o Django e na capacidade do framework de fornecer uma solução robusta e escalável. Além disso, o Django Rest Framework facilita a criação de APIs, enquanto a biblioteca `python-creditcard` fornece validações prontas para números de cartões de crédito. O PostgreSQL foi escolhido como banco de dados por ser um dos mais populares e por ter suporte nativo ao Django. O Docker foi usado para facilitar a execução do projeto em diferentes ambientes. O Git foi usado para versionamento do código e o GitHub para hospedagem do repositório. O Pipenv foi usado para gerenciamento de dependências. O Python foi escolhido como linguagem de programação por ser a linguagem mais popular para desenvolvimento web.

### Melhorias

- Melhorias na documentação da API, melhorando os exemplos e adicionando mais detalhes.
- Melhorias na arquitetura da aplicação, como uma melhor separação de responsabilidades, divisão em camadas de serviço e casos de uso, entre outros.
- Melhorias na arquitetura do banco de dados, como a criação de índices e a normalização de tabelas.
- Melhorias na segurança, como a adição de HTTPS, autenticação por token JWT, implementação de CORS e outras medidas de proteção listadas na [OWASP](https://owasp.org/www-project-top-ten/).
- Adição de um CI/CD, como o GitHub Actions, para automatizar a execução de testes e a implantação do projeto.
- Adição de um servidor de aplicação, como o Gunicorn, para melhorar a performance e a segurança do projeto quando executado em produção.
- Melhorias na arquitetura de testes, como a criação de factories e mocks, melhor divisão dos testes de integração e unitários.
- Criação de um script para popular o banco de dados com dados de teste.
- Criação de um arquivo do Postman com exemplos de requisições para a API.
- Adição de um sistema de logs, como o Sentry, para monitorar erros e falhas.
- Separar ambientes de desenvolvimento, teste e produção.
- Adicionar um sistema de cache, como o Redis, para melhorar a performance da API.
- Adicionar um sistema de observabilidade, como o New Relic, para monitorar a performance da API.

### Referências

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [python-creditcard](https://github.com/MaisTodos/python-creditcard)

---

Qualquer dúvida, entre em contato com <danielbfr3@gmail.com>.
