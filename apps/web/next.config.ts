import type { NextConfig } from "next";

const apiOrigin =
  process.env.MASMS_API_ORIGIN?.replace(/\/$/, "") ||
  process.env.NEXT_PUBLIC_API_ORIGIN?.replace(/\/$/, "") ||
  "http://127.0.0.1:8000";

const nextConfig: NextConfig = {
  // Keep prod build output (`.next`) separate from `next dev` (`.next-dev`)
  // so `npm run build` cannot invalidate an active local session and cause
  // `/_next/static/...` 404s in the browser.
  distDir: process.env.NODE_ENV === "development" ? ".next-dev" : ".next",
  async rewrites() {
    // Same-origin /api/* → FastAPI. Avoids browser CORS during local/dev UI work.
    return [
      {
        source: "/api/:path*",
        destination: `${apiOrigin}/api/:path*`,
      },
      {
        source: "/health",
        destination: `${apiOrigin}/health`,
      },
      {
        source: "/health/:path*",
        destination: `${apiOrigin}/health/:path*`,
      },
    ];
  },
};

export default nextConfig;
