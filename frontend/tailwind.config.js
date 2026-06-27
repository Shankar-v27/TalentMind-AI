/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
      },
      colors: {
        /* Tailwind CSS custom vars */
        border: "hsl(var(--border))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        muted: { DEFAULT: "hsl(var(--muted))", foreground: "hsl(var(--muted-foreground))" },
        card: { DEFAULT: "hsl(var(--card))", foreground: "hsl(var(--card-foreground))" },
        primary: { DEFAULT: "hsl(var(--primary))", foreground: "hsl(var(--primary-foreground))" },
        accent: { DEFAULT: "hsl(var(--accent))", foreground: "hsl(var(--accent-foreground))" },

        /* Enterprise palette */
        tm: {
          base: "#09090B",
          elevated: "#111113",
          surface: "#18181B",
          subtle: "#27272A",
        },
      },
      boxShadow: {
        "glow-sm":     "0 0 12px rgba(37,99,235,0.25)",
        "glow":        "0 0 32px rgba(37,99,235,0.35), 0 0 64px rgba(37,99,235,0.15)",
        "glow-violet": "0 0 32px rgba(124,58,237,0.3), 0 0 64px rgba(124,58,237,0.12)",
        "glow-cyan":   "0 0 32px rgba(14,165,233,0.25), 0 0 64px rgba(14,165,233,0.1)",
        "glow-emerald":"0 0 24px rgba(16,185,129,0.3)",
        "elevation-1": "0 1px 3px rgba(0,0,0,0.5)",
        "elevation-2": "0 4px 20px rgba(0,0,0,0.55)",
        "elevation-3": "0 12px 48px rgba(0,0,0,0.65)",
        "elevation-4": "0 24px 80px rgba(0,0,0,0.75)",
      },
      borderRadius: {
        "2xl": "1rem",
        "3xl": "1.5rem",
        "4xl": "2rem",
      },
      backdropBlur: {
        xs: "4px",
        "4xl": "64px",
      },
      animation: {
        "float":      "float 6s ease-in-out infinite",
        "spin-slow":  "spin 12s linear infinite",
        "ping-slow":  "ping 3s cubic-bezier(0,0,0.2,1) infinite",
        "shimmer":    "shimmer 1.8s infinite",
        "glow-pulse": "glowPulse 2s ease-in-out infinite",
        "slide-up":   "slideUp 0.5s cubic-bezier(0.4,0,0.2,1)",
        "fade-in":    "fadeIn 0.4s ease",
        "scale-in":   "scaleIn 0.3s cubic-bezier(0.4,0,0.2,1)",
        "border-flow":"borderFlow 4s linear infinite",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-8px)" },
        },
        shimmer: {
          "0%":   { backgroundPosition: "200% 0" },
          "100%": { backgroundPosition: "-200% 0" },
        },
        glowPulse: {
          "0%, 100%": { opacity: "0.7" },
          "50%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(16px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        scaleIn: {
          "0%": { opacity: "0", transform: "scale(0.94)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        borderFlow: {
          "0%": { backgroundPosition: "0% 50%" },
          "100%": { backgroundPosition: "200% 50%" },
        },
      },
      typography: {
        DEFAULT: { css: { color: "rgba(255,255,255,0.8)" } },
      },
      spacing: {
        "18": "4.5rem",
        "22": "5.5rem",
        "68": "17rem",
        "72": "18rem",
        "76": "19rem",
        "80": "20rem",
      },
    },
  },
  plugins: [],
};
