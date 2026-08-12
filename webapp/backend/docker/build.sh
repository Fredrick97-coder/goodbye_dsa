#!/usr/bin/env bash
# Build the sandbox images used by the docker executor -- one per runtime.
#
# Adding a language with a new runtime means adding its Dockerfile and one line
# here; the executor picks the image up from the language table.
set -euo pipefail
cd "$(dirname "$0")"

build() {
  local image="$1" file="$2"
  echo "building $image"
  docker build -q -f "$file" -t "$image" . >/dev/null
  docker image inspect "$image" --format "  $image  {{.Size}} bytes  user={{.Config.User}}"
}

build "${FORGE_DOCKER_IMAGE:-forge-runner:latest}"      runner.Dockerfile
build "${FORGE_NODE_IMAGE:-forge-runner-node:latest}"   node-runner.Dockerfile

echo
echo "done. /api/health reports which images the executor found."
