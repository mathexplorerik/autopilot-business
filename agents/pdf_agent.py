import os
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

class PDFAgent:

    # ✅ KDP Standard Specs
    PAGE_WIDTH  = 8.5 * inch
    PAGE_HEIGHT = 11 * inch
    BLEED       = 0.125 * inch
    MARGIN      = 0.25 * inch

    def build(self, book):
        print("\n📄 PDF Agent Running...\n")
        os.makedirs("output/pdfs", exist_ok=True)

        safe_title = book["title"].replace(" ", "_")
        pdf_path   = f"output/pdfs/{safe_title}.pdf"

        # ✅ Exact KDP size — 8.5 x 11 inch
        c = canvas.Canvas(
            pdf_path,
            pagesize=(self.PAGE_WIDTH, self.PAGE_HEIGHT)
        )

        # ✅ Title Page
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(
            self.PAGE_WIDTH / 2,
            self.PAGE_HEIGHT - 2 * inch,
            book["title"]
        )
        c.setFont("Helvetica", 16)
        c.drawCentredString(
            self.PAGE_WIDTH / 2,
            self.PAGE_HEIGHT - 2.6 * inch,
            book.get("subtitle", "")
        )
        c.setFont("Helvetica", 12)
        c.drawCentredString(
            self.PAGE_WIDTH / 2,
            self.PAGE_HEIGHT - 3.2 * inch,
            f"Ages {book.get('target_age', '4-8 Years')}"
        )
        c.showPage()

        # ✅ Interior Pages — full bleed
        total   = book["pages"]
        found   = 0
        missing = 0

        for page in range(1, total + 1):
            image_path = f"output/images/page_{page:03}.png"

            if os.path.exists(image_path):
                try:
                    img = ImageReader(image_path)
                    # Full page — no margins for coloring books
                    c.drawImage(
                        img,
                        0, 0,
                        width=self.PAGE_WIDTH,
                        height=self.PAGE_HEIGHT,
                        preserveAspectRatio=True,
                        anchor='c',
                        mask="auto"
                    )
                    found += 1
                    print(f"  ✅ Page {page:03}/{total}")
                except Exception as e:
                    print(f"  ❌ Page {page:03} error: {e}")
                    self._placeholder(c, page, self.PAGE_WIDTH, self.PAGE_HEIGHT)
                    missing += 1
            else:
                self._placeholder(c, page, self.PAGE_WIDTH, self.PAGE_HEIGHT)
                missing += 1

            c.showPage()

        c.save()

        # ✅ File size check
        size_mb = os.path.getsize(pdf_path) / (1024 * 1024)

        print(f"\n  {'='*40}")
        print(f"  ✅ PDF Created  : {pdf_path}")
        print(f"  📄 Pages        : {total + 1} (title + {total} content)")
        print(f"  ✅ With images  : {found}")
        print(f"  ⚠️  Placeholders : {missing}")
        print(f"  📦 File size    : {size_mb:.1f} MB")
        print(f"  📐 Page size    : 8.5 x 11 inch (KDP standard)")
        print(f"  {'='*40}\n")

        return pdf_path

    def _placeholder(self, c, page_num, width, height):
        """Placeholder page jab image missing ho"""
        c.setFillColorRGB(0.98, 0.98, 0.98)
        c.rect(0, 0, width, height, fill=1)
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width/2, height/2 + 20, f"Page {page_num}")
        c.setFont("Helvetica", 12)
        c.drawCentredString(width/2, height/2 - 10, "Image coming soon...")
        # Border
        c.setStrokeColorRGB(0.8, 0.8, 0.8)
        c.rect(0.5*inch, 0.5*inch, width - inch, height - inch)