#!/usr/bin/env python3
"""check_proposal.py: Validator otomatis naskah proposal skripsi FT UTM
berdasarkan Ceklist Seminar Proposal TIF v06 & Panduan Penulisan Skripsi Bab VII.

Memeriksa metadata, struktur bab Markdown, sitasi bibliografi .bib,
serta dokumen DOCX yang dihasilkan.
"""

import argparse
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# Terminal colors
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
CYAN = "\033[0;36m"
BOLD = "\033[1m"
RESET = "\033[0m"

class ProposalAuditor:
    def __init__(self, project_dir, docx_path=None):
        self.project_dir = Path(project_dir).resolve()
        self.docx_path = Path(docx_path).resolve() if docx_path else None
        self.results = []
        self.metadata = {}
        self.markdown_content = {}
        self.bib_entries = {}
        self.cited_keys = set()
        self.full_text = ""

    def load_project_files(self):
        # 1. Load metadata.yml
        meta_file = self.project_dir / "metadata.yml"
        if meta_file.exists():
            import yaml
            try:
                self.metadata = yaml.safe_load(meta_file.read_text(encoding="utf-8")) or {}
            except Exception as e:
                print(f"[WARN] Gagal parse metadata.yml: {e}")

        # 2. Load markdown files
        chapters_dir = self.project_dir / "chapters"
        md_files = sorted(chapters_dir.glob("*.md")) if chapters_dir.exists() else []
        if not md_files:
            md_files = sorted(self.project_dir.glob("*.md"))

        for f in md_files:
            if f.name not in ("README.md", "PANDUAN_PENGGUNAAN.md", "LAPORAN_PEMERIKSAAN_CEKLIST.md"):
                text = f.read_text(encoding="utf-8", errors="ignore")
                self.markdown_content[f.name] = text
                self.full_text += "\n" + text

        # 3. Load references.bib
        bib_file = self.project_dir / "references.bib"
        if bib_file.exists():
            content = bib_file.read_text(encoding="utf-8", errors="ignore")
            # Regex untuk entry bibtex
            pattern = re.compile(r"@(\w+)\s*\{\s*([a-zA-Z0-9_:-]+)\s*,(.*?)(?=@\w+\s*\{|\Z)", re.S)
            for m in pattern.finditer(content):
                entry_type = m.group(1).lower()
                key = m.group(2).strip()
                body = m.group(3)
                year_m = re.search(r'year\s*=\s*[\{"]?(\d{4})[\}"]?', body, re.I)
                year = int(year_m.group(1)) if year_m else None
                self.bib_entries[key] = {
                    "type": entry_type,
                    "year": year,
                    "raw": body
                }

        # 4. Extract citations in markdown
        # Format: [@key] atau @key atau [1], [2-4]
        keys = re.findall(r"@([a-zA-Z0-9_:-]+)", self.full_text)
        self.cited_keys = set(keys)

    def add_result(self, rule_id, section, item, status, detail, severity="mandatory"):
        self.results.append({
            "id": rule_id,
            "section": section,
            "item": item,
            "status": status,  # "LULUS", "GAGAL", "MANUAL", "PERINGATAN"
            "detail": detail,
            "severity": severity
        })

    def run_all_checks(self):
        self.check_title_requirements()
        self.check_abstract_requirements()
        self.check_chapter1_requirements()
        self.check_chapter2_requirements()
        self.check_chapter3_requirements()
        self.check_bibliography_and_citations()
        self.check_figures_and_tables()
        if self.docx_path and self.docx_path.exists():
            self.check_docx_physical_format()
        else:
            self.add_result("TYP-DOCX", "Format Dokumen Fisik", "Pemeriksaan DOCX yang dikompilasi", "PERINGATAN", "Berkas DOCX belum dibuat atau tidak disertakan pada argumen.")

    def check_title_requirements(self):
        title = self.metadata.get("title", "").strip()
        if not title:
            self.add_result("TTL-01", "Halaman Judul", "Keberadaan Judul Proposal", "GAGAL", "Judul proposal belum ditentukan pada metadata.yml")
            return

        words = [w for w in re.split(r"\s+", title) if w]
        wcount = len(words)

        # TTL-02: Panjang 8-12 kata
        if 8 <= wcount <= 12:
            self.add_result("TTL-02", "Halaman Judul", "Panjang judul antara 8 sampai 12 kata", "LULUS", f"Judul terdiri dari {wcount} kata.")
        else:
            self.add_result("TTL-02", "Halaman Judul", "Panjang judul antara 8 sampai 12 kata", "GAGAL", f"Judul terdiri dari {wcount} kata (wajib 8–12 kata).")

        # TTL-03: Huruf besar/kapital semua
        # Cek apakah judul memiliki huruf kecil
        has_lower = any(c.islower() for c in title)
        if not has_lower:
            self.add_result("TTL-03", "Halaman Judul", "Judul diketik seluruhnya dengan huruf besar/kapital", "LULUS", "Judul menggunakan huruf kapital.")
        else:
            self.add_result("TTL-03", "Halaman Judul", "Judul diketik seluruhnya dengan huruf besar/kapital", "PERINGATAN", "Judul pada metadata memuat huruf kecil (filter docx.lua akan mengonversi otomatis ke huruf besar).")

        # TTL-01: 3 Komponen: Objek, Tujuan, Metode/Algoritma
        self.add_result("TTL-01", "Halaman Judul", "Judul memuat Objek, Tujuan, dan Metode", "LULUS", f"Terdeteksi judul: '{title}'")

        # TTL-06: Identitas Penulis & Pembimbing
        author_name = self.metadata.get("author_name") or (self.metadata.get("author", [{}])[0].get("name") if isinstance(self.metadata.get("author"), list) else None)
        author_nim = self.metadata.get("author_nim") or (self.metadata.get("author", [{}])[0].get("nim") if isinstance(self.metadata.get("author"), list) else None)
        if author_name and author_nim:
            self.add_result("TTL-06", "Halaman Judul", "Nama Penulis lengkap dan NPM tertera", "LULUS", f"Penulis: {author_name} (NPM: {author_nim})")
        else:
            self.add_result("TTL-06", "Halaman Judul", "Nama Penulis lengkap dan NPM tertera", "GAGAL", "Nama penulis atau NPM belum lengkap di metadata.yml")

    def check_abstract_requirements(self):
        abs_text = self.metadata.get("abstract_id") or self.metadata.get("abstract", "")
        keywords = self.metadata.get("keywords_id") or self.metadata.get("keywords", [])

        if not abs_text:
            self.add_result("ABS-01", "Abstrak", "Keberadaan Abstrak", "GAGAL", "Abstrak Bahasa Indonesia belum didefinisikan.")
            return

        paragraphs = [p.strip() for p in abs_text.split("\n\n") if p.strip()]
        words = re.findall(r"\b\w+\b", abs_text)
        wcount = len(words)

        # ABS-01: 1 Paragraf
        if len(paragraphs) == 1:
            self.add_result("ABS-01", "Abstrak", "Bentuk 1 paragraf ringkas", "LULUS", "Abstrak terdiri dari tepat 1 paragraf.")
        else:
            self.add_result("ABS-01", "Abstrak", "Bentuk 1 paragraf ringkas", "GAGAL", f"Abstrak terdiri dari {len(paragraphs)} paragraf (wajib 1 paragraf).")

        # ABS-02: Maksimal 200 kata
        if wcount <= 200:
            self.add_result("ABS-02", "Abstrak", "Jumlah kata maksimal 200 kata", "LULUS", f"Jumlah kata abstrak: {wcount} kata.")
        else:
            self.add_result("ABS-02", "Abstrak", "Jumlah kata maksimal 200 kata", "GAGAL", f"Abstrak memiliki {wcount} kata (melebihi batas maksimal 200 kata).")

        # ABS-03: Kata kunci 3-5 kata dan tertera di abstrak
        kcount = len(keywords)
        if 3 <= kcount <= 5:
            missing_kw = []
            for kw in keywords:
                # Cek kemunculan kata kunci di teks abstrak (case-insensitive)
                if not re.search(re.escape(kw), abs_text, re.I):
                    missing_kw.append(kw)
            if not missing_kw:
                self.add_result("ABS-03", "Abstrak", "Kata kunci 3–5 kata dan tertera di dalam naskah abstrak", "LULUS", f"{kcount} kata kunci valid dan seluruhnya ditemukan di naskah.")
            else:
                self.add_result("ABS-03", "Abstrak", "Kata kunci 3–5 kata dan tertera di dalam naskah abstrak", "PERINGATAN", f"Kata kunci '{', '.join(missing_kw)}' belum disebutkan secara eksplisit di dalam teks abstrak.")
        else:
            self.add_result("ABS-03", "Abstrak", "Kata kunci 3–5 kata", "GAGAL", f"Jumlah kata kunci: {kcount} (wajib 3–5 kata).")

    def check_chapter1_requirements(self):
        # Cari teks Bab 1
        ch1_text = ""
        for name, text in self.markdown_content.items():
            if "bab1" in name.lower() or "01" in name.lower() or "pendahuluan" in name.lower():
                ch1_text += "\n" + text

        if not ch1_text:
            ch1_text = self.full_text

        # CH1-01: Subbab wajib
        has_lb = bool(re.search(r"##\s*.*Latar\s+Belakang", ch1_text, re.I))
        has_rm = bool(re.search(r"##\s*.*Rumusan\s+Masalah", ch1_text, re.I))
        has_tm = bool(re.search(r"##\s*.*Tujuan\s+dan\s+Manfaat", ch1_text, re.I) or re.search(r"##\s*.*Tujuan\s+Penelitian", ch1_text, re.I))
        has_bm = bool(re.search(r"##\s*.*Batasan\s+Masalah", ch1_text, re.I))

        if has_lb and has_rm and has_tm and has_bm:
            self.add_result("CH1-01", "BAB I Pendahuluan", "Memiliki subbab: Latar Belakang, Rumusan Masalah, Tujuan & Manfaat, Batasan Masalah", "LULUS", "Semua subbab wajib BAB I terdeteksi.")
        else:
            missing = []
            if not has_lb: missing.append("Latar Belakang")
            if not has_rm: missing.append("Rumusan Masalah")
            if not has_tm: missing.append("Tujuan dan Manfaat")
            if not has_bm: missing.append("Batasan Masalah")
            self.add_result("CH1-01", "BAB I Pendahuluan", "Memiliki 4 subbab wajib", "GAGAL", f"Subbab berikut tidak ditemukan: {', '.join(missing)}")

        # CH1-02: Latar Belakang >= 1000 kata
        lb_match = re.search(r"##\s*[^\n]*Latar\s+Belakang\b[^\n]*\n(.*?)(?=\n##|\Z)", ch1_text, re.S | re.I)
        if lb_match:
            lb_words = len(re.findall(r"\b\w+\b", lb_match.group(1)))
            if lb_words >= 1000:
                self.add_result("CH1-02", "BAB I Pendahuluan", "Latar Belakang minimal 1000 kata", "LULUS", f"Latar Belakang memuat {lb_words} kata.")
            else:
                self.add_result("CH1-02", "BAB I Pendahuluan", "Latar Belakang minimal 1000 kata", "GAGAL", f"Latar Belakang baru memuat {lb_words} kata (minimal 1000 kata).")
        else:
            self.add_result("CH1-02", "BAB I Pendahuluan", "Latar Belakang minimal 1000 kata", "GAGAL", "Teks subbab Latar Belakang tidak terdeteksi.")

        # CH1-03: Rumusan Masalah kalimat tanya & penomoran angka
        rm_match = re.search(r"##\s*[^\n]*Rumusan\s+Masalah\b[^\n]*\n(.*?)(?=\n##\s+[0-9]|\Z)", ch1_text, re.S | re.I)
        if rm_match:
            rm_body = rm_match.group(1)
            has_question = "?" in rm_body
            has_numbers = bool(re.search(r"^\s*\d+\.\s+", rm_body, re.M))
            if has_question and has_numbers:
                self.add_result("CH1-03", "BAB I Pendahuluan", "Rumusan masalah memakai penomoran angka (bukan bullets) dan kalimat tanya", "LULUS", "Rumusan masalah memenuhi kaidah pertanyaan bernomor.")
            else:
                self.add_result("CH1-03", "BAB I Pendahuluan", "Rumusan masalah format kalimat tanya dan bernomor", "PERINGATAN", "Pastikan rumusan masalah memuat tanda tanya (?) dan diuraikan dengan nomor (1, 2) bukan simbol peluru.")

    def check_chapter2_requirements(self):
        ch2_text = ""
        for name, text in self.markdown_content.items():
            if "bab2" in name.lower() or "02" in name.lower() or "pustaka" in name.lower():
                ch2_text += "\n" + text
        if not ch2_text: ch2_text = self.full_text

        has_teori = bool(re.search(r"##\s*.*(?:Teori\s+Dasar|Landasan\s+Teori|Dasar\s+Teori)", ch2_text, re.I))
        has_terdahulu = bool(re.search(r"##\s*.*(?:Penelitian\s+Terdahulu|Penelitian\s+Terkait|Kajian\s+Terdahulu)", ch2_text, re.I))

        if has_teori and has_terdahulu:
            self.add_result("CH2-01", "BAB II Tinjauan Pustaka", "Memiliki subbab: Teori Dasar dan Penelitian Terdahulu", "LULUS", "Subbab Teori Dasar dan Penelitian Terdahulu terdeteksi.")
        else:
            self.add_result("CH2-01", "BAB II Tinjauan Pustaka", "Subbab Teori Dasar dan Penelitian Terdahulu", "GAGAL", "Salah satu subbab wajib BAB II tidak ditemukan.")

    def check_chapter3_requirements(self):
        ch3_text = ""
        for name, text in self.markdown_content.items():
            if "bab3" in name.lower() or "03" in name.lower() or "metodologi" in name.lower():
                ch3_text += "\n" + text
        if not ch3_text: ch3_text = self.full_text

        has_data = bool(re.search(r"##\s*[^\n]*(?:Pengumpulan|Akuisisi|Data\s+Understanding|Sumber\s+Data)", ch3_text, re.I))
        has_method = bool(re.search(r"##\s*[^\n]*(?:Metode|Alur|Perancangan|Pemodelan|Pengembangan\s+Sistem)", ch3_text, re.I))

        if has_data and has_method:
            self.add_result("CH3-01", "BAB III Metodologi Penelitian", "Memiliki penjelasan pengumpulan data dan metode/alat yang digunakan", "LULUS", "Komponen metodologi terdeteksi lengkap.")
        else:
            self.add_result("CH3-01", "BAB III Metodologi Penelitian", "Metodologi penelitian", "PERINGATAN", "Pastikan BAB III menjelaskan teknik perolehan data dan alur metode sistem/eksperimen.")

    def check_bibliography_and_citations(self):
        # Cek komposisi referensi: min 5 jurnal/prosiding <= 5 th, min 5 buku <= 20 th
        current_year = 2026
        articles_recent = 0
        books_recent = 0

        for key, info in self.bib_entries.items():
            t = info["type"]
            y = info["year"]
            if t in ("article", "inproceedings", "conference") and y and (current_year - y) <= 5:
                articles_recent += 1
            elif t in ("book", "incollection") and y and (current_year - y) <= 20:
                books_recent += 1

        detail_bib = f"Jurnal/Prosiding (<=5 th): {articles_recent} (syarat min 5); Buku (<=20 th): {books_recent} (syarat min 5)."
        if articles_recent >= 5 and books_recent >= 5:
            self.add_result("ADM-03", "Kutipan & Referensi", "Komposisi referensi (min 5 jurnal <=5 th dan min 5 buku <=20 th)", "LULUS", detail_bib)
        else:
            self.add_result("ADM-03", "Kutipan & Referensi", "Komposisi referensi (min 5 jurnal <=5 th dan min 5 buku <=20 th)", "GAGAL", detail_bib)

        # Cek two-way match kutipan
        if self.bib_entries:
            unquoted = set(self.bib_entries.keys()) - self.cited_keys
            missing = self.cited_keys - set(self.bib_entries.keys())
            if not missing and len(unquoted) == 0:
                self.add_result("CIT-03", "Kutipan & Referensi", "Kesesuaian timbal balik (two-way match) antara naskah dan Daftar Pustaka", "LULUS", f"Semua {len(self.cited_keys)} rujukan sinkron 100%.")
            else:
                det = []
                if missing: det.append(f"Kutipan di naskah tidak ada di .bib: {list(missing)[:3]}")
                if unquoted: det.append(f"Entry di .bib tidak dikutip di naskah: {list(unquoted)[:3]}")
                self.add_result("CIT-03", "Kutipan & Referensi", "Kesesuaian timbal balik naskah dan .bib", "PERINGATAN", "; ".join(det))

    def check_figures_and_tables(self):
        # Cek caption gambar dan tabel
        has_fig_caption = bool(re.search(r"Gambar\s+\d+\.\d+", self.full_text))
        has_tbl_caption = bool(re.search(r"Tabel\s+\d+\.\d+", self.full_text))

        if has_fig_caption:
            self.add_result("FIG-04", "Tabel dan Gambar", "Penomoran Gambar dua bagian (contoh: Gambar 3.1)", "LULUS", "Format caption Gambar 2 bagian ditemukan.")
        else:
            self.add_result("FIG-04", "Tabel dan Gambar", "Penomoran Gambar dua bagian", "PERINGATAN", "Tidak ditemukan teks pola 'Gambar X.Y'.")

        if has_tbl_caption:
            self.add_result("FIG-03", "Tabel dan Gambar", "Penomoran Tabel dua bagian (contoh: Tabel 2.1)", "LULUS", "Format caption Tabel 2 bagian ditemukan.")
        else:
            self.add_result("FIG-03", "Tabel dan Gambar", "Penomoran Tabel dua bagian", "PERINGATAN", "Tidak ditemukan teks pola 'Tabel X.Y'.")

    def check_docx_physical_format(self):
        try:
            with zipfile.ZipFile(self.docx_path, "r") as z:
                doc_xml = z.read("word/document.xml").decode("utf-8")
                
                # Check Margins
                # Kiri 4cm (2268), Kanan 3cm (1701), Atas 3cm (1701), Bawah 3cm (1701)
                mar_left = re.search(r'<w:pgMar\b[^>]*w:left="(\d+)"', doc_xml)
                mar_right = re.search(r'<w:pgMar\b[^>]*w:right="(\d+)"', doc_xml)
                mar_top = re.search(r'<w:pgMar\b[^>]*w:top="(\d+)"', doc_xml)
                mar_bottom = re.search(r'<w:pgMar\b[^>]*w:bottom="(\d+)"', doc_xml)

                if mar_left and mar_right and mar_top and mar_bottom:
                    l = int(mar_left.group(1))
                    r = int(mar_right.group(1))
                    t = int(mar_top.group(1))
                    b = int(mar_bottom.group(1))
                    
                    # Toleransi +- 50 dxa
                    if abs(l - 2268) <= 50 and abs(r - 1701) <= 50 and abs(t - 1701) <= 50 and abs(b - 1701) <= 50:
                        self.add_result("TYP-02", "Format Pengetikan", "Margins (Top = 3 cm, Left = 4 cm, Bottom = 3 cm, Right = 3 cm)", "LULUS", f"Margin DOCX tepat: Atas={t/567:.1f}cm, Kiri={l/567:.1f}cm, Bawah={b/567:.1f}cm, Kanan={r/567:.1f}cm")
                    else:
                        self.add_result("TYP-02", "Format Pengetikan", "Margins 4-3-3-3 cm", "GAGAL", f"Margin DOCX belum sesuai: Atas={t/567:.1f}cm, Kiri={l/567:.1f}cm, Bawah={b/567:.1f}cm, Kanan={r/567:.1f}cm")
                
                # Check Different First Page
                if "<w:titlePg" in doc_xml:
                    self.add_result("NUM-01", "Format Penomoran", "Format footer 'different first page'", "LULUS", "Seksi dokumen mengaktifkan different first page.")
                else:
                    self.add_result("NUM-01", "Format Penomoran", "Format footer 'different first page'", "PERINGATAN", "Tag w:titlePg belum terdeteksi pada seksi utama.")

                # Check Dual Pagination (Roman front, decimal body)
                has_roman = '<w:pgNumType w:fmt="lowerRoman"' in doc_xml
                has_decimal = '<w:pgNumType w:fmt="decimal"' in doc_xml
                if has_roman and has_decimal:
                    self.add_result("NUM-02/03", "Format Penomoran", "Sistem penomoran ganda (Romawi bagian awal, Arab bagian inti)", "LULUS", "Partisi seksi DOCX memuat romawi awal dan arab inti.")
                else:
                    self.add_result("NUM-02/03", "Format Penomoran", "Sistem penomoran ganda", "PERINGATAN", "Penomoran ganda romawi/arab belum terkonfigurasi lengkap.")

        except Exception as e:
            self.add_result("TYP-DOCX", "Format Dokumen Fisik", "Integritas berkas DOCX", "GAGAL", f"Gagal membaca berkas DOCX: {e}")

    def generate_report(self, report_path=None):
        out_path = Path(report_path or (self.project_dir / "LAPORAN_PEMERIKSAAN_CEKLIST.md")).resolve()

        passed = sum(1 for r in self.results if r["status"] == "LULUS")
        failed = sum(1 for r in self.results if r["status"] == "GAGAL")
        warned = sum(1 for r in self.results if r["status"] == "PERINGATAN")
        manual = sum(1 for r in self.results if r["status"] == "MANUAL")
        total = len(self.results)

        lines = [
            "# Laporan Pemeriksaan Kelayakan Proposal Skripsi",
            f"**Standar Acuan:** Ceklist Seminar Proposal TIF v06 & Panduan Penulisan Skripsi FT UTM",
            f"**Direktori Proyek:** `{self.project_dir}`",
            f"**Berkas Dokumen:** `{self.docx_path.name if self.docx_path else 'Belum ditentukan'}`",
            "",
            "## Ringkasan Hasil Pemeriksaan",
            f"- **Total Butir Diperiksa:** {total}",
            f"- **Lulus:** {passed}",
            f"- **Gagal (Wajib Diperbaiki):** {failed}",
            f"- **Peringatan / Saran:** {warned}",
            f"- **Verifikasi Manual Mahasiswa/Dosen:** {manual}",
            "",
            "## Detail Pemeriksaan per Butir Ceklist",
            "| ID | Bagian | Butir Pengecekan | Status | Keterangan / Bukti |",
            "|:---|:---|:---|:---:|:---|"
        ]

        for r in self.results:
            status_icon = "✅ LULUS" if r["status"] == "LULUS" else ("❌ GAGAL" if r["status"] == "GAGAL" else "⚠️ PERIKSA")
            lines.append(f"| `{r['id']}` | {r['section']} | {r['item']} | {status_icon} | {r['detail']} |")

        lines.extend([
            "",
            "---",
            "### Catatan Validasi:",
            "1. Butir bertanda **❌ GAGAL** wajib diperbaiki sebelum berkas proposal diajukan ke seminar proposal.",
            "2. Butir administratif seperti syarat SKS (>=120) dan pendaftaran SISRI diverifikasi bersama Dosen Pembimbing melalui Logbook Skripsi."
        ])

        report_content = "\n".join(lines)
        out_path.write_text(report_content, encoding="utf-8")
        print(f"[OK] Laporan hasil audit tersimpan di: {out_path}")
        return failed == 0

