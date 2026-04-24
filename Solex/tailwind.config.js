module.exports = {
  content: [
    './solex/templates/**/*.html',
    './solex/static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        solex: { /* placeholder palette — Plan 4 replaces this */ },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
