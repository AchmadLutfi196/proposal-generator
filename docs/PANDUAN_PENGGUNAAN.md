# Panduan Penggunaan Proposal Generator FT UTM

> Untuk panduan lengkap lintas OS (Linux/Windows/WSL2), cara pakai via agent, arsitektur, dan troubleshooting, lihat [PANDUAN_LENGKAP.md](PANDUAN_LENGKAP.md).


Framework ini dirancang untuk memudahkan mahasiswa dan dosen pembimbing dalam menyusun proposal skripsi berstandar resmi **Fakultas Teknik Universitas Trunojoyo Madura (FT UTM)**, mematuhi seluruh butir pada **Daftar Cek Seminar Proposal TIF v06** dan **Buku Panduan Penulisan Skripsi Bab VII**.

---

## 1. Prasyarat Sistem

Sebelum menjalankan generator, pastikan perangkat Anda telah terpasang:
- **Python 3.10+**
- **Pandoc 3.0+** (`pandoc --version`)
- **LibreOffice** (`soffice --version`) — untuk sinkronisasi nomor halaman TOC otomatis
- **Poppler Utils** (`pdftotext -v`, `pdfinfo -v`)
- **ImageMagick** (`convert -version`) — untuk render gambar diagram PNG

Di Ubuntu/Debian, dependensi dapat dipasang melalui terminal:
```bash
sudo apt update
sudo apt install pandoc libreoffice poppler-utils imagemagick python3-yaml
```

---

## 2. Struktur Direktori Proyek

```
proposal-generator/
├── checklists/
│   └── ft-utm-tif-v06.yml       # Definisi mesin ceklist v06 (6 halaman)
├── presets/
│   ├── utm-proposal.yml         # Preset resmi FT UTM (margin 4-3-3-3 cm, TNR 12pt, spasi 1.5)
│   └── standard.yml             # Preset umum proposal akademik
├── skeletons/
│   ├── KC-Kecerdasan-Komputasi/ # Kerangka Kecerdasan Komputasional (CNN/ML/metrik)
│   ├── KBA-Komputasi-Bahasa-Alami/ # Kerangka Komputasi Bahasa Alami (NLP/IndoBERT)
│   ├── TPL-Teknologi-Perangkat-Lunak/ # Kerangka Rekayasa Perangkat Lunak (Waterfall/UML)
│   └── STD-Sistem-Terdistribusi/  # Kerangka Sistem Terdistribusi (load balancing/failover)
├── templates/
│   ├── reference.docx           # Dokumen referensi OpenXML dengan style resmi
│   ├── docx.lua                 # Filter Pandoc penata bab, cover V-shape, & TOC
│   ├── apa-numeric.csl          # Format sitasi APA numerik [1], [2–4]
│   └── logo-utm.jpg             # Lambang resmi UTM pentagon 4 cm
├── scripts/
│   ├── build_proposal.py        # Eksekutor utama pembuatan proposal (DOCX + PDF)
│   ├── check_proposal.py        # Pemeriksa otomatis kepatuhan ceklist
│   ├── make_reference_docx.py   # Generator reference.docx
│   ├── finalize_docx.py         # Penata partisi seksi (Romawi awal, Arab inti)
│   ├── docx_pagenum.py          # Sinkronisasi nomor halaman riil daftar isi
│   └── render_figures.py        # Pembuat diagram alir ISO 5807
└── examples/
    └── demo-proposal/           # Contoh proposal utuh yang 100% lulus audit ceklist
```

---

## 3. Alur Pembuatan Proposal Baru

### Langkah 1: Gandakan Kerangka Pilihan Anda
Pilih kerangka yang sesuai dengan bidang minat Anda:
- **KC (Kecerdasan Komputasional):** AI / Computer Vision / Data Science / prediksi.
- **KBA (Komputasi Bahasa Alami):** NLP / teks / bahasa.
- **TPL (Teknologi Perangkat Lunak):** Rekayasa Perangkat Lunak / Web / Mobile / IoT.
- **STD (Sistem Terdistribusi):** Load balancing / microservice / replikasi / failover.

