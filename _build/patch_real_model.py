# One-time patch: swaps the hand-built body for the real Sketchfab Mustang (mustang.glb).
# Run from the mustang-garage folder: python _build/patch_real_model.py
p = 'index.html'
s = open(p, encoding='utf-8').read()

def rep(a, b, cnt=1):
    global s
    n = s.count(a)
    if n != cnt:
        raise SystemExit(f'count {n} for: {a[:90]}')
    s = s.replace(a, b)

rep("import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';",
    "import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';\nimport { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';\nimport { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';")
rep("const DPR = Math.min(window.devicePixelRatio || 1, 1.75);",
    "const MOBILE = matchMedia('(pointer: coarse)').matches || innerWidth < 820;\nconst DPR = Math.min(window.devicePixelRatio || 1, MOBILE ? 1.35 : 1.75);\nconst RQ = MOBILE ? 0.35 : 0.6;")
rep("textureWidth: Math.round(innerWidth * DPR * 0.6), textureHeight: Math.round(innerHeight * DPR * 0.6)",
    "textureWidth: Math.round(innerWidth * DPR * RQ), textureHeight: Math.round(innerHeight * DPR * RQ)")
rep("studio.mirror.getRenderTarget().setSize(Math.round(innerWidth * DPR * 0.6), Math.round(innerHeight * DPR * 0.6));",
    "studio.mirror.getRenderTarget().setSize(Math.round(innerWidth * DPR * RQ), Math.round(innerHeight * DPR * RQ));")
rep("sun.shadow.mapSize.set(2048, 2048);", "sun.shadow.mapSize.set(MOBILE ? 1024 : 2048, MOBILE ? 1024 : 2048);")
rep("const mood = []; // things whose color shifts with Halloween mode",
    "const mood = [], blobs = []; // mood: things whose color shifts with Halloween mode")
rep("b.rotation.x = -Math.PI / 2; b.position.set(x, 0.005, z); b.renderOrder = 1; scene.add(b);",
    "b.rotation.x = -Math.PI / 2; b.position.set(x, 0.005, z); b.renderOrder = 1; scene.add(b); blobs.push(b);")
rep("const XF = 2.395, XR = -2.395, FA = 1.445, RA = -1.275, WR = 0.36, ARCH = 0.412;",
    "let XF = 2.395, XR = -2.395, FA = 1.445, RA = -1.275, WR = 0.36, ARCH = 0.412;")
rep("""function topHeight(x, z) {
  const s = section(x), az = Math.abs(z), p = s.pts;
  for (let j = JT; j < JC; j++) { const a = p[j], b = p[j + 1]; if (az <= a.z && az >= b.z) return lerp(a.y, b.y, (a.z - az) / Math.max(1e-6, a.z - b.z)); }
  return s.P.yBelt;
}""", """function topHeight(x, z) {
  ray.set(new THREE.Vector3(x, 4, z), new THREE.Vector3(0, -1, 0));
  const h = ray.intersectObject(body, false)[0];
  return h ? h.point.y : 0.9;
}""")
rep("const STYLES = {\n  stock: { label: 'Split 5', sub: 'Stock 18 in, yours',",
    "const STYLES = {\n  factory: { label: 'Factory GT', sub: 'On the model', conc: 0.032, count: 5, finish: { hex: '#b9b4b6', metal: 0.9, rough: 0.28 }, shapes: null },\n  stock: { label: 'Split 5', sub: 'Like yours',")
rep("for (const k in STYLES) styleGeos[k] = spokeGeometry(STYLES[k]);",
    "for (const k in STYLES) if (STYLES[k].shapes) styleGeos[k] = spokeGeometry(STYLES[k]);")
rep("""  const spots = [[FA, 0.79, 1], [FA, -0.79, -1], [RA, 0.815, 1], [RA, -0.815, -1]];
  for (const [x, z, side] of spots) {
    const root = new THREE.Group(); root.position.set(x, WR, z); if (side < 0) root.rotation.y = Math.PI;""",
    """  const spots = realSpots || [[FA, 0.79, 1, WR, 1], [FA, -0.79, -1, WR, 1], [RA, 0.815, 1, WR, 1], [RA, -0.815, -1, WR, 1]];
  for (const [x, z, side, y, sc] of spots) {
    const root = new THREE.Group(); root.position.set(x, y, z); root.scale.setScalar(sc); if (side < 0) root.rotation.y = Math.PI;""")
