"""
Image QA tests (V16)
Builds synthetic images with Pillow and checks that ImageQA
accepts good line-art and rejects colour, shading, tiny images,
corrupt and missing files, without ever crashing.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PIL import Image, ImageDraw

from agents.image_engine.image_qa import ImageQA


def _line_art(path, size=(850, 1100)):
    img = Image.new("RGB", size, (255, 255, 255))
    d = ImageDraw.Draw(img)
    w, h = size
    d.ellipse((w // 4, h // 4, 3 * w // 4, h // 2), outline=(0, 0, 0), width=8)
    d.rectangle((w // 5, h // 2 + 40, 4 * w // 5, 3 * h // 4), outline=(0, 0, 0), width=8)
    img.save(path)


def _colourful(path, size=(850, 1100)):
    img = Image.new("RGB", size, (255, 255, 255))
    d = ImageDraw.Draw(img)
    w, h = size
    d.rectangle((0, 0, w, h // 3), fill=(220, 30, 30))
    d.rectangle((0, h // 3, w, 2 * h // 3), fill=(30, 200, 60))
    d.rectangle((0, 2 * h // 3, w, h), fill=(30, 60, 220))
    img.save(path)


def _grey_shaded(path, size=(850, 1100)):
    Image.new("RGB", size, (128, 128, 128)).save(path)


def _transparent_line_art(path, size=(850, 1100)):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    w, h = size
    d.ellipse((w // 4, h // 4, 3 * w // 4, h // 2), outline=(0, 0, 0, 255), width=8)
    img.save(path)


def test_good_line_art_passes(tmp):
    p = os.path.join(tmp, "good.png")
    _line_art(p)
    r = ImageQA().check(p)
    assert r["passed"], "good line-art was rejected: " + str(r["issues"])
    print("[PASS] clean black-on-white line-art passes", r["metrics"])


def test_colourful_image_fails(tmp):
    p = os.path.join(tmp, "colour.png")
    _colourful(p)
    r = ImageQA().check(p)
    assert not r["passed"], "a fully coloured image was accepted"
    assert any("colour" in i for i in r["issues"]), "colour was not named in the issues"
    print("[PASS] coloured image is rejected with a clear reason")


def test_grey_shaded_image_fails(tmp):
    p = os.path.join(tmp, "grey.png")
    _grey_shaded(p)
    r = ImageQA().check(p)
    assert not r["passed"], "a flat grey image was accepted"
    print("[PASS] grey/shaded image is rejected")


def test_low_resolution_warns_but_passes(tmp):
    p = os.path.join(tmp, "lowres.png")
    _line_art(p, size=(700, 900))
    r = ImageQA().check(p)
    assert r["passed"], "a usable but low-resolution image was hard-failed: " + str(r["issues"])
    assert r["warnings"], "no warning was given for a below-300-DPI image"
    print("[PASS] low-resolution image warns but still passes")


def test_tiny_image_fails(tmp):
    p = os.path.join(tmp, "tiny.png")
    _line_art(p, size=(200, 260))
    r = ImageQA().check(p)
    assert not r["passed"], "a tiny image was accepted for print"
    print("[PASS] tiny image is rejected")


def test_transparent_background_counts_as_white(tmp):
    p = os.path.join(tmp, "transparent.png")
    _transparent_line_art(p)
    r = ImageQA().check(p)
    assert r["passed"], "transparent-background line-art was rejected: " + str(r["issues"])
    print("[PASS] transparent background is treated as white")


def test_corrupt_file_fails_cleanly(tmp):
    p = os.path.join(tmp, "corrupt.png")
    with open(p, "wb") as f:
        f.write(b"this is not an image")
    r = ImageQA().check(p)
    assert not r["passed"] and r["issues"], "corrupt file was not reported"
    print("[PASS] corrupt file fails cleanly, no crash")


def test_empty_and_missing_files_fail_cleanly(tmp):
    empty = os.path.join(tmp, "empty.png")
    open(empty, "wb").close()
    assert not ImageQA().check(empty)["passed"], "empty file was accepted"
    assert not ImageQA().check(os.path.join(tmp, "nope.png"))["passed"], "missing file was accepted"
    assert not ImageQA().check(None)["passed"], "None path was accepted"
    print("[PASS] empty, missing and None paths fail cleanly")


def run_all():
    tests = [
        test_good_line_art_passes,
        test_colourful_image_fails,
        test_grey_shaded_image_fails,
        test_low_resolution_warns_but_passes,
        test_tiny_image_fails,
        test_transparent_background_counts_as_white,
        test_corrupt_file_fails_cleanly,
        test_empty_and_missing_files_fail_cleanly,
    ]
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for test in tests:
            try:
                test(tmp)
            except AssertionError as e:
                failed += 1
                print("[FAIL] " + test.__name__ + ": " + str(e))
            except Exception as e:
                failed += 1
                print("[ERROR] " + test.__name__ + ": " + type(e).__name__ + ": " + str(e))
    print()
    if failed:
        print(str(failed) + "/" + str(len(tests)) + " image QA tests FAILED")
    else:
        print("All " + str(len(tests)) + " image QA tests PASSED")
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if run_all() else 1)
