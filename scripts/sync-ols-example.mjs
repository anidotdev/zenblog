import { copyFile, mkdir } from 'node:fs/promises';

const source = new URL('../examples/ols/ols.py', import.meta.url);
const destination = new URL('../public/code/ols.py', import.meta.url);
await mkdir(new URL('../public/code/', import.meta.url), { recursive: true });
await copyFile(source, destination);
console.log('Synced the tested OLS implementation to public/code/ols.py');
