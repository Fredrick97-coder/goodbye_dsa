#!/usr/bin/env bash
# Build the sandbox image used by the docker executor.
set -euo pipefail
cd "$(dirname "$0")"
IMAGE="${FORGE_DOCKER_IMAGE:-forge-runner:latest}"
echo "building $IMAGE"
docker build -f runner.Dockerfile -t "$IMAGE" .
echo
echo "built $IMAGE:"
docker image inspect "$IMAGE" --format '  size: {{.Size}} bytes
  python: {{index .Config.Env 0}}
  user:   {{.Config.User}}'
