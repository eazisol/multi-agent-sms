"use client";

import { useCallback, useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { ScrollRegion } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import { listAgentDefinitions, type AgentDefinition } from "@/lib/api";
import { notifyApiError } from "@/lib/toast";

export function AgentsDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<AgentDefinition[]>([]);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await listAgentDefinitions(session);
      setItems(result);
    } catch (err) {
      notifyApiError("Unable to load agent definitions", err);
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    void load();
  }, [load]);

  return (
    <AppShell>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Agents"
          description="Agent runtime registry (MOD-360). Seeded catalog codes with stub LangGraph execution."
        />

        <Card className="flex min-h-0 flex-1 flex-col overflow-hidden">
          <CardHeader className="shrink-0">
            <h2 className="font-display text-lg">Agent definitions</h2>
            <p className="text-sm text-[var(--muted)]">From `/api/v1/agent-runtime/definitions`.</p>
          </CardHeader>
          {loading ? (
            <SkeletonRows />
          ) : items.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No agents"
                body="Definitions seed automatically when the agent-runtime API is called."
              />
            </CardBody>
          ) : (
            <ScrollRegion className="flex-1">
              <ul className="divide-y divide-[var(--line)]">
                {items.map((item) => (
                  <li key={item.id} className="px-5 py-3">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div>
                        <span className="font-medium">{item.title}</span>
                        <p className="text-xs text-[var(--muted)]">{item.code}</p>
                      </div>
                      <StatusBadge status={item.status} />
                    </div>
                    <p className="mt-1 text-xs text-[var(--muted)]">
                      {item.department_code} · authority {item.authority_level}
                    </p>
                  </li>
                ))}
              </ul>
            </ScrollRegion>
          )}
        </Card>
      </div>
    </AppShell>
  );
}
