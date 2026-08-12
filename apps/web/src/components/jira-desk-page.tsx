"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { RefreshCw } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { ScrollRegion } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader } from "@/components/ui-states";
import {
  createJiraCommentSync,
  formatUtc,
  listJiraCommentSyncs,
  listJiraIssuePushes,
  pushJiraIssue,
  retryJiraCommentSync,
  sendJiraStatusWebhook,
  type JiraCommentSync,
  type JiraIssuePush,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";

export function JiraDeskPage() {
  const { session } = useSession();
  const [issues, setIssues] = useState<JiraIssuePush[]>([]);
  const [commentSyncs, setCommentSyncs] = useState<JiraCommentSync[]>([]);
  const [loading, setLoading] = useState(true);

  const [summary, setSummary] = useState("Implement feature flow");
  const [simulatedKey, setSimulatedKey] = useState("SIM-520");
  const [externalStatus, setExternalStatus] = useState("Done");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [issuePage, syncPage] = await Promise.all([
        listJiraIssuePushes(session),
        listJiraCommentSyncs(session),
      ]);
      setIssues(issuePage.items);
      setCommentSyncs(syncPage.items);
    } catch (err) {
      notifyApiError("Unable to load Jira desk", err);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onPushApprovedIssue(event: FormEvent) {
    event.preventDefault();
    try {
      await pushJiraIssue(session, {
        internal_ticket_id: crypto.randomUUID(),
        summary: summary.trim(),
        approval_status: "approved",
        simulated_jira_key: simulatedKey.trim(),
      });
      notifySuccess("Approved issue pushed to Jira");
      setSummary("Implement additional requirement");
      await load();
    } catch (err) {
      notifyApiError("Jira push failed", err);
    }
  }

  async function onCreateConflict(event: FormEvent) {
    event.preventDefault();
    const issue = issues[0];
    if (!issue) return;
    try {
      await sendJiraStatusWebhook(session, {
        issue_push_id: issue.id,
        external_status: externalStatus.trim(),
        attempted_internal_status: "closed",
      });
      notifySuccess("Conflict registered");
      await load();
    } catch (err) {
      notifyApiError("Webhook conflict call failed", err);
      await load();
    }
  }

  async function onSyncFailThenRetry(event: FormEvent) {
    event.preventDefault();
    const issue = issues[0];
    if (!issue) return;
    try {
      const failed = await createJiraCommentSync(session, {
        issue_push_id: issue.id,
        comment_text: "Please update estimate.",
        force_fail: true,
      });
      await retryJiraCommentSync(session, failed.id);
      notifySuccess("Comment sync retried successfully");
      await load();
    } catch (err) {
      notifyApiError("Comment sync flow failed", err);
    }
  }

  return (
    <AppShell>
      <PageHeader
        title="Jira"
        description="Approval-gated Jira push, protected status webhooks, and retriable comment sync (M1 simulated)."
        actions={
          <Button variant="secondary" onClick={() => void load()}>
            <RefreshCw className="h-4 w-4" />
            Refresh
          </Button>
        }
      />
      <ScrollRegion className="space-y-6 p-6">
        <div className="grid gap-6 lg:grid-cols-3">
          <Card>
            <CardHeader title="Approved issue push" />
            <CardBody>
              <form onSubmit={onPushApprovedIssue} className="grid gap-3">
                <Field label="Summary">
                  <Input value={summary} onChange={(e) => setSummary(e.target.value)} required />
                </Field>
                <Field label="Simulated Jira key">
                  <Input
                    value={simulatedKey}
                    onChange={(e) => setSimulatedKey(e.target.value)}
                    required
                  />
                </Field>
                <Button type="submit">Push approved issue</Button>
              </form>
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Inbound status webhook" />
            <CardBody>
              <form onSubmit={onCreateConflict} className="grid gap-3">
                <Field label="External status">
                  <Input
                    value={externalStatus}
                    onChange={(e) => setExternalStatus(e.target.value)}
                    required
                  />
                </Field>
                <Button type="submit" disabled={issues.length === 0}>
                  Create conflict
                </Button>
              </form>
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Comment sync retry" />
            <CardBody>
              <form onSubmit={onSyncFailThenRetry} className="grid gap-3">
                <Button type="submit" disabled={issues.length === 0}>
                  Fail sync then retry
                </Button>
              </form>
            </CardBody>
          </Card>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader title="Pushed issues" />
            <CardBody>
              {!loading && issues.length === 0 ? (
                <EmptyState title="No pushed issues" body="Push an approved issue to populate this list." />
              ) : (
                <ul className="space-y-2 text-sm">
                  {issues.map((issue) => (
                    <li key={issue.id} className="rounded border p-2">
                      <div className="flex items-center justify-between gap-2">
                        <span className="font-medium">{issue.jira_issue_key}</span>
                        <StatusBadge status={issue.push_status} />
                      </div>
                      <div className="text-muted-foreground">
                        {issue.summary} - {formatUtc(issue.created_at)}
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Comment sync attempts" />
            <CardBody>
              {!loading && commentSyncs.length === 0 ? (
                <EmptyState title="No comment sync records" body="Run sync flow to create records." />
              ) : (
                <ul className="space-y-2 text-sm">
                  {commentSyncs.map((sync) => (
                    <li key={sync.id} className="rounded border p-2">
                      <div className="flex items-center justify-between gap-2">
                        <span className="font-medium">Retries: {sync.retry_count}</span>
                        <StatusBadge status={sync.sync_status} />
                      </div>
                      <div className="text-muted-foreground">
                        {sync.comment_text} - {formatUtc(sync.updated_at)}
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </CardBody>
          </Card>
        </div>
      </ScrollRegion>
    </AppShell>
  );
}
