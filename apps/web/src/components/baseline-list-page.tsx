"use client";

import Link from "next/link";
import { FormEvent, useCallback, useEffect, useState } from "react";

import { useSession } from "@/components/session-provider";
import { EmptyState, LoadingBlock, StatusBanner } from "@/components/ui-states";
import { ApiError, formatUtc, listBaselines, type Baseline } from "@/lib/api";
import { can } from "@/lib/roles";

export function BaselineListPage() {
  const { session } = useSession();
  const [items, setItems] = useState<Baseline[]>([]);
  const [total, setTotal] = useState(0);
  const [q, setQ] = useState("");
  const [status, setStatus] = useState("");
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const limit = 10;

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const page = await listBaselines(session, {
        limit,
        offset,
        q: q || undefined,
        status: status || undefined,
        sort: "baseline_key",
      });
      setItems(page.items);
      setTotal(page.page.total);
    } catch (err) {
      if (err instanceof ApiError && err.status === 403) {
        setError("Forbidden: you cannot list baselines with the current principal.");
      } else if (err instanceof ApiError) {
        setError(err.problem.message);
      } else {
        setError("Unable to reach the API. Is the FastAPI server running?");
      }
      setItems([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  }, [session, offset, q, status]);

  useEffect(() => {
    void load();
  }, [load]);

  function onFilter(event: FormEvent) {
    event.preventDefault();
    setOffset(0);
    void load();
  }

  if (!can(session.variant, "view_list")) {
    return (
      <StatusBanner kind="error">
        This UI role cannot view the baseline list.
      </StatusBanner>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h2 className="font-display text-3xl tracking-tight">Source baselines</h2>
          <p className="mt-1 text-sm text-[var(--muted)]">
            Approved sources of truth for MASMS. Server authorization is authoritative.
          </p>
        </div>
        {can(session.variant, "create") ? (
          <Link
            href="/governance/baselines/new"
            className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white hover:opacity-90"
          >
            New baseline
          </Link>
        ) : null}
      </div>

      <form
        onSubmit={onFilter}
        className="flex flex-wrap items-end gap-3 rounded border border-[var(--line)] bg-white p-4"
        aria-label="Filter baselines"
      >
        <label className="flex min-w-48 flex-1 flex-col gap-1 text-sm">
          <span>Search</span>
          <input
            className="rounded border border-[var(--line)] px-3 py-2"
            value={q}
            onChange={(event) => setQ(event.target.value)}
            placeholder="Key or title"
          />
        </label>
        <label className="flex min-w-40 flex-col gap-1 text-sm">
          <span>Status</span>
          <select
            className="rounded border border-[var(--line)] px-3 py-2"
            value={status}
            onChange={(event) => setStatus(event.target.value)}
          >
            <option value="">Any</option>
            <option value="draft">draft</option>
            <option value="submitted">submitted</option>
            <option value="under_review">under_review</option>
            <option value="approved">approved</option>
            <option value="rejected">rejected</option>
          </select>
        </label>
        <button
          type="submit"
          className="rounded border border-[var(--line)] bg-[var(--panel)] px-4 py-2 text-sm font-medium"
        >
          Apply
        </button>
      </form>

      {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
      {loading ? <LoadingBlock label="Loading baselines" /> : null}

      {!loading && !error && items.length === 0 ? (
        <EmptyState
          title="No baselines yet"
          body="Create the first source baseline when your role allows it."
          action={
            can(session.variant, "create") ? (
              <Link className="text-[var(--accent)] underline" href="/governance/baselines/new">
                Create baseline
              </Link>
            ) : undefined
          }
        />
      ) : null}

      {!loading && items.length > 0 ? (
        <div className="overflow-x-auto rounded border border-[var(--line)] bg-white">
          <table className="min-w-full text-left text-sm">
            <thead className="border-b border-[var(--line)] bg-[var(--panel)] text-[var(--muted)]">
              <tr>
                <th scope="col" className="px-4 py-3 font-medium">
                  Key
                </th>
                <th scope="col" className="px-4 py-3 font-medium">
                  Title
                </th>
                <th scope="col" className="px-4 py-3 font-medium">
                  Status
                </th>
                <th scope="col" className="px-4 py-3 font-medium">
                  Version
                </th>
                <th scope="col" className="px-4 py-3 font-medium">
                  Updated (UTC)
                </th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id} className="border-b border-[var(--line)] last:border-0">
                  <td className="px-4 py-3">
                    <Link
                      className="font-medium text-[var(--accent)] underline-offset-2 hover:underline"
                      href={`/governance/baselines/${item.id}`}
                    >
                      {item.baseline_key}
                    </Link>
                  </td>
                  <td className="px-4 py-3">{item.title}</td>
                  <td className="px-4 py-3">{item.approval_status}</td>
                  <td className="px-4 py-3">{item.version}</td>
                  <td className="px-4 py-3">{formatUtc(item.updated_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}

      <div className="flex items-center justify-between text-sm">
        <p className="text-[var(--muted)]">
          Showing {items.length} of {total}
        </p>
        <div className="flex gap-2">
          <button
            type="button"
            className="rounded border border-[var(--line)] px-3 py-1 disabled:opacity-40"
            disabled={offset === 0 || loading}
            onClick={() => setOffset((value) => Math.max(0, value - limit))}
          >
            Previous
          </button>
          <button
            type="button"
            className="rounded border border-[var(--line)] px-3 py-1 disabled:opacity-40"
            disabled={offset + limit >= total || loading}
            onClick={() => setOffset((value) => value + limit)}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}
