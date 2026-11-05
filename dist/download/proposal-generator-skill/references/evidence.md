# Bukti verifikasi (2026-11-05)

## Test engine
| Uji | Hasil |
|---|---|
| `new_proposal.py --dry-run "Sistem Informasi Peminjaman Laboratorium Berbasis Web"` | TPL — Teknologi Perangkat Lunak (skor TPL=3) |
| `new_proposal.py --dry-run "Klasifikasi Citra Penyakit Daun Kopi dengan CNN"` | KC — Kecerdasan Komputasional (skor KC=4) |
| `new_proposal.py --dry-run "Sistem Penilaian Esai ... IndoBERT"` | KBA — Komputasi Bahasa Alami (skor KBA=3) |
| `new_proposal.py --dry-run "Sistem Terdistribusi ... Load Balancing"` | STD — Sistem Terdistribusi (skor STD=3) |
| `new_proposal.py --dry-run --opsi std "Klasifikasi..."` | STD (manual, lowercase diterima) |
| Scaffold riil `/tmp/pg-e2e` "Klasifikasi Citra Penyakit Daun Kopi dengan CNN" | OK, `topik.yml` terbuat |
| `check_proposal.py examples/demo-proposal` | SUKSES (seluruh butir otomatis LULUS) |
| `build_proposal.py examples/demo-proposal` | OK → `output/Proposal_Skripsi.docx`, audit akhir SUKSES |

## Kinerja
Demo proposal: judul 11 kata, Latar Belakang 1059 kata, abstrak 138 kata / 4 kata kunci, sitasi dua-arah 11 rujukan sinkron 100%, margin DOCX tepat 3/4/3/3 cm, partisi romawi-awal/arab-inti valid.

## Catatan
Audit scaffold baru biasanya hanya gagal di TTL-02 (judul 6 kata) — ini by-design sebelum agent menyusun judul final 8–12 kata.
