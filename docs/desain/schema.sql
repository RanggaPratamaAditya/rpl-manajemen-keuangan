PRAGMA foreign_keys = ON;

CREATE TABLE pengguna (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE CHECK (LENGTH(TRIM(username)) > 0),
    password_hash TEXT NOT NULL CHECK (LENGTH(TRIM(password_hash)) > 0),
    peran         TEXT NOT NULL CHECK (peran IN ('pemilik', 'kasir'))
);

CREATE TABLE kategori (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_kategori TEXT NOT NULL UNIQUE CHECK (LENGTH(TRIM(nama_kategori)) > 0),
    jenis_default TEXT NOT NULL DEFAULT 'umum' CHECK (jenis_default IN ('pemasukan', 'pengeluaran', 'umum'))
);

CREATE TABLE transaksi (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tanggal     TEXT NOT NULL CHECK (LENGTH(tanggal) = 10),
    jenis       TEXT NOT NULL CHECK (jenis IN ('pemasukan', 'pengeluaran')),
    keterangan  TEXT NOT NULL CHECK (LENGTH(TRIM(keterangan)) BETWEEN 1 AND 50),
    nominal     INTEGER NOT NULL CHECK (nominal > 0),
    kategori_id INTEGER NOT NULL REFERENCES kategori(id),
    pengguna_id INTEGER NOT NULL REFERENCES pengguna(id)
);

CREATE TABLE anggaran_bulanan (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    bulan         TEXT NOT NULL CHECK (LENGTH(bulan) = 7),
    kategori_id   INTEGER NOT NULL REFERENCES kategori(id),
    batas_nominal INTEGER NOT NULL CHECK (batas_nominal > 0),
    pengguna_id   INTEGER NOT NULL REFERENCES pengguna(id),
    UNIQUE (bulan, kategori_id)
);