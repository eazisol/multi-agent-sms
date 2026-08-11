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
import { EmptyState, PageHeader, SkeletonRows, StatusBanner } from "@/components/ui-states";
import {
  ApiError,
  formatUtc,
  listApprovals,
  listOpenFollowUps,
  listProjects,
  listQueries,
  type ApprovalRequest,
  type FollowUp,
  type Project,
  type ClientQuery,
} from "@/lib/api";

type AttentionItem = {
  title: string;
  meta: string;
  href: string;
};

export function DashboardPage() {
  const { session } = useSession();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [projects, setProjects] = useState<Project[]>([]);
  const [approvals, setApprovals] = useState<ApprovalRequest[]>([]);
  const [followUps, setFollowUps] = useState<FollowUp[]>([]);
  const [queries, setQueries] = useState<ClientQuery[]>([]);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [projectRows, approvalRows, followUpRows, queryRows] = await Promise.all([
        listProjects(session, { limit: 100 }),
        listApprovals(session, { status: "pending" }),
        listOpenFollowUps(session),
        listQueries(session, { limit: 100 }),
      ]);
      setProjects(projectRows);
      setApprovals(approvalRows);
      setFollowUps(followUpRows);
      setQueries(queryRows);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Unable to load dashboard");
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    void load();
  }, [load]);

  const now = Date.now();

  const activeProjects = useMemo(
    () => projects.filter((p) => p.status === "active"),
    [projects],
  );
  const atRiskProjects = useMemo(
    () => projects.filter((p) => ["at_risk", "blocked", "on_hold"].includes(p.status)),
    [projects],
  );
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
      value: `${activeProjects.length} active`,
      hint:
        atRiskProjects.length > 0
          ? `${atRiskProjects.length} at risk / blocked`
          : `${projects.length} total in org`,
      href: "/projects",
    },
    {
      label: "Approvals",
      value: `${approvals.length} pending`,
      hint: approvals.length ? "Needs human decision" : "Queue clear",
      href: "/approvals",
    },
    {
      label: "Follow-ups",
      value: `${followUps.length} open`,
      hint:
        overdueFollowUps.length > 0
          ? `${overdueFollowUps.length} overdue`
          : "None overdue",
      href: "/follow-ups",
    },
    {
      label: "Queries",
      value: `${queries.length} total`,
      hint:
        breachedQueries.length > 0
          ? `${breachedQueries.length} SLA breached`
          : `${queries.filter((q) => q.status === "received").length} newly received`,
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
        description="Live counts from Projects, Approvals, Follow-ups, and Queries for this organization."
        actions={
          <>
            <Button variant="outline" onClick={() => void load()}>
              Refresh
            </Button>
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

      {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}

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
