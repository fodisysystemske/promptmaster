# Building the KDP interior PDF from `PROMPTMASTER_KDP_MANUSCRIPT.md`

This manuscript is authored in **Markdown** so it can be version-controlled, diffed, and deposited on **Zenodo** alongside checksums. Amazon KDP accepts **PDF** for print and many ebook flows; the standard professional path is **Markdown → PDF** or **Markdown → DOCX → Word template → PDF**.

## Option A — Pandoc to PDF (LaTeX engine)

1. Install [Pandoc](https://pandoc.org/) and a LaTeX distribution (e.g., MiKTeX on Windows, TeX Live on Linux/macOS).
2. From the repository root:

```powershell
cd "d:\SOFTWARE ENGINEERING\BLOG"
pandoc PROMPTMASTER_KDP_MANUSCRIPT.md -o PROMPTMASTER_KDP_INTERIOR.pdf --pdf-engine=xelatex -V geometry:margin=1in -V documentclass=book -V linestretch=1.15 --toc --toc-depth=2
```

3. **Mermaid:** Pandoc does not render Mermaid natively. Either:
   - install [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) (`mmdc`) and replace each fenced `mermaid` block with an exported PNG/SVG before PDF, or  
   - use a toolchain that supports Mermaid (some commercial converters), or  
   - leave diagrams as code in the PDF for a technical audience (not ideal for mass-market print).

## Option B — Pandoc to DOCX, then Microsoft Word

```powershell
pandoc PROMPTMASTER_KDP_MANUSCRIPT.md -o PROMPTMASTER_KDP_INTERIOR.docx --toc --toc-depth=2
```

Open in Word, apply **Heading 1–3** styles, set **KDP-compatible embed fonts** (File → Options → Save → embed fonts), fix page breaks, insert rendered Mermaid images, then **Save As PDF**.

## Option C — KDP CreateSpace / Kindle Create

Import DOCX into Amazon’s interior tools where supported; verify trim size (e.g., 6×9 in) and gutter margins against KDP’s latest bleed guidelines.

## Zenodo bundle

Zip at minimum:

- `PROMPTMASTER_KDP_MANUSCRIPT.md` (generated)
- `promptmaster.json`
- `promptmaster_livebook_volume2.md`
- `scripts/build_kdp_manuscript.py` and `scripts/kernel_depth_data.py`
- `promptmaster_training/` (full tree)
- `pyproject.toml`, `README_PROMPTMASTER.md`
- `checksums.txt` (SHA-256 of each file)

Tag the Zenodo record version to match your KDP **edition** number on the copyright page.
