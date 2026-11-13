const fs = require('fs');
const path = require('path');
const os = require('os');
let PptxGenJS;
try { PptxGenJS = require('pptxgenjs'); }
catch { PptxGenJS = require(path.join(os.tmpdir(), 'ld3-presentation-deps', 'node_modules', 'pptxgenjs')); }

const ROOT = path.resolve(__dirname, '..');
const OUT = __dirname;
const FIG = path.join(ROOT, 'figuras');
const EVD = path.join(FIG, 'evidencias_ltspice');
const ACT = path.join(OUT, 'activos');
// Official marks: UNMSM (unmsm.edu.pe/img/logos/Logos%20UNMSM.zip) and
// FIEE (fiee.unmsm.edu.pe/images/home/logo_fiee.png); cropped only to visible bounds.
const LOGO_UNMSM = path.join(ACT, 'logo_unmsm.png');
const LOGO_FIEE = path.join(ACT, 'logo_fiee.png');
const PPTX_FILE = path.join(OUT, 'LD3_IGBT_Yactayo.pptx');

const pptx = new PptxGenJS();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Leonardo Sait Yactayo Tolentino';
pptx.subject = 'Laboratorio Dirigido N.° 3 — Caracterización y simulación comparativa de IGBT';
pptx.title = 'Caracterización y simulación comparativa de transistores IGBT en LTspice';
pptx.company = 'Universidad Nacional Mayor de San Marcos — FIEE';
pptx.lang = 'es-PE';
pptx.theme = {
  headFontFace: 'Aptos Display',
  bodyFontFace: 'Aptos',
  lang: 'es-PE'
};

const W = 13.333;
const H = 7.5;
const C = {
  navy: '10253F',
  navy2: '183A5A',
  ink: '1B2F45',
  muted: '5F7287',
  bg: 'F4F7FA',
  white: 'FFFFFF',
  line: 'D9E2EA',
  teal: '008A96',
  tealLight: 'E3F2F2',
  blue: '3178A6',
  blueLight: 'E9F1F8',
  amber: 'D49A32',
  amberLight: 'FBF3E1',
  red: 'C95C55',
  green: '3C8B70',
  purpleLight: 'F1EAF3',
  pBody: 'EADDEB',
  drift: 'DCEBF2',
  emitter: 'D9ECE4',
  collector: 'F2DEDB'
};
const FONT = 'Aptos';
const HEAD = 'Aptos Display';

function addText(slide, text, x, y, w, h, opts = {}) {
  slide.addText(text, {
    x, y, w, h,
    fontFace: opts.fontFace || FONT,
    fontSize: opts.fontSize || 16,
    color: opts.color || C.ink,
    bold: Boolean(opts.bold),
    margin: opts.margin === undefined ? 0 : opts.margin,
    breakLine: false,
    fit: 'shrink',
    valign: opts.valign || 'mid',
    align: opts.align || 'left',
    paraSpaceAfterPt: 0,
    charSpacing: opts.charSpacing || 0,
    italic: Boolean(opts.italic),
    isTextBox: true,
    ...opts
  });
}

function rect(slide, x, y, w, h, fill, line = fill, radius = true, transparency = 0) {
  slide.addShape(radius ? pptx.ShapeType.roundRect : pptx.ShapeType.rect, {
    x, y, w, h,
    rectRadius: 0.08,
    fill: { color: fill, transparency },
    line: { color: line, width: line === fill ? 0.6 : 1 }
  });
}

function rule(slide, x1, y1, x2, y2, color = C.line, width = 1.2, dash, endArrowType) {
  const x = Math.min(x1, x2);
  const y = Math.min(y1, y2);
  const w = Math.abs(x2 - x1) || 0.001;
  const h = Math.abs(y2 - y1) || 0.001;
  const reversed = (x2 < x1) !== (y2 < y1);
  slide.addShape(pptx.ShapeType.line, {
    x, y, w, h,
    flipV: reversed,
    line: { color, width, dashType: dash, endArrowType }
  });
}

function addImageFit(slide, imagePath, x, y, w, h) {
  const data = fs.readFileSync(imagePath);
  const iw = data.readUInt32BE(16);
  const ih = data.readUInt32BE(20);
  const aspect = iw / ih;
  let dw = w;
  let dh = w / aspect;
  if (dh > h) {
    dh = h;
    dw = h * aspect;
  }
  slide.addImage({ path: imagePath, x: x + (w - dw) / 2, y: y + (h - dh) / 2, w: dw, h: dh });
}

