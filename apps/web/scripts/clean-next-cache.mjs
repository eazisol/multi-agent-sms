/**
 * Clears Next.js local caches used by this app.
 * Safe to run before `npm run dev:clean`.
 */
import { rmSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const webRoot = join(root, "..");

for (const dir of [".next-dev", ".next"]) {
  const target = join(webRoot, dir);
  rmSync(target, { recursive: true, force: true });
  console.log(`removed ${dir}`);
}
