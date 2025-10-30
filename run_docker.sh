#!/bin/bash
# ------------------------------
# Uso:
#   ./run_docker.sh              -> lift the container normally
#   ./run_docker.sh -d           -> knocks down containers and packages.
# ------------------------------

set -e

show_help() {
  echo "Use: $0 [-d]"
  echo "  -d    Run 'docker-compose down -v' before starting."
  exit 0
}

if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  show_help
fi

if [[ "$1" == "-d" ]]; then
  echo "Knocking down containers and packages..."
  docker-compose down -v
  echo "Containers successfully removed."
fi

echo "Uploading containers..."
docker-compose up --build
exit 0
