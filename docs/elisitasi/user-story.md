# Daftar User Story (Tahap Simulasi Persona 1)

## US-01 Mencatat penjualan dan memotong stok otomatis
Sebagai kasir, saya ingin mencatat transaksi penjualan barang agar jumlah stok di gudang langsung berkurang otomatis tanpa perlu memberi tahu pegawai gudang secara manual.
Kriteria penerimaan:
- Given stok barang "Semen 50kg" berjumlah 20 sak, When kasir mencatat penjualan 5 sak, Then stok "Semen 50kg" otomatis berubah menjadi 15 sak.
- Given stok barang "Cat 5kg" berjumlah 2 kaleng, When kasir mencoba mencatat penjualan 4 kaleng, Then sistem menolak transaksi dan menampilkan pesan "Stok tidak mencukupi (tersisa 2)".
Sumber: catatan wawancara simulasi Persona 1 no. 1 dan 3
[Asumsi: tidak]

## US-02 Memperbarui harga beli dan harga jual barang
Sebagai pemilik toko, saya ingin mengubah harga beli dan harga jual barang yang sudah terdaftar agar harga di kasir selalu sesuai dengan perubahan mingguan.
Kriteria penerimaan:
- Given barang "Pipa PVC 3/4" memiliki harga jual Rp 25.000, When pemilik mengubah harga jual menjadi Rp 27.500 dan menyimpan, Then transaksi penjualan baru langsung memakai harga Rp 27.500.
- Given pemilik membuka formulir ubah harga, When pemilik memasukkan harga negatif atau 0, Then sistem menolak perubahan dan menampilkan pesan "Harga harus lebih dari 0".
Sumber: catatan wawancara simulasi Persona 1 no. 2
[Asumsi: tidak]

## US-03 Mencatat dan memantau piutang kontraktor tempo 2 minggu
Sebagai pemilik toko, saya ingin mencatat transaksi pembelian tempo beserta tanggal jatuh temponya agar saya dapat melihat daftar piutang yang harus ditagih tanpa ada yang terlewat.
Kriteria penerimaan:
- Given kasir mencatat pembelian tempo senilai Rp 1.500.000 atas nama "Kontraktor A" pada tanggal 1 November, When transaksi disimpan dengan tempo 14 hari, Then transaksi muncul di daftar piutang belum lunas dengan tanggal jatuh tempo 15 November.
- Given piutang "Kontraktor A" sudah melewati tanggal jatuh tempo dan berstatus belum lunas, When pemilik membuka daftar piutang, Then baris piutang tersebut diberi tanda peringatan "Jatuh Tempo".
Sumber: catatan wawancara simulasi Persona 1 no. 4
[Asumsi: tidak]

## US-04 Melihat ringkasan mingguan barang terlaris dan stok menipis
Sebagai pemilik toko, saya ingin melihat daftar barang terlaris dan barang yang stoknya hampir habis setiap hari Sabtu agar saya dapat merencanakan pembelian ulang barang dengan tepat.
Kriteria penerimaan:
- Given terdapat transaksi penjualan selama 7 hari terakhir, When pemilik membuka halaman ringkasan mingguan, Then sistem menampilkan daftar 5 barang dengan jumlah unit terjual terbanyak beserta total unitnya.
- Given batas minimum stok barang ditetapkan 5 unit dan stok "Paku 5cm" tersisa 3 kg, When pemilik membuka halaman ringkasan mingguan, Then "Paku 5cm" tampil pada bagian "Stok Hampir Habis".
Sumber: catatan wawancara simulasi Persona 1 no. 5
[Asumsi: ya — angka batas minimum stok 5 unit dan jumlah 5 barang terlaris perlu dikonfirmasi ke pemilik]

## US-05 Mencatat penambahan stok masuk oleh pegawai gudang
Sebagai pegawai gudang, saya ingin mencatat barang masuk dari pemasok dengan formulir sederhana bertulisan besar agar jumlah stok tercatat akurat sesuai kondisi fisik di gudang.
Kriteria penerimaan:
- Given stok "Semen 50kg" saat ini 15 sak, When pegawai gudang mencatat stok masuk 30 sak, Then stok "Semen 50kg" bertambah menjadi 45 sak dan tercatat pada riwayat stok masuk.
- Given pegawai gudang membuka halaman stok masuk di laptop toko, When halaman dimuat secara lokal tanpa koneksi internet, Then formulir tetap terbuka dan ukuran teks label minimal 16px agar mudah dibaca.
Sumber: catatan wawancara simulasi Persona 1 no. 1, 6
[Asumsi: ya — ukuran teks minimal 16px perlu dikonfirmasi kenyamanannya ke pegawai]

