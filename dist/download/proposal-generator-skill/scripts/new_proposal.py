#!/usr/bin/env python3
"""new_proposal.py — Scaffold proposal baru dari satu kata kunci topik.

Mahasiswa cukup menjalankan:
    python3 scripts/new_proposal.py "Sistem Informasi Peminjaman Laboratorium Berbasis Web"

Lalu agent (Codex / Opencode / Orca / Cursor / ChatGPT Work / dll.) membaca
`topik.yml` + `agent/AGENT_PROMPT.md` dan mengisi isi bab sampai lulus audit.

Sumber otoritas format: presets/utm-proposal.yml + checklists/ft-utm-tif-v06.yml
"""
import argparse
import re
import shutil
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKELETONS = {
    "A": ROOT / "skeletons/Opsi-A-TPL",
    "B": ROOT / "skeletons/Opsi-B-Kecerdasan-Komputasi",
}

# --- Heuristik pemilihan opsi dari topik bebas ---
KEYWORDS_B = [
    "ai", "artificial intelligence", "machine learning", "deep learning",
    "nlp", "computer vision", "vision", "data mining", "data science",
    "neural", "bert", "cnn", "lstm", "gan", "transformer", "llm",
    "klasifikasi", "prediksi", "deteksi", "segmentasi", "rekomendasi",
    "chatbot", "sentimen", "sentiment", "ekstraksi", "ringkasan",
    "kecerdasan komputasi", "soft computing", "fuzzy", "genetika",
    "image", "citra", "teks", "bahasa alami", "indobert",
]
KEYWORDS_A = [
    "sistem informasi", "website", "web", "aplikasi", "mobile", "android",
    "iot", "embedded", "basis data", "database", "erp", "crm",
    "rekayasa perangkat lunak", "perangkat lunak", "api", "rest",
    "manajemen", "administrasi", "e-commerce", "ecommerce",
]

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:60].strip("-") or "proposal"

def infer_opsi(topik: str) -> tuple[str, str]:
    t = f" {topik.lower()} "
    score_b = sum(1 for k in KEYWORDS_B if f" {k} " in t or k in t)
    score_a = sum(1 for k in KEYWORDS_A if f" {k} " in t or k in t)
    if score_b > score_a and score_b > 0:
        return "B", f"heuristic: skor B={score_b} > A={score_a}"
    if score_a > 0:
        return "A", f"heuristic: skor A={score_a} >= B={score_b}"
    return "B", "default B (Kecerdasan Komputasi) — tidak ada keyword A/B terdeteksi; ganti dengan --opsi A bila perlu"

def patch_metadata(meta_path: Path, args) -> None:
    if not meta_path.exists():
        return
    try:
        import yaml
    except ImportError:
        print("[WARN] pyyaml tidak tersedia; metadata.yml disalin apa adanya.")
        return
    data = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
    if args.topik:
        data["title"] = args.topik.upper()
    if args.nama:
        data["author_name"] = args.nama.upper()
    if args.nim:
        data["author_nim"] = args.nim
    if args.dosen1:
        data["advisor_1_name"] = args.dosen1
    if args.dosen2:
        data["advisor_2_name"] = args.dosen2
    if args.tahun:
        data["year"] = str(args.tahun)
    meta_path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")

