import React from 'react';
import {Composition} from 'remotion';
import {HeroLoop} from './HeroLoop';
import {ProcessSteps} from './ProcessSteps';
import {HomeHeroCarousel, FPS, SLIDE, PHOTOS} from './HomeHeroCarousel';
export const Root: React.FC = () => (
  <>
    <Composition id="HeroLoop" component={HeroLoop} durationInFrames={288} fps={24} width={1600} height={900} />
    {/* Home hero carousel (Re-Bath-style hero, 2026-11-20): desktop matches the photo column of the hero
        (about 1.6:1 beside the consultation panel), phone matches the portrait full-width hero (720x944). */}
    <Composition id="HomeHeroCarousel" component={HomeHeroCarousel} durationInFrames={SLIDE * PHOTOS.length} fps={FPS} width={1280} height={800} defaultProps={{positions: ['50% 55%', '50% 55%', '50% 55%']}} />
    <Composition id="HomeHeroCarouselMobile" component={HomeHeroCarousel} durationInFrames={SLIDE * PHOTOS.length} fps={FPS} width={720} height={944} defaultProps={{positions: ['56% 50%', '62% 50%', '40% 50%']}} />
    <Composition id="ProcessSteps" component={ProcessSteps} durationInFrames={300} fps={30} width={1600} height={240} />
  </>
);
