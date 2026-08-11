"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Plus, Sparkles } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Textarea } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, StatusBanner } from "@/components/ui-states";
import {
  ApiError,
  approveRequirementsBrief,
  computeCompleteness,
  createClarification,
  createQuestionnaire,
  createQuestionnaireVersion,
  createRequirementsBrief,
  listRequirementsBriefs,
  publishQuestionnaireVersion,
  upsertRequirementAnswer,
  type CompletenessScore,
  type RequirementsBrief,
} from "@/lib/api";
import { can } from "@/lib/roles";
import {
  getWorkspaceProjectId,
  getWorkspaceRequirementEntityId,
  setWorkspaceRequirementEntityId,
} from "@/lib/workspace";

const DEFAULT_QUESTIONS = [
  { key: "problem", text: "What problem are we solving?", mandatory: true },
  { key: "users", text: "Who are the primary users?", mandatory: true },
  { key: "success", text: "What does success look like?", mandatory: true },
];

export function RequirementsDeskPage() {
  const { session } = useSession();
  const [error, setError] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const [showBootstrap, setShowBootstrap] = useState(false);
  const [code, setCode] = useState("intake");
  const [title, setTitle] = useState("Discovery intake");
  const [versionId, setVersionId] = useState("");
  const [entityId, setEntityId] = useState("");
  const [answers, setAnswers] = useState<Record<string, string>>({
    problem: "",
    users: "",
    success: "",
  });
  const [score, setScore] = useState<CompletenessScore | null>(null);
  const [briefs, setBriefs] = useState<RequirementsBrief[]>([]);

  useEffect(() => {
    const existing = getWorkspaceRequirementEntityId();
    if (existing) setEntityId(existing);
    else {
      const id = crypto.randomUUID();
      setEntityId(id);
      setWorkspaceRequirementEntityId(id);
    }
  }, []);

  const refreshBriefs = useCallback(async () => {
    if (!entityId) return;
    try {
      setBriefs(await listRequirementsBriefs(session, "opportunity", entityId));
    } catch {
      setBriefs([]);
    }
  }, [entityId, session]);

  useEffect(() => {
    void refreshBriefs();
  }, [refreshBriefs]);

  async function onBootstrap(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setOk(null);
    try {
      const questionnaire = await createQuestionnaire(session, {
        code: code.trim().toLowerCase(),
        title: title.trim(),
      });
      const version = await createQuestionnaireVersion(session, {
        questionnaire_id: questionnaire.id,
        questions: DEFAULT_QUESTIONS,
      });
      const published = await publishQuestionnaireVersion(session, version.id);
      setVersionId(published.id);
      setOk(`“${questionnaire.title}” is ready for answers`);
      setShowBootstrap(false);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not publish questionnaire");
    }
  }

  async function onSaveAnswers(event: FormEvent) {
    event.preventDefault();
    if (!versionId || !entityId) return;
    setError(null);
    setOk(null);
    try {
      const projectId = getWorkspaceProjectId();
      for (const q of DEFAULT_QUESTIONS) {
        const text = answers[q.key]?.trim();
        if (!text) continue;
        await upsertRequirementAnswer(session, {
          questionnaire_version_id: versionId,
          related_entity_type: "opportunity",
          related_entity_id: entityId,
          question_key: q.key,
          answer_text: text,
          project_id: projectId || undefined,
        });
      }
      const computed = await computeCompleteness(session, {
        questionnaire_version_id: versionId,
        related_entity_type: "opportunity",
        related_entity_id: entityId,
      });
      setScore(computed);
      setOk(
        computed.meets_threshold
          ? `Completeness ${computed.percentage}% — ready for a brief`
          : `Completeness ${computed.percentage}% — fill remaining gaps`,
      );
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not save answers");
    }
  }

  async function onCreateGaps() {
    if (!versionId || !entityId || !score) return;
    setError(null);
    setOk(null);
    try {
      for (const key of score.gap_question_keys) {
        const q = DEFAULT_QUESTIONS.find((item) => item.key === key);
        await createClarification(session, {
          questionnaire_version_id: versionId,
          related_entity_type: "opportunity",
          related_entity_id: entityId,
          question_key: key,
          question_text: q?.text ?? key,
          owner_actor_id: session.actorId,
        });
      }
      setOk(
        score.gap_question_keys.length === 1
          ? "1 clarification created"
          : `${score.gap_question_keys.length} clarifications created`,
      );
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not create clarifications");
    }
  }

  async function onBrief() {
    if (!versionId || !entityId) return;
    setError(null);
    setOk(null);
    try {
      const brief = await createRequirementsBrief(session, {
        related_entity_type: "opportunity",
        related_entity_id: entityId,
        title: `${title} brief`,
        summary: "Draft brief from discovery answers",
        questionnaire_version_id: versionId,
        completeness_score_id: score?.id,
        project_id: getWorkspaceProjectId() || undefined,
      });
      const approved = await approveRequirementsBrief(session, brief.id);
      setOk(`Brief version ${approved.version_number} approved`);
      await refreshBriefs();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not create brief");
    }
  }

  return (
    <AppShell title="Requirements" breadcrumbs={["Project Delivery", "Requirements"]}>
      <PageHeader
        title="Requirements"
        description="Discovery questionnaires, completeness scoring, clarifications, and human-approved briefs."
        actions={
          can(session.variant, "create") && !versionId ? (
            <Button onClick={() => setShowBootstrap((v) => !v)}>
              <Plus className="h-4 w-4" />
              Start questionnaire
            </Button>
          ) : null
        }
      />

      {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
      {ok ? <StatusBanner kind="success">{ok}</StatusBanner> : null}

      {showBootstrap && can(session.variant, "create") ? (
        <Card className="mb-6">
          <CardHeader>
            <h2 className="font-display text-lg">Publish intake questionnaire</h2>
            <p className="text-sm text-[var(--muted)]">
              Standard discovery questions help BD and delivery agree on the problem before a brief.
            </p>
          </CardHeader>
          <CardBody>
            <form
              onSubmit={onBootstrap}
              className="grid gap-4 md:grid-cols-2"
              aria-label="Publish questionnaire"
            >
              <Field label="Short name" hint="Internal reference for this intake form">
                <Input
                  required
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  pattern="[a-z0-9_]+"
                  placeholder="intake"
                />
              </Field>
              <Field label="Title">
                <Input
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Discovery intake"
                />
              </Field>
              <div className="flex justify-end gap-2 md:col-span-2">
                <Button type="button" variant="ghost" onClick={() => setShowBootstrap(false)}>
                  Cancel
                </Button>
                <Button type="submit">Publish questionnaire</Button>
              </div>
            </form>
          </CardBody>
        </Card>
      ) : null}

      {!versionId && !showBootstrap ? (
        <EmptyState
          title="No questionnaire yet"
          body="Publish an intake questionnaire, capture answers, then draft an approved requirements brief."
          action={
            can(session.variant, "create") ? (
              <Button onClick={() => setShowBootstrap(true)}>Start questionnaire</Button>
            ) : null
          }
          secondaryAction={
            <Button variant="ai">
              <Sparkles className="h-4 w-4" />
              Suggest questions
            </Button>
          }
        />
      ) : null}

      {versionId && can(session.variant, "create") ? (
        <Card className="mb-6">
          <CardHeader>
            <h2 className="font-display text-lg">{title}</h2>
            <p className="text-sm text-[var(--muted)]">
              Answer the discovery questions. Completeness is scored against mandatory items.
            </p>
          </CardHeader>
          <CardBody>
            <form onSubmit={onSaveAnswers} className="grid gap-4" aria-label="Answer questionnaire">
              {DEFAULT_QUESTIONS.map((q) => (
                <Field key={q.key} label={q.text}>
                  <Textarea
                    rows={2}
                    value={answers[q.key] ?? ""}
                    onChange={(e) =>
                      setAnswers((prev) => ({ ...prev, [q.key]: e.target.value }))
                    }
                    placeholder="Your answer"
                  />
                </Field>
              ))}
              <div className="flex justify-end">
                <Button type="submit">Save answers &amp; score</Button>
              </div>
            </form>
          </CardBody>
        </Card>
      ) : null}

      {score ? (
        <Card className="mb-6">
          <CardHeader className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h2 className="font-display text-lg">Completeness</h2>
              <p className="text-sm text-[var(--muted)]">
                {score.covered_count} of {score.mandatory_total} mandatory questions covered
              </p>
            </div>
            <StatusBadge status={score.meets_threshold ? "ready" : "pending"} />
          </CardHeader>
          <CardBody className="space-y-3">
            <p className="text-sm">
              Score <span className="font-semibold">{String(score.percentage)}%</span>
              {score.meets_threshold
                ? " — threshold met; you can create a brief."
                : " — clarify remaining gaps before approving a brief."}
            </p>
            <div className="flex flex-wrap gap-2">
              {score.gap_question_keys.length > 0 ? (
                <Button variant="outline" onClick={() => void onCreateGaps()}>
                  Create clarifications
                </Button>
              ) : null}
              {score.meets_threshold &&
              (can(session.variant, "approve") || can(session.variant, "create")) ? (
                <Button onClick={() => void onBrief()}>Create &amp; approve brief</Button>
              ) : null}
            </div>
          </CardBody>
        </Card>
      ) : null}

      <Card>
        <CardHeader>
          <h2 className="font-display text-lg">Briefs</h2>
          <p className="text-sm text-[var(--muted)]">
            Approved briefs summarize discovery for delivery planning.
          </p>
        </CardHeader>
        {briefs.length === 0 ? (
          <CardBody>
            <EmptyState
              title="No briefs yet"
              body="Complete the questionnaire and meet the completeness threshold to draft a brief."
            />
          </CardBody>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead className="sticky top-0 bg-[var(--surface-muted)] text-xs uppercase tracking-wide text-[var(--muted)]">
                <tr>
                  <th className="px-5 py-3 font-medium">Brief</th>
                  <th className="px-5 py-3 font-medium">Version</th>
                  <th className="px-5 py-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                {briefs.map((b) => (
                  <tr
                    key={b.id}
                    className="border-t border-[var(--line)] hover:bg-[var(--surface-muted)]/70"
                  >
                    <td className="px-5 py-3 font-medium">{b.title}</td>
                    <td className="px-5 py-3 text-[var(--muted)]">v{b.version_number}</td>
                    <td className="px-5 py-3">
                      <StatusBadge status={b.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </AppShell>
  );
}
