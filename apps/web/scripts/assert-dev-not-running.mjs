/**
 * Fail production builds if port 3000 is already in use (usually `next dev` / `next start`).
 * Prevents racing an active local web session.
 */
import { execSync } from "node:child_process";

function port3000InUse() {
  try {
    if (process.platform === "win32") {
      const out = execSync("netstat -ano", { encoding: "utf8" });
      return /^[ \t]*TCP\s+\S+:3000\s+\S+\s+LISTENING/im.test(out);
    }
    const out = execSync("lsof -iTCP:3000 -sTCP:LISTEN -n -P || true", {
      encoding: "utf8",
      shell: "/bin/bash",
    });
    return /:3000/.test(out);
  } catch {
    return false;
  }
}

if (port3000InUse()) {
  console.error(
    [
      "Refusing to run `next build` while something is listening on port 3000.",
      "Stop `npm run dev` / `npm start` first, then build.",
      "Dev cache is `.next-dev`; prod cache is `.next` — but an open browser tab can still 404 if you rebuild mid-session.",
    ].join("\n"),
  );
  process.exit(1);
}
