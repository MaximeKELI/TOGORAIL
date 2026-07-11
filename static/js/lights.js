/* ==========================================================================
   Togo Rail — Cinematic light system
   Canvas golden particles + speed light streaks in the hero, a global
   cursor-follow spotlight, and animated volumetric beams.
   ========================================================================== */
(function () {
  "use strict";

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced) return;

  /* ======================================================================
     GLOBAL CURSOR SPOTLIGHT (subtle radial glow that follows the pointer)
     ====================================================================== */
  (function spotlight() {
    if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
    const el = document.createElement("div");
    el.style.cssText =
      "position:fixed;inset:0;z-index:1;pointer-events:none;mix-blend-mode:screen;" +
      "transition:opacity .6s ease;opacity:0;background:radial-gradient(600px circle at 50% 50%," +
      "rgba(201,162,39,0.10),transparent 60%);";
    document.body.appendChild(el);
    let raf;
    window.addEventListener("mousemove", (e) => {
      el.style.opacity = "1";
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        el.style.background =
          `radial-gradient(600px circle at ${e.clientX}px ${e.clientY}px,` +
          `rgba(201,162,39,0.10),transparent 60%)`;
      });
    });
  })();

  /* ======================================================================
     HERO CANVAS — golden particles + speed light streaks
     ====================================================================== */
  const canvas = document.getElementById("hero-lights");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  let W, H, dpr;
  const particles = [];
  const streaks = [];
  let running = true;

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    const rect = canvas.parentElement.getBoundingClientRect();
    W = rect.width;
    H = rect.height;
    canvas.width = W * dpr;
    canvas.height = H * dpr;
    canvas.style.width = W + "px";
    canvas.style.height = H + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  resize();
  window.addEventListener("resize", resize);

  function rand(a, b) {
    return a + Math.random() * (b - a);
  }

  // Floating golden dust particles
  const COUNT = window.innerWidth < 768 ? 40 : 90;
  for (let i = 0; i < COUNT; i++) {
    particles.push({
      x: rand(0, W),
      y: rand(0, H),
      r: rand(0.4, 2.2),
      vx: rand(-0.15, 0.15),
      vy: rand(-0.25, -0.05),
      a: rand(0.1, 0.7),
      tw: rand(0.005, 0.02),
      tp: rand(0, Math.PI * 2),
    });
  }

  function spawnStreak() {
    const y = rand(H * 0.55, H * 0.95);
    streaks.push({
      x: -rand(50, 300),
      y,
      len: rand(120, 340),
      speed: rand(9, 20),
      w: rand(1, 2.4),
      a: rand(0.15, 0.5),
    });
  }
  let streakTimer = 0;

  function draw() {
    if (!running) return;
    ctx.clearRect(0, 0, W, H);

    // particles
    for (const p of particles) {
      p.x += p.vx;
      p.y += p.vy;
      p.tp += p.tw;
      if (p.y < -10) {
        p.y = H + 10;
        p.x = rand(0, W);
      }
      if (p.x < -10) p.x = W + 10;
      if (p.x > W + 10) p.x = -10;
      const alpha = p.a * (0.6 + 0.4 * Math.sin(p.tp));
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(232,212,139,${alpha})`;
      ctx.shadowColor = "rgba(201,162,39,0.8)";
      ctx.shadowBlur = 8;
      ctx.fill();
    }
    ctx.shadowBlur = 0;

    // speed streaks
    streakTimer++;
    if (streakTimer > 26) {
      streakTimer = 0;
      if (Math.random() > 0.35) spawnStreak();
    }
    for (let i = streaks.length - 1; i >= 0; i--) {
      const s = streaks[i];
      s.x += s.speed;
      const grad = ctx.createLinearGradient(s.x, s.y, s.x + s.len, s.y);
      grad.addColorStop(0, "rgba(201,162,39,0)");
      grad.addColorStop(0.5, `rgba(255,225,150,${s.a})`);
      grad.addColorStop(1, "rgba(201,162,39,0)");
      ctx.strokeStyle = grad;
      ctx.lineWidth = s.w;
      ctx.beginPath();
      ctx.moveTo(s.x, s.y);
      ctx.lineTo(s.x + s.len, s.y);
      ctx.stroke();
      if (s.x > W + 100) streaks.splice(i, 1);
    }

    requestAnimationFrame(draw);
  }
  draw();

  // Pause when hero off-screen (perf)
  const hero = canvas.closest("#hero");
  if (hero && "IntersectionObserver" in window) {
    new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          running = e.isIntersecting;
          if (running) draw();
        });
      },
      { threshold: 0 }
    ).observe(hero);
  }
})();
