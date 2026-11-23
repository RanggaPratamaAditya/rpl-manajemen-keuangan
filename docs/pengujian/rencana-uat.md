# Rencana User Acceptance Test (UAT)

- **Tujuan**       : Memastikan pemilik usaha dan kasir UMKM dapat menggunakan aplikasi untuk mencatat pemasukan/pengeluaran harian, memantau saldo, menyaring riwayat, dan mengunduh laporan CSV dengan mudah dan akurat.
- **Peserta**      : Pemilik usaha UMKM (peran `pemilik`), staf kasir (peran `kasir`); Pengamat & Pencatat: Rangga Pratama Aditya.
- **Tanggal & Tempat**: Minggu 14 (sesuai konfirmasi jadwal klien), di tempat usaha klien / ruang simulasi; durasi 45 menit.
- **Lingkungan & Data**: Aplikasi berjalan lokal (`http://127.0.0.1:5000`); menggunakan data transaksi karangan dan 2 akun uji (`pemilik` dan `kasir`) tanpa data keuangan pribadi nyata klien.
- **Kriteria Lulus**: Seluruh 6 skenario inti UAT berstatus Lulus, tidak ada cacat dengan keparahan Kritis atau Tinggi yang terbuka, dan klien menandatangani lembar penerimaan.

## Tabel Skenario UAT (Bahasa Klien)

| ID | KF | Skenario (Bahasa Klien) | Langkah Pengujian | Hasil Diharapkan | Lulus? | Catatan |
|---|---|---|---|---|---|---|
| **UAT-1** | KF-07 | Masuk ke sistem dan cek keamanan sandi | 1) Buka aplikasi, coba masukkan sandi salah. 2) Masukkan nama pengguna dan sandi `pemilik` yang benar. | Muncul pesan umum saat salah; berhasil masuk ke halaman Riwayat & Saldo saat benar. | [ ] | |
| **UAT-2** | KF-01 | Menyiapkan kategori pemasukan dan pengeluaran usaha | 1) Buka menu Kategori. 2) Tambahkan kategori `"Penjualan Harian"` (pemasukan) dan `"Belanja Bahan"` (pengeluaran). | Kedua kategori baru tersimpan dan muncul di daftar kategori. | [ ] | |
| **UAT-3** | KF-02, KF-03 | Mencatat transaksi harian dan melihat perubahan saldo | 1) Klik Catat Transaksi, masukkan pemasukan Rp 350.000. 2) Catat pengeluaran Rp 100.000. | Kedua transaksi tampil di daftar dengan nama kategorinya, dan Saldo Akhir otomatis menunjukkan Rp 250.000. | [ ] | |
| **UAT-4** | KF-05 | Mencari dan menyaring riwayat transaksi tertentu | 1) Ketik kata kunci keterangan di kotak pencarian lalu klik Cari. 2) Saring berdasarkan jenis `"pengeluaran"` dan bulan berjalan. | Hanya transaksi yang sesuai kata kunci dan jenis/bulan tersebut yang tampil. | [ ] | |
| **UAT-5** | KF-06 | Mengunduh laporan rekap keuangan ke Excel/CSV | 1) Klik menu Ekspor CSV pada akun `pemilik`. 2) Buka berkas `.csv` yang terunduh. | Berkas rekap terunduh dan memuat kolom Tanggal, Jenis, Kategori, Keterangan, serta Nominal sesuai data. | [ ] | |
| **UAT-6** | KF-04, KF-07 | Membatasi hak akses staf kasir | 1) Keluar dari akun pemilik, masuk sebagai `kasir`. 2) Catat 1 transaksi baru, lalu periksa menu Kategori, Ekspor CSV, dan tombol Hapus. | Kasir dapat mencatat transaksi, tetapi menu Kategori, Ekspor CSV, dan tombol Hapus tidak tersedia (akses langsung ditolak). | [ ] | |

- **Cara Merekam Temuan**: Pengamat mengisi kolom *Lulus?* dan *Catatan* pada lembar ini selama UAT berlangsung; setiap kendala dipindahkan ke `docs/pengujian/laporan-cacat.md` dan diklasifikasikan sebagai cacat atau permintaan perubahan (`CR`).