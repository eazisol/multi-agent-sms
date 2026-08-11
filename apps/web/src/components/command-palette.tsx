"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { Search } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/field";
import { NAV_SECTIONS } from "@/lib/navigation";

export function CommandPalette({
  open,
  onClose,
}: {
  open: boolean;
  onClose: () => void;
}) {
  const router = useRouter();
  const [q, setQ] = useState("");

  const items = useMemo(() => {
    const flat = NAV_SECTIONS.flatMap((s) =>
      s.items.map((item) => ({ ...item, section: s.label })),
    );
    const query = q.trim().toLowerCase();
    if (!query) return flat.slice(0, 12);
    return flat.filter(
      (item) =>
        item.label.toLowerCase().includes(query) ||
        item.section.toLowerCase().includes(query),
    );
  }, [q]);

  useEffect(() => {
    if (!open) setQ("");
  }, [open]);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        if (open) onClose();
        else document.dispatchEvent(new CustomEvent("masms:open-command"));
      }
      if (e.key === "Escape" && open) onClose();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose, open]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center bg-black/40 p-4 pt-[12vh]"
      role="dialog"
      aria-modal="true"
      aria-label="Command palette"
      onClick={onClose}
    >
      <div
        className="w-full max-w-xl overflow-hidden rounded-[var(--radius-xl)] border border-[var(--line)] bg-[var(--surface)] shadow-float"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center gap-2 border-b border-[var(--line)] px-3">
          <Search className="h-4 w-4 text-[var(--muted)]" aria-hidden />
          <Input
            autoFocus
            className="border-0 shadow-none focus:ring-0"
            placeholder="Search MASMS..."
            value={q}
            onChange={(e) => setQ(e.target.value)}
            aria-label="Search commands"
          />
        </div>
        <ul className="max-h-80 overflow-auto p-2">
          {items.map((item) => (
            <li key={item.href}>
              <button
                type="button"
                className="flex w-full items-center justify-between rounded-[var(--radius-sm)] px-3 py-2 text-left text-sm hover:bg-[var(--surface-muted)]"
                onClick={() => {
                  router.push(item.href);
                  onClose();
                }}
              >
                <span>{item.label}</span>
                <span className="text-xs text-[var(--muted)]">{item.section}</span>
              </button>
            </li>
          ))}
          {items.length === 0 ? (
            <li className="px-3 py-6 text-center text-sm text-[var(--muted)]">
              No matches
            </li>
          ) : null}
        </ul>
        <div className="flex items-center justify-between border-t border-[var(--line)] px-3 py-2 text-xs text-[var(--muted)]">
          <span>Navigate to a module</span>
          <Button variant="ghost" size="sm" onClick={onClose}>
            Esc
          </Button>
        </div>
      </div>
    </div>
  );
}