function bg(slide, color = C.bg) {
  slide.background = { color };
}

function header(slide, n, title, subtitle = '') {
  addText(slide, title, 0.58, 0.34, 12.1, 0.54, {
    fontFace: HEAD, fontSize: 27.5, bold: true, color: C.navy
  });
  if (subtitle) addText(slide, subtitle, 0.6, 0.9, 12.0, 0.3, { fontSize: 11.5, color: C.muted });
  rule(slide, 0.58, 7.13, 12.75, 7.13, C.line, 0.7);
  addText(slide, 'LD3 · IGBT · UNMSM FIEE', 0.6, 7.18, 4.0, 0.16, { fontSize: 8.5, color: C.muted });
  addText(slide, String(n).padStart(2, '0'), 12.22, 7.16, 0.5, 0.2, {
    fontSize: 9, color: C.muted, align: 'right'
  });
}

function tag(slide, label, x, y, w, fill = C.tealLight, color = C.teal) {
  rect(slide, x, y, w, 0.28, fill, fill, true);
  addText(slide, label, x + 0.09, y + 0.01, w - 0.18, 0.25, {
    fontSize: 9.5, bold: true, color, charSpacing: 0.5, align: 'center'
  });
}

function drawCoverCircuit(slide, x, y) {
  const white = 'D8E5EF';
  const active = '4ABAC3';
  // Compact editable DPT motif, drawn as simple circuit blocks and conductors.
  rule(slide, x + 0.25, y + 0.55, x + 2.35, y + 0.55, white, 1.8);
  rule(slide, x + 0.25, y + 0.55, x + 0.25, y + 2.45, white, 1.8);
  rule(slide, x + 2.35, y + 0.55, x + 2.35, y + 2.45, white, 1.8);
  rule(slide, x + 0.25, y + 2.45, x + 2.35, y + 2.45, white, 1.8);
  rect(slide, x + 0.75, y + 0.28, 1.15, 0.54, C.navy2, active, true);
  addText(slide, 'L  ·  DPT', x + 0.82, y + 0.34, 1.0, 0.4, { fontSize: 12, color: white, bold: true, align: 'center' });
  rect(slide, x + 0.92, y + 1.48, 0.85, 0.8, C.navy2, active, true);
  addText(slide, 'IGBT', x + 0.96, y + 1.65, 0.77, 0.42, { fontSize: 12, color: white, bold: true, align: 'center' });
  rule(slide, x + 0.25, y + 1.87, x + 0.92, y + 1.87, active, 2.2);
  rule(slide, x + 1.34, y + 2.28, x + 1.34, y + 2.45, active, 2.2);
  addText(slide, 'SWITCHING  /  WAVEFORMS', x + 0.26, y + 2.73, 2.1, 0.28, {
    fontSize: 9, color: 'A8BECE', bold: true, align: 'center', charSpacing: 0.6
  });
}

