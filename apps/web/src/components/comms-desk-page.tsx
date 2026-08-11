"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { EmptyState, StatusBanner } from "@/components/ui-states";
import {
  ApiError,
  addMessageRecipient,
  approveCommsMessage,
  createCommsMessage,
  createConversation,
  formatUtc,
  listConversationMessages,
  sendCommsMessage,
  type CommsMessage,
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
  const [subject, setSubject] = useState("");
  const [classification, setClassification] = useState("internal");
  const [entityType, setEntityType] = useState("client_query");
  const [entityId, setEntityId] = useState("");
  const [conversationId, setConversationId] = useState("");
  const [messageBody, setMessageBody] = useState("");
  const [recipient, setRecipient] = useState("ops@example.com");
  const [activeMessage, setActiveMessage] = useState<CommsMessage | null>(null);
  const [messages, setMessages] = useState<CommsMessage[]>([]);

  useEffect(() => {
    setConversationId(getWorkspaceConversationId());
    setEntityId(getWorkspaceQueryId() || crypto.randomUUID());
  }, []);

  const refreshMessages = useCallback(async () => {
    if (!conversationId) {
      setMessages([]);
      return;
    }
    try {
      setMessages(await listConversationMessages(session, conversationId));
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Load messages failed");
    }
  }, [conversationId, session]);

  useEffect(() => {
    void refreshMessages();
  }, [refreshMessages]);

  async function onCreateConversation(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setOk(null);
    try {
      const projectId = getWorkspaceProjectId();
      const created = await createConversation(session, {
        subject: subject.trim(),
        related_entity_type: entityType.trim(),
        related_entity_id: entityId.trim(),
        classification,
        project_id: projectId || undefined,
      });
      setConversationId(created.id);
      setWorkspaceConversationId(created.id);
      setOk(`Conversation opened (${created.classification})`);
      setSubject("");
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Create conversation failed");
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
          ? "Draft needs approval before send"
          : "Message drafted with recipient",
      );
      await refreshMessages();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Draft message failed");
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
      setError(err instanceof ApiError ? err.problem.message : "Approve failed");
    }
  }

  async function onSend() {
    if (!activeMessage) return;
    setError(null);
    setOk(null);
    try {
      const sent = await sendCommsMessage(session, activeMessage.id);
      setActiveMessage(sent);
      setOk("Message sent — history is immutable");
      await refreshMessages();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Send failed");
    }
  }

  return (
    <AppShell title="Comms">
      <div className="space-y-6">
        <div>
          <h2 className="font-display text-3xl tracking-tight">Communications</h2>
          <p className="mt-1 text-sm text-[var(--muted)]">
            MOD-220 entity-linked conversations. Sensitive classifications require approval
            before send.
          </p>
        </div>
        {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
        {ok ? <StatusBanner kind="success">{ok}</StatusBanner> : null}

        {can(session.variant, "create") ? (
          <form
            onSubmit={onCreateConversation}
            className="grid gap-3 rounded border border-[var(--line)] bg-white p-4 md:grid-cols-2"
            aria-label="Open conversation"
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
            <label className="flex flex-col gap-1 text-sm">
              <span>Related entity type</span>
              <input
                required
                className="rounded border border-[var(--line)] px-3 py-2"
                value={entityType}
                onChange={(e) => setEntityType(e.target.value)}
                pattern="[a-z0-9_]+"
              />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span>Related entity id</span>
              <input
                required
                className="rounded border border-[var(--line)] px-3 py-2 font-mono text-xs"
                value={entityId}
                onChange={(e) => setEntityId(e.target.value)}
              />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span>Classification</span>
              <select
                className="rounded border border-[var(--line)] px-3 py-2"
                value={classification}
                onChange={(e) => setClassification(e.target.value)}
              >
                <option value="internal">internal</option>
                <option value="confidential">confidential (needs approval)</option>
                <option value="restricted">restricted (needs approval)</option>
              </select>
            </label>
            <button
              type="submit"
              className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white md:col-span-2 md:w-fit"
            >
              Open conversation
            </button>
          </form>
        ) : (
          <StatusBanner kind="error">This UI role cannot create conversations.</StatusBanner>
        )}

        {conversationId ? (
          <p className="text-sm text-[var(--muted)]">
            Active conversation: <code>{conversationId}</code>
          </p>
        ) : null}

        {conversationId && can(session.variant, "create") ? (
          <form
            onSubmit={onCreateMessage}
            className="grid gap-3 rounded border border-[var(--line)] bg-white p-4"
            aria-label="Draft message"
          >
            <label className="flex flex-col gap-1 text-sm">
              <span>Message body</span>
              <textarea
                required
                rows={4}
                className="rounded border border-[var(--line)] px-3 py-2"
                value={messageBody}
                onChange={(e) => setMessageBody(e.target.value)}
              />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span>Recipient</span>
              <input
                required
                type="email"
                className="rounded border border-[var(--line)] px-3 py-2"
                value={recipient}
                onChange={(e) => setRecipient(e.target.value)}
              />
            </label>
            <button
              type="submit"
              className="w-fit rounded bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white"
            >
              Draft message
            </button>
          </form>
        ) : null}

        {activeMessage ? (
          <div className="flex flex-wrap gap-2">
            {activeMessage.requires_approval && can(session.variant, "approve") ? (
              <button
                type="button"
                onClick={() => void onApprove()}
                className="rounded border border-[var(--line)] bg-white px-3 py-2 text-sm"
              >
                Approve message
              </button>
            ) : null}
            {can(session.variant, "submit") || can(session.variant, "create") ? (
              <button
                type="button"
                onClick={() => void onSend()}
                className="rounded border border-[var(--line)] bg-white px-3 py-2 text-sm"
              >
                Send message
              </button>
            ) : null}
          </div>
        ) : null}

        <section aria-label="Conversation messages">
          <h3 className="font-display text-xl">Messages</h3>
          {messages.length === 0 ? (
            <EmptyState title="No messages yet" body="Draft a message after opening a conversation." />
          ) : (
            <ul className="mt-3 divide-y divide-[var(--line)] rounded border border-[var(--line)] bg-white">
              {messages.map((m) => (
                <li key={m.id} className="px-4 py-3 text-sm">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <span className="font-medium">{m.status}</span>
                    <span className="text-[var(--muted)]">{formatUtc(m.created_at)}</span>
                  </div>
                  <p className="mt-1 whitespace-pre-wrap">{m.body}</p>
                  <p className="mt-1 text-xs text-[var(--muted)]">
                    {m.classification}
                    {m.requires_approval ? " · approval required" : ""}
                    {m.sent_at ? ` · sent ${formatUtc(m.sent_at)}` : ""}
                  </p>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </AppShell>
  );
}
