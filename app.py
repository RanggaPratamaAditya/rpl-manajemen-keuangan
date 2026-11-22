import csv
import io
import logging
import os
import secrets
import sqlite3
from datetime import date
from functools import wraps

from flask import (
    Flask,
    Response,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import models
import percobaan
import services

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Konfigurasi dari lingkungan. Pada produksi (APP_ENV=production) SECRET_KEY WAJIB diatur.
PRODUKSI = os.environ.get("APP_ENV") == "production"
app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    if PRODUKSI:
        raise RuntimeError("SECRET_KEY wajib diatur pada lingkungan produksi.")
    app.secret_key = "dev-only-ganti-di-produksi"  # hanya untuk pengembangan lokal

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=PRODUKSI,
)
models.init_db()


def csrf_token():
    """Token acak per sesi untuk setiap formulir POST."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return session["csrf_token"]


app.jinja_env.globals["csrf_token"] = csrf_token


@app.before_request
def muat_pengguna():
    """Isi g.pengguna dari sesi; None bila belum masuk."""
    pengguna_id = session.get("pengguna_id")
    g.pengguna = models.ambil_pengguna(pengguna_id) if pengguna_id else None


@app.before_request
def periksa_csrf():
    """Tolak POST tanpa token yang cocok dengan token sesi."""
    if request.method == "POST":
        dikirim = request.form.get("csrf_token", "").encode()
        asli = session.get("csrf_token", "").encode()
        if not asli or not secrets.compare_digest(dikirim, asli):
            app.logger.warning("CSRF gagal path=%r ip=%s", request.path, request.remote_addr)
            abort(400)


@app.after_request
def tambah_header(respons):
    respons.headers["X-Content-Type-Options"] = "nosniff"
    respons.headers["X-Frame-Options"] = "DENY"
    respons.headers["Referrer-Policy"] = "same-origin"
    return respons


def peran_diperlukan(*peran):
    """Batasi rute: belum masuk -> /login; peran tidak cocok -> 403."""
    def dekorator(fungsi):
        @wraps(fungsi)
        def bungkus(*args, **kwargs):
            if g.pengguna is None:
                return redirect(url_for("login", next=request.full_path.rstrip("?")))
            if g.pengguna["peran"] not in peran:
                abort(403)
            return fungsi(*args, **kwargs)
        return bungkus
    return dekorator


semua_peran = peran_diperlukan(*services.PERAN)
hanya_pemilik = peran_diperlukan("pemilik")


def _tujuan_aman(tujuan):
    """Terima hanya alamat dalam situs ini (cegah open redirect)."""
    if tujuan and tujuan.startswith("/") and not tujuan.startswith("//") and "\\" not in tujuan:
        return tujuan
    return None


def _form_kategori(judul, kategori, galat):
    return render_template("kategori_form.html", judul=judul, kategori=kategori, galat=galat)


def _form_transaksi(judul, transaksi, galat):
    return render_template(
        "transaksi_form.html",
        judul=judul,
        transaksi=transaksi,
        kategori=models.semua_kategori(),
        galat=galat,
        default_tanggal=date.today().isoformat(),
    )


@app.errorhandler(400)
def permintaan_buruk(_galat):
    return render_template("400.html"), 400


@app.errorhandler(403)
def dilarang(_galat):
    pengguna = g.pengguna["username"] if g.get("pengguna") else "-"
    app.logger.warning("akses ditolak user=%r path=%r", pengguna, request.path)
    return render_template("403.html"), 403


@app.route("/login", methods=["GET", "POST"])
def login():
    galat, status = [], 200
    username = request.form.get("username", "")
    if request.method == "POST":
        kunci = f"{request.remote_addr}|{username.strip().lower()}"
        if percobaan.terkunci(kunci):
            app.logger.warning("login terkunci user=%r ip=%s", username, request.remote_addr)
            galat.append("Terlalu banyak percobaan gagal. Coba lagi beberapa menit lagi.")
            status = 429
        else:
            pengguna = services.autentikasi(username, request.form.get("password"))
            if pengguna:
                percobaan.reset(kunci)
                session.clear()
                session["pengguna_id"] = pengguna["id"]
                app.logger.info("login berhasil user=%r", pengguna["username"])
                return redirect(_tujuan_aman(request.args.get("next")) or url_for("daftar_transaksi"))
            percobaan.catat_gagal(kunci)
            app.logger.warning("login gagal user=%r ip=%s", username, request.remote_addr)
            galat.append("Nama pengguna atau kata sandi salah.")
            status = 401
    return render_template("login.html", galat=galat, username=username), status


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Anda telah keluar.")
    return redirect(url_for("login"))


@app.route("/")
@semua_peran
def beranda():
    return redirect(url_for("daftar_transaksi"))


@app.route("/kategori")
@hanya_pemilik
def daftar_kategori():
    return render_template("kategori_list.html", kategori=models.semua_kategori())


@app.route("/kategori/tambah", methods=["GET", "POST"])
@hanya_pemilik
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
        return _form_kategori("Tambah Kategori", request.form, galat)
    return _form_kategori("Tambah Kategori", {}, [])


@app.route("/kategori/<int:kategori_id>/ubah", methods=["GET", "POST"])
@hanya_pemilik
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
        return _form_kategori("Ubah Kategori", request.form, galat)
    return _form_kategori("Ubah Kategori", dict(kategori), [])


@app.route("/kategori/<int:kategori_id>/hapus", methods=["POST"])
@hanya_pemilik
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
@semua_peran
def daftar_transaksi():
    kata = request.args.get("q", "").strip()
    jenis = request.args.get("jenis", "").strip()
    bulan = request.args.get("bulan", "").strip()
    transaksi = models.cari_transaksi(kata, jenis, bulan)
    return render_template(
        "transaksi_list.html",
        transaksi=transaksi,
        ringkasan=models.ringkasan_saldo(),
        kata=kata,
        jenis=jenis,
        bulan=bulan,
    )


@app.route("/transaksi/tambah", methods=["GET", "POST"])
@semua_peran
def tambah_transaksi():
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
                    g.pengguna["id"],
                )
            except sqlite3.IntegrityError:
                galat.append("Kategori atau pengguna tidak valid.")
            else:
                flash("Transaksi berhasil disimpan.")
                return redirect(url_for("daftar_transaksi"))
        return _form_transaksi("Catat Transaksi", request.form, galat)
    return _form_transaksi("Catat Transaksi", {}, [])


@app.route("/transaksi/<int:transaksi_id>/ubah", methods=["GET", "POST"])
@semua_peran
def ubah_transaksi(transaksi_id):
    trx = models.ambil_transaksi(transaksi_id)
    if trx is None:
        abort(404)
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
        return _form_transaksi("Ubah Transaksi", request.form, galat)
    return _form_transaksi("Ubah Transaksi", dict(trx), [])


@app.route("/transaksi/<int:transaksi_id>/hapus", methods=["POST"])
@hanya_pemilik
def hapus_transaksi(transaksi_id):
    if models.ambil_transaksi(transaksi_id) is None:
        abort(404)
    models.hapus_transaksi(transaksi_id)
    flash("Transaksi berhasil dihapus.")
    return redirect(url_for("daftar_transaksi"))


@app.route("/ekspor")
@hanya_pemilik
def ekspor_csv():
    bulan = request.args.get("bulan", "").strip()
    data = models.cari_transaksi(bulan=bulan)
    if not data:
        flash("Tidak ada data untuk diekspor.")
        return redirect(url_for("daftar_transaksi"))

    buffer = io.StringIO()
    penulis = csv.writer(buffer)
    penulis.writerow(["Tanggal", "Jenis", "Kategori", "Keterangan", "Nominal"])
    for t in data:
        penulis.writerow([t["tanggal"], t["jenis"], t["nama_kategori"], t["keterangan"], t["nominal"]])

    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=rekap-keuangan-{bulan or 'semua'}.csv"},
    )


if __name__ == "__main__":
    # Mode debug hanya bila diminta lewat lingkungan (FLASK_DEBUG=1) dan tidak pernah pada produksi.
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1" and not PRODUKSI)