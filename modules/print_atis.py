import os
import json
import sys
from fpdf import FPDF
import subprocess

SETTINGS_FILE = "data/settings.json"
PDF_OUTPUT = "output_atis.pdf"
PDFTOPRINTER_PATH = os.path.join("modules", "PDFtoPrinter_m.exe")

class CustomPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="L")  # Landscape orientation
        self.set_auto_page_break(auto=True, margin=10)

    def add_text(self, content):
        self.add_page()
        self.set_font("Arial", size=10)  # Smaller font
        self.multi_cell(0, 5, content)  # Dynamic text wrapping

def load_settings():
    """Load printer settings from settings.json."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    raise FileNotFoundError("settings.json not found")

def generate_pdf(content, pdf_path):
    """Generate a PDF with the given content."""
    pdf = CustomPDF()
    pdf.add_text(content)
    pdf.output(pdf_path)

def print_pdf(printer_name, pdf_path):
    """Print the PDF using PDFtoPrinter_m."""
    try:
        subprocess.run([PDFTOPRINTER_PATH, pdf_path, printer_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error printing PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python print_atis.py <atis>")
        sys.exit(1)

    settings = load_settings()
    printer_name = settings.get("printer_name")

    if not printer_name:
        print("Error: Printer name not set in settings.json!")
        sys.exit(1)

    atis = sys.argv[1]

    generate_pdf(atis, PDF_OUTPUT)
    print_pdf(printer_name, PDF_OUTPUT)

    os.remove(PDF_OUTPUT)
