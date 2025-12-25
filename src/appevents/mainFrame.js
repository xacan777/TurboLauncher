import { BrowserWindow } from 'electron';
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib';

export default async function createMainWindow() {
  const win = new BrowserWindow({
    width: 1100,
    height: 800,
    skipTaskbar: false,
    autoHideMenuBar: true,
    frame: false,
    resizable: false,
    show: false,
    backgroundColor: '#161624',
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
    await win.loadURL('http://localhost:8080/#');
    if (!process.env.IS_TEST) win.webContents.openDevTools();
  } else {
    createProtocol('app');
    // Load the index.html when not in development
    // win.loadURL('app://./index.html');
    const setURL =
      process.env.NODE_ENV === 'development'
        ? 'http://localhost:8080/#'
        : `file://${__dirname}/index.html#`;
    await win.loadURL(setURL);
  }

  // win.webContents.openDevTools();

  return win;
}
