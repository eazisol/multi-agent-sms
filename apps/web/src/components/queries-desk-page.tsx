"use client";

import { FormEvent, useEffect, useState } from "react";
import { Plus } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Textarea } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, StatusBanner } from "@/components/ui-states";
import {
  ApiError,
  createQuery,
  createQuerySource,
  transitionQuery,
  type ClientQuery,
} from "@/lib/api";
import { can } from "@/lib/roles";
import { getWorkspaceQueryId, setWorkspaceQueryId } from "@/lib/workspace";

export function QueriesDeskPage() {
  const { session } = useSession();
  const [error, setError] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const [sourceId, setSourceId] = useState("");
  const [subject, setSubject] = useState("");
  const [summary, setSummary] = useState("");
  const [current, setCurrent] = useState<ClientQuery | null>(null);
  const [showCreate, setShowCreate] = useState(false);

  useEffect(() => {
    const id = getWorkspaceQueryId();
    if (id) {
      setCurrent((prev) => prev ?? ({ id, subject: "Active inquiry", summary: "", status: "new", sla_status: "ok", client_id: null, project_id: null, source_id: null, created_at: new Date().toISOString() }));
    }
  }, []);

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
    setError(null);
    setOk(null);
    try {
      const sid = await ensureSource();
      const created = await createQuery(session, {
        subject: subject.trim(),
        summary: summary.trim(),
        source_id: sid,
      });
      setCurrent(created);
      setWorkspaceQueryId(created.id);
      setOk("Inquiry captured");
      setSubject("");
      setSummary("");
      setShowCreate(false);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not create inquiry");
    }
  }

  async function onTransition(next: string) {
    if (!current) return;
    setError(null);
    setOk(null);
    try {
      const updated = await transitionQuery(session, current.id, {
        next_status: next,
        classification: next === "classified" ? "new_build" : undefined,
      });
      setCurrent(updated);
      setOk(`Moved to ${updated.status.replace(/_/g, " ")}`);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Transition failed");
    }
  }

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

      {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
      {ok ? <StatusBanner kind="success">{ok}</StatusBanner> : null}

      <div className="mb-4 flex flex-wrap gap-2">
        {["All", "New", "Waiting client", "Qualified", "Overdue"].map((tab, idx) => (
          <span
            key={tab}
            className={`rounded-full px-3 py-1 text-xs font-medium ${
              idx === 0
                ? "bg-[var(--accent-soft)] text-[var(--accent)]"
                : "bg-[var(--surface)] text-[var(--muted)] border border-[var(--line)]"
            }`}
          >
            {tab}
          </span>
        ))}
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

      {!current ? (
        <EmptyState
          title="No inquiry selected"
          body="New inbound requests appear here. Capture an inquiry to start qualification and requirement gathering."
          action={
            can(session.variant, "create") ? (
              <Button onClick={() => setShowCreate(true)}>New inquiry</Button>
            ) : null
          }
        />
      ) : (
        <div className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
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
                Move the inquiry through intake using the allowed actions for your role.
              </p>
              <div className="flex flex-wrap gap-2">
                {["classified", "qualified", "waiting_client"].map((next) => (
                  <Button
                    key={next}
                    variant="outline"
                    size="sm"
                    onClick={() => void onTransition(next)}
                  >
                    Mark {next.replace(/_/g, " ")}
                  </Button>
                ))}
              </div>
            </CardBody>
          </Card>
          <Card>
            <CardHeader>
              <h3 className="font-display text-lg">BD assistant</h3>
            </CardHeader>
            <CardBody className="space-y-3 text-sm">
              <p className="text-[var(--muted)]">
                Completeness and clarification prompts will appear here once requirement gathering
                is linked to this inquiry.
              </p>
              <Button variant="ai" size="sm">
                Generate clarifying questions
              </Button>
            </CardBody>
          </Card>
        </div>
      )}
    </AppShell>
  );
}
