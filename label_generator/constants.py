import logging
import math
import os
import platform


# Millimeters per pixel
MM_PER_PIXEL = 0.2645833333

# Default label sizes (mm / mm_per_inch)
LABEL_WIDTH = math.floor(50 / MM_PER_PIXEL)
LABEL_HEIGHT = math.floor(12 / MM_PER_PIXEL)

# Just in case no path was passed on the CLI
DEFAULT_OUTPUT_PATH = os.getcwd()

if platform.system() == "Linux":
    FONTS_DIR = "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf"

elif platform.system() == "Darwin":
    FONTS_DIR = "/Library/Fonts/"

else:
    FONTS_DIR = "C:\\Windows\\Fonts folder"

# Logging levels mapping
DEBUG_LOGGING_MAP = {
    0: logging.CRITICAL,
    1: logging.WARNING,
    2: logging.INFO,
    3: logging.DEBUG,
}
