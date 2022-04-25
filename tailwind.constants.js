/*
Light theme constants
*/

const {borderOpacity} = require("./tailwind.utils");
const {textOpacity} = require("./tailwind.utils");
const PRIMARY = 'rgb(0,58,173)'
const SECONDARY = 'rgb(173,0,0)'
const ACCENT = 'rgb(23,139,62)'
const TEXT = 'rgba(0,0,0,0.8)'
const SHADOW = 'rgba(0,0,0,0.17)'
const PRIMARY_SHADOW = 'rgba(0,58,173,0.17)'
const SECONDARY_SHADOW = 'rgba(255,0,0,0.17)'
const ACCENT_SHADOW = 'rgba(0,255,92,0.17)'
const CARD = 'rgb(255,255,255)'
const BACKGROUND = 'rgb(236,236,236)'
const HOVER = 'rgba(0,0,0,0.05)'
const BORDER = 'rgba(0,0,0,0.17)'
const MAIN_NAVIGATION = CARD
const MAIN_NAVIGATION_SECONDARY = CARD
const SIDE_NAVIGATION = CARD
const SIDE_NAVIGATION_SECONDARY = CARD
/*

Dark theme constants

*/
const {opacity} = require('./tailwind.utils')

const PRIMARY_DARK = 'rgb(79,131,229)'
const SECONDARY_DARK = 'rgb(187,79,79)'
const ACCENT_DARK = 'rgb(88,215,130)'
const TEXT_DARK = 'rgba(255,255,255,0.8)'
const SHADOW_DARK = 'rgba(255,255,255,0.17)'
const PRIMARY_SHADOW_DARK = 'rgba(0,95,255,0.17)'
const SECONDARY_SHADOW_DARK = 'rgba(255,0,0,0.17)'
const ACCENT_SHADOW_DARK = 'rgba(0,255,27,0.17)'
const CARD_DARK = 'rgb(38,46,59)'
const BACKGROUND_DARK = 'rgb(26,31,40)'
const HOVER_DARK = 'rgba(255,255,255,0.05)'
const BORDER_DARK = 'rgba(255,255,255,0.25)'
const MAIN_NAVIGATION_DARK = CARD_DARK
const MAIN_NAVIGATION_SECONDARY_DARK = CARD_DARK
const SIDE_NAVIGATION_DARK = CARD_DARK
const SIDE_NAVIGATION_SECONDARY_DARK = CARD_DARK

const main_colors = {
    'primary': opacity('--primary'),
    'secondary': opacity('--secondary'),
    'accent': opacity('--accent'),
    'main-text': opacity('--text'),
    'shadow': opacity('--shadow'),
    'card': opacity('--card'),
    'main-bg': opacity('--background'),
    'main-nav': opacity('--main-nav'),
    'hover': opacity('--hover'),
    'border': opacity('--border'),
}

const text_colors = {
    'primary': textOpacity('--primary'),
    'secondary': textOpacity('--secondary'),
    'accent': textOpacity('--accent'),
    'main-text': textOpacity('--text'),
    'shadow': textOpacity('--shadow'),
    'card': textOpacity('--card'),
    'main-bg': textOpacity('--background'),
    'hover': textOpacity('--hover'),
    'border': textOpacity('--border'),
}
const border_colors = {
    'primary': borderOpacity('--primary'),
    'secondary': borderOpacity('--secondary'),
    'accent': borderOpacity('--accent'),
    'main-text': borderOpacity('--text'),
    'shadow': borderOpacity('--shadow'),
    'card': borderOpacity('--card'),
    'main-bg': borderOpacity('--main-nav'),
    'hover': borderOpacity('--hover'),
    'border': borderOpacity('--border'),
}

module.exports = {
    main_colors,
    text_colors,
    border_colors,
}