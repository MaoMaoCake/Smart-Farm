/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,svelte,ts}"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
  themes: [
    {
      sf_dark: {
         "primary": "#38540A",

         "secondary": "#619230",

         "accent": "#1FB2A6",

         "neutral": "#D9D9D9",

         "base-100": "#1E1E1E",

         "info": "#3ABFF8",

         "success": "#36D399",

         "warning": "#FBBD23",

         "error": "#F87272",
      },
    },
  ],
},
}