def main():
    p = argparse.ArgumentParser(description="Scaffold proposal FT UTM dari topik bebas.")
    p.add_argument("topik", help="Judul/topik bebas, mis. 'Sistem Klasifikasi Citra Daun Kopi dengan CNN'")
    p.add_argument("--dir", "-d", help="Nama folder proyek tujuan (default: slug dari topik)")
    p.add_argument("--opsi", choices=["auto", "A", "B"], default="auto")
    p.add_argument("--nama", help="Nama lengkap mahasiswa")
    p.add_argument("--nim", help="NIM")
    p.add_argument("--dosen1", help="Nama dosen pembimbing 1")
    p.add_argument("--dosen2", help="Nama dosen pembimbing 2")
    p.add_argument("--tahun", default="2026")
    p.add_argument("--dry-run", action="store_true", help="Tampilkan rencana tanpa menulis file")
    args = p.parse_args()

    if args.opsi == "auto" or not args.opsi:
        opsi, alasan = infer_opsi(args.topik)
    else:
        opsi, alasan = args.opsi.upper(), "manual (--opsi)"
    skeleton = SKELETONS[opsi]
    if not skeleton.exists():
        print(f"[ERROR] Skeleton tidak ditemukan: {skeleton}"); sys.exit(1)

    dest = Path(args.dir) if args.dir else Path(slugify(args.topik))
    if dest.is_absolute():
        dest = dest
    else:
        dest = (Path.cwd() / dest) if not dest.parent.is_absolute() else dest

    print(f"[INFO] Topik      : {args.topik}")
    print(f"[INFO] Opsi       : {opsi} ({alasan})")
    print(f"[INFO] Skeleton   : {skeleton.relative_to(ROOT)}")
    print(f"[INFO] Tujuan     : {dest}")

    if args.dry_run:
        print("[DRY-RUN] Tidak ada file ditulis."); return

    if dest.exists():
        print(f"[WARN] Folder sudah ada: {dest} — scaffold dilewati agar tidak menimpa isi."); sys.exit(0)

    shutil.copytree(skeleton, dest)
    (dest / "output").mkdir(parents=True, exist_ok=True)

    patch_metadata(dest / "metadata.yml", args)

    # topik.yml = satu-satunya input yang perlu diisi mahasiswa/agent
    topik_yml = dest / "topik.yml"
    topik_yml.write_text(f"""\
# topik.yml — SATU-SATUNYA berkas yang perlu diisi dari topik bebas.
# Agent: baca berkas ini, lalu isi metadata.yml + chapters/*.md + references.bib
# sampai `python3 ../scripts/check_proposal.py . --docx output/Proposal_Skripsi.docx` LULUS.
topik: "{args.topik}"
opsi: "{opsi}"   # A=TPL (sistem/web/iot) | B=Kecerdasan Komputasi (AI/NLP/CV/Data)
alasan_opsi: "{alasan}"
nama: "{args.nama or 'TODO: Nama Lengkap Mahasiswa'}"
nim: "{args.nim or 'TODO: NIM'}"
dosen_pembimbing_1: "{args.dosen1 or 'TODO: Nama Dosen Pembimbing I, Gelar'}"
dosen_pembimbing_2: "{args.dosen2 or 'TODO: Nama Dosen Pembimbing II, Gelar'}"
tahun: {args.tahun}
judul_usulan: ""   # 8-12 kata kapital, bentuk V-shape di cover — isi setelah agent menyusun judul final
metode_usulan: ""  # mis. Waterfall vs CNN/Transformer — disimpulkan agent dari topik
""", encoding="utf-8")

    (dest / "PETUNJUK_AGENT.md").write_text(
        f"""# PETUNJUK_AGENT — Proposal: {args.topik}\n\n"""
        "Baca `agent/AGENT_PROMPT.md` di akar repo proposal-generator, lalu:\n\n"
        "1. Baca `topik.yml` (topik + identitas).\n"
        "2. Susun judul final 8-12 kata kapital, tulis ke `metadata.yml` + `judul_usulan` di `topik.yml`.\n"
        "3. Isi `chapters/01-pendahuluan.md`, `02-tinjauan-pustaka.md`, `03-metodologi.md` sesuai skeleton Opsi "
        f"{opsi}.\n"
        "4. Tambahkan referensi nyata (>=5 jurnal/prosiding <=5 th, >=5 textbook <=20 th) di `references.bib`, "
        "sitasi dengan `[@citekey]`.\n"
        "5. Abstrak ID+EN <=200 kata + kata kunci (lihat `examples/demo-proposal/metadata.yml`).\n"
        "6. Jangan ubah format (.docx) — hanya isi konten.\n"
        "7. Jalankan: `python3 ../scripts/build_proposal.py .` lalu "
        "`python3 ../scripts/check_proposal.py . --docx output/Proposal_Skripsi.docx`\n"
        "8. Perbaiki sampai tidak ada FAIL pada ceklist otomatis; manual items (ADM-*) biarkan apa adanya.\n"
        "\nAturan otoritas: `presets/utm-proposal.yml` + `checklists/ft-utm-tif-v06.yml`.\n",
        encoding="utf-8",
    )

    print(f"\n[OK] Scaffold selesai di: {dest}")
    print("Langkah berikut untuk agent yang menjalankannya:")
    print(f"  cd {dest}")
    print("  # isi topik.yml / metadata.yml, chapters/*.md, references.bib")
    print("  python3 ../scripts/build_proposal.py .")

if __name__ == "__main__":
    main()
