#!/usr/bin/env node

const recommendedMajor = 16;
const current = process.versions.node;
const major = Number(current.split('.')[0]);

if (Number.isNaN(major) || major < recommendedMajor) {
  console.warn(
    `\n[check-node] Detected Node ${current}. Recommended version is ${recommendedMajor}.x for dependency compatibility.\n`
  );
}