rep("function placeHubs(style) {", """let realSpots = null; const modelWheels = [], modelRims = [];
function applyWheelStyle() {
  const f = state.style === 'factory';
  modelWheels.forEach(n => n.visible = f);
  wheels.forEach(w => { w.root.visible = !f; if (!f) w.spokes.geometry = styleGeos[state.style]; });
  if (!f) placeHubs(state.style);
}
async function buildRealCar() {
  const loader = new GLTFLoader(), draco = new DRACOLoader();
  draco.setDecoderPath('https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/libs/draco/gltf/');
  loader.setDRACOLoader(draco);
  const m = (await loader.loadAsync('mustang.glb')).scene;
  m.updateMatrixWorld(true);
  // the file runs nose-to-tail along z; the front caliper tells us which end is the nose
  const box = new THREE.Box3().setFromObject(m), mid = (box.min.z + box.max.z) / 2;
  const cal = m.getObjectByName('CaliperLF');
  const calZ = cal ? new THREE.Box3().setFromObject(cal).getCenter(new THREE.Vector3()).z : mid + 1;
  m.position.set(-(box.min.x + box.max.x) / 2, -box.min.y, -mid);
  const pivot = new THREE.Group(); pivot.add(m);
  pivot.scale.setScalar(4.79 / (box.max.z - box.min.z));
  pivot.rotation.y = calZ > mid ? Math.PI / 2 : -Math.PI / 2;
  car.add(pivot); car.updateMatrixWorld(true);
  const darkGlass = new THREE.MeshPhysicalMaterial({ color: 0x07090c, roughness: 0.02, metalness: 0, transparent: true, opacity: 0.78, clearcoat: 1, side: THREE.DoubleSide });
  const paintMeshes = [];
  pivot.traverse(o => {
    if (!o.isMesh) {
      if (/^Wheel_/i.test(o.name) && !(o.parent && /^Wheel_/i.test(o.parent.name))) modelWheels.push(o);
      return;
    }
    o.castShadow = true; o.receiveShadow = true;
    const n = o.material.name, light = /Light/i.test(o.name);
    if (n === 'CarPaint2') { o.material = paintPlain; if (!/Caliper/i.test(o.name)) paintMeshes.push(o); }
    else if (n === 'WindowGlass' && !light) o.material = darkGlass;
    else if (n === 'Weels') modelRims.push(o);
    else if (n === 'Material.003') { o.material.userData.base = Math.max(1, o.material.emissiveIntensity) * 2.5; if (!lightsFx.tail.includes(o.material)) lightsFx.tail.push(o.material); }
    else if (n === 'material') { o.material.userData.base = Math.max(1, o.material.emissiveIntensity) * 2.5; if (!lightsFx.head.includes(o.material)) lightsFx.head.push(o.material); }
  });
  // one invisible merged copy of the paint, used for raycasts and the Halloween decals
  const geos = paintMeshes.map(o => {
    const g = o.geometry.clone(); g.applyMatrix4(o.matrixWorld);
    for (const k of Object.keys(g.attributes)) if (k !== 'position' && k !== 'normal') g.deleteAttribute(k);
    if (!g.attributes.normal) g.computeVertexNormals();
    return g.index ? g : null;
  }).filter(Boolean);
  body = new THREE.Mesh(mergeGeometries(geos), new THREE.MeshBasicMaterial({ visible: false }));
  car.add(body);
  // wheel centers and size, so swap-in wheels and floor shadows land in the right spots
  realSpots = modelWheels.map(n => {
    const b = new THREE.Box3().setFromObject(n), c = b.getCenter(new THREE.Vector3()), r = (b.max.y - b.min.y) / 2;
    return [c.x, c.z, Math.sign(c.z) || 1, c.y, r / 0.36];
  });
  const fb = new THREE.Box3().setFromObject(pivot);
  XF = fb.max.x; XR = fb.min.x;
  if (realSpots.length) {
    FA = Math.max(...realSpots.map(s => s[0])); RA = Math.min(...realSpots.map(s => s[0]));
    WR = realSpots.reduce((a, s) => a + s[3], 0) / realSpots.length; ARCH = WR + 0.05;
    realSpots.forEach((s, i) => { if (blobs[i]) blobs[i].position.set(s[0], 0.005, s[1]); });
  }
  for (const s of [1, -1]) {
    const sp = new THREE.SpotLight(0xf2f6ff, 0, 18, 0.5, 0.95, 1.2); sp.position.set(XF - 0.1, 0.68, s * 0.6); sp.target.position.set(9, 0.0, s * 1.8);
    car.add(sp, sp.target); lightsFx.spots.push(sp);
  }
}
function placeHubs(style) {""")
rep("if (!swap.done && swap.t > 0.5) { wheels.forEach(w => w.spokes.geometry = styleGeos[state.style]); placeHubs(state.style); setRimTarget(); swap.done = true; shadowDirty = true; }",
    "if (!swap.done && swap.t > 0.5) { applyWheelStyle(); setRimTarget(); swap.done = true; shadowDirty = true; }")
