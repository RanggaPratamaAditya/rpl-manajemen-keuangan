# Rencana Pengujian — Sistem Manajemen Keuangan UMKM

## 1. Tujuan dan Ruang Lingkup
- **Tujuan:** Memastikan seluruh fungsi utama aplikasi pencatatan keuangan UMKM bekerja sesuai spesifikasi kebutuhan pada `docs/srs.md` dan kriteria penerimaan `PRD.md` sebelum diserahkan kepada klien.
- **Ruang lingkup:** Menguji seluruh kebutuhan fungsional berprioritas **Must** (`KF-01` s.d. `KF-07`) dan **Should** (`KF-08` s.d. `KF-10`). Fitur berprioritas *Won't have* berada di luar ruang lingkup pengujian.

## 2. Strategi Pengujian
1. **Uji black-box manual:** Menguji setiap fitur melalui antarmuka web berdasarkan kriteria penerimaan *Given–When–Then* dengan teknik partisi ekuivalen (valid dan tidak valid) serta analisis nilai batas.
2. **Uji otomatis dasar (Minggu 13):** Menguji logika inti pada `services.py` dan integritas skema SQLite pada `models.py` menggunakan skrip uji Python (`pytest` dan `tests/cek_skema.py`).
3. **User Acceptance Testing / UAT (Minggu 13–14):** Pengujian langsung bersama klien menggunakan skenario pencatatan harian untuk memastikan tampilan terbaca dan mudah digunakan.

## 3. Lingkungan, Data Uji, dan Pembagian Tugas
- **Perangkat lunak & keras:** Laptop Windows (Visual Studio Code, Python 3.10+, Flask, SQLite lokal, peramban Chrome/Edge).
- **Data uji:** Menggunakan data karangan (fiktif) tanpa mencantumkan data pribadi, kata sandi asli, atau angka keuangan nyata milik klien.
- **Pembagian tugas penguji:** Pengembang/Mahasiswa (Rangga Pratama Aditya — NIM 23554010008) melaksanakan uji black-box dan uji otomatis; Klien (Pemilik Usaha) melaksanakan UAT pada tahap penerimaan.

## 4. Kriteria Lulus
- 100% *test case* untuk kebutuhan berprioritas **Must** (`TC-01` s.d. `TC-12`) berstatus **Lulus**.
- Jumlah cacat berat (*critical/blocker*, seperti salah hitung saldo atau gagal simpan data valid) = **0**.
- Seluruh pesan galat validasi tampil jelas sesuai rancangan wireframe.

