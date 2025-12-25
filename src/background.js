/* eslint-disable no-unused-vars */
import { app, protocol, BrowserWindow, Menu, ipcMain, dialog, shell } from 'electron';

import loadingFrame from '@/appevents/loadingFrame';
import createAuthWindow from '@/appevents/authFrame';
import createMainWindow from '@/appevents/mainFrame';
import utility from './utility';
import DownloadManager from './downloader';
import { sSocket, sActions } from './server-connection/instances';

require('@electron/remote/main').initialize();

const isDevelopment = process.env.NODE_ENV !== 'production';

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  {
    scheme: 'app',
    privileges: {
      secure: true,
      standard: true,
    },
  },
]);

const downloadManager = new DownloadManager();

const menu = Menu.buildFromTemplate([
  {
    label: 'Edit',
    submenu: [
      {
        label: 'Undo',
        accelerator: 'CmdOrCtrl+Z',
        selector: 'undo:',
      },
      {
        label: 'Redo',
        accelerator: 'Shift+CmdOrCtrl+Z',
        selector: 'redo:',
      },
      {
        type: 'separator',
      },
      {
        label: 'Cut',
        accelerator: 'CmdOrCtrl+X',
        selector: 'cut:',
      },
      {
        label: 'Copy',
        accelerator: 'CmdOrCtrl+C',
        selector: 'copy:',
      },
      {
        label: 'Paste',
        accelerator: 'CmdOrCtrl+V',
        selector: 'paste:',
      },
      {
        label: 'Select All',
        accelerator: 'CmdOrCtrl+A',
        selector: 'selectAll:',
      },
    ],
  },
]);

Menu.setApplicationMenu(menu);

const writeFormData = async ({ command }) => {
  if (command === 'authFrame') {
    BrowserWindow.getAllWindows()[0].close();
    createAuthWindow().then((authWin) => {
      authWin.show();
    });
  } else if (command === 'mainFrame') {
    BrowserWindow.getAllWindows()[0].close();
    createMainWindow().then((mainWin) => {
      mainWin.webContents.session.clearCache(() => {
        console.log('clear cached');
      });
      mainWin.show();
    });
  } else if (command === 'selectFolder') {
    const { filePaths } = await dialog.showOpenDialog({
      properties: ['openDirectory'],
    });
    console.log('filePaths', filePaths);
    BrowserWindow.getAllWindows()[0].webContents.send('selectFolder', filePaths);
  } else if (command === 'startDownloadClient') {
    downloadManager.checkFilesHash();
  } else {
    app.quit();
  }
};
ipcMain.on('app-event', (event, args) => writeFormData(args));

ipcMain.on('download-path', (event, userPath) => {
  downloadManager.setSavePath(userPath);
  downloadManager.checkFilesHash();
});

ipcMain.on('download-pause', (event) => {
  downloadManager.pauseDownload();
});

ipcMain.on('start-gaming', (event, { param1, param2 }) => {
  downloadManager.startGaming(param1, param2);
});

// new logic of authorization
ipcMain.on('auth', (event, { login, password }) => {
  console.log(login, password);
  sActions
    .onLoginUser(login, password)
    .then((data) => {
      console.log(data);
      event.sender.send('auth-response', { success: true, data });
      // BrowserWindow.getAllWindows()[0].webContents.send('auth-response', { success: true, data });
    })
    .catch((err) => {
      console.log(err);
      event.sender.send('auth-response', { success: false, data: err });
      // BrowserWindow.getAllWindows()[0].webContents.send('auth-response', {
      //   success: false,
      //   data: err,
      // });
    });
});

ipcMain.on('notfy', (event, { title = 'R2Legacy', message, pushOnFocus = true }) => {
  utility.showNotify({
    title,
    message,
    pushOnFocus,
  });
});

app.on('web-contents-created', (createEvent, contents) => {
  contents.setWindowOpenHandler((data) => {
    const { url } = data;
    if (
      url.indexOf('https://pay.freekassa.ru') !== -1 ||
      url.indexOf('https://oplata.qiwi.com') !== -1
    ) {
      return {
        action: 'allow',
      };
    }
    setImmediate(() => {
      shell.openExternal(url);
    });
    return { action: 'deny' };
  });
});

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  // if (BrowserWindow.getAllWindows().length === 0) createWindow();
  if (BrowserWindow.getAllWindows().length === 0) loadingFrame();
});

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', async () => {
  sSocket.connectToServer();
  await loadingFrame();
});

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        app.quit();
      }
    });
  } else {
    process.on('SIGTERM', () => {
      app.quit();
    });
  }
}

export default app;
