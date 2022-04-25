const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const {CleanWebpackPlugin} = require('clean-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');

const isDevelopment = process.env.NODE_ENV === 'development'


// This is the main configuration object.
// Here you write different options and tell Webpack what to do
module.exports = {
    watch: (process.env.NODE_ENV !== 'development' && process.env.NODE_ENV !== 'production'),
    // Path to your entry point. From this file Webpack will begin his work
    entry: [
        // Main App JS
        './frontend/js/index.js'
        //add other js file to compile it individually
        , './frontend/scss/index.scss',
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
                test: /\.(jpg|jpeg|png|gif|mp3|svg)$/,
                use: ["file-loader"]
            },
            {
                test: /\.js$/,
                exclude: /(node_modules)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            },
            {
                test: /\.module\.s(a|c)ss$/,
                loader: [
                    isDevelopment ? 'style-loader' : MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader',
                        options: {
                            modules: true,
                            sourceMap: isDevelopment
                        }
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: isDevelopment
                        }
                    }
                ]
            },
            {
                test: /\.css$/i,
                use: [MiniCssExtractPlugin.loader, 'css-loader'],
            },
            {
                test: /\.s(a|c)ss$/,
                exclude: /\.module.(s(a|c)ss)$/,
                loader: [
                    isDevelopment ? 'style-loader' : MiniCssExtractPlugin.loader,
                    'css-loader',
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: isDevelopment
                        }
                    }
                ]
            },
            {
            test: /\.(png|woff|woff2|eot|ttf|svg|jpg)$/,
                loader: 'url-loader'
            }
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
        new CleanWebpackPlugin(),
        new BundleTracker({filename: './static/webpack-stats.json'}),
        new MiniCssExtractPlugin({
            chunkFilename: '[id].css',
            filename: isDevelopment ? '[name].css' : '[name].[hash].css',
            // filename: '[name].css',
            // chunkFilename: '[id].css'
        })
    ],
    optimization: {
        minimize: true,
        minimizer: [
            // For webpack@5 you can use the `...` syntax to extend existing minimizers (i.e. `terser-webpack-plugin`), uncomment the next line
            // `...`,
            new CssMinimizerPlugin(),
        ],
    },

};
