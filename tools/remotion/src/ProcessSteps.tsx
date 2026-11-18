import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, Easing} from 'remotion';
import {C, loadBrandFonts} from './brand';
// "How a project runs": a brass line draws across four steps; each step's line icon draws in.
const STEPS = [
  {n: '1', t: 'Conversation & walkthrough', icon: 'M8 10h8M8 14h5M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12Z'},
  {n: '2', t: 'Design & selections', icon: 'M3 21l3.5-1 11-11-2.5-2.5-11 11L3 21ZM14 6l2.5 2.5M4 4h6M4 4v6'},
  {n: '3', t: 'Scope, price & permits', icon: 'M7 3h7l4 4v14H7V3ZM14 3v4h4M10 12h5M10 16h5'},
  {n: '4', t: 'Build & walk-through', icon: 'M14 4l6 6-3 3-6-6 3-3ZM11 7L3 15l3 3 8-8M4 21h7'},
];
const ease = Easing.bezier(0.22, 1, 0.36, 1);
// Animated header for the four-column steps list on the home page: icons above, a brass rule that
// draws across, a node per column. Labels stay in the HTML list below (no duplicated text).
export const ProcessSteps: React.FC = () => {
  loadBrandFonts();
  const f = useCurrentFrame();
  const W = 1600, lineY = 200, pad = 38; // 28px column padding at 1180px container width
  const draw = interpolate(f, [10, 200], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
  const out = interpolate(f, [268, 296], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const xs = STEPS.map((_, i) => (i === 0 ? 0 : i * (W / 4) + pad));
  return (
    <AbsoluteFill style={{backgroundColor: C.ivory}}>
      <div style={{position: 'absolute', left: 0, top: lineY, width: W, height: 1, background: C.line}} />
      <div style={{position: 'absolute', inset: 0, opacity: out}}>
        <div style={{position: 'absolute', left: 0, top: lineY - 1, width: W * draw, height: 3, background: C.brass}} />
        {STEPS.map((s, i) => {
          const at = 10 + (xs[i] / W) * 190; // frame when the rule reaches this column
          const p = interpolate(f, [at - 4, at + 44], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
          const dot = interpolate(f, [at - 2, at + 12], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
          const x = xs[i];
          return (
            <React.Fragment key={s.n}>
              <div style={{position: 'absolute', left: x + (i === 0 ? 0 : -9), top: lineY - 9, width: 18, height: 18, borderRadius: 9, background: C.ivory, border: `2px solid ${C.brass}`, transform: `scale(${dot})`}} />
              <div style={{position: 'absolute', left: x + (i === 0 ? 5 : -4), top: lineY - 4, width: 8, height: 8, borderRadius: 4, background: C.navy, opacity: dot}} />
              <svg viewBox="0 0 24 24" width={84} height={84} fill="none" stroke={C.navy} strokeWidth={0.9} strokeLinecap="round" strokeLinejoin="round"
                style={{position: 'absolute', left: x - 6, top: 70, opacity: Math.min(1, p * 1.4), transform: `translateY(${(1 - p) * 14}px)`}}>
                <path d={s.icon} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
              </svg>
            </React.Fragment>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
