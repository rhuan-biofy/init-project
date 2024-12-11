FROM python:3.11-alpine

WORKDIR /app/

# Instalar dependências do sistema
RUN apk add --no-cache bash curl gcc musl-dev libffi-dev python3-dev build-base

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry && \
    poetry config virtualenvs.create false

# Copiar arquivos do projeto
COPY ./pyproject.toml /app/
COPY ./poetry.lock /app/

# Instalar dependências
ARG INSTALL_DEV=false
RUN if [ "$INSTALL_DEV" = "true" ] ; then \
        poetry install --no-root ; \
    else \
        poetry install --no-root --only main ; \
    fi

# Configurar variáveis de ambiente
ENV PYTHONPATH=/app

# Comando de execução
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]