function drawCrossSection(slide, x, y, w) {
  // Simplified editable N-channel IGBT section: P+ collector / N- drift / P-body / N+ emitter.
  addText(slide, 'Corte conceptual · N-IGBT', x, y, w, 0.28, { fontSize: 11, bold: true, color: C.muted });
  const left = x + 0.22;
  const bodyW = w - 0.44;
  const bodyY = y + 1.02;
  rect(slide, left, bodyY, bodyW, 0.58, C.pBody, C.pBody, false);
  addText(slide, 'P-body', left + 1.17, bodyY + 0.17, bodyW - 2.34, 0.2, { fontSize: 10.5, color: C.ink, bold: true, align: 'center' });
  rect(slide, left + 0.16, bodyY + 0.03, 0.84, 0.25, C.emitter, C.emitter, false);
  rect(slide, left + bodyW - 1.0, bodyY + 0.03, 0.84, 0.25, C.emitter, C.emitter, false);
  addText(slide, 'N+', left + 0.2, bodyY + 0.04, 0.76, 0.2, { fontSize: 9.5, bold: true, color: C.green, align: 'center' });
  addText(slide, 'N+', left + bodyW - 0.96, bodyY + 0.04, 0.76, 0.2, { fontSize: 9.5, bold: true, color: C.green, align: 'center' });
  rect(slide, left + 1.15, y + 0.56, bodyW - 2.3, 0.23, C.navy2, C.navy2, false);
  addText(slide, 'G', left + 1.15, y + 0.3, bodyW - 2.3, 0.22, { fontSize: 10.5, color: C.navy2, bold: true, align: 'center' });
  rect(slide, left + 1.15, y + 0.81, bodyW - 2.3, 0.07, C.amber, C.amber, false);
  addText(slide, 'SiO₂', left + 1.15, y + 0.88, bodyW - 2.3, 0.16, { fontSize: 8.5, color: C.amber, align: 'center' });
  rect(slide, left, bodyY + 0.58, bodyW, 1.28, C.drift, C.drift, false);
  addText(slide, 'N⁻ drift · portadores almacenados', left + 0.12, bodyY + 0.98, bodyW - 0.24, 0.28, {
    fontSize: 10.2, color: C.blue, bold: true, align: 'center'
  });
  rect(slide, left, bodyY + 1.86, bodyW, 0.35, C.collector, C.collector, false);
  addText(slide, 'P+ collector', left + 0.1, bodyY + 1.91, bodyW - 0.2, 0.22, { fontSize: 10, color: C.red, bold: true, align: 'center' });
  addText(slide, 'Al apagar, el canal se cierra antes de que desaparezca toda la carga en la región de deriva.', x, y + 3.48, w, 0.4, {
    fontSize: 11, color: C.ink, valign: 'top', breakLine: false
  });
  rect(slide, x, y + 3.96, w, 0.82, C.amberLight, C.amberLight, true);
  addText(slide, 'CORRIENTE DE COLA', x + 0.15, y + 4.04, w - 0.3, 0.2, { fontSize: 9, color: C.amber, bold: true, charSpacing: 0.5 });
  addText(slide, 'Portadores minoritarios remanentes se extraen y recombinan; IC decae gradualmente.', x + 0.15, y + 4.27, w - 0.3, 0.39, { fontSize: 10.8, color: C.ink, valign: 'top' });
}

