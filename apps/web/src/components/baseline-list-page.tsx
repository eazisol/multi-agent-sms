"use client";

import Link from "next/link";
import { FormEvent, useCallback, useEffect, useState } from "react";
import { Plus, Search } from "lucide-react";

import { ListPagination } from "@/components/list-pagination";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Select } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows, StatusBanner } from "@/components/ui-states";
import {
  EMPTY_PAGE_META,
  formatUtc,
  listBaselines,
  type Baseline,
  type PageMeta,
} from "@/lib/api";
import { notifyApiError } from "@/lib/toast";
import { can } from "@/lib/roles";

export function BaselineListPage() {
  const { session } = useSession();
  const [items, setItems] = useState<Baseline[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [q, setQ] = useState("");
  const [status, setStatus] = useState("");
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(10);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const page = await listBaselines(session, {
        limit,
        offset,
        q: q || undefined,
        status: status || undefined,
        sort: "baseline_key",
      });
      setItems(page.items);
      setPageMeta(page.page);
    } catch (err) {
      notifyApiError("Unable to load baselines", err);
      setItems([]);
      setPageMeta(EMPTY_PAGE_META);
    } finally {
      setLoading(false);
    }
  }, [session, offset, limit, q, status]);

  useEffect(() => {
    void load();
  }, [load]);

  function onFilter(event: FormEvent) {
    event.preventDefault();
    setOffset(0);
    void load();
  }

  if (!can(session.variant, "view_list")) {
    return (
      <StatusBanner kind="error">Your role cannot view source baselines.</StatusBanner>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Source baselines"
        description="Approved sources of truth for requirements, architecture, and delivery governance."
        actions={
          can(session.variant, "create") ? (
            <Link href="/governance/baselines/new">
              <Button>
                <Plus className="h-4 w-4" />
                New baseline
              </Button>
            </Link>
          ) : null
        }
      />

      <Card>
        <CardHeader>
          <form
            onSubmit={onFilter}
            className="flex flex-wrap items-end gap-3"
            aria-label="Filter baselines"
          >
            <Field label="Search" className="min-w-[220px] flex-1">
              <div className="relative">
                <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--muted)]" />
                <Input
                  className="pl-9"
                  value={q}
                  onChange={(event) => setQ(event.target.value)}
                  placeholder="Key or title"
                />
              </div>
            </Field>
            <Field label="Status" className="min-w-[160px]">
              <Select value={status} onChange={(event) => setStatus(event.target.value)}>
                <option value="">Any</option>
                <option value="draft">Draft</option>
                <option value="submitted">Submitted</option>
                <option value="under_review">Under review</option>
                <option value="approved">Approved</option>
                <option value="rejected">Rejected</option>
              </Select>
            </Field>
            <Button type="submit" variant="outline">
              Apply
            </Button>
          </form>
        </CardHeader>

        {loading ? (
          <SkeletonRows />
        ) : items.length === 0 ? (
          <CardBody>
            <EmptyState
              title="No baselines yet"
              body="Create the first source baseline when your role allows it."
              action={
                can(session.variant, "create") ? (
                  <Link href="/governance/baselines/new">
                    <Button>
                      <Plus className="h-4 w-4" />
                      Create baseline
                    </Button>
                  </Link>
                ) : null
              }
            />
          </CardBody>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead className="sticky top-0 bg-[var(--surface-muted)] text-xs uppercase tracking-wide text-[var(--muted)]">
                <tr>
                  <th className="px-5 py-3 font-medium">Key</th>
                  <th className="px-5 py-3 font-medium">Title</th>
                  <th className="px-5 py-3 font-medium">Status</th>
                  <th className="px-5 py-3 font-medium">Version</th>
                  <th className="px-5 py-3 font-medium">Updated</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item) => (
                  <tr
                    key={item.id}
                    className="border-t border-[var(--line)] hover:bg-[var(--surface-muted)]/70"
                  >
                    <td className="px-5 py-3">
                      <Link
                        className="font-medium text-[var(--accent)] underline-offset-2 hover:underline"
                        href={`/governance/baselines/${item.id}`}
                      >
                        {item.baseline_key}
                      </Link>
                    </td>
                    <td className="px-5 py-3">{item.title}</td>
                    <td className="px-5 py-3">
                      <StatusBadge status={item.approval_status} />
                    </td>
                    <td className="px-5 py-3 text-[var(--muted)]">{item.version}</td>
                    <td className="px-5 py-3 text-[var(--muted)]">{formatUtc(item.updated_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        {!loading && (items.length > 0 || pageMeta.total > 0) ? (
          <ListPagination
            page={pageMeta}
            onOffsetChange={setOffset}
            onLimitChange={setLimit}
            label="baselines"
          />
        ) : null}
      </Card>
    </div>
  );
}
