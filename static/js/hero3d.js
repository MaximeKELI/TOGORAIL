// Lightweight Three.js particle field for the hero — a golden starfield /
// rail-dust cloud that gently drifts and reacts to the mouse. Degrades
// gracefully if Three.js is unavailable or reduced motion is requested.
(function () {
  "use strict";

  const canvas = document.getElementById("hero-3d");
  if (!canvas) return;

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced || typeof THREE === "undefined") return;

  const hero = canvas.closest("#hero") || canvas.parentElement;
  let width = hero.clientWidth;
  let height = hero.clientHeight;

  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: true,
    powerPreference: "high-performance",
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.6));
  renderer.setSize(width, height, false);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(70, width / height, 0.1, 100);
  camera.position.z = 22;

  // Particle geometry
  const COUNT = window.innerWidth < 768 ? 900 : 1800;
  const positions = new Float32Array(COUNT * 3);
  const speeds = new Float32Array(COUNT);
  for (let i = 0; i < COUNT; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 60;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 40;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 40;
    speeds[i] = 0.01 + Math.random() * 0.05;
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));

  // Soft round golden sprite
  const sprite = makeSprite();
  const material = new THREE.PointsMaterial({
    size: 0.5,
    map: sprite,
    color: new THREE.Color(0xe8d48b),
    transparent: true,
    opacity: 0.85,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  });

  const points = new THREE.Points(geometry, material);
  scene.add(points);

  // Subtle secondary layer (cooler, further away) for depth
  const geo2 = geometry.clone();
  const mat2 = material.clone();
  mat2.color = new THREE.Color(0x6fa8ff);
  mat2.opacity = 0.25;
  mat2.size = 0.35;
  const points2 = new THREE.Points(geo2, mat2);
  points2.position.z = -10;
  scene.add(points2);

  let mouseX = 0;
  let mouseY = 0;
  let targetX = 0;
  let targetY = 0;

  window.addEventListener(
    "pointermove",
    (e) => {
      mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
      mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
    },
    { passive: true }
  );

  let running = true;
  const io = new IntersectionObserver(
    (entries) => {
      running = entries[0].isIntersecting;
      if (running) loop();
    },
    { threshold: 0 }
  );
  io.observe(hero);

  const clock = new THREE.Clock();

  function loop() {
    if (!running) return;
    requestAnimationFrame(loop);
    const t = clock.getElapsedTime();

    targetX += (mouseX - targetX) * 0.04;
    targetY += (mouseY - targetY) * 0.04;

    points.rotation.y = t * 0.02 + targetX * 0.3;
    points.rotation.x = targetY * 0.2;
    points2.rotation.y = -t * 0.015 - targetX * 0.2;

    // drift particles forward for a gentle "moving through space" feel
    const pos = geometry.attributes.position.array;
    for (let i = 0; i < COUNT; i++) {
      pos[i * 3 + 2] += speeds[i];
      if (pos[i * 3 + 2] > 25) pos[i * 3 + 2] = -25;
    }
    geometry.attributes.position.needsUpdate = true;

    camera.position.x += (targetX * 2 - camera.position.x) * 0.05;
    camera.position.y += (-targetY * 1.5 - camera.position.y) * 0.05;
    camera.lookAt(scene.position);

    renderer.render(scene, camera);
  }
  loop();

  function onResize() {
    width = hero.clientWidth;
    height = hero.clientHeight;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height, false);
  }
  window.addEventListener("resize", onResize, { passive: true });

  function makeSprite() {
    const c = document.createElement("canvas");
    c.width = c.height = 64;
    const ctx = c.getContext("2d");
    const g = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
    g.addColorStop(0, "rgba(255,255,255,1)");
    g.addColorStop(0.3, "rgba(255,240,200,0.8)");
    g.addColorStop(1, "rgba(255,240,200,0)");
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, 64, 64);
    const tex = new THREE.CanvasTexture(c);
    return tex;
  }
})();
