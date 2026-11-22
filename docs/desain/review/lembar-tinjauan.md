# Lembar Tinjauan Design Review dan Keputusan Revisi

- **Kelompok penelaah:** [Isi nama kelompok penelaah / Rekan sejawat]
- **Kelompok yang ditinjau / proyek:** Rangga Pratama Aditya (23554010008) / Sistem Manajemen Keuangan UMKM
- **Tanggal:** 22-11-2026

## 1. Daftar Periksa Tinjauan (Lampiran C)
| No | Pertanyaan periksa | Ya | Tidak | Catatan |
|---|---|---|---|---|
| 1 | Setiap use case Must dapat diselesaikan melalui halaman yang digambar? | Ya | | Seluruh UC-01 s.d. UC-07 tercakup pada `wf-01` s.d. `wf-07`. |
| 2 | Peta navigasi jelas; setiap halaman dapat dicapai dan ada jalan kembali? | Ya | | Maksimal 2 klik dari Beranda; tidak ada halaman yatim. |
| 3 | Menu, tombol, dan istilah konsisten di semua halaman? | Ya | | Header navigasi dan posisi tombol kanan bawah seragam. |
| 4 | Pesan keberhasilan dan galat tergambar (umpan balik)? | Ya | | Kotak pesan galat dan sukses ada di tiap halaman utama. |
| 5 | Isian dibatasi untuk mencegah galat (angka, wajib isi)? | Ya | | Ada batas nominal > 0, maks. 50 karakter, dan konfirmasi hapus. |
| 6 | Tulisan terbaca dan memakai istilah klien? | Ya | | Bahasa Indonesia awam tanpa istilah teknis. |
| 7 | Setiap KF Must punya test case; hasil diharapkan terukur? | Ya | | 15 test case terukur dengan partisi tidak valid dan nilai batas. |
| 8 | Ada elemen yang tidak berasal dari SRS (fitur tambahan)? | | Tidak | Seluruh elemen merujuk ke SRS dan kamus data. |

## 2. Ringkasan Masukan Penelaah
- **Kekuatan rancangan:** Konsistensi header navigasi, pemisahan hak akses `(Pemilik)`, serta penggambaran kotak galat dan konfirmasi hapus sangat jelas.
- **Temuan penting:** Pada `wf-03` (Catat Transaksi), sebaiknya tanggal otomatis terisi tanggal hari ini agar mempercepat pencatatan harian (memenuhi `KNF-04`).
- **Saran perbaikan:** (1) Tambahkan informasi jumlah karakter tersisa (mis. `0/50`) di bawah kotak keterangan `wf-03` dan `wf-05`; (2) Tambahkan tombol pintasan "Ekspor CSV" langsung di halaman `wf-04` (Riwayat).
- **Pertanyaan penelaah:** Bagaimana jika pengguna menekan tombol `Simpan` dua kali dengan cepat pada `wf-03`?

## 3. Tabel Keputusan Revisi (Langkah 12)
| No | Masukan penelaah | Keputusan | Perubahan / Alasan |
|---|---|---|---|
| 1 | Tanggal pada `wf-03` otomatis terisi tanggal hari ini (`default today`) agar tidak perlu mengetik manual setiap kali mencatat. | **Terima** | Ditambahkan aturan `default = tanggal hari ini` pada `docs/desain/wireframe/anotasi.md` untuk mendukung kecepatan pencatatan (`KNF-04`). |
| 2 | Tambahkan penghitung karakter (`0/50`) pada kolom keterangan di `wf-03` dan `wf-05`. | **Terima** | Dicatat pada `anotasi.md` agar pengguna tahu batas 50 karakter (`KNF-02`) sebelum menekan Simpan. |
| 3 | Tambahkan tombol "Ekspor CSV" langsung di halaman `wf-04` (Riwayat). | **Tolak** | Ditolak untuk menjaga prinsip **Kesederhanaan** dan pemisahan hak akses (menu `Ekspor CSV` khusus Pemilik sudah dapat diakses 1 klik dari menu navigasi atas). |