function drawDptCard(slide, x, y, w, h, polarity) {
  const isN = polarity === 'N';
  rect(slide, x, y, w, h, C.white, C.line, true);
  addText(slide, isN ? 'DPT · N · lado bajo' : 'DPT · P · lado alto', x + 0.16, y + 0.13, w - 0.32, 0.3, {
    fontSize: 13, bold: true, color: C.navy, align: 'center'
  });
  const railY = y + 0.75;
  if (isN) {
    // N low-side: +bus -> load inductor -> collector; emitter shunt returns to ground.
    rect(slide, x + 0.2, railY, 0.72, 0.56, C.blueLight, C.blueLight, true);
    addText(slide, '+400 V', x + 0.23, railY + 0.08, 0.66, 0.4, { fontSize: 10.2, color: C.blue, bold: true, align: 'center' });
    rect(slide, x + 1.02, railY, 1.05, 0.56, C.tealLight, C.tealLight, true);
    addText(slide, 'Lload\n100 µH', x + 1.08, railY + 0.04, 0.93, 0.47, { fontSize: 10, color: C.teal, bold: true, align: 'center' });
    rect(slide, x + 2.18, railY, 0.9, 0.56, C.blueLight, C.blueLight, true);
    addText(slide, 'Q_N\nlow-side', x + 2.22, railY + 0.04, 0.82, 0.47, { fontSize: 9.6, color: C.blue, bold: true, align: 'center' });
    rule(slide, x + 0.92, railY + 0.28, x + 1.02, railY + 0.28, C.muted, 1.2, undefined, 'triangle');
    rule(slide, x + 2.07, railY + 0.28, x + 2.18, railY + 0.28, C.muted, 1.2, undefined, 'triangle');
    rule(slide, x + 2.63, railY + 0.56, x + 2.63, y + 2.04, C.muted, 1.1);
    rect(slide, x + 2.14, y + 2.04, 0.98, 0.43, C.bg, C.line, true);
    addText(slide, 'R2 1 mΩ\n→ referencia', x + 2.19, y + 2.07, 0.88, 0.36, { fontSize: 8.7, color: C.ink, align: 'center' });
  } else {
    // P high-side: reference/shunt -> emitter -> collector -> load -> negative bus.
    rect(slide, x + 0.2, railY, 0.88, 0.56, C.bg, C.line, true);
    addText(slide, 'R2 1 mΩ\nreferencia', x + 0.24, railY + 0.04, 0.8, 0.47, { fontSize: 8.9, color: C.ink, bold: true, align: 'center' });
    rect(slide, x + 1.2, railY, 0.88, 0.56, C.blueLight, C.blueLight, true);
    addText(slide, 'Q_P\nhigh-side', x + 1.24, railY + 0.04, 0.8, 0.47, { fontSize: 9.6, color: C.blue, bold: true, align: 'center' });
    rect(slide, x + 2.2, railY, 1.03, 0.56, C.tealLight, C.tealLight, true);
    addText(slide, 'Lload 100 µH\n→ −400 V', x + 2.25, railY + 0.04, 0.93, 0.47, { fontSize: 9.2, color: C.teal, bold: true, align: 'center' });
    rule(slide, x + 1.08, railY + 0.28, x + 1.2, railY + 0.28, C.muted, 1.2, undefined, 'triangle');
    rule(slide, x + 2.08, railY + 0.28, x + 2.2, railY + 0.28, C.muted, 1.2, undefined, 'triangle');
  }
  addText(slide, 'D1 // Lload', x + 0.26, y + 1.42, isN ? 1.65 : w - 0.52, 0.28, { fontSize: 9.4, color: C.muted, italic: true, align: isN ? 'left' : 'center' });
  // Gate-drive branch is labeled separately from the collector current path.
  rect(slide, x + 0.3, y + 2.58, w - 0.6, 0.37, C.amberLight, C.amberLight, true);
  addText(slide, isN ? 'Drive G(Q): RG 10 Ω · VGE 0 → +15 V' : 'Drive G(Q): RG 10 Ω · VGE 0 → −15 V', x + 0.38, y + 2.62, w - 0.76, 0.28, {
    fontSize: 9.2, color: C.amber, bold: true, align: 'center'
  });
  addText(slide, isN ? 'Pulso 1: establece I(L); pulso 2: apagado.' : 'Banco P de doble pulso con polaridad invertida.', x + 0.2, y + 3.0, w - 0.4, 0.24, {
    fontSize: 8.8, color: C.muted, align: 'center'
  });
}

function metricCard(slide, x, y, w, h, label, value, accent = C.teal, fill = C.white, small = '') {
  rect(slide, x, y, w, h, fill, fill, true);
  rect(slide, x, y + 0.08, 0.055, h - 0.16, accent, accent, false);
  addText(slide, label.toUpperCase(), x + 0.18, y + 0.08, w - 0.32, 0.18, { fontSize: 8.8, color: C.muted, bold: true, charSpacing: 0.4 });
  addText(slide, value, x + 0.18, y + 0.29, w - 0.32, 0.48, { fontSize: 22, color: accent, bold: true });
  if (small) addText(slide, small, x + 0.18, y + h - 0.29, w - 0.32, 0.2, { fontSize: 8.8, color: C.muted });
}

