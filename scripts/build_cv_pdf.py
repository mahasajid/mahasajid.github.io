#!/usr/bin/env python3
from pathlib import Path
import re
import textwrap

SOURCE = Path("assets/pdf/cv_content.md")
OUT = Path("assets/pdf/Maha_Sajid_CV.pdf")

PAGE_W, PAGE_H = 612, 792
LEFT, TOP, BOTTOM = 42, 42, 42

def clean(s: str) -> str:
    repl = {
        "\u2013": "-", "\u2014": "--", "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"', "\u00b7": "-", "\u2022": "-",
        "\u00a0": " ", "&": "and",
    }
    for k, v in repl.items():
        s = s.replace(k, v)
    s = re.sub(r"\*\*(.*?)\*\*", r"\1", s)
    s = re.sub(r"\*(.*?)\*", r"\1", s)
    s = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", s)
    return s.strip()

def esc(s: str) -> str:
    return clean(s).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

def wrap(line: str, width: int, hanging: int = 0):
    if not line:
        return [""]
    return textwrap.wrap(line, width=width, subsequent_indent=" " * hanging, break_long_words=False, break_on_hyphens=False) or [""]

def add_line(pages, page, y, text, font="F1", size=8.2, leading=10.2, indent=0):
    if y < BOTTOM + leading:
        pages.append(page)
        page = []
        y = PAGE_H - TOP
    page.append((text, font, size, LEFT + indent, y))
    return page, y - leading

def layout(markdown: str):
    pages, page, y = [], [], PAGE_H - TOP
    lines = markdown.splitlines()
    for raw in lines:
        s = raw.rstrip()
        if not s:
            y -= 4
            continue
        level = 0
        if s.startswith("# "):
            level = 1
            s = s[2:]
        elif s.startswith("## "):
            level = 2
            s = s[3:]
        elif s.startswith("### "):
            level = 3
            s = s[4:]
        elif s.startswith("#### "):
            level = 4
            s = s[5:]
        s = clean(s)
        if not s:
            continue
        if level == 1:
            page, y = add_line(pages, page, y, s, "F2", 16, 19)
        elif level == 2:
            y -= 4
            page, y = add_line(pages, page, y, s, "F2", 11, 14)
            page.append(("_" * 92, "F1", 6, LEFT, y + 5))
        elif level in (3, 4):
            page, y = add_line(pages, page, y, s, "F2", 9, 11)
        else:
            bullet = s.startswith("- ")
            indent = 14 if bullet else 0
            for piece in wrap(s, 100 if bullet else 105, 2 if bullet else 0):
                page, y = add_line(pages, page, y, piece, "F1", 8.2, 10.2, indent)
    if page:
        pages.append(page)
    return pages

def stream_for(lines):
    return "\n".join(
        f"BT /{font} {size:.1f} Tf 1 0 0 1 {x:.1f} {y:.1f} Tm ({esc(text)}) Tj ET"
        for text, font, size, x, y in lines
    ).encode("latin-1", "replace")

def build_pdf(pages):
    objects = []
    kids = []
    streams = []
    for i, lines in enumerate(pages):
        page_obj = 5 + i * 2
        content_obj = page_obj + 1
        kids.append(f"{page_obj} 0 R")
        streams.append((page_obj, content_obj, stream_for(lines)))
    objects.append("1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    objects.append(f"2 0 obj\n<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(kids)} >>\nendobj\n")
    objects.append("3 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")
    objects.append("4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n")
    for page_obj, content_obj, stream in streams:
        objects.append(f"{page_obj} 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_W} {PAGE_H}] /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {content_obj} 0 R >>\nendobj\n")
        objects.append(f"{content_obj} 0 obj\n<< /Length {len(stream)} >>\nstream\n".encode("latin-1") + stream + b"\nendstream\nendobj\n")
    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf.extend(obj.encode("latin-1", "replace") if isinstance(obj, str) else obj)
    xref = len(pdf)
    pdf.extend(f"xref\n0 {len(objects)+1}\n".encode())
    pdf.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        pdf.extend(f"{off:010d} 00000 n \n".encode())
    pdf.extend(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    return bytes(pdf)

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pages = layout(SOURCE.read_text(encoding="utf-8"))
    OUT.write_bytes(build_pdf(pages))
    print(f"Wrote {OUT} ({len(pages)} pages, {OUT.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
