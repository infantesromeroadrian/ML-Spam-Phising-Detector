/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'dark-bg': '#0a0e27',
        'dark-card': '#141937',
        'neon-cyan': '#00d9ff',
        'neon-purple': '#a855f7',
        'threat-high': '#ef4444',
        'threat-medium': '#f59e0b',
        'threat-low': '#10b981',
      },
    },
  },
  plugins: [],
}
