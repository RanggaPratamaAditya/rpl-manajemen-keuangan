import os

from flask import Flask, redirect, url_for

import models

app = Flask(__name__)
# Kunci rahasia dibaca dari lingkungan; nilai bawaan hanya untuk pengembangan lokal.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-ganti-di-produksi")
models.init_db()


@app.route("/")
def beranda():
    return redirect(url_for("daftar_kategori"))


@app.route("/kategori")
def daftar_kategori():
    return "Kerangka Sistem Manajemen Keuangan UMKM berjalan."


if __name__ == "__main__":
    app.run(debug=True)