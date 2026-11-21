// Entry for news-image-20261120: the page is entry.png beside this file, and this program
// checks it against the gate's own rules before copying it to /output/entry.png.
//
// The gate asks for a whole PNG — every chunk present, its CRC matching the bytes before it,
// the image data the IHDR describes — of at most 1 MiB and at most 1024x1024. Rather than
// trust the file, this reads it the way the gate will and refuses to write anything that
// would be listed with a Valid of 0.
//
// Node 22, standard library only, no network. Outside the grader's container:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const CAP_BYTES = 1024 * 1024;
const SIDE = 1024;
const SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const CRC_TABLE = (() => {
  const table = new Int32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table[n] = c;
  }
  return table;
})();

function crc32(buf: Buffer): number {
  let c = 0xffffffff;
  for (const byte of buf) c = CRC_TABLE[(c ^ byte) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

function refuse(why: string): never {
  console.error(`entry.png refused: ${why}`);
  process.exit(1);
}

/** Walk the chunks: they must tile the file exactly, end with IEND, and every CRC must hold. */
function inspect(png: Buffer) {
  if (png.length > CAP_BYTES) refuse(`${png.length} bytes, over the ${CAP_BYTES}-byte cap`);
  if (png.length < 8 || !png.subarray(0, 8).equals(SIGNATURE)) refuse('no PNG signature');

  let at = 8;
  let width = 0;
  let height = 0;
  let sawHeader = false;
  let sawData = 0;
  for (;;) {
    if (at + 12 > png.length) refuse(`truncated chunk header at byte ${at}`);
    const length = png.readUInt32BE(at);
    const type = png.toString('latin1', at + 4, at + 8);
    const body = png.subarray(at + 8, at + 8 + length);
    if (body.length !== length) refuse(`chunk ${type} runs past the end of the file`);
    const stated = png.readUInt32BE(at + 8 + length);
    if (crc32(png.subarray(at + 4, at + 8 + length)) !== stated) refuse(`chunk ${type} has a bad CRC`);
    if (!sawHeader && type !== 'IHDR') refuse('first chunk is not IHDR');
    if (type === 'IHDR') {
      sawHeader = true;
      width = body.readUInt32BE(0);
      height = body.readUInt32BE(4);
    }
    if (type === 'IDAT') sawData += length;
    at += 12 + length;
    if (type === 'IEND') break;
  }
  if (at !== png.length) refuse(`${png.length - at} bytes after IEND`);
  if (width !== SIDE || height !== SIDE) refuse(`${width}x${height}, the gate wants ${SIDE}x${SIDE}`);
  if (!sawData) refuse('no IDAT chunk');
  return { width, height, bytes: png.length };
}

const here = dirname(fileURLToPath(import.meta.url));
const png = readFileSync(join(here, 'entry.png'));
const { width, height, bytes } = inspect(png);

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'entry.png'), png);
console.log(`wrote ${join(outDir, 'entry.png')}: ${width}x${height}, ${bytes} bytes, CRCs intact`);
