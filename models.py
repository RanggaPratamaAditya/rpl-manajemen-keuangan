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

def hapus_kategori(kategori_id):
    with koneksi() as db:
        db.execute("DELETE FROM kategori WHERE id = ?", (kategori_id,))

def semua_transaksi():
    with koneksi() as db:
        return db.execute(
            """
            SELECT t.id, t.tanggal, t.jenis, t.keterangan, t.nominal,
                   t.kategori_id, k.nama_kategori
            FROM transaksi t
            JOIN kategori k ON k.id = t.kategori_id
            ORDER BY t.tanggal DESC, t.id DESC
            """
        ).fetchall()


def ambil_transaksi(transaksi_id):
    with koneksi() as db:
        return db.execute(
            "SELECT * FROM transaksi WHERE id = ?",
            (transaksi_id,),
        ).fetchone()


def ringkasan_saldo():
    with koneksi() as db:
        row = db.execute(
            """
            SELECT
            COALESCE(SUM(CASE WHEN jenis = 'pemasukan' THEN nominal ELSE 0 END), 0) AS total_masuk,
            COALESCE(SUM(CASE WHEN jenis = 'pengeluaran' THEN nominal ELSE 0 END), 0) AS total_keluar
            FROM transaksi
            """
        ).fetchone()
        return {
            "total_masuk": row["total_masuk"],
            "total_keluar": row["total_keluar"],
            "saldo": row["total_masuk"] - row["total_keluar"],
        }


def tambah_transaksi(tanggal, jenis, keterangan, nominal, kategori_id, pengguna_id=1):
    with koneksi() as db:
        db.execute(
            """
            INSERT INTO transaksi (tanggal, jenis, keterangan, nominal, kategori_id, pengguna_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (tanggal, jenis, keterangan, nominal, kategori_id, pengguna_id),
        )


def ubah_transaksi(transaksi_id, tanggal, jenis, keterangan, nominal, kategori_id):
    with koneksi() as db:
        db.execute(
            """
            UPDATE transaksi
            SET tanggal = ?, jenis = ?, keterangan = ?, nominal = ?, kategori_id = ?
            WHERE id = ?
            """,
            (tanggal, jenis, keterangan, nominal, kategori_id, transaksi_id),
        )


def hapus_transaksi(transaksi_id):
    with koneksi() as db:
        db.execute("DELETE FROM transaksi WHERE id = ?", (transaksi_id,))