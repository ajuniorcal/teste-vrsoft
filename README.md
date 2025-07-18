# 📨 Sistema de Notificações Assíncronas — Desafio Técnico VR Software

Este projeto foi desenvolvido como solução para o desafio técnico da VR Software, com foco em arquitetura assíncrona, mensageria via RabbitMQ e boas práticas de desenvolvimento com FastAPI.

---

## Tecnologias Utilizadas

- **Python 3.11+**
- **FastAPI** — Web Framework moderno e performático
- **aio-pika** — Cliente assíncrono para RabbitMQ
- **RabbitMQ (CloudAMQP)** — Broker de mensagens
- **Docker + Docker Compose** — Containerização e orquestração
- **UUID / Pydantic / asyncio** — Utilitários auxiliares

---

## Funcionalidades Implementadas

### ✔️ POST `/api/notificar`
- Recebe notificações via payload JSON
- Valida os dados com Pydantic
- Gera e associa um `traceId` único à requisição
- Salva a notificação em memória com status `"RECEBIDO"`
- Publica a mensagem na fila RabbitMQ `fila.notificacao.entrada.antonio`
- Retorna status `202 Accepted` com `mensagemId` e `traceId`

---

## Estrutura do Projeto

```bash
app/
├── __pycache__/               # Arquivos compilados (.pyc)
├── consumers/                 # Consumers para filas RabbitMQ
│   ├── __init__.py
│   ├── entrada.py
│   ├── validacao.py
│   ├── retry.py
│   └── dlq.py
├── infra/                     # Conexão com RabbitMQ e armazenamento em memória
│   ├── __init__.py
│   ├── connection.py          # Setup de conexão RabbitMQ
│   ├── publisher.py           # Função para publicar mensagens
│   ├── store.py               # Armazenamento em memória (dicionário)
│   ├── config.py              # Configurações do sistema (URLs, variáveis)
│   ├── main.py                # Entrypoint da API FastAPI
│   ├── models.py              # Schemas de entrada e saída (Pydantic)
│   └── runner.py              # Entrypoint dos workers consumidores
tests/
├── __init__.py
└── test_publisher.py          # Teste unitário da publicação de mensagens
docker-compose.yml             # Orquestração de serviços com Docker
Dockerfile                     # Imagem da aplicação
requirements.txt               # Dependências da aplicação
README.md                      # Documentação do projeto
```

---

## Como Executar com Docker

### Requisitos
- Docker instalado
- Docker Compose instalado

### Passo a Passo

1. Clone este repositório:
   ```bash
   git clone https://github.com/seuusuario/seurepo.git
   cd seurepo
   ```

2. Construa e suba os containers:
   ```bash
   docker-compose up --build
   ```

3. Acesse a documentação interativa da API:
   ```
   http://localhost:8000/docs
   ```

---

## Exemplo de Payload

```json
POST /api/notificar
Content-Type: application/json

{
  "mensagemId": "7fa3951e-392f-4178-8eb3-8ef153501298",
  "conteudoMensagem": "Olá, bem-vindo ao sistema!",
  "tipoNotificacao": "EMAIL"
}
```

### Resposta (HTTP 202)

```json
{
  "mensagemId": "7fa3951e-392f-4178-8eb3-8ef153501298",
  "traceId": "a40ffec3-f837-4f2a-82d6-df1cfe070ae0",
  "status": "RECEBIDO"
}
```

---

## Sobre o RabbitMQ

- A aplicação se conecta a um cluster da **CloudAMQP**, utilizando uma URL no formato:

  ```
  amqp://USUARIO:SENHA@host.cloudamqp.com/vhost
  ```

- Essa URL está configurada em `config.py` e também passada como variável de ambiente no `docker-compose.yml`.

---

## Tratamento de Erros e Robustez

- Validações automáticas com Pydantic
- Tratamento de reconexão robusta com `aio_pika.connect_robust`
- Fila de Retry (`fila.notificacao.retry.antonio`)
- Fila de Dead Letter (`fila.notificacao.dlq.antonio`)
- Controle de status e histórico em memória (`store.py`)

---

## Arquivos Adicionais

### `.dockerignore`
```dockerignore
__pycache__
*.pyc
*.pyo
*.db
*.env
.venv/
.env/
*.egg-info/
```

### `requirements.txt`
```txt
fastapi==0.110.2
uvicorn==0.29.0
aio-pika==9.3.0
pydantic==2.7.1
pytest==8.2.1
pytest-asyncio==0.23.6
```

---

## 👨‍💻 Autor

Desenvolvido por **Antonio Amaral** como parte do processo seletivo para **Programador Python Pleno/Sênior na VR Software**.

---

## 💡 Possíveis Melhorias Futuras

- Persistência em banco (PostgreSQL, Redis)
- Integração com ferramentas externas de envio (email, SMS, push)
- Cache e observabilidade (Prometheus + Grafana)
