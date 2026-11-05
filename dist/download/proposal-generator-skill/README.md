# proposal-generator (skill)

Skill standalone berbasis `SKILL.md` untuk membuat proposal skripsi FT UTM (Ceklist TIF v06) dari satu topik bebas — bisa dipasang di Claude.ai / Codex / OpenCode / Orca / Cursor / ChatGPT Work, dll.

## Isi bundle

| Berkas | Fungsi |
|---|---|
| `SKILL.md` | SOP skill (alat yang dibaca agent; frasa trigger: proposal skripsi, seminar proposal, generate proposal, scaffold dari topik) |
| `scripts/new_proposal.py` | CLI scaffold: topik bebas → folder proyek + `topik.yml` + `PETUNJUK_AGENT.md`, pilih Opsi A/B otomatis |
| `scripts/build_proposal.py` | Pipeline kompilasi (Pandoc → finalisasi seksi → sinkron TOC → audit) |
| `scripts/check_proposal.py` | Auditor ceklist v06 → `LAPORAN_PEMERIKSAAN_CEKLIST.md` |
| `templates/agent_AGENTS.md` | Template `AGENTS.md` repo-level (simpan sebagai `AGENTS.md` repo tujuan) |
| `references/evidence.md` | Buki verifikasi (hasil test engine & audit) |

## Prasyarat

Python 3.10+, Pandoc 3.0+, LibreOffice (`soffice`), Poppler (`pdftotext`, `pdfinfo`), ImageMagick (`convert`), PyYAML. Linux: `sudo apt install pandoc libreoffice poppler-utils imagemagick python3-yaml`. Windows: WSL2 direkomendasikan (atau `py -3` + PATH LibreOffice).

## Cara pasang di harness

- **Claude.ai**: Settings → Skills → upload `.zip` berisi folder skill ini (harus ada file `SKILL.md` di akar zip).
- **Codex CLI**: `git clone` repo `proposal-generator`, jalankan dari folder repo (skill tersedia di `.agents/skills/proposal-generator/`); atau salin folder ini ke `~/.agents/skills/proposal-generator/`.
- **OpenCode/Cursor/Orca**: salin folder ini ke direktori skills harness masing-masing (biasanya `~/.agents/skills/` atau folder `.agents/skills/` di repo).

## Sekali jalan

```bash
python3 scripts/new_proposal.py "<topik bebas>" --nama "<Nama>" --nim "<NIM>"
cd <folder-proyek>
python3 ../scripts/build_proposal.py .
```

Hasil: `output/Proposal_Skripsi.docx` + `LAPORAN_PEMERIKSAAN_CEKLIST.md` tanpa FAIL otomatis (format: A4 4-3-3-3 cm, TNR 12pt spasi 1.5, cover V-shape 8-12 kata, penomoran romawi/arab ganda, sitasi apa-numeric).
