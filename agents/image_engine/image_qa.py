"""
Image QA (V16)
Checks one generated page image against what a colouring-book
page should look like: black line-art on a white background,
no colour, not shaded, big enough to print.

IMPORTANT: every threshold below is a first guess. They have not
been tuned against a real Stability image yet. Run check() on the
first real image, read the metrics, then adjust the numbers.
"""

import os

from PIL import Image


class ImageQA:

    # Colour: pixels with HSV saturation above the cutoff count as coloured
    COLOUR_SATURATION_CUTOFF = 40
    MAX_COLOURFUL_FRACTION = 0.02

    # White background
    WHITE_CUTOFF = 235
    MIN_WHITE_FRACTION = 0.60

    # Shading: share of mid-grey pixels (line-art edges add a few)
    MIDGRAY_LOW = 60
    MIDGRAY_HIGH = 200
    WARN_MIDGRAY_FRACTION = 0.10
    FAIL_MIDGRAY_FRACTION = 0.20

    # Page geometry (KDP 8.5 x 11 inch)
    PAGE_WIDTH_INCHES = 8.5
    PAGE_HEIGHT_INCHES = 11.0
    ASPECT_WARN_DEVIATION = 0.10
    WARN_DPI = 300
    FAIL_DPI = 72

    def check(self, path):
        issues = []
        warnings = []
        metrics = {}

        if not path or not os.path.exists(path):
            return self._result(path, ["file does not exist"], warnings, metrics)
        if os.path.getsize(path) == 0:
            return self._result(path, ["file is empty (0 bytes)"], warnings, metrics)

        try:
            img = Image.open(path)
            img.load()
        except Exception as e:
            return self._result(
                path, ["cannot be read as an image (" + type(e).__name__ + ")"], warnings, metrics
            )

        width, height = img.size
        if width <= 0 or height <= 0:
            return self._result(path, ["image has zero width or height"], warnings, metrics)
        metrics["width_px"] = width
        metrics["height_px"] = height

        # Flatten onto white so transparent backgrounds count as white
        if img.mode != "RGB":
            rgba = img.convert("RGBA")
            background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
            img = Image.alpha_composite(background, rgba).convert("RGB")

        total = width * height

        # Colour
        saturation = img.convert("HSV").split()[1].histogram()
        colourful = sum(saturation[self.COLOUR_SATURATION_CUTOFF:]) / total
        metrics["colourful_fraction"] = round(colourful, 4)
        if colourful > self.MAX_COLOURFUL_FRACTION:
            issues.append(
                "image contains colour (" + str(round(colourful * 100, 1))
                + "% coloured pixels) - colouring pages must be black and white"
            )

        # White background and shading
        grey = img.convert("L").histogram()
        white = sum(grey[self.WHITE_CUTOFF:]) / total
        midgray = sum(grey[self.MIDGRAY_LOW:self.MIDGRAY_HIGH + 1]) / total
        metrics["white_fraction"] = round(white, 4)
        metrics["midgray_fraction"] = round(midgray, 4)

        if white < self.MIN_WHITE_FRACTION:
            issues.append(
                "background is not mostly white (" + str(round(white * 100, 1))
                + "% white pixels)"
            )
        if midgray > self.FAIL_MIDGRAY_FRACTION:
            issues.append(
                "image looks shaded or grey (" + str(round(midgray * 100, 1))
                + "% mid-grey pixels)"
            )
        elif midgray > self.WARN_MIDGRAY_FRACTION:
            warnings.append(
                "some grey shading present (" + str(round(midgray * 100, 1))
                + "% mid-grey pixels)"
            )

        # Resolution and shape
        effective_dpi = width / self.PAGE_WIDTH_INCHES
        metrics["effective_dpi_at_page_width"] = round(effective_dpi, 1)
        if effective_dpi < self.FAIL_DPI:
            issues.append(
                "resolution far too low for print (about " + str(round(effective_dpi))
                + " DPI at page width)"
            )
        elif effective_dpi < self.WARN_DPI:
            warnings.append(
                "below 300 DPI at full page width (about " + str(round(effective_dpi))
                + " DPI) - may look soft in print"
            )

        target_aspect = self.PAGE_WIDTH_INCHES / self.PAGE_HEIGHT_INCHES
        aspect = width / height
        deviation = abs(aspect - target_aspect) / target_aspect
        metrics["aspect_ratio"] = round(aspect, 4)
        metrics["aspect_deviation_from_page"] = round(deviation, 4)
        if deviation > self.ASPECT_WARN_DEVIATION:
            warnings.append(
                "shape differs from 8.5x11 by " + str(round(deviation * 100, 1))
                + "% - page will show white bands"
            )

        return self._result(path, issues, warnings, metrics)

    def _result(self, path, issues, warnings, metrics):
        return {
            "path": path,
            "passed": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "metrics": metrics,
        }
