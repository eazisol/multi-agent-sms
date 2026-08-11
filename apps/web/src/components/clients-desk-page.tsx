"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { EmptyState, LoadingBlock, StatusBanner } from "@/components/ui-states";
import {
  ApiError,
  createClient,
  formatUtc,
  listClients,
  type Client,
} from "@/lib/api";
import { can } from "@/lib/roles";

export function ClientsDeskPage() {
  const { session } = useSession();
  const [items, setItems] = useState<Client[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const [code, setCode] = useState("");
  const [legalName, setLegalName] = useState("");
  const [industry, setIndustry] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const page = await listClients(session, { limit: 50, offset: 0 });
      setItems(page.items);
      setTotal(page.page.total);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "API unreachable");
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onCreate(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setOk(null);
    try {
      const created = await createClient(session, {
        code: code.trim().toLowerCase(),
        legal_name: legalName.trim(),
        industry: industry.trim() || undefined,
      });
      setOk(`Created client ${created.code}`);
      setCode("");
      setLegalName("");
      setIndustry("");
      await load();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Create failed");
    }
  }

  return (
    <AppShell title="Clients">
      <div className="space-y-6">
        <div>
          <h2 className="font-display text-3xl tracking-tight">Client desk</h2>
          <p className="mt-1 text-sm text-[var(--muted)]">
            MOD-200 clients. Server authorization remains authoritative.
          </p>
        </div>

        {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
        {ok ? <StatusBanner kind="success">{ok}</StatusBanner> : null}

        {can(session.variant, "create") ? (
          <form
            onSubmit={onCreate}
            className="grid gap-3 rounded border border-[var(--line)] bg-white p-4 md:grid-cols-4"
            aria-label="Create client"
          >
            <label className="flex flex-col gap-1 text-sm">
              <span>Code</span>
              <input
                required
                className="rounded border border-[var(--line)] px-3 py-2"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="acme"
                pattern="[a-z0-9_-]+"
              />
            </label>
            <label className="flex flex-col gap-1 text-sm md:col-span-2">
              <span>Legal name</span>
              <input
                required
                className="rounded border border-[var(--line)] px-3 py-2"
                value={legalName}
                onChange={(e) => setLegalName(e.target.value)}
              />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span>Industry</span>
              <input
                className="rounded border border-[var(--line)] px-3 py-2"
                value={industry}
                onChange={(e) => setIndustry(e.target.value)}
              />
            </label>
            <button
              type="submit"
              className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white md:col-span-4 md:w-fit"
            >
              Create client
            </button>
          </form>
        ) : (
          <StatusBanner kind="error">This UI role cannot create clients.</StatusBanner>
        )}

        {loading ? <LoadingBlock label="Loading clients" /> : null}
        {!loading && items.length === 0 ? (
          <EmptyState title="No clients yet" body="Create a client to start Phase 2 work." />
        ) : null}
        {!loading && items.length > 0 ? (
          <div className="overflow-x-auto rounded border border-[var(--line)] bg-white">
            <table className="min-w-full text-left text-sm">
              <caption className="sr-only">Clients ({total})</caption>
              <thead className="border-b border-[var(--line)] bg-[var(--panel)]">
                <tr>
                  <th className="px-3 py-2 font-medium">Code</th>
                  <th className="px-3 py-2 font-medium">Legal name</th>
                  <th className="px-3 py-2 font-medium">Status</th>
                  <th className="px-3 py-2 font-medium">Created</th>
                </tr>
              </thead>
              <tbody>
                {items.map((client) => (
                  <tr key={client.id} className="border-b border-[var(--line)]">
                    <td className="px-3 py-2 font-medium">{client.code}</td>
                    <td className="px-3 py-2">{client.legal_name}</td>
                    <td className="px-3 py-2">{client.status}</td>
                    <td className="px-3 py-2 text-[var(--muted)]">
                      {formatUtc(client.created_at)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null}
      </div>
    </AppShell>
  );
}
