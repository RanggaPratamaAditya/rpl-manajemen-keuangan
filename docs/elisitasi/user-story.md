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