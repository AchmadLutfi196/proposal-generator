#!/usr/bin/env python3
"""finalize_docx.py: Menyesuaikan partisi seksi dan sistem penomoran halaman DOCX:
  - Cover            : Tanpa nomor halaman (hapus footerReference)
  - Bagian Awal      : Angka Romawi kecil (i, ii, iii...) di bawah-tengah
  - Bagian Inti      : Angka Arab (1, 2, 3...)
                       - Awal bab (first page) : Bawah-tengah
                       - Lanjutan bab          : Kanan-atas (header)
  - Tab Stop TOC     : Rata kanan sesuai batas margin (7937 DXA untuk 4-3-3-3 cm)
"""

import re
import sys
import zipfile
from pathlib import Path

SECT_IN_PPR = re.compile(r"<w:pPr><w:sectPr>(.*?)</w:sectPr></w:pPr>", re.S)
FOOTER_REF = re.compile(r"<w:footerReference[^/]*/>")
HEADER_REF = re.compile(r"<w:headerReference[^/]*/>")

def next_heading_text(doc, start):
    nxt = doc[start:]
    m = re.search(r'<w:pStyle w:val="Heading1"[^>]*/>', nxt)
    if not m:
        return ""
    hdr = nxt[m.end():]
    t = re.search(r"<w:t[^>]*>([^<]*)", hdr)
    return t.group(1) if t else ""

def is_front_matter_heading(t):
    norm = t.strip().upper()
    return norm in (
        "KATA PENGANTAR", "PRAKATA", "ABSTRAK", "ABSTRACT",
        "DAFTAR ISI", "DAFTAR TABEL", "DAFTAR GAMBAR", "DAFTAR LAMPIRAN", "DAFTAR SINGKATAN"
    )

def is_chapter_1(t):
    norm = t.strip().upper()
    return bool(re.match(r"^BAB\s+(?:I|1|01)\b", norm) or norm.startswith("PENDAHULUAN"))

def is_chapter_2_plus(t):
    norm = t.strip().upper()
    return bool(re.match(r"^BAB\s+(?:II|III|IV|V|2|3|4|5)\b", norm) or
                any(norm.startswith(k) for k in ("KAJIAN PUSTAKA", "TINJAUAN PUSTAKA", "METODOLOGI")))

def classify(text):
    t = text.strip()
    if is_front_matter_heading(t):
        return "cover"
    if is_chapter_1(t):
        return "roman"
    if is_chapter_2_plus(t):
        return "decimal-start"
    return "body"

def add_pgnum(sect, fmt, start=None):
    if "<w:pgNumType" in sect:
        return sect
    start_attr = f' w:start="{start}"' if start is not None else ""
    tag = f'<w:pgNumType w:fmt="{fmt}"{start_attr}/>'
    return sect + tag

def process_document_xml(doc):
    matches = list(SECT_IN_PPR.finditer(doc))
    if not matches:
        return doc, 0

    out = []
    last = 0
    changed = 0

    for m in matches:
        out.append(doc[last:m.start()])
        sect = m.group(1)
        next_hdr = next_heading_text(doc, m.end())
        kind = classify(next_hdr)

        if kind == "cover":
            # Hapus footer & header pada cover
            sect = FOOTER_REF.sub("", sect)
            sect = HEADER_REF.sub("", sect)
            changed += 1
        elif kind == "roman":
            # Bagian awal: romawi kecil mulai i
            sect = add_pgnum(sect, "lowerRoman", "1")
            changed += 1
        elif kind == "decimal-start":
            # BAB I: arab mulai 1, aktifkan different first page
            sect = add_pgnum(sect, "decimal", "1")
            if "<w:titlePg" not in sect:
                sect = sect + "<w:titlePg/>"
            changed += 1

        out.append(f"<w:pPr><w:sectPr>{sect}</w:sectPr></w:pPr>")
        last = m.end()

    out.append(doc[last:])
    return "".join(out), changed

def get_tab_pos(doc):
    # A4 (11906) - Left (2268) - Right (1701) = 7937
    sz = re.search(r'<w:pgSz\b[^>]*w:w="(\d+)"', doc)
    mar_left = re.search(r'<w:pgMar\b[^>]*w:left="(\d+)"', doc)
    mar_right = re.search(r'<w:pgMar\b[^>]*w:right="(\d+)"', doc)
    if sz and mar_left and mar_right:
        try:
            return int(sz.group(1)) - int(mar_left.group(1)) - int(mar_right.group(1))
        except Exception:
            pass
    return 7937

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 finalize_docx.py input.docx output.docx")
        sys.exit(1)

    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    
    with zipfile.ZipFile(src, "r") as zin:
        items = {n: zin.read(n) for n in zin.namelist()}

    doc = items["word/document.xml"].decode("utf-8")
    tab_pos = get_tab_pos(doc)

    # Sesuaikan posisi tab dot leader pada daftar isi
    doc = re.sub(
        r'(<w:pStyle w:val="TOC[123]"/>.*?<w:tab w:val="right" w:leader="dot" w:pos=)"\d+"',
        rf'\g<1>"{tab_pos}"',
        doc,
    )

    new_doc, changed = process_document_xml(doc)
    items["word/document.xml"] = new_doc.encode("utf-8")

    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for n, content in items.items():
            zout.writestr(n, content)

    print(f"[OK] finalize_docx: {changed} seksi disesuaikan (tab={tab_pos}) -> {dst}")

if __name__ == "__main__":
    main()
