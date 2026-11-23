"""Uji kebersihan rilis: versi, cadangan, .gitignore, changelog, dan dependensi."""
import re
import sqlite3
from pathlib import Path

import cadangkan
from versi import VERSI

AKAR = Path(__file__).resolve().parent.parent


def test_versi_berformat_semver():
    assert re.fullmatch(r"\d+\.\d+\.\d+", VERSI)


def test_versi_tampil_di_halaman(tamu):
    assert f"v{VERSI}" in tamu.get("/login").text


def test_changelog_memuat_versi_rilis():
    assert f"## [{VERSI}]" in (AKAR / "CHANGELOG.md").read_text(encoding="utf-8")


def test_gitignore_mengecualikan_rahasia_dan_data():
    baris = (AKAR / ".gitignore").read_text(encoding="utf-8").splitlines()
    for wajib in (".env", "keuangan.db", "cadangan/"):
        assert wajib in baris


def test_requirements_dikunci_versinya():
    for baris in (AKAR / "requirements.txt").read_text(encoding="utf-8").splitlines():
        if baris.strip() and not baris.startswith("#"):
            assert "==" in baris, baris


def test_cadangan_berisi_data_yang_sama(pemilik, kirim, tmp_path):
    kirim(pemilik, "/kategori/tambah", nama_kategori="Penjualan", jenis_default="pemasukan")
    berkas = cadangkan.cadangkan(tmp_path)
    db = sqlite3.connect(berkas)
    try:
        assert db.execute(
            "SELECT nama_kategori, jenis_default FROM kategori"
        ).fetchall() == [("Penjualan", "pemasukan")]
    finally:
        db.close()