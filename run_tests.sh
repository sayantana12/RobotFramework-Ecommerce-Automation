#!/usr/bin/env bash
# Runs the full Robot Framework suite from the command line and writes
# log.html / report.html / output.xml into the Results folder.
#
# Usage:
#   ./run_tests.sh                # runs everything with Chrome
#   ./run_tests.sh firefox        # runs everything with Firefox
set -e

BROWSER=${1:-chrome}

robot \
    --variable BROWSER:"${BROWSER}" \
    --outputdir Results \
    --loglevel INFO \
    TestSuites
