"use client";

import { useCallback, useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { ListPagination } from "@/components/list-pagination";
import { ScrollRegion } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Card, CardBody } from "@/components/ui/card";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  EMPTY_PAGE_META,
  formatUtc,
  listAuditLogs,
  type ObservabilityAuditLog,
  type PageMeta,
} from "@/lib/api";
import { notifyApiError } from "@/lib/toast";

export function AuditLogsDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<ObservabilityAuditLog[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await listAuditLogs(session, { limit, offset });
      setItems(result.items);
      setPageMeta(result.page);
    } catch (err) {
      notifyApiError("Unable to load audit logs", err);
      setItems([]);
      setPageMeta(EMPTY_PAGE_META);
    } finally {
      setLoading(false);
    }
  }, [session, limit, offset]);

  useEffect(() => {
    void load();
  }, [load]);

  return (
    <AppShell>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Audit Logs"
          description="Append-only operational audit trail. Mutations are refused by the API."
        />
        <ScrollRegion>
          <Card>
            <CardBody>
              {loading ? (
                <SkeletonRows />
              ) : items.length === 0 ? (
                <EmptyState
                  title="No audit events"
                  body="Actions in this organization will appear here."
                />
              ) : (
                <ul className="divide-y divide-[var(--line)]">
                  {items.map((row) => (
                    <li key={row.id} className="py-3">
                      <p className="font-medium">
                        {row.action} · {row.entity_type}
                      </p>
                      <p className="text-sm text-[var(--muted)]">
                        {formatUtc(row.created_at)} · actor {row.actor_kind} · entity{" "}
                        {row.entity_id.slice(0, 8)}
                      </p>
                    </li>
                  ))}
                </ul>
              )}
              <ListPagination
                page={pageMeta}
                onOffsetChange={setOffset}
                onLimitChange={setLimit}
                label="events"
              />
            </CardBody>
          </Card>
        </ScrollRegion>
      </div>
    </AppShell>
  );
}
