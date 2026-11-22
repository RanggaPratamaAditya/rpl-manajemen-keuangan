"""Uji regresi cepat: jalankan `python tests/uji_cepat.py` dari folder proyek.
Memakai basis data sementara sehingga keuangan.db asli tidak tersentuh."""
import sqlite3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import models
import services

models.DB_PATH = Path(tempfile.mkdtemp()) / "uji.db"
import app as aplikasi

# Buat 2 akun uji ter-hash pada DB sementara
assert services.buat_pengguna("bos_uji", "sandi_pemilik_123", "pemilik") == []
assert services.buat_pengguna("kasir_uji", "sandi_kasir_123", "kasir") == []

c = aplikasi.app.test_client()


def kirim(url, **data):
    return c.post(url, data=data, follow_redirects=True)


def ada(teks, hasil):
    assert teks in hasil.text, f"Tidak ditemukan: {teks!r}"


def masuk(username, password):
    return kirim("/login", username=username, password=password)


# --- 1. Uji Autentikasi, Hash, dan Open Redirect ---
pengguna_bos = models.cari_pengguna("bos_uji")
assert pengguna_bos["password_hash"] != "sandi_pemilik_123"
assert pengguna_bos["password_hash"].startswith(("scrypt:", "pbkdf2:"))

# Tamu diarahkan ke /login
res_tamu = c.get("/transaksi")
assert res_tamu.status_code == 302 and "/login" in res_tamu.headers["Location"]

# Pesan galat sama untuk sandi salah dan username tidak ada
galat_sandi = masuk("bos_uji", "salah_banget").text
galat_user = masuk("tidak_ada", "salah_banget").text
assert "Nama pengguna atau kata sandi salah." in galat_sandi
assert "Nama pengguna atau kata sandi salah." in galat_user

# Open redirect diabaikan
res_next = c.post(
    "/login?next=https://jahat.example",
    data={"username": "bos_uji", "password": "sandi_pemilik_123"},
)
assert res_next.status_code == 302
assert "jahat.example" not in res_next.headers["Location"]

# --- 2. Uji Peran Penuh (Pemilik): Kategori & Transaksi ---
ada("Belum ada data kategori", c.get("/kategori"))
for nama, jenis in [("Penjualan", "pemasukan"), ("Operasional", "pengeluaran"), ("Lainnya", "umum")]:
    ada("berhasil ditambahkan", kirim("/kategori/tambah", nama_kategori=nama, jenis_default=jenis))
ada("sudah terdaftar", kirim("/kategori/tambah", nama_kategori="Penjualan", jenis_default="pemasukan"))
ada("berhasil diubah", kirim("/kategori/2/ubah", nama_kategori="Operasional Toko", jenis_default="pengeluaran"))
assert c.get("/kategori/999/ubah").status_code == 404

ada("Belum ada data transaksi", c.get("/transaksi"))
ada(
    "berhasil disimpan",
    kirim(
        "/transaksi/tambah",
        tanggal="2026-11-23",
        jenis="pemasukan",
        kategori_id=1,
        keterangan="Penjualan harian",
        nominal=250000,
    ),
)
ada(
    "berhasil disimpan",
    kirim(
        "/transaksi/tambah",
        tanggal="2026-11-23",
        jenis="pengeluaran",
        kategori_id=2,
        keterangan="Diskon 100% bahan",
        nominal=50000,
    ),
)
ada("lebih dari 0", kirim("/transaksi/tambah", tanggal="2026-11-23", jenis="pemasukan", kategori_id=1, keterangan="Tes", nominal=-5))
ada("TTTT-BB-HH", kirim("/transaksi/tambah", tanggal="10-11-2026", jenis="pemasukan", kategori_id=1, keterangan="Tes", nominal=1000))
ada("tidak ditemukan", kirim("/transaksi/tambah", tanggal="2026-11-23", jenis="pemasukan", kategori_id=999, keterangan="Tes", nominal=1000))
assert models.ringkasan_saldo()["saldo"] == 200000

# --- 3. Pencarian, Penyaringan, Atomisitas, FK, dan Ekspor CSV ---
hasil = c.get("/transaksi?q=HARIAN")
ada("Penjualan harian", hasil)
assert "Diskon 100% bahan" not in hasil.text
hasil = c.get("/transaksi?q=%25")
ada("Diskon 100% bahan", hasil)
ada("Tidak ada transaksi yang cocok", c.get("/transaksi?q=' OR 1=1 --"))

jumlah_kat_awal = len(models.semua_kategori())
try:
    models.tambah_kategori_dan_transaksi("Gagal", "umum", "2026-11-23", "pemasukan", "Tes", 1000, pengguna_id=999)
except sqlite3.IntegrityError:
    pass
assert len(models.semua_kategori()) == jumlah_kat_awal

ada("tidak dapat dihapus", kirim("/kategori/1/hapus"))
assert c.get("/kategori/1/hapus").status_code == 405
ada("berhasil dihapus", kirim("/kategori/3/hapus"))

res_csv = c.get("/ekspor")
assert res_csv.status_code == 200 and "text/csv" in res_csv.content_type

# --- 4. Uji Logout dan Otorisasi Peran Terbatas (Kasir) ---
ada("Anda telah keluar.", kirim("/logout"))
assert c.get("/transaksi").status_code == 302

masuk("kasir_uji", "sandi_kasir_123")
assert c.get("/transaksi").status_code == 200
assert c.get("/kategori").status_code == 403
assert c.get("/ekspor").status_code == 403
assert c.post("/transaksi/1/hapus").status_code == 403
assert models.ambil_transaksi(1) is not None  # data tetap aman

print("SEMUA UJI LULUS")