import os

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


class PDFAgent:

    def build(self, book):

        print("\n📄 PDF Agent Running...\n")

        os.makedirs("output/pdfs", exist_ok=True)

        safe_title = book["title"].replace(" ", "_")
        pdf_path = f"output/pdfs/{safe_title}.pdf"

        c = canvas.Canvas(
            pdf_path,
            pagesize=(8.5 * inch, 11 * inch)
        )

        # Title Page
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(306, 720, book["title"])

        c.setFont("Helvetica", 16)
        c.drawCentredString(306, 690, book["subtitle"])

        c.showPage()

        # Interior Pages
        for page in range(1, book["pages"] + 1):

            image_path = f"output/images/page_{page:03}.png"

            if os.path.exists(image_path):

                img = ImageReader(image_path)

                c.drawImage(
                    img,
                    0,
                    0,
                    width=8.5 * inch,
                    height=11 * inch,
                    preserveAspectRatio=True,
                    mask="auto"
                )

            else:

                c.setFont("Helvetica-Bold", 16)
                c.drawString(40, 780, f"Page {page}")

                c.rect(40, 60, 530, 680)

                c.setFont("Helvetica", 12)
                c.drawCentredString(
                    306,
                    40,
                    f"Missing image: {image_path}"
                )

            c.showPage()

        c.save()

        print("✅ PDF Created")

        return pdf_path