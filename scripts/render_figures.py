#!/usr/bin/env python3
"""render_figures.py: Generator diagram berstandar ISO 5807 dan UML.
Menghasilkan SVG dan PNG tajam (anti-aliasing) untuk disertakan ke dalam proposal.
"""

import math
import sys
from html import escape
from pathlib import Path

class DiagramCanvas:
    def __init__(self, width=650, height=800):
        self.w = width
        self.h = height
        self.s = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect width="100%" height="100%" fill="white"/>'
        ]

    def line(self, pts, arrow=False, dash=False, width=1.8, color="#222222"):
        pts_str = " ".join(f"{x},{y}" for x, y in pts)
        dash_str = ' stroke-dasharray="7 5"' if dash else ""
        self.s.append(f'<polyline points="{pts_str}" fill="none" stroke="{color}" stroke-width="{width}"{dash_str}/>')
        if arrow and len(pts) >= 2:
            x, y = pts[-1]
            px, py = pts[-2]
            a = math.atan2(y - py, x - px)
            l, q = 10, 4.5
            coords = [
                (x, y),
                (x - l * math.cos(a) + q * math.sin(a), y - l * math.sin(a) - q * math.cos(a)),
                (x - l * math.cos(a) - q * math.sin(a), y - l * math.sin(a) + q * math.cos(a))
            ]
            c_str = " ".join(f"{cx},{cy}" for cx, cy in coords)
            self.s.append(f'<polygon points="{c_str}" fill="{color}"/>')

    def rect(self, x, y, w, h, fill="white", rounding=0):
        self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rounding}" fill="{fill}" stroke="#222222" stroke-width="1.8"/>')

    def poly(self, pts, fill="white"):
        closed = list(pts) + [pts[0]]
        pts_str = " ".join(f"{x},{y}" for x, y in closed)
        self.s.append(f'<polygon points="{pts_str}" fill="{fill}" stroke="#222222" stroke-width="1.8"/>')

    def text(self, x, y, text_str, size=18, bold=False, anchor="middle", leading=None):
        lines = text_str.split("\n")
        leading = leading or size * 1.25
        weight = "bold" if bold else "normal"
        for k, line in enumerate(lines):
            self.s.append(
                f'<text x="{x}" y="{y + k * leading}" font-family="Times New Roman,serif" font-size="{size}" '
                f'font-weight="{weight}" text-anchor="{anchor}">{escape(line)}</text>'
            )

    def box(self, x, y, w, h, text_str, shape="process", size=18, fill="white"):
        """Simbol baku ISO 5807: terminal, process, io, decision"""
        if shape == "decision":
            self.poly([(x + w / 2, y), (x + w, y + h / 2), (x + w / 2, y + h), (x, y + h / 2)], fill)
        elif shape == "io":
            self.poly([(x + 20, y), (x + w, y), (x + w - 20, y + h), (x, y + h)], fill)
        elif shape == "terminal":
            self.rect(x, y, w, h, fill, rounding=h / 2)
        else:
            self.rect(x, y, w, h, fill, rounding=0)

        n = len(text_str.split("\n"))
        self.text(x + w / 2, y + h / 2 - (n - 1) * size * 0.55 + size * 0.3, text_str, size)

    def save(self, output_base):
        svg_code = "".join(self.s) + "</svg>"
        svg_path = Path(f"{output_base}.svg")
        png_path = Path(f"{output_base}.png")
        svg_path.write_text(svg_code, encoding="utf-8")

        # Konversi ke PNG via PyMuPDF (fitz) atau ImageMagick
        try:
            import fitz
            f = fitz.open(stream=svg_code.encode("utf-8"), filetype="svg")
            pix = f[0].get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=False)
            pix.save(str(png_path))
            print(f"[OK] Diagram PNG tersimpan (via PyMuPDF): {png_path}")
            return
        except ImportError:
            pass

        import shutil, subprocess
        if shutil.which("convert"):
            try:
                subprocess.run(["convert", "-density", "200", str(svg_path), str(png_path)], check=True)
                print(f"[OK] Diagram PNG tersimpan (via ImageMagick): {png_path}")
                return
            except Exception as e:
                pass

        print(f"[OK] Diagram SVG tersimpan: {svg_path} (install PyMuPDF/ImageMagick untuk auto PNG)")

def generate_sample_research_flow(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    c = DiagramCanvas(600, 780)
    x, w = 150, 300
    
    # ISO 5807 Flowchart Penelitian
    c.box(x, 30, w, 45, "Mulai", shape="terminal")
    c.line([(x + w/2, 75), (x + w/2, 110)], arrow=True)
    
    c.box(x, 110, w, 55, "Studi Literatur &\nIdentifikasi Masalah", shape="process")
    c.line([(x + w/2, 165), (x + w/2, 200)], arrow=True)
    
    c.box(x, 200, w, 55, "Pengumpulan Data &\nStudi Lapangan", shape="io")
    c.line([(x + w/2, 255), (x + w/2, 290)], arrow=True)
    
    c.box(x, 290, w, 55, "Analisis Kebutuhan &\nPerancangan Sistem", shape="process")
    c.line([(x + w/2, 345), (x + w/2, 380)], arrow=True)
    
    c.box(x, 380, w, 55, "Implementasi Kode &\nIntegrasi Model", shape="process")
    c.line([(x + w/2, 435), (x + w/2, 470)], arrow=True)
    
    c.box(x, 470, w, 80, "Pengujian Sistem &\nEvaluasi Hasil?", shape="decision")
    c.line([(x + w/2, 550), (x + w/2, 600)], arrow=True)
    c.text(x + w/2 + 20, 575, "Ya", size=16, anchor="start")
    
    # Loop back jika tidak
    c.line([(x + w, 510), (x + w + 50, 510), (x + w + 50, 407), (x + w, 407)], arrow=True)
    c.text(x + w + 10, 500, "Tidak", size=16, anchor="start")
    
    c.box(x, 600, w, 55, "Penyusunan Laporan &\nDokumentasi Hasil", shape="process")
    c.line([(x + w/2, 655), (x + w/2, 690)], arrow=True)
    
    c.box(x, 690, w, 45, "Selesai", shape="terminal")
    
    c.save(out_dir / "flowchart_penelitian")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "gambar"
    generate_sample_research_flow(out)
