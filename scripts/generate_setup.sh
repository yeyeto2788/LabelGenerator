#!/bin/bash
poetry build &&\
tar -xvf dist/*.tar.gz --wildcards --no-anchored '*/setup.py' --strip=1 &&\
rm -rf dist