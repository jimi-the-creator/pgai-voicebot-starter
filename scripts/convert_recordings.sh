#!/usr/bin/env bash
set -euo pipefail

mkdir -p calls/recordings/converted

for f in calls/recordings/*; do
  [ -f "$f" ] || continue
  base="$(basename "$f")"
  name="${base%.*}"

  case "$f" in
    *.mp3|*.ogg)
      echo "Already acceptable: $f"
      ;;
    *)
      echo "Converting $f -> calls/recordings/converted/$name.mp3"
      ffmpeg -y -i "$f" "calls/recordings/converted/$name.mp3"
      ;;
  esac
done
