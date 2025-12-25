/**
 * Author @mrs4z
 * 07.10.2023
 * @link www.bytecrafter.ru
 * @info Initial Socket connetion to LOGIN SERVER
 */

import * as net from 'net';

// eslint-disable-next-line import/prefer-default-export
export class SSocket {
  constructor() {
    console.log('INIT SOCKET!');
    if (SSocket.instance) {
      // eslint-disable-next-line no-constructor-return
      return SSocket.instance;
    }

    this.clientSocket = new net.Socket();
    this.ip = null;
    this.port = null;

    this.BUFFER_SIZE = 2048;

    this.debugEnabled = true;

    SSocket.instance = this;
  }

  setConnectionConfiguration(ip, port) {
    this.ip = ip;
    this.port = port;
  }

  connectToServer() {
    console.log('START CONNECTION SOCKET');
    return new Promise((resolve, reject) => {
      if (!this.clientSocket.connecting && !this.clientSocket.destroyed) {
        this.clientSocket.connect(this.port, this.ip, () => {
          console.log('SOCKET CONNECTED');
          resolve(true);
        });

        // eslint-disable-next-line no-unused-vars
        this.clientSocket.on('error', (_err) => {
          // eslint-disable-next-line prefer-promise-reject-errors
          reject(false);
        });
      } else {
        resolve(true);
      }
    });
  }

  sendData(str) {
    return new Promise((resolve, reject) => {
      if (!this.clientSocket.connecting) {
        const buffer = this.xorEncode(Buffer.from(str, 'utf8'));

        this.clientSocket.write(buffer, (err) => {
          if (err) {
            // eslint-disable-next-line prefer-promise-reject-errors
            reject(false);
          } else {
            resolve(true);
          }
        });
      } else {
        resolve(false);
      }
    });
  }

  receiveData() {
    return new Promise((resolve, reject) => {
      this.clientSocket.once('data', (buffer) => {
        if (buffer.length > 0) {
          const decodedData = this.xorDecode(buffer);
          resolve(decodedData.toString('utf8'));
        } else {
          resolve('');
        }
      });

      this.clientSocket.on('error', (err) => {
        console.error('Error:', err.message);
        // eslint-disable-next-line prefer-promise-reject-errors
        reject('');
      });
    });
  }

  // private utils
  // eslint-disable-next-line class-methods-use-this
  xorEncode(buffer) {
    const out = Buffer.alloc(buffer.length + 2);
    out[0] = Math.floor(Math.random() * 224) + 1;
    out[1] = Math.floor(Math.random() * 96) + 4;

    // eslint-disable-next-line no-plusplus
    for (let i = 0; i < buffer.length; i++) {
      // eslint-disable-next-line no-bitwise
      out[i + 2] = out[i + 2] ^ out[1];
      // eslint-disable-next-line no-bitwise
      out[i + 2] = out[i + 2] ^ 24;
      // eslint-disable-next-line no-bitwise
      out[i + 2] = buffer[i] ^ out[0];
    }

    // eslint-disable-next-line no-bitwise
    out[0] ^= out[1];
    return out;
  }

  // eslint-disable-next-line class-methods-use-this
  xorDecode(buffer) {
    const out = Buffer.alloc(buffer.length - 2);
    let a = 0;

    // eslint-disable-next-line no-plusplus
    for (let i = 2; i < buffer.length; i++) {
      // eslint-disable-next-line operator-assignment, no-bitwise
      out[a] = out[a] ^ buffer[1];
      // eslint-disable-next-line operator-assignment, no-bitwise
      out[a] = out[a] ^ 24;
      // eslint-disable-next-line operator-assignment, no-bitwise
      out[a] = buffer[i] ^ (buffer[0] ^ buffer[1]);
      // eslint-disable-next-line no-plusplus
      a++;
    }

    return out;
  }
}
