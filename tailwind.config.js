module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      spacing:{ // 왼쪽은 class name, 오른쪽은 css
        "25vh": "25vh",
        "50vh": "50vh",
        "60vh": "60vh",
        "75vh": "75vh"
      },
      borderRadius: {
        "xl": "1.5rem"
      },
      minHeight: {
        "50vh": "50vh",
        "75vh": "75vh"
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
