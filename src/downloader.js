/* eslint-disable class-methods-use-this */
/* eslint-disable no-restricted-syntax */
/* eslint-disable no-plusplus */
/* eslint-disable no-unused-vars */
/* eslint-disable prefer-destructuring */
/* eslint-disable consistent-return */
/* eslint-disable no-promise-executor-return */
/* eslint-disable no-async-promise-executor */
/* eslint-disable no-mixed-operators */
/* eslint-disable no-await-in-loop */
import { BrowserWindow, ipcMain } from 'electron';
import { XMLParser } from 'fast-xml-parser';
import axios from 'axios';
import fs from 'fs';
import path from 'path';
import { exec, spawn } from 'child_process';
import unzipper from 'unzipper';
import utility from './utility';

export default class {
  constructor(options = {}) {
    this.path = options.path || null;
    this.clientURL = options.clientURL || null;
    this.totalFiles = 0;
    this.$http = axios.create({
      baseURL: 'https://user81700.clients-cdnnow.ru/r2club',
    });
    this.saveData = {
      files: [],
      lastSize: 0,
      lastSizeChunk: 0,
      total: 0,
      fullSize: 0,
      partSize: 0,
    };
    this.state = 'default';
  }

  get dirSaveClient() {
    return this.path;
  }

  get urlClient() {
    return this.clientURL;
  }

  setSavePath(pathUser) {
    this.path = pathUser;
  }

  async pauseDownload() {
    console.log('SET PAuSE');
    if (this.state === 'pause') {
      this.state = 'default';
      await this.downloadFiles({
        total: this.saveData.total,
        fullSize: this.saveData.fullSize,
        files: this.saveData.files,
        partSize: this.saveData.partSize,
        nextStartDownload: this.saveData.lastSize,
        nextChunkDownload: this.saveData.lastSizeChunk,
      });
    } else {
      this.state = 'pause';
      console.log('pause setted');
    }
  }

  sendEvent(type, data) {
    if (BrowserWindow.getAllWindows().length > 0) {
      BrowserWindow.getAllWindows()[0].webContents.send('download-progress', {
        type,
        data,
      });
    }
  }

  // async startGaming(param1, param2) {
  //   const gamePath = this.dirSaveClient;

  //   const args = [
  //     'tn5ZR50|0012396171|7c4a8d09ca3762af61e59520943dc26494f8941b_7f3c3d9073510602a05e79bbb97143303d6eb44f',
  //     '1063763511',
  //     '1063759441',
  //     '1063763736',
  //     '1063763511',
  //     '1063763782',
  //     '1063758637',
  //   ];
  //   const child = spawn('R2Client.exe', args, {
  //     cwd: gamePath,
  //   });

  //   child.stdout.on('data', (data) => {
  //     console.log(`stdout: ${data}`);
  //   });

  //   child.stderr.on('data', (data) => {
  //     console.log(`stderr: ${data}`);
  //   });

  //   child.on('error', (error) => {
  //     console.log(`error: ${error.message}`);
  //   });

  //   child.on('close', (code) => {
  //     console.log(`child process exited with code ${code}`);
  //     BrowserWindow.getAllWindows()[0].webContents.send('start-gaming', {
  //       err: code !== 0 ? new Error(`Exit with code ${code}`) : null,
  //       data: null,
  //     });
  //   });
  // }

  async startGaming(param1, param2) {
    const gamePath = this.dirSaveClient;
    const execPath = `start "" R2Client "${param1}" ${param2}`;
    console.log('EXEC PATH!', execPath);
    exec(
      execPath,
      {
        cwd: gamePath,
      },
      (err, data) => {
        console.log(err, data);
        BrowserWindow.getAllWindows()[0].webContents.send('start-gaming', {
          err,
          data,
        });
      }
    );
  }

  // async startGaming(userId, superPassWd, pathItem) {
  //   const gamePath = this.dirSaveClient;
  //   exec(
  //     `start "" R2Client "P=&H1=OTkuMDUuMDMuMDQ=&P0=${Buffer.from(userId.trim()).toString(
  //       'base64'
  //     )}&P1=Q19SMg==&P2=NDYxMg==&P3=&P4=${Buffer.from(superPassWd.trim()).toString(
  //       'base64'
  //     )}&P5=&PC1=Tg==&PC2=Tg==\\" 46773916 46772778 46772834 46773916 46772794 46773044\\""`,
  //     {
  //       cwd: gamePath,
  //     },
  //     (err, data) => {
  //       console.log(err, data);
  //       BrowserWindow.getAllWindows()[0].webContents.send('start-gaming', {
  //         err,
  //         data,
  //       });
  //     }
  //   );
  // }

