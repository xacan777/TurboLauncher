/* eslint-disable prefer-promise-reject-errors */
/**
 * Author @mrs4z
 * 07.10.2023
 * @link www.bytecrafter.ru
 * @info Client start and Authorization user
 */
import * as crypto from 'crypto';

// eslint-disable-next-line import/prefer-default-export
export class SActions {
  constructor(sSocket) {
    if (SActions.instance) {
      // eslint-disable-next-line no-constructor-return
      return SActions.instance;
    }

    this.s_socket = sSocket;
    this.s_token = null;

    SActions.instance = this;
  }

  setClientPath(clientPath) {
    this.s_clientPath = clientPath;
  }

  setSocket(socket) {
    this.s_socket = socket;
  }

  onLoginUser(login, password) {
    // eslint-disable-next-line no-async-promise-executor
    return new Promise(async (resolve, reject) => {
      // todo: authorization logic
      try {
        console.log('on strt');
        // step one - get hash
        await this.s_socket.sendData(this.base64DecodeEx('W0pATl9UT0pfSlRfLTo7OzotZX5nZw==', 11));
        const receiveHashData = await this.s_socket.receiveData();
        if (receiveHashData) {
          const receivedDataFormatted = receiveHashData.split('&');
          if (receivedDataFormatted.length === 3) {
            const hashedData = receivedDataFormatted[2];

            // hook for socket waitor after receiver
            // eslint-disable-next-line no-promise-executor-return
            await new Promise((res) => setTimeout(res, 2000));

            // authorization sender
            await this.s_socket.sendData(
              `${
                this.base64DecodeEx('loeNg5KZgoeSh5mS4Pf29vTg', 198) + hashedData
              }&${login}&${this.sha1Hash(password)}&11111111111111111111111111111111 `
            );
            const receiveAuthorizationData = await this.s_socket.receiveData();
            if (receiveAuthorizationData) {
              const dataFormatter = receiveAuthorizationData.split('&');
              // eslint-disable-next-line no-unused-vars
              const [_, code, param1, param2, param3] = dataFormatter;

              // eslint-disable-next-line eqeqeq
              if (code == 1002) {
                const paramResponse1 = `${param2}|${param1.replace('|', '_')}`;
                const paramResponse2 =
                  '1063763511 1063759441 1063763736 1063763511 1063763782 1063758637';
                resolve({
                  param1: paramResponse1,
                  param2: paramResponse2,
                });
              } else {
                reject(receiveAuthorizationData);
              }
            } else {
              reject('Invalid Authorization');
            }
          } else {
            reject('Invalid Get Hash #2');
          }
        } else {
          reject('Invalid Get Hash #1');
        }
      } catch (err) {
        reject(err);
      }
    });
  }

  static async onStartClient() {
    // todo: actions start client with token
    return true;
  }

  // eslint-disable-next-line class-methods-use-this
  base64DecodeEx(base64EncodedData, xor) {
    const base64DecodedBuffer = Buffer.from(base64EncodedData, 'base64');
    // eslint-disable-next-line no-plusplus
    for (let i = 0; i < base64DecodedBuffer.length; i++) {
      // eslint-disable-next-line operator-assignment, no-bitwise
      base64DecodedBuffer[i] = base64DecodedBuffer[i] ^ xor;
    }
    return base64DecodedBuffer.toString('utf8');
  }

  // eslint-disable-next-line class-methods-use-this
  sha1Hash(data) {
    return crypto.createHash('sha1').update(data).digest('hex');
  }
}
