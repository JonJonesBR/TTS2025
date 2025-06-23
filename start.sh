#!/usr/bin/env bash

# Cria os diretórios 'uploads' e 'audiobooks' se eles não existirem.
# Isso garante que o aplicativo tenha onde salvar arquivos temporários.
mkdir -p uploads
mkdir -p audiobooks

# Inicia o servidor Uvicorn para o seu aplicativo FastAPI
# main:app significa que 'app' é a instância FastAPI no arquivo 'main.py'
uvicorn main:app --host 0.0.0.0 --port $PORT