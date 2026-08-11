"use client";

import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import {
  ArrowRight,
  Clock3,
  Inbox,
  MessageSquareText,
  Plus,
  Search,
  Sparkles,
} from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { ListPagination } from "@/components/list-pagination";
import { ScrollRegion } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Textarea } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  EMPTY_PAGE_META,
  createQuery,
  createQuerySource,
  formatUtc,
  listQueries,
  transitionQuery,
  type ClientQuery,
  type PageMeta,
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

function slaTone(sla: string) {
  if (sla === "breached") return "text-[var(--danger)]";
  if (sla === "at_risk") return "text-[var(--warning)]";
  if (sla === "met") return "text-[var(--success)]";
  return "text-[var(--muted)]";
}

export function QueriesDeskPage() {
  const { session } = useSession();
  const [items, setItems] = useState<ClientQuery[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [loading, setLoading] = useState(true);
  const [sourceId, setSourceId] = useState("");
  const [subject, setSubject] = useState("");
  const [summary, setSummary] = useState("");
  const [currentId, setCurrentId] = useState<string | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [activeTab, setActiveTab] = useState("all");
  const [search, setSearch] = useState("");
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const tab = FILTER_TABS.find((t) => t.id === activeTab) ?? FILTER_TABS[0];
      const result = await listQueries(session, {
        status: tab.status,
        sla_status: tab.sla_status,
        q: search.trim() || undefined,
        limit,
        offset,
      });
      setItems(result.items);
      setPageMeta(result.page);
      const rows = result.items;
      const workspaceId = getWorkspaceQueryId();
      setCurrentId((prev) => {
        if (prev && rows.some((r) => r.id === prev)) return prev;
        if (workspaceId && rows.some((r) => r.id === workspaceId)) return workspaceId;
        return rows[0]?.id ?? null;
      });
    } catch (err) {
      notifyApiError("Unable to load inquiries", err);
      setItems([]);
      setPageMeta(EMPTY_PAGE_META);
    } finally {
      setLoading(false);
    }
  }, [session, activeTab, search, limit, offset]);

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
      setOffset(0);
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
  const activeFilterLabel =
    FILTER_TABS.find((tab) => tab.id === activeTab)?.label ?? "All";

  return (
    <AppShell title="Queries" breadcrumbs={["Business Development", "Queries"]} fill>
      <div className="flex min-h-0 flex-1 flex-col gap-4">
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

        <Card className="shrink-0 overflow-hidden">
          <CardBody className="flex flex-col gap-3 py-3 sm:flex-row sm:items-center">
            <div
              className="flex flex-wrap gap-1 rounded-[var(--radius-md)] bg-[var(--surface-muted)] p-1"
              role="tablist"
              aria-label="Filter inquiries"
            >
              {FILTER_TABS.map((tab) => {
                const active = activeTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    type="button"
                    role="tab"
                    aria-selected={active}
                    onClick={() => {
                      setActiveTab(tab.id);
                      setOffset(0);
                    }}
                    className={`rounded-[var(--radius-sm)] px-3 py-1.5 text-xs font-medium transition ${
                      active
                        ? "bg-[var(--surface)] text-[var(--ink)] shadow-sm ring-1 ring-[var(--line)]"
                        : "text-[var(--muted)] hover:text-[var(--ink)]"
                    }`}
                  >
                    {tab.label}
                  </button>
                );
              })}
            </div>
            <div className="relative min-w-[12rem] flex-1 sm:ml-auto sm:max-w-sm">
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--muted)]" />
              <Input
                className="pl-9"
                placeholder="Search subject or summary"
                value={search}
                onChange={(e) => {
                  setSearch(e.target.value);
                  setOffset(0);
                }}
                aria-label="Search inquiries"
              />
            </div>
          </CardBody>
        </Card>

        {showCreate ? (
          <Card className="shrink-0 border-[var(--accent)]/30 shadow-float">
            <CardHeader className="bg-[var(--surface-muted)]/60">
              <div className="flex items-start gap-3">
                <div className="mt-0.5 flex h-9 w-9 items-center justify-center rounded-[var(--radius-md)] bg-[var(--accent-soft)] text-[var(--accent)]">
                  <MessageSquareText className="h-4 w-4" />
                </div>
                <div>
                  <h2 className="font-display text-lg">Capture inquiry</h2>
                  <p className="mt-1 text-sm text-[var(--muted)]">
                    Record what the client asked for so BD and AI agents can qualify next steps.
                  </p>
                </div>
              </div>
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
          <Card className="min-h-0 flex-1">
            <SkeletonRows rows={6} />
          </Card>
        ) : items.length === 0 && pageMeta.total === 0 ? (
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
          <div className="grid min-h-0 flex-1 gap-4 overflow-hidden lg:grid-cols-[minmax(18rem,0.95fr)_minmax(0,1.25fr)]">
            <Card className="flex min-h-0 flex-col overflow-hidden">
              <CardHeader className="flex shrink-0 flex-row items-center justify-between gap-3 bg-[var(--surface-muted)]/40 py-3.5">
                <div className="flex items-center gap-2.5">
                  <div className="flex h-8 w-8 items-center justify-center rounded-[var(--radius-sm)] bg-[var(--accent-soft)] text-[var(--accent)]">
                    <Inbox className="h-4 w-4" />
                  </div>
                  <div>
                    <h2 className="font-display text-base leading-tight">Inbox</h2>
                    <p className="text-xs text-[var(--muted)]">
                      {pageMeta.total} · {activeFilterLabel}
                    </p>
                  </div>
                </div>
              </CardHeader>
              {items.length === 0 ? (
                <CardBody>
                  <EmptyState
                    title="No inquiries on this page"
                    body="Try the previous page or change the filter."
                    className="border-0 bg-transparent py-10"
                  />
                </CardBody>
              ) : (
                <ScrollRegion className="flex-1">
                  <ul className="divide-y divide-[var(--line)]" role="listbox" aria-label="Inquiry inbox">
                    {items.map((item) => {
                      const selected = item.id === currentId;
                      const breached = item.sla_status === "breached";
                      return (
                        <li key={item.id}>
                          <button
                            type="button"
                            role="option"
                            aria-selected={selected}
                            onClick={() => selectQuery(item.id)}
                            className={`relative w-full px-4 py-3.5 text-left transition ${
                              selected
                                ? "bg-[var(--accent-soft)]/70"
                                : "bg-transparent hover:bg-[var(--surface-muted)]/80"
                            }`}
                          >
                            {selected ? (
                              <span
                                aria-hidden
                                className="absolute inset-y-2 left-0 w-0.5 rounded-full bg-[var(--accent)]"
                              />
                            ) : null}
                            <div className="flex items-start justify-between gap-3">
                              <div className="min-w-0 flex-1">
                                <p className="truncate font-medium text-[var(--ink)]">{item.subject}</p>
                                <p className="mt-1 line-clamp-2 text-xs leading-relaxed text-[var(--muted)]">
                                  {item.summary}
                                </p>
                                <div className="mt-2 flex flex-wrap items-center gap-x-2 gap-y-1 text-[11px] text-[var(--muted)]">
                                  <span className="inline-flex items-center gap-1">
                                    <Clock3 className="h-3 w-3" />
                                    {formatUtc(item.created_at)}
                                  </span>
                                  <span aria-hidden>·</span>
                                  <span className={slaTone(item.sla_status)}>
                                    SLA {item.sla_status.replace(/_/g, " ")}
                                    {breached ? " · overdue" : ""}
                                  </span>
                                </div>
                              </div>
                              <StatusBadge status={item.status} className="shrink-0" />
                            </div>
                          </button>
                        </li>
                      );
                    })}
                  </ul>
                </ScrollRegion>
              )}
              {items.length > 0 || pageMeta.total > 0 ? (
                <div className="shrink-0">
                  <ListPagination
                    page={pageMeta}
                    onOffsetChange={setOffset}
                    onLimitChange={setLimit}
                    label="inquiries"
                  />
                </div>
              ) : null}
            </Card>

            {current ? (
              <ScrollRegion className="min-h-0">
                <div className="grid gap-4 pb-2">
                  <Card className="overflow-hidden">
                    <div className="border-b border-[var(--line)] bg-[linear-gradient(180deg,color-mix(in_srgb,var(--accent-soft)_55%,transparent),transparent)] px-5 py-5">
                      <div className="flex flex-wrap items-start justify-between gap-3">
                        <div className="min-w-0 flex-1">
                          <p className="text-xs font-medium uppercase tracking-wide text-[var(--muted)]">
                            Inquiry detail
                          </p>
                          <h2 className="mt-1 font-display text-2xl leading-tight tracking-tight">
                            {current.subject}
                          </h2>
                          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-[var(--muted)]">
                            {current.summary}
                          </p>
                        </div>
                        <StatusBadge status={current.status} />
                      </div>
                      <div className="mt-4 grid gap-2 sm:grid-cols-2">
                        <div className="rounded-[var(--radius-md)] border border-[var(--line)] bg-[var(--surface)]/80 px-3 py-2.5">
                          <p className="text-[11px] uppercase tracking-wide text-[var(--muted)]">SLA</p>
                          <p className={`mt-0.5 text-sm font-medium ${slaTone(current.sla_status)}`}>
                            {current.sla_status.replace(/_/g, " ")}
                          </p>
                        </div>
                        <div className="rounded-[var(--radius-md)] border border-[var(--line)] bg-[var(--surface)]/80 px-3 py-2.5">
                          <p className="text-[11px] uppercase tracking-wide text-[var(--muted)]">Created</p>
                          <p className="mt-0.5 text-sm font-medium text-[var(--ink)]">
                            {formatUtc(current.created_at)}
                          </p>
                        </div>
                      </div>
                    </div>
                    <CardBody className="space-y-3">
                      <p className="text-xs font-medium uppercase tracking-wide text-[var(--muted)]">
                        Next action
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
                            <ArrowRight className="h-3.5 w-3.5" />
                          </Button>
                        ))}
                        {actions.length === 0 ? (
                          <p className="rounded-[var(--radius-md)] border border-dashed border-[var(--line-strong)] bg-[var(--surface-muted)]/50 px-3 py-2.5 text-sm text-[var(--muted)]">
                            No further intake transitions from status{" "}
                            <span className="font-medium text-[var(--ink)]">
                              {current.status.replace(/_/g, " ")}
                            </span>
                            .
                          </p>
                        ) : null}
                      </div>
                    </CardBody>
                  </Card>

                  <Card className="overflow-hidden border-[var(--accent)]/20">
                    <CardHeader className="bg-[linear-gradient(135deg,color-mix(in_srgb,var(--ai-from)_18%,transparent),color-mix(in_srgb,var(--ai-to)_12%,transparent))]">
                      <div className="flex items-center gap-2.5">
                        <div className="flex h-8 w-8 items-center justify-center rounded-full ai-gradient text-white shadow-sm">
                          <Sparkles className="h-4 w-4" />
                        </div>
                        <div>
                          <h3 className="font-display text-base">BD assistant</h3>
                          <p className="text-xs text-[var(--muted)]">Guided qualification support</p>
                        </div>
                      </div>
                    </CardHeader>
                    <CardBody className="space-y-4 text-sm">
                      <p className="leading-relaxed text-[var(--muted)]">
                        Completeness and clarification prompts will appear here once requirement
                        gathering is linked to this inquiry.
                      </p>
                      <Button variant="ai" size="sm">
                        <Sparkles className="h-3.5 w-3.5" />
                        Generate clarifying questions
                      </Button>
                    </CardBody>
                  </Card>
                </div>
              </ScrollRegion>
            ) : (
              <Card className="flex min-h-[16rem] items-center justify-center">
                <EmptyState
                  title="Select an inquiry"
                  body="Choose a row from the inbox to review status, SLA, and next steps."
                  className="border-0 bg-transparent"
                />
              </Card>
            )}
          </div>
        )}
      </div>
    </AppShell>
  );
}
