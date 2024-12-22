import os
import json
import sys
from fpdf import FPDF
import subprocess

SETTINGS_FILE = "data/settings.json"
PDF_OUTPUT = "data/output_atis.pdf"
PDFTOPRINTER_PATH = os.path.join("modules", "PDFtoPrinter_m.exe")

class CustomPDF(FPDF):
    def __init__(self, width, height):
        super().__init__(orientation="P", unit="mm", format=(width, height))
        self.set_auto_page_break(auto=True, margin=2)  # Reduce top/bottom margins
        self.set_margins(2, 2, 2)  # Minimize left/right margins
        self.width = width

    def add_text(self, content):
        self.add_page()
        font_size = 10  # Start with a larger font size
        self.set_font("Courier", style="B", size=font_size)  # Use monospace bold font for better formatting

        # Wrap and fit text to available space
        self.multi_cell(self.width - 6, 6, content, align="L")  # Increase line height and use left alignment

def load_settings():
    """Load printer settings from settings.json."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    raise FileNotFoundError("settings.json not found")

def generate_pdf(content, pdf_path, printer_size):
    """Generate a PDF with the given content and size."""

    # Define page dimensions for 80mm width and a taller height to fit longer messages
    page_width, page_height = 80, 300  # Increase height for larger content

    pdf = CustomPDF(width=page_width, height=page_height)
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
    printer_size = settings.get("printer_size", "80mm")

    if not printer_name:
        print("Error: Printer name not set in settings.json!")
        sys.exit(1)

    atis = sys.argv[1]

    # Debugging step: Print ATIS content to console
    print("ATIS Content:", atis)

    generate_pdf(atis, PDF_OUTPUT, printer_size)
    print_pdf(printer_name, PDF_OUTPUT)

    # PDF is no longer deleted after printing
    print(f"PDF saved at: {os.path.abspath(PDF_OUTPUT)}")
