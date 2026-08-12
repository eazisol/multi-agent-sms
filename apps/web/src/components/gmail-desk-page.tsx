"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Plus, RefreshCw } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { ScrollRegion } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  activateGmailConnection,
  approveGmailDraft,
  createGmailConnection,
  createGmailDraft,
  formatUtc,
  listGmailConnections,
  listGmailMessages,
  listGmailThreads,
  processGmailInbound,
  receiveGmailPush,
  sendGmailDraft,
  submitGmailDraft,
  type GmailConnection,
  type GmailMessageMapping,
  type GmailThreadMapping,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";

export function GmailDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [connections, setConnections] = useState<GmailConnection[]>([]);
  const [threads, setThreads] = useState<GmailThreadMapping[]>([]);
  const [messages, setMessages] = useState<GmailMessageMapping[]>([]);

  const [code, setCode] = useState("gmail-main");
  const [email, setEmail] = useState("inbox@example.com");
  const [selectedConnId, setSelectedConnId] = useState("");

  const [gmailMessageId, setGmailMessageId] = useState("msg-sim-1");
  const [gmailThreadId, setGmailThreadId] = useState("thread-sim-1");
  const [fromEmail, setFromEmail] = useState("client@example.com");
  const [pushEventId, setPushEventId] = useState("push-sim-1");

  const [draftSubject, setDraftSubject] = useState("Re: Your inquiry");
  const [draftTo, setDraftTo] = useState("client@example.com");
  const [draftBody, setDraftBody] = useState("Thank you for your message.");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const listed = await listGmailConnections(session, { limit: 20 });
      setConnections(listed.items);
      const connId = selectedConnId || listed.items[0]?.id || "";
      if (!selectedConnId && connId) setSelectedConnId(connId);
      if (connId) {
        const [threadPage, messagePage] = await Promise.all([
          listGmailThreads(session, { connection_id: connId, limit: 10 }),
          listGmailMessages(session, { connection_id: connId, limit: 10 }),
        ]);
        setThreads(threadPage.items);
        setMessages(messagePage.items);
      } else {
        setThreads([]);
        setMessages([]);
      }
    } catch (err) {
      notifyApiError("Unable to load Gmail desk", err);
    } finally {
      setLoading(false);
    }
  }, [session, selectedConnId]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onCreateConnection(event: FormEvent) {
    event.preventDefault();
    try {
      const created = await createGmailConnection(session, {
        code: code.trim(),
        email_address: email.trim(),
      });
      if (created.status === "draft") {
        await activateGmailConnection(session, created.id);
      }
      notifySuccess(`Gmail connection ${created.code} created`);
      setCode(`gmail-${connections.length + 2}`);
      await load();
    } catch (err) {
      notifyApiError("Could not create Gmail connection", err);
    }
  }

  async function onSimulateInbound(event: FormEvent) {
    event.preventDefault();
    if (!selectedConnId) return;
    try {
      await processGmailInbound(session, {
        connection_id: selectedConnId,
        gmail_message_id: gmailMessageId.trim(),
        gmail_thread_id: gmailThreadId.trim(),
        from_email: fromEmail.trim(),
        subject: "Simulated inbound",
        snippet: "Inbound email simulation",
      });
      notifySuccess("Inbound email processed");
      setGmailMessageId(`msg-sim-${Date.now()}`);
      await load();
    } catch (err) {
      notifyApiError("Inbound process failed", err);
    }
  }

  async function onSimulatePush(event: FormEvent) {
    event.preventDefault();
    if (!selectedConnId) return;
    try {
      await receiveGmailPush(session, {
        connection_id: selectedConnId,
        external_event_id: pushEventId.trim(),
        event_type: "message_received",
        payload: {
          gmail_message_id: `push-msg-${Date.now()}`,
          gmail_thread_id: `push-thread-${Date.now()}`,
          from_email: fromEmail.trim(),
          subject: "Push notification",
        },
      });
      notifySuccess("Push notification received");
      setPushEventId(`push-sim-${Date.now()}`);
      await load();
    } catch (err) {
      notifyApiError("Push receive failed", err);
    }
  }

  async function onDraftSendFlow(event: FormEvent) {
    event.preventDefault();
    if (!selectedConnId) return;
    try {
      const draft = await createGmailDraft(session, {
        connection_id: selectedConnId,
        to_addresses: draftTo.trim(),
        subject: draftSubject.trim(),
        body_preview: draftBody.trim(),
      });
      await submitGmailDraft(session, draft.id);
      await approveGmailDraft(session, draft.id);
      const sent = await sendGmailDraft(session, draft.id);
      notifySuccess(`Sent via ${sent.approved_send.external_send_id}`);
      await load();
    } catch (err) {
      notifyApiError("Draft review/send failed", err);
    }
  }

  return (
    <AppShell>
      <PageHeader
        title="Gmail"
        description="Connect Gmail mailboxes, sync inbound messages, review drafts, and send approved replies (M1 simulated)."
        actions={
          <Button variant="secondary" onClick={() => void load()}>
            <RefreshCw className="h-4 w-4" />
            Refresh
          </Button>
        }
      />
      <ScrollRegion className="space-y-6 p-6">
        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader title="Connections" />
            <CardBody className="space-y-4">
              <form onSubmit={onCreateConnection} className="grid gap-3 sm:grid-cols-2">
                <Field label="Code">
                  <Input value={code} onChange={(e) => setCode(e.target.value)} required />
                </Field>
                <Field label="Email address">
                  <Input value={email} onChange={(e) => setEmail(e.target.value)} required />
                </Field>
                <div className="sm:col-span-2">
                  <Button type="submit">
                    <Plus className="h-4 w-4" />
                    Add connection
                  </Button>
                </div>
              </form>
              {loading ? (
                <SkeletonRows rows={3} />
              ) : connections.length === 0 ? (
                <EmptyState title="No Gmail connections" body="Create a connection to begin." />
              ) : (
                <ul className="divide-y rounded-md border">
                  {connections.map((conn) => (
                    <li
                      key={conn.id}
                      className={`flex cursor-pointer items-center justify-between gap-2 p-3 text-sm ${
                        selectedConnId === conn.id ? "bg-muted/50" : ""
                      }`}
                      onClick={() => setSelectedConnId(conn.id)}
                    >
                      <div>
                        <div className="font-medium">{conn.code}</div>
                        <div className="text-muted-foreground">{conn.email_address}</div>
                      </div>
                      <StatusBadge status={conn.status} />
                    </li>
                  ))}
                </ul>
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Simulate inbound" />
            <CardBody>
              <form onSubmit={onSimulateInbound} className="grid gap-3">
                <Field label="Gmail message ID">
                  <Input
                    value={gmailMessageId}
                    onChange={(e) => setGmailMessageId(e.target.value)}
                    required
                  />
                </Field>
                <Field label="Gmail thread ID">
                  <Input
                    value={gmailThreadId}
                    onChange={(e) => setGmailThreadId(e.target.value)}
                    required
                  />
                </Field>
                <Field label="From email">
                  <Input value={fromEmail} onChange={(e) => setFromEmail(e.target.value)} required />
                </Field>
                <Button type="submit" disabled={!selectedConnId}>
                  Process inbound
                </Button>
              </form>
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Push notification" />
            <CardBody>
              <form onSubmit={onSimulatePush} className="grid gap-3">
                <Field label="External event ID">
                  <Input
                    value={pushEventId}
                    onChange={(e) => setPushEventId(e.target.value)}
                    required
                  />
                </Field>
                <Button type="submit" disabled={!selectedConnId}>
                  Receive push
                </Button>
              </form>
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Draft review & send" />
            <CardBody>
              <form onSubmit={onDraftSendFlow} className="grid gap-3">
                <Field label="To">
                  <Input value={draftTo} onChange={(e) => setDraftTo(e.target.value)} required />
                </Field>
                <Field label="Subject">
                  <Input
                    value={draftSubject}
                    onChange={(e) => setDraftSubject(e.target.value)}
                    required
                  />
                </Field>
                <Field label="Body preview">
                  <Input value={draftBody} onChange={(e) => setDraftBody(e.target.value)} />
                </Field>
                <Button type="submit" disabled={!selectedConnId}>
                  Create → submit → approve → send
                </Button>
              </form>
            </CardBody>
          </Card>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader title="Thread mappings" />
            <CardBody>
              {threads.length === 0 ? (
                <EmptyState title="No threads" body="Process inbound email to create mappings." />
              ) : (
                <ul className="space-y-2 text-sm">
                  {threads.map((t) => (
                    <li key={t.id} className="rounded border p-2">
                      <div className="font-medium">{t.gmail_thread_id}</div>
                      <div className="text-muted-foreground">
                        Query: {t.query_id ?? "—"} · {formatUtc(t.created_at)}
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Message mappings" />
            <CardBody>
              {messages.length === 0 ? (
                <EmptyState title="No messages" body="Inbound or outbound messages appear here." />
              ) : (
                <ul className="space-y-2 text-sm">
                  {messages.map((m) => (
                    <li key={m.id} className="rounded border p-2">
                      <div className="flex items-center justify-between gap-2">
                        <span className="font-medium">{m.gmail_message_id}</span>
                        <StatusBadge status={m.direction} />
                      </div>
                      <div className="text-muted-foreground">
                        {m.subject ?? "—"} · {formatUtc(m.created_at)}
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
