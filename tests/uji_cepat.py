"""Uji regresi cepat: jalankan `python tests/uji_cepat.py` dari folder proyek.
Memakai basis data sementara sehingga keuangan.db asli tidak tersentuh."""
import sqlite3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import models

models.DB_PATH = Path(tempfile.mkdtemp()) / "uji.db"
import app as aplikasi

# Siapkan 1 pengguna fiktif pada DB sementara agar FK pengguna_id=1 valid
with models.koneksi() as db:
    db.execute(
        "INSERT INTO pengguna (username, password_hash, peran) VALUES (?, ?, ?)",
        ("pemilik_uji", "hash_uji", "pemilik"),
    )

c = aplikasi.app.test_client()


def kirim(url, **data):
    return c.post(url, data=data, follow_redirects=True)


def ada(teks, hasil):
    assert teks in hasil.text, f"Tidak ditemukan: {teks!r}"


# --- 1. Modul Kategori (CRUD) ---
ada("Belum ada data kategori", c.get("/kategori"))
for nama, jenis in [("Penjualan", "pemasukan"), ("Operasional", "pengeluaran"), ("Lainnya", "umum")]:
    ada("berhasil ditambahkan", kirim("/kategori/tambah", nama_kategori=nama, jenis_default=jenis))
ada("sudah terdaftar", kirim("/kategori/tambah", nama_kategori="Penjualan", jenis_default="pemasukan"))
ada("berhasil diubah", kirim("/kategori/2/ubah", nama_kategori="Operasional Toko", jenis_default="pengeluaran"))
assert c.get("/kategori/999/ubah").status_code == 404

# --- 2. Modul Transaksi (Relasi JOIN & Validasi) ---
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
# Uji masukan tidak valid
ada("lebih dari 0", kirim("/transaksi/tambah", tanggal="2026-11-23", jenis="pemasukan", kategori_id=1, keterangan="Tes", nominal=-5))
ada("TTTT-BB-HH", kirim("/transaksi/tambah", tanggal="10-11-2026", jenis="pemasukan", kategori_id=1, keterangan="Tes", nominal=1000))
ada("tidak ditemukan", kirim("/transaksi/tambah", tanggal="2026-11-23", jenis="pemasukan", kategori_id=999, keterangan="Tes", nominal=1000))
ada("Pilih kategori", kirim("/transaksi/tambah", tanggal="2026-11-23", jenis="pemasukan", kategori_id="", keterangan="Tes", nominal=1000))
assert models.ringkasan_saldo()["saldo"] == 200000

# --- 3. Pencarian & Penyaringan ---
hasil = c.get("/transaksi?q=HARIAN")
ada("Penjualan harian", hasil)
assert "Diskon 100% bahan" not in hasil.text

hasil = c.get("/transaksi?jenis=pengeluaran")
ada("Diskon 100% bahan", hasil)
assert "Penjualan harian" not in hasil.text

hasil = c.get("/transaksi?q=%25")  # tanda % dicari secara harfiah
ada("Diskon 100% bahan", hasil)
assert "Penjualan harian" not in hasil.text

ada("Tidak ada transaksi yang cocok", c.get("/transaksi?q=' OR 1=1 --"))

# --- 4. Uji Atomisitas Transaksi Dua Tabel ---
jumlah_kat_awal = len(models.semua_kategori())
try:
    models.tambah_kategori_dan_transaksi("Gagal", "umum", "2026-11-23", "pemasukan", "Tes", 1000, pengguna_id=999)
except sqlite3.IntegrityError:
    pass
assert len(models.semua_kategori()) == jumlah_kat_awal

# --- 5. Uji Kunci Asing & Metode Hapus ---
ada("tidak dapat dihapus", kirim("/kategori/1/hapus"))  # Penjualan sudah dipakai transaksi
assert c.get("/kategori/1/hapus").status_code == 405
ada("berhasil dihapus", kirim("/kategori/3/hapus"))     # Lainnya belum dipakai

# --- 6. Uji Ekspor CSV (KF-10) ---
res_csv = c.get("/ekspor")
assert res_csv.status_code == 200
assert "text/csv" in res_csv.content_type
assert "Tanggal,Jenis,Kategori,Keterangan,Nominal" in res_csv.text

print("SEMUA UJI LULUS")