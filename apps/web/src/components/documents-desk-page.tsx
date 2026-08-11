"use client";

import { FormEvent, useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { StatusBanner } from "@/components/ui-states";
import {
  ApiError,
  createDocument,
  createDocumentVersion,
  markDocumentAvailable,
  recordDocumentScan,
  type DocumentVersion,
} from "@/lib/api";
import { can } from "@/lib/roles";
import {
  getWorkspaceDocumentId,
  getWorkspaceProjectId,
  setWorkspaceDocumentId,
} from "@/lib/workspace";

export function DocumentsDeskPage() {
  const { session } = useSession();
  const [error, setError] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const [title, setTitle] = useState("");
  const [documentId, setDocumentId] = useState("");
  const [filename, setFilename] = useState("spec.pdf");
  const [storageKey, setStorageKey] = useState("s3://bucket/org/spec.pdf");
  const [version, setVersion] = useState<DocumentVersion | null>(null);
  const [verdict, setVerdict] = useState("clean");

  useEffect(() => {
    setDocumentId(getWorkspaceDocumentId());
  }, []);

  async function onCreateDocument(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setOk(null);
    try {
      const projectId = getWorkspaceProjectId() || undefined;
      const doc = await createDocument(session, {
        title: title.trim(),
        classification: "internal",
        project_id: projectId,
      });
      setDocumentId(doc.id);
      setWorkspaceDocumentId(doc.id);
      setOk(`Document created (${doc.id})`);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Create failed");
    }
  }

  async function onCreateVersion(event: FormEvent) {
    event.preventDefault();
    if (!documentId) return;
    setError(null);
    setOk(null);
    try {
      const created = await createDocumentVersion(session, {
        document_id: documentId,
        storage_key: storageKey.trim(),
        filename: filename.trim(),
        content_type: "application/pdf",
        size_bytes: 1024,
      });
      setVersion(created);
      setOk(`Version ${created.version_number} created (status ${created.status})`);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Version create failed");
    }
  }

  async function onScan() {
    if (!version) return;
    setError(null);
    setOk(null);
    try {
      const scan = await recordDocumentScan(session, {
        document_version_id: version.id,
        verdict,
        detail: verdict === "clean" ? "stub clean" : "stub unsafe",
      });
      setOk(`Scan recorded: ${scan.verdict}`);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Scan failed");
    }
  }

  async function onAvailable() {
    if (!version) return;
    setError(null);
    setOk(null);
    try {
      const available = await markDocumentAvailable(session, version.id, {
        effective_at: new Date().toISOString(),
      });
      setVersion(available);
      setOk(
        `Version available · indexing_allowed=${String(available.indexing_allowed)}`,
      );
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Mark available failed");
    }
  }

  return (
    <AppShell title="Documents">
      <div className="space-y-6">
        <div>
          <h2 className="font-display text-3xl tracking-tight">Documents desk</h2>
          <p className="mt-1 text-sm text-[var(--muted)]">
            MOD-250 metadata + scan gate. Object bytes stay in storage via storage_key.
          </p>
        </div>
        {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
        {ok ? <StatusBanner kind="success">{ok}</StatusBanner> : null}

        {can(session.variant, "create") ? (
          <>
            <form
              onSubmit={onCreateDocument}
              className="grid gap-3 rounded border border-[var(--line)] bg-white p-4 md:grid-cols-2"
            >
              <label className="flex flex-col gap-1 text-sm md:col-span-2">
                <span>Document title</span>
                <input
                  required
                  className="rounded border border-[var(--line)] px-3 py-2"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                />
              </label>
              <button
                type="submit"
                className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white md:w-fit"
              >
                Create document
              </button>
            </form>

            <label className="flex flex-col gap-1 text-sm">
              <span>Active document id</span>
              <input
                className="rounded border border-[var(--line)] bg-white px-3 py-2 font-mono text-xs"
                value={documentId}
                onChange={(e) => {
                  setDocumentId(e.target.value);
                  setWorkspaceDocumentId(e.target.value);
                }}
              />
            </label>

            <form
              onSubmit={onCreateVersion}
              className="grid gap-3 rounded border border-[var(--line)] bg-white p-4 md:grid-cols-2"
            >
              <label className="flex flex-col gap-1 text-sm">
                <span>Filename</span>
                <input
                  required
                  className="rounded border border-[var(--line)] px-3 py-2"
                  value={filename}
                  onChange={(e) => setFilename(e.target.value)}
                />
              </label>
              <label className="flex flex-col gap-1 text-sm">
                <span>Storage key</span>
                <input
                  required
                  className="rounded border border-[var(--line)] px-3 py-2"
                  value={storageKey}
                  onChange={(e) => setStorageKey(e.target.value)}
                />
              </label>
              <button
                type="submit"
                className="rounded border border-[var(--line)] bg-[var(--panel)] px-4 py-2 text-sm md:w-fit"
                disabled={!documentId}
              >
                Add version
              </button>
            </form>
          </>
        ) : (
          <StatusBanner kind="error">This UI role cannot create documents.</StatusBanner>
        )}

        {version ? (
          <section className="space-y-3 rounded border border-[var(--line)] bg-white p-4 text-sm">
            <p>
              Version {version.version_number} · status <strong>{version.status}</strong>
            </p>
            <label className="flex max-w-xs flex-col gap-1">
              <span>Scan verdict</span>
              <select
                className="rounded border border-[var(--line)] px-3 py-2"
                value={verdict}
                onChange={(e) => setVerdict(e.target.value)}
              >
                <option value="clean">clean</option>
                <option value="infected">infected</option>
                <option value="suspicious">suspicious</option>
              </select>
            </label>
            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                className="rounded border border-[var(--line)] px-3 py-1.5"
                onClick={() => void onScan()}
              >
                Record scan
              </button>
              <button
                type="button"
                className="rounded border border-[var(--line)] px-3 py-1.5"
                onClick={() => void onAvailable()}
                disabled={!can(session.variant, "approve")}
              >
                Mark available
              </button>
            </div>
          </section>
        ) : null}
      </div>
    </AppShell>
  );
}