// 1 — Cover.
{
  const s = pptx.addSlide();
  bg(s, C.navy);
  s.background = { color: C.navy };
  rect(s, 0, 0, W, 1.36, 'F8FAFC', 'F8FAFC', false);
  rect(s, 0.12, 1.35, W - 0.12, 0.015, C.line, C.line, false);
  rect(s, 0, 0, 0.12, H, C.teal, C.teal, false);
  addImageFit(s, LOGO_UNMSM, 0.65, 0.16, 3.38, 1.04);
  addImageFit(s, LOGO_FIEE, 10.85, 0.06, 1.85, 1.24);
  rect(s, 0.82, 1.56, 2.8, 0.37, C.navy2, C.navy2, true);
  addText(s, 'LABORATORIO DIRIGIDO N.º 3', 0.98, 1.61, 2.48, 0.25, { fontSize: 10.5, color: 'D3EEF0', bold: true, charSpacing: 0.65, align: 'center' });
  addText(s, 'Caracterización y simulación\ncomparativa de transistores IGBT\nen LTspice', 0.82, 2.1, 8.4, 2.03, {
    fontFace: HEAD, fontSize: 30.5, bold: true, color: C.white, valign: 'top', breakLine: false
  });
  rule(s, 0.84, 4.35, 7.9, 4.35, C.teal, 2.3);
  addText(s, 'Microelectrónica y Sistemas Nanoelectrónicos  ·  Semestre 2026-II', 0.84, 4.52, 7.9, 0.34, {
    fontSize: 14, color: 'C4D4DF'
  });
  rect(s, 0.82, 5.2, 7.72, 1.2, '18334F', '294660', true);
  addText(s, 'DOCENTE', 1.05, 5.38, 1.2, 0.18, { fontSize: 8.8, color: '82A9BC', bold: true, charSpacing: 0.5 });
  addText(s, 'MsC. Luz Adanaqué Infante', 1.05, 5.61, 3.1, 0.33, { fontSize: 13.3, color: C.white, bold: true });
  addText(s, 'ESTUDIANTE · AUTOR INDIVIDUAL', 4.45, 5.38, 3.65, 0.18, { fontSize: 8.8, color: '82A9BC', bold: true, charSpacing: 0.35 });
  addText(s, 'Leonardo Sait Yactayo Tolentino  ·  23190214', 4.45, 5.61, 3.75, 0.42, { fontSize: 11.5, color: C.white, bold: true });
  addText(s, '21 de octubre de 2026', 0.84, 6.75, 4.0, 0.3, { fontSize: 12.5, color: 'A7BECC', bold: true });
  drawCoverCircuit(s, 9.75, 2.08);
  addText(s, 'DPT  ·  VGE  ·  VCE  ·  IC', 9.7, 5.25, 2.55, 0.33, { fontSize: 10.5, color: 'A7BECC', align: 'center', charSpacing: 0.3 });
  addText(s, 'RESULTADOS Y MODELOS LTSPICE', 9.45, 6.35, 3.0, 0.25, { fontSize: 9, color: '7895A9', bold: true, charSpacing: 0.7, align: 'center' });
}

// 2 — Physical basis and DPT method.
{
  const s = pptx.addSlide(); bg(s);
  header(s, 2, 'Fundamento y metodología DPT', 'Del transporte de portadores a la medición de conmutación en las dos polaridades.');
  rect(s, 0.55, 1.35, 4.45, 5.55, C.white, C.line, true);
  tag(s, 'ESTRUCTURA Y FÍSICA', 0.77, 1.55, 1.85);
  drawCrossSection(s, 0.78, 1.86, 4.0);
  rect(s, 5.22, 1.35, 7.56, 5.55, C.white, C.line, true);
  tag(s, 'ESQUEMAS DE PRUEBA DPT', 5.45, 1.55, 2.72);
  drawDptCard(s, 5.45, 1.95, 3.48, 3.36, 'N');
  drawDptCard(s, 9.1, 1.95, 3.43, 3.36, 'P');
  rect(s, 5.45, 5.52, 7.08, 1.02, C.bg, C.bg, true);
  addText(s, 'DUNCAN · N/P', 5.67, 5.68, 1.45, 0.19, { fontSize: 9, color: C.blue, bold: true, charSpacing: 0.3 });
  addText(s, '400 V · 100 µH · RG 10 Ω · 27 °C · Lσ = 0 nH', 7.18, 5.64, 5.08, 0.28, { fontSize: 10.5, color: C.ink, bold: true });
  addText(s, 'FUJI SERIE X', 5.67, 6.02, 1.45, 0.19, { fontSize: 9, color: C.teal, bold: true, charSpacing: 0.3 });
  addText(s, '400 V · 100 µH · Lσ = 25 nH · 25 °C · RG 10/20 Ω', 7.18, 5.98, 5.08, 0.28, { fontSize: 10.2, color: C.ink, bold: true });
  addText(s, 'Primer pulso: establece corriente en L. Segundo pulso: observa el apagado.', 5.67, 6.31, 6.6, 0.18, { fontSize: 9.2, color: C.muted });
}

