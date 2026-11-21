from datetime import datetime
import json
import os
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
DATA_FILE = "data_keuangan.json"

def salam_waktu(jam):
    """Mengembalikan salam sesuai jam (0-23)."""
    if 4 <= jam < 11:
        return "Selamat pagi"
    if 11 <= jam < 15:
        return "Selamat siang"
    if 15 <= jam < 18:
        return "Selamat sore"
    return "Selamat malam"

def muat_transaksi():
    """Membaca daftar transaksi dari berkas JSON lokal."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as berkas:
        try:
            return json.load(berkas)
        except json.JSONDecodeError:
            return []


def simpan_transaksi(daftar_transaksi):
    """Menyimpan daftar transaksi ke berkas JSON lokal."""
    with open(DATA_FILE, "w", encoding="utf-8") as berkas:
        json.dump(daftar_transaksi, berkas, ensure_ascii=False, indent=2)


@app.template_filter("rupiah")
def format_rupiah(nilai):
    """Mengubah angka menjadi format mata uang Rupiah."""
    return f"Rp {nilai:,.0f}".replace(",", ".")


@app.route("/", methods=["GET", "POST"])
def beranda():
    daftar_transaksi = muat_transaksi()
    pesan_error = ""

    if request.method == "POST":
        # Ambil dan bersihkan masukan pengguna (validasi di sisi server)
        keterangan = request.form.get("keterangan", "").strip()[:100]
        jenis = request.form.get("jenis", "").strip()
        nominal_teks = request.form.get("nominal", "").strip()

        if not keterangan:
            pesan_error = "Keterangan transaksi tidak boleh kosong."
        elif jenis not in ("pemasukan", "pengeluaran"):
            pesan_error = "Jenis transaksi tidak valid."
        elif not nominal_teks.isdigit() or int(nominal_teks) <= 0:
            pesan_error = "Nominal harus berupa angka positif lebih dari 0."
        else:
            id_baru = max((t["id"] for t in daftar_transaksi), default=0) + 1
            transaksi_baru = {
                "id": id_baru,
                "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "keterangan": keterangan,
                "jenis": jenis,
                "nominal": int(nominal_teks),
            }
            daftar_transaksi.append(transaksi_baru)
            simpan_transaksi(daftar_transaksi)
            return redirect(url_for("beranda"))

    # Hitung ringkasan keuangan
    total_pemasukan = sum(
        t["nominal"] for t in daftar_transaksi if t["jenis"] == "pemasukan"
    )
    total_pengeluaran = sum(
        t["nominal"] for t in daftar_transaksi if t["jenis"] == "pengeluaran"
    )
    saldo = total_pemasukan - total_pengeluaran
    sekarang = datetime.now()

    return render_template(
        "index.html",
        salam=salam_waktu(sekarang.hour),
        waktu=sekarang.strftime("%d-%m-%Y %H:%M"),
        transaksi=list(reversed(daftar_transaksi)),
        total_pemasukan=total_pemasukan,
        total_pengeluaran=total_pengeluaran,
        saldo=saldo,
        pesan_error=pesan_error,
    )


@app.route("/hapus/<int:id_transaksi>", methods=["POST"])
def hapus_transaksi(id_transaksi):
    """Menghapus satu transaksi berdasarkan ID."""
    daftar_transaksi = muat_transaksi()
    daftar_baru = [t for t in daftar_transaksi if t["id"] != id_transaksi]
    simpan_transaksi(daftar_baru)
    return redirect(url_for("beranda"))


if __name__ == "__main__":
    app.run(debug=True)