# Daftar Temuan Keamanan — Pertemuan 11 (Bahan Code Review Pertemuan 12)

| No | Temuan Keamanan | Kategori / Risiko | Status & Tindakan |
|---|---|---|---|
| 1 | Belum ada pembatasan percobaan login (*rate limiting*) pada `/login`. | Autentikasi (*Brute Force*) | Ditunda ke Pertemuan 12 (*code review* & keamanan). |
| 2 | Formulir `POST` (tambah, ubah, hapus, logout) belum dilengkapi token CSRF. | Integritas / CSRF | Ditunda ke Pertemuan 12 (penambahan proteksi CSRF). |
| 3 | Atribut cookie `SESSION_COOKIE_SECURE=True` belum aktif dan `app.run(debug=True)` masih dipakai lokal. | Konfigurasi Keamanan | Diaktifkan saat rilis HTTPS (Pertemuan 12 & 14); `debug=False` wajib sebelum produksi. |
| 4 | Nilai bawaan `SECRET_KEY` masih memiliki *fallback* lokal di `app.py`. | Manajemen Rahasia | Wajib diisi dari variabel lingkungan tanpa *fallback* saat produksi (Pertemuan 12). |