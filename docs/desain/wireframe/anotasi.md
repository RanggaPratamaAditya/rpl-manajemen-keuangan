# Anotasi Wireframe dan Penerapan Prinsip Antarmuka — Sistem Manajemen Keuangan UMKM

## 1. Tabel Anotasi Halaman Utama
| Halaman | No | Elemen | Data / aksi | Aturan / pesan yang muncul | Prinsip antarmuka |
|---|---|---|---|---|---|
| Semua (`wf-02`–`wf-07`) | 1 | Menu navigasi atas | Pindah halaman & tombol Keluar | Posisi dan urutan menu sama di semua halaman; menu `Kategori` dan `Ekspor CSV` hanya tampil bagi `Pemilik`; ukuran huruf utama >= 16 piksel (`KNF-05`). | Konsistensi & Keterbacaan |
| `wf-01` Login | 2–4 | Form username, sandi, & pesan galat | `pengguna.username`, `password_hash`, aksi Masuk | Kedua kolom wajib diisi; bila salah tampil pesan `"Username atau kata sandi salah"`. | Umpan balik & Pencegahan galat |
| `wf-02` Beranda | 2–4 | Kartu ringkasan saldo & 5 transaksi terbaru | `SUM(transaksi.nominal)` per jenis & 5 baris terbaru | Total dihitung otomatis (tidak disimpan); bila data kosong tampil `Rp 0` tanpa galat (`UC-03`). | Kesederhanaan & Umpan balik |
| `wf-03` Catat Transaksi | 2 | Ruang pesan galat/sukses | Status penyimpanan transaksi | Sukses: `"Transaksi berhasil disimpan"`. Gagal: `"Keterangan dan kategori wajib diisi"` atau `"Nominal harus berupa angka bulat positif"` (`UC-01`, `KF-02`). | Umpan balik |
| `wf-03` Catat Transaksi | 3 | Isian keterangan & nominal | `transaksi.keterangan`, `transaksi.nominal` | Keterangan wajib 1–50 karakter (`KNF-02`); nominal hanya angka bulat `> 0` (`KF-02`); pencatatan selesai dalam <= 3 langkah (`KNF-04`). | Pencegahan galat & Kegunaan |
| `wf-03` Catat Transaksi | 4 | Tombol `Batal` & `Simpan Transaksi` | Kembali ke Beranda / simpan data | Tombol utama selalu di kanan bawah. | Konsistensi |
| `wf-04` Riwayat & Filter | 2–3 | Filter bulan/tahun, pencarian, & pesan kosong | Filter `transaksi.tanggal`, cari `keterangan` | Jika periode kosong tampil `"Tidak ada transaksi pada periode ini"`; jika kata kunci tidak cocok tampil `"Transaksi tidak ditemukan"` (`UC-06`). | Umpan balik |
| `wf-04` Riwayat & Filter | 5 | Tombol `Hapus` & kotak konfirmasi | Hapus `transaksi` berdasarkan `id` (khusus Pemilik) | Wajib menampilkan konfirmasi `"Yakin ingin menghapus transaksi ini?"` sebelum menghapus permanen (`UC-05`, `KF-05`). Jika ID tidak ada tampil `"Transaksi tidak ditemukan"`. | Pencegahan galat & Umpan balik |
| `wf-05` Ubah Transaksi | 2–4 | Formulir data lama & tombol `Simpan Perubahan` | Ubah `transaksi` berdasarkan `id` | Validasi sama dengan `wf-03` (`KF-02`); keterangan > 50 karakter dipotong di server; tombol `Batal` menutup form tanpa mengubah data (`UC-04`). | Konsistensi & Pencegahan galat |
| `wf-06` Kelola Kategori | 2–3 | Form tambah kategori | `kategori.nama_kategori`, `jenis_default` | `nama_kategori` wajib unik; bila ganda tampil `"Nama kategori sudah terdaftar"`. | Pencegahan galat |
| `wf-07` Ekspor CSV | 2–5 | Pilih periode, pratinjau, & tombol `Unduh Berkas CSV` | Ekspor `transaksi` terfilter ke `.csv` | Jika periode tidak memiliki data, tombol unduh dinonaktifkan dan tampil pesan `"Tidak ada data untuk diekspor"` (`UC-07`). | Pencegahan galat & Kesederhanaan |

## 2. Contoh Perbaikan Sebelum–Sesudah Penerapan Prinsip Antarmuka
- **Sebelum:** Pada sketsa awal halaman `wf-04` (Riwayat Transaksi), tombol `Hapus` langsung menghapus baris data dalam sekali klik tanpa konfirmasi, dan tidak ada ruang pesan pemberitahuan ketika hasil filter bulan kosong. Selain itu, formulir pencatatan transaksi sempat digabung di halaman yang sama dengan tabel riwayat lengkap sehingga halaman terlalu penuh.
- **Sesudah:**
  1. **Pencegahan galat:** Ditambahkan kotak dialog konfirmasi *"Yakin ingin menghapus transaksi ini? [Batal] [Ya, Hapus]"* sebelum data dihapus permanen, dan tombol `Hapus` hanya ditampilkan untuk peran `Pemilik`.
  2. **Umpan balik:** Ditambahkan kotak pesan khusus di atas tabel untuk menampilkan *"Tidak ada transaksi pada periode ini"* atau *"Transaksi berhasil dihapus"*.
  3. **Kesederhanaan:** Formulir pencatatan dipisahkan ke halaman tersendiri (`wf-03-catat-transaksi.png`) agar halaman riwayat fokus pada pencarian dan penyaringan data.