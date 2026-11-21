# Aturan Proyek untuk Asisten AI

## Stack
- Python 3.14 (minimal 3.10), Flask, dan SQLite (tahap awal prototipe memakai JSON lokal sebelum migrasi basis data).
- Paket eksternal lain hanya boleh ditambahkan setelah disetujui kelompok dan dicatat pada `requirements.txt`.

## Struktur Folder
- `app.py`: berkas utama aplikasi Flask dan rute.
- `templates/`: templat HTML (Jinja2 dengan auto-escaping aktif).
- `static/`: berkas gaya CSS atau aset statis.
- `tests/`: berkas uji otomatis (ditambahkan pada Minggu 13).
- `docs/`: seluruh dokumen proyek (`kesepakatan-tim.md`, `product-backlog.md`, `srs.md`, dan folder `docs/elisitasi/`).
- Folder utama (*root*): `PRD.md`, `aturan-proyek.md`, `jurnal-vibe-coding.md`, dan `.github/pull_request_template.md`.

## Konvensi
- Komentar kode, pesan galat, label antarmuka, dan pesan commit menggunakan bahasa Indonesia yang jelas.
- Nama fungsi dan variabel menggunakan gaya `snake_case` yang deskriptif.
- Satu fitur/perbaikan dikerjakan pada satu branch terpisah (`fitur-...`, `perbaikan-...`, `docs-...`) dan digabung lewat Pull Request.

## Larangan
- Jangan menambah paket/pustaka luar tanpa izin.
- Jangan menaruh kata sandi, token, kunci akses, atau data pribadi klien di dalam kode maupun dokumen.
- Jangan mengubah berkas di luar yang diminta pada prompt.
- Jangan menghapus, melewati, atau melemahkan pengujian yang sudah ada.
- Jangan menuliskan fitur di luar `PRD.md` tanpa persetujuan.

## Menjalankan dan Menguji
- Aktifkan lingkungan virtual (`.venv\Scripts\Activate.ps1`), lalu jalankan aplikasi dengan:
  `python app.py`
- Buka `http://127.0.0.1:5000` di peramban untuk pengujian manual.
- Uji otomatis (`pytest`) akan ditambahkan dan dijalankan pada Minggu 13.