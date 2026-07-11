/* ==========================================================================
   Togo Rail — core UX (smooth scroll, navbar, menu, toasts, interactions)
   ========================================================================== */
(function () {
  "use strict";

  document.documentElement.classList.add("js");

  const prefersReduced = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  /* ---------- Lenis smooth scrolling ---------- */
  let lenis = null;
  if (window.Lenis && !prefersReduced) {
    lenis = new Lenis({
      lerp: 0.2,
      wheelMultiplier: 1.6,
      touchMultiplier: 2,
      smoothWheel: true,
    });

    function raf(time) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);
    window.__lenis = lenis;

    // Anchor links routed through Lenis
    document.querySelectorAll('a[href^="#"]').forEach((a) => {
      const id = a.getAttribute("href");
      if (id.length > 1) {
        a.addEventListener("click", (e) => {
          const target = document.querySelector(id);
          if (target) {
            e.preventDefault();
            lenis.scrollTo(target, { offset: -80, duration: 0.8 });
          }
        });
      }
    });
  }

  /* ---------- Navbar: scrolled state + scroll progress ---------- */
  const navbar = document.getElementById("navbar");
  const progress = document.getElementById("scroll-progress");

  function onScroll() {
    const y = window.scrollY || document.documentElement.scrollTop;
    if (navbar) navbar.classList.toggle("scrolled", y > 40);
    if (progress) {
      const h =
        document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = (h > 0 ? (y / h) * 100 : 0) + "%";
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile menu ---------- */
  const toggle = document.getElementById("menu-toggle");
  const menu = document.getElementById("mobile-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", () => {
      menu.classList.toggle("hidden");
      const bars = toggle.querySelectorAll("[data-bar]");
      const open = !menu.classList.contains("hidden");
      bars[0].style.transform = open
        ? "translateY(4px) rotate(45deg)"
        : "";
      bars[1].style.transform = open
        ? "translateY(-2px) rotate(-45deg)"
        : "";
    });
    menu.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => menu.classList.add("hidden"))
    );
  }

  /* ---------- Toast auto-dismiss ---------- */
  document.querySelectorAll("[data-toast]").forEach((t) => {
    setTimeout(() => {
      t.style.transition = "opacity .5s ease, transform .5s ease";
      t.style.opacity = "0";
      t.style.transform = "translateX(20px)";
      setTimeout(() => t.remove(), 500);
    }, 5000);
  });

  /* ---------- Service card cursor glow tracking ---------- */
  document.querySelectorAll(".service-card").forEach((card) => {
    card.addEventListener("mousemove", (e) => {
      const r = card.getBoundingClientRect();
      card.style.setProperty("--mx", `${e.clientX - r.left}px`);
      card.style.setProperty("--my", `${e.clientY - r.top}px`);
    });
  });

  /* ---------- Current year (fallback) ---------- */
  document
    .querySelectorAll("[data-year]")
    .forEach((el) => (el.textContent = new Date().getFullYear()));
})();
