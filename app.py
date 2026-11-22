import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, url_for

import models
import services

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-ganti-di-produksi")
models.init_db()


@app.route("/")
def beranda():
    return redirect(url_for("daftar_kategori"))


@app.route("/kategori")
def daftar_kategori():
    return render_template("kategori_list.html", kategori=models.semua_kategori())


@app.route("/kategori/tambah", methods=["GET", "POST"])
def tambah_kategori():
    if request.method == "POST":
        data, galat = services.validasi_kategori(request.form)
        if not galat:
            try:
                models.tambah_kategori(data["nama_kategori"], data["jenis_default"])
            except sqlite3.IntegrityError:
                galat.append("Nama kategori sudah terdaftar.")
            else:
                flash("Kategori berhasil ditambahkan.")
                return redirect(url_for("daftar_kategori"))
        return render_template("kategori_form.html", judul="Tambah Kategori", kategori=request.form, galat=galat)
    return render_template("kategori_form.html", judul="Tambah Kategori", kategori={}, galat=[])


if __name__ == "__main__":
    app.run(debug=True)