#!/bin/sh

ROOT_DIR="$(pwd)"
SRC_DIR="${ROOT_DIR}/src"

OUTPUT_DIR="${SRC_DIR}/out"

OUTPUT_ARTIFACTS_DIR="${SRC_DIR}/artifacts"

export ROOT_DIR
export SRC_DIR
export OUTPUT_DIR

export OUTPUT_ARTIFACTS_DIR

python3 -u ./scripts/python/release.py
