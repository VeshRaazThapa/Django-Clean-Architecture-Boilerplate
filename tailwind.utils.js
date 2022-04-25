// converts any color into rgba. Returns list of r,g,b,a value
/*
Examples:
    colorValues('transparent'); // [0,0,0,0]
    colorValues('white'); // [255, 255, 255, 1]
    colorValues('teal'); // [0, 128, 128, 1]
    colorValues('rgba(11,22,33,.44)'); // [11, 22, 33, 0.44]
    colorValues('rgb(11,22,33)'); // [11, 22, 33, 1]
    colorValues('#abc'); // [170, 187, 204, 1]
    colorValues('#abc6'); // [170, 187, 204, 0.4]
    colorValues('#aabbcc'); // [170, 187, 204, 1]
    colorValues('#aabbcc66'); // [170, 187, 204, 0.4]
    colorValues('asdf'); // undefined
    colorValues(''); // undefined
    colorValues(NaN); // Script Error
    colorValues(123); // Script Error
*/

function colorValues(color) {
    if (!color)
        return;
    if (color.toLowerCase() === 'transparent')
        return [0, 0, 0, 0];
    if (color[0] === '#') {
        if (color.length < 7) {
            // convert #RGB and #RGBA to #RRGGBB and #RRGGBBAA
            color = '#' + color[1] + color[1] + color[2] + color[2] + color[3] + color[3] + (color.length > 4 ? color[4] + color[4] : '');
        }
        return [parseInt(color.substr(1, 2), 16),
            parseInt(color.substr(3, 2), 16),
            parseInt(color.substr(5, 2), 16),
            color.length > 7 ? parseInt(color.substr(7, 2), 16) / 255 : 1];
    }
    if (color.indexOf('rgb') === -1) {
        // convert named colors
        var temp_elem = document.body.appendChild(document.createElement('fictum')); // intentionally use unknown tag to lower chances of css rule override with !important
        var flag = 'rgb(1, 2, 3)'; // this flag tested on chrome 59, ff 53, ie9, ie10, ie11, edge 14
        temp_elem.style.color = flag;
        if (temp_elem.style.color !== flag)
            return; // color set failed - some monstrous css rule is probably taking over the color of our object
        temp_elem.style.color = color;
        if (temp_elem.style.color === flag || temp_elem.style.color === '')
            return; // color parse failed
        color = getComputedStyle(temp_elem).color;
        document.body.removeChild(temp_elem);
    }
    if (color.indexOf('rgb') === 0) {
        if (color.indexOf('rgba') === -1)
            color += ',1'; // convert 'rgb(R,G,B)' to 'rgb(R,G,B)A' which looks awful but will pass the regxep below
        return color.match(/[\.\d]+/g).map(function (a) {
            return +a
        });
    }
}

function removeSpace(string) {
    return string.replace(' ', '')
}

const bgOpacity = function (color) {
    return () => {
        let colorValue = colorValues(removeSpace(color));
        let r, g, b, a, finalColor
        r = colorValue[0]
        g = colorValue[1]
        b = colorValue[2]
        return `rgba(${r}, ${g}, ${b}, var(--tw-bg-opacity))`
    }
}

const opacity = function (color) {
    return ({opacity}) => {
        let a, finalColor
        finalColor = `rgba(var(${color}),var(--tw-bg-opacity))`
        return finalColor
    }
}
const textOpacity = function (color) {
    return ({opacity}) => {
        let a, finalColor
        finalColor = `rgba(var(${color}),var(--tw-text-opacity))`
        return finalColor
    }
}
const borderOpacity = function (color) {
    return ({opacity}) => {
        let a, finalColor
        finalColor = `rgba(var(${color}),var(--tw-border-opacity))`
        return finalColor
    }
}


module.exports = {
    opacity: opacity,
    textOpacity: textOpacity,
    borderOpacity: borderOpacity,
}