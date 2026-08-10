#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "Building Linux executable..."
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o numerology_linux

echo "Build complete: ./numerology_linux"
