"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Plus, Search, Sparkles } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows, StatusBanner } from "@/components/ui-states";
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
  const [q, setQ] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [legalName, setLegalName] = useState("");
  const [code, setCode] = useState("");
  const [industry, setIndustry] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const page = await listClients(session, {
        q: q.trim() || undefined,
        limit: 50,
        offset: 0,
      });
      setItems(page.items);
      setTotal(page.page.total);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Unable to load clients");
      setItems([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  }, [session, q]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onCreate(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setOk(null);
    try {
      const created = await createClient(session, {
        code: (code || legalName).trim().toLowerCase().replace(/\s+/g, "-"),
        legal_name: legalName.trim(),
        industry: industry.trim() || undefined,
      });
      setOk(`${created.legal_name} added`);
      setLegalName("");
      setCode("");
      setIndustry("");
      setShowCreate(false);
      await load();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not create client");
    }
  }

  return (
    <AppShell title="Clients" breadcrumbs={["Business Development", "Clients"]}>
      <PageHeader
        title="Clients"
        description="Accounts your team delivers for — contacts, projects, and commercial context in one place."
        actions={
          can(session.variant, "create") ? (
            <Button onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              New client
            </Button>
          ) : null
        }
      />

      {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
      {ok ? <StatusBanner kind="success">{ok}</StatusBanner> : null}

      {showCreate ? (
        <Card className="mb-6">
          <CardHeader>
            <h2 className="font-display text-lg">Create client</h2>
            <p className="text-sm text-[var(--muted)]">
              Add the basic business information. More contacts and ownership can be assigned later.
            </p>
          </CardHeader>
          <CardBody>
            <form onSubmit={onCreate} className="grid gap-4 md:grid-cols-2" aria-label="Create client">
              <Field label="Client name" hint="Legal or trading name used with the customer">
                <Input
                  required
                  value={legalName}
                  onChange={(e) => {
                    setLegalName(e.target.value);
                    if (!code) {
                      setCode(
                        e.target.value
                          .toLowerCase()
                          .replace(/[^a-z0-9]+/g, "-")
                          .replace(/^-|-$/g, ""),
                      );
                    }
                  }}
                  placeholder="Acme Corporation"
                />
              </Field>
              <Field label="Industry">
                <Input
                  value={industry}
                  onChange={(e) => setIndustry(e.target.value)}
                  placeholder="Technology"
                />
              </Field>
              <Field label="Short code" hint="Used in reports and references">
                <Input
                  required
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  pattern="[a-z0-9_-]+"
                />
              </Field>
              <div className="flex items-end justify-end gap-2 md:col-span-2">
                <Button type="button" variant="ghost" onClick={() => setShowCreate(false)}>
                  Cancel
                </Button>
                <Button type="submit">Create client</Button>
              </div>
            </form>
          </CardBody>
        </Card>
      ) : null}

      <Card>
        <CardHeader className="flex flex-wrap items-center gap-3">
          <div className="relative min-w-[220px] flex-1">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--muted)]" />
            <Input
              className="pl-9"
              placeholder="Search name, code, or industry…"
              value={q}
              onChange={(e) => setQ(e.target.value)}
              aria-label="Search clients"
            />
          </div>
          <p className="text-sm text-[var(--muted)]">
            {total} match{total === 1 ? "" : "es"}
          </p>
        </CardHeader>
        {loading ? (
          <SkeletonRows />
        ) : items.length === 0 ? (
          <CardBody>
            <EmptyState
              title={q.trim() ? "No matching clients" : "No clients yet"}
              body={
                q.trim()
                  ? "Try a different name, code, or industry."
                  : "Clients anchor every query, project, and delivery conversation. Start by adding your first account."
              }
              action={
                !q.trim() && can(session.variant, "create") ? (
                  <Button onClick={() => setShowCreate(true)}>
                    <Plus className="h-4 w-4" />
                    Add client
                  </Button>
                ) : null
              }
              secondaryAction={
                !q.trim() ? (
                  <Button variant="ai">
                    <Sparkles className="h-4 w-4" />
                    Import with AI
                  </Button>
                ) : null
              }
            />
          </CardBody>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead className="sticky top-0 bg-[var(--surface-muted)] text-xs uppercase tracking-wide text-[var(--muted)]">
                <tr>
                  <th className="px-5 py-3 font-medium">Client</th>
                  <th className="px-5 py-3 font-medium">Industry</th>
                  <th className="px-5 py-3 font-medium">Status</th>
                  <th className="px-5 py-3 font-medium">Created</th>
                </tr>
              </thead>
              <tbody>
                {items.map((client) => (
                  <tr
                    key={client.id}
                    className="border-t border-[var(--line)] hover:bg-[var(--surface-muted)]/70"
                  >
                    <td className="px-5 py-3">
                      <p className="font-medium">{client.legal_name}</p>
                      <p className="text-xs text-[var(--muted)]">{client.code}</p>
                    </td>
                    <td className="px-5 py-3 text-[var(--muted)]">
                      {client.industry || "—"}
                    </td>
                    <td className="px-5 py-3">
                      <StatusBadge status={client.status} />
                    </td>
                    <td className="px-5 py-3 text-[var(--muted)]">
                      {formatUtc(client.created_at)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </AppShell>
  );
}
