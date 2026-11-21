# Jurnal Vibe Coding - Jobsheet 1

Nama: Rangga Pratama Aditya
NIM: 23554010008
Kelas: Sistem informasi

| No | Tujuan | Prompt (ringkas) | Hasil AI | Keputusan | Alasan |
|---|---|---|---|---|---|
| 1 | Membuat beranda manajemen keuangan + formulir transaksi | Meminta aplikasi Flask manajemen keuangan tanpa DB dan JS, aman dari XSS, dengan simpan JSON | Menghasilkan `app.py` dan `templates/index.html` berisi ringkasan saldo, formulir, dan riwayat transaksi | Terima | Semua kriteria penerimaan terpenuhi, kode sudah ditinjau, dan uji masukan `<b>tes</b>` tampil aman |
| 2 | Menambahkan salam sesuai waktu server di beranda | Minta AI menambahkan fungsi `salam_waktu(jam)` dan menampilkannya sebelum waktu server tanpa mengubah fitur lain | Menambahkan fungsi `salam_waktu` di `app.py` dan baris salam di `templates/index.html` | Terima | Uji batas jam (3, 4, 10, 11, 14, 15, 17, 18) di terminal menghasilkan keluaran sesuai spesifikasi dan tampil benar di peramban |