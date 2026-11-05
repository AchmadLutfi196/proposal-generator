---
name: proposal-generator
description: "Generate proposal skripsi FT UTM (TIF v06) dari topik bebas untuk agent harness mana pun (Codex, OpenCode, Orca, Cursor, ChatGPT Work). Gunakan saat user meminta proposal skripsi, seminar proposal, atau scaffold dari satu topik."
---

# Proposal Generator FT UTM — Skill

## Kapan dipakai
User menyebut proposal skripsi / seminar proposal / "buatkan proposal dari topik ini" / "generate proposal".

## SOP (baca sebelum menulis apa pun)
1. Baca `agent/AGENT_PROMPT.md` (Kontrak agent — pipeline wajib, aturan otoritas).
2. Scaffold proyek baru dari topik bebas:
   ```bash
   python3 scripts/new_proposal.py "<topik bebas>" [--nama ...] [--nim ...] [--opsi KC|KBA|TPL|STD]
   ```
3. Di folder proyek (`topik.yml` + `PETUNJUK_AGENT.md`), isi `metadata.yml`, `chapters/*.md`, `references.bib` mengikuti skeleton bidang minatnya (KC/KBA/TPL/STD — 4 bidang resmi TIF v06).
4. Loop kompilasi + audit sampai lulus:
   ```bash
   python3 ../scripts/build_proposal.py .
   python3 ../scripts/check_proposal.py . --docx output/Proposal_Skripsi.docx
   ```
5. Serahkan `output/Proposal_Skripsi.docx` + laporan.

## Gaya penulisan
Gunakan skill `humanizer` + `stop-slop` (`.agents/skills/humanizer/`, `.agents/skills/stop-slop/`) sebagai pass anti-slop pada `chapters/*.md` dan abstrak sebelum kompilasi. Jangan ubah fakta, sitasi, atau struktur heading.

## Aturan
- Jangan edit engine/template/preset/checklist — hanya isi konten proyek.
- Jangan mengarang referensi; semua entri bib harus nyata & terverifikasi.
- Otoritas format: `presets/utm-proposal.yml` + `checklists/ft-utm-tif-v06.yml` (bukan ingatan model).
- Bila dijalankan di Orca & perlu multi-agent, pecah jadi Task per peran dengan bukti selesai = audit lulus.

Panduan lengkap: `docs/PANDUAN_LENGKAP.md`.