---

## Tinjauan Saran AI Berdasarkan Kriteria INVEST (Langkah 9)
| ID | Sesuai kebutuhan klien? | Kecil dan teruji? | Keputusan | Alasan |
|---|---|---|---|---|
| US-01 | Ya | Ya | Terima | Saran AI menambahkan kriteria penolakan saat stok kurang membuat story lebih teruji (*Testable*). |
| US-02 | Ya | Ya | Terima | Saran AI menambahkan validasi harga `<= 0` mencegah kesalahan ketik saat memperbarui harga mingguan. |
| US-03 | Ya | Ya | Ubah | AI menyarankan fitur pengiriman pengingat otomatis lewat WhatsApp/SMS; bagian itu dihapus karena internet toko tidak stabil dan butuh biaya layanan pihak ketiga, sehingga diubah cukup menjadi tanda "Jatuh Tempo" di layar. |
| US-04 | Ya | Ya | Ubah | AI menyarankan grafik analitik interaktif bulanan; diubah menjadi daftar teks sederhana 5 barang terlaris dan stok menipis agar mudah dibaca di laptop lama, dan angka batas diberi tanda `[Asumsi]`. |
| US-05 | Ya | Ya | Tolak (sebagian) | AI menyarankan penambahan pemindaian barcode dengan kamera HP; ditolak karena klien tidak menyebut kebutuhan barcode dan perangkat di toko terbatas. |

---

# Daftar User Story Klien Nyata (Langkah 13)

## US-01 Mencatat transaksi pemasukan harian
Sebagai pemilik usaha, saya ingin mencatat setiap transaksi pemasukan beserta tanggal, keterangan, dan nominal agar seluruh uang masuk terdokumentasi rapi.
Kriteria penerimaan:
- Given saldo saat ini Rp 500.000, When pemilik mencatat pemasukan "Penjualan harian" sebesar Rp 250.000, Then transaksi tersimpan di daftar riwayat dan saldo otomatis menjadi Rp 750.000.
- Given formulir transaksi terbuka, When pemilik mengirim pemasukan dengan nominal 0 atau negatif, Then sistem menolak penyimpanan dan menampilkan pesan "Nominal harus berupa angka bulat positif".
Sumber: catatan wawancara klien no. 1
[Asumsi: ya — konfirmasi format keterangan ke klien]

## US-02 Mencatat transaksi pengeluaran harian
Sebagai pemilik usaha, saya ingin mencatat setiap transaksi pengeluaran operasional agar seluruh biaya keluar terpantau dan mengurangi saldo secara otomatis.
Kriteria penerimaan:
- Given saldo saat ini Rp 750.000, When pemilik mencatat pengeluaran "Beli bahan baku" sebesar Rp 150.000, Then transaksi tersimpan dan saldo otomatis menjadi Rp 600.000.
- Given formulir transaksi terbuka, When pemilik mengosongkan kolom keterangan lalu menekan simpan, Then sistem menolak penyimpanan dan menampilkan pesan "Keterangan wajib diisi".
Sumber: catatan wawancara klien no. 1
[Asumsi: ya — konfirmasi jenis pengeluaran rutin ke klien]

## US-03 Melihat ringkasan total pemasukan, pengeluaran, dan saldo akhir
Sebagai pemilik usaha, saya ingin melihat ringkasan total pemasukan, total pengeluaran, dan saldo akhir langsung di halaman utama agar tidak perlu menghitung manual dengan kalkulator.
Kriteria penerimaan:
- Given terdapat 2 pemasukan (Rp 300.000 dan Rp 200.000) serta 1 pengeluaran (Rp 120.000), When pemilik membuka beranda, Then sistem menampilkan Total Pemasukan Rp 500.000, Total Pengeluaran Rp 120.000, dan Saldo Akhir Rp 380.000.
- Given belum ada transaksi yang dicatat, When pemilik membuka beranda, Then seluruh angka ringkasan tampil sebagai Rp 0 tanpa galat.
Sumber: catatan wawancara klien no. 2
[Asumsi: ya — konfirmasi ke klien]

