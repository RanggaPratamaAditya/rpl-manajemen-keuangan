# SRS Ringkas — Sistem Manajemen Keuangan UMKM

## 1. Pendahuluan
- **Tujuan dan ruang lingkup:** Dokumen ini menetapkan spesifikasi kebutuhan Sistem Manajemen Keuangan untuk usaha mikro/kecil (UMKM) bidang perdagangan/jasa di Sampit guna membantu pemilik dan staf mencatat pemasukan serta pengeluaran harian, menghitung saldo otomatis, dan membuat rekap keuangan bulanan. Sistem ini **tidak mencakup** integrasi rekening bank/e-wallet, penghitungan pajak otomatis, modul penggajian karyawan, maupun aplikasi ponsel (*mobile native*).
- **Definisi / istilah:**
  - **Transaksi:** Catatan uang masuk (pemasukan) atau uang keluar (pengeluaran) yang memiliki tanggal, keterangan, kategori, dan nominal rupiah.
  - **Saldo akhir:** Selisih antara total pemasukan dan total pengeluaran yang tersimpan pada sistem.
  - **Klien:** Pemilik UMKM yang menjadi narasumber kebutuhan (identitas disamarkan sesuai etika).

## 2. Gambaran Umum
- **Pengguna dan peran:**
  - *Pemilik usaha:* Pengambil keputusan dan pengguna utama; mampu memakai peramban dasar di laptop, tidak terbiasa dengan rumus lembar kerja yang rumit.
  - *Staf kasir / admin keuangan:* Pengguna harian yang mencatat transaksi masuk/keluar; terbiasa memakai peramban dasar dan ponsel.
- **Lingkungan operasi:** Berjalan pada 1 laptop standar di meja kasir klien (sistem operasi Windows) melalui peramban web standar; koneksi internet menggunakan tethering ponsel yang tidak selalu stabil dan listrik sesekali padam.
- **Batasan:**
  1. *Waktu:* Pengembangan sistem harus selesai paling lambat Minggu 16 perkuliahan (4 sprint dua mingguan).
  2. *Anggaran:* Klien tidak menghendaki biaya langganan bulanan atau sewa layanan berbayar pihak ketiga.
  3. *Perangkat & jaringan:* Sistem harus ringan dijalankan pada laptop standar milik klien dan tetap berfungsi saat koneksi internet terputus.
  4. *Kemampuan pengguna:* Antarmuka wajib berbahasa Indonesia, sederhana, dan tidak memerlukan pelatihan teknis yang rumit.
- **Asumsi (beserta rencana konfirmasi):**
  1. *Daftar kategori transaksi tetap* (Penjualan, Bahan Baku, Operasional, Listrik/Air, Lainnya) dianggap mewakili kebutuhan klien — **Rencana konfirmasi:** dikonfirmasi langsung ke pemilik usaha pada Langkah 14.
  2. *Format ekspor berkas rekap (CSV)* dapat dibuka langsung pada aplikasi lembar kerja di laptop klien — **Rencana konfirmasi:** diuji dan dikonfirmasi bersama klien pada Langkah 14.
  3. *Batas waktu muat halaman $\le 2$ detik* dan ukuran teks utama minimal 16 piksel sudah nyaman bagi pengguna — **Rencana konfirmasi:** diuji langsung pada laptop klien saat demonstrasi.

