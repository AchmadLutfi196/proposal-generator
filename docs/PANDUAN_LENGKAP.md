# Panduan Lengkap — Proposal Generator FT UTM

> Dokumentasi lengkap framework proposal skripsi FT UTM berstandar Ceklist Seminar Proposal Teknik Informatika (TIF) v06.
> Target pembaca: mahasiswa/dosen pembimbing yang ingin membuat proposal dari **satu topik bebas** — dengan agent (Codex, OpenCode, Orca, Cursor, ChatGPT Work, Claude Code) atau manual.

## Daftar isi

1. [Ringkasan: framework ini untuk apa?](#ringkasan-framework-ini-untuk-apa)
2. [Arsitektur: konten vs format](#arsitektur-konten-vs-format)
3. [Prasyarat sistem (Linux, Windows native, Windows WSL2)](#prasyarat-sistem-linux-windows-native-windows-wsl2)
4. [Cara pakai via agent (tanpa mulai dari nol)](#cara-pakai-via-agent-tanpa-mulai-dari-nol)
5. [Cara pakai manual (tanpa agent)](#cara-pakai-manual-tanpa-agent)
6. [Berkas-berkas dalam repo](#berkas-berkas-dalam-repo)
7. [Aturan otoritas & resolusi konflik](#aturan-otoritas--resolusi-konflik)
8. [Troubleshooting](#troubleshooting)
9. [Atribusi & lisensi](#atribusi--lisensi)

---

## Ringkasan: framework ini untuk apa?

Framework ini menulis **konten proposal dalam Markdown murni** di folder proyek, lalu **engine deterministik (Pandoc + OpenXML)** mengubahnya menjadi `.docx` berstandar resmi FT UTM dan memeriksa kepatuhan terhadap ceklist TIF v06. Format yang dijamin engine:

- **Geometri**: kertas A4, margin atas 3 cm, kiri 4 cm, bawah 3 cm, kanan 3 cm, font Times New Roman 12 pt, spasi 1,5.
- **Penomoran ganda**: cover tanpa nomor; bagian awal (abstrak, daftar isi, daftar gambar, daftar tabel) romawi kecil (`i, ii, iii`) di bawah-tengah; bagian inti (BAB I–BAB III) angka arab (awal bab di bawah-tengah, lanjutan kanan-atas via *different first page*).
- **Cover V-shape**: judul 8–12 kata kapital dipecah menjadi piramida terbalik, lambang UTM pentagon 4 cm, identitas mahasiswa, dosen pembimbing.
- **Daftar isi dinamis**: nomor halaman disinkronkan dari render PDF riil (tahap `docx_pagenum.py`), bukan dibuat manual.
- **Sitasi APA numerik**: `[@citekey]` di naskah → `[1]`, `[2–4]` urut kemunculan, Daftar Pustaka otomatis via `apa-numeric.csl`.
- **Audit otomatis**: `check_proposal.py` menilai naskah + DOCX berdasarkan `checklists/ft-utm-tif-v06.yml` dan menghasilkan `LAPORAN_PEMERIKSAAN_CEKLIST.md`.

Dua skeleton siap pakai:

| Opsi | Bidang | Ciri khas |
|---|---|---|
| **A (TPL)** | Rekayasa Perangkat Lunak: sistem/web/mobile/IoT/manajemen | Waterfall/prototype, analisis kebutuhan fungsional, diagram UML, black box testing |
| **B (Kecerdasan Komputasi)** | AI/NLP/CV/data mining | Pipeline ML, pemodelan data, evaluasi QWK/RMSE/MAE/akurasi |

---

## Arsitektur: konten vs format

```
topik bebas
    │
    ▼  scripts/new_proposal.py (scaffold + heuristik opsi A/B)
folder proyek (metadata.yml, chapters/*.md, references.bib, topik.yml)
    │  ◄── agent/manual mengisi KONTEN di sini
    ▼  scripts/build_proposal.py (pipeline 4 tahap)
  [1] Pandoc + templates/docx.lua + apa-numeric.csl + reference.docx
  [2] scripts/finalize_docx.py  (partisi seksi romawi/arab)
  [3] scripts/docx_pagenum.py   (render PDF via LibreOffice -> sinkron TOC)
  [4] scripts/check_proposal.py (audit ceklist)
    │
    ▼
output/Proposal_Skripsi.docx  +  LAPORAN_PEMERIKSAAN_CEKLIST.md
```

Prinsip kerasnya: **jangan edit engine/template/preset/checklist** untuk keperluan isi proposal. Tugas penulis (manusia/agent) hanya mengisi konten folder proyek. Aturan otoritas format dibaca dari file, bukan dari ingatan: `presets/utm-proposal.yml` + `checklists/ft-utm-tif-v06.yml`.

---

## Prasyarat sistem (Linux, Windows native, Windows WSL2)

### Butuh apa & buat apa

| Prasyarat | Untuk apa di framework ini |
|---|---|
| Python 3.10+ | Menjalankan semua `scripts/*.py` (new/build/check) |
| Pandoc 3.0+ | Tahap [1]: mengubah Markdown+BibTeX menjadi DOCX awal |
| LibreOffice (`soffice`) | Tahap [3]: render DOCX→PDF headless supaya nomor halaman Daftar Isi bisa disinkron ke halaman riil |
| Poppler (`pdftotext`, `pdfinfo`) | Tahap [3]: membaca PDF hasil render LibreOffice per halaman |
| ImageMagick (`convert`) | Render diagram SVG→PNG (opsional; fallback SVG bila tidak ada) |
| PyYAML | Parsing `metadata.yml` saat scaffold/build |

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install pandoc libreoffice poppler-utils imagemagick python3-yaml
```

### Windows native (PowerShell)

Install semua dan pastikan masuk PATH, lalu jalankan scripts dengan `py -3`:

```powershell
winget install python.org
winget install JohnMacFarlane.Pandoc
winget install LibreOffice.LibreOffice   # pastikan C:\Program Files\LibreOffice\program ada di PATH
winget install oschwald.poppler          # atau: scoop install poppler
winget install ImageMagick.ImageMagick
pip install pyyaml
```

```powershell
py -3 scripts\new_proposal.py "<topik bebas>" --nama "<Nama>" --nim "<NIM>"
cd <folder-proyek>
py -3 ..\scripts\build_proposal.py .
```

### Windows WSL2 (direkomendasikan untuk Windows native)

1. PowerShell (admin): `wsl --install`, buka Ubuntu.
2. Di WSL, pakai perintah Linux di atas (sudah terbukti jalan di mesin ini).
3. Clone repo di WSL, jalanin scaffold/build seperti biasa. File bisa diakses dari Windows lewat `\\wsl$\Ubuntu\home\<user>\...`.

### Fallback bila LibreOffice/Poppler tidak ada

`docx_pagenum.py` cek PATH; bila tidak ditemukan ia mencetak `[warn] ... melewati injeksi` dan dokumen tetap jadi — hanya nomor halaman Daftar Isi tidak disinkron otomatis.

---

## Cara pakai via agent (tanpa mulai dari nol)

Mahasiswa cukup memasukkan satu topik bebas. Kontrak portable `agent/AGENT_PROMPT.md` + `.agents/skills/proposal-generator/SKILL.md` dibaca oleh agent apa pun di harness-nya masing-masing.

```bash
# 1) Clone + scaffold dari topik bebas (opsi A/B dipilih otomatis; override dengan --opsi)
python3 scripts/new_proposal.py "Sistem Informasi Peminjaman Laboratorium Berbasis Web" \
  --nama "Nama Mahasiswa" --nim "210411100099"
# LIHAT dulu tanpa menulis: tambahkan --dry-run

# 2) Masuk folder proyek, buka agent (Codex/OpenCode/Orca/Cursor/ChatGPT Work)
cd sistem-informasi-peminjaman-laboratorium-berbasis-web
# Kirim prompt: "Baca ../agent/AGENT_PROMPT.md dan ikuti SOP-nya sampai audit lulus."

# 3) Kompilasi (agent akan mengisi metadata/chapters/references lalu menjalankan ini)
python3 ../scripts/build_proposal.py .
python3 ../scripts/check_proposal.py . --docx output/Proposal_Skripsi.docx
```

### Apa yang dilakukan `new_proposal.py`

- Heuristik keyword: topik "sistem/web/aplikasi/iot" → Opsi A; "AI/CNN/NLP/klasifikasi/citra/deteksi" → Opsi B; tanpa keyword → default B (bisa override `--opsi A`).
- Menyalo skeleton pilihan ke folder proyek, membuat `topik.yml` (topik + identitas + alasan opsi), `PETUNJUK_AGENT.md`, dan mengisi `metadata.yml` dari `--nama/--nim/--dosen1/--dosen2/--tahun`.

### Pipeline agent (`agent/AGENT_PROMPT.md`, ringkas)

1. Baca `topik.yml` + `metadata.yml`.
2. Konfirmasi skeleton A/B.
3. Susun judul final 8–12 kata kapital → `metadata.yml:title`, `topik.yml:judul_usulan`.
4. Isi metadata (nama, NIM, pembimbing, abstrak ID+EN ≤200 kata 1 paragraf, kata kunci 3–5).
5. Tulis bab (`01-pendahuluan.md` Latar Belakang ≥1000 kata + Rumusan Masalah/Tujuan/Manfaat/Batasan/Sistematika/Jadwal; `02-tinjauan-pustaka.md` teori + ≥5 penelitian terdahulu + tabel komparasi; `03-metodologi.md` alur + data + metode + skenario pengujian). Sitasi selalu `[@citekey]`.
6. **Anti-slop wajib**: pass skill `humanizer` + `stop-slop` pada `chapters/*.md` + abstrak (buang frasa AI generik; jangan ubah fakta, sitasi, angka, heading).
7. Referensi nyata di `references.bib` (≥5 jurnal/prosiding ≤5 th; ≥5 textbook ≤20 th). Jangan karang — verifikasi venue/tahun.
8. Loop build + audit sampai **tidak ada FAIL otomatis**. Butir `manual` (ADM-01/02/04/05/07–10: sks, KP, SISRI, logbook, dll.) dibiarkan.
9. Serahkan `output/Proposal_Skripsi.docx` + laporan.

Orca opsional multi-agent: pecah Task per peran (`penulis-bab1`, `penulis-bab2`, `penulis-bab3`, `kurator-referensi`, `auditor`), bukti selesai = audit lulus.

### Skill gaya tulisan (bawaan repo)

- `.agents/skills/humanizer/` — Humanizer oleh Siqi Chen (@blader), dari repo GitHub [blader/humanizer](https://github.com/blader/humanizer), lisensi MIT. 29 pola tulisan AI + voice calibration.
- `.agents/skills/stop-slop/` — Stop Slop oleh Hardik Pandya (MIT), dengan `references/` (phrases, structures, examples).

---

## Cara pakai manual (tanpa agent)

```bash
git clone https://github.com/AchmadLutfi196/proposal-generator.git
cd proposal-generator

# 1) Gandakan skeleton
cp -r skeletons/Opsi-B-Kecerdasan-Komputasi proposal-saya   # atau Opsi-A-TPL
cd proposal-saya

# 2) Edit metadata.yml (judul 8–12 kata kapital, nama, NIM, pembimbing, abstrak, kata kunci)
# 3) Tulis chapters/01-pendahuluan.md, 02-tinjauan-pustaka.md, 03-metodologi.md
# 4) Tambahkan referensi BibTeX di references.bib, sitasi dengan [@citekey]

# 5) Kompilasi -> output/Proposal_Skripsi.docx + audit otomatis
python3 ../scripts/build_proposal.py .

# 6) Audit saja
python3 ../scripts/check_proposal.py . --docx output/Proposal_Skripsi.docx
```

Contoh utuh yang sudah lulus audit: `examples/demo-proposal/` (judul *Pengembangan Sistem Penilaian Esai Multi-Rater Otomatis Menggunakan IndoBERT Pada Ujian Sekolah*).

---

## Berkas-berkas dalam repo

```
proposal-generator/
├── README.md                        # overview + quickstart
├── AGENTS.md                        # kontrak kerja agent di repo ini
├── agent/
│   ├── AGENT_PROMPT.md              # SOP agent penulis (pipeline wajib)
│   └── README.md                    # kontrak portable lintas harness
├── .agents/skills/
│   ├── proposal-generator/SKILL.md  # auto-trigger skill generator
│   ├── humanizer/{SKILL.md,LICENSE} # skill gaya (MIT, blader/humanizer)
│   └── stop-slop/{SKILL.md,LICENSE,references/}  # skill gaya (MIT, Hardik Pandya)
├── scripts/
│   ├── new_proposal.py              # CLI scaffold dari topik bebas
│   ├── build_proposal.py            # pipeline kompilasi (Pandoc → finalisasi → pagenum → audit)
│   ├── check_proposal.py            # auditor ceklist v06
│   ├── finalize_docx.py             # partisi seksi + penomoran romawi/arab
│   ├── docx_pagenum.py              # sinkron TOC dari render PDF (LibreOffice+Poppler)
│   ├── make_reference_docx.py       # generator reference.docx berstandar
│   └── render_figures.py            # diagram ISO 5807 → SVG/PNG
├── skeletons/
│   ├── Opsi-A-TPL/                  # sistem/web/mobile/IoT (waterfall/UML/black box)
│   └── Opsi-B-Kecerdasan-Komputasi/ # AI/NLP/CV/data (pipeline ML/metrik)
├── templates/                       # apa-numeric.csl, docx.lua, reference.docx, logo
├── presets/                         # utm-proposal.yml (resmi), standard.yml (umum)
├── checklists/                      # ft-utm-tif-v06.yml (definisi rule audit)
├── examples/demo-proposal/          # proposal contoh yang sudah lulus audit
└── docs/
    ├── PANDUAN_LENGKAP.md           # dokumen ini
    ├── PANDUAN_PENGGUNAAN.md        # panduan langkah detail
    ├── CEKLIST_MAPPING.md           # matriks rule → modul pelaksana
    └── CONFLICTS_RESOLVED.md        # resolusi konflik antar dokumen pedoman
```

### Perintah utama

| Perintah | Fungsi |
|---|---|
| `python3 scripts/new_proposal.py "<topik>" [--nama ...] [--nim ...] [--opsi A\|B] [--dry-run]` | Scaffold proyek baru |
| `python3 scripts/build_proposal.py .` (dari folder proyek) | Kompilasi → `output/Proposal_Skripsi.docx` + audit |
| `python3 scripts/check_proposal.py . --docx output/Proposal_Skripsi.docx` | Audit saja → `LAPORAN_PEMERIKSAAN_CEKLIST.md` |
| `python3 scripts/render_figures.py` | Diagram ISO 5807 |
| `python3 scripts/make_reference_docx.py templates/reference.docx` | Regen `reference.docx` |

### Produk per folder proyek

- `metadata.yml` — judul, penulis, NIM, pembimbing, abstrak, kata kunci
- `chapters/*.md` — naskah Bab I–III (Markdown + sitasi `[@key]`)
- `references.bib` — entri BibTeX
- `gambar/` — diagram (`flowchart_penelitian.svg|png`)
- `topik.yml` + `PETUNJUK_AGENT.md` — input kontrak agent (hanya ada pada hasil scaffold)
- `output/Proposal_Skripsi.docx` + `LAPORAN_PEMERIKSAAN_CEKLIST.md` — hasil build/audit

---

## Aturan otoritas & resolusi konflik

Sumber otoritas (baca filenya, jangan hafalkan):

- `presets/utm-proposal.yml` — margin 4-3-3-3 cm, Times New Roman 12 pt, spasi 1,5, judul 8–12 kata, sitasi apa-numeric.
- `checklists/ft-utm-tif-v06.yml` — rule yang `type: automated` wajib lulus 100%; `manual` (ADM-*) ranah admin/dosen.
- `docs/PANDUAN_PENGGUNAAN.md`, `docs/CEKLIST_MAPPING.md`, `examples/demo-proposal/`.

Kebijakan presedensi ketat (lihat `docs/CONFLICTS_RESOLVED.md`):

```
Ceklist Seminar Proposal v06  ≻  Template Proposal Resmi  ≻  Buku Panduan Fakultas
```

Contoh hasil rekonsiliasi: penomoran subbab `2.1` tanpa titik akhir; caption `Tabel 2.1` rapat; sitasi `[3]`, `[5–8]` dengan bibliografi APA; Latar Belakang minimal 1000 kata; minimal 5 penelitian terdahulu.

---

## Troubleshooting

| Gejala | Penyebab & fix |
|---|---|
| `[warn] ... melewati injeksi` di tahap [3/4] | LibreOffice/Poppler tidak ada di PATH (Windows). Install & tambahkan `C:\Program Files\LibreOffice\program` ke PATH. Dokumen tetap jadi. |
| `GAGAL TTL-02` (judul 6 kata) | Judul kurang dari 8 kata. Susun ulang judul final 8–12 kata kapital; engine memecahnya jadi V-shape sendiri. |
| `GAGAL ADM-03` (komposisi referensi) | Kurang dari 5 jurnal ≤5 th / 5 textbook ≤20 th di `references.bib`, atau rentang tahun salah. |
| `GAGAL CIT-03` (two-way match) | Ada `[@key]` tanpa entri di `.bib`, atau entri `.bib` tak disitasi. Sinkronkan dua arah. |
| `GAGAL CH1-02` (Latar Belakang <1000 kata) | Tambah isi Bab 1.1 sampai ≥1000 kata. |
| Pandoc error di tahap [1/4] | Pandoc <3.0 atau `reference.docx` rusak. Update Pandoc, atau regenerate `reference.docx`. |
| `or...` / tidak ada skill orchestration | Skill orchestration (Orca) tidak diperlukan untuk framework ini; pakai `scripts/new_proposal.py` + `agent/AGENT_PROMPT.md` yang agnostik harness. |

---

## Atribusi & lisensi

Framework: MIT ([LICENSE](LICENSE)). Skill gaya tulisan:

- Humanizer — © 2025 Siqi Chen, [github.com/blader/humanizer](https://github.com/blader/humanizer), MIT.
- Stop Slop — © 2025 Hardik Pandya, MIT.

Dokumen pedoman prodi (Ceklist TIF v06, Template Proposal, Panduan Penulisan Skripsi) dirujuk sebagai sumber format; framework tidak mengklaimnya sebagai milik proyek.
