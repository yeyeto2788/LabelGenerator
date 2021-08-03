# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["label_generator"]

package_data = {"": ["*"]}

install_requires = ["Pillow>=8.3.1,<9.0.0", "click>=8.0.1,<9.0.0", "qrcode[pil]>=7.2,<8.0"]

entry_points = {"console_scripts": ["label_generator = label_generator.cli:main_cli"]}

setup_kwargs = {
    "name": "label-generator",
    "version": "0.1.0",
    "description": "Label generator for label printers",
    "long_description": None,
    "author": "Juan Biondi",
    "author_email": None,
    "maintainer": None,
    "maintainer_email": None,
    "url": None,
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.7,<4.0",
}


setup(**setup_kwargs)