## US-04 Menghapus transaksi yang salah input
Sebagai pemilik usaha, saya ingin menghapus transaksi yang keliru dicatat agar perhitungan saldo dan laporan keuangan kembali akurat.
Kriteria penerimaan:
- Given terdapat transaksi pengeluaran Rp 50.000 dan saldo Rp 450.000, When pemilik menekan tombol "Hapus" pada transaksi tersebut, Then transaksi hilang dari daftar riwayat dan saldo kembali menjadi Rp 500.000.
- Given transaksi ber-ID 3 telah dihapus, When halaman dimuat ulang, Then transaksi ID 3 tidak muncul kembali pada berkas penyimpanan.
Sumber: catatan wawancara klien no. 3
[Asumsi: ya — konfirmasi apakah perlu tombol konfirmasi sebelum hapus]

## US-05 Mengubah data transaksi yang keliru
Sebagai admin keuangan, saya ingin mengubah keterangan atau nominal transaksi yang sudah tersimpan agar salah ketik dapat diperbaiki tanpa harus menghapus dan mengetik ulang dari awal.
Kriteria penerimaan:
- Given transaksi "Bayar listrik" tercatat Rp 100.000, When admin mengubah nominal menjadi Rp 150.000 dan menyimpan, Then riwayat menampilkan Rp 150.000 dan total pengeluaran bertambah Rp 50.000.
- Given admin mengubah keterangan menjadi lebih dari 50 karakter, When data disimpan, Then server memotong keterangan menjadi maksimal 50 karakter.
Sumber: catatan wawancara klien no. 3
[Asumsi: ya — konfirmasi ke klien]

## US-06 Mengelompokkan transaksi berdasarkan kategori
Sebagai pemilik usaha, saya ingin memilih kategori pada setiap transaksi (misalnya Penjualan, Bahan Baku, Operasional, Lainnya) agar saya dapat mengetahui pos pengeluaran terbesar.
Kriteria penerimaan:
- Given daftar kategori tersedia di formulir, When pemilik menyimpan pengeluaran Rp 80.000 berkategori "Operasional", Then kolom kategori pada tabel riwayat menampilkan "Operasional".
- Given pemilik memilih jenis transaksi, When formulir dikirim tanpa memilih kategori, Then sistem menolak penyimpanan dan meminta kategori dipilih.
Sumber: catatan wawancara klien no. 4
[Asumsi: ya — daftar kategori pasti perlu dikonfirmasi dari buku kas klien]

## US-07 Menyaring riwayat transaksi berdasarkan bulan dan tahun
Sebagai pemilik usaha, saya ingin menyaring riwayat transaksi berdasarkan bulan tertentu agar proses rekapitulasi bulanan selesai dalam hitungan detik.
Kriteria penerimaan:
- Given terdapat 3 transaksi pada bulan Oktober dan 4 transaksi pada bulan November, When pemilik memilih filter bulan "November", Then tabel hanya menampilkan 4 transaksi bulan November beserta total pemasukan dan pengeluaran bulan tersebut.
- Given tidak ada transaksi pada bulan Desember, When pemilik memilih filter "Desember", Then sistem menampilkan pesan "Tidak ada transaksi pada periode ini".
Sumber: catatan wawancara klien no. 2 dan 7
[Asumsi: ya — konfirmasi periode rekap rutin klien (mingguan/bulanan)]

## US-08 Mencari transaksi berdasarkan kata kunci keterangan
Sebagai admin keuangan, saya ingin mencari transaksi berdasarkan kata kunci pada keterangan agar saya dapat menemukan catatan nota tertentu dengan cepat.
Kriteria penerimaan:
- Given terdapat 20 transaksi dan 2 di antaranya memuat kata "semen", When admin mengetik "semen" di kotak pencarian, Then sistem hanya menampilkan 2 transaksi yang memuat kata tersebut.
- Given admin mencari kata "xyz" yang tidak ada di riwayat, When pencarian dijalankan, Then sistem menampilkan pesan "Transaksi tidak ditemukan".
Sumber: catatan wawancara klien no. 3 dan 4
[Asumsi: ya — konfirmasi ke klien]

