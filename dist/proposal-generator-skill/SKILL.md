---
name: proposal-generator
description: "Generate proposal skripsi berstandar FT UTM (Ceklist TIF v06) dari satu topik bebas. Gunakan saat pengguna meminta proposal skripsi, seminar proposal, atau scaffold dari satu topik. Mengekseskusi engine di scripts/ (Pandoc + docx.lua + reference.docx) dan audit ceklist otomatis sampai lulus."
---

# Proposal Generator FT UTM

Skill ini mengubah **satu topik bebas atau sekadar ide "mau buat apa"** menjadi `Proposal_Skripsi.docx` FT UTM yang lulus audit ceklist — tanpa mulai dari nol. Engine sumber disimpan di repo `proposal-generator`; skill ini adalah CLI-nya.

## 0. Satu Prasyarat

Verifikasi dulu environment. Kalau ada yang hilang, berhenti dan Suruh user install (lihat prasyarat di bawah) — jangan melanjut separuh jalan.

```bash
python3 --version       # butuh >=3.10
pandoc --version | head -1   # butuh >=3.0
soffice --version       # opsional; bila tidak ada, TOC tidak disinkron otomatis (ada fallback)
pdftotext -v; pdfinfo -v; convert -version | head -1
python3 -c "import yaml" 2>&1
```

Prasyarat Linux/Debian: `sudo apt install pandoc libreoffice poppler-utils imagemagick python3-yaml`.
Windows: WSL2 direkomendasikan; Windows native pakai `py -3` dan pastikan `C:\Program Files\LibreOffice\program` di PATH.

## 1. Aturan otoritas (baca filenya, jangan dari ingatan)

- `presets/utm-proposal.yml` — margin A4 4-3-3-3 cm, Times New Roman 12 pt, spasi 1,5, judul 8–12 kata, sitasi apa-numeric.
- `checklists/ft-utm-tif-v06.yml` — rule `type: automated` wajib lulus 100%; `manual` (ADM-*) ranah admin/dosen.
- `docs/PANDUAN_LENGKAP.md` — dokumen lengkap engine.
- `examples/demo-proposal/` — contoh naskah yang sudah lulus audit (pola isi, bukan untuk disalin mentah).

## 2. Pipeline wajib (jangan skip)

### Langkah 1 — Scaffold dari topik bebas (pilih opsi otomatis)

```bash
python3 scripts/new_proposal.py "<topik bebas>" \
  --nama "<Nama Lengkap>" --nim "<NIM>" \
  [--dosen1 "<Pemb I, Gelar>"] [--dosen2 "<Pemb II, Gelar>"] \
  [--opsi A|B] [--dry-run]
```

Heuristik: sistem/web/aplikasi/iot/manajemen → **A (TPL: waterfall/UML/black box)**; AI/CNN/NLP/klasifikasi/citra/deteksi → **B (Kecerdasan Komputasi: pipeline ML/metrik)**; tak ada keyword → default B. Scaffold menghasilkan folder proyek berisi `topik.yml` (topik+identitas+alasan opsi), `PETUNJUK_AGENT.md`, `metadata.yml`, `chapters/`, `references.bib`.

### Langkah 2 — Produkkan konten dari `topik.yml`

1. **Judul final** 8–12 kata kapital → `metadata.yml:title`, `topik.yml:judul_usulan` (engine yang membuat V-shape).
2. **Metadata**: penulis, NIM, pembimbing + NIP, tahun; abstrak ID+EN tepat 1 paragraf ≤200 kata; kata kunci 3–5.
3. **Bab**:
   - `chapters/01-pendahuluan.md`: Latar Belakang ≥1000 kata (global→lokal→gap→kontribusi), Rumusan Masalah (Permasalahan/Metode Usulan/Pertanyaan Penelitian), Tujuan, Manfaat (teoritis+praktis), Batasan, Sistematika, Jadwal Penelitian (tabel).
   - `chapters/02-tinjauan-pustaka.md`: teori dasar + ≥5 penelitian terdahulu + tabel komparasi + celah riset.
   - `chapters/03-metodologi.md`: alur/diagram ISO 5807, data, metode komputasi/perancangan, skenario pengujian.
   - Sitasi selalu `[@citekey]`; **jangan** tulis `[1]` manual — engine yang menomori.
4. **Referensi**: ≥5 jurnal/prosiding ≤5 tahun + ≥5 textbook ≤20 tahun di `references.bib`. **Dilarang mengarang** — verifikasi venue/tahun.

### Langkah 3 — Pass anti-slop (wajib)

Bacakan skill `.agents/skills/humanizer/SKILL.md` dan `.agents/skills/stop-slop/SKILL.md` (+ `references/`-nya), lalu terapkan pada `chapters/*.md` + abstrak: buang frasa AI generik ("Di era digital…", "Selain itu…", "Secara keseluruhan…"), pola "bukan X melainkan Y" berlebih, triad repetitif. Suara tetap formal akademik, kalimat bervariasi, tanpa em dash/pull-quote. **Jangan** mengubah fakta, sitasi `[@key]`, angka, atau struktur heading.

### Langkah 4 — Kompilasi & audit (loop sampai lulus)

```bash
# Dari dalam folder proyek:
python3 ../scripts/build_proposal.py .
python3 ../scripts/check_proposal.py . --docx output/Proposal_Skripsi.docx
```

Perbaiki setiap `FAIL` otomatis sampai bersih; butir `manual` ADM-* biarkan. **Target: `output/Proposal_Skripsi.docx` + `LAPORAN_PEMERIKSAAN_CEKLIST.md` tanpa FAIL otomatis.**

### Langkah 5 — Serahkan

Laporkan path `.docx`, hasil audit, judul final, opsi terpilih, daftar referensi yang dipakai.

## 3. Larangan keras

- Jangan edit file di luar folder proyek (engine, `templates/`, `presets/`, `checklists/`).
- Jangan memalsukan sitasi, judul jurnal, atau data hasil penelitian.
- Jangan mengubah identitas dari `topik.yml` tanpa konfirmasi user.
- Jangan klaim "selesai" sebelum audit tanpa FAIL otomatis.

## 4. Orca opsional (multi-agent)

Pecah jadi Task per peran: `penulis-bab1`, `penulis-bab2`, `penulis-bab3`, `kurator-referensi`, `auditor` — satu Task satu spec mandiri, bukti selesai = audit lulus.
