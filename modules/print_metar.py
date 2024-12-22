import os
import json
import sys
from fpdf import FPDF
import subprocess

SETTINGS_FILE = "data/settings.json"
PDF_OUTPUT = "data/output_metar_taf.pdf"
PDFTOPRINTER_PATH = os.path.join("modules", "PDFtoPrinter_m.exe")


class CustomPDF(FPDF):
    def __init__(self, width, height):
        super().__init__(orientation="P", unit="mm", format=(width, height))
        self.set_auto_page_break(auto=True, margin=5)
        self.set_margins(5, 5, 5)
        self.width = width

    def add_section(self, title, content, font_size=10):
        # Add bold section title
        self.set_font("Arial", "B", font_size)
        self.cell(0, 5, title, ln=True, align="L")
        self.ln(1)  # Add small spacing after title

        # Add bold content
        self.set_font("Arial", "B", font_size)
        self.multi_cell(0, 4, content, align="L")  # Smaller line height for compactness
        self.ln(3)  # Add spacing after section


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    raise FileNotFoundError("settings.json not found")


def generate_pdf(metar, taf, pdf_path):
    page_width, page_height = 80, 297  # Standard 80mm width, A4 height

    pdf = CustomPDF(width=page_width, height=page_height)
    pdf.add_page()

    # Add METAR and TAF sections
    pdf.add_section("METAR:", metar or "No METAR data available.")
    pdf.add_section("TAF:", taf or "No TAF data available.")

    pdf.output(pdf_path)


def print_pdf(printer_name, pdf_path):
    try:
        subprocess.run([PDFTOPRINTER_PATH, pdf_path, printer_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error printing PDF: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python print_metar.py <metar> <taf>")
        sys.exit(1)

    settings = load_settings()
    printer_name = settings.get("printer_name")

    if not printer_name:
        print("Error: Printer name not set in settings.json!")
        sys.exit(1)

    metar = sys.argv[1]
    taf = sys.argv[2]

    generate_pdf(metar, taf, PDF_OUTPUT)
    print_pdf(printer_name, PDF_OUTPUT)

    print(f"PDF saved at: {os.path.abspath(PDF_OUTPUT)}")
