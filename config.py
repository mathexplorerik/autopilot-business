from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# ==========================
# AI MODEL
# ==========================

OLLAMA_MODEL = "gemma3"
OLLAMA_URL = "http://localhost:11434"

# ==========================
# BOOK SETTINGS
# ==========================

BOOK_TYPE = "Coloring Book"
BOOK_SIZE = (8.5, 11)
DPI = 300
LANGUAGE = "English"

# ==========================
# OUTPUT
# ==========================

OUTPUT_DIR = "output"

IMAGE_FOLDER = "output/images"
PDF_FOLDER = "output/pdfs"
COVER_FOLDER = "output/covers"
MARKETING_FOLDER = "output/social"

# ==========================
# AMAZON KDP
# ==========================

BLEED = True
MARGIN = 0.25

# ==========================
# IMAGE GENERATION
# ==========================

IMAGE_STYLE = "Black and White Line Art"
BACKGROUND = "White"

# ==========================
# SOCIAL MEDIA
# ==========================

PINTEREST = True
INSTAGRAM = True
FACEBOOK = True
X = True

# ==========================
# LOGGING
# ==========================

LOG_FOLDER = "logs"
# Image Provider
IMAGE_PROVIDER = "leonardo"

# Leonardo API
LEONARDO_API_KEY = ""