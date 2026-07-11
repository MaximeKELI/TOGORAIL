/* ==========================================================================
   Togo Rail — Premium interaction layer
   Custom magnetic cursor, split-text reveals, 3D tilt, mouse parallax,
   scroll-velocity marquee, pinned horizontal scroll, back-to-top ring,
   preloader intro.
   ========================================================================== */
(function () {
  "use strict";

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  const hasGsap = !!window.gsap;
  if (hasGsap && window.ScrollTrigger) gsap.registerPlugin(ScrollTrigger);

  /* ======================================================================
     1. PRELOADER
     ====================================================================== */
  (function preloader() {
    const pre = document.getElementById("preloader");
    if (!pre) return;
    document.body.classList.add("loading");
    const bar = pre.querySelector(".pl-bar span");
    const count = pre.querySelector(".pl-count");
    const drawEls = pre.querySelectorAll(".pl-path, .pl-ring");
    // Prepare SVG stroke-draw
    drawEls.forEach((p) => {
      try {
        const len = p.getTotalLength();
        p.style.strokeDasharray = len;
        p.style.strokeDashoffset = len;
      } catch (e) {}
    });
    const obj = { v: 0 };

    function finish() {
      document.body.classList.remove("loading");
      if (hasGsap && !reduced) {
        gsap.to(pre, {
          yPercent: -100,
          duration: 0.9,
          ease: "expo.inOut",
          onComplete: () => pre.remove(),
          delay: 0.15,
        });
      } else {
        pre.remove();
      }
      document.dispatchEvent(new Event("preloader:done"));
    }

    if (reduced || !hasGsap) {
      finish();
      return;
    }
    const tl = gsap.timeline({ onComplete: finish });
    tl.to(drawEls, {
      strokeDashoffset: 0,
      duration: 1.1,
      ease: "power2.inOut",
    });
    tl.to(
      obj,
      {
        v: 100,
        duration: 1.2,
        ease: "power2.inOut",
        onUpdate: () => {
          const val = Math.round(obj.v);
          if (bar) bar.style.width = val + "%";
          if (count) count.textContent = String(val).padStart(3, "0");
        },
      },
      0
    );
  })();

  /* ======================================================================
     2. CUSTOM MAGNETIC CURSOR
     ====================================================================== */
  if (finePointer && hasGsap && !reduced) {
    const dot = document.createElement("div");
    const ring = document.createElement("div");
    dot.className = "cursor-dot";
    ring.className = "cursor-ring";
    document.body.appendChild(dot);
    document.body.appendChild(ring);
    document.body.classList.add("has-custom-cursor");

    const xDot = gsap.quickTo(dot, "x", { duration: 0.15, ease: "power3" });
    const yDot = gsap.quickTo(dot, "y", { duration: 0.15, ease: "power3" });
    const xRing = gsap.quickTo(ring, "x", { duration: 0.4, ease: "power3" });
    const yRing = gsap.quickTo(ring, "y", { duration: 0.4, ease: "power3" });

    window.addEventListener("mousemove", (e) => {
      xDot(e.clientX);
      yDot(e.clientY);
      xRing(e.clientX);
      yRing(e.clientY);
    });
    window.addEventListener("mousedown", () => ring.classList.add("is-down"));
    window.addEventListener("mouseup", () => ring.classList.remove("is-down"));

    const hoverSel = "a, button, .service-card, [data-magnetic], input, textarea";
    document.querySelectorAll(hoverSel).forEach((el) => {
      el.addEventListener("mouseenter", () => ring.classList.add("is-hover"));
      el.addEventListener("mouseleave", () => ring.classList.remove("is-hover"));
    });

    // Contextual cursor label (e.g. "Voir", "Lire", "Explorer")
    const label = document.querySelector(".cursor-label");
    if (label) {
      const xLbl = gsap.quickTo(label, "x", { duration: 0.2, ease: "power3" });
      const yLbl = gsap.quickTo(label, "y", { duration: 0.2, ease: "power3" });
      window.addEventListener("mousemove", (e) => {
        xLbl(e.clientX);
        yLbl(e.clientY);
      });
      document.querySelectorAll("[data-cursor]").forEach((el) => {
        el.addEventListener("mouseenter", () => {
          label.textContent = el.dataset.cursor;
          label.classList.add("show");
          ring.classList.add("is-media");
        });
        el.addEventListener("mouseleave", () => {
          label.classList.remove("show");
          ring.classList.remove("is-media");
        });
      });
    }
  }

  /* ======================================================================
     3. MAGNETIC BUTTONS
     ====================================================================== */
  if (finePointer && hasGsap && !reduced) {
    document.querySelectorAll("[data-magnetic]").forEach((el) => {
      const strength = parseFloat(el.dataset.magnetic) || 0.4;
      const xTo = gsap.quickTo(el, "x", { duration: 0.5, ease: "power3" });
      const yTo = gsap.quickTo(el, "y", { duration: 0.5, ease: "power3" });
      el.addEventListener("mousemove", (e) => {
        const r = el.getBoundingClientRect();
        xTo((e.clientX - (r.left + r.width / 2)) * strength);
        yTo((e.clientY - (r.top + r.height / 2)) * strength);
      });
      el.addEventListener("mouseleave", () => {
        xTo(0);
        yTo(0);
      });
    });
  }

  /* ======================================================================
     4. SPLIT-TEXT REVEALS
     ====================================================================== */
  // Recursively split text nodes into per-word / per-character spans while
  // preserving inner elements (e.g. <span class="text-gradient">). Template
  // indentation whitespace is normalized so titles never get a broken indent,
  // and real spaces stay as text nodes so long titles can wrap naturally.
  function wrapTextNode(node) {
    const raw = node.textContent;
    const hadLead = /^\s/.test(raw);
    const hadTrail = /\s$/.test(raw);
    const prev = node.previousSibling;
    const next = node.nextSibling;
    const words = raw.trim().split(/\s+/).filter(Boolean);
    if (!words.length) return;

    const frag = document.createDocumentFragment();
    if (hadLead && prev && prev.nodeType === Node.ELEMENT_NODE) {
      frag.appendChild(document.createTextNode(" "));
    }
    words.forEach((word, i) => {
      const wordSpan = document.createElement("span");
      wordSpan.className = "split-word";
      for (const ch of word) {
        const span = document.createElement("span");
        span.className = "split-char";
        span.textContent = ch;
        wordSpan.appendChild(span);
      }
      frag.appendChild(wordSpan);
      if (i < words.length - 1) frag.appendChild(document.createTextNode(" "));
    });
    if (hadTrail && next && next.nodeType === Node.ELEMENT_NODE) {
      frag.appendChild(document.createTextNode(" "));
    }
    node.parentNode.replaceChild(frag, node);
  }

  function splitToChars(el) {
    const nodes = [];
    el.childNodes.forEach((n) => nodes.push(n));
    nodes.forEach((n) => {
      if (n.nodeType === Node.TEXT_NODE && n.textContent.trim() !== "") {
        wrapTextNode(n);
      } else if (n.nodeType === Node.ELEMENT_NODE) {
        splitToChars(n);
      }
    });
    return el.querySelectorAll(".split-char");
  }

  if (hasGsap && !reduced) {
    document.querySelectorAll("[data-split]").forEach((el) => {
      const chars = splitToChars(el);
      el.classList.add("is-ready");
      gsap.set(el, { visibility: "visible" });
      gsap.from(chars, {
        yPercent: 120,
        opacity: 0,
        rotateX: -40,
        duration: 0.9,
        ease: "expo.out",
        stagger: 0.02,
        scrollTrigger: el.hasAttribute("data-split-scroll")
          ? { trigger: el, start: "top 85%", once: true }
          : undefined,
        delay: el.hasAttribute("data-split-scroll") ? 0 : 0.25,
      });
    });
  } else {
    document.querySelectorAll("[data-split]").forEach((el) => {
      el.style.visibility = "visible";
    });
  }

  /* ======================================================================
     5. 3D TILT CARDS
     ====================================================================== */
  if (finePointer && !reduced) {
    document.querySelectorAll("[data-tilt]").forEach((card) => {
      const max = 10;
      card.addEventListener("mousemove", (e) => {
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - 0.5;
        const py = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform =
          `perspective(900px) rotateY(${px * max}deg) rotateX(${-py * max}deg) translateY(-6px)`;
      });
      card.addEventListener("mouseleave", () => {
        card.style.transform = "perspective(900px) rotateY(0) rotateX(0)";
      });
    });
  }

  /* ======================================================================
     6. HERO MOUSE PARALLAX
     ====================================================================== */
  if (finePointer && hasGsap && !reduced) {
    const scene = document.querySelector("[data-parallax-scene]");
    if (scene) {
      const layers = scene.querySelectorAll("[data-depth]");
      scene.addEventListener("mousemove", (e) => {
        const cx = window.innerWidth / 2;
        const cy = window.innerHeight / 2;
        const dx = (e.clientX - cx) / cx;
        const dy = (e.clientY - cy) / cy;
        layers.forEach((l) => {
          const depth = parseFloat(l.dataset.depth) || 0.1;
          gsap.to(l, {
            x: -dx * 40 * depth,
            y: -dy * 40 * depth,
            duration: 0.8,
            ease: "power3.out",
          });
        });
      });
    }
  }

  /* ======================================================================
     7. SCROLL-VELOCITY REACTIVE MARQUEE
     ====================================================================== */
  if (hasGsap && !reduced) {
    const track = document.querySelector(".logo-track");
    if (track && window.ScrollTrigger) {
      const half = track.scrollWidth / 2;
      const base = gsap.to(track, {
        x: -half,
        duration: 26,
        ease: "none",
        repeat: -1,
        modifiers: { x: (x) => `${parseFloat(x) % half}px` },
      });
      let dir = 1;
      ScrollTrigger.create({
        onUpdate: (self) => {
          const v = self.getVelocity();
          if (v !== 0) dir = v < 0 ? -1 : 1;
          const boost = 1 + Math.min(Math.abs(v) / 400, 6);
          base.timeScale(dir * boost);
          gsap.to(base, { timeScale: dir * 1, duration: 0.6, overwrite: true });
        },
      });
    }
  }

  /* ======================================================================
     7b. KINETIC TYPOGRAPHY (opposite-direction infinite rows)
     ====================================================================== */
  if (hasGsap && !reduced) {
    const kinetics = [];
    document.querySelectorAll("[data-kinetic]").forEach((row) => {
      const dir = row.dataset.dir === "right" ? 1 : -1;
      const half = row.scrollWidth / 2;
      if (!half) return;
      const tween = gsap.fromTo(
        row,
        { x: dir < 0 ? 0 : -half },
        {
          x: dir < 0 ? -half : 0,
          duration: 24,
          ease: "none",
          repeat: -1,
        }
      );
      kinetics.push({ tween, dir });
    });
    // React to scroll velocity
    if (window.ScrollTrigger && kinetics.length) {
      ScrollTrigger.create({
        onUpdate: (self) => {
          const boost = 1 + Math.min(Math.abs(self.getVelocity()) / 300, 6);
          kinetics.forEach((k) => {
            k.tween.timeScale(boost);
            gsap.to(k.tween, { timeScale: 1, duration: 0.8, overwrite: true });
          });
        },
      });
    }
  }

  /* ======================================================================
     8. PINNED HORIZONTAL SCROLL
     ====================================================================== */
  if (hasGsap && window.ScrollTrigger && !reduced) {
    document.querySelectorAll("[data-hscroll]").forEach((section) => {
      const track = section.querySelector(".h-scroll-track");
      if (!track) return;
      if (window.innerWidth < 768) return; // vertical on mobile
      const distance = track.scrollWidth - window.innerWidth;
      gsap.to(track, {
        x: -distance,
        ease: "none",
        scrollTrigger: {
          trigger: section,
          start: "top top",
          end: () => "+=" + distance,
          scrub: 1,
          pin: true,
          anticipatePin: 1,
          invalidateOnRefresh: true,
        },
      });
    });
  }

  /* ======================================================================
     9. IMAGE / ELEMENT CLIP REVEAL
     ====================================================================== */
  if (hasGsap && window.ScrollTrigger && !reduced) {
    document.querySelectorAll("[data-clip]").forEach((el) => {
      gsap.to(el, {
        clipPath: "inset(0 0% 0 0)",
        duration: 1.2,
        ease: "expo.out",
        scrollTrigger: { trigger: el, start: "top 85%", once: true },
      });
    });
  }

  /* ======================================================================
     10. BACK-TO-TOP + PROGRESS RING
     ====================================================================== */
  (function backToTop() {
    const btn = document.getElementById("to-top");
    if (!btn) return;
    const fg = btn.querySelector(".fg");
    const R = 25;
    const CIRC = 2 * Math.PI * R;
    if (fg) {
      fg.style.strokeDasharray = CIRC;
      fg.style.strokeDashoffset = CIRC;
    }
    function update() {
      const y = window.scrollY;
      const h = document.documentElement.scrollHeight - window.innerHeight;
      const p = h > 0 ? y / h : 0;
      if (fg) fg.style.strokeDashoffset = CIRC * (1 - p);
      btn.classList.toggle("show", y > 500);
    }
    window.addEventListener("scroll", update, { passive: true });
    update();
    btn.addEventListener("click", () => {
      if (window.__lenis) window.__lenis.scrollTo(0, { duration: 0.7 });
      else window.scrollTo({ top: 0, behavior: "smooth" });
    });
  })();

  /* ======================================================================
     11. NAV: hide on scroll down, show on scroll up
     ====================================================================== */
  (function smartNav() {
    const nav = document.getElementById("navbar");
    if (!nav) return;
    let last = 0;
    window.addEventListener(
      "scroll",
      () => {
        const y = window.scrollY;
        if (y > 200 && y > last) {
          nav.style.transform = "translateY(-120%)";
        } else {
          nav.style.transform = "translateY(0)";
        }
        last = y;
      },
      { passive: true }
    );
  })();

  /* ======================================================================
     12. FAQ ACCORDION
     ====================================================================== */
  (function accordion() {
    document.querySelectorAll(".accordion").forEach((item) => {
      const trigger = item.querySelector(".accordion-trigger");
      const panel = item.querySelector(".accordion-panel");
      if (!trigger || !panel) return;
      trigger.addEventListener("click", () => {
        const open = item.classList.contains("open");
        // Close siblings for a clean single-open accordion feel
        item.parentElement
          .querySelectorAll(".accordion.open")
          .forEach((sib) => {
            if (sib !== item) {
              sib.classList.remove("open");
              sib.querySelector(".accordion-panel").style.maxHeight = null;
              sib.querySelector(".accordion-trigger").setAttribute("aria-expanded", "false");
            }
          });
        if (open) {
          item.classList.remove("open");
          panel.style.maxHeight = null;
          trigger.setAttribute("aria-expanded", "false");
        } else {
          item.classList.add("open");
          panel.style.maxHeight = panel.scrollHeight + "px";
          trigger.setAttribute("aria-expanded", "true");
        }
      });
    });
  })();

  /* ======================================================================
     13. TESTIMONIAL SLIDER (auto + dots)
     ====================================================================== */
  (function testimonials() {
    document.querySelectorAll("[data-testimonials]").forEach((root) => {
      const track = root.querySelector("[data-testimonial-track]");
      const slides = root.querySelectorAll("[data-testimonial-slide]");
      const dotsWrap = root.querySelector("[data-testimonial-dots]");
      if (!track || slides.length === 0) return;
      let index = 0;
      let timer;

      if (dotsWrap) {
        slides.forEach((_, i) => {
          const b = document.createElement("button");
          b.className = "t-dot";
          b.setAttribute("aria-label", "Slide " + (i + 1));
          b.addEventListener("click", () => go(i, true));
          dotsWrap.appendChild(b);
        });
      }
      const dots = dotsWrap ? dotsWrap.querySelectorAll(".t-dot") : [];

      function go(i, manual) {
        index = (i + slides.length) % slides.length;
        track.style.transform = `translateX(-${index * 100}%)`;
        dots.forEach((d, di) => d.classList.toggle("active", di === index));
        if (manual) restart();
      }
      function next() {
        go(index + 1);
      }
      function restart() {
        clearInterval(timer);
        if (!reduced) timer = setInterval(next, 6000);
      }
      go(0);
      restart();
      root.addEventListener("mouseenter", () => clearInterval(timer));
      root.addEventListener("mouseleave", restart);
    });
  })();

  /* ======================================================================
     14. PAGE TRANSITIONS (golden overlay sweep on internal navigation)
     ====================================================================== */
  (function pageTransition() {
    const overlay = document.getElementById("page-transition");
    if (!overlay || reduced) return;

    // Reveal-in on load
    overlay.classList.add("is-hidden");

    function isInternal(a) {
      if (!a || a.target === "_blank" || a.hasAttribute("download")) return false;
      const href = a.getAttribute("href") || "";
      if (
        href.startsWith("#") ||
        href.startsWith("mailto:") ||
        href.startsWith("tel:") ||
        href.startsWith("http")
      )
        return false;
      if (a.hostname && a.hostname !== window.location.hostname) return false;
      return true;
    }

    document.addEventListener("click", (e) => {
      const a = e.target.closest("a[href]");
      if (!a || !isInternal(a)) return;
      // Skip language form buttons, lightbox etc.
      if (a.getAttribute("href") === window.location.pathname) return;
      e.preventDefault();
      const url = a.href;
      overlay.classList.remove("is-hidden");
      overlay.classList.add("is-active");
      setTimeout(() => {
        window.location.href = url;
      }, 550);
    });

    window.addEventListener("pageshow", (e) => {
      if (e.persisted) {
        overlay.classList.remove("is-active");
        overlay.classList.add("is-hidden");
      }
    });
  })();

  if (hasGsap && window.ScrollTrigger) {
    window.addEventListener("load", () => ScrollTrigger.refresh());
  }
})();
