"use client";

import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import { Plus, Search } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Textarea } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  createQuery,
  createQuerySource,
  formatUtc,
  listQueries,
  transitionQuery,
  type ClientQuery,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";
import { can } from "@/lib/roles";
import { getWorkspaceQueryId, setWorkspaceQueryId } from "@/lib/workspace";

type FilterTab = {
  id: string;
  label: string;
  status?: string;
  sla_status?: string;
};

const FILTER_TABS: FilterTab[] = [
  { id: "all", label: "All" },
  { id: "new", label: "New", status: "received" },
  { id: "classified", label: "Classified", status: "classified" },
  { id: "qualifying", label: "Qualifying", status: "qualifying" },
  { id: "qualified", label: "Qualified", status: "qualified" },
  { id: "overdue", label: "Overdue", sla_status: "breached" },
];

const NEXT_ACTIONS: Record<string, { next: string; label: string; classification?: string }[]> = {
  received: [{ next: "classified", label: "Mark classified", classification: "new_build" }],
  classified: [{ next: "qualifying", label: "Start qualifying" }],
  qualifying: [{ next: "qualified", label: "Mark qualified" }],
};

export function QueriesDeskPage() {
  const { session } = useSession();
  const [items, setItems] = useState<ClientQuery[]>([]);
  const [loading, setLoading] = useState(true);
  const [sourceId, setSourceId] = useState("");
  const [subject, setSubject] = useState("");
  const [summary, setSummary] = useState("");
  const [currentId, setCurrentId] = useState<string | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [activeTab, setActiveTab] = useState("all");
  const [search, setSearch] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const tab = FILTER_TABS.find((t) => t.id === activeTab) ?? FILTER_TABS[0];
      const rows = await listQueries(session, {
        status: tab.status,
        sla_status: tab.sla_status,
        q: search.trim() || undefined,
        limit: 100,
      });
      setItems(rows);
      const workspaceId = getWorkspaceQueryId();
      setCurrentId((prev) => {
        if (prev && rows.some((r) => r.id === prev)) return prev;
        if (workspaceId && rows.some((r) => r.id === workspaceId)) return workspaceId;
        return rows[0]?.id ?? null;
      });
    } catch (err) {
      notifyApiError("Unable to load inquiries", err);
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, [session, activeTab, search]);

  useEffect(() => {
    void load();
  }, [load]);

  const current = useMemo(
    () => items.find((item) => item.id === currentId) ?? null,
    [items, currentId],
  );

  async function ensureSource() {
    if (sourceId) return sourceId;
    const source = await createQuerySource(session, {
      code: `web_${Date.now().toString(36)}`,
      title: "Web intake",
      channel: "web",
    });
    setSourceId(source.id);
    return source.id;
  }

  async function onCreate(event: FormEvent) {
    event.preventDefault();
    try {
      const sid = await ensureSource();
      const created = await createQuery(session, {
        subject: subject.trim(),
        summary: summary.trim(),
        source_id: sid,
      });
      setWorkspaceQueryId(created.id);
      setCurrentId(created.id);
      notifySuccess("Inquiry captured");
      setSubject("");
      setSummary("");
      setShowCreate(false);
      setActiveTab("all");
      await load();
    } catch (err) {
      notifyApiError("Could not create inquiry", err);
    }
  }

  async function onTransition(next: string, classification?: string) {
    if (!current) return;
    try {
      const updated = await transitionQuery(session, current.id, {
        next_status: next,
        classification,
      });
      notifySuccess(`Moved to ${updated.status.replace(/_/g, " ")}`);
      await load();
    } catch (err) {
      notifyApiError("Transition failed", err);
    }
  }

  function selectQuery(id: string) {
    setCurrentId(id);
    setWorkspaceQueryId(id);
  }

  const actions = current ? NEXT_ACTIONS[current.status] ?? [] : [];

  return (
    <AppShell title="Queries" breadcrumbs={["Business Development", "Queries"]}>
      <PageHeader
        title="Queries"
        description="Business-development inbox for new inquiries — qualify, respond, and route to opportunities."
        actions={
          can(session.variant, "create") ? (
            <Button onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              New inquiry
            </Button>
          ) : null
        }
      />

      <div className="mb-4 flex flex-wrap items-center gap-2">
        {FILTER_TABS.map((tab) => (
          <button
            key={tab.id}
            type="button"
            onClick={() => setActiveTab(tab.id)}
            className={`rounded-full px-3 py-1 text-xs font-medium ${
              activeTab === tab.id
                ? "bg-[var(--accent-soft)] text-[var(--accent)]"
                : "border border-[var(--line)] bg-[var(--surface)] text-[var(--muted)]"
            }`}
          >
            {tab.label}
          </button>
        ))}
        <div className="relative ml-auto min-w-[12rem] flex-1 max-w-xs">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--muted)]" />
          <Input
            className="pl-9"
            placeholder="Search subject or summary"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            aria-label="Search inquiries"
          />
        </div>
      </div>

      {showCreate ? (
        <Card className="mb-6">
          <CardHeader>
            <h2 className="font-display text-lg">Capture inquiry</h2>
            <p className="text-sm text-[var(--muted)]">
              Record what the client asked for so BD and AI agents can qualify next steps.
            </p>
          </CardHeader>
          <CardBody>
            <form onSubmit={onCreate} className="grid gap-4" aria-label="Create inquiry">
              <Field label="Subject">
                <Input
                  required
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  placeholder="Mobile app for field crews"
                />
              </Field>
              <Field label="Summary">
                <Textarea
                  required
                  rows={4}
                  value={summary}
                  onChange={(e) => setSummary(e.target.value)}
                  placeholder="What they need, timeline, and any known constraints"
                />
              </Field>
              <div className="flex justify-end gap-2">
                <Button type="button" variant="ghost" onClick={() => setShowCreate(false)}>
                  Cancel
                </Button>
                <Button type="submit">Save inquiry</Button>
              </div>
            </form>
          </CardBody>
        </Card>
      ) : null}

      {loading ? (
        <SkeletonRows rows={5} />
      ) : items.length === 0 ? (
        <EmptyState
          title="No inquiries found"
          body="New inbound requests appear here. Capture an inquiry or change the filter."
          action={
            can(session.variant, "create") ? (
              <Button onClick={() => setShowCreate(true)}>New inquiry</Button>
            ) : null
          }
        />
      ) : (
        <div className="grid gap-4 lg:grid-cols-[0.9fr_1.1fr]">
          <Card>
            <CardHeader>
              <h2 className="font-display text-lg">Inbox</h2>
              <p className="text-sm text-[var(--muted)]">{items.length} inquiries</p>
            </CardHeader>
            <CardBody className="space-y-2">
              {items.map((item) => {
                const selected = item.id === currentId;
                return (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => selectQuery(item.id)}
                    className={`w-full rounded-lg border px-3 py-3 text-left transition ${
                      selected
                        ? "border-[var(--accent)] bg-[var(--accent-soft)]"
                        : "border-[var(--line)] bg-[var(--surface)] hover:border-[var(--accent)]"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <p className="font-medium text-[var(--ink)]">{item.subject}</p>
                        <p className="mt-1 line-clamp-2 text-xs text-[var(--muted)]">
                          {item.summary}
                        </p>
                        <p className="mt-1 text-[11px] text-[var(--muted)]">
                          {formatUtc(item.created_at)}
                        </p>
                      </div>
                      <StatusBadge status={item.status} />
                    </div>
                  </button>
                );
              })}
            </CardBody>
          </Card>

          {current ? (
            <div className="grid gap-4">
              <Card>
                <CardHeader className="flex items-start justify-between gap-3">
                  <div>
                    <h2 className="font-display text-xl">{current.subject}</h2>
                    <p className="mt-1 text-sm text-[var(--muted)]">{current.summary}</p>
                  </div>
                  <StatusBadge status={current.status} />
                </CardHeader>
                <CardBody className="space-y-3">
                  <p className="text-sm text-[var(--muted)]">
                    SLA: {current.sla_status.replace(/_/g, " ")} · Created{" "}
                    {formatUtc(current.created_at)}
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {actions.map((action) => (
                      <Button
                        key={action.next}
                        variant="outline"
                        size="sm"
                        onClick={() => void onTransition(action.next, action.classification)}
                      >
                        {action.label}
                      </Button>
                    ))}
                    {actions.length === 0 ? (
                      <p className="text-sm text-[var(--muted)]">
                        No further intake transitions from status{" "}
                        {current.status.replace(/_/g, " ")}.
                      </p>
                    ) : null}
                  </div>
                </CardBody>
              </Card>
              <Card>
                <CardHeader>
                  <h3 className="font-display text-lg">BD assistant</h3>
                </CardHeader>
                <CardBody className="space-y-3 text-sm">
                  <p className="text-[var(--muted)]">
                    Completeness and clarification prompts will appear here once requirement
                    gathering is linked to this inquiry.
                  </p>
                  <Button variant="ai" size="sm">
                    Generate clarifying questions
                  </Button>
                </CardBody>
              </Card>
            </div>
          ) : null}
        </div>
      )}
    </AppShell>
  );
}
