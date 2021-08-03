import csv
import logging
import os
import textwrap

import qrcode

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

from label_generator.constants import LABEL_HEIGHT
from label_generator.constants import LABEL_WIDTH


logger = logging.getLogger(__name__)


def generate_label(text: str, output: str, font: str, qr_data: str):
    """Generate single label.

    Args:
        text (str): Text to be displayed on the label.
        output (str): Path to the output file
        font (str): Path to the font to be used.
        qr_data (str): Data to be added to the qr code.

    Raises:
        ValueError:
            When text provided can not fit on the label.
    """

    # # Make some important checks
    if not output.endswith(".png"):
        ValueError(f"The extension of the file '{output}' should be '.png'")

    border_pixels = 1
    # Space between text and top and bottom border
    padding = 6
    # Max characters per line
    max_characters = 30

    if qr_data:
        logger.debug("Generating QR code")
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=1,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_width, qr_height = qr_img.size
        logger.debug(f"QR generated with width: '{qr_width}' and height height: '{qr_height}'")

        size = (
            LABEL_WIDTH - qr_width - (border_pixels * 2),
            LABEL_HEIGHT - (border_pixels * 2),
        )

    else:
        size = (LABEL_WIDTH - (border_pixels * 2), LABEL_HEIGHT - (border_pixels * 2))

    logger.debug(f"Label text image size: '{size}'")

    img = Image.new("RGB", size, "white")
    drawing = ImageDraw.Draw(img)

    for multiplier in range(1, 21):
        # Reduce the font size until it fits on label.
        font_size = LABEL_HEIGHT - (2 * multiplier)

        if font_size < 8:
            raise ValueError(f"Provided text will not be readable.\nit has {len(text)} chars!")

        # Reduce also amount of charaters in order to fit them all
        if multiplier % 10 == 0:
            max_characters -= 2

        image_font = ImageFont.truetype(font, size=font_size)
        image_text = "\n".join(textwrap.wrap(text, width=max_characters))

        text_width, text_height = drawing.textsize(image_text, font=image_font)

        max_label_width = size[0] - (padding // 2)
        max_label_height = LABEL_HEIGHT - padding

        if (text_width <= max_label_width) and (text_height <= max_label_height):

            logger.debug(f"max_label_width: '{max_label_width}', max_label_height: '{max_label_height}'")
            logger.debug(f"text_width {text_width}, text_height {text_height}")
            logger.debug(f"Font size: {font_size}, max_chars: {max_characters} with '{multiplier}'")
            logger.debug(f"Total characters of the string: '{len(text)}'")
            # Try centering the text
            drawing.text(
                (border_pixels, (LABEL_HEIGHT - text_height) // 2),
                image_text,
                font=image_font,
                fill="black",
            )

            break

    # Add the QR code to the label
    if qr_data:
        # Create the border image
        background_image = Image.new("RGB", size=(LABEL_WIDTH, LABEL_HEIGHT), color="black")
        # Create white center image due to qr being different on size
        white_img = Image.new(
            "RGB",
            size=(LABEL_WIDTH - border_pixels, LABEL_HEIGHT - border_pixels),
            color="white",
        )
        background_image.paste(white_img, (border_pixels, border_pixels))
        # Add the label to the border/background
        background_image.paste(img, (border_pixels, border_pixels))
        qr_width, qr_height = qr_img.size
        # Add the qr code image to the label
        qr_vertical_position = (LABEL_HEIGHT - qr_height) // 2
        background_image.paste(qr_img, (LABEL_WIDTH - qr_width, qr_vertical_position))
    else:
        # Add border to the image
        background_image = ImageOps.expand(img, border=border_pixels, fill="black")

    logger.debug(f"Saving image at {output}")
    background_image.save(output)
    background_image.close()
    logger.info(f"Image saved at {output}")


def generate_labels_from_csv(csv_path: str, font: str, output: str):

    with open(csv_path) as csv_file:
        # Get the lines with data and skip empty ones.
        lines = [not_empty_line for not_empty_line in (line.rstrip() for line in csv_file) if not_empty_line]
        images_count = len(lines) - 1
        # Reset cursor to be at beginning
        csv_file.seek(0)
        csv_reader = csv.DictReader(csv_file, fieldnames=["text", "qr_data"])
        # Skip csv headers
        next(csv_reader)
        # Create base image where all images are being pasted
        base_image = Image.new("RGB", (LABEL_WIDTH, LABEL_HEIGHT * images_count), color="white")
        paste_height = 0

        for index, row in enumerate(csv_reader):
            logger.debug(f"Generating label with data '{row}'")
            filename = f"./{index}.png"
            generate_label(
                text=row["text"],
                output=filename,
                font=font,
                qr_data=row["qr_data"],
            )
            logger.debug(f"Opening image '{filename}'")
            # Open image to paste
            image_to_paste = Image.open(filename)
            paste_height = LABEL_HEIGHT * index
            base_image.paste(image_to_paste, box=(0, paste_height))
            image_to_paste.close()
            # Delete label already pasted.
            os.remove(filename)

        base_image.save(output)
