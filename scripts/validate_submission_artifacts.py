"""Validate Paper 61 final submission artifacts."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PAPER_PDF = ROOT / "paper" / "main.pdf"
DOWNLOADS_PDF = Path(r"C:\Users\wangz\Downloads\61.pdf")
DESKTOP_PDF = Path(r"C:\Users\wangz\Desktop\61.pdf")
EXPECTED_MAIN_ROWS = 17600
EXPECTED_ABLATION_ROWS = 1440
MIN_PAGES = 25


def count_rows(path: Path) -> int:
    if not path.exists():
        return -1
    with path.open(newline="", encoding="utf-8") as f:
        return sum(1 for _ in csv.DictReader(f))


def page_count(path: Path) -> int:
    try:
        import PyPDF2

        return len(PyPDF2.PdfReader(str(path)).pages)
    except Exception:
        try:
            from pypdf import PdfReader

            return len(PdfReader(str(path)).pages)
        except Exception:
            try:
                result = subprocess.run(["pdfinfo", str(path)], check=True, capture_output=True, text=True)
                for line in result.stdout.splitlines():
                    if line.startswith("Pages:"):
                        return int(line.split(":", 1)[1].strip())
            except Exception:
                return -1


def main() -> int:
    checks = []
    main_rows = count_rows(RESULTS / "mujoco_contact_raw.csv")
    ablation_rows = count_rows(RESULTS / "mujoco_contact_ablation_raw.csv")
    paper_pages = page_count(PAPER_PDF)
    downloads_pages = page_count(DOWNLOADS_PDF)
    checks.append(("main_rows", main_rows == EXPECTED_MAIN_ROWS, main_rows))
    checks.append(("ablation_rows", ablation_rows == EXPECTED_ABLATION_ROWS, ablation_rows))
    checks.append(("paper_pdf_exists", PAPER_PDF.exists(), str(PAPER_PDF)))
    checks.append(("downloads_pdf_exists", DOWNLOADS_PDF.exists(), str(DOWNLOADS_PDF)))
    checks.append(("paper_pdf_pages", paper_pages >= MIN_PAGES, paper_pages))
    checks.append(("downloads_pdf_pages", downloads_pages >= MIN_PAGES, downloads_pages))
    checks.append(("desktop_pdf_absent", not DESKTOP_PDF.exists(), str(DESKTOP_PDF)))
    if PAPER_PDF.exists() and DOWNLOADS_PDF.exists():
        checks.append(("downloads_matches_paper_size", PAPER_PDF.stat().st_size == DOWNLOADS_PDF.stat().st_size, f"{PAPER_PDF.stat().st_size}/{DOWNLOADS_PDF.stat().st_size}"))

    failed = False
    for name, ok, value in checks:
        status = "PASS" if ok else "FAIL"
        print(f"{status}\t{name}\t{value}")
        failed = failed or not ok
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
