import React from 'react';
import {Composition} from 'remotion';
import {HeroLoop} from './HeroLoop';
import {ProcessSteps} from './ProcessSteps';
export const Root: React.FC = () => (
  <>
    <Composition id="HeroLoop" component={HeroLoop} durationInFrames={288} fps={24} width={1600} height={900} />
    <Composition id="ProcessSteps" component={ProcessSteps} durationInFrames={300} fps={30} width={1600} height={240} />
  </>
);
