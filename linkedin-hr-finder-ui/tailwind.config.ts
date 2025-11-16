import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        linkedin: {
          50: '#e7f3ff',
          100: '#d0e7ff',
          200: '#a8d5ff',
          300: '#74bbff',
          400: '#3d97ff',
          500: '#0a66c2',
          600: '#004182',
          700: '#002e5f',
          800: '#001f3f',
          900: '#001529',
        },
      },
    },
  },
  plugins: [],
}
export default config
