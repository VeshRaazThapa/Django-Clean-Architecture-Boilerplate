const {border_colors} = require("./tailwind.constants");
const {text_colors} = require("./tailwind.constants");
const {main_colors} = require("./tailwind.constants");
module.exports = {
    mode: process.env.NODE_ENV === 'production' ? 'production' : 'jit',
    // prefix:'t',
    purge: [
        './**/*.html',
        './apps/**/*.html',
        './frontend/**/*.js',
        './frontend/**/*.css',
        './frontend/**/*.scss',
    ],
    darkMode: 'media', // or 'media' or 'class'
    theme: {
        extend: {
            colors: {...main_colors},
            borderColor: {...border_colors},
            textColor: {...text_colors},
            fontFamily: {
                'caption': ['Poppins', 'sans-serif'],
                'body': ['Roboto', 'sans-serif'],
            }
        },
    },
    variants: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/forms'),
    ],
}