  async delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  async checkFilesHash() {
    if (!this.dirSaveClient) return false;

    // Проверить, пуста ли папка
    const isFolderEmpty = fs.readdirSync(this.dirSaveClient).length === 0;

    // Если папка пуста, скачать и распаковать архив с клиентом
    if (isFolderEmpty) {
      const clientArchiveURL = 'https://user81700.clients-cdnnow.ru/r2club/client5.zip';
      const archivePath = path.join(this.dirSaveClient, 'clientArchive.zip');
      await this.downloadClientArchive(clientArchiveURL, archivePath);
      await this.extractArchive(archivePath, this.dirSaveClient);
      fs.unlinkSync(archivePath);
    }

    try {
      const { data } = await this.$http.get('UpdateInfo.xml');

      const parser = new XMLParser();
      const xml = parser.parse(data);
      const { Folder } = xml.UpdateInfo;

      const filesCount = await this.getTotalFiles(Folder);
      this.totalFiles = filesCount;
      this.sendEvent('verify', {
        total: this.totalFiles,
        current: 0,
        fileName: '',
        isEnd: false,
      });

      const files = await this.recoursiveParsingExistFolderAndFiles(Folder);
      this.sendEvent('verify', {
        total: this.totalFiles,
        current: files.total,
        fileName: '',
        isEnd: true,
      });
      await this.delay(2000);

      if (files.total) {
        this.sendEvent('download', {
          total: files.total,
          current: 0,
          totalSize: files.partSize,
          fileName: '',
          isEnd: false,
        });
        await this.downloadFiles(files);
        if (this.state === 'pause') return;
        this.sendEvent('download', {
          total: files.total,
          current: 0,
          totalSize: files.partSize,
          fileName: '',
          isEnd: true,
        });
      }
      utility.showNotify({
        message: 'Игрвой клиент готов к запуску',
        pushOnFocus: false,
      });
      await this.delay(1000);
      this.sendEvent('play', {});
    } catch (e) {
      console.log('GET OF ERROR!', e);
      this.sendEvent('error', {
        code: e.response.status,
        message: e.response.statusText,
      });

      await this.delay(5000);
      utility.showNotify({
        message: `Ошибка загрузки клиента: ${e.response.status} ${e.response.statusText}`,
        pushOnFocus: false,
      });
    }
  }

  async downloadClientArchive(url, archivePath) {
    const writer = fs.createWriteStream(archivePath);
    const response = await axios({
      url,
      method: 'GET',
      responseType: 'stream',
    });

    const totalLength = parseInt(response.headers['content-length'], 10);
    let downloadedLength = 0;

    response.data.on('data', (chunk) => {
      downloadedLength += chunk.length;
      const percentage = (downloadedLength / totalLength) * 100;

      this.sendEvent('download', {
        total: totalLength,
        current: downloadedLength,
        totalSize: totalLength,
        fileName: 'clientArchive.zip',
        isEnd: false,
      });
    });

    response.data.pipe(writer);

    return new Promise((resolve, reject) => {
      writer.on('finish', () => {
        this.sendEvent('download', {
          total: totalLength,
          current: downloadedLength,
          totalSize: totalLength,
          fileName: 'clientArchive.zip',
          isEnd: true,
        });
        resolve();
      });
      writer.on('error', reject);
    });
  }

  async extractArchive(archivePath, destinationFolderPath) {
    return new Promise((resolve, reject) => {
      fs.createReadStream(archivePath)
        .pipe(unzipper.Extract({ path: destinationFolderPath }))
        .on('finish', resolve)
        .on('error', reject);
    });
  }

  async getTotalFiles(Folder) {
    let filesCount = 0;
    const parsingStart = async (folder, folderNextPath = '/') => {
      const { Folders, Files } = folder;

      const fileModel = Array.isArray(Files.FileModel) ? Files.FileModel : [Files.FileModel];
      for (const _ of fileModel) {
        filesCount++;
      }

      if (Folders) {
        const folderModel = Array.isArray(Folders.FolderModel)
          ? Folders.FolderModel
          : [Folders.FolderModel];
        for (const folderNext of folderModel) {
          await parsingStart(folderNext, `${folderNextPath + folderNext.Name}/`);
        }
      }
    };

    await parsingStart(Folder);

    return filesCount;
  }

