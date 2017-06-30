#!/bin/bash

python feed_package.py

DATA_PATH=$(pwd)

git -C ${DATA_PATH} commit -a -m \"Auto-commit rss feed\"

git -C ${DATA_PATH} push
