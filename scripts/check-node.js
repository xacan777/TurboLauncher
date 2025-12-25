#!/usr/bin/env node

const requiredMajor = 16;
const current = process.versions.node;
const major = Number(current.split('.')[0]);

if (Number.isNaN(major) || major !== requiredMajor) {
  console.error(
    `\n[check-node] Detected Node ${current}. This project requires Node ${requiredMajor}.x for dependency compatibility (see @achrinza/node-ipc engine constraint).\n` +
      `Please switch Node versions before running install/build. Examples:\n` +
      `  nvm use ${requiredMajor}\n` +
      `  nvm install ${requiredMajor} && nvm use ${requiredMajor}\n`
  );
  process.exit(1);
}
