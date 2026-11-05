#!/usr/bin/env python3
"""make_reference_docx.py: Menghasilkan reference.docx berstandar resmi FT UTM
dengan margin 4-3-3-3 cm, Times New Roman 12pt, spasi 1.5, dan seluruh custom styles.
"""

import os
import sys
import zipfile
import subprocess
import tempfile
from pathlib import Path

def build_reference_docx(out_path):
    out_path = Path(out_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 1. Bangun basis dari pandoc default jika belum ada
    tmp_dir = tempfile.mkdtemp(prefix="make_ref_")
    tmp_base = os.path.join(tmp_dir, "base.docx")
    subprocess.run(["pandoc", "-o", tmp_base, "--print-default-data-file", "reference.docx"], check=True)
    
    with zipfile.ZipFile(tmp_base, "r") as zin:
        items = {n: zin.read(n) for n in zin.namelist()}
        
    # Margin FT UTM: Kiri 4cm (2268), Kanan 3cm (1701), Atas 3cm (1701), Bawah 3cm (1701)
    pg_mar_utm = '<w:pgMar w:top="1701" w:right="1701" w:bottom="1701" w:left="2268" w:header="720" w:footer="720" w:gutter="0"/>'
    pg_sz_a4 = '<w:pgSz w:w="11906" w:h="16838"/>'
    
    # 2. Update document.xml
    doc_xml = items["word/document.xml"].decode("utf-8")
    import re
    if "<w:pgMar" in doc_xml:
        doc_xml = re.sub(r'<w:pgMar\b[^>]*/>', pg_mar_utm, doc_xml)
    else:
        doc_xml = doc_xml.replace("</w:sectPr>", f"{pg_sz_a4}{pg_mar_utm}</w:sectPr>")
    if "<w:pgSz" in doc_xml:
        doc_xml = re.sub(r'<w:pgSz\b[^>]*/>', pg_sz_a4, doc_xml)
    items["word/document.xml"] = doc_xml.encode("utf-8")
    
    # 3. Update styles.xml
    styles_xml = items["word/styles.xml"].decode("utf-8")
    
    # Ganti docDefaults font menjadi Times New Roman 12pt
    tnr_rpr = (
        '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman"/>'
        '<w:sz w:val="24"/><w:szCs w:val="24"/>'
    )
    styles_xml = re.sub(
        r'<w:docDefaults>.*?<w:rPrDefault><w:rPr>.*?</w:rPr></w:rPrDefault>',
        f'<w:docDefaults><w:rPrDefault><w:rPr>{tnr_rpr}</w:rPr></w:rPrDefault>',
        styles_xml,
        flags=re.S
    )
    
    # Custom styles definition
    custom_styles = """
    <!-- Normal Paragraf 1.5 spasi -->
    <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
      <w:name w:val="Normal"/>
      <w:qFormat/>
      <w:pPr>
        <w:spacing w:line="360" w:lineRule="auto" w:before="0" w:after="0"/>
        <w:jc w:val="both"/>
      </w:pPr>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:color w:val="000000"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
      </w:rPr>
    </w:style>

    <!-- Heading 1 (BAB I PENDAHULUAN) 14pt Bold Center -->
    <w:style w:type="paragraph" w:styleId="Heading1">
      <w:name w:val="heading 1"/>
      <w:basedOn w:val="Normal"/>
      <w:next w:val="Normal"/>
      <w:qFormat/>
      <w:pPr>
        <w:spacing w:before="0" w:after="240" w:line="360" w:lineRule="auto"/>
        <w:jc w:val="center"/>
        <w:outlineLvl w:val="0"/>
      </w:pPr>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:b/>
        <w:bCs/>
        <w:sz w:val="28"/>
        <w:szCs w:val="28"/>
      </w:rPr>
    </w:style>

    <!-- Heading 2 (1.1 Latar Belakang) 12pt Bold Left -->
    <w:style w:type="paragraph" w:styleId="Heading2">
      <w:name w:val="heading 2"/>
      <w:basedOn w:val="Normal"/>
      <w:next w:val="Normal"/>
      <w:qFormat/>
      <w:pPr>
        <w:spacing w:before="240" w:after="120" w:line="360" w:lineRule="auto"/>
        <w:jc w:val="left"/>
        <w:outlineLvl w:val="1"/>
      </w:pPr>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:b/>
        <w:bCs/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
      </w:rPr>
    </w:style>

    <!-- Heading 3 (1.1.1 Subsubbab) 12pt Bold Left -->
    <w:style w:type="paragraph" w:styleId="Heading3">
      <w:name w:val="heading 3"/>
      <w:basedOn w:val="Normal"/>
      <w:next w:val="Normal"/>
      <w:qFormat/>
      <w:pPr>
        <w:spacing w:before="120" w:after="60" w:line="360" w:lineRule="auto"/>
        <w:jc w:val="left"/>
        <w:outlineLvl w:val="2"/>
      </w:pPr>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:b/>
        <w:bCs/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
      </w:rPr>
    </w:style>

    <!-- Chapter Label -->
    <w:style w:type="paragraph" w:customStyle="1" w:styleId="ChapterLabel">
      <w:name w:val="Chapter Label"/>
      <w:basedOn w:val="Normal"/>
      <w:pPr>
        <w:spacing w:before="0" w:after="120" w:line="360" w:lineRule="auto"/>
        <w:jc w:val="center"/>
      </w:pPr>
      <w:rPr>
        <w:b/><w:bCs/><w:sz w:val="28"/><w:szCs w:val="28"/>
      </w:rPr>
    </w:style>

    <!-- Caption Gambar (di bawah gambar, spasi 1.0, center, TNR 12pt) -->
    <w:style w:type="paragraph" w:customStyle="1" w:styleId="CaptionFigure">
      <w:name w:val="CaptionFigure"/>
      <w:basedOn w:val="Normal"/>
      <w:pPr>
        <w:spacing w:before="120" w:after="120" w:line="240" w:lineRule="auto"/>
        <w:jc w:val="center"/>
      </w:pPr>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
        <w:sz w:val="24"/><w:szCs w:val="24"/>
      </w:rPr>
    </w:style>

    <!-- Caption Tabel (di atas tabel, spasi 1.0, center, TNR 12pt) -->
    <w:style w:type="paragraph" w:customStyle="1" w:styleId="CaptionTable">
      <w:name w:val="CaptionTable"/>
      <w:basedOn w:val="Normal"/>
      <w:pPr>
        <w:spacing w:before="120" w:after="120" w:line="240" w:lineRule="auto"/>
        <w:jc w:val="center"/>
      </w:pPr>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
        <w:sz w:val="24"/><w:szCs w:val="24"/>
      </w:rPr>
    </w:style>

    <!-- Baris Sumber Gambar/Tabel -->
    <w:style w:type="paragraph" w:customStyle="1" w:styleId="Source">
      <w:name w:val="Source"/>
      <w:basedOn w:val="Normal"/>
      <w:pPr>
        <w:spacing w:before="60" w:after="120" w:line="240" w:lineRule="auto"/>
        <w:jc w:val="center"/>
      </w:pPr>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
        <w:sz w:val="24"/><w:szCs w:val="24"/>
      </w:rPr>
    </w:style>

    <!-- Paragraf Abstrak (spasi 1.0, rata kiri-kanan, indent 1.25cm) -->
    <w:style w:type="paragraph" w:customStyle="1" w:styleId="AbstractBody">
      <w:name w:val="Abstract Body"/>
      <w:basedOn w:val="Normal"/>
      <w:pPr>
        <w:spacing w:line="240" w:lineRule="auto" w:before="0" w:after="120"/>
        <w:ind w:firstLine="720"/>
        <w:jc w:val="both"/>
      </w:pPr>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
        <w:sz w:val="24"/><w:szCs w:val="24"/>
      </w:rPr>
    </w:style>

    <!-- Daftar Pustaka (hanging indent 0.5 inci, spasi 1.0) -->
    <w:style w:type="paragraph" w:customStyle="1" w:styleId="Bibliography1">
      <w:name w:val="Bibliography1"/>
      <w:basedOn w:val="Normal"/>
      <w:pPr>
        <w:spacing w:line="240" w:lineRule="auto" w:before="0" w:after="120"/>
        <w:ind w:left="720" w:hanging="720"/>
        <w:jc w:val="both"/>
      </w:pPr>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
        <w:sz w:val="24"/><w:szCs w:val="24"/>
      </w:rPr>
    </w:style>

    <!-- Judul Lampiran -->
    <w:style w:type="paragraph" w:customStyle="1" w:styleId="AppendixTitle">
      <w:name w:val="Appendix Title"/>
      <w:basedOn w:val="Normal"/>
      <w:pPr>
        <w:spacing w:before="240" w:after="240" w:line="240" w:lineRule="auto"/>
        <w:jc w:val="center"/>
      </w:pPr>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
        <w:b/><w:bCs/><w:sz w:val="24"/><w:szCs w:val="24"/>
      </w:rPr>
    </w:style>

    <!-- Cover Page Elements -->
    <w:style w:type="paragraph" w:customStyle="1" w:styleId="CoverTitle">
      <w:name w:val="CoverTitle"/>
      <w:basedOn w:val="Normal"/>
      <w:pPr>
        <w:spacing w:line="280" w:lineRule="auto" w:before="0" w:after="180"/>
        <w:jc w:val="center"/>
      </w:pPr>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
        <w:b/><w:bCs/><w:sz w:val="28"/><w:szCs w:val="28"/>
      </w:rPr>
    </w:style>

    <w:style w:type="paragraph" w:customStyle="1" w:styleId="CoverName">
      <w:name w:val="CoverName"/>
      <w:basedOn w:val="Normal"/>
      <w:pPr>
        <w:spacing w:line="240" w:lineRule="auto" w:before="60" w:after="60"/>
        <w:jc w:val="center"/>
      </w:pPr>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
        <w:b/><w:bCs/><w:u w:val="single"/><w:sz w:val="24"/><w:szCs w:val="24"/>
      </w:rPr>
    </w:style>

    <w:style w:type="paragraph" w:customStyle="1" w:styleId="CoverLine">
      <w:name w:val="CoverLine"/>
      <w:basedOn w:val="Normal"/>
      <w:pPr>
        <w:spacing w:line="240" w:lineRule="auto" w:before="60" w:after="60"/>
        <w:jc w:val="center"/>
      </w:pPr>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
        <w:sz w:val="24"/><w:szCs w:val="24"/>
      </w:rPr>
    </w:style>

    <w:style w:type="paragraph" w:customStyle="1" w:styleId="CoverInstitution">
      <w:name w:val="CoverInstitution"/>
      <w:basedOn w:val="Normal"/>
      <w:pPr>
        <w:spacing w:line="240" w:lineRule="auto" w:before="0" w:after="60"/>
        <w:jc w:val="center"/>
      </w:pPr>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
        <w:b/><w:bCs/><w:sz w:val="24"/><w:szCs w:val="24"/>
      </w:rPr>
    </w:style>
    """
    
    styles_xml = styles_xml.replace("</w:styles>", custom_styles + "</w:styles>")
    items["word/styles.xml"] = styles_xml.encode("utf-8")
    
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in items.items():
            zout.writestr(name, data)
            
    print(f"[OK] Reference docx berhasil dibuat: {out_path}")

if __name__ == "__main__":
    dst = sys.argv[1] if len(sys.argv) > 1 else "templates/reference.docx"
    build_reference_docx(dst)
