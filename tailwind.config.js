module.exports = {
  content: ['./index.html', './src/*/**.{ts,vue,md}'],
  css: ['src/styles/main.css'],
  plugins: [require('daisyui')],
  daisyui: {
    themes: [{
      'cloudapp': {
        'primary': '#14EED1',
        'secondary': '#2B5EBF',
        'accent': '#0E766E',
        'info': '#0C2E59',
        'success': '#66FF33',
        'warning': '#EC690E',
        'error': '#653DF1'
    }}]
  }}