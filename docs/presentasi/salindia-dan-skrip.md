# Kerangka Salindia & Skrip Presentasi UAS (±20 Menit)
**Proyek:** Sistem Manajemen Keuangan UMKM (`rpl-manajemen-keuangan` v1.0.0)  
**Presenter:** Rangga Pratama Aditya (NIM 23554010008)

---

## A. Kerangka Salindia (13 Slide — Alur Masalah → Solusi → Bukti → Pelajaran)

| Slide | Judul Slide | Pesan Utama (1 Kalimat) | Bukti / Visual pada Slide |
|---|---|---|---|
| 1 | Judul Proyek | Rancang bangun Sistem Manajemen Keuangan UMKM v1.0.0. | Nama proyek, klien UMKM, nama & NIM, tautan repositori GitHub. |
| 2 | Masalah Klien | Pencatatan kas manual rawan salah hitung dan tidak memisahkan wewenang pemilik dengan kasir. | Poin masalah operasional harian UMKM & dampak kesalahan rekap. |
| 3 | Solusi & Kebutuhan | Aplikasi web Flask–SQLite memenuhi 7 kebutuhan fungsional (`KF-01`–`KF-07`) dengan 2 peran. | Tabel ringkas `KF-01`–`KF-07` & perbandingan hak akses `pemilik` vs `kasir`. |
| 4 | Rancangan Sistem | Pemisahan arsitektur 3 lapis (`app.py`, `services.py`, `models.py`) menjaga kode teruji dan aman. | Diagram arsitektur 3 lapis + ERD ringkas (`pengguna`, `kategori`, `transaksi`). |
| 5 | Alur Vibe Coding Terkendali | AI digunakan lewat siklus 6 langkah dengan manusia sebagai peninjau akhir. | Diagram 6 langkah + 1 contoh nyata Entri 70 (`TOKO_DB` CMD → `KEUANGAN_DB` PowerShell). |
| 6 | Demo Hidup — Peran Pemilik | Alur penuh pencatatan transaksi, kelola kategori, ringkasan saldo, dan ekspor CSV. | Demo langsung pada tag `v1.0.0` (cadangan: `01-halaman-masuk.png` – `04-kelola-kategori.png`). |
| 7 | Demo Hidup — Peran Kasir & Keamanan | Bukti pemisahan hak akses (`403 Forbidden`), validasi batas nominal, dan kunci gagal login. | Demo langsung akun kasir (cadangan: `05-tampilan-kasir.png` + log `uji_cepat.py`). |
| 8 | Tinjauan Kode & Keamanan | 4 temuan keamanan OWASP (`T-01`–`T-04`) ditutup secara berlapis di server dan antarmuka. | Tabel `T-01`–`T-04` + cuplikan kode sebelum–sesudah tombol Hapus + token CSRF. |
| 9 | Pengujian Otomatis & Cacat | 24 kasus uji dan 45 uji otomatis `pytest` lulus 100% setelah menutup 3 cacat nilai batas. | Tangkapan layar `45 passed in 1.77s` + ringkasan cacat `D-01`, `D-02`, `D-03`. |
| 10 | UAT & Rilis `v1.0.0` | 6 skenario UAT lulus dengan skor SUS rata-rata 86,3 dan rilis resmi tersedia di GitHub. | Tangkapan layar GitHub Release `v1.0.0`, skor SUS (82,5 & 90,0), dan tabel triase. |
| 11 | Analisis Jurnal Vibe Coding | Dari 70 entri, 31,4% keluaran AI perlu diubah—membuktikan verifikasi manusia tetap krusial. | Grafik/tabel 48 Terima (68,6%), 22 Ubah (31,4%), 0 Tolak + jenis galat dominan. |
| 12 | Keterbatasan & Rencana `v1.1.0` | Rilis `v1.0.0` stabil untuk 1 gerai dengan backlog terukur untuk versi berikutnya. | 3 keterbatasan (akun via CLI, cadangan manual, sampel kecil) & 3 rencana `v1.1.0`. |
| 13 | Penutup & Tanya Jawab | Seluruh kode, dokumentasi, dan rilis `v1.0.0` siap diuji dan dimodifikasi langsung. | Tautan repositori & GitHub Release `v1.0.0`, kesiapan sesi tanya jawab tanpa AI. |

---

## B. Skrip Waktu Presentasi (±20 Menit)

| Waktu | Slide | Fokus Penyampaian |
|---|---|---|
| 0:00 – 2:00 | 1 – 2 | Perkenalan singkat, konteks permasalahan pencatatan kas UMKM, dan tujuan aplikasi. |
| 2:00 – 5:00 | 3 – 5 | Ringkasan `KF-01`–`KF-07`, pemisahan 3 lapis, perubahan rancangan dari Bab 3, dan siklus *vibe coding*. |
| 5:00 – 11:00 | 6 – 7 | **Demo hidup** memakai tag `v1.0.0` dengan Waitress & data karangan: login `pemilik`, tambah kategori, catat transaksi, cek saldo & ekspor CSV, lalu login `kasir` dan buktikan penolakan akses `403` ke `/kategori` atau `/ekspor`. |
| 11:00 – 14:00 | 8 – 9 | Pemaparan 4 temuan keamanan OWASP (`T-01`–`T-04`), pembuktian `45 passed` (`pytest`), dan 3 cacat batas (`D-01`–`D-03`). |
| 14:00 – 17:00 | 10 – 12 | Hasil UAT & SUS (86,3 beserta keterbatasan sampel), rilis `v1.0.0`, analisis kritis 70 entri jurnal, dan rencana `v1.1.0`. |
| 17:00 – 20:00 | 13 | Penutup dan transisi ke sesi **tanya jawab individu serta modifikasi kode tanpa AI**. |