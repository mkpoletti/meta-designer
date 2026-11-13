/* Meta Designer · céu 3D contínuo (Three.js): gradiente, sol, nuvens, partículas, estrelas e as telas do hero */
import * as THREE from "three";

const MD = window.MD || { hero: 0, ceu: 0, total: 0, rato: { x: 0, y: 0 } };
const S = window.SITE || {};
const canvas = document.getElementById("ceu");
const CEU_T0 = performance.now();
const reduzir = matchMedia("(prefers-reduced-motion: reduce)").matches;
const movel = innerWidth <= 760;
const fraco = movel || (navigator.deviceMemory && navigator.deviceMemory <= 4) || (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 4);
const lim = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const lerp = (a, b, t) => a + (b - a) * t;
const suave = (a, b, v) => { const t = lim((v - a) / (b - a)); return t * t * (3 - 2 * t); };

let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: !fraco, alpha: false, powerPreference: "high-performance" });
} catch (e) {
  document.documentElement.classList.add("sem-webgl");
  throw e;
}
renderer.setPixelRatio(Math.min(devicePixelRatio || 1, movel ? 1 : 1.5));
renderer.setSize(innerWidth, innerHeight, false);
renderer.outputColorSpace = THREE.SRGBColorSpace;

const cena = new THREE.Scene();
const camara = new THREE.PerspectiveCamera(50, innerWidth / innerHeight, 0.1, 1200);
cena.add(camara);

/* ── Paleta (manhã, meio-dia, fim de tarde, crepúsculo) ────── */
const PAL = [["#7DB8FF", "#DCEEFF"], ["#4A90F0", "#CFE6FF"], ["#F6B27A", "#FFE3C2"], ["#1C2B54", "#6D6A9C"]]
  .map((p) => p.map((h) => new THREE.Color(h)));
const NUVEM = ["#ffffff", "#ffffff", "#FFE6D2", "#8F8DB8"].map((h) => new THREE.Color(h));
const SOMBRA_NUVEM = ["#C9DEF7", "#BCD5F5", "#E9B39A", "#4A4F7E"].map((h) => new THREE.Color(h));
const SOL = ["#FFFDF4", "#FFFFFF", "#FFC27A", "#FF9C6B"].map((h) => new THREE.Color(h));
const corEm = (lista, v) => {
  const i = Math.min(lista.length - 2, Math.floor(v)), f = lim(v - i);
  return lista[i].clone().lerp(lista[i + 1], f);
};
const corPal = (v, k) => {
  const i = Math.min(2, Math.floor(v)), f = lim(v - i);
  return PAL[i][k].clone().lerp(PAL[i + 1][k], f);
};

/* ── Céu: esfera com gradiente vertical ────────────────────── */
const ceuMat = new THREE.ShaderMaterial({
  side: THREE.BackSide, depthWrite: false,
  uniforms: { topo: { value: PAL[0][0].clone() }, horizonte: { value: PAL[0][1].clone() }, solDir: { value: new THREE.Vector3(0.3, 0.4, -1).normalize() }, solCor: { value: SOL[0].clone() } },
  vertexShader: `varying vec3 vDir; void main(){ vDir = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }`,
  fragmentShader: `
    uniform vec3 topo; uniform vec3 horizonte; uniform vec3 solDir; uniform vec3 solCor; varying vec3 vDir;
    void main(){
      float y = clamp(vDir.y, -1.0, 1.0);
      float t = pow(clamp(y * 1.25 + 0.08, 0.0, 1.0), 0.75);
      vec3 c = mix(horizonte, topo, t);
      c = mix(c, horizonte * 1.02, smoothstep(0.0, -0.4, y));
      float s = max(dot(normalize(vDir), solDir), 0.0);
      c += solCor * (pow(s, 24.0) * 0.35 + pow(s, 4.0) * 0.08);
      gl_FragColor = vec4(c, 1.0);
      #include <colorspace_fragment>
    }`,
});
const ceu = new THREE.Mesh(new THREE.SphereGeometry(600, 32, 16), ceuMat);
camara.add(ceu); // acompanha a câmara: o céu está sempre "no infinito"