## 3. Kebutuhan Fungsional
| ID | Pernyataan kebutuhan | Sumber | Prioritas | Asumsi? |
|---|---|---|---|---|
| KF-01 | Sistem harus mencatat transaksi pemasukan harian yang memuat tanggal, keterangan, dan nominal, lalu menambahkannya ke saldo akhir. | US-01 | Must | Tidak |
| KF-02 | Sistem harus menolak penyimpanan transaksi apabila keterangan kosong atau nominal bernilai 0 atau negatif, serta menampilkan pesan peringatan yang jelas. | US-01, US-02 | Must | Tidak |
| KF-03 | Sistem harus mencatat transaksi pengeluaran harian yang memuat tanggal, keterangan, dan nominal, lalu menguranginya dari saldo akhir secara otomatis. | US-02 | Must | Tidak |
| KF-04 | Sistem harus menampilkan ringkasan total pemasukan, total pengeluaran, dan saldo akhir secara otomatis pada halaman utama. | US-03 | Must | Tidak |
| KF-05 | Sistem harus menghapus transaksi yang dipilih dari daftar riwayat dan memperbarui perhitungan saldo akhir secara otomatis. | US-04 | Must | Tidak |
| KF-06 | Sistem harus mengubah keterangan atau nominal transaksi yang sudah tersimpan dan memperbarui total serta saldo terkait. | US-05 | Must | Tidak |
| KF-07 | Sistem harus mengelompokkan setiap transaksi berdasarkan kategori yang dipilih pengguna saat pencatatan. | US-06 | Must | Ya |
| KF-08 | Sistem harus menyaring daftar riwayat transaksi berdasarkan bulan dan tahun tertentu beserta ringkasan total periode tersebut. | US-07 | Should | Ya |
| KF-09 | Sistem harus mencari transaksi pada daftar riwayat berdasarkan kata kunci keterangan dan menampilkan pesan bila tidak ditemukan. | US-08 | Should | Ya |
| KF-10 | Sistem harus mengekspor daftar transaksi yang sedang ditampilkan ke dalam berkas rekap berformat tabel terpisah koma (CSV). | US-09 | Should | Ya |
| KF-11 | Sistem harus menampilkan halaman panduan penggunaan yang memuat minimal 3 langkah bernomor cara mencatat transaksi. | US-11 | Could | Ya |
| KF-12 | Sistem harus menampilkan peringatan apabila total pengeluaran pada bulan berjalan melebihi batas anggaran yang ditetapkan pemilik. | Backlog JS-2 | Could | Ya |

## 4. Kebutuhan Non-Fungsional
| ID | Kategori | Pernyataan terukur | Sumber | Prioritas |
|---|---|---|---|---|
| KNF-01 | Keandalan | Sistem harus tetap dapat mencatat, menyimpan, dan memuat ulang seluruh data transaksi secara lokal tanpa koneksi internet. | US-12, Catatan no. 6 | Must |
| KNF-02 | Keamanan | Sistem harus menampilkan karakter khusus penanda halaman pada masukan keterangan sebagai teks biasa tanpa mengeksekusinya dan membatasi panjang keterangan maksimal 50 karakter di sisi server. | US-10, Catatan no. 5 | Must |
| KNF-03 | Kinerja | Halaman utama dan proses penyimpanan transaksi harus selesai dimuat dalam waktu <= 2 detik pada laptop standar klien. | Catatan no. 6 (Asumsi) | Should |
| KNF-04 | Kegunaan | Pengguna baru tanpa latar belakang teknis harus dapat mencatat satu transaksi tanpa bantuan setelah membaca panduan singkat, dalam maksimal 3 langkah isian. | US-11, Catatan no. 5 | Should |
| KNF-05 | Kompatibilitas | Antarmuka sistem harus dapat dibaca dengan jelas pada layar laptop klien dengan ukuran tulisan utama minimal 16 piksel. | Catatan no. 5, 6 (Asumsi) | Could |

### Ringkasan Proporsi & Alasan Prioritas MoSCoW
- **Persentase Must:** 7 dari 12 KF (**58,3%**) atau 9 dari 17 total kebutuhan KF+KNF (**52,9%**) — memenuhi batas maksimal $\pm 60\%$.
- **Alasan butir Must:**
  - `KF-01` s.d. `KF-07`: Merupakan fungsi inti pencatatan kas harian, koreksi salah input, pengelompokan kategori, dan perhitungan saldo otomatis; tanpanya masalah utama klien (selisih hitung dan rekap manual) tidak terselesaikan.
  - `KNF-01`: Wajib karena internet di lokasi klien hanya memakai tethering HP yang tidak stabil.
  - `KNF-02`: Wajib sebagai standar keamanan dasar pengolahan masukan pengguna.
- **Alasan butir Won't have:** Lihat Bagian 5 di bawah.

