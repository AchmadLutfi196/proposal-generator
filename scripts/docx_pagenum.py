#!/usr/bin/env python3
"""docx_pagenum.py: Sinkronisasi nomor halaman aktual dari render PDF ke Daftar Isi DOCX.
Mencegah bug pencarian pada halaman Daftar Isi sendiri dan mendukung deteksi nomor
pada header (kanan-atas) maupun footer (bawah-tengah).
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROMAN = re.compile(r"^[ivxlcdm]+$", re.I)
DECIMAL = re.compile(r"^\d+$")

def page_count(pdf):
    out = subprocess.check_output(["pdfinfo", pdf], text=True, timeout=15)
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    return int(m.group(1)) if m else 0

def page_texts(pdf):
    n = page_count(pdf)
    pages = {}
    for p in range(1, n + 1):
        out = subprocess.check_output(
            ["pdftotext", "-f", str(p), "-l", str(p), "-layout", pdf, "-"],
            text=True,
            timeout=15,
        )
        lines = [l.strip() for l in out.splitlines() if l.strip()]
        pages[p] = lines
    return pages

def extract_page_number_from_lines(lines):
    if not lines:
        return ""
    # Cek footer (baris terakhir)
    last = lines[-1]
    if ROMAN.match(last) or DECIMAL.match(last):
        return last
    # Cek header (baris pertama, jika penomoran lanjutan di kanan atas)
    first = lines[0]
    # Biasanya nomor di kanan atas muncul sebagai token terakhir di baris pertama
    tokens = first.split()
    if tokens and (ROMAN.match(tokens[-1]) or DECIMAL.match(tokens[-1])):
        return tokens[-1]
    return ""

def find_toc_start(pages):
    for p, lines in sorted(pages.items()):
        for l in lines:
            if l.strip() == "DAFTAR ISI":
                return p
    return None

def first_decimal_page(pages, start):
    for p, lines in sorted(pages.items()):
        if p <= start:
            continue
        pnum = extract_page_number_from_lines(lines)
        if DECIMAL.match(pnum):
            return p
    return None

def find_page(pages, needle, start, end):
    for p in range(start, end + 1):
        text = "\n".join(pages.get(p, []))
        if needle in text:
            return p
    return None

def parse_entries(doc):
    entries = []
    par_pat = re.compile(r"<w:p>(?:(?!</w:p>).)*?</w:p>", re.S)
    for pm in par_pat.finditer(doc):
        p = pm.group(0)
        m = re.search(r'<w:hyperlink w:anchor="([^"]+)"[^>]*>.*?<w:t[^>]*>([^<]*)</w:t>', p, re.S)
        r = re.search(r"<w:instrText[^>]*>\s*PAGEREF\s+(\S+)\s+\\h\s*</w:instrText>", p)
        if m and r and m.group(1) == r.group(1):
            entries.append((p, m.group(1), m.group(2)))
    return entries

def needle_of(entry_text):
    if entry_text.startswith("BAB "):
        parts = entry_text.split(" ", 2)
        return parts[2] if len(parts) == 3 else parts[1]
    return entry_text.strip()

def render_pdf(docx):
    tmp = tempfile.mkdtemp(prefix="lo_pagenum_")
    profile = os.path.join(tmp, "profile")
    subprocess.run(
        [
            "soffice", "--headless", "--norestore",
            "-env:UserInstallation=file://" + profile,
            "--convert-to", "pdf", "--outdir", tmp, docx,
        ],
        check=True,
        capture_output=True,
        timeout=60,
    )
    base = os.path.basename(docx).rsplit(".", 1)[0] + ".pdf"
    return os.path.join(tmp, base)

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 docx_pagenum.py input.docx output.docx")
        sys.exit(1)

    src, dst = sys.argv[1], sys.argv[2]
    shutil.copy(src, dst)

    if not shutil.which("soffice") or not shutil.which("pdftotext"):
        print("[warn] docx_pagenum: soffice/pdftotext tidak ditemukan, melewati injeksi.")
        return

    with zipfile.ZipFile(src, "r") as zin:
        items = {n: zin.read(n) for n in zin.namelist()}
    doc = items["word/document.xml"].decode("utf-8")

    try:
        pdf = render_pdf(src)
    except Exception as err:
        print(f"[warn] docx_pagenum: render LibreOffice gagal ({err}).")
        return

    try:
        pages = page_texts(pdf)
    except Exception as err:
        print(f"[warn] docx_pagenum: ekstraksi teks PDF gagal ({err}).")
        return
    finally:
        shutil.rmtree(os.path.dirname(pdf), ignore_errors=True)

    toc_start = find_toc_start(pages) or 2
    first_dec = first_decimal_page(pages, toc_start) or (toc_start + 2)

    entries = parse_entries(doc)
    injected = 0
    for para, pid, text in entries:
        norm_txt = text.strip().upper()
        if norm_txt in ("ABSTRAK", "ABSTRACT", "KATA PENGANTAR", "DAFTAR TABEL", "DAFTAR GAMBAR"):
            page = find_page(pages, norm_txt, 1, first_dec - 1)
        else:
            page = find_page(pages, needle_of(text), first_dec, max(pages))

        if not page:
            continue

        val = extract_page_number_from_lines(pages[page])
        if not val:
            continue

        new_para = re.sub(
            r'(<w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t[^>]*>)[^<]*(</w:t>)',
            r"\g<1>" + val + r"\g<2>",
            para,
            count=1,
        )
        doc = doc.replace(para, new_para)
        injected += 1

    items["word/document.xml"] = doc.encode("utf-8")
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for n, content in items.items():
            zout.writestr(n, content)

    print(f"[OK] docx_pagenum: {injected} nomor halaman terisi akurat -> {dst}")

if __name__ == "__main__":
    main()
