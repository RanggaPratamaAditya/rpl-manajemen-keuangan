# Jurnal Vibe Coding - Jobsheet 1

Nama: Rangga Pratama Aditya
NIM: 23554010008
Kelas: Sistem informasi

| No | Tujuan | Prompt (ringkas) | Hasil AI | Keputusan | Alasan |
|---|---|---|---|---|---|
| 1 | Membuat beranda manajemen keuangan + formulir transaksi | Meminta aplikasi Flask manajemen keuangan tanpa DB dan JS, aman dari XSS, dengan simpan JSON | Menghasilkan `app.py` dan `templates/index.html` berisi ringkasan saldo, formulir, dan riwayat transaksi | Terima | Semua kriteria penerimaan terpenuhi, kode sudah ditinjau, dan uji masukan `<b>tes</b>` tampil aman |
| 2 | Menambahkan salam sesuai waktu server di beranda | Minta AI menambahkan fungsi `salam_waktu(jam)` dan menampilkannya sebelum waktu server tanpa mengubah fitur lain | Menambahkan fungsi `salam_waktu` di `app.py` dan baris salam di `templates/index.html` | Terima | Uji batas jam (3, 4, 10, 11, 14, 15, 17, 18) di terminal menghasilkan keluaran sesuai spesifikasi dan tampil benar di peramban |
| 3 | Menambahkan halaman `/tentang` beserta tautan dari beranda | Minta AI membuat rute `/tentang` dan templat `tentang.html` berisi identitas mahasiswa serta navigasi | Menambahkan rute `/tentang` di `app.py`, berkas `templates/tentang.html`, dan tautan di `index.html` | Terima | Tautan dari beranda dan tombol kembali berfungsi dengan baik, identitas tampil lengkap |
| 4 | Menambahkan validasi panjang masukan 50 karakter di sisi server | Minta AI membatasi teks keterangan maksimal 50 karakter di `app.py` menggunakan slicing `[:50]` | Mengubah pengambilan form `keterangan` menjadi `.strip()[:50]` di `app.py` | Terima | Terbukti lewat uji Inspect Element (`F12`) dengan 80 karakter, data yang tersimpan tetap terpotong menjadi 50 karakter |