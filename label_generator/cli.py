#!/usr/bin/env python3
import logging
import math
import os

import click

from label_generator.constants import DEBUG_LOGGING_MAP
from label_generator.constants import FONTS_DIR
from label_generator.constants import LABEL_HEIGHT
from label_generator.constants import LABEL_WIDTH
from label_generator.constants import MM_PER_PIXEL
from label_generator.controller import generate_label
from label_generator.controller import generate_labels_from_csv


logger = logging.getLogger()

__CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


class Mutex(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if: list = kwargs.pop("not_required_if")

        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs["help"] = (
            kwargs.get("help", "")
            + " This option is mutually exclusive with "
            + ", ".join([f"'{option}'" for option in self.not_required_if])
            + "."
        ).strip()
        super(Mutex, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        current_opt: bool = self.name in opts
        for mutex_opt in self.not_required_if:
            if mutex_opt in opts:
                if current_opt:
                    raise click.UsageError(
                        "Illegal usage: '" + str(self.name) + "' is mutually exclusive with " + str(mutex_opt) + "."
                    )
                else:
                    self.prompt = None
        return super(Mutex, self).handle_parse_result(ctx, opts, args)


@click.command(context_settings=__CONTEXT_SETTINGS, no_args_is_help=True)
@click.option(
    "-t",
    "--text",
    type=click.STRING,
    cls=Mutex,
    not_required_if=["from_csv"],
    help="Text to add on the label (Max. 86 characters).",
)
@click.option(
    "--from_csv",
    type=click.Path(exists=True),
    cls=Mutex,
    not_required_if=["text", "qr_data"],
    help="Read labels to create from '.csv' file.",
)
@click.option(
    "-o",
    "--output_path",
    default="./label.png",
    type=click.Path(dir_okay=True),
    required=False,
    help="Full path where to create the image",
)
@click.option(
    "--font",
    default=FONTS_DIR,
    type=click.Path(exists=True),
    required=False,
    help="Font path to be use.",
)
@click.option(
    "--qr_data",
    required=False,
    cls=Mutex,
    not_required_if=["from_csv"],
    help="Data to embed on the label as QR code.",
)
@click.option(
    "-ls",
    "--label_size",
    default=(LABEL_WIDTH, LABEL_HEIGHT),
    nargs=2,
    type=click.Tuple([click.FLOAT, click.FLOAT]),
    required=False,
    help="Size in millimeters of the labels (Width, Height)",
)
@click.option(
    "--verbose",
    "-v",
    help="Sets the debug noise level, specify multiple times " "for more verbosity.",
    type=click.IntRange(0, 3, clamp=True),
    count=True,
)
def main_cli(text, output_path, font, qr_data, verbose, from_csv, label_size):

    label_width = LABEL_WIDTH if label_size[0] == LABEL_WIDTH else math.floor(label_size[0] / MM_PER_PIXEL)
    label_height = LABEL_HEIGHT if label_size[1] == LABEL_HEIGHT else math.floor(label_size[1] / MM_PER_PIXEL)
    label_size = (label_width, label_height)

    if verbose > 0:

        logging.basicConfig(format="[%(levelname)s][%(asctime)-15s] %(message)s")
        logger.setLevel(DEBUG_LOGGING_MAP.get(verbose, logging.DEBUG))

    logger.debug(f"Executing script from '{os.getcwd()}'")

    if from_csv:
        generate_labels_from_csv(
            csv_path=from_csv, font=font, output=os.path.abspath(output_path), label_size=label_size
        )

    else:
        generate_label(text, output=os.path.abspath(output_path), font=font, qr_data=qr_data, label_size=label_size)


if __name__ == "__main__":
    main_cli()
