"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Plus } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { ListPagination } from "@/components/list-pagination";
import { ScrollRegion } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Select, Textarea } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  EMPTY_PAGE_META,
  createArchitectureDecision,
  listArchitectureDecisions,
  transitionArchitectureDecision,
  type ArchitectureDecision,
  type PageMeta,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";

export function ArchitectureDecisionsDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<ArchitectureDecision[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);
  const [status, setStatus] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [adrKey, setAdrKey] = useState("");
  const [title, setTitle] = useState("");
  const [context, setContext] = useState("");
  const [decision, setDecision] = useState("");
  const [consequences, setConsequences] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await listArchitectureDecisions(session, {
        status: status || undefined,
        limit,
        offset,
      });
      setItems(result.items);
      setPageMeta(result.page);
    } catch (err) {
      notifyApiError("Unable to load architecture decisions", err);
      setItems([]);
      setPageMeta(EMPTY_PAGE_META);
    } finally {
      setLoading(false);
    }
  }, [session, status, limit, offset]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onCreate(event: FormEvent) {
    event.preventDefault();
    try {
      await createArchitectureDecision(session, {
        adr_key: adrKey.trim(),
        title: title.trim(),
        context: context.trim(),
        decision: decision.trim(),
        consequences: consequences.trim(),
      });
      notifySuccess("ADR created as proposed");
      setAdrKey("");
      setTitle("");
      setContext("");
      setDecision("");
      setConsequences("");
      setShowCreate(false);
      setOffset(0);
      await load();
    } catch (err) {
      notifyApiError("Could not create ADR", err);
    }
  }

  async function onAccept(row: ArchitectureDecision) {
    try {
      await transitionArchitectureDecision(session, row.id, {
        target_status: "accepted",
        expected_version: row.version,
        reason: "Accepted from architecture desk",
      });
      notifySuccess("ADR accepted");
      await load();
    } catch (err) {
      notifyApiError("Could not accept ADR", err);
    }
  }

  return (
    <AppShell>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Architecture Decisions"
          description="ADR register. Accepting an ADR requires a human actor (governance)."
          actions={
            <Button type="button" onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              New ADR
            </Button>
          }
        />

        <div className="flex shrink-0 gap-2">
          <Select value={status} onChange={(e) => { setStatus(e.target.value); setOffset(0); }}>
            <option value="">All statuses</option>
            <option value="proposed">proposed</option>
            <option value="accepted">accepted</option>
            <option value="deprecated">deprecated</option>
            <option value="superseded">superseded</option>
          </Select>
        </div>

        {showCreate ? (
          <Card className="shrink-0">
            <CardHeader>
              <h2 className="font-display text-lg">Propose ADR</h2>
            </CardHeader>
            <CardBody>
              <form onSubmit={onCreate} className="grid gap-4 md:grid-cols-2" aria-label="Create ADR">
                <Field label="ADR key">
                  <Input required value={adrKey} onChange={(e) => setAdrKey(e.target.value)} placeholder="ADR-001" />
                </Field>
                <Field label="Title">
                  <Input required value={title} onChange={(e) => setTitle(e.target.value)} />
                </Field>
                <Field label="Context" className="md:col-span-2">
                  <Textarea required rows={3} value={context} onChange={(e) => setContext(e.target.value)} />
                </Field>
                <Field label="Decision" className="md:col-span-2">
                  <Textarea required rows={3} value={decision} onChange={(e) => setDecision(e.target.value)} />
                </Field>
                <Field label="Consequences" className="md:col-span-2">
                  <Textarea required rows={3} value={consequences} onChange={(e) => setConsequences(e.target.value)} />
                </Field>
                <Button type="submit">Create</Button>
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
                <EmptyState title="No ADRs" body="Propose an architecture decision." />
              ) : (
                <ul className="divide-y divide-[var(--line)]">
                  {items.map((row) => (
                    <li key={row.id} className="flex items-start justify-between gap-3 py-3">
                      <div>
                        <p className="font-medium">
                          {row.adr_key} · {row.title}
                        </p>
                        <p className="text-sm text-[var(--muted)]">{row.decision}</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <StatusBadge status={row.status} />
                        {row.status === "proposed" ? (
                          <Button type="button" variant="ghost" onClick={() => void onAccept(row)}>
                            Accept
                          </Button>
                        ) : null}
                      </div>
                    </li>
                  ))}
                </ul>
              )}
              <ListPagination
                page={pageMeta}
                onOffsetChange={setOffset}
                onLimitChange={setLimit}
                label="ADRs"
              />
            </CardBody>
          </Card>
        </ScrollRegion>
      </div>
    </AppShell>
  );
}
