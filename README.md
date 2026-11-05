# Proposal Generator FT UTM

> **Framework Otomatisasi Pembuatan Proposal Skripsi Berstandar Resmi Fakultas Teknik Universitas Trunojoyo Madura (FT UTM)**  
> *Sesuai dengan Daftar Cek Seminar Proposal Teknik Informatika (TIF) v06 & Panduan Penulisan Skripsi Bab VII.*

[![Format](https://img.shields.io/badge/Standar-FT%20UTM%20v06-blue.svg)](checklists/ft-utm-tif-v06.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)](https://www.python.org/)
[![Pandoc](https://img.shields.io/badge/Pandoc-3.0+-orange.svg)](https://pandoc.org/)

---

## Gambaran Umum

**Proposal Generator FT UTM** adalah framework rekayasa dokumen akademik yang mengubah naskah Markdown sederhana menjadi dokumen Microsoft Word (`.docx`) dan PDF resmi yang siap diserahkan ke Dosen Pembimbing dan penguji seminar proposal.

Menulis naskah akademik di Microsoft Word secara manual sering kali menimbulkan frustrasi akibat pergeseran margin, penomoran halaman yang kacau (campuran romawi dan arab), daftar isi yang halamannya tidak sinkron, serta tata letak tabel dan gambar yang tidak konsisten. Framework ini memisahkan secara tegas antara **konten naskah** (ditulis dalam Markdown murni) dan **tata letak visual** (diatur secara deterministik oleh OpenXML engine dan Pandoc).

---

## Fitur Utama

- **Kepatuhan Ceklist 100%:** Divalidasi secara otomatis terhadap seluruh ketentuan operasional *Daftar Cek Seminar Proposal TIF v06*.
- **Pemisahan Seksi & Penomoran Halaman Ganda:** 
  - Cover tanpa nomor halaman.
  - Bagian awal (*Abstrak, Daftar Isi, Daftar Gambar, Daftar Tabel*) menggunakan angka Romawi kecil (`i, ii, iii...`) di bawah-tengah.
  - Bagian inti (*BAB I s.d. BAB III*) menggunakan angka Arab (`1, 2, 3...`) dengan penomoran awal bab di bawah-tengah dan halaman lanjutan di kanan-atas (*different first page*).
- **Daftar Isi Dinamis dengan Nomor Halaman Riil:** Nomor halaman di Daftar Isi disinkronkan langsung dari hasil render fisik PDF, sehingga akurat tanpa perlu pembaruan manual (*update field*).
- **Format Sampul Resmi (V-Shape):** Pemecahan baris judul proposal secara proporsional membentuk piramida terbalik (huruf V) lengkap dengan lambang UTM pentagon 4 cm, identitas mahasiswa, dan dosen pembimbing.
- **Sitasi Otomatis Bergaya APA Numerik:** Sitasi naskah diformat menggunakan angka kurung siku urut kemunculan (`[1]`, `[2–4]`) dan terhubung otomatis dengan bibliografi APA 7th Edition di Daftar Pustaka.
- **Dua Pilihan Kerangka Naskah:** Tersedia starter kit siap pakai untuk:
  - **Opsi A (TPL):** Rekayasa Perangkat Lunak (Waterfall/Prototype, analisis kebutuhan fungsional, diagram UML, dan black box testing).
  - **Opsi B (Kecerdasan Komputasional):** Artificial Intelligence / NLP / Data Science (alur penelitian ISO 5807, pemodelan data, evaluasi QWK/RMSE/MAE).
- **Generator Diagram ISO 5807:** Pembuatan bagan alir penelitian dan perancangan sistem beresolusi tinggi (200–300 DPI) bebas blur.
- **Auditor Ceklist Otomatis:** Perintah mandiri untuk memeriksa dokumen dan menghasilkan laporan kepatuhan `LAPORAN_PEMERIKSAAN_CEKLIST.md`.

---

## Prasyarat Sistem

Pastikan perangkat Anda memiliki:
- Python 3.10 atau lebih baru
- Pandoc 3.0 atau lebih baru
- LibreOffice (untuk auto-inject nomor halaman TOC)
- Poppler-utils (`pdftotext`, `pdfinfo`)
- ImageMagick (`convert`)

### Instalasi di Ubuntu / Debian:
```bash
sudo apt update
sudo apt install pandoc libreoffice poppler-utils imagemagick python3-yaml
```

---

## Panduan Cepat (Quickstart)

### 1. Gandakan Repositori
```bash
git clone https://github.com/AchmadLutfi196/proposal-generator.git
cd proposal-generator
```

### 2. Mulai Proyek Proposal Baru
Pilih salah satu kerangka yang sesuai dengan topik Anda:

```bash
# Untuk topik AI / Data Science (Opsi B):
cp -r skeletons/Opsi-B-Kecerdasan-Komputasi proposal-saya
cd proposal-saya

# Atau untuk topik Rekayasa Perangkat Lunak (Opsi A):
# cp -r skeletons/Opsi-A-TPL proposal-saya
# cd proposal-saya
```

### 3. Edit Metadata dan Konten Naskah
- Buka `metadata.yml` untuk mengisi Judul (8–12 kata kapital), Nama Penulis, NPM, Dosen Pembimbing, Abstrak, dan Kata Kunci.
- Edit naskah di dalam folder `chapters/`:
  - `chapters/01-pendahuluan.md`
  - `chapters/02-tinjauan-pustaka.md`
  - `chapters/03-metodologi.md`
- Tambahkan referensi BibTeX di `references.bib` dan sitasi dengan `@citekey`.

### 4. Kompilasi Proposal Menjadi Word
```bash
python3 ../scripts/build_proposal.py .
```
Dokumen Word final akan dibuat di `output/Proposal_Skripsi.docx` dan sistem akan langsung menjalankan audit kepatuhan terhadap ceklist.

### 5. Menjalankan Audit Ceklist Saja
```bash
python3 ../scripts/check_proposal.py . --docx output/Proposal_Skripsi.docx
```

---

## Dokumentasi Tambahan

- [Panduan Lengkap Penggunaan](docs/PANDUAN_PENGGUNAAN.md)
- [Matriks Pemetaan Ceklist Seminar Proposal v06](docs/CEKLIST_MAPPING.md)
- [Dokumentasi Resolusi Konflik Aturan Penulisan](docs/CONFLICTS_RESOLVED.md)

---

## Kontribusi dan Lisensi

Dikembangkan sebagai proyek sumber terbuka untuk mendukung kegiatan akademik mahasiswa dan dosen di Fakultas Teknik Universitas Trunojoyo Madura.

Didistribusikan di bawah lisensi [MIT](LICENSE).
