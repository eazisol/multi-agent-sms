"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Download, Plus, RefreshCw, Search } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { ScrollRegion } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  createInsightsExport,
  createSavedFilter,
  formatUtc,
  globalSearch,
  listInsightsActivity,
  listInsightsExports,
  listSavedFilters,
  refreshInsightsDashboard,
  type InsightsActivityEvent,
  type InsightsDashboardSnapshot,
  type InsightsExport,
  type InsightsSavedFilter,
  type InsightsSearchDocument,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";

export function InsightsDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [snapshot, setSnapshot] = useState<InsightsDashboardSnapshot | null>(null);
  const [query, setQuery] = useState("");
  const [searchHits, setSearchHits] = useState<InsightsSearchDocument[]>([]);
  const [activity, setActivity] = useState<InsightsActivityEvent[]>([]);
  const [filters, setFilters] = useState<InsightsSavedFilter[]>([]);
  const [exports, setExports] = useState<InsightsExport[]>([]);
  const [filterName, setFilterName] = useState("");
  const [filterJson, setFilterJson] = useState('{"status":"open"}');

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [snap, act, filt, exp] = await Promise.allSettled([
        refreshInsightsDashboard(session),
        listInsightsActivity(session, { limit: 20 }),
        listSavedFilters(session, { limit: 20 }),
        listInsightsExports(session, { limit: 20 }),
      ]);
      if (snap.status === "fulfilled") {
        setSnapshot(snap.value);
      } else {
        setSnapshot(null);
        notifyApiError("Unable to refresh insights dashboard", snap.reason);
      }
      setActivity(act.status === "fulfilled" ? act.value.items : []);
      setFilters(filt.status === "fulfilled" ? filt.value.items : []);
      setExports(exp.status === "fulfilled" ? exp.value.items : []);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onSearch(event: FormEvent) {
    event.preventDefault();
    const q = query.trim();
    if (!q) return;
    try {
      const result = await globalSearch(session, { q, limit: 20 });
      setSearchHits(result.items);
      notifySuccess(`${result.page.total} search hit(s)`);
    } catch (err) {
      notifyApiError("Search failed", err);
      setSearchHits([]);
    }
  }

  async function onCreateFilter(event: FormEvent) {
    event.preventDefault();
    try {
      await createSavedFilter(session, {
        name: filterName.trim(),
        module_key: "insights",
        filter_json: filterJson.trim() || "{}",
      });
      notifySuccess("Saved filter created");
      setFilterName("");
      await load();
    } catch (err) {
      notifyApiError("Could not save filter", err);
    }
  }

  async function onCreateExport() {
    try {
      await createInsightsExport(session, {
        export_format: "json",
        include_dashboard_metrics: true,
      });
      notifySuccess("Export ready (in-DB preview)");
      await load();
    } catch (err) {
      notifyApiError("Could not create export", err);
    }
  }

  const metrics = snapshot?.metrics ?? {};

  return (
    <AppShell title="Insights" breadcrumbs={["Workspace", "Insights"]}>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Insights"
          description="Org-scoped dashboard snapshot, search index, activity, saved filters, and export previews (MOD-450)."
          actions={
            <div className="flex flex-wrap gap-2">
              <Button type="button" variant="outline" onClick={() => void load()}>
                <RefreshCw className="h-4 w-4" />
                Refresh snapshot
              </Button>
              <Button type="button" onClick={() => void onCreateExport()}>
                <Download className="h-4 w-4" />
                Create export
              </Button>
            </div>
          }
        />

        <div className="grid shrink-0 gap-4 md:grid-cols-2 xl:grid-cols-4">
          {loading && !snapshot
            ? Array.from({ length: 4 }).map((_, i) => (
                <Card key={i}>
                  <CardBody>
                    <SkeletonRows rows={2} />
                  </CardBody>
                </Card>
              ))
            : [
                { label: "Projects", value: String(metrics.projects_total ?? "—") },
                { label: "Tickets open", value: String(metrics.tickets_open ?? "—") },
                { label: "Bugs open", value: String(metrics.bugs_open ?? "—") },
                {
                  label: "Freshness",
                  value: snapshot?.is_fresh ? "Fresh" : snapshot ? "Stale" : "—",
                },
              ].map((card) => (
                <Card key={card.label}>
                  <CardBody>
                    <p className="text-xs font-medium uppercase tracking-wide text-[var(--muted)]">
                      {card.label}
                    </p>
                    <p className="mt-2 font-display text-2xl tracking-tight">{card.value}</p>
                  </CardBody>
                </Card>
              ))}
        </div>

        {snapshot ? (
          <p className="shrink-0 text-sm text-[var(--muted)]">
            Snapshot refreshed {formatUtc(snapshot.refreshed_at)}
            {snapshot.is_fresh ? " · fresh (under 60s)" : " · stale"} · reconciled=
            {String(metrics.reconciled ?? false)}
          </p>
        ) : null}

        <div className="grid min-h-0 flex-1 gap-4 xl:grid-cols-2">
          <Card className="flex min-h-0 flex-col overflow-hidden">
            <CardHeader className="shrink-0">
              <h2 className="font-display text-lg">Search</h2>
              <p className="text-sm text-[var(--muted)]">Indexed documents only (org-scoped).</p>
            </CardHeader>
            <CardBody className="shrink-0">
              <form onSubmit={onSearch} className="flex gap-2" aria-label="Global search">
                <Input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Search indexed titles…"
                  aria-label="Search query"
                />
                <Button type="submit">
                  <Search className="h-4 w-4" />
                  Search
                </Button>
              </form>
            </CardBody>
            <ScrollRegion className="flex-1">
              {searchHits.length === 0 ? (
                <CardBody>
                  <EmptyState title="No hits" body="Index documents via API, then search here." />
                </CardBody>
              ) : (
                <ul className="divide-y divide-[var(--line)]">
                  {searchHits.map((hit) => (
                    <li key={hit.id} className="px-5 py-3">
                      <p className="font-medium">{hit.title}</p>
                      <p className="text-xs text-[var(--muted)]">
                        {hit.entity_type} · {hit.classification} · {formatUtc(hit.indexed_at)}
                      </p>
                    </li>
                  ))}
                </ul>
              )}
            </ScrollRegion>
          </Card>

          <Card className="flex min-h-0 flex-col overflow-hidden">
            <CardHeader className="shrink-0">
              <h2 className="font-display text-lg">Activity</h2>
            </CardHeader>
            <ScrollRegion className="flex-1">
              {loading ? (
                <SkeletonRows />
              ) : activity.length === 0 ? (
                <CardBody>
                  <EmptyState title="No activity" body="Record activity events via the insights API." />
                </CardBody>
              ) : (
                <ul className="divide-y divide-[var(--line)]">
                  {activity.map((item) => (
                    <li key={item.id} className="px-5 py-3">
                      <p className="text-sm font-medium">{item.summary}</p>
                      <p className="text-xs text-[var(--muted)]">
                        {item.event_type} · {item.entity_type} · {formatUtc(item.occurred_at)}
                      </p>
                    </li>
                  ))}
                </ul>
              )}
            </ScrollRegion>
          </Card>

          <Card className="flex min-h-0 flex-col overflow-hidden">
            <CardHeader className="shrink-0">
              <h2 className="font-display text-lg">Saved filters</h2>
            </CardHeader>
            <CardBody className="shrink-0">
              <form onSubmit={onCreateFilter} className="grid gap-3 md:grid-cols-2" aria-label="Create saved filter">
                <Field label="Name">
                  <Input required value={filterName} onChange={(e) => setFilterName(e.target.value)} />
                </Field>
                <Field label="Filter JSON">
                  <Input required value={filterJson} onChange={(e) => setFilterJson(e.target.value)} />
                </Field>
                <div className="md:col-span-2">
                  <Button type="submit">
                    <Plus className="h-4 w-4" />
                    Save filter
                  </Button>
                </div>
              </form>
            </CardBody>
            <ScrollRegion className="flex-1">
              {filters.length === 0 ? (
                <CardBody>
                  <EmptyState title="No saved filters" body="Create a filter to reuse desk queries." />
                </CardBody>
              ) : (
                <ul className="divide-y divide-[var(--line)]">
                  {filters.map((item) => (
                    <li key={item.id} className="px-5 py-3">
                      <p className="font-medium">{item.name}</p>
                      <p className="text-xs text-[var(--muted)]">
                        {item.module_key} · {item.is_shared ? "shared" : "private"}
                      </p>
                    </li>
                  ))}
                </ul>
              )}
            </ScrollRegion>
          </Card>

          <Card className="flex min-h-0 flex-col overflow-hidden">
            <CardHeader className="shrink-0">
              <h2 className="font-display text-lg">Exports</h2>
              <p className="text-sm text-[var(--muted)]">In-DB payload preview only (not S3).</p>
            </CardHeader>
            <ScrollRegion className="flex-1">
              {exports.length === 0 ? (
                <CardBody>
                  <EmptyState title="No exports" body="Create an export to capture org metrics preview." />
                </CardBody>
              ) : (
                <ul className="divide-y divide-[var(--line)]">
                  {exports.map((item) => (
                    <li key={item.id} className="flex items-center justify-between gap-3 px-5 py-3">
                      <div>
                        <p className="font-medium">{item.export_format.toUpperCase()} · {item.row_count} rows</p>
                        <p className="text-xs text-[var(--muted)]">{formatUtc(item.created_at)}</p>
                      </div>
                      <StatusBadge status={item.status} />
                    </li>
                  ))}
                </ul>
              )}
            </ScrollRegion>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}
