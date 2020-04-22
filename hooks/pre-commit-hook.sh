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


#####
echo "## Security"
SECONDS=0
security="$(poetry run bandit -r $main_module/ -o hooks/reports/bandit)"
duration=$SECONDS
security_exit_code=$?
echo "$security"
echo "total    $(($duration / 60))m$(($duration % 60))s"
if [[ ! $security_exit_code == 0 ]]; then
  echo "security issues found"
  exit 1
fi

time poetry run pip freeze | poetry run safety check --stdin --cache >> hooks/reports/safety