Contoh membuat proyek baru:
```bash
cp -r skeletons/KC-Kecerdasan-Komputasi proyek-proposal-saya   # KBA/TPL/STD untuk bidang lain
cd proyek-proposal-saya
```

### Langkah 2: Sesuaikan Metadata (`metadata.yml`)
Buka berkas `metadata.yml` dan sesuaikan data penelitian Anda:
```yaml
title: "JUDUL PROPOSAL SKRIPSI ANDA MEMUAT DELAPAN HINGGA DUA BELAS KATA"
author_name: "NAMA LENGKAP MAHASISWA"
author_nim: "210411100099"
advisor_1_name: "Nama Dosen Pembimbing I, Gelar"
advisor_1_nip: "198001012005011001"
advisor_2_name: "Nama Dosen Pembimbing II, Gelar"
advisor_2_nip: "198502022010012002"
abstract_id: |
  Tulis abstrak dalam tepat 1 paragraf, maksimal 200 kata, spasi 1.0...
keywords_id:
  - Kata Kunci 1
  - Kata Kunci 2
  - Kata Kunci 3
```

### Langkah 3: Tulis Naskah Bab di `chapters/`
Tulis isi proposal menggunakan format Markdown standar:
- `chapters/01-pendahuluan.md`: Latar Belakang (minimal 1000 kata), Rumusan Masalah bernomor (1., 2.), Tujuan, Manfaat, Batasan Masalah, dan Jadwal Penelitian.
- `chapters/02-tinjauan-pustaka.md`: Teori Dasar dan Penelitian Terdahulu (minimal 5 penelitian, format tabel komparasi).
- `chapters/03-metodologi.md`: Alur penelitian dengan diagram, teknik perolehan data, metode komputasi, dan skenario pengujian.

### Langkah 4: Tambahkan Referensi di `references.bib`
Tambahkan entri BibTeX di `references.bib`. Sitasi di dalam naskah dilakukan dengan sintaks `@citekey`, contoh:
```markdown
Menurut penelitian terdahulu yang dilakukan oleh Xiao et al. [@xiao2025human], ...
```
Filter akan mengonversinya secara otomatis menjadi sitasi berurutan `[1]`, `[2–4]` sesuai ketentuan ceklist FT UTM.

---

## 4. Perintah Kompilasi dan Pemeriksaan

### Kompilasi Naskah Menjadi DOCX
Jalankan perintah berikut di folder proyek proposal Anda:
```bash
python3 ../scripts/build_proposal.py .
```
Dokumen Word final akan tersimpan di `output/Proposal_Skripsi.docx` lengkap dengan:
1. Cover resmi piramida terbalik dan logo 4 cm.
2. Penomoran romawi kecil (`i, ii, ...`) di bawah-tengah pada bagian awal.
3. Penomoran arab (`1, 2, ...`) pada bagian inti (awal bab di bawah-tengah, halaman lanjutan di kanan-atas).
4. Daftar Isi dengan nomor halaman aktual.
5. Tabel dan Gambar ber-caption resmi beserta baris Sumber.

### Menjalankan Audit Ceklist Mandiri
Untuk memeriksa apakah dokumen Anda sudah memenuhi seluruh ketentuan ceklist sebelum diserahkan ke dosen:
```bash
python3 ../scripts/check_proposal.py . --docx output/Proposal_Skripsi.docx
```
Laporan lengkap akan ditampilkan di terminal dan disimpan dalam berkas `LAPORAN_PEMERIKSAAN_CEKLIST.md`.

---

## 5. Cara Pakai via Agent (Codex / Opencode / Orca / Cursor / ChatGPT Work)

Mahasiswa lain tidak perlu belajar struktur skeleton. Cukup scaffold dari satu topik bebas, lalu serahkan folder proyek ke agent apa pun:

```bash
python3 scripts/new_proposal.py "<topik bebas>" --nama "<Nama>" --nim "<NIM>"
cd <folder-proyek>
# agent membaca topik.yml + ../agent/AGENT_PROMPT.md dan mengisi bab sampai audit lulus
python3 ../scripts/build_proposal.py .
```

SOP agent: lihat `agent/AGENT_PROMPT.md`. Skill untuk harness yang mendukung skill: `.agents/skills/proposal-generator/SKILL.md`.
