"use client";

import Link from "next/link";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  Clock3,
} from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  formatUtc,
  listApprovals,
  listOpenFollowUps,
  listProjects,
  listQueries,
  refreshInsightsDashboard,
  type ApprovalRequest,
  type FollowUp,
  type InsightsDashboardSnapshot,
  type Project,
  type ClientQuery,
} from "@/lib/api";
import { notifyApiError } from "@/lib/toast";

type AttentionItem = {
  title: string;
  meta: string;
  href: string;
};

export function DashboardPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [projects, setProjects] = useState<Project[]>([]);
  const [projectsTotal, setProjectsTotal] = useState(0);
  const [activeProjectsTotal, setActiveProjectsTotal] = useState(0);
  const [atRiskTotal, setAtRiskTotal] = useState(0);
  const [approvals, setApprovals] = useState<ApprovalRequest[]>([]);
  const [approvalsTotal, setApprovalsTotal] = useState(0);
  const [followUps, setFollowUps] = useState<FollowUp[]>([]);
  const [followUpsTotal, setFollowUpsTotal] = useState(0);
  const [queries, setQueries] = useState<ClientQuery[]>([]);
  const [queriesTotal, setQueriesTotal] = useState(0);
  const [breachedQueriesTotal, setBreachedQueriesTotal] = useState(0);
  const [receivedQueriesTotal, setReceivedQueriesTotal] = useState(0);
  const [insightsSnap, setInsightsSnap] = useState<InsightsDashboardSnapshot | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [
        projectsResult,
        activeResult,
        atRiskResult,
        blockedResult,
        onHoldResult,
        approvalsResult,
        followUpsResult,
        queriesResult,
        breachedResult,
        receivedResult,
        insightsResult,
      ] = await Promise.allSettled([
        listProjects(session, { limit: 20 }),
        listProjects(session, { status: "active", limit: 1 }),
        listProjects(session, { status: "at_risk", limit: 1 }),
        listProjects(session, { status: "blocked", limit: 1 }),
        listProjects(session, { status: "on_hold", limit: 1 }),
        listApprovals(session, { status: "pending", limit: 20 }),
        listOpenFollowUps(session, { limit: 20 }),
        listQueries(session, { limit: 20 }),
        listQueries(session, { sla_status: "breached", limit: 1 }),
        listQueries(session, { status: "received", limit: 1 }),
        refreshInsightsDashboard(session),
      ]);

      if (projectsResult.status === "fulfilled") {
        setProjects(projectsResult.value.items);
        setProjectsTotal(projectsResult.value.page.total);
      } else {
        setProjects([]);
        setProjectsTotal(0);
        notifyApiError("Unable to load projects", projectsResult.reason);
      }

      setActiveProjectsTotal(
        activeResult.status === "fulfilled" ? activeResult.value.page.total : 0,
      );
      const riskTotal =
        (atRiskResult.status === "fulfilled" ? atRiskResult.value.page.total : 0) +
        (blockedResult.status === "fulfilled" ? blockedResult.value.page.total : 0) +
        (onHoldResult.status === "fulfilled" ? onHoldResult.value.page.total : 0);
      setAtRiskTotal(riskTotal);

      if (approvalsResult.status === "fulfilled") {
        setApprovals(approvalsResult.value.items);
        setApprovalsTotal(approvalsResult.value.page.total);
      } else {
        setApprovals([]);
        setApprovalsTotal(0);
        notifyApiError("Unable to load approvals", approvalsResult.reason);
      }

      if (followUpsResult.status === "fulfilled") {
        setFollowUps(followUpsResult.value.items);
        setFollowUpsTotal(followUpsResult.value.page.total);
      } else {
        setFollowUps([]);
        setFollowUpsTotal(0);
        notifyApiError("Unable to load follow-ups", followUpsResult.reason);
      }

      if (queriesResult.status === "fulfilled") {
        setQueries(queriesResult.value.items);
        setQueriesTotal(queriesResult.value.page.total);
      } else {
        setQueries([]);
        setQueriesTotal(0);
        notifyApiError("Unable to load queries", queriesResult.reason);
      }

      setBreachedQueriesTotal(
        breachedResult.status === "fulfilled" ? breachedResult.value.page.total : 0,
      );
      setReceivedQueriesTotal(
        receivedResult.status === "fulfilled" ? receivedResult.value.page.total : 0,
      );

      if (insightsResult.status === "fulfilled") {
        setInsightsSnap(insightsResult.value);
      } else {
        setInsightsSnap(null);
      }
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    void load();
  }, [load]);

  const now = Date.now();

  const overdueFollowUps = useMemo(
    () => followUps.filter((f) => new Date(f.due_at).getTime() < now),
    [followUps, now],
  );
  const breachedQueries = useMemo(
    () => queries.filter((q) => q.sla_status === "breached"),
    [queries],
  );

  const kpis = [
    {
      label: "Projects",
      value: `${activeProjectsTotal} active`,
      hint:
        atRiskTotal > 0
          ? `${atRiskTotal} at risk / blocked`
          : `${projectsTotal} total in org`,
      href: "/projects",
    },
    {
      label: "Approvals",
      value: `${approvalsTotal} pending`,
      hint: approvalsTotal ? "Needs human decision" : "Queue clear",
      href: "/approvals",
    },
    {
      label: "Follow-ups",
      value: `${followUpsTotal} open`,
      hint:
        overdueFollowUps.length > 0
          ? `${overdueFollowUps.length} overdue (this page)`
          : "None overdue in loaded set",
      href: "/follow-ups",
    },
    {
      label: "Queries",
      value: `${queriesTotal} total`,
      hint:
        breachedQueriesTotal > 0
          ? `${breachedQueriesTotal} SLA breached`
          : `${receivedQueriesTotal} newly received`,
      href: "/queries",
    },
  ];

  const attention: AttentionItem[] = useMemo(() => {
    const items: AttentionItem[] = [];
    for (const a of approvals.slice(0, 3)) {
      items.push({
        title: a.title,
        meta: `Approval · ${a.action_code} · v${a.target_version}`,
        href: "/approvals",
      });
    }
    for (const f of overdueFollowUps.slice(0, 3)) {
      items.push({
        title: f.title,
        meta: `Follow-up overdue · due ${formatUtc(f.due_at)}`,
        href: "/follow-ups",
      });
    }
    for (const q of breachedQueries.slice(0, 2)) {
      items.push({
        title: q.subject,
        meta: `Inquiry SLA breached · ${q.status}`,
        href: "/queries",
      });
    }
    return items.slice(0, 6);
  }, [approvals, overdueFollowUps, breachedQueries]);

  const recent = useMemo(() => {
    const rows: { label: string; at: string; href: string }[] = [];
    for (const p of projects.slice(0, 3)) {
      rows.push({
        label: `Project ${p.code} — ${p.title}`,
        at: p.created_at,
        href: "/projects",
      });
    }
    for (const q of queries.slice(0, 3)) {
      rows.push({
        label: `Inquiry — ${q.subject}`,
        at: q.created_at,
        href: "/queries",
      });
    }
    for (const a of approvals.slice(0, 2)) {
      rows.push({
        label: `Pending approval — ${a.title}`,
        at: a.created_at,
        href: "/approvals",
      });
    }
    return rows
      .sort((x, y) => new Date(y.at).getTime() - new Date(x.at).getTime())
      .slice(0, 6);
  }, [projects, queries, approvals]);

  const hour = new Date().getHours();
  const greeting =
    hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";

  return (
    <AppShell title="Dashboard" breadcrumbs={["Workspace", "Dashboard"]}>
      <PageHeader
        title={`${greeting}`}
        description="Live counts from Projects, Approvals, Follow-ups, and Queries for this organization. Insights snapshot shown when available."
        actions={
          <>
            <Button variant="outline" onClick={() => void load()}>
              Refresh
            </Button>
            <Link href="/insights">
              <Button variant="outline">Insights</Button>
            </Link>
            <Link href="/queries">
              <Button variant="outline">Open Queries</Button>
            </Link>
            <Link href="/projects">
              <Button>
                View Projects
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
          </>
        }
      />

      {insightsSnap ? (
        <Card className="mb-4">
          <CardBody className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="text-xs font-medium uppercase tracking-wide text-[var(--muted)]">
                Insights snapshot
              </p>
              <p className="mt-1 text-sm">
                projects_total={String(insightsSnap.metrics.projects_total ?? "—")} · tickets_open=
                {String(insightsSnap.metrics.tickets_open ?? "—")} · bugs_open=
                {String(insightsSnap.metrics.bugs_open ?? "—")} · followups_open=
                {String(insightsSnap.metrics.followups_open ?? "—")}
              </p>
              <p className="mt-1 text-xs text-[var(--muted)]">
                refreshed {formatUtc(insightsSnap.refreshed_at)} ·{" "}
                {insightsSnap.is_fresh ? "fresh" : "stale"}
              </p>
            </div>
            <StatusBadge status={insightsSnap.is_fresh ? "fresh" : "stale"} />
          </CardBody>
        </Card>
      ) : null}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {loading
          ? Array.from({ length: 4 }).map((_, i) => (
              <Card key={i}>
                <CardBody>
                  <SkeletonRows rows={2} />
                </CardBody>
              </Card>
            ))
          : kpis.map((card) => (
              <Link key={card.label} href={card.href}>
                <Card className="transition hover:border-[var(--accent)]">
                  <CardBody>
                    <p className="text-xs font-medium uppercase tracking-wide text-[var(--muted)]">
                      {card.label}
                    </p>
                    <p className="mt-2 font-display text-2xl tracking-tight">{card.value}</p>
                    <p className="mt-1 text-sm text-[var(--muted)]">{card.hint}</p>
                  </CardBody>
                </Card>
              </Link>
            ))}
      </div>

      <div className="mt-6 grid gap-4 xl:grid-cols-3">
        <Card className="xl:col-span-2">
          <CardHeader className="flex items-center justify-between">
            <h2 className="font-display text-lg">Projects</h2>
            <Link href="/projects" className="text-sm text-[var(--accent)] hover:underline">
              Open projects
            </Link>
          </CardHeader>
          {loading ? (
            <SkeletonRows />
          ) : projects.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No projects yet"
                body="Create a project to start tracking delivery health here."
                action={
                  <Link href="/projects">
                    <Button>Go to Projects</Button>
                  </Link>
                }
              />
            </CardBody>
          ) : (
            <CardBody className="space-y-4">
              {projects.slice(0, 8).map((project) => (
                <div key={project.id} className="flex items-center justify-between gap-3">
                  <div>
                    <p className="font-medium">
                      {project.code} · {project.title}
                    </p>
                    <p className="text-xs text-[var(--muted)]">
                      Created {formatUtc(project.created_at)}
                    </p>
                  </div>
                  <StatusBadge status={project.status} />
                </div>
              ))}
            </CardBody>
          )}
        </Card>

        <Card>
          <CardHeader className="flex items-center justify-between">
            <h2 className="font-display text-lg">Needs attention</h2>
            <Link href="/approvals" className="text-sm text-[var(--accent)] hover:underline">
              Approvals
            </Link>
          </CardHeader>
          {loading ? (
            <SkeletonRows />
          ) : attention.length === 0 ? (
            <CardBody>
              <EmptyState
                title="Nothing urgent"
                body="No pending approvals, overdue follow-ups, or breached inquiry SLAs."
              />
            </CardBody>
          ) : (
            <CardBody className="space-y-3">
              {attention.map((item) => (
                <Link
                  key={`${item.href}-${item.title}-${item.meta}`}
                  href={item.href}
                  className="block rounded-[var(--radius-md)] border border-[var(--line)] bg-[var(--surface-muted)] p-3 transition hover:border-[var(--accent)]"
                >
                  <div className="flex items-start gap-2">
                    <AlertTriangle className="mt-0.5 h-4 w-4 text-[var(--warning)]" />
                    <div>
                      <p className="text-sm font-medium">{item.title}</p>
                      <p className="mt-0.5 text-xs text-[var(--muted)]">{item.meta}</p>
                    </div>
                  </div>
                </Link>
              ))}
            </CardBody>
          )}
        </Card>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <h2 className="font-display text-lg">Recent movement</h2>
          </CardHeader>
          {loading ? (
            <SkeletonRows />
          ) : recent.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No recent records"
                body="Create inquiries or projects to populate this feed."
              />
            </CardBody>
          ) : (
            <CardBody className="space-y-3">
              {recent.map((line) => (
                <Link
                  key={`${line.href}-${line.label}-${line.at}`}
                  href={line.href}
                  className="flex items-start gap-2 text-sm hover:text-[var(--accent)]"
                >
                  <CheckCircle2 className="mt-0.5 h-4 w-4 text-[var(--success)]" />
                  <span>
                    {line.label}
                    <span className="mt-0.5 block text-xs text-[var(--muted)]">
                      {formatUtc(line.at)}
                    </span>
                  </span>
                </Link>
              ))}
            </CardBody>
          )}
        </Card>
        <Card>
          <CardHeader>
            <h2 className="font-display text-lg">Quick start</h2>
          </CardHeader>
          <CardBody className="grid gap-2 sm:grid-cols-2">
            {[
              { href: "/clients", label: "Clients" },
              { href: "/queries", label: "Queries" },
              { href: "/follow-ups", label: "Follow-ups" },
              { href: "/approvals", label: "Approvals" },
            ].map((item) => (
              <Link key={item.href} href={item.href}>
                <Button variant="outline" className="w-full justify-between">
                  {item.label}
                  <Clock3 className="h-4 w-4 text-[var(--muted)]" />
                </Button>
              </Link>
            ))}
          </CardBody>
        </Card>
      </div>
    </AppShell>
  );
}
