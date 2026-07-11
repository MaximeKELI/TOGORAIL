/* ==========================================================================
   Togo Rail — core UX (smooth scroll, navbar, menu, toasts, interactions)
   ========================================================================== */
(function () {
  "use strict";

  document.documentElement.classList.add("js");

  const prefersReduced = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  /* ---------- Native scrolling (Lenis smooth-scroll disabled) ----------
     We keep native browser scrolling for a normal, responsive feel.
     GSAP ScrollTrigger works natively, so all animations stay intact. */
  window.__lenis = null;

  // Smooth anchor jumps only (native scroll for the wheel/trackpad).
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    const id = a.getAttribute("href");
    if (id.length > 1) {
      a.addEventListener("click", (e) => {
        const target = document.querySelector(id);
        if (target) {
          e.preventDefault();
          const y = target.getBoundingClientRect().top + window.scrollY - 80;
          window.scrollTo({ top: y, behavior: "smooth" });
        }
      });
    }
  });

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

  /* ---------- Theme toggle (dark / light) ---------- */
  (function themeToggle() {
    const root = document.documentElement;
    const btn = document.getElementById("theme-toggle");
    function sync() {
      const dark = root.classList.contains("dark");
      if (btn) {
        const sun = btn.querySelector(".icon-sun");
        const moon = btn.querySelector(".icon-moon");
        if (sun) sun.classList.toggle("hidden", !dark);
        if (moon) moon.classList.toggle("hidden", dark);
      }
      const meta = document.querySelector('meta[name="theme-color"]');
      if (meta) meta.setAttribute("content", dark ? "#05070c" : "#f4f5f8");
    }
    sync();
    if (btn) {
      btn.addEventListener("click", () => {
        root.classList.toggle("dark");
        try {
          localStorage.setItem(
            "tr-theme",
            root.classList.contains("dark") ? "dark" : "light"
          );
        } catch (e) {}
        sync();
      });
    }
  })();

  /* ---------- Active section indicator (home in-page sections) ---------- */
  (function activeSection() {
    const sections = document.querySelectorAll("section[id]");
    if (!sections.length || !("IntersectionObserver" in window)) return;
    const links = document.querySelectorAll("#navbar a[href]");
    const map = {};
    links.forEach((l) => {
      const href = l.getAttribute("href") || "";
      const hash = href.split("#")[1];
      if (hash) map[hash] = l;
    });
    if (!Object.keys(map).length) return;
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting && map[en.target.id]) {
            links.forEach((l) => l.classList.remove("section-active"));
            map[en.target.id].classList.add("section-active");
          }
        });
      },
      { rootMargin: "-45% 0px -50% 0px" }
    );
    sections.forEach((s) => io.observe(s));
  })();

  /* ---------- Newsletter AJAX ---------- */
  (function newsletter() {
    const form = document.getElementById("newsletter-form");
    if (!form) return;
    const msg = document.getElementById("newsletter-msg");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = new FormData(form);
      try {
        const res = await fetch(form.action, {
          method: "POST",
          body: data,
          headers: { "X-Requested-With": "XMLHttpRequest" },
        });
        const json = await res.json();
        if (msg) {
          msg.textContent = json.message;
          msg.classList.remove("hidden");
          msg.style.color = json.ok ? "#c9a227" : "#f87171";
        }
        if (json.ok) form.reset();
      } catch (err) {
        if (msg) {
          msg.textContent = "Erreur réseau.";
          msg.classList.remove("hidden");
        }
      }
    });
  })();
})();
