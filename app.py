from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def conectar_banco():
    conexao = sqlite3.connect("estoque.db")
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela():
    conexao = conectar_banco()

    conexao.execute("""
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
    conexao.close()


@app.route("/")
def inicio():
    conexao = conectar_banco()

    produtos = conexao.execute(
        "SELECT * FROM produtos ORDER BY id DESC"
    ).fetchall()

    conexao.close()

    return render_template("index.html", produtos=produtos)


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    quantidade = request.form["quantidade"]
    estoque_minimo = request.form["estoque_minimo"]
    preco = request.form["preco"]

    conexao = conectar_banco()

    conexao.execute(
        """
        INSERT INTO produtos
        (nome, categoria, quantidade, estoque_minimo, preco)
        VALUES (?, ?, ?, ?, ?)
        """,
        (nome, categoria, quantidade, estoque_minimo, preco)
    )

    conexao.commit()
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

        conexao.execute(
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
        conexao.close()

        return redirect("/")

    produto = conexao.execute(
        "SELECT * FROM produtos WHERE id = ?",
        (id,)
    ).fetchone()

    conexao.close()

    return render_template("editar.html", produto=produto)


@app.route("/excluir/<int:id>")
def excluir(id):
    conexao = conectar_banco()

    conexao.execute(
        "DELETE FROM produtos WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")

criar_tabela()

if __name__ == "__main__":
    app.run(debug=True)