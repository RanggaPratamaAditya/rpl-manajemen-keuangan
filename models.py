import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).with_name("keuangan.db")
SCHEMA = Path(__file__).parent / "docs" / "desain" / "schema.sql"


@contextmanager
def koneksi():
    """Buka koneksi SQLite, aktifkan kunci asing, lalu commit dan tutup."""
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    try:
        yield db
        db.commit()
    finally:
        db.close()


def init_db():
    """Buat basis data dari schema.sql bila belum ada."""
    if not DB_PATH.exists():
        with koneksi() as db:
            db.executescript(SCHEMA.read_text(encoding="utf-8"))

def semua_kategori():
    with koneksi() as db:
        return db.execute(
            "SELECT id, nama_kategori, jenis_default FROM kategori ORDER BY nama_kategori"
        ).fetchall()

def tambah_kategori(nama_kategori, jenis_default):
    with koneksi() as db:
        db.execute(
            "INSERT INTO kategori (nama_kategori, jenis_default) VALUES (?, ?)",
            (nama_kategori, jenis_default),
        )

def ambil_kategori(kategori_id):
    with koneksi() as db:
        return db.execute(
            "SELECT id, nama_kategori, jenis_default FROM kategori WHERE id = ?",
            (kategori_id,),
        ).fetchone()


def ubah_kategori(kategori_id, nama_kategori, jenis_default):
    with koneksi() as db:
        db.execute(
            "UPDATE kategori SET nama_kategori = ?, jenis_default = ? WHERE id = ?",
            (nama_kategori, jenis_default, kategori_id),
        )