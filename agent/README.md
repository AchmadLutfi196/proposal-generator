# agent/ — Lapisan Agent untuk Proposal Generator FT UTM

Folder ini adalah **kontrak portable** agar mahasiswa lain cukup memasukkan topik bebas, lalu menjalankannya di agent harness masing-masing (Codex, OpenCode, Orca, Cursor, ChatGPT Work, Claude Code) tanpa mulai dari nol.

| Berkas | Fungsi |
|---|---|
| `AGENT_PROMPT.md` | SOP utama agent penulis: pipeline, aturan otoritas, loop audit |
| `../scripts/new_proposal.py` | CLI scaffold: `topik bebas → folder proyek + topik.yml + PETUNJUK_AGENT.md` |

## Alur cepat

```bash
# 1. Scaffold dari topik bebas (pilih opsi A/B otomatis, bisa override --opsi)
python3 scripts/new_proposal.py "Sistem Informasi Peminjaman Laboratorium Berbasis Web" \
  --nama "Nama Mahasiswa" --nim "210411100099"

# 2. Buka folder proyek, serahkan topik.yml + PETUNJUK_AGENT.md ke agent apa pun
cd sistem-informasi-peminjaman-laboratorium-berbasis-web

# 3. Agent mengikuti AGENT_PROMPT.md sampai audit lulus
python3 ../scripts/build_proposal.py .
python3 ../scripts/check_proposal.py . --docx output/Proposal_Skripsi.docx
```

## Kenapa bukan skill Orca lagi?

Skill `orchestration` lama mengatur multi-agent di dalam Orca. Kontrak baru ini **agnostik-harness**: yang dibawa ke mesin mahasiswa bukan skill Orca, melainkan `topik.yml` + SOP + CLI, sehingga Codex/OpenCode/Cursor/dll. semuanya membaca instruksi yang sama. Orca tetap bisa dipakai sebagai orkestrator (lihat §3 AGENT_PROMPT.md).

## Skill gaya tulisan
`.agents/skills/humanizer/` — Humanizer (dari repo GitHub [@blader/humanizer](https://github.com/blader/humanizer), MIT).
`.agents/skills/stop-slop/` — Stop Slop oleh Hardik Pandya (MIT), dengan `references/` (phrases, structures, examples).

## Prasyarat
Python 3.10+, Pandoc 3.0+, LibreOffice, Poppler, ImageMagick — lihat `README.md` utama.

Panduan lengkap: `docs/PANDUAN_LENGKAP.md`.
