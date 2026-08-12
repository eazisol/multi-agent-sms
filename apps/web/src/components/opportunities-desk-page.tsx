"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Plus } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { ListPagination } from "@/components/list-pagination";
import { ScrollRegion } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Select } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  EMPTY_PAGE_META,
  convertQuery,
  formatUtc,
  listOpportunities,
  listQueries,
  type ClientQuery,
  type Opportunity,
  type PageMeta,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";

export function OpportunitiesDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<Opportunity[]>([]);
  const [queries, setQueries] = useState<ClientQuery[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);
  const [status, setStatus] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [queryId, setQueryId] = useState("");
  const [title, setTitle] = useState("");
  const [value, setValue] = useState("");
  const [notes, setNotes] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [opps, queryPage] = await Promise.all([
        listOpportunities(session, { status: status || undefined, limit, offset }),
        listQueries(session, { status: "qualified", limit: 50, offset: 0 }),
      ]);
      setItems(opps.items);
      setPageMeta(opps.page);
      setQueries(queryPage.items);
      setQueryId((prev) => prev || queryPage.items[0]?.id || "");
    } catch (err) {
      notifyApiError("Unable to load opportunities", err);
      setItems([]);
      setPageMeta(EMPTY_PAGE_META);
    } finally {
      setLoading(false);
    }
  }, [session, status, limit, offset]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onConvert(event: FormEvent) {
    event.preventDefault();
    try {
      await convertQuery(session, queryId, {
        title: title.trim(),
        estimated_value: value.trim() || undefined,
        conversion_notes: notes.trim() || undefined,
      });
      notifySuccess("Query converted to opportunity");
      setTitle("");
      setValue("");
      setNotes("");
      setShowCreate(false);
      setOffset(0);
      await load();
    } catch (err) {
      notifyApiError("Could not convert query", err);
    }
  }

  return (
    <AppShell>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Opportunities"
          description="Commercial opportunities converted from qualified queries (MOD-210)."
          actions={
            <Button type="button" onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              Convert query
            </Button>
          }
        />

        <div className="flex shrink-0 gap-2">
          <Select value={status} onChange={(e) => { setStatus(e.target.value); setOffset(0); }}>
            <option value="">All statuses</option>
            <option value="open">open</option>
          </Select>
        </div>

        {showCreate ? (
          <Card className="shrink-0">
            <CardHeader>
              <h2 className="font-display text-lg">Convert qualified query</h2>
            </CardHeader>
            <CardBody>
              <form onSubmit={onConvert} className="grid gap-4 md:grid-cols-2" aria-label="Convert query">
                <Field label="Qualified query">
                  <Select required value={queryId} onChange={(e) => setQueryId(e.target.value)}>
                    {queries.length === 0 ? (
                      <option value="">No qualified queries</option>
                    ) : (
                      queries.map((row) => (
                        <option key={row.id} value={row.id}>
                          {row.subject}
                        </option>
                      ))
                    )}
                  </Select>
                </Field>
                <Field label="Opportunity title">
                  <Input required value={title} onChange={(e) => setTitle(e.target.value)} />
                </Field>
                <Field label="Estimated value">
                  <Input value={value} onChange={(e) => setValue(e.target.value)} placeholder="50000.00" />
                </Field>
                <Field label="Conversion notes">
                  <Input value={notes} onChange={(e) => setNotes(e.target.value)} />
                </Field>
                <Button type="submit" disabled={!queryId}>
                  Convert
                </Button>
              </form>
            </CardBody>
          </Card>
        ) : null}

        <ScrollRegion>
          <Card>
            <CardBody>
              {loading ? (
                <SkeletonRows />
              ) : items.length === 0 ? (
                <EmptyState
                  title="No opportunities"
                  body="Convert a qualified query to create one."
                />
              ) : (
                <ul className="divide-y divide-[var(--line)]">
                  {items.map((row) => (
                    <li key={row.id} className="flex items-center justify-between gap-3 py-3">
                      <div>
                        <p className="font-medium">{row.title}</p>
                        <p className="text-sm text-[var(--muted)]">
                          {row.currency} {row.estimated_value ?? "—"} · {formatUtc(row.created_at)}
                        </p>
                      </div>
                      <StatusBadge status={row.status} />
                    </li>
                  ))}
                </ul>
              )}
              <ListPagination
                page={pageMeta}
                onOffsetChange={setOffset}
                onLimitChange={setLimit}
                label="opportunities"
              />
            </CardBody>
          </Card>
        </ScrollRegion>
      </div>
    </AppShell>
  );
}
