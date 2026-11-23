import re
from datetime import date

from werkzeug.security import check_password_hash, generate_password_hash

import models

JENIS_KATEGORI_VALID = ("pemasukan", "pengeluaran", "umum")
JENIS_TRANSAKSI_VALID = ("pemasukan", "pengeluaran")
PERAN = ("pemilik", "kasir")
BATAS_NOMINAL = 1_000_000_000

# Hash palsu agar waktu respons sama saat username tidak ditemukan
_HASH_PALSU = generate_password_hash("bukan-kata-sandi-sungguhan")


def _bilangan_positif(teks):
    """Ubah teks menjadi bilangan bulat ASCII 1..BATAS_NOMINAL, atau None bila tidak valid."""
    teks = (teks or "").strip()
    if not (teks.isascii() and teks.isdigit()) or len(teks) > 10:
        return None
    angka = int(teks)
    return angka if 1 <= angka <= BATAS_NOMINAL else None


def validasi_kategori(form):
    """Kembalikan (data, daftar_galat) sesuai aturan kamus-data.md."""
    galat = []
    nama = (form.get("nama_kategori") or "").strip()
    jenis = (form.get("jenis_default") or "").strip()

    if not nama:
        galat.append("Nama kategori wajib diisi.")
    elif len(nama) > 50:
        galat.append("Nama kategori maksimal 50 karakter.")

    if jenis not in JENIS_KATEGORI_VALID:
        galat.append("Jenis bawaan harus dipilih (pemasukan, pengeluaran, atau umum).")

    data = {"nama_kategori": nama, "jenis_default": jenis}
    return data, galat


def validasi_transaksi(form):
    """Validasi masukan transaksi sesuai KF-02 dan kamus-data.md."""
    galat = []
    tanggal = (form.get("tanggal") or "").strip()
    jenis = (form.get("jenis") or "").strip()
    keterangan = (form.get("keterangan") or "").strip()
    nominal_teks = (form.get("nominal") or "").strip()
    kategori_teks = (form.get("kategori_id") or "").strip()

    try:
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", tanggal):
            raise ValueError("Format tanggal wajib TTTT-BB-HH.")
        date.fromisoformat(tanggal)
    except ValueError:
        galat.append("Tanggal harus berformat TTTT-BB-HH.")

    if jenis not in JENIS_TRANSAKSI_VALID:
        galat.append("Jenis transaksi harus pemasukan atau pengeluaran.")
    if not keterangan:
        galat.append("Keterangan wajib diisi.")
    elif len(keterangan) > 50:
        galat.append("Keterangan maksimal 50 karakter.")

    nominal = _bilangan_positif(nominal_teks)
    if nominal is None:
        galat.append("Nominal harus berupa angka lebih dari 0 (maksimal 1.000.000.000).")

    kategori_id = _bilangan_positif(kategori_teks)
    if kategori_id is None:
        galat.append("Pilih kategori terlebih dahulu.")

    data = {
        "tanggal": tanggal,
        "jenis": jenis,
        "keterangan": keterangan,
        "nominal": nominal,
        "kategori_id": kategori_id,
    }
    return data, galat


def validasi_pengguna_baru(username, password, peran):
    """Aturan pembuatan akun; kembalikan daftar galat."""
    galat = []
    if not re.fullmatch(r"[A-Za-z0-9_]{3,30}", username or ""):
        galat.append("Nama pengguna 3-30 karakter: huruf, angka, atau garis bawah.")
    if len(password or "") < 8:
        galat.append("Kata sandi minimal 8 karakter.")
    if peran not in PERAN:
        galat.append("Peran harus pemilik atau kasir.")
    return galat


def buat_pengguna(username, password, peran):
    """Simpan pengguna dengan kata sandi ter-hash. Kembalikan daftar galat."""
    galat = validasi_pengguna_baru(username, password, peran)
    if not galat:
        models.tambah_pengguna(username, generate_password_hash(password), peran)
    return galat


def autentikasi(username, password):
    """Kembalikan baris pengguna bila cocok, selain itu None."""
    pengguna = models.cari_pengguna((username or "").strip())
    hash_tersimpan = pengguna["password_hash"] if pengguna else _HASH_PALSU
    cocok = check_password_hash(hash_tersimpan, password or "")
    return pengguna if (pengguna and cocok) else None