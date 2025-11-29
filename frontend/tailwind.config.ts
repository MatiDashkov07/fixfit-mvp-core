import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // FixFit brand colors
        primary: {
          DEFAULT: "#10B981",
          dark: "#059669",
        },
        error: {
          DEFAULT: "#EF4444",
          dark: "#DC2626",
        },
        background: "#0F172A",
        surface: "#1E293B",
        text: {
          primary: "#F8FAFC",
          secondary: "#94A3B8",
        },
      },
      fontFamily: {
        sans: ["var(--font-geist-sans)", "system-ui", "sans-serif"],
        mono: ["var(--font-geist-mono)", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;

