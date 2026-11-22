# Kamus Data — Sistem Manajemen Keuangan UMKM

## 1. Tabel `pengguna`
| Kolom | Tipe | Wajib | Kunci | Aturan nilai | Sumber |
|---|---|---|---|---|---|
| `id` | INTEGER | Ya | PK | Otomatis (`AUTOINCREMENT`) | — |
| `username` | TEXT | Ya | UK | Unik; tidak kosong | SRS Bag. 2 |
| `password_hash` | TEXT | Ya | — | Disimpan dalam bentuk hash, bukan teks asli | Aturan keamanan |
| `peran` | TEXT | Ya | — | Hanya `'pemilik'` atau `'kasir'` | SRS Bag. 2, PRD Bag. 2 |

## 2. Tabel `kategori`
| Kolom | Tipe | Wajib | Kunci | Aturan nilai | Sumber |
|---|---|---|---|---|---|
| `id` | INTEGER | Ya | PK | Otomatis (`AUTOINCREMENT`) | — |
| `nama_kategori` | TEXT | Ya | UK | Unik; tidak kosong (mis. Penjualan, Bahan Baku, Operasional, Listrik/Air, Lainnya) | KF-07 |
| `jenis_default` | TEXT | Ya | — | Hanya `'pemasukan'`, `'pengeluaran'`, atau `'umum'` (bawaan `'umum'`) | KF-07 |

## 3. Tabel `transaksi`
| Kolom | Tipe | Wajib | Kunci | Aturan nilai | Sumber |
|---|---|---|---|---|---|
| `id` | INTEGER | Ya | PK | Otomatis (`AUTOINCREMENT`) | — |
| `tanggal` | TEXT | Ya | — | Format ISO `YYYY-MM-DD`; tidak kosong | KF-01, KF-03, KF-08 |
| `jenis` | TEXT | Ya | — | Hanya `'pemasukan'` atau `'pengeluaran'` | KF-01, KF-03 |
| `keterangan` | TEXT | Ya | — | Tidak kosong; panjang 1–50 karakter (`LENGTH(TRIM(keterangan)) BETWEEN 1 AND 50`) | KF-02, KNF-02, KF-06, KF-09 |
| `nominal` | INTEGER | Ya | — | `> 0`; rupiah bulat tanpa desimal | KF-01, KF-02, KF-03, KF-04 |
| `kategori_id` | INTEGER | Ya | FK | Merujuk `kategori(id)` | KF-07 |
| `pengguna_id` | INTEGER | Ya | FK | Merujuk `pengguna(id)` | SRS Bag. 2, UC-01 |

## 4. Tabel `anggaran_bulanan`
| Kolom | Tipe | Wajib | Kunci | Aturan nilai | Sumber |
|---|---|---|---|---|---|
| `id` | INTEGER | Ya | PK | Otomatis (`AUTOINCREMENT`) | — |
| `bulan` | TEXT | Ya | UK* | Format `YYYY-MM` (panjang 7 karakter); unik bersama `kategori_id` | KF-12 |
| `kategori_id` | INTEGER | Ya | FK, UK* | Merujuk `kategori(id)`; unik bersama `bulan` | KF-12 |
| `batas_nominal` | INTEGER | Ya | — | `> 0`; rupiah bulat tanpa desimal | KF-12 |
| `pengguna_id` | INTEGER | Ya | FK | Merujuk `pengguna(id)` | KF-12 |