#!/usr/bin/env bash

# for debugging call `./.git/hooks/pre-commit`

# Keep in mind: these checks (or parts of it) can also be run in your CI-pipeline
# There is no need to run them on every commit with a CI-server checking on every push

main_module="samplemlproject"

project_dir="$(
  cd "$(dirname "$0")/../.."
  pwd -P
)"
cd "$project_dir"

#####
echo "## Formatting"
time poetry run black "$main_module"

