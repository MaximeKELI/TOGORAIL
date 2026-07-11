/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./templates/**/*.html",
    "./core/**/*.py",
    "./static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#05070c",
        navy: "#0a1628",
        panel: "#0b1220",
        gold: "#c9a227",
        goldsoft: "#e8d48b",
        muted: "#9aa3b5",
      },
      fontFamily: {
        display: ["Syne", "sans-serif"],
        body: ["'DM Sans'", "sans-serif"],
      },
      boxShadow: {
        glow: "0 0 40px rgba(201,162,39,0.25)",
        glowlg: "0 0 80px rgba(201,162,39,0.20)",
      },
      keyframes: {
        shimmer: { "100%": { transform: "translateX(100%)" } },
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
