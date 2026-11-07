#!/bin/sh
# Regenerates data/results.js from data/results.json so index.html works when opened directly (file://)
cd "$(dirname "$0")" && { printf 'window.SKATE_DATA = '; cat data/results.json; printf ';\n'; } > data/results.js && echo "data/results.js updated"
