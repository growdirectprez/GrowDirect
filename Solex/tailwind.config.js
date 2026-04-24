module.exports = {
  content: [
    './solex/templates/**/*.html',
    './solex/static/js/**/*.js',
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Cormorant Garamond"', 'Georgia', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        solex: {
          // Earthy wellness palette — tune after real screenshots
          ink:    '#1C1C1A',   // headers, body on white
          body:   '#3F3F3B',
          muted:  '#8A8A84',
          line:   '#E5E2DC',
          cream:  '#F7F4EE',   // page background
          sand:   '#E8E0D1',   // subtle section background
          leaf:   '#5E7A5A',   // accent (buttons, links hover)
          teal:   '#1F5961',   // primary accent (CTAs, logo)
          gold:   '#B79355',   // secondary accent (badges, highlights)
          clay:   '#A35E3E',   // tertiary (labels, alerts)
        },
      },
      maxWidth: {
        content: '76rem',      // 1216px narrow content
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
      },
      borderRadius: {
        'brand': '0.25rem',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
