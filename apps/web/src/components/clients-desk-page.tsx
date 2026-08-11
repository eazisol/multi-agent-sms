"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Plus, Search, Sparkles } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { ListPagination } from "@/components/list-pagination";
import { TableScroll } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Select } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  EMPTY_PAGE_META,
  createClient,
  formatUtc,
  listClients,
  type Client,
  type PageMeta,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";
import { can } from "@/lib/roles";

export function ClientsDeskPage() {
  const { session } = useSession();
  const [items, setItems] = useState<Client[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [loading, setLoading] = useState(true);
  const [q, setQ] = useState("");
  const [status, setStatus] = useState("");
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);
  const [showCreate, setShowCreate] = useState(false);
  const [legalName, setLegalName] = useState("");
  const [code, setCode] = useState("");
  const [industry, setIndustry] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await listClients(session, {
        q: q.trim() || undefined,
        status: status || undefined,
        limit,
        offset,
      });
      setItems(result.items);
      setPageMeta(result.page);
    } catch (err) {
      notifyApiError("Unable to load clients", err);
      setItems([]);
      setPageMeta(EMPTY_PAGE_META);
    } finally {
      setLoading(false);
    }
  }, [session, q, status, limit, offset]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onCreate(event: FormEvent) {
    event.preventDefault();
    try {
      const created = await createClient(session, {
        code: (code || legalName).trim().toLowerCase().replace(/\s+/g, "-"),
        legal_name: legalName.trim(),
        industry: industry.trim() || undefined,
      });
      notifySuccess(`${created.legal_name} added`);
      setLegalName("");
      setCode("");
      setIndustry("");
      setShowCreate(false);
      await load();
    } catch (err) {
      notifyApiError("Could not create client", err);
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
        <CardHeader className="flex flex-wrap items-end gap-3">
          <div className="relative min-w-[220px] flex-1">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--muted)]" />
            <Input
              className="pl-9"
              placeholder="Search name, code, or industry…"
              value={q}
              onChange={(e) => {
                setQ(e.target.value);
                setOffset(0);
              }}
              aria-label="Search clients"
            />
          </div>
          <Field label="Status" className="mb-0 min-w-[10rem]">
            <Select
              value={status}
              onChange={(e) => {
                setStatus(e.target.value);
                setOffset(0);
              }}
              aria-label="Filter by status"
            >
              <option value="">Any status</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
              <option value="prospect">Prospect</option>
              <option value="archived">Archived</option>
            </Select>
          </Field>
          <p className="pb-2 text-sm text-[var(--muted)]">
            {pageMeta.total} match{pageMeta.total === 1 ? "" : "es"}
          </p>
        </CardHeader>
        {loading ? (
          <SkeletonRows />
        ) : items.length === 0 ? (
          <CardBody>
            <EmptyState
              title={q.trim() || status ? "No matching clients" : "No clients yet"}
              body={
                q.trim() || status
                  ? "Try a different name, code, industry, or status."
                  : "Clients anchor every query, project, and delivery conversation. Start by adding your first account."
              }
              action={
                !q.trim() && !status && can(session.variant, "create") ? (
                  <Button onClick={() => setShowCreate(true)}>
                    <Plus className="h-4 w-4" />
                    Add client
                  </Button>
                ) : null
              }
              secondaryAction={
                !q.trim() && !status ? (
                  <Button variant="ai">
                    <Sparkles className="h-4 w-4" />
                    Import with AI
                  </Button>
                ) : null
              }
            />
          </CardBody>
        ) : (
          <>
            <TableScroll className="rounded-none border-0 border-t border-[var(--line)]">
              <table className="w-full min-w-full table-fixed text-left text-sm">
                <thead className="sticky top-0 z-10 bg-[var(--surface-muted)] text-xs uppercase tracking-wide text-[var(--muted)]">
                  <tr>
                    <th className="w-[40%] px-5 py-3 font-medium">Client</th>
                    <th className="w-[25%] px-5 py-3 font-medium">Industry</th>
                    <th className="w-[15%] px-5 py-3 font-medium">Status</th>
                    <th className="w-[20%] px-5 py-3 font-medium">Created</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((client) => (
                    <tr
                      key={client.id}
                      className="border-t border-[var(--line)] hover:bg-[var(--surface-muted)]/70"
                    >
                      <td className="px-5 py-3">
                        <p className="truncate font-medium">{client.legal_name}</p>
                        <p className="truncate text-xs text-[var(--muted)]">{client.code}</p>
                      </td>
                      <td className="px-5 py-3 text-[var(--muted)]">
                        <span className="line-clamp-2">{client.industry || "—"}</span>
                      </td>
                      <td className="px-5 py-3">
                        <StatusBadge status={client.status} />
                      </td>
                      <td className="whitespace-nowrap px-5 py-3 text-[var(--muted)]">
                        {formatUtc(client.created_at)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </TableScroll>
            <ListPagination
              page={pageMeta}
              onOffsetChange={setOffset}
              onLimitChange={setLimit}
              label="clients"
            />
          </>
        )}
        {!loading && items.length === 0 && pageMeta.total > 0 ? (
          <ListPagination
            page={pageMeta}
            onOffsetChange={setOffset}
            onLimitChange={setLimit}
            label="clients"
          />
        ) : null}
      </Card>
    </AppShell>
  );
}
