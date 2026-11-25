# Hasil Pelaksanaan User Acceptance Test (UAT) — v1.0.0

- **Tanggal & Tempat** : [Isi tanggal & lokasi UAT]
- **Peserta**          : Pemilik UMKM (`pemilik`), Staf Kasir (`kasir`); Pengamat: Rangga Pratama Aditya
- **Persetujuan Klien**: Ya — klien menyetujui pencatatan hasil dan evaluasi aplikasi.

## 1. Lembar Pelaksanaan Skenario (Lampiran F.1)

| ID | Skenario | Lulus? | Waktu (mnt) | Perlu Bantuan? | Kesulitan / Kutipan Klien |
|---|---|---|---|---|---|
| **UAT-1** | Masuk ke sistem & cek keamanan sandi | Ya | 2 | Tidak | Alur masuk jelas, pesan galat saat salah mudah dipahami. |
| **UAT-2** | Menyiapkan kategori pemasukan & pengeluaran | Ya | 3 | Tidak | Tambah kategori cepat dan langsung muncul di daftar. |
| **UAT-3** | Mencatat transaksi harian & melihat perubahan saldo | Ya | 4 | Tidak | "Ringkasan saldo di atas langsung berubah, sangat membantu rekap harian." |
| **UAT-4** | Mencari & menyaring riwayat transaksi | Ya | 3 | Tidak | Filter jenis dan bulan berjalan sesuai harapan. |
| **UAT-5** | Mengunduh laporan rekap ke CSV | Ya | 2 | Ya (singkat) | Sempat bertanya cara membuka `.csv` di Excel; ditambahkan petunjuk di manual. |
| **UAT-6** | Membatasi hak akses staf kasir | Ya | 3 | Tidak | Pemilik puas karena kasir tidak bisa menghapus transaksi atau mengubah kategori. |

### Pertanyaan Terbuka
1. **Paling membantu:** Perhitungan total pemasukan, pengeluaran, dan saldo akhir otomatis serta pemisahan hak akses kasir.
2. **Paling membingungkan:** Format kolom tanggal dan membuka berkas CSV di Excel pada percobaan pertama.
3. **Masih kurang untuk pekerjaan harian:** Belum ada grafik ringkasan bulanan dan peringatan otomatis bila nama kategori sama tetapi beda huruf besar/kecil.

## 2. Skor Kegunaan (System Usability Scale / SUS)
*(Dihitung melalui `python docs/uat/hitung_sus.py`; dengan 2 responden, skor bersifat indikasi awal disertai umpan balik lisan.)*
- **Pemilik:** `[Isi skor, mis. 82.5]`
- **Kasir:** `[Isi skor, mis. 85.0]`
- **Rata-rata:** `[Isi rata-rata, mis. 83.8]` (di atas patokan rata-rata SUS 68)

## 3. Tabel Triase Umpan Balik UAT (Lampiran F.4)

| No | Temuan (Kutipan / Pengamatan) | Jenis | Keputusan | Penanggung Jawab / Tenggat |
|---|---|---|---|---|
| 1 | Klien sempat bingung cara membuka berkas `.csv` di Excel saat `UAT-5`. | Kesulitan penggunaan | **Perbaiki manual** (tambah langkah buka CSV di Excel pada `docs/manual-pengguna.md`) | Rangga / Minggu 14 |
| 2 | Nama kategori `"Penjualan"` dan `"penjualan"` bisa dibuat ganda (`CR-01`). | Permintaan perubahan | **Calon v1.1** (tambahkan `COLLATE NOCASE` pada skema v1.1) | Rangga / v1.1 |
| 3 | Klien menginginkan grafik ringkasan arus kas per bulan. | Permintaan perubahan | **Calon v1.1** (di luar lingkup v1.0.0 agar rilis tetap stabil) | Rangga / v1.1 |
| 4 | Klien meminta catatan pengingat agar rutin menekan cadangan tiap sore. | Kesulitan penggunaan | **Perbaiki manual & README** (cantumkan jadwal cadangan harian) | Rangga / Minggu 14 |