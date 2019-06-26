#!/bin/bash

set -euxo pipefail

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TOP="$( dirname "${BASEDIR}" )"

if ! which docker ; then
    echo 'Docker is missing!' >&2
    exit 1
fi
if ! which docker-compose ; then
    echo 'Docker-Compose is missing!' >&2
    exit 1
fi

TMPFILE=$(mktemp /tmp/vso_check.XXXXXX)
function finish {
  rm -f "${TMPFILE}"
}
trap finish EXIT

cp "${TOP}/README.rst" "${TOP}/ci/docker/"
cp "${TOP}/setup.py" "${TOP}/ci/docker/"
cp "${TOP}/pytest_azurepipelines.py" "${TOP}/ci/docker/"

USEROPT="$(id -u):$(id -g)"
cd "${TOP}"
docker-compose build
docker-compose up -d
docker-compose run --rm -u "${USEROPT}" app /workspace/ci/in_docker.sh | tee "${TMPFILE}"
docker-compose down

# Validate the path mapping has occurred.
if ! grep "^[#][#]*vso[[].*${TOP}" "${TMPFILE}" ; then
    echo "Implicit Docker Path Mapping is missing! check availability of /proc/1/mountinfo" >&2
    echo "see https://github.com/tonybaloney/pytest-azurepipelines/pull/25" >&2
    exit 1
fi
