import os
import json
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

class TracingAgent:

    PAGE_W = 8.5 * inch
    PAGE_H = 11 * inch

    def generate(self, book):
        print("\n✏️  Tracing Agent Running...\n")

        niche     = book.get("niche", "alphabet")
        age       = book.get("target_age", "3-6 Years")
        title     = book.get("title", "Tracing Book for Kids")

        os.makedirs("output/tracing", exist_ok=True)
        os.makedirs("output/prompts", exist_ok=True)

        all_pages   = []
        all_prompts = []

        # ✅ Section 1 — Uppercase A-Z
        print("  📝 Section 1: Uppercase A-Z...")
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            all_pages.append({
                "type":    "uppercase",
                "content": letter,
                "page":    i + 1,
                "title":   f"Trace Letter {letter}"
            })
            all_prompts.append(
                f"Kids tracing worksheet, large dotted letter {letter} uppercase, "
                f"dashed outline for tracing, cute {self._letter_animal(letter)} illustration, "
                f"thick black outlines, white background, educational, printable, "
                f"simple clean design, kids age 3-6"
            )

        # ✅ Section 2 — Lowercase a-z
        print("  📝 Section 2: Lowercase a-z...")
        for i, letter in enumerate("abcdefghijklmnopqrstuvwxyz"):
            all_pages.append({
                "type":    "lowercase",
                "content": letter,
                "page":    i + 27,
                "title":   f"Trace Letter {letter}"
            })
            all_prompts.append(
                f"Kids tracing worksheet, large dotted letter {letter} lowercase, "
                f"dashed outline for tracing, cute illustration, "
                f"thick black outlines, white background, educational, printable, "
                f"simple clean design, kids age 3-6"
            )

        # ✅ Section 3 — Numbers 1-20
        print("  📝 Section 3: Numbers 1-20...")
        for i in range(1, 21):
            all_pages.append({
                "type":    "number",
                "content": str(i),
                "page":    i + 52,
                "title":   f"Trace Number {i}"
            })
            all_prompts.append(
                f"Kids tracing worksheet, large dotted number {i}, "
                f"dashed outline for tracing, cute {self._number_object(i)} illustration, "
                f"thick black outlines, white background, educational, printable, "
                f"simple clean design, kids age 3-6"
            )

        # ✅ Section 4 — Basic Shapes
        shapes = ["circle", "square", "triangle", "rectangle", "oval",
                  "diamond", "star", "heart", "pentagon", "hexagon"]
        print("  📝 Section 4: Basic Shapes...")
        for i, shape in enumerate(shapes):
            all_pages.append({
                "type":    "shape",
                "content": shape,
                "page":    i + 73,
                "title":   f"Trace {shape.title()}"
            })
            all_prompts.append(
                f"Kids tracing worksheet, large dotted {shape} shape, "
                f"dashed outline for tracing, cute illustration inside, "
                f"thick black outlines, white background, educational, printable, "
                f"simple clean design, kids age 3-6"
            )

        total = len(all_pages)
        print(f"\n  📊 Total Pages : {total}")
        print(f"     A-Z Upper  : 26")
        print(f"     a-z Lower  : 26")
        print(f"     Numbers    : 20")
        print(f"     Shapes     : 10")

        # ✅ Save prompts
        self._save_prompts(all_prompts, all_pages)

        # ✅ Generate PDF (Python version)
        pdf_path = self._generate_pdf(all_pages, title, age)

        return {
            "pages":    total,
            "prompts":  all_prompts,
            "pdf_path": pdf_path,
            "sections": {
                "uppercase": 26,
                "lowercase": 26,
                "numbers":   20,
                "shapes":    10
            }
        }

    def _letter_animal(self, letter):
        """Har letter ke liye animal"""
        animals = {
            "A": "ant", "B": "bear", "C": "cat", "D": "dog",
            "E": "elephant", "F": "fox", "G": "giraffe", "H": "horse",
            "I": "iguana", "J": "jaguar", "K": "kangaroo", "L": "lion",
            "M": "monkey", "N": "narwhal", "O": "owl", "P": "penguin",
            "Q": "quail", "R": "rabbit", "S": "snake", "T": "tiger",
            "U": "unicorn", "V": "vulture", "W": "whale", "X": "fox",
            "Y": "yak", "Z": "zebra"
        }
        return animals.get(letter, "animal")

    def _number_object(self, num):
        """Har number ke liye object"""
        objects = {
            1: "sun", 2: "eyes", 3: "leaves", 4: "paws",
            5: "fingers", 6: "flowers", 7: "stars", 8: "legs spider",
            9: "balloons", 10: "toes", 11: "butterflies", 12: "eggs",
            13: "hearts", 14: "dots", 15: "fish", 16: "candles",
            17: "birds", 18: "apples", 19: "bubbles", 20: "flowers"
        }
        return objects.get(num, "objects")

    def _save_prompts(self, prompts, pages):
        """Prompts save karo"""
        txt_path  = "output/prompts/tracing_prompts.txt"
        json_path = "output/prompts/tracing_prompts.json"

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("TRACING BOOK PROMPTS\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total: {len(prompts)} pages\n")
            f.write("="*60 + "\n\n")
            for i, (prompt, page) in enumerate(zip(prompts, pages), 1):
                f.write(f"--- Page {i:02} | {page['type'].upper()} | {page['content']} ---\n")
                f.write(f"{prompt}\n\n")

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "type":      "tracing",
                "total":     len(prompts),
                "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "prompts":   [{"page": p["page"], "type": p["type"],
                               "content": p["content"], "prompt": pr}
                              for p, pr in zip(pages, prompts)]
            }, f, indent=2)

        print(f"\n  📄 Prompts TXT  : {txt_path}")
        print(f"  📄 Prompts JSON : {json_path}")

    def _generate_pdf(self, pages, title, age):
        """Python se basic tracing PDF banao"""
        pdf_path = f"output/pdfs/Tracing_Book_for_Kids.pdf"
        c = canvas.Canvas(pdf_path, pagesize=(self.PAGE_W, self.PAGE_H))

        # ✅ Title Page
        c.setFillColor(HexColor("#FFE066"))
        c.rect(0, 0, self.PAGE_W, self.PAGE_H, fill=1)
        c.setFillColor(HexColor("#2C3E50"))
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(self.PAGE_W/2, self.PAGE_H - 2*inch, title)
        c.setFont("Helvetica", 18)
        c.drawCentredString(self.PAGE_W/2, self.PAGE_H - 2.8*inch, f"Ages {age}")
        c.setFont("Helvetica", 14)
        c.drawCentredString(self.PAGE_W/2, self.PAGE_H - 3.4*inch, "Alphabet • Numbers • Shapes")
        c.showPage()

        # ✅ Section Headers + Pages
        sections = {
            "uppercase": ("🔤 UPPERCASE LETTERS", "#FF6B6B"),
            "lowercase": ("🔡 LOWERCASE LETTERS", "#4ECDC4"),
            "number":    ("🔢 NUMBERS",            "#45B7D1"),
            "shape":     ("🔷 SHAPES",             "#96CEB4"),
        }

        current_section = None

        for page in pages:
            ptype = page["type"]

            # Section header page
            if ptype != current_section:
                current_section = ptype
                name, color = sections.get(ptype, ("", "#FFFFFF"))
                c.setFillColor(HexColor(color))
                c.rect(0, 0, self.PAGE_W, self.PAGE_H, fill=1)
                c.setFillColor(HexColor("#FFFFFF"))
                c.setFont("Helvetica-Bold", 40)
                c.drawCentredString(self.PAGE_W/2, self.PAGE_H/2, name)
                c.showPage()

            # Tracing page
            self._draw_tracing_page(c, page)
            c.showPage()

        c.save()

        size_mb = os.path.getsize(pdf_path) / (1024*1024)
        print(f"\n  ✅ PDF Created  : {pdf_path}")
        print(f"  📦 Size         : {size_mb:.1f} MB")
        print(f"  📄 Pages        : {len(pages) + 5} total")

        return pdf_path

    def _draw_tracing_page(self, c, page):
        """Ek tracing page draw karo"""
        content = page["content"]
        ptype   = page["type"]
        title   = page["title"]

        # Background
        c.setFillColor(HexColor("#FAFAFA"))
        c.rect(0, 0, self.PAGE_W, self.PAGE_H, fill=1)

        # Border
        c.setStrokeColor(HexColor("#CCCCCC"))
        c.setLineWidth(2)
        c.rect(0.3*inch, 0.3*inch,
               self.PAGE_W - 0.6*inch,
               self.PAGE_H - 0.6*inch)

        # Title
        c.setFillColor(HexColor("#2C3E50"))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(self.PAGE_W/2, self.PAGE_H - 0.7*inch, title)

        # Big dotted letter/number/shape
        if ptype in ("uppercase", "lowercase", "number"):
            # Big letter
            c.setFillColor(HexColor("#EEEEEE"))
            c.setFont("Helvetica-Bold", 200)
            c.drawCentredString(self.PAGE_W/2, self.PAGE_H/2 - 1.5*inch, content)

            # Dotted overlay
            c.setFillColor(HexColor("#999999"))
            c.setFont("Helvetica", 8)
            c.drawCentredString(self.PAGE_W/2, 1.2*inch, "Trace the letter with your pencil ✏️")

        elif ptype == "shape":
            # Shape draw karo
            self._draw_shape(c, content)
            c.setFillColor(HexColor("#666666"))
            c.setFont("Helvetica", 12)
            c.drawCentredString(self.PAGE_W/2, 1.2*inch, f"Trace the {content} ✏️")

        # Tracing lines at bottom
        c.setStrokeColor(HexColor("#CCCCCC"))
        c.setLineWidth(1)
        y = 0.9 * inch
        for _ in range(3):
            c.line(0.8*inch, y, self.PAGE_W - 0.8*inch, y)
            y += 0.25 * inch

    def _draw_shape(self, c, shape):
        """Basic shape draw karo"""
        cx = self.PAGE_W / 2
        cy = self.PAGE_H / 2

        c.setStrokeColor(HexColor("#AAAAAA"))
        c.setLineWidth(3)
        c.setDash(6, 4)

        if shape == "circle":
            c.circle(cx, cy, 1.5*inch)
        elif shape == "square":
            c.rect(cx - 1.5*inch, cy - 1.5*inch, 3*inch, 3*inch)
        elif shape == "triangle":
            p = c.beginPath()
            p.moveTo(cx, cy + 1.8*inch)
            p.lineTo(cx - 1.6*inch, cy - 1.2*inch)
            p.lineTo(cx + 1.6*inch, cy - 1.2*inch)
            p.close()
            c.drawPath(p)
        elif shape == "rectangle":
            c.rect(cx - 2*inch, cy - 1*inch, 4*inch, 2*inch)
        elif shape == "oval":
            c.ellipse(cx - 2*inch, cy - 1*inch, cx + 2*inch, cy + 1*inch)
        elif shape == "diamond":
            p = c.beginPath()
            p.moveTo(cx, cy + 1.8*inch)
            p.lineTo(cx + 1.4*inch, cy)
            p.lineTo(cx, cy - 1.8*inch)
            p.lineTo(cx - 1.4*inch, cy)
            p.close()
            c.drawPath(p)
        elif shape == "star":
            self._draw_star(c, cx, cy, 1.5*inch, 0.6*inch)
        elif shape == "heart":
            c.setFont("Helvetica", 150)
            c.setFillColor(HexColor("#EEEEEE"))
            c.drawCentredString(cx, cy - 1*inch, "♥")
        else:
            c.circle(cx, cy, 1.5*inch)

        c.setDash()

    def _draw_star(self, c, cx, cy, outer, inner):
        """Star draw karo"""
        import math
        p = c.beginPath()
        for i in range(10):
            angle = math.pi/2 + i * math.pi/5
            r     = outer if i % 2 == 0 else inner
            x     = cx + r * math.cos(angle)
            y     = cy + r * math.sin(angle)
            if i == 0:
                p.moveTo(x, y)
            else:
                p.lineTo(x, y)
        p.close()
        c.drawPath(p)