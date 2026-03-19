#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

NO_CACHE=false
if [[ "${1:-}" == "--no-cache" ]]; then
  NO_CACHE=true
fi

if command -v shasum >/dev/null 2>&1; then
  UNIQUE_ID="$(printf '%s' "${ROOT_DIR}:$(id -un)" | shasum -a 256 | awk '{print substr($1,1,10)}')"
else
  UNIQUE_ID="$(printf '%s' "${ROOT_DIR}:$(id -un)" | sha256sum | awk '{print substr($1,1,10)}')"
fi

BASE_IMAGE_REPO="valencia-mcp-base-${UNIQUE_ID}"
APP_IMAGE_REPO="valencia-mcp-server-${UNIQUE_ID}"
BASE_IMAGE_TAG="${BASE_IMAGE_REPO}:latest"
APP_IMAGE_TAG="${APP_IMAGE_REPO}:latest"

BUILD_FLAGS=()
if [[ "${NO_CACHE}" == "true" ]]; then
  BUILD_FLAGS+=(--no-cache)
fi

echo "Building base image: ${BASE_IMAGE_TAG}"
docker build "${BUILD_FLAGS[@]}" -f base.Dockerfile -t "${BASE_IMAGE_TAG}" .

echo "Building app image: ${APP_IMAGE_TAG}"
docker build "${BUILD_FLAGS[@]}" -f app.Dockerfile --build-arg "BASE_IMAGE=${BASE_IMAGE_TAG}" -t "${APP_IMAGE_TAG}" .

echo "Build complete."
echo "APP_IMAGE=${APP_IMAGE_TAG}"
