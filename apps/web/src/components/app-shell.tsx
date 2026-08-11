"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import {
  Bell,
  Menu,
  Moon,
  PanelLeftClose,
  PanelLeftOpen,
  Plus,
  Search,
  Sparkles,
  Sun,
  X,
} from "lucide-react";

import { CommandPalette } from "@/components/command-palette";
import { PageShell } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { useTheme } from "@/components/theme-provider";
import { Button } from "@/components/ui/button";
import { Select } from "@/components/ui/field";
import { cn } from "@/lib/cn";
import { findNavLabel, NAV_SECTIONS } from "@/lib/navigation";
import { VARIANT_OPTIONS } from "@/lib/roles";

export function AppShell({
  title,
  breadcrumbs,
  children,
  fill = false,
}: {
  title?: string;
  breadcrumbs?: string[];
  children: React.ReactNode;
  /** Page fills the main pane and manages its own nested scrolling (split desks). */
  fill?: boolean;
}) {
  const { session, setVariant } = useSession();
  const { theme, toggle } = useTheme();
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [commandOpen, setCommandOpen] = useState(false);
  const mainRef = useRef<HTMLElement>(null);

  useEffect(() => {
    function onOpen() {
      setCommandOpen(true);
    }
    document.addEventListener("masms:open-command", onOpen);
    return () => document.removeEventListener("masms:open-command", onOpen);
  }, []);

  useEffect(() => {
    setMobileOpen(false);
    mainRef.current?.scrollTo({ top: 0 });
  }, [pathname]);

  const pageTitle = title ?? findNavLabel(pathname);
  const crumbs = breadcrumbs ?? [pageTitle];

  const sidebar = (
    <aside
      className={cn(
        "flex h-full min-h-0 flex-col bg-[var(--sidebar)] text-[var(--sidebar-ink)] transition-[width]",
        collapsed ? "w-[72px]" : "w-[260px]",
      )}
    >
      <div className="flex h-14 shrink-0 items-center justify-between border-b border-white/10 px-4">
        {!collapsed ? (
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[var(--sidebar-muted)]">
              MASMS
            </p>
            <p className="text-sm font-semibold">Command Center</p>
          </div>
        ) : (
          <span className="mx-auto text-xs font-bold">M</span>
        )}
        <button
          type="button"
          className="hidden rounded-md p-1.5 text-[var(--sidebar-muted)] hover:bg-white/5 hover:text-white lg:inline-flex"
          onClick={() => setCollapsed((v) => !v)}
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <PanelLeftOpen className="h-4 w-4" /> : <PanelLeftClose className="h-4 w-4" />}
        </button>
      </div>
      <nav className="min-h-0 flex-1 overflow-y-auto px-2 py-3" aria-label="Primary">
        {NAV_SECTIONS.map((section) => (
          <div key={section.id} className="mb-4">
            {!collapsed ? (
              <p className="mb-1 px-2 text-[10px] font-semibold uppercase tracking-[0.14em] text-[var(--sidebar-muted)]">
                {section.label}
              </p>
            ) : null}
            <ul className="space-y-0.5">
              {section.items.map((item) => {
                const active =
                  item.href === "/"
                    ? pathname === "/"
                    : pathname === item.href || pathname.startsWith(`${item.href}/`);
                return (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      title={item.label}
                      aria-current={active ? "page" : undefined}
                      className={cn(
                        "flex items-center gap-2 rounded-md px-2.5 py-2 text-sm transition",
                        active
                          ? "bg-[var(--sidebar-active)] text-white"
                          : "text-[var(--sidebar-muted)] hover:bg-white/5 hover:text-white",
                        collapsed && "justify-center px-0",
                      )}
                    >
                      {!collapsed ? (
                        <>
                          <span className="flex-1 truncate">{item.label}</span>
                          {!item.ready ? (
                            <span className="rounded bg-white/10 px-1.5 text-[10px]">Soon</span>
                          ) : null}
                        </>
                      ) : (
                        <span className="text-[11px] font-semibold">
                          {item.label.slice(0, 1)}
                        </span>
                      )}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </nav>
    </aside>
  );

  return (
    <div className="flex h-dvh overflow-hidden bg-[var(--background)] text-[var(--ink)]">
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded focus:bg-white focus:px-3 focus:py-2"
      >
        Skip to content
      </a>

      <div className="hidden h-full min-h-0 shrink-0 lg:block">{sidebar}</div>

      {mobileOpen ? (
        <div className="fixed inset-0 z-40 flex lg:hidden">
          <button
            type="button"
            className="absolute inset-0 bg-black/50"
            aria-label="Close menu"
            onClick={() => setMobileOpen(false)}
          />
          <div className="relative z-10 h-full">{sidebar}</div>
        </div>
      ) : null}

      <div className="flex min-h-0 min-w-0 flex-1 flex-col overflow-hidden">
        <header className="z-30 shrink-0 border-b border-[var(--line)] bg-[var(--surface)]/95 backdrop-blur">
          <div className="flex h-14 items-center gap-3 px-4">
            <button
              type="button"
              className="rounded-md p-2 text-[var(--muted)] hover:bg-[var(--surface-muted)] lg:hidden"
              onClick={() => setMobileOpen(true)}
              aria-label="Open navigation"
            >
              <Menu className="h-5 w-5" />
            </button>
            <div className="min-w-0 flex-1">
              <p className="truncate text-xs text-[var(--muted)]">
                {crumbs.join(" / ")}
              </p>
              <p className="truncate text-sm font-semibold">{pageTitle}</p>
            </div>
            <button
              type="button"
              onClick={() => setCommandOpen(true)}
              className="hidden h-9 min-w-[220px] items-center gap-2 rounded-[var(--radius-sm)] border border-[var(--line)] bg-[var(--surface-muted)] px-3 text-left text-sm text-[var(--muted)] hover:border-[var(--line-strong)] md:inline-flex"
            >
              <Search className="h-4 w-4" />
              <span className="flex-1">Search anything...</span>
              <kbd className="rounded border border-[var(--line)] bg-[var(--surface)] px-1.5 text-[10px]">
                ⌘K
              </kbd>
            </button>
            <Button variant="primary" size="sm" className="hidden sm:inline-flex">
              <Plus className="h-4 w-4" />
              Create
            </Button>
            <Button variant="ghost" size="sm" aria-label="Notifications">
              <Bell className="h-4 w-4" />
            </Button>
            <Button variant="ai" size="sm" className="hidden md:inline-flex">
              <Sparkles className="h-4 w-4" />
              AI
            </Button>
            <Button variant="ghost" size="sm" onClick={toggle} aria-label="Toggle theme">
              {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </Button>
            <label className="hidden items-center gap-2 text-xs text-[var(--muted)] xl:flex">
              Role
              <Select
                className="h-8 w-[140px]"
                value={session.variant}
                onChange={(e) => setVariant(e.target.value as typeof session.variant)}
                aria-label="UI role variant"
              >
                {VARIANT_OPTIONS.map((option) => (
                  <option key={option.id} value={option.id}>
                    {option.label}
                  </option>
                ))}
              </Select>
            </label>
            <div
              className="flex h-8 w-8 items-center justify-center rounded-full bg-[var(--accent-soft)] text-xs font-semibold text-[var(--accent)]"
              title="Signed-in user"
            >
              {session.actorKind === "agent" ? "AI" : "You"}
            </div>
            {mobileOpen ? (
              <button type="button" className="lg:hidden" onClick={() => setMobileOpen(false)}>
                <X className="h-5 w-5" />
              </button>
            ) : null}
          </div>
        </header>
        <main
          id="main"
          ref={mainRef}
          className={cn(
            "min-h-0 flex-1",
            fill ? "overflow-hidden" : "overflow-y-auto",
          )}
        >
          <PageShell fill={fill}>{children}</PageShell>
        </main>
      </div>

      <CommandPalette open={commandOpen} onClose={() => setCommandOpen(false)} />
    </div>
  );
}
