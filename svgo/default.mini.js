module.exports = {
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