# Skenario Use Case — Sistem Manajemen Keuangan UMKM

## UC-01 Catat transaksi harian
- **Aktor:** Pemilik Usaha, Staf Kasir / Admin
- **KF terkait:** KF-01, KF-02, KF-03, KF-07
- **Prasyarat:** Aplikasi web berjalan secara lokal di peramban dan pengguna berada di halaman utama.

### Alur utama
1. Aktor membuka formulir pencatatan transaksi pada halaman utama.
2. Aktor memilih jenis transaksi (pemasukan atau pengeluaran), memilih kategori, mengisi keterangan, dan memasukkan nominal rupiah.
3. Aktor menekan tombol "Simpan".
4. Sistem memvalidasi kelengkapan keterangan, pilihan kategori, batas panjang keterangan (maksimal 50 karakter), dan nilai nominal (harus bilangan bulat positif) (UC-02).
5. Sistem menyimpan transaksi ke penyimpanan lokal, memperbarui total pemasukan/pengeluaran serta saldo akhir, lalu menampilkan daftar riwayat terbaru.

### Alur alternatif
- 2a. Jika aktor mencatat transaksi pengeluaran, sistem mengurangi nilai nominal dari saldo akhir (KF-03); jika pemasukan, sistem menambahkannya ke saldo akhir (KF-01).

### Pengecualian
- 4a. Jika keterangan kosong atau kategori belum dipilih, sistem menolak penyimpanan dan menampilkan pesan "Keterangan dan kategori wajib diisi" (KF-02).
- 4b. Jika nominal bernilai 0, negatif, atau bukan angka bulat, sistem menolak penyimpanan dan menampilkan pesan "Nominal harus berupa angka bulat positif" (KF-02).

### Pascakondisi
Transaksi baru tersimpan permanen pada berkas penyimpanan lokal dan saldo akhir terbarui otomatis.

---

## UC-03 Lihat ringkasan saldo
- **Aktor:** Pemilik Usaha
- **KF terkait:** KF-04
- **Prasyarat:** Aplikasi web berjalan secara lokal di peramban.

### Alur utama
1. Aktor membuka halaman utama aplikasi (`/`).
2. Sistem membaca seluruh daftar transaksi dari penyimpanan lokal.
3. Sistem menjumlahkan seluruh transaksi pemasukan, seluruh transaksi pengeluaran, dan menghitung selisihnya sebagai saldo akhir.
4. Sistem menampilkan kartu Total Pemasukan, Total Pengeluaran, dan Saldo Akhir dalam format Rupiah di bagian atas halaman.

### Alur alternatif
- 2a. Jika belum ada satu pun transaksi yang tersimpan, sistem menampilkan seluruh angka ringkasan sebagai `Rp 0` tanpa galat.

### Pengecualian
- 2b. Jika berkas penyimpanan lokal tidak ditemukan atau rusak, sistem membuat berkas penyimpanan kosong baru dan menampilkan ringkasan `Rp 0` beserta pesan pemberitahuan.

### Pascakondisi
Pemilik Usaha melihat kondisi total pemasukan, pengeluaran, dan saldo akhir terkini secara akurat.

---

## UC-04 Ubah transaksi
- **Aktor:** Pemilik Usaha, Staf Kasir / Admin
- **KF terkait:** KF-06, KF-02
- **Prasyarat:** Minimal terdapat satu transaksi tersimpan pada daftar riwayat.

### Alur utama
1. Aktor memilih tombol "Ubah" pada salah satu baris transaksi di tabel riwayat.
2. Sistem menampilkan formulir ubah transaksi yang sudah terisi data lama (jenis, kategori, keterangan, dan nominal).
3. Aktor mengubah data yang keliru lalu menekan tombol "Simpan Perubahan".
4. Sistem memvalidasi masukan baru (UC-02).
5. Sistem memperbarui data transaksi pada penyimpanan lokal, menghitung ulang total dan saldo akhir, lalu kembali ke halaman utama.

### Alur alternatif
- 3a. Jika aktor menekan tombol "Batal", sistem menutup formulir ubah tanpa mengubah data yang tersimpan.

### Pengecualian
- 4a. Jika nominal baru bernilai 0 atau negatif, sistem menolak perubahan dan menampilkan pesan "Nominal harus berupa angka bulat positif" (KF-02).
- 4b. Jika keterangan baru melebihi 50 karakter, sistem memotong teks menjadi maksimal 50 karakter di sisi server sebelum menyimpan.

### Pascakondisi
Data transaksi terpilih terbarui dan ringkasan saldo otomatis menyesuaikan nilai baru.

---

## UC-05 Hapus transaksi
- **Aktor:** Pemilik Usaha
- **KF terkait:** KF-05
- **Prasyarat:** Minimal terdapat satu transaksi tersimpan pada daftar riwayat.

### Alur utama
1. Aktor menekan tombol "Hapus" pada baris transaksi yang keliru di tabel riwayat.
2. Sistem menampilkan pesan konfirmasi penghapusan kepada aktor.
3. Aktor menyetujui penghapusan.
4. Sistem menghapus transaksi berdasarkan ID dari penyimpanan lokal, menghitung ulang total dan saldo akhir, lalu menampilkan daftar riwayat terbaru.

### Alur alternatif
- 3a. Jika aktor membatalkan konfirmasi, sistem tidak menghapus data dan tetap menampilkan daftar transaksi seperti semula.

### Pengecualian
- 4a. Jika ID transaksi yang hendak dihapus tidak ditemukan pada penyimpanan lokal, sistem mengabaikan penghapusan dan menampilkan pesan "Transaksi tidak ditemukan".

### Pascakondisi
Transaksi terpilih terhapus permanen dan saldo akhir kembali sesuai sisa transaksi yang ada.

---

## UC-06 Filter dan cari riwayat transaksi
- **Aktor:** Pemilik Usaha, Staf Kasir / Admin
- **KF terkait:** KF-08, KF-09
- **Prasyarat:** Pengguna berada di halaman utama dan terdapat data transaksi tersimpan.

### Alur utama
1. Aktor memilih bulan dan tahun pada kotak filter periode, atau mengetikkan kata kunci keterangan pada kotak pencarian.
2. Aktor menekan tombol "Terapkan / Cari".
3. Sistem menyaring daftar transaksi yang cocok dengan periode dan/atau kata kunci yang dimasukkan.
4. Sistem menampilkan baris transaksi yang sesuai beserta subtotal pemasukan dan pengeluaran untuk hasil penyaringan tersebut.

### Alur alternatif
- 1a. Jika aktor menekan tombol "Reset Filter", sistem menampilkan kembali seluruh transaksi yang tersimpan.

### Pengecualian
- 3a. Jika tidak ada transaksi yang cocok dengan bulan/tahun yang dipilih, sistem menampilkan pesan "Tidak ada transaksi pada periode ini" (KF-08).
- 3b. Jika tidak ada transaksi yang cocok dengan kata kunci pencarian, sistem menampilkan pesan "Transaksi tidak ditemukan" (KF-09).

### Pascakondisi
Aktor melihat daftar transaksi terfilter beserta ringkasan angkanya secara akurat.