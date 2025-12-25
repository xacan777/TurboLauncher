import { BrowserWindow } from 'electron';
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib';

export default async () => {
  async function createLoaderWindow() {
    try {
      // Create the browser window.
      const win = new BrowserWindow({
        width: 300,
        height: 300,
        skipTaskbar: false,
        autoHideMenuBar: true,
        frame: false,
        resizable: false,
        transparent: true,
        webPreferences: {
          // Use pluginOptions.nodeIntegration, leave this alone
          nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
          contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION,
        },
      });

      if (process.env.WEBPACK_DEV_SERVER_URL) {
        // Load the url of the dev server if in development mode
        win.setMenuBarVisibility(false);
        await win.loadURL('http://localhost:8080/#/loader');
        // if (!process.env.IS_TEST) win.webContents.openDevTools();
      } else {
        createProtocol('app');
        // Load the index.html when not in development
        // win.loadURL('app://./index.html');
        const setURL =
          process.env.NODE_ENV === 'development'
            ? 'http://localhost:8080/#/loader'
            : `file://${__dirname}/index.html#/loader`;
        await win.loadURL(setURL);
        await win.show();
      }
    } catch (err) {
      console.log(err);
    }
  }

  await createLoaderWindow();
};
