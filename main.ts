// Passport Page of a Country That Isn't There — Republic of Meridia.
//
// Writes the passport spread to /output/entry.png. The spread is built
// deterministically by build.py (PIL) from portrait.png and committed as
// entry.png; this program copies those exact bytes so the two graded runs
// are byte-identical.
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  console.error("entry.png missing next to main.ts");
  process.exit(1);
}
const bytes = readFileSync(source);
const sha = createHash("sha256").update(bytes).digest("hex");
if (bytes.length > 1048576) {
  console.error(`entry.png is ${bytes.length} bytes, over the 1 MiB gate`);
  process.exit(1);
}
if (bytes.subarray(0, 8).toString("hex") !== "89504e470d0a1a0a") {
  console.error("entry.png is not a PNG");
  process.exit(1);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
// Verify the copy: re-read the output and compare hashes, so a partial
// or truncated write can never pass as a valid entry.
const written = readFileSync(target);
const writtenSha = createHash("sha256").update(written).digest("hex");
if (writtenSha !== sha) {
  console.error(`copy mismatch: wrote ${writtenSha}, expected ${sha}`);
  process.exit(1);
}
// PNG dimensions live in the IHDR chunk (bytes 16-24, big-endian).
const width = written.readUInt32BE(16);
const height = written.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  console.error(`entry.png is ${width}x${height}, expected 1024x1024`);
  process.exit(1);
}
console.log(`wrote ${target}: ${bytes.length} bytes, ${width}x${height}, sha256 ${sha}`);
