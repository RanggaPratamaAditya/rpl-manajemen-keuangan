# Rencana Sprint RTM-2 — Sistem Manajemen Keuangan UMKM

| Sprint | Minggu | Target Modul & Fitur | Luaran / Milestone |
|---|---|---|---|
| **Sprint 1** | Minggu 9–10 | Kerangka proyek, CRUD `kategori` (`KF-07`), CRUD `transaksi` (`KF-01` s.d. `KF-06`), relasi FK, filter periode & pencarian (`KF-08`, `KF-09`), ekspor CSV (`KF-10`). | Fitur CRUD inti dan relasi berjalan di `main` dengan jurnal >= 15 entri. |
| **Sprint 2** | Minggu 11–12 | Penyempurnaan antarmuka sesuai wireframe (`KNF-04`, `KNF-05`), autentikasi 2 peran (`pemilik` & `kasir`) dengan hash sandi, pembatasan hak akses, validasi ketat, *code review* & keamanan (`debug=False`, `SECRET_KEY`). | **Checkpoint Minggu 12:** Aplikasi fitur Must + Should selesai dan lolos tinjauan keamanan. |
| **Sprint 3** | Minggu 13–14 | Eksekusi >= 20 *test case* (`>= 8` uji otomatis `pytest` + `cek_skema.py`), UAT langsung bersama klien, penyusunan `README.md` & manual pengguna, rilis `v1.0`. | Laporan hasil uji, berita acara UAT, dan rilis `v1.0` di GitHub. |
| **Sprint 4** | Minggu 15–16 | Perbaikan temuan UAT, penyusunan **Laporan Bab 4 (Implementasi dan Pengujian)** beserta analisis Jurnal Vibe Coding (>= 30 entri), persiapan demo UAS. | **Progress Check Minggu 15 & Demo UAS Minggu 16.** |

## Rincian Target Sprint 2 (Minggu 11–12 — Checkpoint RTM-2)
1. **Antarmuka sesuai wireframe (`wf-01` s.d. `wf-07`):** Merapikan CSS lokal (ukuran teks >= 16 px, kontras tinggi, tombol kanan bawah, dan tampilan kartu ringkasan saldo di Beranda).
2. **Autentikasi & Hak Akses 2 Peran:** Halaman `/login` dan `/logout` dengan *password hashing* (`werkzeug.security`), pembatasan menu `Kategori`, `Hapus Transaksi`, dan `Ekspor CSV` khusus peran `pemilik`.
3. **Code Review & Keamanan (Minggu 12):** Menghapus `debug=True` saat rilis, memastikan `SECRET_KEY` aman, dan meninjau ulang seluruh rute terhadap daftar periksa keamanan.