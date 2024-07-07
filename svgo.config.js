/*
* * SVGO Configuration
* * SVGO is used to optimize and minify SVG files in the library.
* */

module.exports = {
  multipass: true,
  plugins: [

    // Enable built-in plugins with an object to configure plugins
    {
      name: 'preset-default',
      params: {
        overrides: {
          // Disable remove viewbox
          removeViewBox: false,

          // disable a default plugin
          cleanupIds: false,

          // customize the params of a default plugin
          inlineStyles: {
            onlyMatchedOnce: false,
          }
        }
      }
    }
  ]
};
