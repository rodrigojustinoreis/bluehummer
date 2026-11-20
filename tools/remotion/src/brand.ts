import {continueRender, delayRender, staticFile} from 'remotion';
// Palette A (docs/brand.md). Keep in sync with site-src/assets/main.css.
export const C = {ivory: '#FBF8F2', navy: '#0B2347', navy2: '#071830', royal: '#1E4FA3', limestone: '#F3EEE3', line: '#E4DCCB', brass: '#A88B5A', accentText: '#7A6232', ink: '#14243D', muted: '#525D6B'};
const faces: [string, string, string, string][] = [
  ['Gambetta', 'fonts/gambetta-400.woff2', '400', 'normal'],
  ['Gambetta', 'fonts/gambetta-400-italic.woff2', '400', 'italic'],
  ['Switzer', 'fonts/switzer-500.woff2', '500', 'normal'],
  ['Switzer', 'fonts/switzer-700.woff2', '700', 'normal'],
];
let loaded = false;
export const loadBrandFonts = () => {
  if (loaded) return; loaded = true;
  const h = delayRender('brand fonts');
  Promise.all(faces.map(([fam, file, weight, style]) => {
    const f = new FontFace(fam, `url(${staticFile(file)}) format('woff2')`, {weight, style});
    return f.load().then((ff) => { (document.fonts as any).add(ff); });
  })).then(() => continueRender(h)).catch((e) => { console.error(e); continueRender(h); });
};
export const serif = '"Gambetta", Georgia, serif';
export const sans = '"Switzer", Helvetica, Arial, sans-serif';
