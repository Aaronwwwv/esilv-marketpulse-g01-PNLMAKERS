#!/usr/bin/env bash
# Compute the next semantic version from commit messages since the last tag.
# fix: -> PATCH, feat: -> MINOR, type!: -> MAJOR
set -euo pipefail

last_tag=$(git describe --tags --abbrev=0 --match "v*.*.*" 2>/dev/null || echo "v0.0.0")

if [ "$last_tag" = "v0.0.0" ]; then
  range="HEAD"
else
  range="${last_tag}..HEAD"
fi

messages=$(git log "$range" --pretty=format:%s)

version=${last_tag#v}
IFS=. read -r major minor patch <<< "$version"

if echo "$messages" | grep -qE '^[a-z]+(\(.+\))?!:'; then
  major=$((major + 1)); minor=0; patch=0
elif echo "$messages" | grep -qE '^feat(\(.+\))?:'; then
  minor=$((minor + 1)); patch=0
elif echo "$messages" | grep -qE '^fix(\(.+\))?:'; then
  patch=$((patch + 1))
else
  echo "No feat/fix commit since $last_tag: no release."
  echo "next=" >> "$GITHUB_OUTPUT"
  exit 0
fi

next="v${major}.${minor}.${patch}"
echo "Last tag: $last_tag -> next: $next"
echo "next=$next" >> "$GITHUB_OUTPUT"
