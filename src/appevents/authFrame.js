import { BrowserWindow } from 'electron';
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib';

export default async function createAuthWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    skipTaskbar: false,
    autoHideMenuBar: true,
    frame: false,
    resizable: false,
    show: false,
    backgroundColor: '#312450',
    webPreferences: {
      webviewTag: true,
      nodeIntegration: true,
      webSecurity: false,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION,
    },
  });

  // eslint-disable-next-line global-require
  require('@electron/remote/main').enable(win.webContents);

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    win.setMenuBarVisibility(false);
    await win.loadURL('http://localhost:8080/#/login');
    if (!process.env.IS_TEST) win.webContents.openDevTools();
  } else {
    createProtocol('app');
    // Load the index.html when not in development
    // win.loadURL('app://./index.html');
    const setURL =
      process.env.NODE_ENV === 'development'
        ? 'http://localhost:8080/#/login'
        : `file://${__dirname}/index.html#/login`;
    await win.loadURL(setURL);
  }

  return win;
}
