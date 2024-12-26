/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./bookstore/templates/bookstore/**/*.html", // Includes all HTML files in the bookstore folder and its subdirectories
  ],
  theme: {
    extend: {
      fontFamily: {
        roboto: ["Roboto", "sans-serif"],
        openSans: ["Open Sans", "sans-serif"],
      },
    },
  },
  plugins: [],
};
