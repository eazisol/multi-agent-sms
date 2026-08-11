"use client";

import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import { MessageSquarePlus, Plus, Search } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Select, Textarea } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows, StatusBanner } from "@/components/ui-states";
import {
  ApiError,
  addMessageRecipient,
  approveCommsMessage,
  createCommsMessage,
  createConversation,
  formatUtc,
  listConversationMessages,
  listConversations,
  sendCommsMessage,
  type CommsMessage,
  type Conversation,
} from "@/lib/api";
import { can } from "@/lib/roles";
import {
  getWorkspaceConversationId,
  getWorkspaceProjectId,
  getWorkspaceQueryId,
  setWorkspaceConversationId,
} from "@/lib/workspace";

export function CommsDeskPage() {
  const { session } = useSession();
  const [error, setError] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [subject, setSubject] = useState("");
  const [classification, setClassification] = useState("internal");
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [messageBody, setMessageBody] = useState("");
  const [recipient, setRecipient] = useState("");
  const [activeMessage, setActiveMessage] = useState<CommsMessage | null>(null);
  const [messages, setMessages] = useState<CommsMessage[]>([]);

  const loadConversations = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const rows = await listConversations(session, {
        q: search.trim() || undefined,
        limit: 100,
      });
      setConversations(rows);
      const workspaceId = getWorkspaceConversationId();
      setConversationId((prev) => {
        if (prev && rows.some((r) => r.id === prev)) return prev;
        if (workspaceId && rows.some((r) => r.id === workspaceId)) return workspaceId;
        return rows[0]?.id ?? null;
      });
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Unable to load conversations");
      setConversations([]);
    } finally {
      setLoading(false);
    }
  }, [session, search]);

  useEffect(() => {
    void loadConversations();
  }, [loadConversations]);

  const current = useMemo(
    () => conversations.find((item) => item.id === conversationId) ?? null,
    [conversations, conversationId],
  );

  const refreshMessages = useCallback(async () => {
    if (!conversationId) {
      setMessages([]);
      return;
    }
    try {
      setMessages(await listConversationMessages(session, conversationId));
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Unable to load messages");
    }
  }, [conversationId, session]);

  useEffect(() => {
    void refreshMessages();
  }, [refreshMessages]);

  function selectConversation(id: string) {
    setConversationId(id);
    setWorkspaceConversationId(id);
    setActiveMessage(null);
  }

  async function onCreateConversation(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setOk(null);
    try {
      const projectId = getWorkspaceProjectId();
      const linkedQuery = getWorkspaceQueryId();
      const relatedEntityId = linkedQuery || crypto.randomUUID();
      const created = await createConversation(session, {
        subject: subject.trim(),
        related_entity_type: linkedQuery ? "client_query" : "opportunity",
        related_entity_id: relatedEntityId,
        classification,
        project_id: projectId || undefined,
      });
      setWorkspaceConversationId(created.id);
      setConversationId(created.id);
      setOk(
        created.classification === "confidential" || created.classification === "restricted"
          ? "Conversation opened — sensitive messages will need approval before send"
          : "Conversation opened",
      );
      setSubject("");
      setShowCreate(false);
      await loadConversations();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not open conversation");
    }
  }

  async function onCreateMessage(event: FormEvent) {
    event.preventDefault();
    if (!conversationId) return;
    setError(null);
    setOk(null);
    try {
      const message = await createCommsMessage(session, {
        conversation_id: conversationId,
        body: messageBody.trim(),
        classification,
      });
      await addMessageRecipient(session, {
        message_id: message.id,
        address: recipient.trim(),
        role: "to",
      });
      setActiveMessage(message);
      setMessageBody("");
      setOk(
        message.requires_approval
          ? "Draft saved — approval required before send"
          : "Draft saved with recipient",
      );
      await refreshMessages();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not draft message");
    }
  }

  async function onApprove() {
    if (!activeMessage) return;
    setError(null);
    setOk(null);
    try {
      const approved = await approveCommsMessage(session, activeMessage.id);
      setActiveMessage(approved);
      setOk("Message approved");
      await refreshMessages();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Approval failed");
    }
  }

  async function onSend() {
    if (!activeMessage) return;
    setError(null);
    setOk(null);
    try {
      const sent = await sendCommsMessage(session, activeMessage.id);
      setActiveMessage(sent);
      setOk("Message sent");
      await refreshMessages();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Send failed");
    }
  }

  return (
    <AppShell title="Messages" breadcrumbs={["Coordination", "Messages"]}>
      <PageHeader
        title="Messages"
        description="Entity-linked conversations with the client and team. Sensitive classifications require approval before send."
        actions={
          can(session.variant, "create") ? (
            <Button onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              New conversation
            </Button>
          ) : null
        }
      />

      {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
      {ok ? <StatusBanner kind="success">{ok}</StatusBanner> : null}

      {showCreate && can(session.variant, "create") ? (
        <Card className="mb-6">
          <CardHeader>
            <h2 className="font-display text-lg">Open conversation</h2>
            <p className="text-sm text-[var(--muted)]">
              Links to the active inquiry from Queries when available, otherwise a new opportunity
              thread.
            </p>
          </CardHeader>
          <CardBody>
            <form
              onSubmit={onCreateConversation}
              className="grid gap-4 md:grid-cols-2"
              aria-label="Open conversation"
            >
              <Field label="Subject" className="md:col-span-2">
                <Input
                  required
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  placeholder="Follow-up on discovery workshop"
                />
              </Field>
              <Field
                label="Sensitivity"
                hint="Confidential and restricted drafts need approval before send."
              >
                <Select
                  value={classification}
                  onChange={(e) => setClassification(e.target.value)}
                >
                  <option value="internal">Internal</option>
                  <option value="confidential">Confidential</option>
                  <option value="restricted">Restricted</option>
                </Select>
              </Field>
              <div className="flex items-end justify-end gap-2">
                <Button type="button" variant="ghost" onClick={() => setShowCreate(false)}>
                  Cancel
                </Button>
                <Button type="submit">Open conversation</Button>
              </div>
            </form>
          </CardBody>
        </Card>
      ) : null}

      <div className="grid gap-4 lg:grid-cols-[minmax(280px,340px)_1fr]">
        <Card>
          <CardHeader>
            <h2 className="font-display text-lg">Inbox</h2>
            <p className="text-sm text-[var(--muted)]">Conversations for this organization.</p>
            <div className="relative mt-3">
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--muted)]" />
              <Input
                className="pl-9"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search subject"
                aria-label="Search conversations"
              />
            </div>
          </CardHeader>
          {loading ? (
            <SkeletonRows />
          ) : conversations.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No conversations yet"
                body="Start a thread for a client inquiry or opportunity."
                action={
                  can(session.variant, "create") ? (
                    <Button onClick={() => setShowCreate(true)}>
                      <MessageSquarePlus className="h-4 w-4" />
                      New conversation
                    </Button>
                  ) : null
                }
              />
            </CardBody>
          ) : (
            <ul className="divide-y divide-[var(--line)]">
              {conversations.map((item) => (
                <li key={item.id}>
                  <button
                    type="button"
                    onClick={() => selectConversation(item.id)}
                    className={`w-full px-5 py-3 text-left transition hover:bg-[var(--surface-muted)]/70 ${
                      item.id === conversationId ? "bg-[var(--accent-soft)]" : ""
                    }`}
                  >
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <span className="font-medium">{item.subject}</span>
                      <StatusBadge status={item.status} />
                    </div>
                    <div className="mt-1 flex flex-wrap gap-2">
                      <StatusBadge status={item.classification} />
                      <span className="text-xs text-[var(--muted)]">{item.channel}</span>
                    </div>
                    <p className="mt-1 text-xs text-[var(--muted)]">{formatUtc(item.created_at)}</p>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </Card>

        {conversationId && current ? (
          <div className="grid gap-4 lg:grid-cols-[1fr_1fr]">
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">{current.subject}</h2>
                <p className="text-sm text-[var(--muted)]">
                  Draft the next message and choose a recipient.
                </p>
              </CardHeader>
              <CardBody>
                {can(session.variant, "create") ? (
                  <form
                    onSubmit={onCreateMessage}
                    className="grid gap-4"
                    aria-label="Draft message"
                  >
                    <Field label="Message">
                      <Textarea
                        required
                        rows={5}
                        value={messageBody}
                        onChange={(e) => setMessageBody(e.target.value)}
                        placeholder="Write the message to send…"
                      />
                    </Field>
                    <Field label="Recipient">
                      <Input
                        required
                        type="email"
                        value={recipient}
                        onChange={(e) => setRecipient(e.target.value)}
                        placeholder="ops@client.com"
                      />
                    </Field>
                    <Field label="Message sensitivity">
                      <Select
                        value={classification}
                        onChange={(e) => setClassification(e.target.value)}
                      >
                        <option value="internal">Internal</option>
                        <option value="confidential">Confidential</option>
                        <option value="restricted">Restricted</option>
                      </Select>
                    </Field>
                    <div className="flex flex-wrap justify-end gap-2">
                      <Button type="submit">Draft message</Button>
                      {activeMessage?.requires_approval && can(session.variant, "approve") ? (
                        <Button type="button" variant="outline" onClick={() => void onApprove()}>
                          Approve draft
                        </Button>
                      ) : null}
                      {activeMessage &&
                      (can(session.variant, "submit") || can(session.variant, "create")) ? (
                        <Button type="button" variant="outline" onClick={() => void onSend()}>
                          Send
                        </Button>
                      ) : null}
                    </div>
                  </form>
                ) : (
                  <StatusBanner kind="warning">Your role cannot draft messages.</StatusBanner>
                )}
              </CardBody>
            </Card>

            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">Thread</h2>
                <p className="text-sm text-[var(--muted)]">
                  Sent and draft history for this conversation.
                </p>
              </CardHeader>
              {messages.length === 0 ? (
                <CardBody>
                  <EmptyState
                    title="No messages yet"
                    body="Draft the first message to start the thread."
                  />
                </CardBody>
              ) : (
                <ul className="divide-y divide-[var(--line)]">
                  {messages.map((m) => (
                    <li key={m.id} className="px-5 py-4 text-sm">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <div className="flex flex-wrap items-center gap-2">
                          <StatusBadge status={m.status} />
                          <StatusBadge status={m.classification} />
                          {m.requires_approval ? (
                            <span className="text-xs text-[var(--warning)]">Needs approval</span>
                          ) : null}
                        </div>
                        <span className="text-xs text-[var(--muted)]">{formatUtc(m.created_at)}</span>
                      </div>
                      <p className="mt-2 whitespace-pre-wrap">{m.body}</p>
                      {m.sent_at ? (
                        <p className="mt-1 text-xs text-[var(--muted)]">
                          Sent {formatUtc(m.sent_at)}
                        </p>
                      ) : null}
                      <button
                        type="button"
                        className="mt-2 text-xs font-medium text-[var(--accent)] hover:underline"
                        onClick={() => setActiveMessage(m)}
                      >
                        Select for actions
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </Card>
          </div>
        ) : !loading ? (
          <EmptyState
            title="Select a conversation"
            body="Choose a thread from the inbox or open a new conversation."
            action={
              can(session.variant, "create") ? (
                <Button onClick={() => setShowCreate(true)}>
                  <MessageSquarePlus className="h-4 w-4" />
                  New conversation
                </Button>
              ) : null
            }
          />
        ) : null}
      </div>
    </AppShell>
  );
}