// 3 — Duncan nominal N/P results.
{
  const s = pptx.addSlide(); bg(s);
  header(s, 3, 'Duncan N/P: señales y corrientes nominales', 'Las tres trazas del DPT son visibles en paneles sincronizados; las corrientes de referencia son distintas.');
  tag(s, 'N-IGBT · 19 A', 1.95, 1.28, 1.65, C.blueLight, C.blue);
  tag(s, 'P-IGBT · 40 A', 9.72, 1.28, 1.65, C.purpleLight, '76527E');
  addImageFit(s, path.join(FIG, 'fig1_dpt_nigbt_transitorios.png'), 0.58, 1.62, 6.02, 4.48);
  addImageFit(s, path.join(FIG, 'fig2_dpt_pigbt_transitorios.png'), 6.75, 1.62, 6.02, 4.48);
  rect(s, 0.67, 6.15, 5.9, 0.44, C.blueLight, C.blueLight, true);
  addText(s, 'VCE(on)  1.88 V     ·     Eoff  691.5 µJ', 0.84, 6.23, 5.55, 0.26, { fontSize: 13, color: C.blue, bold: true, align: 'center' });
  rect(s, 6.78, 6.15, 5.9, 0.44, C.purpleLight, C.purpleLight, true);
  addText(s, 'VCE(on)  2.51 V     ·     Eoff  2115.3 µJ', 6.95, 6.23, 5.55, 0.26, { fontSize: 13, color: '76527E', bold: true, align: 'center' });
  addText(s, 'No es una comparación a corriente idéntica: 19 A frente a 40 A. Control P a 19,48 A: Eoff = 1011,8 µJ confirmados en log; métricas dinámicas no verificadas sin RAW.', 0.66, 6.66, 12.05, 0.3, { fontSize: 9.4, color: C.muted, align: 'center' });
}

// 4 — Turn-off cursors, tail and operational energy.
{
  const s = pptx.addSlide(); bg(s);
  header(s, 4, 'Apagado: cursores reales y corriente de cola', 'td(off): intervalo entre 90 % de VGE y 90 % de IC. Evidencias LTspice conservadas.');
  rect(s, 0.55, 1.3, 7.78, 3.23, C.white, C.line, true);
  addImageFit(s, path.join(FIG, 'fig3_detalle_corriente_cola.png'), 0.66, 1.36, 7.56, 3.06);
  rect(s, 8.52, 1.3, 4.25, 3.23, C.white, C.line, true);
  metricCard(s, 8.73, 1.5, 3.83, 0.82, 'N · cursor LTspice', '150,81 ns', C.blue, C.blueLight);
  metricCard(s, 8.73, 2.42, 3.83, 0.82, 'P · cursor LTspice', '194,37 ns', '76527E', C.purpleLight);
  addText(s, 'El log automatizado reporta 194,57 ns (.meas).', 8.9, 3.28, 3.5, 0.2, { fontSize: 9, color: C.muted });
  metricCard(s, 8.73, 3.54, 3.83, 0.78, 'N · integral de apagado', '691,48 µJ', C.teal, C.tealLight);
  addText(s, 'No equivale directamente al calor interno.', 8.72, 4.32, 3.65, 0.18, { fontSize: 8.3, color: C.muted });
  const proof = [
    ['E03_cursor_zoom.png', 'N · cursores: 150,81081 ns', 'E03'],
    ['E04_cursor_zoom.png', 'P · cursores: 194,3662 ns', 'E04'],
    ['E05_energia_zoom.png', 'Integral LTspice: 691,48 µJ', 'E05']
  ];
  proof.forEach((item, i) => {
    const x = 0.55 + i * 4.09;
    rect(s, x, 4.76, 3.92, 2.12, C.white, C.line, true);
    tag(s, item[2] + ' · EVIDENCIA ORIGINAL', x + 0.13, 4.89, 2.05, C.bg, C.muted);
    addImageFit(s, path.join(EVD, item[0]), x + 0.16, 5.23, 3.6, 1.32);
    addText(s, item[1], x + 0.18, 6.57, 3.55, 0.19, { fontSize: 9.1, color: C.ink, bold: true, align: 'center' });
  });
}

