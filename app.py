import os
import sqlite3
from datetime import date

from flask import Flask, abort, flash, redirect, render_template, request, url_for

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
        return render_template(
            "kategori_form.html", judul="Tambah Kategori", kategori=request.form, galat=galat
        )
    return render_template(
        "kategori_form.html", judul="Tambah Kategori", kategori={}, galat=[]
    )


@app.route("/kategori/<int:kategori_id>/ubah", methods=["GET", "POST"])
def ubah_kategori(kategori_id):
    kategori = models.ambil_kategori(kategori_id)
    if kategori is None:
        abort(404)
    if request.method == "POST":
        data, galat = services.validasi_kategori(request.form)
        if not galat:
            try:
                models.ubah_kategori(
                    kategori_id, data["nama_kategori"], data["jenis_default"]
                )
            except sqlite3.IntegrityError:
                galat.append("Nama kategori sudah terdaftar.")
            else:
                flash("Kategori berhasil diubah.")
                return redirect(url_for("daftar_kategori"))
        return render_template(
            "kategori_form.html", judul="Ubah Kategori", kategori=request.form, galat=galat
        )
    return render_template(
        "kategori_form.html", judul="Ubah Kategori", kategori=dict(kategori), galat=[]
    )


@app.route("/kategori/<int:kategori_id>/hapus", methods=["POST"])
def hapus_kategori(kategori_id):
    if models.ambil_kategori(kategori_id) is None:
        abort(404)
    try:
        models.hapus_kategori(kategori_id)
    except sqlite3.IntegrityError:
        flash("Kategori tidak dapat dihapus karena sudah dipakai pada transaksi.")
    else:
        flash("Kategori berhasil dihapus.")
    return redirect(url_for("daftar_kategori"))


@app.route("/transaksi")
def daftar_transaksi():
    return render_template(
        "transaksi_list.html",
        transaksi=models.semua_transaksi(),
        ringkasan=models.ringkasan_saldo(),
    )


@app.route("/transaksi/tambah", methods=["GET", "POST"])
def tambah_transaksi():
    kategori = models.semua_kategori()
    hari_ini = date.today().isoformat()
    if request.method == "POST":
        data, galat = services.validasi_transaksi(request.form)
        if not galat and models.ambil_kategori(data["kategori_id"]) is None:
            galat.append("Kategori tidak ditemukan.")
        if not galat:
            try:
                models.tambah_transaksi(
                    data["tanggal"],
                    data["jenis"],
                    data["keterangan"],
                    data["nominal"],
                    data["kategori_id"],
                )
            except sqlite3.IntegrityError:
                galat.append("Kategori atau pengguna tidak valid.")
            else:
                flash("Transaksi berhasil disimpan.")
                return redirect(url_for("daftar_transaksi"))
        return render_template(
            "transaksi_form.html",
            judul="Catat Transaksi",
            transaksi=request.form,
            kategori=kategori,
            galat=galat,
            default_tanggal=hari_ini,
        )
    return render_template(
        "transaksi_form.html",
        judul="Catat Transaksi",
        transaksi={},
        kategori=kategori,
        galat=[],
        default_tanggal=hari_ini,
    )


@app.route("/transaksi/<int:transaksi_id>/ubah", methods=["GET", "POST"])
def ubah_transaksi(transaksi_id):
    trx = models.ambil_transaksi(transaksi_id)
    if trx is None:
        abort(404)
    kategori = models.semua_kategori()
    hari_ini = date.today().isoformat()
    if request.method == "POST":
        data, galat = services.validasi_transaksi(request.form)
        if not galat and models.ambil_kategori(data["kategori_id"]) is None:
            galat.append("Kategori tidak ditemukan.")
        if not galat:
            try:
                models.ubah_transaksi(
                    transaksi_id,
                    data["tanggal"],
                    data["jenis"],
                    data["keterangan"],
                    data["nominal"],
                    data["kategori_id"],
                )
            except sqlite3.IntegrityError:
                galat.append("Kategori tidak valid.")
            else:
                flash("Transaksi berhasil diubah.")
                return redirect(url_for("daftar_transaksi"))
        return render_template(
            "transaksi_form.html",
            judul="Ubah Transaksi",
            transaksi=request.form,
            kategori=kategori,
            galat=galat,
            default_tanggal=hari_ini,
        )
    return render_template(
        "transaksi_form.html",
        judul="Ubah Transaksi",
        transaksi=dict(trx),
        kategori=kategori,
        galat=[],
        default_tanggal=hari_ini,
    )


@app.route("/transaksi/<int:transaksi_id>/hapus", methods=["POST"])
def hapus_transaksi(transaksi_id):
    if models.ambil_transaksi(transaksi_id) is None:
        abort(404)
    models.hapus_transaksi(transaksi_id)
    flash("Transaksi berhasil dihapus.")
    return redirect(url_for("daftar_transaksi"))


if __name__ == "__main__":
    app.run(debug=True)