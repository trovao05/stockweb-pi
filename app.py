from flask import Flask, render_template, request, redirect
import os
import sqlite3

import psycopg2
import psycopg2.extras


app = Flask(__name__)


def usando_postgres():
    return os.environ.get("DATABASE_URL") is not None


def conectar_banco():
    if usando_postgres():
        conexao = psycopg2.connect(
            os.environ.get("DATABASE_URL")
        )
        return conexao

    conexao = sqlite3.connect("estoque.db")
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    if usando_postgres():
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                estoque_minimo INTEGER NOT NULL,
                preco REAL NOT NULL
            )
        """)
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                estoque_minimo INTEGER NOT NULL,
                preco REAL NOT NULL
            )
        """)

    conexao.commit()
    cursor.close()
    conexao.close()


@app.route("/")
def inicio():
    conexao = conectar_banco()

    if usando_postgres():
        cursor = conexao.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )
    else:
        cursor = conexao.cursor()

    # Lista de produtos
    cursor.execute(
        "SELECT * FROM produtos ORDER BY id DESC"
    )
    produtos = cursor.fetchall()

    # Total de produtos cadastrados
    cursor.execute("""
        SELECT COUNT(*)
        FROM produtos
    """)
    total_produtos = cursor.fetchone()[0]

    # Total de unidades
    cursor.execute("""
        SELECT COALESCE(SUM(quantidade), 0)
        FROM produtos
    """)
    total_unidades = cursor.fetchone()[0]

    # Valor total do estoque
    cursor.execute("""
        SELECT COALESCE(SUM(quantidade * preco), 0)
        FROM produtos
    """)
    valor_estoque = cursor.fetchone()[0]

    # Produtos com estoque baixo
    cursor.execute("""
        SELECT COUNT(*)
        FROM produtos
        WHERE quantidade <= estoque_minimo
    """)
    estoque_baixo = cursor.fetchone()[0]

    # Produtos por categoria
    cursor.execute("""
        SELECT categoria, COUNT(*) AS quantidade
        FROM produtos
        GROUP BY categoria
        ORDER BY categoria
    """)
    dados_categoria = cursor.fetchall()

    categorias = [
        linha["categoria"]
        for linha in dados_categoria
    ]

    quantidades_categoria = [
        linha["quantidade"]
        for linha in dados_categoria
    ]

    cursor.close()
    conexao.close()

    return render_template(
        "index.html",
        produtos=produtos,
        total_produtos=total_produtos,
        total_unidades=total_unidades,
        valor_estoque=valor_estoque,
        estoque_baixo=estoque_baixo,
        categorias=categorias,
        quantidades_categoria=quantidades_categoria
    )


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    quantidade = request.form["quantidade"]
    estoque_minimo = request.form["estoque_minimo"]
    preco = request.form["preco"]

    conexao = conectar_banco()
    cursor = conexao.cursor()

    if usando_postgres():
        cursor.execute(
            """
            INSERT INTO produtos
            (
                nome,
                categoria,
                quantidade,
                estoque_minimo,
                preco
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                nome,
                categoria,
                quantidade,
                estoque_minimo,
                preco
            )
        )
    else:
        cursor.execute(
            """
            INSERT INTO produtos
            (
                nome,
                categoria,
                quantidade,
                estoque_minimo,
                preco
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                nome,
                categoria,
                quantidade,
                estoque_minimo,
                preco
            )
        )

    conexao.commit()
    cursor.close()
    conexao.close()

    return redirect("/")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conexao = conectar_banco()

    if request.method == "POST":
        nome = request.form["nome"]
        categoria = request.form["categoria"]
        quantidade = request.form["quantidade"]
        estoque_minimo = request.form["estoque_minimo"]
        preco = request.form["preco"]

        cursor = conexao.cursor()

        if usando_postgres():
            cursor.execute(
                """
                UPDATE produtos
                SET nome = %s,
                    categoria = %s,
                    quantidade = %s,
                    estoque_minimo = %s,
                    preco = %s
                WHERE id = %s
                """,
                (
                    nome,
                    categoria,
                    quantidade,
                    estoque_minimo,
                    preco,
                    id
                )
            )
        else:
            cursor.execute(
                """
                UPDATE produtos
                SET nome = ?,
                    categoria = ?,
                    quantidade = ?,
                    estoque_minimo = ?,
                    preco = ?
                WHERE id = ?
                """,
                (
                    nome,
                    categoria,
                    quantidade,
                    estoque_minimo,
                    preco,
                    id
                )
            )

        conexao.commit()
        cursor.close()
        conexao.close()

        return redirect("/")

    if usando_postgres():
        cursor = conexao.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        cursor.execute(
            "SELECT * FROM produtos WHERE id = %s",
            (id,)
        )
    else:
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM produtos WHERE id = ?",
            (id,)
        )

    produto = cursor.fetchone()

    cursor.close()
    conexao.close()

    return render_template(
        "editar.html",
        produto=produto
    )


@app.route("/excluir/<int:id>")
def excluir(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    if usando_postgres():
        cursor.execute(
            "DELETE FROM produtos WHERE id = %s",
            (id,)
        )
    else:
        cursor.execute(
            "DELETE FROM produtos WHERE id = ?",
            (id,)
        )

    conexao.commit()
    cursor.close()
    conexao.close()

    return redirect("/")


criar_tabela()


if __name__ == "__main__":
    app.run(debug=True)