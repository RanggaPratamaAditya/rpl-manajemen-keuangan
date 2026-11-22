"""Uji regresi cepat: jalankan `python tests/uji_cepat.py` dari folder proyek.
Memakai basis data sementara sehingga keuangan.db asli tidak tersentuh."""
import sqlite3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import models
import percobaan
import services

models.DB_PATH = Path(tempfile.mkdtemp()) / "uji.db"
import app as aplikasi

assert services.buat_pengguna("bos_uji", "sandi_pemilik_123", "pemilik") == []
assert services.buat_pengguna("kasir_uji", "sandi_kasir_123", "kasir") == []

c = aplikasi.app.test_client()


def _siapkan_token(klien, token="token-uji"):
    with klien.session_transaction() as s:
        s.setdefault("csrf_token", token)
        return s["csrf_token"]


def kirim(url, klien=None, ikuti=True, **data):
    klien = klien or c
    data.setdefault("csrf_token", _siapkan_token(klien))
    return klien.post(url, data=data, follow_redirects=ikuti)


def ada(teks, hasil):
    assert teks in hasil.text, f"Tidak ditemukan: {teks!r}"


def masuk(username, password, klien=None):
    return kirim("/login", klien=klien, username=username, password=password)


# --- 1. Uji CSRF (POST tanpa token harus 400) ---
assert c.post("/login", data={"username": "bos_uji", "password": "sandi_pemilik_123"}).status_code == 400

# --- 2. Uji Autentikasi, Hash, dan Open Redirect ---
pengguna_bos = models.cari_pengguna("bos_uji")
assert pengguna_bos["password_hash"] != "sandi_pemilik_123"
assert pengguna_bos["password_hash"].startswith(("scrypt:", "pbkdf2:"))

res_tamu = c.get("/transaksi")
assert res_tamu.status_code == 302 and "/login" in res_tamu.headers["Location"]

galat_sandi = masuk("bos_uji", "salah_banget").text
galat_user = masuk("tidak_ada", "salah_banget").text
assert "Nama pengguna atau kata sandi salah." in galat_sandi
assert "Nama pengguna atau kata sandi salah." in galat_user

res_next = kirim(
    "/login?next=https://jahat.example",
    ikuti=False,
    username="bos_uji",
    password="sandi_pemilik_123",
)
assert res_next.status_code == 302
assert "jahat.example" not in res_next.headers["Location"]

# --- 3. Uji Header Keamanan ---
h = c.get("/transaksi").headers
assert h["X-Content-Type-Options"] == "nosniff"
assert h["X-Frame-Options"] == "DENY"
assert h["Referrer-Policy"] == "same-origin"

# --- 4. Uji Peran Penuh (Pemilik): Kategori, Transaksi, Pencarian, Atomisitas, FK, CSV ---
ada("Belum ada data kategori", c.get("/kategori"))
for nama, jenis in [("Penjualan", "pemasukan"), ("Operasional", "pengeluaran"), ("Lainnya", "umum")]:
    ada("berhasil ditambahkan", kirim("/kategori/tambah", nama_kategori=nama, jenis_default=jenis))
ada("sudah terdaftar", kirim("/kategori/tambah", nama_kategori="Penjualan", jenis_default="pemasukan"))
ada("berhasil diubah", kirim("/kategori/2/ubah", nama_kategori="Operasional Toko", jenis_default="pengeluaran"))
assert c.get("/kategori/999/ubah").status_code == 404

ada("Belum ada data transaksi", c.get("/transaksi"))
ada("berhasil disimpan", kirim("/transaksi/tambah", tanggal="2026-11-23", jenis="pemasukan", kategori_id=1, keterangan="Penjualan harian", nominal=250000))
ada("berhasil disimpan", kirim("/transaksi/tambah", tanggal="2026-11-23", jenis="pengeluaran", kategori_id=2, keterangan="Diskon 100% bahan", nominal=50000))
ada("lebih dari 0", kirim("/transaksi/tambah", tanggal="2026-11-23", jenis="pemasukan", kategori_id=1, keterangan="Tes", nominal=-5))
ada("TTTT-BB-HH", kirim("/transaksi/tambah", tanggal="10-11-2026", jenis="pemasukan", kategori_id=1, keterangan="Tes", nominal=1000))
ada("tidak ditemukan", kirim("/transaksi/tambah", tanggal="2026-11-23", jenis="pemasukan", kategori_id=999, keterangan="Tes", nominal=1000))
assert models.ringkasan_saldo()["saldo"] == 200000

hasil = c.get("/transaksi?q=HARIAN")
ada("Penjualan harian", hasil)
assert "Diskon 100% bahan" not in hasil.text
ada("Diskon 100% bahan", c.get("/transaksi?q=%25"))
ada("Tidak ada transaksi yang cocok", c.get("/transaksi?q=' OR 1=1 --"))

jumlah_kat_awal = len(models.semua_kategori())
try:
    models.tambah_kategori_dan_transaksi("Gagal", "umum", "2026-11-23", "pemasukan", "Tes", 1000, pengguna_id=999)
except sqlite3.IntegrityError:
    pass
assert len(models.semua_kategori()) == jumlah_kat_awal

assert c.post("/kategori/1/hapus", data={}).status_code == 400  # tanpa CSRF
ada("tidak dapat dihapus", kirim("/kategori/1/hapus"))
assert c.get("/kategori/1/hapus").status_code == 405
ada("berhasil dihapus", kirim("/kategori/3/hapus"))

res_csv = c.get("/ekspor")
assert res_csv.status_code == 200 and "text/csv" in res_csv.content_type

# --- 5. Uji Logout & Peran Terbatas (Kasir) ---
ada("Anda telah keluar.", kirim("/logout"))
assert c.get("/transaksi").status_code == 302

masuk("kasir_uji", "sandi_kasir_123")
assert c.get("/transaksi").status_code == 200
assert c.get("/kategori").status_code == 403
assert c.get("/ekspor").status_code == 403
assert kirim("/transaksi/1/hapus", ikuti=False).status_code == 403
assert models.ambil_transaksi(1) is not None

# --- 6. Uji Batas Percobaan Login (429) & Kedaluwarsa ---
korban = aplikasi.app.test_client()
for _ in range(percobaan.BATAS):
    r_gagal = kirim("/login", klien=korban, ikuti=False, username="kasir_uji", password="salah")
    assert r_gagal.status_code == 401
r_kunci = kirim("/login", klien=korban, ikuti=False, username="kasir_uji", password="sandi_kasir_123")
assert r_kunci.status_code == 429 and "Terlalu banyak percobaan" in r_kunci.text

# Uji fungsi percobaan.py langsung dengan argumen waktu (kedaluwarsa 300 detik)
percobaan.reset("uji|waktu")
for _ in range(percobaan.BATAS):
    percobaan.catat_gagal("uji|waktu", sekarang=1000)
assert percobaan.terkunci("uji|waktu", sekarang=1100) is True
assert percobaan.terkunci("uji|waktu", sekarang=1301) is False

print("SEMUA UJI LULUS")