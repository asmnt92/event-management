/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./templates/**/*.html", // Templates at the project level or rot level 
      "./**/templates/**/*.html", // Templates inside apps
    ],
    theme: {
      extend: {},
    },
    plugins: [],
  };