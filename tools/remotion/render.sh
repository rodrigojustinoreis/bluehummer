#!/bin/bash
# Render brand motion for the site. Output: blue_hammer_remodeling_site/assets/video/
# Usage: cd tools/remotion && ./render.sh             (everything; needs `npm install` once)
#        cd tools/remotion && ./render.sh home-hero   (only the home hero carousel, 2026-11-20)
set -euo pipefail
cd "$(dirname "$0")"
OUT=../../blue_hammer_remodeling_site/assets/video
mkdir -p "$OUT"
E="src/index.ts"

# Home hero carousel (composition HomeHeroCarousel / HomeHeroCarouselMobile in src/HomeHeroCarousel.tsx).
# Sources: public/home-hero-*-1920.webp (copies of the published 1920 stills). No audio track, MP4 with
# +faststart (moov atom first). A keyframe at every slide start (every 165 frames = 5.5 s) so a seek to a
# slide lands on a keyframe. Masters go to out/ (gitignored).
render_home_hero() {
  mkdir -p out
  for v in "HomeHeroCarousel:1280" "HomeHeroCarouselMobile:720"; do
    id=${v%%:*}; w=${v##*:}
    # One near-lossless master per size from Remotion, then both delivery formats from it with ffmpeg.
    npx remotion render $E "$id" "out/home-hero-$w-master.mp4" --codec=h264 --crf=12 --pixel-format=yuv420p --muted --log=error
    ffmpeg -y -loglevel error -i "out/home-hero-$w-master.mp4" -an -c:v libx264 -preset veryslow -crf 29 -pix_fmt yuv420p \
      -g 165 -keyint_min 165 -sc_threshold 0 -force_key_frames "expr:eq(mod(n,165),0)" -movflags +faststart "$OUT/home-hero-$w.mp4"
    ffmpeg -y -loglevel error -i "out/home-hero-$w-master.mp4" -an -c:v libvpx-vp9 -crf 41 -b:v 0 -row-mt 1 -deadline good -cpu-used 1 \
      -g 165 -force_key_frames "expr:eq(mod(n,165),0)" "$OUT/home-hero-$w.webm"
  done
  ls -la "$OUT"/home-hero-*
}
if [ "${1:-all}" = "home-hero" ]; then render_home_hero; exit 0; fi

npx remotion render $E HeroLoop "$OUT/hero-loop.mp4"  --codec=h264 --crf=23 --pixel-format=yuv420p --muted --log=error
npx remotion render $E HeroLoop "$OUT/hero-loop.webm" --codec=vp9  --crf=34 --muted --log=error
npx remotion still  $E HeroLoop "$OUT/hero-loop-poster.jpg" --frame=0 --image-format=jpeg --jpeg-quality=80 --log=error
npx remotion render $E ProcessSteps "$OUT/process-steps.mp4"  --codec=h264 --crf=28 --pixel-format=yuv420p --muted --log=error
npx remotion render $E ProcessSteps "$OUT/process-steps.webm" --codec=vp9  --crf=40 --muted --log=error
npx remotion still  $E ProcessSteps "$OUT/process-steps-poster.jpg" --frame=250 --image-format=jpeg --jpeg-quality=85 --log=error
render_home_hero
ls -la "$OUT"