/* ── Texturas geradas (nuvem macia, brilho) ─────────────────── */
const rnd = (() => { let s = 7; return () => ((s = (s * 16807) % 2147483647) / 2147483647); })();
function texNuvem(seed) {
  const c = document.createElement("canvas"); c.width = c.height = 256;
  const g = c.getContext("2d");
  for (let k = 0; k < seed; k++) rnd();
  for (let i = 0; i < 60; i++) {
    const a = rnd() * Math.PI * 2, d = Math.pow(rnd(), 0.7);
    const x = 128 + Math.cos(a) * d * 78, y = 140 + Math.sin(a) * d * 38 - (1 - d) * 26;
    const r = 26 + rnd() * 34 * (1 - d * 0.5);
    const gr = g.createRadialGradient(x, y, 0, x, y, r);
    gr.addColorStop(0, "rgba(255,255,255,0.95)");
    gr.addColorStop(0.5, "rgba(255,255,255,0.7)");
    gr.addColorStop(1, "rgba(255,255,255,0)");
    g.fillStyle = gr; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill();
  }
  // sombra suave na base (o shader pinta-a com a cor de sombra)
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}
function texBrilho(stops) {
  const c = document.createElement("canvas"); c.width = c.height = 256;
  const g = c.getContext("2d");
  const gr = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  stops.forEach(([p, a]) => gr.addColorStop(p, `rgba(255,255,255,${a})`));
  g.fillStyle = gr; g.fillRect(0, 0, 256, 256);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
const TEX_NUVENS = [texNuvem(1), texNuvem(40), texNuvem(90), texNuvem(160)];

/* ── Sol ───────────────────────────────────────────────────── */
const solMat = new THREE.SpriteMaterial({ map: texBrilho([[0, 1], [0.12, 0.95], [0.2, 0.5], [0.5, 0.12], [1, 0]]), blending: THREE.AdditiveBlending, depthWrite: false, transparent: true });
const sol = new THREE.Sprite(solMat);
sol.scale.set(150, 150, 1);
camara.add(sol);

/* ── Nuvens: 3 camadas, vento contínuo, respiração ──────────── */
const nuvemShader = (mat) => {
  mat.onBeforeCompile = (sh) => {
    sh.uniforms.sombra = mat.userData.sombra;
    sh.fragmentShader = sh.fragmentShader
      .replace("void main() {", "uniform vec3 sombra;\nvoid main() {")
      .replace("#include <map_fragment>", `
        #include <map_fragment>
        float base = smoothstep(0.75, 0.25, vMapUv.y);
        diffuseColor.rgb = mix(diffuseColor.rgb, sombra, base * 0.55);`);
  };
};
const corNuvem = { value: new THREE.Color("#fff") }, corSombra = { value: SOMBRA_NUVEM[0].clone() };
const nuvens = [];
const CAMADAS = [
  { n: fraco ? 4 : 6, esc: [16, 26], op: 0.9, vel: 6, dist: [8, 24], y: [-9, -2] },
  { n: fraco ? 8 : 10, esc: [26, 44], op: 0.8, vel: 3, dist: [30, 70], y: [-20, -4] },
  { n: fraco ? 12 : 15, esc: [40, 75], op: 0.65, vel: 1, dist: [80, 180], y: [-42, -6] },
];
const PERCURSO = 60; // unidades que a câmara avança no eixo Z ao longo da página
const LARGURA = 160;
CAMADAS.forEach((cam, li) => {
  for (let i = 0; i < cam.n; i++) {
    const mat = new THREE.SpriteMaterial({ map: TEX_NUVENS[i % 4], transparent: true, depthWrite: false, opacity: cam.op, fog: false });
    mat.userData.sombra = corSombra;
    nuvemShader(mat);
    const sp = new THREE.Sprite(mat);
    const e = lerp(cam.esc[0], cam.esc[1], rnd());
    sp.scale.set(e * 1.6, e, 1);
    // espalhadas ao longo do percurso, afastadas do centro do ecrã
    const lado = rnd() < 0.5 ? -1 : 1;
    const x = lado * lerp(li === 0 ? 7 : 2, li === 2 ? LARGURA * 0.5 : LARGURA * 0.3, rnd());
    const z = -lerp(cam.dist[0], cam.dist[1], rnd()) - rnd() * (PERCURSO + 20) + 10;
    sp.position.set(x, lerp(cam.y[0], cam.y[1], rnd()), z);
    sp.userData = { camada: li, op: cam.op, vel: cam.vel, fase: rnd() * 6.28, rot: (rnd() - 0.5) * 0.02, baseRot: (rnd() - 0.5) * 0.3 };
    mat.rotation = sp.userData.baseRot;
    cena.add(sp);
    nuvens.push(sp);
  }
});

/* ── Partículas de luz e estrelas ──────────────────────────── */
const pGeo = new THREE.BufferGeometry();
const nP = fraco ? 100 : 200;
const pPos = new Float32Array(nP * 3);
for (let i = 0; i < nP; i++) { pPos[i * 3] = (rnd() - 0.5) * 40; pPos[i * 3 + 1] = (rnd() - 0.5) * 24; pPos[i * 3 + 2] = -rnd() * 40; }
pGeo.setAttribute("position", new THREE.BufferAttribute(pPos, 3));
const poeira = new THREE.Points(pGeo, new THREE.PointsMaterial({ color: 0xffffff, size: 1.6, sizeAttenuation: false, transparent: true, opacity: 0.3, depthWrite: false }));
camara.add(poeira);

const eGeo = new THREE.BufferGeometry();
const nE = 700, ePos = new Float32Array(nE * 3);
for (let i = 0; i < nE; i++) {
  const th = rnd() * Math.PI * 2, ph = Math.acos(lerp(0.12, 1, rnd()));
  ePos[i * 3] = Math.sin(ph) * Math.cos(th) * 500; ePos[i * 3 + 1] = Math.cos(ph) * 500; ePos[i * 3 + 2] = Math.sin(ph) * Math.sin(th) * 500;
}
eGeo.setAttribute("position", new THREE.BufferAttribute(ePos, 3));
const estrelasMat = new THREE.PointsMaterial({ color: 0xffffff, size: 1.6, sizeAttenuation: false, transparent: true, opacity: 0, depthWrite: false });
const estrelas = new THREE.Points(eGeo, estrelasMat);
camara.add(estrelas);

/* ── Telas do hero ─────────────────────────────────────────── */
const grupoTelas = new THREE.Group();
camara.add(grupoTelas);
const telas = [];
const W = 3.2, H = 2.05, BARRA = 0.17;
const loader = new THREE.TextureLoader();

function texBarra(texto) {
  const c = document.createElement("canvas"); c.width = 1024; c.height = Math.round(1024 * BARRA / W);
  const g = c.getContext("2d");
  g.fillStyle = "#F2F5FA"; g.fillRect(0, 0, c.width, c.height);
  const cy = c.height / 2;
  ["#FF6058", "#FFBD2E", "#28CA42"].forEach((cor, i) => { g.fillStyle = cor; g.beginPath(); g.arc(30 + i * 24, cy, 7, 0, Math.PI * 2); g.fill(); });
  const pw = 420, px = (c.width - pw) / 2;
  g.fillStyle = "#fff"; g.beginPath(); g.roundRect(px, cy - 14, pw, 28, 14); g.fill();
  g.fillStyle = "#3D4F6B"; g.font = "500 15px Inter, system-ui, sans-serif"; g.textAlign = "center"; g.textBaseline = "middle";
  g.fillText(texto, c.width / 2, cy + 1);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
}

const telaVert = `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }`;
const telaFrag = `
  uniform sampler2D mapa; uniform sampler2D barra; uniform float fracV; uniform float offset; uniform float barraF;
  uniform vec2 tam; uniform float raio; uniform float opac; uniform float brilho;
  varying vec2 vUv;
  float rr(vec2 p, vec2 b, float r){ vec2 q = abs(p) - b + r; return length(max(q,0.0)) + min(max(q.x,q.y),0.0) - r; }
  void main(){
    vec2 p = (vUv - 0.5) * tam;
    float d = rr(p, tam * 0.5, raio);
    float a = 1.0 - smoothstep(-0.006, 0.006, d);
    vec3 c;
    if (vUv.y > 1.0 - barraF) {
      vec2 bu = vec2(vUv.x, (vUv.y - (1.0 - barraF)) / barraF);
      c = texture2D(barra, bu).rgb;
    } else {
      float vy = vUv.y / (1.0 - barraF);
      vec2 tu = vec2(vUv.x, 1.0 - (offset + (1.0 - vy) * fracV));
      c = texture2D(mapa, tu).rgb;
    }
    c += brilho * 0.06;
    gl_FragColor = vec4(c, a * opac);
    #include <colorspace_fragment>
  }`;

const texSombra = texBrilho([[0, 0.55], [0.5, 0.18], [1, 0]]);
const nTelas = movel ? 3 : 7;
const lista = (S.telas || []).slice();
const escolhidas = movel ? [lista[1], lista[3], lista[5]].filter(Boolean) : lista.slice(0, 7);
escolhidas.forEach((d, idx) => {
  const i = idx - Math.floor(nTelas / 2); // -3..3
  const mat = new THREE.ShaderMaterial({
    transparent: true, depthWrite: true,
    uniforms: {
      mapa: { value: null }, barra: { value: texBarra(d.url || d.nome) }, fracV: { value: 0.8 }, offset: { value: 0 },
      barraF: { value: BARRA / H }, tam: { value: new THREE.Vector2(W, H) }, raio: { value: 0.12 }, opac: { value: 0 }, brilho: { value: 0 },
    },
    vertexShader: telaVert, fragmentShader: telaFrag,
  });
  const malha = new THREE.Mesh(new THREE.PlaneGeometry(W, H), mat);
  const sombra = new THREE.Mesh(new THREE.PlaneGeometry(W * 1.5, H * 0.9), new THREE.MeshBasicMaterial({ map: texSombra, color: 0x0B1B33, transparent: true, opacity: 0.22, depthWrite: false }));
  sombra.position.set(0, -H * 0.55, -0.35);
  sombra.rotation.x = -0.25;
  const pivo = new THREE.Group();
  pivo.add(sombra, malha);
  grupoTelas.add(pivo);
  loader.load(d.img, (t) => {
    t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; t.minFilter = THREE.LinearMipmapLinearFilter;
    mat.uniforms.mapa.value = t;
    const conteudoAsp = (H - BARRA) / W; // altura/largura da área visível
    const imgAsp = t.image.height / t.image.width;
    mat.uniforms.fracV.value = Math.min(1, conteudoAsp / imgAsp);
    malha.userData.carregado = performance.now();
  });
  telas.push({ i, d, pivo, malha, sombra, mat, fase: rnd() * 6.28, periodo: lerp(4, 6, rnd()), hover: 0, entrada: 0 });
});

/* nuvens que passam à frente e atrás das telas */
const nuvensHero = [];
{
  [[-6.5, -1.6, -4, 4.5], [6.8, -2.2, -5, 5], [-2.5, -3.6, -9, 7], [3.5, -3.2, -12, 8]].forEach(([x, y, z, e], k) => {
    const mat = new THREE.SpriteMaterial({ map: TEX_NUVENS[k % 4], transparent: true, depthWrite: false, opacity: 0.85 });
    mat.userData.sombra = corSombra; nuvemShader(mat);
    const sp = new THREE.Sprite(mat);
    sp.scale.set(e * 1.6, e, 1); sp.position.set(x, y, z);
    sp.userData = { x0: x, fase: k * 1.7 };
    grupoTelas.add(sp); nuvensHero.push(sp);
  });
}

/* ── Hover e etiqueta ──────────────────────────────────────── */
const etiqueta = document.querySelector(".tela-etiqueta");
const ray = new THREE.Raycaster();
const ratoV = new THREE.Vector2(-9, -9);
let sobre = null;
addEventListener("pointermove", (e) => { ratoV.set((e.clientX / innerWidth) * 2 - 1, -(e.clientY / innerHeight) * 2 + 1); }, { passive: true });
document.addEventListener("pointerleave", () => ratoV.set(-9, -9));

/* ── Disposição em arco ────────────────────────────────────── */
const R = 6;
function layout(t, h, agora) {
  const aspect = innerWidth / innerHeight;
  const recuo = aspect < 1.2 ? 1.6 : aspect < 1.5 ? 0.8 : 0; // ecrãs estreitos: afasta o arco
  const baseY = movel ? -1.5 : -1.75;
  const fase1 = suave(0, 0.5, h), fase2 = suave(0.5, 1, h);
  grupoTelas.rotation.y = lerp(grupoTelas.rotation.y, (reduzir ? 0 : MD.rato.x * 0.087) + fase1 * 0.25, 0.05);
  grupoTelas.rotation.x = lerp(grupoTelas.rotation.x, reduzir ? 0 : MD.rato.y * 0.05, 0.05);

  for (const tl of telas) {
    const { i, pivo, malha, mat } = tl;
    const k = Math.abs(i);
    let x, y, z, ry = 0, rz = 0, s;
    if (movel) {
      // leque empilhado
      x = i * 1.05; z = -8.4 - k * 0.8 - recuo; y = baseY - k * 0.25; rz = -i * 0.08; ry = -i * 0.25; s = k === 0 ? 1.05 : 0.88;
    } else {
      const a = i * 0.34;
      x = Math.sin(a) * R; z = -2.2 - Math.cos(a) * R - k * 0.55 - recuo; ry = -a; s = k === 0 ? 1.1 : 0.92 - k * 0.08;
      y = baseY - k * 0.08;
    }
    // flutuação
    const fl = reduzir ? 0 : Math.sin(t * (6.283 / tl.periodo) + tl.fase);
    y += fl * 0.08; rz += reduzir ? 0 : Math.sin(t * 0.5 + tl.fase) * 0.012;
    // entrada a partir do fundo (z -20), stagger 0.08 s
    const t0 = MD.inicio ? (agora - Math.max(MD.inicio, CEU_T0)) / 1000 - 0.9 - (k + (i < 0 ? 0.5 : 0)) * 0.08 : -1;
    const ent = reduzir ? 1 : 1 - Math.pow(1 - lim(t0 / 1.2), 3);
    tl.entrada = ent;
    z = lerp(-20, z, ent); ry += (1 - ent) * 0.5 * Math.sign(i || 1);
    // hover
    tl.hover = lerp(tl.hover, sobre === tl ? 1 : 0, 0.12);
    z += tl.hover * 0.3;
    // scroll: laterais saem, a central avança até encher o ecrã
    if (k > 0) {
      x += Math.sign(i) * fase1 * (10 + k * 3);
      z -= fase1 * 2;
    } else {
      const vFov = THREE.MathUtils.degToRad(camara.fov);
      const largura = W * s, altura = H * s;
      const dEncher = Math.max(altura / (2 * Math.tan(vFov / 2)), largura / (2 * Math.tan(vFov / 2) * camara.aspect)) * 0.82;
      x = lerp(x, 0, fase2); y = lerp(y, 0.06 * s, fase2); z = lerp(z, -dEncher, fase2); ry = lerp(ry, 0, fase2); rz = lerp(rz, 0, fase2);
    }
    pivo.position.set(x, y, z);
    pivo.rotation.set(0, ry - (k === 0 ? grupoTelas.rotation.y * fase2 : 0), rz);
    pivo.scale.setScalar(s);
    mat.uniforms.opac.value = ent * (k > 0 ? 1 - suave(0.3, 0.55, h) : 1) * (mat.uniforms.mapa.value ? 1 : 0);
    mat.uniforms.brilho.value = tl.hover;
    tl.sombra.material.opacity = (0.18 + tl.hover * 0.14) * ent * (1 - fase2);
    // conteúdo a rolar dentro da tela (vai e volta, devagar)
    const extra = 1 - mat.uniforms.fracV.value;
    if (extra > 0.001 && !reduzir) {
      const dur = tl.d.longo ? 26 : 9;
      const u = (t / dur + tl.fase) % 2, pp = u < 1 ? u : 2 - u;
      mat.uniforms.offset.value = extra * (pp * pp * (3 - 2 * pp));
    }
  }
  for (const n of nuvensHero) {
    n.position.x = n.userData.x0 + Math.sin(t * 0.08 + n.userData.fase) * 0.8 + fase1 * Math.sign(n.userData.x0) * 6;
    n.material.opacity = 0.85 * (1 - fase1);
  }
  grupoTelas.visible = h < 0.999 && (MD.filme || 0) < 0.999;
}

/* ── Ciclo ─────────────────────────────────────────────────── */
let ativo = true, ultimo = performance.now(), camZ = 0, rotX = 0, rotY = 0;
const corCeuT = new THREE.Color(), corHorT = new THREE.Color();
const v3 = new THREE.Vector3();

function frame(agora) {
  if (!ativo) return;
  const dt = Math.min(0.05, (agora - ultimo) / 1000); ultimo = agora;
  const t = agora / 1000;
  const v = MD.ceu || 0;

  // cores do céu e do sol
  ceuMat.uniforms.topo.value.copy(corPal(v, 0));
  ceuMat.uniforms.horizonte.value.copy(corPal(v, 1));
  const solY = lerp(0.42, -0.06, suave(0, 3, v) ** 0.8);
  const solDir = v3.set(0.38, solY, -1).normalize();
  ceuMat.uniforms.solDir.value.copy(solDir);
  ceuMat.uniforms.solCor.value.copy(corEm(SOL, v));
  sol.position.copy(solDir).multiplyScalar(500);
  solMat.color.copy(corEm(SOL, v));
  solMat.opacity = 1 - suave(2.6, 3, v) * 0.85;
  corNuvem.value.copy(corEm(NUVEM, v));
  corSombra.value.copy(corEm(SOMBRA_NUVEM, v));
  estrelasMat.opacity = suave(2.5, 3, v) * 0.9;
  poeira.material.opacity = 0.3 * (1 - suave(2.5, 3, v) * 0.5);

  // câmara avança no eixo Z com o scroll; inclina com o rato (máx. 2°)
  camZ = lerp(camZ, -(MD.total || 0) * PERCURSO, reduzir ? 1 : 0.08);
  camara.position.set(0, 0, camZ);
  const max = 0.035;
  rotY = lerp(rotY, reduzir ? 0 : -MD.rato.x * max, 0.05);
  rotX = lerp(rotX, reduzir ? 0 : -MD.rato.y * max * 0.6, 0.05);
  camara.rotation.set(rotX, rotY, 0);

  // nuvens: vento, respiração, desvanecer quando a câmara as atravessa
  for (const n of nuvens) {
    const u = n.userData;
    if (!reduzir) {
      n.position.x += 0.02 * u.vel * dt * 6;
      if (n.position.x > LARGURA * 0.6) n.position.x -= LARGURA * 1.2;
      n.material.rotation = u.baseRot + Math.sin(t * 0.05 + u.fase) * 0.06;
    }
    const resp = reduzir ? 1 : 0.85 + 0.15 * Math.sin(t * 0.3 + u.fase);
    const dz = n.position.z - camZ; // negativo = à frente
    const perto = suave(2, 14, -dz) * (dz < 0 ? 1 : 0);
    n.material.opacity = u.op * resp * perto;
    n.material.color.copy(corNuvem.value);
  }
  for (const n of nuvensHero) n.material.color.copy(corNuvem.value);
  if (!reduzir) poeira.rotation.y = Math.sin(t * 0.05) * 0.2, poeira.position.y = Math.sin(t * 0.2) * 0.3;

  // telas
  const h = MD.hero || 0;
  if (telas.length) {
    camara.updateMatrixWorld();
    layout(t, h, agora);
    // hover
    sobre = null;
    if (h < 0.3 && !matchMedia("(hover: none)").matches) {
      ray.setFromCamera(ratoV, camara);
      const hit = ray.intersectObjects(telas.map((x) => x.malha), false)[0];
      if (hit) sobre = telas.find((x) => x.malha === hit.object);
    }
    if (sobre && etiqueta) {
      const p = new THREE.Vector3(0, H / 2 + 0.12, 0).applyMatrix4(sobre.malha.matrixWorld).project(camara);
      etiqueta.innerHTML = `<b>${sobre.d.nome}</b> · ${sobre.d.setor}`;
      etiqueta.style.left = ((p.x + 1) / 2) * innerWidth + "px";
      etiqueta.style.top = ((1 - p.y) / 2) * innerHeight + "px";
      etiqueta.classList.add("vis");
    } else if (etiqueta) etiqueta.classList.remove("vis");
  }

  renderer.render(cena, camara);
  if (!reduzir || dt === 0) requestAnimationFrame(frame);
  else requestAnimationFrame(frame); // com movimento reduzido o céu continua a acompanhar o scroll, sem deriva
}

addEventListener("resize", () => {
  camara.aspect = innerWidth / innerHeight;
  camara.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight, false);
});
document.addEventListener("visibilitychange", () => {
  ativo = !document.hidden;
  if (ativo) { ultimo = performance.now(); requestAnimationFrame(frame); }
});
requestAnimationFrame((t) => { frame(t); requestAnimationFrame(() => canvas.classList.add("pronto")); });
