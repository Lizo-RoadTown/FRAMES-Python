/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Ascent Basecamp brand colors
        primary: {
          50: '#e6f0ff',
          100: '#b3d1ff',
          200: '#80b3ff',
          300: '#4d94ff',
          400: '#1a75ff',
          500: '#0056e0',
          600: '#0044b3',
          700: '#003380',
          800: '#00224d',
          900: '#00111a',
        },
        secondary: {
          50: '#fff5e6',
          100: '#ffe0b3',
          200: '#ffca80',
          300: '#ffb54d',
          400: '#ff9f1a',
          500: '#e68900',
          600: '#b36b00',
          700: '#804d00',
          800: '#4d2e00',
          900: '#1a1000',
        },
        success: '#10b981',
        warning: '#f59e0b',
        error: '#ef4444',
        info: '#3b82f6',
        
        // Competency levels
        orientation: '#3b82f6',
        competency: '#10b981',
        integration: '#8b5cf6',
        autonomy: '#f59e0b',
        
        // Race celebration colors
        legendary: '#fbbf24',
        excellent: '#8b5cf6',
        good: '#3b82f6',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['Fira Code', 'monospace'],
      },
      boxShadow: {
        'card': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'card-hover': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'confetti': 'confetti 2s ease-in-out',
        'fireworks': 'fireworks 3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        confetti: {
          '0%': { transform: 'translateY(-100vh) rotate(0deg)' },
          '100%': { transform: 'translateY(100vh) rotate(720deg)' },
        },
        fireworks: {
          '0%, 100%': { opacity: '0', transform: 'scale(0.5)' },
          '50%': { opacity: '1', transform: 'scale(1.2)' },
        },
      },
    },
  },
  plugins: [],
  darkMode: 'class',
}
