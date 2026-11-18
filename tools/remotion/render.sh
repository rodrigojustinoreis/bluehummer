#!/bin/bash
# Render brand motion for the site. Output: blue_hammer_remodeling_site/assets/video/
# Usage: cd tools/remotion && ./render.sh   (needs `npm install` once)
set -euo pipefail
cd "$(dirname "$0")"
OUT=../../blue_hammer_remodeling_site/assets/video
mkdir -p "$OUT"
E="src/index.ts"
npx remotion render $E HeroLoop "$OUT/hero-loop.mp4"  --codec=h264 --crf=23 --pixel-format=yuv420p --muted --log=error
npx remotion render $E HeroLoop "$OUT/hero-loop.webm" --codec=vp9  --crf=34 --muted --log=error
npx remotion still  $E HeroLoop "$OUT/hero-loop-poster.jpg" --frame=0 --image-format=jpeg --jpeg-quality=80 --log=error
npx remotion render $E ProcessSteps "$OUT/process-steps.mp4"  --codec=h264 --crf=28 --pixel-format=yuv420p --muted --log=error
npx remotion render $E ProcessSteps "$OUT/process-steps.webm" --codec=vp9  --crf=40 --muted --log=error
npx remotion still  $E ProcessSteps "$OUT/process-steps-poster.jpg" --frame=250 --image-format=jpeg --jpeg-quality=85 --log=error
ls -la "$OUT"
