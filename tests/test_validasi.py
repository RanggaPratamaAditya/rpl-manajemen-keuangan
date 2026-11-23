"""Uji partisi ekuivalen dan nilai batas untuk aturan validasi (services.py)."""
import pytest

import services


def transaksi(**ubah):
    form = {
        "tanggal": "2026-11-23",
        "jenis": "pemasukan",
        "keterangan": "Penjualan harian",
        "nominal": "150000",
        "kategori_id": "1",
    }
    form.update(ubah)
    return form


# TC-01..TC-12: nominal transaksi (batas valid 1..1.000.000.000)
@pytest.mark.parametrize(
    "nominal, valid",
    [
        ("1", True),              # TC-01: batas bawah
        ("2", True),              # TC-02: tepat di atas batas bawah
        ("150000", True),         # TC-03: nilai tipikal
        (" 5000 ", True),         # TC-04: spasi pinggir dipangkas
        ("1000000000", True),     # TC-05: batas atas
        ("0", False),             # TC-06: tepat di bawah batas bawah
        ("-500", False),          # TC-07: negatif
        ("12.5", False),          # TC-08: pecahan
        ("abc", False),           # TC-09: bukan angka
        ("", False),              # TC-10: kosong
        ("1000000001", False),    # TC-11: di atas batas atas
        ("²", False),             # TC-12: angka Unicode
    ],
)
def test_nominal_transaksi(nominal, valid):
    data, galat = services.validasi_transaksi(transaksi(nominal=nominal))
    assert (galat == []) is valid
    if valid:
        assert data["nominal"] == int(nominal.strip())


# TC-13..TC-15: nama kategori (1..50 karakter)
@pytest.mark.parametrize(
    "nama, valid",
    [
        ("Penjualan", True),      # TC-13: normal
        ("a" * 50, True),         # TC-14a: batas atas
        ("a" * 51, False),        # TC-14b: di atas batas atas
        ("   ", False),           # TC-15: hanya spasi
    ],
)
def test_nama_kategori(nama, valid):
    _, galat = services.validasi_kategori({"nama_kategori": nama, "jenis_default": "pemasukan"})
    assert (galat == []) is valid


# TC-16..TC-19: tanggal transaksi (wajib format TTTT-BB-HH)
@pytest.mark.parametrize(
    "tanggal, valid",
    [
        ("2026-11-23", True),     # TC-16: normal ISO
        ("2026-02-30", False),    # TC-17: tanggal kalender tidak valid
        ("23-11-2026", False),    # TC-18: urutan DD-MM-YYYY salah
        ("20261123", False),      # TC-19: tanpa tanda hubung
    ],
)
def test_tanggal_transaksi(tanggal, valid):
    _, galat = services.validasi_transaksi(transaksi(tanggal=tanggal))
    assert (galat == []) is valid


# TC-20: nama pengguna (3-30 karakter) dan kata sandi (minimal 8 karakter)
@pytest.mark.parametrize(
    "username, password, valid",
    [
        ("abc", "12345678", True),     # TC-20a: batas bawah keduanya
        ("ab", "12345678", False),     # TC-20b: username 2 karakter
        ("a" * 30, "12345678", True),  # TC-20c: batas atas username
        ("a" * 31, "12345678", False), # TC-20d: username 31 karakter
        ("abc", "1234567", False),     # TC-20e: sandi 7 karakter
    ],
)
def test_pengguna_baru(username, password, valid):
    assert (services.validasi_pengguna_baru(username, password, "kasir") == []) is valid