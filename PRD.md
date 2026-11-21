# PRD — Sistem Manajemen Keuangan UMKM

## 1. Ringkasan dan Tujuan
Aplikasi web lokal untuk usaha mikro/kecil (UMKM) bidang perdagangan/jasa di Sampit guna mencatat pemasukan dan pengeluaran harian serta menghitung total saldo secara otomatis. Aplikasi ini menyelesaikan masalah selisih hitung manual di buku kas dan lamanya proses rekap keuangan bulanan.

## 2. Pengguna dan Peran
- **Pemilik usaha:** Dapat mencatat pemasukan/pengeluaran, mengubah dan menghapus transaksi, melihat ringkasan saldo, menyaring riwayat per bulan, mencari transaksi, dan mengunduh rekap CSV.
- **Staf kasir / admin keuangan:** Dapat mencatat transaksi harian, memperbaiki salah input, dan mencari riwayat transaksi.

## 3. Fitur

### F-01 Pencatatan pemasukan dan pengeluaran harian (Must, Sprint 1) <- KF-01, KF-02, KF-03, US-01, US-02
Kriteria penerimaan:
- Given saldo saat ini Rp 500.000, When pengguna mencatat pemasukan "Penjualan harian" sebesar Rp 250.000, Then transaksi tersimpan dan saldo menjadi Rp 750.000.
- Given saldo saat ini Rp 750.000, When pengguna mencatat pengeluaran "Beli bahan baku" sebesar Rp 150.000, Then transaksi tersimpan dan saldo menjadi Rp 600.000.
- Given formulir terbuka, When pengguna mengirim keterangan kosong atau nominal <= 0, Then sistem menolak penyimpanan dan menampilkan pesan peringatan yang jelas.

### F-02 Ringkasan saldo otomatis (Must, Sprint 1) <- KF-04, US-03
Kriteria penerimaan:
- Given terdapat 2 pemasukan (Rp 300.000 dan Rp 200.000) serta 1 pengeluaran (Rp 120.000), When pengguna membuka halaman utama, Then sistem menampilkan Total Pemasukan Rp 500.000, Total Pengeluaran Rp 120.000, dan Saldo Akhir Rp 380.000.
- Given belum ada transaksi tersimpan, When pengguna membuka halaman utama, Then seluruh angka ringkasan tampil sebagai Rp 0 tanpa galat.

### F-03 Hapus dan ubah transaksi salah input (Must, Sprint 1) <- KF-05, KF-06, US-04, US-05
Kriteria penerimaan:
- Given terdapat transaksi pengeluaran Rp 50.000 dan saldo Rp 450.000, When pengguna menghapus transaksi tersebut, Then baris hilang dari riwayat dan saldo kembali menjadi Rp 500.000.
- Given transaksi "Bayar listrik" tercatat Rp 100.000, When pengguna mengubah nominal menjadi Rp 150.000 dan menyimpan, Then riwayat menampilkan Rp 150.000 dan total pengeluaran bertambah Rp 50.000.

### F-04 Pengelompokan kategori transaksi (Must, Sprint 2) <- KF-07, US-06
Kriteria penerimaan:
- Given daftar kategori tersedia (Penjualan, Bahan Baku, Operasional, Listrik/Air, Lainnya), When pengguna menyimpan pengeluaran Rp 80.000 berkategori "Operasional", Then tabel riwayat menampilkan kategori "Operasional".
- Given pengguna mengisi transaksi tanpa memilih kategori, When formulir dikirim, Then sistem menolak penyimpanan dan meminta kategori dipilih.

### F-05 Filter riwayat per bulan dan pencarian keterangan (Should, Sprint 2) <- KF-08, KF-09, US-07, US-08
Kriteria penerimaan:
- Given terdapat 3 transaksi bulan Oktober dan 4 transaksi bulan November, When pengguna memilih filter "November", Then tabel hanya menampilkan 4 transaksi bulan November beserta total pemasukan dan pengeluaran bulan tersebut.
- Given terdapat 20 transaksi dan 2 di antaranya memuat kata "semen", When pengguna mencari kata "semen", Then tabel hanya menampilkan 2 transaksi tersebut.

### F-06 Ekspor rekap transaksi ke berkas CSV (Should, Sprint 3) <- KF-10, US-09
Kriteria penerimaan:
- Given terdapat 5 transaksi yang sedang tampil, When pengguna mengklik "Unduh CSV", Then peramban mengunduh berkas `.csv` berisi 1 baris header dan 5 baris data yang sesuai.

### F-07 Keandalan lokal dan keamanan masukan (Must, Sprint 1) <- KNF-01, KNF-02, US-10, US-12
Kriteria penerimaan:
- Given komputer klien tidak terhubung internet, When aplikasi dijalankan secara lokal dan transaksi disimpan, Then data tersimpan permanen dan tetap muncul setelah server dijalankan ulang.
- Given pengguna memasukkan `<b>tes</b>` atau teks > 50 karakter pada keterangan, When disimpan, Then teks tampil apa adanya tanpa dieksekusi sebagai HTML dan dipotong maksimal 50 karakter di sisi server.

## 4. Data Awal
- **Transaksi:** `id` (unik), `tanggal` (YYYY-MM-DD), `jenis` (pemasukan/pengeluaran), `kategori` (teks), `keterangan` (teks, maks. 50 karakter), `nominal` (bilangan bulat positif).
- **Kategori:** `id` (unik), `nama_kategori` (teks).

## 5. Di Luar Lingkup
- **Won't have:** Integrasi rekening bank/e-wallet/payment gateway, penghitungan pajak otomatis, modul penggajian karyawan, dan aplikasi ponsel (*mobile native*).
- **Could have (ditunda bila tidak ada sisa waktu):** Halaman panduan `/bantuan` (KF-11) dan peringatan batas anggaran bulanan (KF-12).

## 6. Pertanyaan Terbuka
1. ~~Apakah daftar 5 kategori awal (Penjualan, Bahan Baku, Operasional, Listrik/Air, Lainnya) sudah sesuai dengan kebutuhan klien?~~ *(Terkonfirmasi 21-11-2026: sudah sesuai.)*
2. ~~Apakah klien membutuhkan filter rekap mingguan selain filter per bulan?~~ *(Terkonfirmasi 21-11-2026: cukup filter per bulan.)*
3. ~~Apakah perlu kotak konfirmasi sebelum transaksi dihapus permanen?~~ *(Terkonfirmasi 21-11-2026: ya, perlu peringatan sebelum hapus.)*
4. ~~Apakah berkas CSV hasil ekspor dapat langsung dibuka dengan rapi di laptop klien?~~ *(Terkonfirmasi 21-11-2026: ya, dapat dibuka.)*