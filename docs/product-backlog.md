# Product Backlog — Sistem Manajemen Keuangan UMKM (Diperbarui Jobsheet 4)

## 1. Daftar Backlog Fitur (Must dan Should)
| No | ID kebutuhan | Butir backlog | Prioritas | Sprint tentatif |
|---|---|---|---|---|
| 1 | KF-01, KF-02 | Formulir dan logika pencatatan pemasukan harian beserta validasi input | Must | Sprint 1 |
| 2 | KF-02, KF-03 | Logika pencatatan pengeluaran harian beserta validasi nominal | Must | Sprint 1 |
| 3 | KF-04 | Kartu ringkasan otomatis total pemasukan, pengeluaran, dan saldo akhir | Must | Sprint 1 |
| 4 | KF-05 | Fitur hapus transaksi salah input dan pembaruan saldo otomatis | Must | Sprint 1 |
| 5 | KF-06 | Fitur ubah (edit) keterangan dan nominal transaksi tersimpan | Must | Sprint 1 |
| 6 | KNF-01, KNF-02 | Penyimpanan lokal tanpa internet, sanitasi tampilan HTML, dan batas 50 karakter server | Must | Sprint 1 |
| 7 | KF-07 | Penambahan pilihan kategori transaksi dan kolom kategori pada tabel riwayat | Must | Sprint 2 |
| 8 | KF-08 | Filter riwayat transaksi berdasarkan bulan dan tahun beserta subtotal periode | Should | Sprint 2 |
| 9 | KF-09 | Kotak pencarian transaksi berdasarkan kata kunci keterangan | Should | Sprint 2 |
| 10 | KF-10 | Fitur ekspor daftar transaksi yang tampil ke berkas CSV | Should | Sprint 3 |

## 2. Rincian Tugas Kecil Sprint 1 (Maksimal 1 Hari Kerja per Tugas)
| Sprint | ID kebutuhan | Tugas kecil | Alasan |
|---|---|---|---|
| Sprint 1 | KNF-01 | Menyiapkan struktur penyimpanan data lokal (JSON/SQLite) untuk entitas Transaksi | Fondasi penyimpanan agar data aman saat offline |
| Sprint 1 | KF-01, KF-03 | Membuat rute `POST /` untuk menyimpan transaksi pemasukan dan pengeluaran | Fungsi pencatatan inti harian klien |
| Sprint 1 | KF-02, KNF-02 | Menambahkan validasi server (keterangan tidak kosong, maks. 50 karakter, nominal > 0) | Mencegah data rusak dan menjaga keamanan masukan |
| Sprint 1 | KF-04 | Membuat fungsi hitung total pemasukan, pengeluaran, dan saldo akhir di beranda | Menyelesaikan masalah hitung kalkulator manual |
| Sprint 1 | KF-05 | Menambahkan rute hapus transaksi berdasarkan ID dan memperbarui penyimpanan | Memungkinkan koreksi cepat bila salah input |
| Sprint 1 | KF-06 | Membuat halaman/rute ubah transaksi untuk mengedit keterangan dan nominal | Memperbaiki salah ketik tanpa input ulang |