// 5 — Fuji parasitic overshoot and co-pack diode.
{
  const s = pptx.addSlide(); bg(s);
  header(s, 5, 'Fuji Serie X: inductancia de lazo y co-pack', 'Lσ = 25 nH · bus de 400 V · formas VCE de modelos discreto y co-pack.');
  rect(s, 0.55, 1.32, 6.08, 2.45, C.white, C.line, true);
  addImageFit(s, path.join(ACT, 'fig6_vce50_crop.png'), 0.67, 1.45, 5.84, 2.18);
  rect(s, 6.77, 1.32, 6.0, 2.45, C.white, C.line, true);
  addImageFit(s, path.join(ACT, 'fig7_vce75_crop.png'), 6.88, 1.45, 5.78, 2.18);
  rect(s, 0.55, 4.02, 5.9, 2.83, C.white, C.line, true);
  tag(s, 'PICOS MEDIDOS · F01/F03', 0.79, 4.22, 2.28, C.blueLight, C.blue);
  addText(s, '50 A', 0.85, 4.78, 1.25, 0.3, { fontSize: 13, color: C.muted, bold: true });
  addText(s, '442,36 V', 2.05, 4.7, 2.0, 0.47, { fontSize: 24, color: C.blue, bold: true });
  addText(s, '+42,36 V sobre bus', 4.06, 4.82, 1.93, 0.26, { fontSize: 10.8, color: C.ink, bold: true });
  rule(s, 0.83, 5.35, 6.12, 5.35, C.line, 0.8);
  addText(s, '75 A', 0.85, 5.58, 1.25, 0.3, { fontSize: 13, color: C.muted, bold: true });
  addText(s, '445,98 V', 2.05, 5.49, 2.0, 0.47, { fontSize: 24, color: C.blue, bold: true });
  addText(s, '+45,98 V sobre bus', 4.06, 5.61, 1.93, 0.26, { fontSize: 10.8, color: C.ink, bold: true });
  addText(s, 'VCE,peak = Vbus + Lσ · |diC/dt|.', 0.83, 6.28, 5.28, 0.35, { fontSize: 10.4, color: C.muted, valign: 'top' });
  rect(s, 6.7, 4.02, 6.07, 2.83, C.tealLight, C.tealLight, true);
  tag(s, 'LECTURA DEL CO-PACK', 6.94, 4.22, 2.07, C.white, C.teal);
  addText(s, 'En este DPT low-side, el diodo co-pack queda polarizado en inversa durante el apagado. La rueda libre la conduce D1; por eso F01/F02 y F03/F04 casi se superponen.', 6.96, 4.7, 5.48, 1.02, { fontSize: 13.1, color: C.ink, valign: 'top' });
  rule(s, 6.95, 5.82, 12.46, 5.82, 'B9D9D9', 0.8);
  addText(s, 'En un medio puente, el diodo sí puede llevar la corriente reactiva al conmutar el dispositivo opuesto.', 6.96, 5.99, 5.47, 0.56, { fontSize: 11.3, color: C.teal, bold: true, valign: 'top' });
}

// 6 — Chip area and gate resistance trade-offs.
{
  const s = pptx.addSlide(); bg(s);
  header(s, 6, 'Área de chip y resistencia de compuerta', 'Comparaciones controladas dentro de la familia Fuji; misma corriente para F01/F05 y F02/F06.');
  rect(s, 0.55, 1.35, 6.1, 5.53, C.white, C.line, true);
  addImageFit(s, path.join(FIG, 'fig8_comparativa_area_50vs75.png'), 0.68, 1.47, 5.84, 5.28);
  rect(s, 6.86, 1.35, 5.92, 1.95, C.white, C.line, true);
  tag(s, 'F01 vs F05 · MISMA CORRIENTE: 50 A', 7.07, 1.54, 3.18, C.blueLight, C.blue);
  addText(s, 'Chip 50 A → 75 A', 7.08, 1.93, 2.4, 0.29, { fontSize: 14, color: C.navy, bold: true });
  addText(s, 'VCE(on)  1,362 → 1,181 V', 7.08, 2.27, 3.35, 0.27, { fontSize: 12.5, color: C.ink, bold: true });
  addText(s, 'Eoff  1066,98 → 1367,85 µJ  (+28,2 %)', 7.08, 2.59, 5.35, 0.28, { fontSize: 12.1, color: C.ink, bold: true });
  addText(s, 'Menor caída en conducción; mayor energía de apagado.', 7.08, 2.93, 5.24, 0.22, { fontSize: 10.1, color: C.muted });
  rect(s, 6.86, 3.42, 5.92, 1.02, C.amberLight, C.amberLight, true);
  addText(s, 'F02 → F06  ·  RG 10 → 20 Ω', 7.08, 3.55, 3.62, 0.29, { fontSize: 14, color: C.navy, bold: true });
  addText(s, 'Eoff +70,5 %', 10.0, 3.49, 2.48, 0.43, { fontSize: 22, color: C.amber, bold: true, align: 'right' });
  addText(s, 'Sobretensión +42,36 → +25,94 V (−38,8 %)', 7.08, 3.94, 5.2, 0.28, { fontSize: 11.5, color: C.ink, bold: true });
  rect(s, 6.86, 4.57, 5.92, 2.31, C.white, C.line, true);
  addImageFit(s, path.join(ACT, 'fig9_rg_current_crop.png'), 6.98, 4.66, 5.68, 2.13);
}

