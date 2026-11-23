import sqlite3
import os
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(os.environ.get("KEUANGAN_DB") or Path(__file__).with_name("keuangan.db"))
SCHEMA = Path(__file__).parent / "docs" / "desain" / "schema.sql"


@contextmanager
def koneksi():
    """Buka koneksi SQLite, aktifkan kunci asing, commit jika sukses, rollback jika gagal."""
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
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
                   t.kategori_id, k.nama_kategori AS nama_kategori
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


def tambah_kategori_dan_transaksi(
    nama_kategori, jenis_default, tanggal, jenis, keterangan, nominal, pengguna_id=1
):
    """Buat kategori baru sekaligus catat transaksi pertamanya dalam satu transaksi atomik."""
    with koneksi() as db:
        cur = db.execute(
            "INSERT INTO kategori (nama_kategori, jenis_default) VALUES (?, ?)",
            (nama_kategori, jenis_default),
        )
        kategori_id_baru = cur.lastrowid
        db.execute(
            """
            INSERT INTO transaksi (tanggal, jenis, keterangan, nominal, kategori_id, pengguna_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (tanggal, jenis, keterangan, nominal, kategori_id_baru, pengguna_id),
        )

def _escape_like(teks):
    """Netralkan % dan _ agar dicari sebagai huruf biasa pada LIKE."""
    return teks.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def cari_transaksi(kata="", jenis="", bulan=""):
    """Daftar transaksi dengan JOIN kategori, opsional pencarian dan penyaringan."""
    sql = (
        "SELECT t.id, t.tanggal, t.jenis, t.keterangan, t.nominal, "
        "       t.kategori_id, k.nama_kategori "
        "FROM transaksi t "
        "JOIN kategori k ON k.id = t.kategori_id "
        "WHERE t.keterangan LIKE ? ESCAPE '\\'"
    )
    param = ["%" + _escape_like(kata) + "%"]

    if jenis in ("pemasukan", "pengeluaran"):
        sql += " AND t.jenis = ?"
        param.append(jenis)
    if bulan and len(bulan) == 7:
        sql += " AND substr(t.tanggal, 1, 7) = ?"
        param.append(bulan)

    sql += " ORDER BY t.tanggal DESC, t.id DESC"
    with koneksi() as db:
        return db.execute(sql, param).fetchall()

def cari_pengguna(username):
    with koneksi() as db:
        return db.execute(
            "SELECT id, username, password_hash, peran FROM pengguna WHERE username = ?",
            (username,),
        ).fetchone()


def ambil_pengguna(pengguna_id):
    with koneksi() as db:
        return db.execute(
            "SELECT id, username, peran FROM pengguna WHERE id = ?",
            (pengguna_id,),
        ).fetchone()


def tambah_pengguna(username, password_hash, peran):
    with koneksi() as db:
        db.execute(
            "INSERT INTO pengguna (username, password_hash, peran) VALUES (?, ?, ?)",
            (username, password_hash, peran),
        )