import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

export async function middleware(request: NextRequest) {
  if (process.env.NEXT_PUBLIC_AUTH_MODE !== "auth0") {
    return NextResponse.next();
  }

  const { getAuth0Client } = await import("@/lib/auth0");
  const auth0 = getAuth0Client();
  const authResponse = await auth0.middleware(request);
  const pathname = request.nextUrl.pathname;
  if (
    pathname.startsWith("/auth") ||
    pathname === "/login" ||
    pathname === "/health" ||
    pathname.startsWith("/health/")
  ) {
    return authResponse;
  }

  const session = await auth0.getSession(request);
  if (!session) {
    const loginUrl = new URL("/login", request.nextUrl.origin);
    loginUrl.searchParams.set("returnTo", pathname + request.nextUrl.search);
    return NextResponse.redirect(loginUrl);
  }
  return authResponse;
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)"],
};
