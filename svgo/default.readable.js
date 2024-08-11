module.exports = {
  js2svg: { indent: 2, pretty: true },
  plugins: [
    {
      name: 'preset-default',
      params: {
        overrides: {
          removeUselessStrokeAndFill: { removeNone: true },
          removeViewBox: false
        }
      }
    }
  ]
};