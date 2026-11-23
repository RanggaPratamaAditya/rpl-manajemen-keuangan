"""Uji asap pertama dengan pytest."""
import services


def test_validasi_kategori_normal():
    data, galat = services.validasi_kategori(
        {"nama_kategori": "Penjualan", "jenis_default": "pemasukan"}
    )
    assert galat == []
    assert data["nama_kategori"] == "Penjualan"