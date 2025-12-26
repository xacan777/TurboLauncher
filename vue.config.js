const { defineConfig } = require('@vue/cli-service');
const path = require('path');

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src/'), // указывает, что '@' ссылается на каталог 'src'
      },
    },
  },
  pluginOptions: {
    electronBuilder: {
      nodeIntegration: true,
      outputDir: 'build',
      builderOptions: {
        // nsis: {
        //   oneClick: false,
        //   perMachine: true,
        //   allowToChangeInstallationDirectory: true,
        // },
        appId: 'com.turbo.launcher',
        productName: 'TURBO Launcher',
        copyright: 'TURBO',
        win: {
          icon: './public/icons/win.ico',
        },
        mac: {
          icon: './public/icons/mac.icns',
        },
      },
    },
  },
  css: {
    loaderOptions: {
      sass: {
        prependData: `
          @import "@/assets/styles/global.scss";
        `,
      },
    },
  },
  chainWebpack: (config) => {
    config.module
      .rule('vue')
      .use('vue-loader')
      .tap((options) => ({
        ...options,
        compilerOptions: {
          // treat any tag that starts with ion- as custom elements
          isCustomElement: (tag) => tag.startsWith('webview'),
        },
      }));
  },
});
