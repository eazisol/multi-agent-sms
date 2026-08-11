"use client";

import Link from "next/link";
import {
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  Clock3,
  Sparkles,
} from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { PageHeader } from "@/components/ui-states";

const HEALTH = [
  { name: "EarthCo CRM", status: "Healthy", progress: 72 },
  { name: "Glaura Platform", status: "At Risk", progress: 54 },
  { name: "Portal Rebuild", status: "Healthy", progress: 87 },
];

const ATTENTION = [
  {
    title: "Development blocker overdue",
    meta: "EarthCo / DEV-134 · 1h 24m overdue",
  },
  {
    title: "Client approval pending",
    meta: "Glaura / SRS 1.3 · 2 days waiting",
  },
  {
    title: "Follow-up SLA at risk",
    meta: "Acme inquiry · due today 2:30 PM",
  },
];

const AGENTS = [
  "PM Agent generated Phase Plan",
  "QA Agent drafted 4 bug reports",
  "BD Agent analyzed a new inquiry",
];

export function DashboardPage() {
  const hour = new Date().getHours();
  const greeting =
    hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";

  return (
    <AppShell title="Dashboard" breadcrumbs={["Workspace", "Dashboard"]}>
      <PageHeader
        title={`${greeting}`}
        description="Here is what needs attention across delivery, approvals, and follow-ups."
        actions={
          <>
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

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {[
          { label: "Projects", value: "12 active", hint: "2 at risk · 1 delayed" },
          { label: "Approvals", value: "8 pending", hint: "3 urgent" },
          { label: "Follow-ups", value: "14 due today", hint: "4 overdue" },
          { label: "Quality", value: "94% pass", hint: "2 high issues" },
        ].map((card) => (
          <Card key={card.label}>
            <CardBody>
              <p className="text-xs font-medium uppercase tracking-wide text-[var(--muted)]">
                {card.label}
              </p>
              <p className="mt-2 font-display text-2xl tracking-tight">{card.value}</p>
              <p className="mt-1 text-sm text-[var(--muted)]">{card.hint}</p>
            </CardBody>
          </Card>
        ))}
      </div>

      <div className="mt-6 grid gap-4 xl:grid-cols-3">
        <Card className="xl:col-span-2">
          <CardHeader className="flex items-center justify-between">
            <h2 className="font-display text-lg">Project health</h2>
            <Link href="/projects" className="text-sm text-[var(--accent)] hover:underline">
              Open projects
            </Link>
          </CardHeader>
          <CardBody className="space-y-4">
            {HEALTH.map((project) => (
              <div key={project.name}>
                <div className="mb-1.5 flex items-center justify-between gap-3">
                  <p className="font-medium">{project.name}</p>
                  <StatusBadge
                    status={project.status === "Healthy" ? "active" : "at_risk"}
                  />
                </div>
                <div className="h-2 overflow-hidden rounded-full bg-[var(--surface-muted)]">
                  <div
                    className="h-full rounded-full bg-[var(--accent)]"
                    style={{ width: `${project.progress}%` }}
                  />
                </div>
                <p className="mt-1 text-xs text-[var(--muted)]">{project.progress}% complete</p>
              </div>
            ))}
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <h2 className="font-display text-lg">Needs attention</h2>
          </CardHeader>
          <CardBody className="space-y-3">
            {ATTENTION.map((item) => (
              <div
                key={item.title}
                className="rounded-[var(--radius-md)] border border-[var(--line)] bg-[var(--surface-muted)] p-3"
              >
                <div className="flex items-start gap-2">
                  <AlertTriangle className="mt-0.5 h-4 w-4 text-[var(--warning)]" />
                  <div>
                    <p className="text-sm font-medium">{item.title}</p>
                    <p className="mt-0.5 text-xs text-[var(--muted)]">{item.meta}</p>
                  </div>
                </div>
              </div>
            ))}
          </CardBody>
        </Card>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader className="flex items-center justify-between">
            <h2 className="font-display text-lg">Recent agent activity</h2>
            <Button variant="ai" size="sm">
              <Sparkles className="h-3.5 w-3.5" />
              Ask assistant
            </Button>
          </CardHeader>
          <CardBody className="space-y-3">
            {AGENTS.map((line) => (
              <div key={line} className="flex items-start gap-2 text-sm">
                <CheckCircle2 className="mt-0.5 h-4 w-4 text-[var(--success)]" />
                <span>{line}</span>
              </div>
            ))}
          </CardBody>
        </Card>
        <Card>
          <CardHeader>
            <h2 className="font-display text-lg">Quick start</h2>
          </CardHeader>
          <CardBody className="grid gap-2 sm:grid-cols-2">
            {[
              { href: "/clients", label: "Clients" },
              { href: "/queries", label: "Queries" },
              { href: "/tickets", label: "Tickets" },
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
