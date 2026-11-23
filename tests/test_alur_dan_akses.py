"""Uji alur aplikasi, perhitungan saldo, matriks akses, dan keamanan lewat HTTP."""
import sqlite3

import pytest

import models
import percobaan


def _buat_kategori(kirim, pemilik, nama="Penjualan", jenis="pemasukan"):
    kirim(pemilik, "/kategori/tambah", nama_kategori=nama, jenis_default=jenis)
    return [k for k in models.semua_kategori() if k["nama_kategori"] == nama][0]["id"]


# --- (a) & (b) Alur Inti CRUD & Perhitungan Ringkasan Saldo ---
def test_alur_tambah_ubah_hapus_transaksi_dan_saldo(pemilik, kirim):
    kid_masuk = _buat_kategori(kirim, pemilik, "Penjualan", "pemasukan")
    kid_keluar = _buat_kategori(kirim, pemilik, "Operasional", "pengeluaran")

    # 1. Catat pemasukan 250.000 & pengeluaran 50.000 -> saldo harus 200.000
    r1 = kirim(
        pemilik,
        "/transaksi/tambah",
        tanggal="2026-11-23",
        jenis="pemasukan",
        kategori_id=kid_masuk,
        keterangan="Penjualan harian",
        nominal="250000",
    )
    assert "Transaksi berhasil disimpan" in r1.text and "Penjualan harian" in r1.text

    kirim(
        pemilik,
        "/transaksi/tambah",
        tanggal="2026-11-23",
        jenis="pengeluaran",
        kategori_id=kid_keluar,
        keterangan="Beli plastik",
        nominal="50000",
    )
    saldo = models.ringkasan_saldo()
    assert saldo["total_masuk"] == 250000
    assert saldo["total_keluar"] == 50000
    assert saldo["saldo"] == 200000

    # 2. Ubah pemasukan menjadi 300.000 -> saldo harus 250.000
    trx_id = models.semua_transaksi()[-1]["id"]
    r_ubah = kirim(
        pemilik,
        f"/transaksi/{trx_id}/ubah",
        tanggal="2026-11-23",
        jenis="pemasukan",
        kategori_id=kid_masuk,
        keterangan="Penjualan harian revisi",
        nominal="300000",
    )
    assert "Transaksi berhasil diubah" in r_ubah.text
    assert models.ringkasan_saldo()["saldo"] == 250000

    # 3. Hapus transaksi -> saldo kembali -50.000
    r_hapus = kirim(pemilik, f"/transaksi/{trx_id}/hapus")
    assert "Transaksi berhasil dihapus" in r_hapus.text
    assert models.ringkasan_saldo()["saldo"] == -50000


def test_transaksi_atomik_rollback_saat_gagal(pemilik, kirim):
    jumlah_awal = len(models.semua_kategori())
    with pytest.raises(sqlite3.IntegrityError):
        models.tambah_kategori_dan_transaksi(
            "Kategori Batal", "umum", "2026-11-23", "pemasukan", "Tes gagal", 10000, pengguna_id=999
        )
    assert len(models.semua_kategori()) == jumlah_awal


def test_kategori_terpakai_tidak_dapat_dihapus(pemilik, kirim):
    kid = _buat_kategori(kirim, pemilik, "Penjualan", "pemasukan")
    kirim(
        pemilik,
        "/transaksi/tambah",
        tanggal="2026-11-23",
        jenis="pemasukan",
        kategori_id=kid,
        keterangan="Transaksi kunci",
        nominal="10000",
    )
    r = kirim(pemilik, f"/kategori/{kid}/hapus")
    assert "tidak dapat dihapus" in r.text
    assert models.ambil_kategori(kid) is not None


def test_pencarian_persen_dan_sql_injection(pemilik, kirim):
    kid = _buat_kategori(kirim, pemilik, "Promo", "pengeluaran")
    kirim(pemilik, "/transaksi/tambah", tanggal="2026-11-23", jenis="pengeluaran", kategori_id=kid, keterangan="Diskon 100% akhir pekan", nominal="25000")
    kirim(pemilik, "/transaksi/tambah", tanggal="2026-11-23", jenis="pengeluaran", kategori_id=kid, keterangan="Biaya listrik", nominal="75000")

    r_persen = pemilik.get("/transaksi?q=%25")
    assert "Diskon 100% akhir pekan" in r_persen.text
    assert "Biaya listrik" not in r_persen.text

    r_sqli = pemilik.get("/transaksi?q=' OR 1=1 --")
    assert "Tidak ada transaksi yang cocok" in r_sqli.text


def test_ekspor_csv_pemilik(pemilik, kirim):
    kid = _buat_kategori(kirim, pemilik, "Penjualan", "pemasukan")
    kirim(pemilik, "/transaksi/tambah", tanggal="2026-11-23", jenis="pemasukan", kategori_id=kid, keterangan="Order pagi", nominal="120000")
    r = pemilik.get("/ekspor")
    assert r.status_code == 200
    assert "text/csv" in r.content_type
    assert "Tanggal,Jenis,Kategori,Keterangan,Nominal" in r.text
    assert "Order pagi" in r.text


# --- (c) Matriks Akses Rute x Peran (Tamu, Kasir, Pemilik) ---
MATRIKS_AKSES = [
    ("GET", "/transaksi", 302, 200, 200),
    ("GET", "/transaksi/tambah", 302, 200, 200),
    ("GET", "/kategori", 302, 403, 200),
    ("GET", "/kategori/tambah", 302, 403, 200),
    ("GET", "/ekspor", 302, 403, 302),
]

@pytest.mark.parametrize("metode, alamat, utk_tamu, utk_kasir, utk_pemilik", MATRIKS_AKSES)
def test_matriks_akses_rute(tamu, kasir, pemilik, metode, alamat, utk_tamu, utk_kasir, utk_pemilik):
    assert tamu.open(alamat, method=metode).status_code == utk_tamu
    assert kasir.open(alamat, method=metode).status_code == utk_kasir
    assert pemilik.open(alamat, method=metode).status_code == utk_pemilik


def test_kasir_ditolak_hapus_transaksi_post(kasir, pemilik, kirim):
    kid = _buat_kategori(kirim, pemilik, "Penjualan", "pemasukan")
    kirim(pemilik, "/transaksi/tambah", tanggal="2026-11-23", jenis="pemasukan", kategori_id=kid, keterangan="Data aman", nominal="50000")
    trx_id = models.semua_transaksi()[0]["id"]
    assert kirim(kasir, f"/transaksi/{trx_id}/hapus", ikuti=False).status_code == 403
    assert models.ambil_transaksi(trx_id) is not None


# --- (d) Penolakan CSRF & Batas Percobaan Login ---
def test_post_tanpa_token_csrf_ditolak(pemilik, tamu):
    assert tamu.post("/login", data={"username": "kasir1", "password": "rahasia-uji-2"}).status_code == 400
    assert pemilik.post("/kategori/tambah", data={"nama_kategori": "X", "jenis_default": "umum"}).status_code == 400


def test_batas_percobaan_login_429(tamu, kirim):
    for _ in range(percobaan.BATAS):
        r = kirim(tamu, "/login", ikuti=False, username="kasir1", password="salah")
        assert r.status_code == 401
    r_kunci = kirim(tamu, "/login", ikuti=False, username="kasir1", password="rahasia-uji-2")
    assert r_kunci.status_code == 429
    assert "Terlalu banyak percobaan gagal" in r_kunci.text