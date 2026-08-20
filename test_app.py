import os
import sqlite3
import tempfile
import pytest

from app import app


@pytest.fixture
def cliente():
    app.config["TESTING"] = True

    with app.test_client() as cliente:
        yield cliente


def test_pagina_inicial_abre(cliente):
    resposta = cliente.get("/")

    assert resposta.status_code == 200
    assert b"StockWeb" in resposta.data


def test_rota_cadastro_existe(cliente):
    resposta = cliente.post(
        "/cadastrar",
        data={
            "nome": "Produto Teste",
            "categoria": "Teste",
            "quantidade": "10",
            "estoque_minimo": "5",
            "preco": "20.00"
        }
    )

    assert resposta.status_code in [302, 200]