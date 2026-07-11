/* ==========================================================================
   Togo Rail — GSAP animation layer
   Hero timeline, scroll reveals, animated counters, infinite logo marquee,
   parallax and timeline draw.
   ========================================================================== */
(function () {
  "use strict";

  if (!window.gsap) return;

  const prefersReduced = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  gsap.registerPlugin(ScrollTrigger);

  // Sync GSAP ScrollTrigger with Lenis if present.
  if (window.__lenis) {
    window.__lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add((time) => window.__lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);
  }

  if (prefersReduced) {
    gsap.set("[data-hero], [data-animate]", { opacity: 1, y: 0 });
    initCounters(true);
    return;
  }

  /* ---------------- HERO timeline ---------------- */
  const heroEls = gsap.utils.toArray("[data-hero]");
  if (heroEls.length) {
    const tl = gsap.timeline({ defaults: { ease: "expo.out" } });
    tl.from("[data-hero-line] > span", {
      yPercent: 120,
      duration: 1.1,
      stagger: 0.12,
      onStart: () => gsap.set("[data-hero]", { opacity: 1 }),
    })
      .from(
        "[data-hero-sub]",
        { y: 26, opacity: 0, duration: 0.9 },
        "-=0.6"
      )
      .from(
        "[data-hero-cta] > *",
        { y: 18, opacity: 0, duration: 0.7, stagger: 0.1 },
        "-=0.55"
      )
      .from(
        "[data-hero-stat]",
        { y: 20, opacity: 0, duration: 0.6, stagger: 0.1 },
        "-=0.5"
      )
      .from(
        "[data-hero-scroll]",
        { opacity: 0, y: 10, duration: 0.6 },
        "-=0.3"
      );
    gsap.set("[data-hero]", { opacity: 1 });
  }

  /* ---------------- HERO parallax ---------------- */
  const heroMedia = document.querySelector("[data-hero-media]");
  if (heroMedia) {
    gsap.to(heroMedia, {
      yPercent: 18,
      scale: 1.12,
      ease: "none",
      scrollTrigger: {
        trigger: "#hero",
        start: "top top",
        end: "bottom top",
        scrub: true,
      },
    });
  }

  /* ---------------- Generic scroll reveals ---------------- */
  gsap.utils.toArray("[data-animate]").forEach((el) => {
    const type = el.dataset.animate || "up";
    const vars = { opacity: 0, duration: 0.9, ease: "power3.out" };
    if (type === "up") vars.y = 50;
    if (type === "left") vars.x = -50;
    if (type === "right") vars.x = 50;
    if (type === "scale") vars.scale = 0.9;

    gsap.from(el, {
      ...vars,
      scrollTrigger: { trigger: el, start: "top 85%", once: true },
      onStart: () => gsap.set(el, { opacity: 1 }),
    });
    gsap.set(el, { opacity: 1 });
  });

  /* ---------------- Staggered groups ---------------- */
  gsap.utils.toArray("[data-stagger]").forEach((group) => {
    const items = group.querySelectorAll("[data-stagger-item]");
    gsap.from(items, {
      y: 48,
      opacity: 0,
      duration: 0.8,
      ease: "power3.out",
      stagger: 0.12,
      scrollTrigger: { trigger: group, start: "top 82%", once: true },
      onStart: () => gsap.set(items, { opacity: 1 }),
    });
    gsap.set(items, { opacity: 1 });
  });

  /* ---------------- Counters ---------------- */
  function initCounters(instant) {
    document.querySelectorAll("[data-counter]").forEach((el) => {
      const end = parseFloat(el.dataset.counter);
      if (instant) {
        el.textContent = end;
        return;
      }
      const obj = { v: 0 };
      ScrollTrigger.create({
        trigger: el,
        start: "top 85%",
        once: true,
        onEnter: () => {
          gsap.to(obj, {
            v: end,
            duration: 1.8,
            ease: "power2.out",
            onUpdate: () => {
              el.textContent = Math.round(obj.v).toLocaleString();
            },
          });
        },
      });
    });
  }
  initCounters(false);

  /* ---------------- Infinite logo marquee ---------------- */
  const track = document.querySelector(".logo-track");
  if (track) {
    const half = track.scrollWidth / 2;
    gsap.to(track, {
      x: -half,
      duration: 26,
      ease: "none",
      repeat: -1,
      modifiers: {
        x: (x) => {
          const v = parseFloat(x) % half;
          return `${v}px`;
        },
      },
    });
    // subtle float
    gsap.to(track, {
      y: 6,
      duration: 3.4,
      ease: "sine.inOut",
      yoyo: true,
      repeat: -1,
    });
  }

  /* ---------------- Timeline vertical draw ---------------- */
  const tline = document.querySelector("[data-timeline-progress]");
  if (tline) {
    gsap.to(tline, {
      scaleY: 1,
      transformOrigin: "top",
      ease: "none",
      scrollTrigger: {
        trigger: "[data-timeline]",
        start: "top 70%",
        end: "bottom 80%",
        scrub: true,
      },
    });
  }

  /* ---------------- Section title char shimmer on enter ---------------- */
  gsap.utils.toArray("[data-title-reveal]").forEach((title) => {
    gsap.from(title, {
      backgroundPositionX: "100%",
      opacity: 0,
      y: 30,
      duration: 1,
      ease: "power3.out",
      scrollTrigger: { trigger: title, start: "top 88%", once: true },
    });
  });

  ScrollTrigger.refresh();
})();
