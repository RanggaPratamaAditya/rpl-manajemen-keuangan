import sqlite3

db = sqlite3.connect(":memory:")
db.execute("PRAGMA foreign_keys = ON")
db.executescript(open("docs/desain/schema.sql", encoding="utf-8").read())

tabel = [
    r[0]
    for r in db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )
]
print("Tabel:", ", ".join(tabel))
for t in tabel:
    print(f"[{t}]")
    for c in db.execute(f"PRAGMA table_info({t})"):
        print("  ", c[1], c[2], "NOT NULL" if c[3] else "", "PK" if c[5] else "")
    for f in db.execute(f"PRAGMA foreign_key_list({t})"):
        print("   FK:", f[3], "->", f[2] + "." + f[4])

# Data awal fiktif valid agar setiap uji pelanggaran menyentuh batasan yang tepat
db.execute(
    "INSERT INTO pengguna(username, password_hash, peran) VALUES ('pemilik_uji', 'hash_dummy_123', 'pemilik')"
)
db.execute(
    "INSERT INTO kategori(nama_kategori, jenis_default) VALUES ('Operasional', 'pengeluaran')"
)

# Uji pelanggaran: setiap perintah di bawah HARUS DITOLAK
UJI = [
    (
        "nominal 0 atau negatif",
        "INSERT INTO transaksi(tanggal, jenis, keterangan, nominal, kategori_id, pengguna_id) "
        "VALUES ('2026-11-22', 'pemasukan', 'Tes nominal nol', 0, 1, 1)",
    ),
    (
        "FK kategori tidak ada",
        "INSERT INTO transaksi(tanggal, jenis, keterangan, nominal, kategori_id, pengguna_id) "
        "VALUES ('2026-11-22', 'pengeluaran', 'Tes FK palsu', 15000, 99, 1)",
    ),
    (
        "username ganda (UNIQUE)",
        "INSERT INTO pengguna(username, password_hash, peran) "
        "VALUES ('pemilik_uji', 'hash_lain_456', 'kasir')",
    ),
    (
        "jenis transaksi di luar daftar",
        "INSERT INTO transaksi(tanggal, jenis, keterangan, nominal, kategori_id, pengguna_id) "
        "VALUES ('2026-11-22', 'hutang', 'Tes jenis salah', 10000, 1, 1)",
    ),
    (
        "keterangan lebih dari 50 karakter",
        "INSERT INTO transaksi(tanggal, jenis, keterangan, nominal, kategori_id, pengguna_id) "
        "VALUES ('2026-11-22', 'pengeluaran', 'Keterangan ini sengaja dibuat sangat panjang melebihi lima puluh karakter', 10000, 1, 1)",
    ),
]

print("\n--- Hasil Uji Pelanggaran ---")
for ket, sql in UJI:
    try:
        db.execute(sql)
        print("GAGAL (seharusnya ditolak):", ket)
    except sqlite3.Error as e:
        print("OK ditolak:", ket, "->", e)