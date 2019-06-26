#!/bin/bash

set -euxo pipefail

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${BASEDIR}"
DEBIAN_FRONTEND=noninteractive apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -qq -y --no-install-recommends apt-utils
DEBIAN_FRONTEND=noninteractive apt-get install -qq -y --no-install-recommends python3 python3-pip
python3 -m pip install --upgrade pip
python3 -m pip install pytest pytest-cov setuptools
python3 -m pip install -e .
