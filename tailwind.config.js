/**
 * @format
 * @type {import('tailwindcss').Config}
 */

module.exports = {
	content: ["./src/**/*.{html,js}"],
	theme: {
		extend: {
      fontFamily: {
        'display': [ 'Noto Sans Display', 'sans-serif']
      }
    },
	},
	plugins: [],
};
