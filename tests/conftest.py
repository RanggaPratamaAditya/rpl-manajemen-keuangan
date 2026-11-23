"""Fixture bersama untuk semua uji pytest. Memakai basis data sementara,
sehingga keuangan.db asli tidak tersentuh."""
import sys
import tempfile
from pathlib import Path

import pytest
from werkzeug.security import generate_password_hash

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import models

models.DB_PATH = Path(tempfile.mkdtemp()) / "uji.db"  # wajib sebelum import app
import app as aplikasi
import percobaan

SANDI_PEMILIK, SANDI_KASIR = "rahasia-uji-1", "rahasia-uji-2"


@pytest.fixture(autouse=True)
def basis_bersih():
    """Setiap uji mulai dari basis data kosong dengan dua akun peran."""
    models.DB_PATH.unlink(missing_ok=True)
    models.init_db()
    percobaan._gagal.clear()
    cepat = lambda s: generate_password_hash(s, method="pbkdf2:sha256:1000")
    models.tambah_pengguna("bu_pemilik", cepat(SANDI_PEMILIK), "pemilik")
    models.tambah_pengguna("kasir1", cepat(SANDI_KASIR), "kasir")


@pytest.fixture
def kirim():
    """Helper POST yang otomatis menyertakan token CSRF yang sah."""
    def _kirim(c, url, ikuti=True, **data):
        with c.session_transaction() as s:
            s.setdefault("csrf_token", "token-uji")
            token = s["csrf_token"]
        data.setdefault("csrf_token", token)
        return c.post(url, data=data, follow_redirects=ikuti)
    return _kirim


@pytest.fixture
def tamu():
    return aplikasi.app.test_client()


@pytest.fixture
def pemilik(kirim):
    c = aplikasi.app.test_client()
    kirim(c, "/login", username="bu_pemilik", password=SANDI_PEMILIK)
    return c


@pytest.fixture
def kasir(kirim):
    c = aplikasi.app.test_client()
    kirim(c, "/login", username="kasir1", password=SANDI_KASIR)
    return c