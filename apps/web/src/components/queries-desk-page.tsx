"use client";

import { FormEvent, useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { StatusBanner } from "@/components/ui-states";
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
  const [sourceCode, setSourceCode] = useState("web_form");
  const [sourceId, setSourceId] = useState("");
  const [subject, setSubject] = useState("");
  const [summary, setSummary] = useState("");
  const [queryId, setQueryId] = useState("");
  const [current, setCurrent] = useState<ClientQuery | null>(null);

  useEffect(() => {
    setQueryId(getWorkspaceQueryId());
  }, []);

  async function onCreateSource(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setOk(null);
    try {
      const source = await createQuerySource(session, {
        code: sourceCode.trim().toLowerCase(),
        title: `Source ${sourceCode}`,
        channel: "web",
      });
      setSourceId(source.id);
      setOk(`Source ready: ${source.code}`);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Source create failed");
    }
  }

  async function onCreateQuery(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setOk(null);
    try {
      const created = await createQuery(session, {
        subject: subject.trim(),
        summary: summary.trim(),
        source_id: sourceId || undefined,
      });
      setCurrent(created);
      setQueryId(created.id);
      setWorkspaceQueryId(created.id);
      setOk(`Query created in status ${created.status}`);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Query create failed");
    }
  }

  async function onTransition(next: string) {
    if (!queryId) return;
    setError(null);
    setOk(null);
    try {
      const updated = await transitionQuery(session, queryId, {
        next_status: next,
        classification: next === "classified" ? "new_build" : undefined,
      });
      setCurrent(updated);
      setOk(`Transitioned to ${updated.status}`);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Transition failed");
    }
  }

  return (
    <AppShell title="Queries">
      <div className="space-y-6">
        <div>
          <h2 className="font-display text-3xl tracking-tight">Query desk</h2>
          <p className="mt-1 text-sm text-[var(--muted)]">
            MOD-210 inquiry capture. List API is deferred — this desk tracks the active query id.
          </p>
        </div>
        {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
        {ok ? <StatusBanner kind="success">{ok}</StatusBanner> : null}

        {!can(session.variant, "create") ? (
          <StatusBanner kind="error">This UI role cannot create queries.</StatusBanner>
        ) : (
          <>
            <form
              onSubmit={onCreateSource}
              className="flex flex-wrap items-end gap-3 rounded border border-[var(--line)] bg-white p-4"
            >
              <label className="flex min-w-40 flex-col gap-1 text-sm">
                <span>Source code</span>
                <input
                  className="rounded border border-[var(--line)] px-3 py-2"
                  value={sourceCode}
                  onChange={(e) => setSourceCode(e.target.value)}
                  required
                />
              </label>
              <button
                type="submit"
                className="rounded border border-[var(--line)] bg-[var(--panel)] px-4 py-2 text-sm"
              >
                Ensure source
              </button>
              {sourceId ? (
                <p className="text-xs text-[var(--muted)]">source_id={sourceId}</p>
              ) : null}
            </form>

            <form
              onSubmit={onCreateQuery}
              className="grid gap-3 rounded border border-[var(--line)] bg-white p-4 md:grid-cols-2"
            >
              <label className="flex flex-col gap-1 text-sm md:col-span-2">
                <span>Subject</span>
                <input
                  required
                  className="rounded border border-[var(--line)] px-3 py-2"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                />
              </label>
              <label className="flex flex-col gap-1 text-sm md:col-span-2">
                <span>Summary</span>
                <textarea
                  required
                  className="min-h-24 rounded border border-[var(--line)] px-3 py-2"
                  value={summary}
                  onChange={(e) => setSummary(e.target.value)}
                />
              </label>
              <button
                type="submit"
                className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white md:w-fit"
              >
                Create query
              </button>
            </form>
          </>
        )}

        <section className="space-y-3 rounded border border-[var(--line)] bg-white p-4">
          <h3 className="font-medium">Active query</h3>
          <label className="flex flex-col gap-1 text-sm">
            <span>Query id</span>
            <input
              className="rounded border border-[var(--line)] px-3 py-2 font-mono text-xs"
              value={queryId}
              onChange={(e) => {
                setQueryId(e.target.value);
                setWorkspaceQueryId(e.target.value);
              }}
            />
          </label>
          {current ? (
            <p className="text-sm text-[var(--muted)]">
              Status <strong>{current.status}</strong> · SLA {current.sla_status}
            </p>
          ) : null}
          <div className="flex flex-wrap gap-2">
            {["classified", "qualifying", "qualified"].map((status) => (
              <button
                key={status}
                type="button"
                className="rounded border border-[var(--line)] px-3 py-1.5 text-sm"
                onClick={() => void onTransition(status)}
                disabled={!queryId || !can(session.variant, "edit_draft")}
              >
                → {status}
              </button>
            ))}
          </div>
        </section>
      </div>
    </AppShell>
  );
}
