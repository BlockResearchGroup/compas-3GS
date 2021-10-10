#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
echo "$BASEDIR"

chmod +x "$BASEDIR"/env/bin/python
"$BASEDIR"/env/bin/python -m compas_pgs.install --plugin_path "$BASEDIR"/../