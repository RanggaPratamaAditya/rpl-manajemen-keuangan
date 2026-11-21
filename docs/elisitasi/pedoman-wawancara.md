# Pedoman Wawancara — Sistem Manajemen Keuangan

## A. Konteks
- **Klien / lokasi:** Usaha Mikro/Kecil (UMKM) bidang perdagangan/jasa di Sampit, Kotawaringin Timur *(nama klien disamarkan sesuai etika)*
- **Masalah utama (dugaan awal yang akan dikonfirmasi ke klien):**
  1. Pencatatan pemasukan dan pengeluaran harian masih dilakukan di buku tulis atau nota terpisah sehingga rawan hilang atau salah hitung.
  2. Pemilik kesulitan mengetahui saldo kas terkini dan total keuntungan bersih secara cepat tanpa menjumlahkan catatan satu per satu.
  3. Rekapitulasi keuangan mingguan/bulanan membutuhkan waktu lama karena transaksi tidak terkelompok menurut kategori.
- **Ruang lingkup:**
  - *Di dalam proyek (dikerjakan):*
    1. Pencatatan transaksi pemasukan dan pengeluaran harian beserta tanggal, keterangan, dan nominal.
    2. Perhitungan otomatis total pemasukan, total pengeluaran, dan saldo akhir.
    3. Pengelompokan kategori transaksi, penyaringan berdasarkan periode, serta riwayat yang dapat dihapus/diubah bila salah input.
  - *Di luar proyek (sengaja tidak dikerjakan):*
    1. Integrasi otomatis dengan rekening bank, mutasi e-wallet, atau gerbang pembayaran (payment gateway).
    2. Penghitungan pajak resmi otomatis dan modul penggajian karyawan kompleks.
- **Batasan:**
  - *Waktu:* Pengembangan selesai paling lambat Minggu 16 perkuliahan.
  - *Perangkat & internet:* Berjalan di peramban laptop/komputer standar milik klien (dapat dipakai lokal bila internet tidak stabil).
  - *Kemampuan pengguna:* Antarmuka harus sederhana, berbahasa Indonesia, dan mudah dipahami oleh pengguna non-teknis.

### Pemangku Kepentingan
| Pemangku kepentingan | Peran | Kepentingan | Cara dilibatkan |
|---|---|---|---|
| Pemilik usaha | Pengambil keputusan & pengguna utama | Mengetahui arus kas, laba rugi, dan saldo secara cepat dan akurat | Wawancara langsung & konfirmasi hasil |
| Staf kasir / admin keuangan | Pengguna harian (operator) | Mencatat transaksi masuk/keluar dengan cepat tanpa kesalahan hitung | Wawancara & observasi proses pencatatan |
| Pelanggan / pemasok | Pihak eksternal penyedia transaksi | Menerima/memberikan bukti pembayaran (nota) yang jelas | Studi dokumen (contoh nota transaksi, nama disamarkan) |

### Teknik Elisitasi Dipilih
| Teknik dipilih | Siapa / apa yang menjadi sumber | Alasan memilih |
|---|---|---|
| Wawancara | Pemilik usaha dan/atau admin pencatat keuangan | Paling tepat untuk menggali alur kerja sehari-hari, keluhan saat merekap kas, serta harapan mereka secara mendalam |
| Studi dokumen | Buku kas harian, buku nota penjualan, dan struk belanja (difoto dengan izin, data pribadi disamarkan) | Untuk melihat langsung kolom data, format angka, dan jenis transaksi yang benar-benar dipakai di lapangan agar tidak hanya mengandalkan ingatan narasumber |

## B. Tujuan Wawancara
1. Memahami proses pencatatan pemasukan, pengeluaran, dan rekapitulasi keuangan yang berjalan saat ini.
2. Mengidentifikasi kendala utama, kesalahan yang sering terjadi, serta kebutuhan informasi keuangan pemilik usaha.
3. Mengumpulkan contoh dokumen/format catatan keuangan yang digunakan sebagai dasar perancangan data.