// 7 — Conclusions.
{
  const s = pptx.addSlide(); bg(s);
  header(s, 7, 'Conclusiones: cuatro hallazgos de diseño', 'Los resultados conectan física del dispositivo, topología y velocidad de conmutación.');
  const cards = [
    { x: 0.65, y: 1.52, color: C.blue, fill: C.blueLight, num: '01', title: 'La cola persiste tras cerrar el canal', body: 'Portadores almacenados en N⁻ drift sostienen una corriente decreciente durante el apagado.' },
    { x: 6.82, y: 1.52, color: '76527E', fill: C.purpleLight, num: '02', title: 'La comparación N/P requiere cautela', body: 'Los nominales son 19 A y 40 A. En P a 19,48 A, Eoff está registrado; métricas dinámicas siguen no verificadas sin RAW.' },
    { x: 0.65, y: 4.06, color: C.teal, fill: C.tealLight, num: '03', title: 'Lσ y el co-pack dependen del circuito', body: 'Con 25 nH aparecen +42 a +46 V; en el low-side el co-pack no altera de forma apreciable el apagado.' },
    { x: 6.82, y: 4.06, color: C.amber, fill: C.amberLight, num: '04', title: 'RG intercambia rapidez por energía', body: 'Duplicar RG reduce 38,8 % la sobretensión, pero sube Eoff 70,5 % en F02/F06.' }
  ];
  cards.forEach(c => {
    rect(s, c.x, c.y, 5.84, 2.18, C.white, C.line, true);
    rect(s, c.x + 0.22, c.y + 0.22, 0.54, 0.48, c.fill, c.fill, true);
    addText(s, c.num, c.x + 0.22, c.y + 0.28, 0.54, 0.34, { fontSize: 12, color: c.color, bold: true, align: 'center' });
    addText(s, c.title, c.x + 0.93, c.y + 0.22, 4.56, 0.47, { fontSize: 16.2, color: C.navy, bold: true, valign: 'top' });
    rule(s, c.x + 0.24, c.y + 0.86, c.x + 5.6, c.y + 0.86, C.line, 0.8);
    addText(s, c.body, c.x + 0.25, c.y + 1.04, 5.3, 0.88, { fontSize: 12.2, color: C.ink, valign: 'top' });
  });
  addText(s, 'El análisis caracteriza la respuesta de los macromodelos bajo las condiciones documentadas; no aísla movilidad microscópica como causa ni convierte la energía de puerto en disipación térmica interna.', 0.82, 6.55, 11.7, 0.35, { fontSize: 9.5, color: C.muted, italic: true, align: 'center' });
}

// 8 — Closing.
{
  const s = pptx.addSlide(); bg(s, C.navy);
  s.background = { color: C.navy };
  addText(s, 'Muchas gracias', 1.2, 2.45, W - 2.4, 0.78, {
    fontFace: HEAD, fontSize: 38, color: C.white, bold: true, align: 'center'
  });
  addText(s, 'Leonardo Sait Yactayo Tolentino', 1.2, 3.62, W - 2.4, 0.36, {
    fontSize: 18, color: 'D5E0E8', align: 'center'
  });
  addText(s, 'Microelectrónica y Sistemas Nanoelectrónicos', 1.2, 4.13, W - 2.4, 0.32, {
    fontSize: 14, color: 'AFC1CE', align: 'center'
  });
  addText(s, '21 de octubre de 2026', 1.2, 4.58, W - 2.4, 0.3, {
    fontSize: 14, color: 'AFC1CE', align: 'center'
  });
}

pptx.writeFile({ fileName: PPTX_FILE })
  .then(() => console.log(`Wrote ${PPTX_FILE}`))
  .catch(err => { console.error(err); process.exit(1); });
