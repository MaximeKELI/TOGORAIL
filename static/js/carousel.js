/* ==========================================================================
   Togo Rail — Premium carousel
   Autoplay + progress bar, arrows, dots, drag / swipe, GSAP easing.
   ========================================================================== */
(function () {
  "use strict";

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const hasGsap = !!window.gsap;
  const AUTOPLAY = 5500;

  document.querySelectorAll("[data-carousel]").forEach((root) => {
    const track = root.querySelector("[data-carousel-track]");
    const slides = Array.from(root.querySelectorAll("[data-carousel-slide]"));
    const dotsWrap = root.querySelector("[data-carousel-dots]");
    const prevBtn = root.querySelector("[data-carousel-prev]");
    const nextBtn = root.querySelector("[data-carousel-next]");
    const progress = root.querySelector("[data-carousel-progress]");
    if (!track || slides.length === 0) return;

    let index = 0;
    let timer = null;
    let progressAnim = null;

    // Build dots
    const dots = [];
    if (dotsWrap) {
      slides.forEach((_, i) => {
        const b = document.createElement("button");
        b.type = "button";
        b.setAttribute("aria-label", "Slide " + (i + 1));
        b.addEventListener("click", () => {
          goTo(i);
          restart();
        });
        dotsWrap.appendChild(b);
        dots.push(b);
      });
    }

    function move(animate) {
      const x = -index * 100;
      if (hasGsap && animate) {
        gsap.to(track, {
          xPercent: x,
          duration: 0.9,
          ease: "expo.out",
        });
      } else {
        track.style.transform = `translateX(${x}%)`;
      }
      dots.forEach((d, i) => d.classList.toggle("active", i === index));

      // Play video on active slide, pause others
      slides.forEach((s, i) => {
        const v = s.querySelector("video");
        if (!v) return;
        if (i === index) {
          v.play().catch(() => {});
        } else {
          v.pause();
        }
      });
    }

    function goTo(i) {
      index = (i + slides.length) % slides.length;
      move(true);
    }
    function next() {
      goTo(index + 1);
    }
    function prev() {
      goTo(index - 1);
    }

    // Autoplay + progress bar
    function startProgress() {
      if (!progress || reduced) return;
      if (progressAnim) progressAnim.kill && progressAnim.kill();
      if (hasGsap) {
        gsap.set(progress, { width: "0%" });
        progressAnim = gsap.to(progress, {
          width: "100%",
          duration: AUTOPLAY / 1000,
          ease: "none",
        });
      }
    }
    function play() {
      if (reduced) return;
      stop();
      startProgress();
      timer = setInterval(() => {
        next();
        startProgress();
      }, AUTOPLAY);
    }
    function stop() {
      if (timer) clearInterval(timer);
      timer = null;
      if (progressAnim && progressAnim.kill) progressAnim.kill();
    }
    function restart() {
      stop();
      play();
    }

    prevBtn && prevBtn.addEventListener("click", () => { prev(); restart(); });
    nextBtn && nextBtn.addEventListener("click", () => { next(); restart(); });

    // Pause on hover (desktop)
    root.addEventListener("mouseenter", stop);
    root.addEventListener("mouseleave", play);

    // Keyboard
    root.setAttribute("tabindex", "0");
    root.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") { prev(); restart(); }
      if (e.key === "ArrowRight") { next(); restart(); }
    });

    // Drag / swipe
    let startX = 0;
    let dragging = false;
    const viewport = root.querySelector(".carousel-viewport") || track;
    viewport.addEventListener("pointerdown", (e) => {
      dragging = true;
      startX = e.clientX;
      stop();
    });
    window.addEventListener("pointerup", (e) => {
      if (!dragging) return;
      dragging = false;
      const dx = e.clientX - startX;
      if (Math.abs(dx) > 60) {
        dx < 0 ? next() : prev();
      }
      play();
    });

    // Pause when off-screen
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(
        (entries) => {
          entries.forEach((en) => (en.isIntersecting ? play() : stop()));
        },
        { threshold: 0.2 }
      ).observe(root);
    }

    move(false);
    play();
  });
})();