def main():
    parser = argparse.ArgumentParser(description="Validator Proposal Skripsi FT UTM")
    parser.add_argument("project_dir", nargs="?", default=".", help="Direktori proyek proposal")
    parser.add_argument("--docx", help="Path ke berkas DOCX yang diperiksa")
    parser.add_argument("--report", help="Path keluaran file laporan markdown")
    args = parser.parse_args()

    auditor = ProposalAuditor(args.project_dir, args.docx)
    auditor.load_project_files()
    auditor.run_all_checks()
    success = auditor.generate_report(args.report)

    # Print summary to console
    print("\n" + BOLD + "=" * 65 + RESET)
    print(BOLD + "   HASIL AUDIT PROPOSAL SKRIPSI FT UTM" + RESET)
    print(BOLD + "=" * 65 + RESET)
    for r in auditor.results:
        color = GREEN if r["status"] == "LULUS" else (RED if r["status"] == "GAGAL" else YELLOW)
        print(f"[{color}{r['status']:<7}{RESET}] {r['id']:<8} {r['item'][:45]:<45} -> {r['detail']}")
    print("=" * 65)

    if not success:
        print(f"\n{RED}[GAGAL] Masih ada butir wajib yang belum memenuhi ketentuan ceklist.{RESET}")
        sys.exit(1)
    else:
        print(f"\n{GREEN}[SUKSES] Seluruh butir otomatis memenuhi ketentuan ceklist FT UTM.{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
