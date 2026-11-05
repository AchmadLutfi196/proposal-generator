# AGENTS.md — Proposal Generator FT UTM

## Tentang repo
Framework otomasi proposal skripsi FT UTM (TIF v06): naskah Markdown → DOCX/PDF berstandar prodi. Engine deterministik (Pandoc + OpenXML), konten ditulis manusia/agent.

## Struktur
- `scripts/` — engine: `build_proposal.py` (pipeline), `check_proposal.py` (auditor), `new_proposal.py` (scaffold dari topik bebas), `finalize_docx.py`, `docx_pagenum.py`, `make_reference_docx.py`, `render_figures.py`
- `agent/AGENT_PROMPT.md` — SOP agent penulis proposal (kontrak portable lintas harness)
- `skeletons/Opsi-A-TPL|Opsi-B-Kecerdasan-Komputasi/` — starter kit per bidang
- `templates/`, `presets/utm-proposal.yml`, `checklists/ft-utm-tif-v06.yml` — otoritas format (baca filenya, jangan hafal)
- `examples/demo-proposal/` — contoh yang sudah lulus audit

## Aturan kerja agent
1. Jangan edit `templates/`, `presets/`, `checklists/`, `scripts/` (selain `new_proposal.py`) untuk keperluan isi proposal — hanya isi konten di folder proyek.
2. Setiap proposal baru dimulai dari `scripts/new_proposal.py "<topik bebas>"` (menghasilkan `topik.yml` + `PETUNJUK_AGENT.md`).
3. Selesai = `output/Proposal_Skripsi.docx` + `check_proposal.py` tanpa FAIL otomatis.
4. Jangan mengarang referensi; semua entri bib harus nyata dan terverifikasi.
5. Gunakan SOP `agent/AGENT_PROMPT.md`; skill auto-trigger di `.agents/skills/proposal-generator/SKILL.md`. Panduan lengkap: `docs/PANDUAN_LENGKAP.md`.