## 5. Daftar Test Case
| ID | KF | Prasyarat / Data Uji | Langkah | Hasil Diharapkan | Teknik |
|---|---|---|---|---|---|
| **TC-01** | KF-01 | Login sebagai Pemilik/Kasir; saldo awal `Rp 0`. Data: `2026-11-22`, Pemasukan, kategori `Penjualan`, ket `"Penjualan harian"`, nominal `250000`. | 1. Buka `wf-03` Catat Transaksi. 2. Isi formulir dengan data uji. 3. Klik `Simpan Transaksi`. | Transaksi tersimpan; muncul pesan `"Transaksi berhasil disimpan"`; saldo akhir di Beranda menjadi `Rp 250.000`. | Partisi valid |
| **TC-02** | KF-02 | Berada di halaman `wf-03`. Data: nominal `1` (tepat di atas batas 0), keterangan `"Tes batas bawah"`. | 1. Isi formulir dengan nominal `1`. 2. Klik `Simpan Transaksi`. | Transaksi diterima dan tersimpan; saldo bertambah `Rp 1`. | Nilai batas (tepat valid) |
| **TC-03** | KF-02 | Berada di halaman `wf-03`. Data: nominal `0` (tepat di batas tidak valid). | 1. Isi formulir dengan nominal `0`. 2. Klik `Simpan Transaksi`. | Ditolak; data tidak tersimpan; tampil pesan `"Nominal harus berupa angka bulat positif"`. | Nilai batas (di batas gagal) |
| **TC-04** | KF-02 | Berada di halaman `wf-03`. Data: nominal `-50000`, keterangan `""` (kosong). | 1. Kosongkan keterangan dan isi nominal `-50000`. 2. Klik `Simpan Transaksi`. | Ditolak; data tidak tersimpan; tampil pesan validasi keterangan wajib diisi dan nominal harus bulat positif. | Partisi tidak valid |
| **TC-05** | KF-02 | Berada di halaman `wf-03`. Data: keterangan tepat `50` karakter, nominal `10000`. | 1. Isi keterangan sepanjang 50 karakter. 2. Klik `Simpan Transaksi`. | Transaksi tersimpan utuh sepanjang 50 karakter tanpa terpotong. | Nilai batas (tepat maks.) |
| **TC-06** | KF-02 | Berada di halaman `wf-03`. Data: keterangan `51` karakter, nominal `10000`. | 1. Isi keterangan sepanjang 51 karakter. 2. Klik `Simpan Transaksi`. | Sistem memotong teks menjadi 50 karakter di server atau menolak penyimpanan sesuai aturan validasi `KNF-02`. | Nilai batas (di atas maks.) |
| **TC-07** | KF-03 | Saldo awal `Rp 250.000`. Data: Pengeluaran, kategori `Bahan Baku`, ket `"Beli bahan"`, nominal `150000`. | 1. Buka `wf-03`. 2. Pilih jenis `Pengeluaran` dan isi data uji. 3. Klik `Simpan Transaksi`. | Pengeluaran tersimpan; total pengeluaran menjadi `Rp 150.000`; saldo akhir berkurang menjadi `Rp 100.000`. | Partisi valid |
| **TC-08** | KF-04 | Terdapat 1 pemasukan `Rp 250.000` dan 1 pengeluaran `Rp 150.000`. | 1. Buka halaman `wf-02` Beranda. 2. Periksa tiga kartu ringkasan saldo. | Total Pemasukan = `Rp 250.000`, Total Pengeluaran = `Rp 150.000`, Saldo Akhir = `Rp 100.000`. | Partisi valid |
| **TC-09** | KF-05 | Login sebagai Pemilik; terdapat transaksi ID #1 (`Rp 150.000`). | 1. Buka `wf-04` Riwayat. 2. Klik `Hapus` pada ID #1. 3. Klik `Ya, Hapus` pada dialog konfirmasi. | Transaksi ID #1 terhapus; tampil pesan `"Transaksi berhasil dihapus"`; saldo akhir kembali `Rp 250.000`. | Partisi valid |
| **TC-10** | KF-05 | Login sebagai Staf Kasir; terdapat transaksi ID #2. | 1. Buka `wf-04` Riwayat. 2. Cek tombol `Hapus` atau akses langsung URL hapus. | Tombol `Hapus` tidak tampil bagi Kasir dan permintaan hapus langsung ditolak (akses ditolak). | Hak akses (tidak valid) |
| **TC-11** | KF-06 | Terdapat transaksi pengeluaran `Rp 100.000` (`Bayar listrik`). | 1. Buka `wf-04` lalu klik `Ubah` (`wf-05`). 2. Ubah nominal menjadi `120000`. 3. Klik `Simpan Perubahan`. | Data transaksi terbarui menjadi `Rp 120.000`; ringkasan saldo otomatis menyesuaikan selisih `-Rp 20.000`. | Partisi valid |
| **TC-12** | KF-07 | Login sebagai Pemilik; kategori `Operasional` sudah terdaftar. | 1. Buka `wf-06` Kelola Kategori. 2. Tambah kategori baru dengan nama `"Operasional"`. | Ditolak; kategori ganda tidak tersimpan; tampil pesan `"Nama kategori sudah terdaftar"`. | Partisi tidak valid |
| **TC-13** | KF-08 | Terdapat transaksi bulan November 2026; tidak ada transaksi bulan Januari 2026. | 1. Buka `wf-04`. 2. Pilih filter `Januari` `2026` lalu klik `Terapkan`. | Tabel kosong dan tampil pesan `"Tidak ada transaksi pada periode ini"`. | Partisi tidak valid |
| **TC-14** | KF-09 | Terdapat transaksi berketerangan `"Bayar listrik"`. | 1. Buka `wf-04`. 2. Ketik `"listrik"` di kotak pencarian lalu klik `Terapkan`. | Hanya baris yang mengandung kata `"listrik"` yang tampil beserta subtotalnya. | Partisi valid |
| **TC-15** | KF-10 | Login sebagai Pemilik; terdapat 2 transaksi pada November 2026. | 1. Buka `wf-07` Ekspor CSV. 2. Pilih `November` `2026`, klik `Tampilkan Pratinjau`, lalu `Unduh Berkas CSV`. | Berkas `.csv` terunduh dan memuat 2 baris data sesuai pratinjau dengan kolom lengkap. | Partisi valid |

### Catatan Verifikasi Draf Test Case dari AI (Langkah 8)
- **Kesalahan AI yang ditemukan:** Pada draf awal, AI menuliskan hasil diharapkan yang tidak terukur (misalnya *"aplikasi berjalan lancar"*), menambahkan *test case* untuk fitur ekspor PDF yang tidak ada di SRS, dan lupa memasukkan nilai batas `nominal = 1` (tepat valid) serta panjang keterangan `50`/`51` karakter.
- **Perbaikan:** Seluruh hasil diharapkan diubah menjadi angka/pesan spesifik yang dapat diverifikasi, *test case* di luar SRS dihapus, dan kasus nilai batas (`TC-02`, `TC-03`, `TC-05`, `TC-06`) ditambahkan.

## 6. Matriks Keterlacakan (KF → Use Case → Halaman → Test Case)
| KF | Use Case | Halaman | Prioritas | Test Case |
|---|---|---|---|---|
| KF-01 | UC-01 | `wf-03` Catat Transaksi | Must | TC-01 |
| KF-02 | UC-02 | `wf-03` Catat Transaksi, `wf-05` Ubah Transaksi | Must | TC-02, TC-03, TC-04, TC-05, TC-06 |
| KF-03 | UC-01 | `wf-03` Catat Transaksi | Must | TC-07 |
| KF-04 | UC-03 | `wf-02` Beranda | Must | TC-08 |
| KF-05 | UC-05 | `wf-04` Riwayat & Filter | Must | TC-09, TC-10 |
| KF-06 | UC-04 | `wf-05` Ubah Transaksi | Must | TC-11 |
| KF-07 | UC-01 | `wf-03` Catat Transaksi, `wf-06` Kelola Kategori | Must | TC-12 |
| KF-08 | UC-06 | `wf-04` Riwayat & Filter | Should | TC-13 |
| KF-09 | UC-06 | `wf-04` Riwayat & Filter | Should | TC-14 |
| KF-10 | UC-07 | `wf-07` Ekspor Rekap CSV | Should | TC-15 |