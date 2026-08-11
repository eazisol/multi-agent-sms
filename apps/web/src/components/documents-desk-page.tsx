"use client";

import { FormEvent, useEffect, useState } from "react";
import { FileUp, Plus, ShieldCheck } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Select } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, StatusBanner } from "@/components/ui-states";
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

function storageKeyFor(filename: string) {
  const safe = filename.trim().replace(/[^a-zA-Z0-9._-]+/g, "-") || "file.bin";
  return `uploads/${Date.now().toString(36)}/${safe}`;
}

export function DocumentsDeskPage() {
  const { session } = useSession();
  const [error, setError] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [showVersion, setShowVersion] = useState(false);
  const [title, setTitle] = useState("");
  const [documentId, setDocumentId] = useState("");
  const [documentTitle, setDocumentTitle] = useState("");
  const [filename, setFilename] = useState("");
  const [version, setVersion] = useState<DocumentVersion | null>(null);
  const [verdict, setVerdict] = useState("clean");
  const workspaceProject = getWorkspaceProjectId();

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
      setDocumentTitle(doc.title);
      setWorkspaceDocumentId(doc.id);
      setOk(`“${doc.title}” added`);
      setTitle("");
      setShowCreate(false);
      setShowVersion(true);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not create document");
    }
  }

  async function onCreateVersion(event: FormEvent) {
    event.preventDefault();
    if (!documentId) return;
    setError(null);
    setOk(null);
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
      setOk(`Version ${created.version_number} uploaded — ready for security scan`);
      setFilename("");
      setShowVersion(false);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not add version");
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
        detail: verdict === "clean" ? "Scan completed clean" : "Scan flagged content",
      });
      setOk(`Scan result: ${scan.verdict}`);
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
        available.indexing_allowed
          ? "Document available for the team and knowledge indexing"
          : "Document marked available",
      );
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not mark available");
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

      {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
      {ok ? <StatusBanner kind="success">{ok}</StatusBanner> : null}

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

      {!documentId && !showCreate ? (
        <EmptyState
          title="No document open"
          body="Create a document to upload versions, run scans, and release files to the delivery team."
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

      {documentId ? (
        <div className="grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
          <Card>
            <CardHeader className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <h2 className="font-display text-xl">{documentTitle || "Current document"}</h2>
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
                    <Field label="File name" hint="The file is registered for this document; scan before release.">
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
      ) : null}
    </AppShell>
  );
}
