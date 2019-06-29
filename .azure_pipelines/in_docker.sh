#!/bin/bash

set -euxo pipefail

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TOP="$( dirname "${BASEDIR}" )"
cd "${TOP}"
python3 -m pytest --cov=. --cov-report=xml -v -m "not testfail" tests
