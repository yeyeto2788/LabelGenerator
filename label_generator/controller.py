import csv
import logging
import math
import os
import textwrap
import typing

import qrcode

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps


logger = logging.getLogger(__name__)


def generate_label(text: str, output: str, font: str, qr_data: str, label_size: typing.Tuple[float, float]):
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

    label_width = label_size[0]
    label_height = label_size[1]

    logger.debug(f"Max widht: {label_width}, Max height: {label_height}")

    border_pixels = 1
    # Space between text and top and bottom border
    padding = 6
    # Max characters per line
    max_characters = 30

    if qr_data:
        qr_box_size = math.ceil(label_height // 45)

        logger.debug(f"Generating QR code with border '{qr_box_size}'")

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=qr_box_size,
            border=1,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_width, qr_height = qr_img.size
        logger.debug(f"QR generated with width: '{qr_width}' and height height: '{qr_height}'")

        size = (
            label_width - qr_width - (border_pixels * 2),
            label_height - (border_pixels * 2),
        )

    else:
        size = (label_width - (border_pixels * 2), label_height - (border_pixels * 2))

    logger.debug(f"Label text image size: '{size}'")

    img = Image.new("RGB", size, "white")
    drawing = ImageDraw.Draw(img)

    for multiplier in range(1, 101):
        # Reduce the font size until it fits on label.
        font_size = label_height - (2 * multiplier)

        if font_size < 8:
            raise ValueError(f"Provided text will not be readable.\nit has {len(text)} chars!")

        # Reduce also amount of charaters in order to fit them all
        if multiplier % 10 == 0:
            max_characters -= 2

        image_font = ImageFont.truetype(font, size=font_size)
        image_text = "\n".join(textwrap.wrap(text, width=max_characters))

        text_width, text_height = drawing.textsize(image_text, font=image_font)

        max_label_width = size[0] - (padding // 2)
        max_label_height = label_height - padding

        if (text_width <= max_label_width) and (text_height <= max_label_height):

            logger.debug(f"max_label_width: '{max_label_width}', max_label_height: '{max_label_height}'")
            logger.debug(f"text_width {text_width}, text_height {text_height}")
            logger.debug(f"Font size: {font_size}, max_chars: {max_characters} with '{multiplier}'")
            logger.debug(f"Total characters of the string: '{len(text)}'")
            # Try centering the text
            drawing.text(
                (border_pixels, (label_height - text_height) // 2),
                image_text,
                font=image_font,
                fill="black",
            )

            break

    # Add the QR code to the label
    if qr_data:
        # Create the border image
        background_image = Image.new("RGB", size=(label_width, label_height), color="black")
        # Create white center image due to qr being different on size
        white_img = Image.new(
            "RGB",
            size=(label_width - border_pixels, label_height - border_pixels),
            color="white",
        )
        background_image.paste(white_img, (border_pixels, border_pixels))
        # Add the label to the border/background
        background_image.paste(img, (border_pixels, border_pixels))
        qr_width, qr_height = qr_img.size
        # Add the qr code image to the label
        qr_vertical_position = (label_height - qr_height) // 2
        background_image.paste(qr_img, (label_width - qr_width, qr_vertical_position))
    else:
        # Add border to the image
        background_image = ImageOps.expand(img, border=border_pixels, fill="black")

    logger.debug(f"Saving image at {output}")
    background_image.save(output)
    logger.info(f"Image saved at {output}")


def generate_labels_from_csv(csv_path: str, font: str, output: str, label_size: typing.Tuple[float, float]):

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
        base_image = Image.new(
            "RGB",
            (label_size[0], label_size[1] * images_count),
            color="white",
        )
        paste_height = 0

        for index, row in enumerate(csv_reader):
            logger.debug(f"Generating label with data '{row}'")
            filename = f"./{index}.png"
            generate_label(text=row["text"], output=filename, font=font, qr_data=row["qr_data"], label_size=label_size)
            logger.debug(f"Opening image '{filename}'")
            # Open image to paste
            image_to_paste = Image.open(filename)
            paste_height = label_size[1] * index
            base_image.paste(image_to_paste, box=(0, paste_height))
            image_to_paste.close()
            # Delete label already pasted.
            os.remove(filename)

        base_image.save(output)
