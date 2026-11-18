import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
// Seamless hero loop over the illustrative craftsperson photo: a slow "breathing" push-in and
// drift (cosine, so the last frame meets the first). No text: the headline is live HTML.
export const HeroLoop: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames: T} = useVideoConfig();
  const w = 0.5 - 0.5 * Math.cos((2 * Math.PI * frame) / T); // 0 -> 1 -> 0
  const scale = 1.0 + 0.055 * w;
  const x = -1.1 * w; // percent, drifts toward the craftsperson
  const y = -0.6 * w;
  return (
    <AbsoluteFill style={{backgroundColor: '#F3EEE3', overflow: 'hidden'}}>
      <Img src={staticFile('hero-craftsman-1920.webp')} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: '62% 35%', transform: `translate(${x}%, ${y}%) scale(${scale})`, transformOrigin: '70% 40%'}} />
    </AbsoluteFill>
  );
};