rep("const state = { paint: 'garnet', style: 'stock',", "const state = { paint: 'garnet', style: 'factory',")
rep("""document.querySelector('.wh-btn[data-k="stock"]').classList.add('on');""",
    """document.querySelector('.wh-btn[data-k="factory"]').classList.add('on');""")
rep("lightsFx.head.forEach(m => m.emissiveIntensity = 3.2 * anim.lights);",
    "lightsFx.head.forEach(m => m.emissiveIntensity = (m.userData.base ?? 3.2) * anim.lights);")
rep("lightsFx.tail.forEach(m => m.emissiveIntensity = 0.25 + 2.9 * anim.lights);",
    "lightsFx.tail.forEach(m => m.emissiveIntensity = (m.userData.base ?? 3) * (0.12 + 0.88 * anim.lights));")
rep("""  await step(30, 'Shaping the body');
  buildCar();
  await step(62, 'Mounting the wheels');
  buildWheels();""", """  await step(30, 'Rolling the Mustang in');
  await buildRealCar();
  await step(62, 'Mounting the wheels');
  buildWheels();
  modelRims.forEach(o => o.material = rimMat);""")
rep("placeHubs('stock');\n}", "placeHubs('stock');\n  applyWheelStyle();\n}")
rep("  if (wide) camera.setViewOffset(innerWidth, innerHeight, 165, 0, innerWidth, innerHeight);",
    "  camera.fov = camera.aspect < 0.8 ? 50 : 32;\n  if (wide) camera.setViewOffset(innerWidth, innerHeight, 165, 0, innerWidth, innerHeight);")
rep('<div class="eyebrow">2018 Ford Mustang &middot; EcoBoost Fastback</div>',
    '<div class="eyebrow">2018 Ford Mustang &middot; Fastback</div>')
rep('<div id="hint">Drag to orbit &middot; Scroll to zoom &middot; Right drag to pan</div>',
    '<div id="hint">Drag to orbit &middot; Scroll to zoom &middot; Right drag to pan</div>\n<div id="credit">3D model: <a href="https://sketchfab.com/3d-models/mustang-gt-2018-dd4365565b6b4e0ea6c06a1ca4113e3e" target="_blank" rel="noopener">&ldquo;Mustang_GT 2018&rdquo; by Demonic Arts</a> &middot; <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a></div>')
rep("  #err {", """  #credit { position:fixed; left:28px; bottom:42px; font:400 10.5px/1.3 "IBM Plex Mono",monospace; color:var(--mute); }
  #credit a { color:var(--mute); }
  #err {""")
rep("    #hud { left:16px; top:14px; } #hud h1 { font-size:30px; } #hint { display:none; }",
    "    #hud { left:16px; top:14px; } #hud h1 { font-size:30px; } #hint { display:none; }\n    #credit { left:16px; bottom:calc(42vh + 18px); font-size:9.5px; }")
open(p, 'w', encoding='utf-8').write(s)
print('patched')
