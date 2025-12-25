import fs from 'fs';
import { crc32 } from 'crc';
import { BrowserWindow, Notification } from 'electron';

const md5FileReadStream = (path) =>
  new Promise((resolve) => {
    const stream = fs.createReadStream(path);
    let crc = null;
    stream.on('data', (data) => {
      if (crc) {
        crc = crc32(data, crc);
      } else {
        crc = crc32(data);
      }
    });
    stream.on('end', () => {
      resolve(crc ? crc.toString(16) : null);
    });
  });

const showNotify = ({ title = 'R2Legacy', message, pushOnFocus = true }) => {
  const focus = BrowserWindow.getAllWindows()[0].isFocused();
  const onShow = pushOnFocus ? true : !focus;
  if (onShow) {
    const notification = new Notification({
      title,
      body: message,
    });
    notification.show();
  }
};

export default {
  fileStream: md5FileReadStream,
  showNotify,
};