## C. Pertanyaan
| No | Kategori | Pertanyaan | Pertanyaan lanjutan |
|---|---|---|---|
| 1 | Proses saat ini | Bagaimana alur Bapak/Ibu mencatat uang masuk dan uang keluar dari buka sampai tutup usaha setiap hari? | Bagian mana dari alur tersebut yang paling sering menyita waktu? |
| 2 | Proses saat ini | Bagaimana cara Bapak/Ibu menghitung saldo akhir atau mengetahui keuntungan pada akhir minggu atau akhir bulan? | Berapa lama biasanya waktu yang dibutuhkan untuk menyelesaikan rekap tersebut? |
| 3 | Masalah | Kejadian apa yang paling sering menimbulkan selisih atau kebingungan pada catatan keuangan selama ini? | Bisa diceritakan kejadian terakhir saat selisih catatan itu terjadi? |
| 4 | Masalah | Apa dampak yang Bapak/Ibu rasakan ketika ada nota pengeluaran atau pemasukan yang lupa dicatat atau terselip? | Bagaimana cara Bapak/Ibu menelusuri atau memperbaiki catatan yang terlewat itu? |
| 5 | Data | Informasi apa saja yang wajib Bapak/Ibu tulis setiap kali mencatat satu transaksi? | Adakah informasi tambahan yang sering ingin dicatat tetapi belum muat di buku sekarang? |
| 6 | Data | *(Meminta contoh dokumen)* Boleh kami melihat contoh halaman buku kas atau catatan pemasukan/pengeluaran yang biasa dipakai? | Dari kolom yang ada di buku tersebut, kolom mana yang paling sering Bapak/Ibu periksa kembali? |
| 7 | Data | *(Meminta contoh dokumen)* Boleh kami melihat contoh nota atau struk belanja yang biasa disimpan sebagai bukti transaksi? | Bagaimana cara Bapak/Ibu mengelompokkan nota-nota tersebut (misalnya per hari atau per jenis belanja)? |
| 8 | Data | *(Meminta contoh dokumen)* Apabila Bapak/Ibu membuat laporan rekap bulanan, boleh kami melihat contoh format rekap yang selama ini dibuat? | Informasi ringkasan apa yang paling utama Bapak/Ibu lihat dari rekap tersebut? |
| 9 | Pengguna | Siapa saja yang bertugas mencatat transaksi harian dan siapa saja yang boleh melihat total saldo atau laporan keuangan? | Bagaimana pembagian tugas pencatatan jika pemilik sedang tidak berada di tempat? |
| 10 | Pengguna | Sejauh mana kebiasaan Bapak/Ibu dan staf dalam menggunakan komputer, laptop, atau ponsel untuk pekerjaan sehari-hari? | Tampilan atau hal seperti apa yang membuat Bapak/Ibu merasa nyaman saat memakai sebuah alat bantu? |
| 11 | Kendala | Bagaimana kondisi perangkat (komputer/ponsel), listrik, dan koneksi internet di lokasi usaha saat jam operasional? | Apa yang biasa dilakukan bila listrik padam atau koneksi internet terganggu? |
| 12 | Kendala | Kendala apa yang pernah Bapak/Ibu alami apabila sebelumnya pernah mencoba mencatat keuangan memakai Excel atau aplikasi lain? | Hal apa yang membuat cara tersebut terasa merepotkan atau akhirnya ditinggalkan? |
| 13 | Harapan | Informasi keuangan apa yang paling ingin Bapak/Ibu ketahui dengan cepat kapan saja dibutuhkan? | Mengapa informasi tersebut paling penting bagi pengambilan keputusan usaha Bapak/Ibu? |
| 14 | Harapan | Perubahan apa yang paling Bapak/Ibu harapkan dari proses pencatatan keuangan ke depannya? | Jika ada satu masalah pencatatan yang harus beres paling dulu, masalah mana yang paling mendesak? |

## D. Etika
- **Izin klien diperoleh pada:** *(diisi saat Langkah 11 setelah klien menyetujui jadwal)*
- **Data pribadi:** Nama lengkap pelanggan/pemasok, nomor telepon, alamat pribadi, dan nomor rekening tidak dicatat dan disamarkan menjadi peran/inisial.