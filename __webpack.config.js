const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const BundleTracker = require('webpack-bundle-tracker');
const {ESBuildMinifyPlugin} = require('esbuild-loader');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const {trimEnd} = require('lodash');

const isDevelopment = process.env.NODE_ENV === 'development'


// This is the main configuration object.
// Here you write different options and tell Webpack what to do
module.exports = {
    watch: isDevelopment,
    // Path to your entry point. From this file Webpack will begin his work
    entry: [
        // Main App JS
        './frontend/js/index.js',
        //add other js file to compile it individually
        './frontend/scss/tailwind/tailwind.css',
        './frontend/scss/index.scss',

    ],

    // Path and filename of your result bundle.
    // Webpack will bundle all JavaScript into this file
    output: {
        path: path.resolve(__dirname, 'static/webpack_bundles'),
        filename: isDevelopment ? '[name].js' : '[name].[hash].js'
    },

    // Default mode for Webpack is production.
    // Depending on mode Webpack will apply different things
    // on final bundle. For now we don't need production's JavaScript
    // minifying and other thing so let's set mode to development
    mode: process.env.NODE_ENV,

    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            },
            {
                test: /\.((s[ac]ss)|(css))$/i,
                // include: path.resolve(__dirname, 'fronted/scss/tailwind/tailwind.css'),
                exclude: /(node_modules)/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader',
                        options: {
                            importLoaders: 1
                        }
                    },
                    {
                        loader: 'sass-loader',
                    },
                ],
            },
            {
                test: /\.css$/i,
                use: [
                    {
                        loader: 'postcss-loader',
                        options: {
                            postcssOptions: {
                                syntax: "postcss-scss",
                                plugins: [
                                    require("postcss-preset-env"),
                                    require("postcss-import")
                                ]
                            }
                        }
                    }
                ]

            },
            {
                test: /\.css$/i,
                exclude: /(node_modules)/,
                use: [
                    {
                        loader: 'postcss-loader',
                        options: {
                            postcssOptions: {
                                syntax: "postcss-scss",
                                plugins: [
                                    require("postcss-preset-env"),
                                    require("postcss-import")({}),
                                    require('postcss-fixes'),
                                    require("tailwindcss"),
                                    require("@fullhuman/postcss-purgecss")({
                                        content: ["**/*.html", "**/*.tsx", "**/*.svelte"],
                                        css: ["**/*.css"],
                                        defaultExtractor: (content) => {
                                            // Capture as liberally as possible, including things like `h-(screen-1.5)`
                                            const broadMatches =
                                                content.match(/[^<>"'`\s]*[^<>"'`\s:]/g) || [];
                                            const broadMatchesWithoutTrailingSlash = broadMatches.map(
                                                (match) => trimEnd(match, "\\")
                                            );

                                            // Capture classes within other delimiters like .block(class="w-1/2") in Pug
                                            const innerMatches =
                                                content.match(
                                                    /[^<>"'`\s.(){}[\]#=%]*[^<>"'`\s.(){}[\]#=%:]/g
                                                ) || [];

                                            return broadMatches
                                                .concat(broadMatchesWithoutTrailingSlash)
                                                .concat(innerMatches);
                                        },
                                    }),
                                    require("autoprefixer"),
                                    require("cssnano"),
                                    {"postcss-nested": {preserveEmpty: true}},
                                ],
                            },
                        }
                    },
                ],
            },
        ]
    },
    resolve: {
        extensions: ['.css', '.scss', '.js', '.jsx'],
        alias: {
            // Provides ability to include node_modules with ~
            '~': path.resolve(process.cwd(), 'src'),
        },
        modules: [path.resolve(__dirname, "src"), "node_modules"]
    },
    plugins: [
        new BundleTracker({filename: './static/webpack-stats.json'}),
        new MiniCssExtractPlugin({
            chunkFilename: '[id].css',
            filename: isDevelopment ? '[name].css' : '[name].[hash].css',
        })
    ],
    optimization: {
        minimize: true,
        minimizer: [
            new CssMinimizerPlugin(),
            new ESBuildMinifyPlugin({
                css: true
            })
        ],
    },
    stats: {},
    watchOptions: {
        ignored: path.resolve('node_modules')
    },
    devtool: 'source-map',
};