  async recoursiveParsingExistFolderAndFiles(folderInit) {
    let counterItem = 0;
    const toDownloadResult = {
      total: 0,
      fullSize: 0,
      partSize: 0,
      files: [],
    };

    const parsingStart = async (folder, folderNextPath = '/') => {
      const { Folders, Files } = folder;

      if (Files) {
        const fileModel = Array.isArray(Files.FileModel) ? Files.FileModel : [Files.FileModel];
        for (const file of fileModel) {
          const { Name, Size, Path } = file;
          const filePath = path.join(this.dirSaveClient, folderNextPath, Name);
          // check folder exist and create
          const folderPath = path.dirname(filePath);
          if (!fs.existsSync(folderPath)) {
            fs.mkdirSync(folderPath, {
              recursive: true,
            });
          }

          const formatDownload = () =>
            `${Path.replace('r2club', 'https://user81700.clients-cdnnow.ru/r2club').replaceAll(
              '\\',
              '/'
            )}/${Name}`;

          // check path exist
          if (!fs.existsSync(filePath)) {
            toDownloadResult.total++;
            toDownloadResult.fullSize += Size;
            toDownloadResult.partSize += Size;
            toDownloadResult.files.push({
              Folder: folderPath,
              Download: formatDownload(),
              Name,
              Size,
            });
          } else {
            let modHash = null;
            const fileHash = await utility.fileStream(filePath);
            const fileHashRemote = file.Hash;

            if (fileHashRemote[0] === '0') {
              for (let i = 0; i < fileHashRemote.length; i++) {
                if (fileHashRemote[i].toString() === '0') {
                  modHash = fileHashRemote.slice(i + 1);
                } else {
                  break;
                }
              }
            } else {
              modHash = fileHashRemote;
            }

            if (modHash.toString() !== fileHash) {
              toDownloadResult.total++;
              toDownloadResult.fullSize += Size;
              toDownloadResult.partSize += Size;
              toDownloadResult.files.push({
                Folder: folderPath,
                Name,
                Download: formatDownload(),
                Size,
                Hash: fileHashRemote,
              });
            }
          }

          counterItem += 1;
          this.sendEvent('verify', {
            total: this.totalFiles,
            current: counterItem,
            fileName: Name,
            isEnd: false,
          });
        }
      }

      if (Folders) {
        const folderModel = Array.isArray(Folders.FolderModel)
          ? Folders.FolderModel
          : [Folders.FolderModel];
        for (const folderNext of folderModel) {
          await parsingStart(folderNext, `${folderNextPath + folderNext.Name}/`);
        }
      }
    };

    await parsingStart(folderInit);
    return toDownloadResult;
  }

  async downloadFiles({
    total,
    fullSize,
    files,
    partSize,
    nextStartDownload = 0,
    nextChunkDownload = 0,
  }) {
    let startDownload = nextStartDownload;
    let currentTotalChunk = nextChunkDownload;
    this.saveData.total = total;
    this.saveData.fullSize = fullSize;
    this.saveData.partSize = partSize;
    const downloadStart = async (file) => {
      const { Folder, Download, Name, Size } = file;

      const filePath = path.join(Folder, Name);
      const writer = fs.createWriteStream(filePath);

      this.sendEvent('download', {
        total,
        current: startDownload,
        fileName: Name,
        isEnd: false,
        totalSize: partSize,
      });

      const currentStateChunk = {
        len: 0,
        total: 0,
        current: 0,
      };

      const cancelToken = axios.CancelToken;
      const source = cancelToken.source();
      const response = await axios(Download, {
        method: 'GET',
        responseType: 'stream',
        cancelToken: source.token,
      });

      currentStateChunk.len = Math.floor(response.headers['content-length'], 10);
      currentStateChunk.total = currentStateChunk.len;

      response.data.pipe(writer);
      response.data.on('data', (chunk) => {
        if (this.state !== 'pause') {
          currentStateChunk.current += chunk.length;
          currentTotalChunk += chunk.length;
          this.sendEvent('chunk', {
            fileName: Name,
            fullSize: currentStateChunk.total.toFixed(2),
            currentSize: currentStateChunk.current.toFixed(2),
            totalSize: currentTotalChunk,
          });
        } else {
          source.cancel();
        }
      });

      return new Promise((resolve, reject) => {
        if (this.state === 'pause') {
          this.sendEvent('download', {
            total,
            current: startDownload,
            fileName: Name,
            isEnd: false,
            totalSize: partSize,
          });
          console.log('resolver!!');

          this.saveData.lastSizeChunk = currentTotalChunk - currentStateChunk.current;
          this.saveData.lastSize = startDownload;
          console.log(this.saveData.lastSizeChunk, this.saveData.lastSize);

          resolve();
        }
        writer.on('finish', () => {
          if (this.state !== 'pause') {
            startDownload += currentStateChunk.current;
          }
          resolve();
        });
        writer.on('error', reject);
      });
    };

    let index = 0;
    for (const file of files) {
      if (this.state === 'pause') {
        this.saveData.lastIndex = index;
        this.saveData.files = files.slice(index, files.length);
        break;
      }
      await downloadStart(file);
      index++;
    }

    if (this.state === 'pause') {
      return 'pause';
    }

    return 'success';
  }
}
