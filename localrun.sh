#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

ACTION="${1:-}"
if [[ -z "${ACTION}" ]]; then
  echo "Usage: $0 up|down"
  exit 1
fi

if command -v shasum >/dev/null 2>&1; then
  UNIQUE_ID="$(printf '%s' "${ROOT_DIR}:$(id -un)" | shasum -a 256 | awk '{print substr($1,1,10)}')"
else
  UNIQUE_ID="$(printf '%s' "${ROOT_DIR}:$(id -un)" | sha256sum | awk '{print substr($1,1,10)}')"
fi

BASE_IMAGE_REPO="valencia-mcp-base-${UNIQUE_ID}"
APP_IMAGE_REPO="valencia-mcp-server-${UNIQUE_ID}"

export BASE_IMAGE="${BASE_IMAGE_REPO}:latest"
export APP_IMAGE="${APP_IMAGE_REPO}:latest"
export CONTAINER_NAME="valencia-mcp-server-${UNIQUE_ID}"
export COMPOSE_PROJECT_NAME="valenciamcp${UNIQUE_ID}"
export HOST_PORT="${HOST_PORT:-8005}"

COMPOSE_FILE="${ROOT_DIR}/docker-compose.yml"

case "${ACTION}" in
  up)
    if ! docker image inspect "${APP_IMAGE}" >/dev/null 2>&1; then
      echo "App image not found (${APP_IMAGE}); running localbuild.sh first."
      "${ROOT_DIR}/localbuild.sh"
    fi
    docker compose -f "${COMPOSE_FILE}" up -d
    echo "MCP server is running."
    echo "MCP endpoint: http://localhost:${HOST_PORT}/mcp/"
    echo "Swagger UI:  http://localhost:${HOST_PORT}/docs"
    ;;
  down)
    docker compose -f "${COMPOSE_FILE}" down --remove-orphans
    echo "MCP server stopped."
    ;;
  *)
    echo "Unknown action: ${ACTION}"
    echo "Usage: $0 up|down"
    exit 1
    ;;
esac
