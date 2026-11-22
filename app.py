import os

from flask import Flask, redirect, render_template, url_for

import models

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-ganti-di-produksi")
models.init_db()


@app.route("/")
def beranda():
    return redirect(url_for("daftar_kategori"))


@app.route("/kategori")
def daftar_kategori():
    return render_template("kategori_list.html", kategori=models.semua_kategori())


@app.route("/kategori/tambah")
def tambah_kategori():
    return "Form tambah kategori (Siklus 3)"


if __name__ == "__main__":
    app.run(debug=True)