## US-09 Mengunduh laporan rekap keuangan ke berkas CSV
Sebagai pemilik usaha, saya ingin mengunduh daftar transaksi ke berkas CSV agar laporan bulanan mudah dicetak atau disimpan sebagai arsip cadangan.
Kriteria penerimaan:
- Given terdapat 5 transaksi tersimpan, When pemilik mengklik tombol "Unduh CSV", Then peramban mengunduh berkas `.csv` berisi 1 baris header dan 5 baris data transaksi yang sesuai.
- Given filter bulan "November" sedang aktif (2 transaksi), When pemilik mengklik "Unduh CSV", Then berkas yang diunduh hanya memuat 2 transaksi bulan November tersebut.
Sumber: catatan wawancara klien no. 2 dan 7
[Asumsi: ya — konfirmasi format arsip yang biasa dipakai klien]

## US-10 Menjaga keamanan tampilan masukan dari karakter HTML
Sebagai pemilik usaha, saya ingin agar teks keterangan yang mengandung simbol atau tanda kurung sudut tidak merusak tampilan halaman agar aplikasi tetap aman saat dipakai sehari-hari.
Kriteria penerimaan:
- Given pengguna mengetik `<b>tes</b>` pada kolom keterangan, When transaksi disimpan dan ditampilkan di tabel, Then teks tampil persis sebagai tulisan `<b>tes</b>` dan tidak berubah menjadi huruf tebal.
- Given pengguna mencoba melewati batas `maxlength` lewat Inspect Element dengan mengirim 80 karakter, When formulir dikirim, Then server hanya menyimpan 50 karakter pertama.
Sumber: catatan wawancara klien no. 5 dan 6
[Asumsi: tidak — kebutuhan keamanan standar dari Jobsheet 1]

## US-11 Menampilkan halaman panduan singkat penggunaan aplikasi
Sebagai staf baru atau pengguna non-teknis, saya ingin membuka halaman `/bantuan` berisi langkah-langkah singkat pencatatan transaksi agar tidak bingung saat pertama kali memakai aplikasi.
Kriteria penerimaan:
- Given pengguna berada di beranda, When pengguna mengklik menu "Bantuan", Then halaman `/bantuan` terbuka dan menampilkan daftar bernomor minimal 3 langkah penggunaan.
- Given pengguna berada di halaman `/bantuan`, When pengguna mengklik tautan "Kembali ke Beranda", Then halaman kembali ke `/`.
Sumber: catatan wawancara klien no. 5 dan 6
[Asumsi: ya — konfirmasi tingkat literasi komputer staf klien]

## US-12 Menjalankan aplikasi secara lokal saat internet tidak stabil
Sebagai pemilik usaha, saya ingin pencatatan keuangan tetap berjalan di komputer lokal meskipun koneksi internet mati agar operasional harian tidak terhenti.
Kriteria penerimaan:
- Given komputer klien tidak terhubung ke internet, When aplikasi dijalankan di `http://127.0.0.1:5000` dan transaksi baru disimpan, Then data tetap tersimpan ke berkas penyimpanan lokal dan muncul di riwayat dalam waktu <= 2 detik.
- Given server dihentikan lalu dijalankan kembali, When beranda dibuka ulang, Then seluruh transaksi yang sudah dicatat sebelumnya tetap tampil lengkap.
Sumber: catatan wawancara klien no. 6
[Asumsi: ya — konfirmasi kestabilan internet di lokasi klien]

---

## Tinjauan Saran AI untuk User Story Klien Nyata (Langkah 13)
| ID | Sesuai kebutuhan klien? | Kecil dan teruji? | Keputusan | Alasan |
|---|---|---|---|---|
| US-01 s.d. US-05 | Ya | Ya | Terima | Seluruh story kecil, spesifik satu kemampuan, dan memiliki angka uji yang jelas pada kriteria Given-When-Then. |
| US-06 & US-07 | Ya | Ya | Ubah | AI sempat menyarankan grafik pie-chart berbasis JavaScript; diubah menjadi tabel filter teks sederhana agar tetap mematuhi batasan tanpa JavaScript dan ringan di laptop standar. |
| US-09 | Ya | Ya | Ubah | AI menyarankan ekspor PDF dengan pustaka eksternal tambahan; diubah menjadi ekspor CSV agar cukup memakai pustaka standar Python (`csv`). |
| Saran tambahan AI (Integrasi Bank/E-Wallet) | Tidak | Tidak | Tolak | Di luar ruang lingkup proyek (Bagian A `pedoman-wawancara.md`) dan tidak diminta klien. |