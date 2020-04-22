#!/usr/bin/env bash

project_dir="$( cd "$(dirname "$0")/.." ; pwd -P )"
cd "$project_dir"

hook_file="$project_dir/.git/hooks/pre-commit"


if [[ -f "$hook_file" ]]; then
    rm "$hook_file"
fi

ln -s "$project_dir/hooks/pre-commit-hook.sh" "$hook_file"
