#!/usr/bin/env python3
"""build_proposal.py: Orkestrator otomatis kompilasi proposal skripsi FT UTM.
Alur Eksekusi:
  1. Parsing metadata dan chapters Markdown
  2. Kompilasi Pandoc + docx.lua + apa-numeric.csl + reference.docx
  3. Partisi seksi dokumen via finalize_docx.py (Romawi awal, Arab inti)
  4. Sinkronisasi nomor halaman TOC riil via docx_pagenum.py
  5. Audit otomatis kepatuhan terhadap ceklist via check_proposal.py
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def build_proposal(project_dir, output_path=None, run_check=True):
    project_dir = Path(project_dir).resolve()
    if not project_dir.exists():
        print(f"[ERROR] Direktori proyek tidak ditemukan: {project_dir}")
        sys.exit(1)

    print(f"\n[INFO] Memulai kompilasi proposal dari: {project_dir}")
    
    # Deteksi berkas input
    meta_file = project_dir / "metadata.yml"
    bib_file = project_dir / "references.bib"
    chapters_dir = project_dir / "chapters"
    
    md_files = sorted(chapters_dir.glob("*.md")) if chapters_dir.exists() else []
    if not md_files:
        md_files = sorted([f for f in project_dir.glob("*.md") if f.name not in ("README.md", "LAPORAN_PEMERIKSAAN_CEKLIST.md")])

    if not md_files:
        print("[ERROR] Tidak ada berkas bab Markdown (*.md) ditemukan.")
        sys.exit(1)

    # Deteksi template & filter
    templates_dir = ROOT_DIR / "templates"
    ref_docx = templates_dir / "reference.docx"
    lua_filter = templates_dir / "docx.lua"
    csl_file = templates_dir / "apa-numeric.csl"

    if not ref_docx.exists():
        print("[INFO] Membangun reference.docx berstandar FT UTM...")
        make_ref_script = ROOT_DIR / "scripts" / "make_reference_docx.py"
        subprocess.run([sys.executable, str(make_ref_script), str(ref_docx)], check=True)

    # Buat direktori output
    out_dir = project_dir / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    final_docx = Path(output_path) if output_path else (out_dir / "Proposal_Skripsi.docx")

    tmp_dir = Path(tempfile.mkdtemp(prefix="build_prop_"))
    try:
        # Salin aset gambar jika ada
        gambar_dir = project_dir / "gambar"
        if gambar_dir.exists():
            shutil.copytree(gambar_dir, tmp_dir / "gambar", dirs_exist_ok=True)

        # Salin logo jika ada
        logo_path = project_dir / "logo.jpg"
        if not logo_path.exists():
            logo_path = templates_dir / "logo.jpg"
        if logo_path.exists():
            shutil.copy(logo_path, tmp_dir / "logo.jpg")

        # Tahap 1: Pandoc
        tmp_pandoc = tmp_dir / "tmp_pandoc.docx"
        pandoc_cmd = [
            "pandoc",
            *[str(f) for f in md_files],
            f"--metadata-file={meta_file}" if meta_file.exists() else "",
            f"--reference-doc={ref_docx}",
            f"--lua-filter={lua_filter}",
            f"--csl={csl_file}" if csl_file.exists() else "",
            f"--bibliography={bib_file}" if bib_file.exists() else "",
            "--citeproc",
            "--top-level-division=chapter",
            "-o", str(tmp_pandoc)
        ]
        pandoc_cmd = [c for c in pandoc_cmd if c]

        print("[1/4] Menjalankan Pandoc dengan filter docx.lua & citeproc...")
        res = subprocess.run(pandoc_cmd, cwd=tmp_dir, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[ERROR] Pandoc gagal: {res.stderr}")
            sys.exit(1)

        # Tahap 2: Finalisasi seksi (finalize_docx.py)
        tmp_sect = tmp_dir / "tmp_sect.docx"
        print("[2/4] Menyesuaikan partisi seksi dan penomoran halaman...")
        finalize_script = ROOT_DIR / "scripts" / "finalize_docx.py"
        subprocess.run([sys.executable, str(finalize_script), str(tmp_pandoc), str(tmp_sect)], check=True)

        # Tahap 3: Sinkronisasi nomor halaman riil (docx_pagenum.py)
        print("[3/4] Melakukan sinkronisasi nomor halaman TOC ke PDF...")
        pagenum_script = ROOT_DIR / "scripts" / "docx_pagenum.py"
        subprocess.run([sys.executable, str(pagenum_script), str(tmp_sect), str(final_docx)], check=True)

        print(f"\n[OK] Dokumen proposal berhasil dibuat di: {final_docx}")

        # Tahap 4: Audit Ceklist
        if run_check:
            print("\n[4/4] Memeriksa kepatuhan terhadap ceklist...")
            check_script = ROOT_DIR / "scripts" / "check_proposal.py"
            subprocess.run([sys.executable, str(check_script), str(project_dir), "--docx", str(final_docx)], check=False)

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

def main():
    parser = argparse.ArgumentParser(description="Compiler Proposal Skripsi FT UTM")
    parser.add_argument("project_dir", nargs="?", default=".", help="Direktori naskah proposal")
    parser.add_argument("--output", "-o", help="Jalur berkas keluaran DOCX")
    parser.add_argument("--no-check", action="store_true", help="Lewati pemeriksaan ceklist otomatis")
    args = parser.parse_args()

    build_proposal(args.project_dir, args.output, run_check=not args.no_check)

if __name__ == "__main__":
    main()