## 5. Di Luar Lingkup (Won't Have — Kali Ini)
1. **Integrasi otomatis rekening bank, mutasi e-wallet, dan gerbang pembayaran** — *Alasan:* Membutuhkan biaya layanan pihak ketiga, koneksi internet stabil, serta melampaui waktu proyek hingga Minggu 16.
2. **Penghitungan pajak resmi otomatis dan modul penggajian karyawan** — *Alasan:* Tidak diminta oleh klien pada wawancara dan berada di luar fokus pencatatan arus kas harian.
3. **Aplikasi ponsel khusus (mobile native Android/iOS)** — *Alasan:* Klien memiliki keterbatasan anggaran dan perangkat utama di meja kasir adalah laptop standar.

## 6. Matriks Keterlacakan
| User story | KF / KNF turunan | Use Case | Uji (diisi Minggu 13) |
|---|---|---|---|
| US-01 | KF-01, KF-02 | UC-01, UC-02 | *(diisi Minggu 13)* |
| US-02 | KF-02, KF-03 | UC-01, UC-02 | *(diisi Minggu 13)* |
| US-03 | KF-04 | UC-03 | *(diisi Minggu 13)* |
| US-04 | KF-05 | UC-05 | *(diisi Minggu 13)* |
| US-05 | KF-06 | UC-04, UC-02 | *(diisi Minggu 13)* |
| US-06 | KF-07 | UC-01 | *(diisi Minggu 13)* |
| US-07 | KF-08 | UC-06 | *(diisi Minggu 13)* |
| US-08 | KF-09 | UC-06 | *(diisi Minggu 13)* |
| US-09 | KF-10 | UC-07 | *(diisi Minggu 13)* |
| US-10 | KNF-02 | UC-01, UC-02, UC-04 | *(diisi Minggu 13)* |
| US-11 | KF-11, KNF-04 | *(Could — opsional)* | *(diisi Minggu 13)* |
| US-12 | KNF-01 | UC-01 s.d. UC-07 | *(diisi Minggu 13)* |
| *(Asumsi / Backlog)* | KF-12, KNF-03, KNF-05 | *(Could / Non-fungsional)* | *(diisi Minggu 13)* |

## 7. Pemodelan UML
Seluruh berkas pemodelan fungsi dan alur sistem tersimpan pada folder `docs/uml/`:
- **Use Case Diagram:** [`docs/uml/use-case.mmd`](uml/use-case.mmd) dan [`docs/uml/use-case.png`](uml/use-case.png)
- **Skenario Use Case (5 skenario):** [`docs/uml/skenario-use-case.md`](uml/skenario-use-case.md)
- **Activity Diagram 1 (Catat Transaksi):** [`docs/uml/activity-01-catat-transaksi.mmd`](uml/activity-01-catat-transaksi.mmd) dan [`docs/uml/activity-01-catat-transaksi.png`](uml/activity-01-catat-transaksi.png)
- **Activity Diagram 2 (Ubah Transaksi):** [`docs/uml/activity-02-ubah-transaksi.mmd`](uml/activity-02-ubah-transaksi.mmd) dan [`docs/uml/activity-02-ubah-transaksi.png`](uml/activity-02-ubah-transaksi.png)
- **Activity Diagram 3 (Hapus Transaksi):** [`docs/uml/activity-03-hapus-transaksi.mmd`](uml/activity-03-hapus-transaksi.mmd) dan [`docs/uml/activity-03-hapus-transaksi.png`](uml/activity-03-hapus-transaksi.png)


## Riwayat Konfirmasi Klien
| Tanggal | Tanggapan | Perubahan |
|---|---|---|
| 21-11-2026 | Klien menyetujui seluruh daftar fitur Must, Should, dan Won't have. Daftar 5 kategori dinilai sudah sesuai, rekap cukup per bulan, format CSV dapat dibuka di laptop klien, dan klien setuju ada konfirmasi sebelum hapus transaksi. | Status asumsi pada KF-07 s.d. KF-10 diubah menjadi Tidak (terkonfirmasi); tidak ada perubahan urutan prioritas MoSCoW. |