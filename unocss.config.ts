import {
  defineConfig,
  presetAttributify,
  presetIcons,
  presetTypography,
  presetUno,
  presetWebFonts,
  transformerDirectives,
  transformerVariantGroup,
} from 'unocss'

export default defineConfig({
  shortcuts: [
    ['btn', 'px-4 py-1 rounded inline-block bg-teal-700 text-white cursor-pointer hover:bg-teal-800 disabled:cursor-default disabled:bg-gray-600 disabled:opacity-50'],
    ['icon-btn', 'inline-block cursor-pointer select-none opacity-75 transition duration-200 ease-in-out hover:opacity-100 hover:text-teal-600'],
    [
      
      'bg-chichi', 'bg-blue-900 text-white font-bold py-2 px-4 rounded-full shadow-lg hover:bg-blue-800 focus:outline-none focus:shadow-outline transition duration-200 ease-in-out hover:bg-blue-700 focus:bg-blue-700 active:bg-blue-700 active:bg-blue-800 active:shadow-outline-teal-800',

    ],
    ['col', 'flex flex-col items-center'],
    ['row', 'flex flex-row']
  ],
  presets: [
    presetUno(),
    presetAttributify(),
    presetIcons({
      scale: 1.2,
      warn: true,
    }),
    presetTypography(),
    presetWebFonts({
      fonts: {
        sans: 'DM Sans',
        serif: 'DM Serif Display',
        mono: 'Fira Mono',
        script: 'DM Handwriting',
      },
    }),
  ],
  transformers: [
    transformerDirectives(),
    transformerVariantGroup(),
  ],
  safelist: 'prose prose-sm m-auto text-left'.split(' '),
})
