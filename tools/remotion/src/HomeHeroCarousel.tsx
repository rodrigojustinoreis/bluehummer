import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';

// Home hero carousel (2026-11-20). Pre-rendered to WebM/MP4 for the site; React never ships to the page.
// Timeline per slide i (SLIDE frames long): fully visible from i*SLIDE to i*SLIDE + SLIDE - FADE, then a soft
// crossfade into slide i+1. The last slide fades back into slide 0, so the loop is seamless and frame 0 is a
// clean slide 0. The site seeks to i*SLIDE/FPS (+ a few ms) for slide i: that frame is never mid-crossfade.
// Keep FPS / SLIDE / FADE and the per-slide positions in sync with data-slide-duration, data-fade and the
// pos / posPhone values in data-slides on the hero in site-src/pages/index.html.
export const FPS = 30;
export const SLIDE = 165; // 5.5 s
export const FADE = 18;   // 0.6 s
export const PHOTOS = [
  'home-hero-kitchen-gudakov-1920.webp',
  'home-hero-bath-beach-1920.webp',
  'home-hero-living-tosolini-1920.webp',
];

type Props = {positions: string[]};

const Slide: React.FC<{src: string; local: number; objectPosition: string}> = ({src, local, objectPosition}) => {
  // Very slow push: 1.000 -> 1.025 across the slide (and its fade-out). Starts at 1.0, so a seek lands on the
  // same framing as the static still.
  const scale = interpolate(local, [0, SLIDE + FADE], [1, 1.025], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <Img src={staticFile(src)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', objectPosition, transform: `scale(${scale})`, transformOrigin: objectPosition}} />
  );
};

export const HomeHeroCarousel: React.FC<Props> = ({positions}) => {
  const frame = useCurrentFrame();
  const n = PHOTOS.length;
  const i = Math.floor(frame / SLIDE) % n;
  const local = frame - i * SLIDE;
  const next = (i + 1) % n;
  const fadeStart = SLIDE - FADE;
  const nextOpacity = interpolate(local, [fadeStart, SLIDE], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: '#F6F3EE', overflow: 'hidden'}}>
      <Slide src={PHOTOS[i]} local={local} objectPosition={positions[i]} />
      {nextOpacity > 0 ? (
        <AbsoluteFill style={{opacity: nextOpacity}}>
          {/* the incoming slide starts at scale 1.0 (local 0) and keeps that framing through the fade */}
          <Slide src={PHOTOS[next]} local={0} objectPosition={positions[next]} />
        </AbsoluteFill>
      ) : null}
    </AbsoluteFill>
  );
};
