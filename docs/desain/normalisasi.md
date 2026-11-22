# Normalisasi Basis Data (1NF – 3NF) — Sistem Manajemen Keuangan UMKM

## 1. Bentuk Tak Ternormalisasi (UNF — Data Mentah Buku Kas Harian)
Satu halaman buku kas harian UMKM mencatat banyak transaksi dalam satu baris/kelompok berulang (data fiktif/anonim):

| kode_halaman | tanggal | username | peran | rincian_transaksi (jenis, kategori, jenis_default, keterangan, nominal) |
|---|---|---|---|---|
| BK-001 | 2026-11-20 | pemilik_a | pemilik | pemasukan - Penjualan (pemasukan) - Penjualan harian (250000); pengeluaran - Bahan Baku (pengeluaran) - Beli bahan (150000) |
| BK-002 | 2026-11-21 | kasir_a | kasir | pengeluaran - Operasional (pengeluaran) - Bayar listrik (100000) |

## 2. Tahap Normalisasi Bertahap

| Bentuk | Hasil Skema | Masalah yang Diperbaiki |
|---|---|---|
| **1NF** | `BUKU_KAS_1NF(kode_halaman, no_baris, tanggal, username, peran, jenis, nama_kategori, jenis_default, keterangan, nominal)` — PK gabungan `(kode_halaman, no_baris)`. | Kolom `rincian_transaksi` berisi banyak nilai sekaligus (tidak atomik). Kelompok berulang dipecah menjadi satu baris per transaksi. |
| **2NF** | `CATATAN_HARIAN(kode_halaman, tanggal, username, peran)` dan `DETAIL_KAS(kode_halaman, no_baris, jenis, nama_kategori, jenis_default, keterangan, nominal)`. | Kolom `tanggal`, `username`, dan `peran` hanya bergantung pada sebagian kunci utama (`kode_halaman`), bukan pada keseluruhan kunci `(kode_halaman, no_baris)` (ketergantungan sebagian). |
| **3NF** | `PENGGUNA(id, username, password_hash, peran)`; `KATEGORI(id, nama_kategori, jenis_default)`; `TRANSAKSI(id, tanggal, jenis, keterangan, nominal, kategori_id -> KATEGORI, pengguna_id -> PENGGUNA)`. | Menghilangkan ketergantungan transitif: `peran` bergantung pada `username` (non-kunci) sehingga dipindah ke tabel `PENGGUNA`; `jenis_default` bergantung pada `nama_kategori` (non-kunci) sehingga dipindah ke tabel `KATEGORI`. |

## 3. Penyesuaian Akhir terhadap ERD
- Karena pada aplikasi web setiap transaksi dicatat langsung per kejadian tanpa mengelompokkan halaman kertas, kunci gabungan `(kode_halaman, no_baris)` disederhanakan menjadi kunci utama otomatis `id` pada tabel `TRANSAKSI`.
- Entitas tambahan `ANGGARAN_BULANAN(id, bulan, kategori_id -> KATEGORI, batas_nominal, pengguna_id -> PENGGUNA)` juga sudah memenuhi 3NF karena seluruh kolom non-kunci (`batas_nominal`, `pengguna_id`) hanya bergantung penuh pada `id` (dan kunci unik `bulan, kategori_id`).
- Seluruh hasil 3NF konsisten 100% dengan 4 entitas pada `docs/desain/erd.mmd`.