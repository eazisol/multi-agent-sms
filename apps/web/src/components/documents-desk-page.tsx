"use client";

import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import { FileUp, Plus, Search, ShieldCheck } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Select } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows, StatusBanner } from "@/components/ui-states";
import {
  createDocument,
  createDocumentVersion,
  formatUtc,
  listDocuments,
  markDocumentAvailable,
  recordDocumentScan,
  type DocumentRecord,
  type DocumentVersion,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";
import { can } from "@/lib/roles";
import {
  getWorkspaceDocumentId,
  getWorkspaceProjectId,
  setWorkspaceDocumentId,
} from "@/lib/workspace";

function storageKeyFor(filename: string) {
  const safe = filename.trim().replace(/[^a-zA-Z0-9._-]+/g, "-") || "file.bin";
  return `uploads/${Date.now().toString(36)}/${safe}`;
}

export function DocumentsDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [showVersion, setShowVersion] = useState(false);
  const [title, setTitle] = useState("");
  const [documents, setDocuments] = useState<DocumentRecord[]>([]);
  const [documentId, setDocumentId] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [filename, setFilename] = useState("");
  const [version, setVersion] = useState<DocumentVersion | null>(null);
  const [verdict, setVerdict] = useState("clean");
  const workspaceProject = getWorkspaceProjectId();

  const loadDocuments = useCallback(async () => {
    setLoading(true);
    try {
      const rows = await listDocuments(session, {
        q: search.trim() || undefined,
        limit: 100,
      });
      setDocuments(rows);
      const workspaceId = getWorkspaceDocumentId();
      setDocumentId((prev) => {
        if (prev && rows.some((r) => r.id === prev)) return prev;
        if (workspaceId && rows.some((r) => r.id === workspaceId)) return workspaceId;
        return rows[0]?.id ?? null;
      });
    } catch (err) {
      notifyApiError("Unable to load documents", err);
      setDocuments([]);
    } finally {
      setLoading(false);
    }
  }, [session, search]);

  useEffect(() => {
    void loadDocuments();
  }, [loadDocuments]);

  const current = useMemo(
    () => documents.find((item) => item.id === documentId) ?? null,
    [documents, documentId],
  );

  function selectDocument(id: string) {
    setDocumentId(id);
    setWorkspaceDocumentId(id);
    setVersion(null);
  }

  async function onCreateDocument(event: FormEvent) {
    event.preventDefault();
    try {
      const projectId = getWorkspaceProjectId() || undefined;
      const doc = await createDocument(session, {
        title: title.trim(),
        classification: "internal",
        project_id: projectId,
      });
      setWorkspaceDocumentId(doc.id);
      setDocumentId(doc.id);
      notifySuccess(`“${doc.title}” added`);
      setTitle("");
      setShowCreate(false);
      setShowVersion(true);
      await loadDocuments();
    } catch (err) {
      notifyApiError("Could not create document", err);
    }
  }

  async function onCreateVersion(event: FormEvent) {
    event.preventDefault();
    if (!documentId) return;
    try {
      const name = filename.trim() || "document.pdf";
      const created = await createDocumentVersion(session, {
        document_id: documentId,
        storage_key: storageKeyFor(name),
        filename: name,
        content_type: "application/pdf",
        size_bytes: 1024,
      });
      setVersion(created);
      notifySuccess(`Version ${created.version_number} uploaded — ready for security scan`);
      setFilename("");
      setShowVersion(false);
    } catch (err) {
      notifyApiError("Could not add version", err);
    }
  }

  async function onScan() {
    if (!version) return;
    try {
      const scan = await recordDocumentScan(session, {
        document_version_id: version.id,
        verdict,
        detail: verdict === "clean" ? "Scan completed clean" : "Scan flagged content",
      });
      notifySuccess(`Scan result: ${scan.verdict}`);
    } catch (err) {
      notifyApiError("Scan failed", err);
    }
  }

  async function onAvailable() {
    if (!version) return;
    try {
      const available = await markDocumentAvailable(session, version.id, {
        effective_at: new Date().toISOString(),
      });
      setVersion(available);
      notifySuccess(
        available.indexing_allowed
          ? "Document available for the team and knowledge indexing"
          : "Document marked available",
      );
    } catch (err) {
      notifyApiError("Could not mark available", err);
    }
  }

  return (
    <AppShell title="Documents" breadcrumbs={["Project Delivery", "Documents"]}>
      <PageHeader
        title="Documents"
        description="Controlled project files — upload a version, run a security scan, then release it to the team."
        actions={
          can(session.variant, "create") ? (
            <Button onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              New document
            </Button>
          ) : null
        }
      />

      {workspaceProject ? (
        <p className="mb-4 text-sm text-[var(--muted)]">
          New documents attach to the workspace project from Projects.
        </p>
      ) : (
        <StatusBanner kind="info">
          Tip: create or select a workspace project on Projects so documents stay linked to delivery.
        </StatusBanner>
      )}

      {showCreate && can(session.variant, "create") ? (
        <Card className="mb-6">
          <CardHeader>
            <h2 className="font-display text-lg">Create document</h2>
            <p className="text-sm text-[var(--muted)]">
              Register the document metadata first, then add a file version.
            </p>
          </CardHeader>
          <CardBody>
            <form onSubmit={onCreateDocument} className="grid gap-4" aria-label="Create document">
              <Field label="Title">
                <Input
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Solution architecture overview"
                />
              </Field>
              <div className="flex justify-end gap-2">
                <Button type="button" variant="ghost" onClick={() => setShowCreate(false)}>
                  Cancel
                </Button>
                <Button type="submit">Create document</Button>
              </div>
            </form>
          </CardBody>
        </Card>
      ) : null}

      <div className="grid gap-4 lg:grid-cols-[minmax(280px,340px)_1fr]">
        <Card>
          <CardHeader>
            <h2 className="font-display text-lg">Document library</h2>
            <p className="text-sm text-[var(--muted)]">Loaded from the organization database.</p>
            <div className="relative mt-3">
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--muted)]" />
              <Input
                className="pl-9"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search title"
                aria-label="Search documents"
              />
            </div>
          </CardHeader>
          {loading ? (
            <SkeletonRows />
          ) : documents.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No documents yet"
                body="Create a document to upload versions, run scans, and release files."
                action={
                  can(session.variant, "create") ? (
                    <Button onClick={() => setShowCreate(true)}>
                      <Plus className="h-4 w-4" />
                      New document
                    </Button>
                  ) : null
                }
              />
            </CardBody>
          ) : (
            <ul className="divide-y divide-[var(--line)]">
              {documents.map((item) => (
                <li key={item.id}>
                  <button
                    type="button"
                    onClick={() => selectDocument(item.id)}
                    className={`w-full px-5 py-3 text-left transition hover:bg-[var(--surface-muted)]/70 ${
                      item.id === documentId ? "bg-[var(--accent-soft)]" : ""
                    }`}
                  >
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <span className="font-medium">{item.title}</span>
                      <StatusBadge status={item.status} />
                    </div>
                    <div className="mt-1 flex flex-wrap gap-2">
                      <StatusBadge status={item.classification} />
                    </div>
                    {item.created_at ? (
                      <p className="mt-1 text-xs text-[var(--muted)]">{formatUtc(item.created_at)}</p>
                    ) : null}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </Card>

        {documentId && current ? (
          <div className="grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
            <Card>
              <CardHeader className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h2 className="font-display text-xl">{current.title}</h2>
                  <p className="mt-1 text-sm text-[var(--muted)]">
                    Upload a file version, then complete the scan gate before sharing.
                  </p>
                </div>
                {version ? <StatusBadge status={version.status} /> : null}
              </CardHeader>
              <CardBody className="space-y-4">
                {can(session.variant, "create") ? (
                  showVersion ? (
                    <form
                      onSubmit={onCreateVersion}
                      className="grid gap-4"
                      aria-label="Add document version"
                    >
                      <Field
                        label="File name"
                        hint="The file is registered for this document; scan before release."
                      >
                        <Input
                          required
                          value={filename}
                          onChange={(e) => setFilename(e.target.value)}
                          placeholder="architecture.pdf"
                        />
                      </Field>
                      <div className="flex justify-end gap-2">
                        <Button type="button" variant="ghost" onClick={() => setShowVersion(false)}>
                          Cancel
                        </Button>
                        <Button type="submit">
                          <FileUp className="h-4 w-4" />
                          Add version
                        </Button>
                      </div>
                    </form>
                  ) : (
                    <Button variant="outline" onClick={() => setShowVersion(true)}>
                      <FileUp className="h-4 w-4" />
                      Add version
                    </Button>
                  )
                ) : (
                  <StatusBanner kind="warning">Your role cannot upload document versions.</StatusBanner>
                )}

                {version ? (
                  <div className="rounded-[var(--radius-sm)] border border-[var(--line)] bg-[var(--surface-muted)]/50 p-4 text-sm">
                    <p className="font-medium">
                      Version {version.version_number}
                      {version.filename ? ` · ${version.filename}` : ""}
                    </p>
                    <p className="mt-1 text-[var(--muted)]">
                      Complete a security scan, then mark the version available when clean.
                    </p>
                  </div>
                ) : null}
              </CardBody>
            </Card>

            <Card>
              <CardHeader>
                <h3 className="font-display text-lg">Scan &amp; release</h3>
              </CardHeader>
              <CardBody className="space-y-4">
                {!version ? (
                  <p className="text-sm text-[var(--muted)]">
                    Add a version to enable security scanning and release actions.
                  </p>
                ) : (
                  <>
                    <Field label="Scan result">
                      <Select value={verdict} onChange={(e) => setVerdict(e.target.value)}>
                        <option value="clean">Clean</option>
                        <option value="infected">Infected</option>
                        <option value="suspicious">Suspicious</option>
                      </Select>
                    </Field>
                    <div className="flex flex-wrap gap-2">
                      <Button variant="outline" onClick={() => void onScan()}>
                        <ShieldCheck className="h-4 w-4" />
                        Record scan
                      </Button>
                      <Button
                        disabled={!can(session.variant, "approve")}
                        onClick={() => void onAvailable()}
                      >
                        Mark available
                      </Button>
                    </div>
                  </>
                )}
              </CardBody>
            </Card>
          </div>
        ) : !loading ? (
          <EmptyState
            title="Select a document"
            body="Choose a file from the library or create a new document."
            action={
              can(session.variant, "create") ? (
                <Button onClick={() => setShowCreate(true)}>
                  <Plus className="h-4 w-4" />
                  New document
                </Button>
              ) : null
            }
          />
        ) : null}
      </div>
    </AppShell>
  );
}
