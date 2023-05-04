#!/bin/sh
set -e

/scripts/init/wait-dependencies.sh
/scripts/init/start.sh

exec "$@"
