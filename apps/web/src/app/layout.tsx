import type { Metadata } from "next";

import { SessionProvider } from "@/components/session-provider";
import "./globals.css";

export const metadata: Metadata = {
  title: "MASMS",
  description: "Multi-Agent Software House Management System",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        <SessionProvider>{children}</SessionProvider>
      </body>
    </html>
  );
}
