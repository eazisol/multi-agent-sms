"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { useSession } from "@/components/session-provider";
import { VARIANT_OPTIONS } from "@/lib/roles";

const NAV = [
  { href: "/clients", label: "Clients" },
  { href: "/queries", label: "Queries" },
  { href: "/comms", label: "Comms" },
  { href: "/requirements", label: "Requirements" },
  { href: "/projects", label: "Projects" },
  { href: "/documents", label: "Documents" },
  { href: "/roadmap", label: "Roadmap" },
  { href: "/tickets", label: "Tickets" },
  { href: "/governance/baselines", label: "Governance" },
] as const;

export function AppShell({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  const { session, setVariant } = useSession();
  const pathname = usePathname();

  return (
    <div className="min-h-screen bg-[var(--surface)] text-[var(--ink)]">
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded focus:bg-white focus:px-3 focus:py-2"
      >
        Skip to content
      </a>
      <header className="border-b border-[var(--line)] bg-[var(--panel)]">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-4 py-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">
              MASMS
            </p>
            <h1 className="font-display text-2xl tracking-tight">{title}</h1>
          </div>
          <nav aria-label="Primary" className="flex flex-wrap items-center gap-3 text-sm">
            {NAV.map((item) => {
              const active =
                pathname === item.href || pathname.startsWith(`${item.href}/`);
              return (
                <Link
                  key={item.href}
                  className={
                    active
                      ? "font-semibold text-[var(--accent)] underline-offset-4 underline"
                      : "underline-offset-4 hover:underline"
                  }
                  href={item.href}
                  aria-current={active ? "page" : undefined}
                >
                  {item.label}
                </Link>
              );
            })}
            <label className="flex items-center gap-2">
              <span className="text-[var(--muted)]">UI role</span>
              <select
                className="rounded border border-[var(--line)] bg-white px-2 py-1"
                value={session.variant}
                onChange={(event) =>
                  setVariant(event.target.value as typeof session.variant)
                }
                aria-label="UI role variant"
              >
                {VARIANT_OPTIONS.map((option) => (
                  <option key={option.id} value={option.id}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>
            {session.actorKind === "agent" ? (
              <span className="rounded bg-[var(--accent-soft)] px-2 py-1 text-xs font-medium text-[var(--accent)]">
                Agent — draft only
              </span>
            ) : null}
          </nav>
        </div>
      </header>
      <main id="main" className="mx-auto max-w-6xl px-4 py-8">
        {children}
      </main>
    </div>
  );
}
