"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { EmptyState, StatusBanner } from "@/components/ui-states";
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
      setOk(`Published questionnaire ${questionnaire.code} v${published.version_number}`);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Questionnaire bootstrap failed");
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
          ? `Completeness ${computed.percentage}% — threshold met`
          : `Completeness ${computed.percentage}% — gaps remain`,
      );
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Save answers failed");
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
      setOk(`Created ${score.gap_question_keys.length} clarification(s)`);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Clarification create failed");
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
        summary: "Draft brief from requirements desk",
        questionnaire_version_id: versionId,
        completeness_score_id: score?.id,
        project_id: getWorkspaceProjectId() || undefined,
      });
      const approved = await approveRequirementsBrief(session, brief.id);
      setOk(`Brief v${approved.version_number} approved`);
      await refreshBriefs();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Brief failed");
    }
  }

  return (
    <AppShell title="Requirements">
      <div className="space-y-6">
        <div>
          <h2 className="font-display text-3xl tracking-tight">Requirements gathering</h2>
          <p className="mt-1 text-sm text-[var(--muted)]">
            MOD-230 questionnaires, completeness (≥95%), clarifications, and human-approved
            briefs.
          </p>
        </div>
        {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
        {ok ? <StatusBanner kind="success">{ok}</StatusBanner> : null}

        {can(session.variant, "create") ? (
          <form
            onSubmit={onBootstrap}
            className="grid gap-3 rounded border border-[var(--line)] bg-white p-4 md:grid-cols-2"
            aria-label="Publish questionnaire"
          >
            <label className="flex flex-col gap-1 text-sm">
              <span>Questionnaire code</span>
              <input
                required
                className="rounded border border-[var(--line)] px-3 py-2"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                pattern="[a-z0-9_]+"
              />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span>Title</span>
              <input
                required
                className="rounded border border-[var(--line)] px-3 py-2"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </label>
            <button
              type="submit"
              className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white md:col-span-2 md:w-fit"
            >
              Publish questionnaire
            </button>
          </form>
        ) : null}

        {versionId ? (
          <p className="text-sm text-[var(--muted)]">
            Version <code>{versionId}</code> · entity <code>{entityId}</code>
          </p>
        ) : null}

        {versionId && can(session.variant, "create") ? (
          <form
            onSubmit={onSaveAnswers}
            className="grid gap-3 rounded border border-[var(--line)] bg-white p-4"
            aria-label="Answer questionnaire"
          >
            {DEFAULT_QUESTIONS.map((q) => (
              <label key={q.key} className="flex flex-col gap-1 text-sm">
                <span>{q.text}</span>
                <textarea
                  rows={2}
                  className="rounded border border-[var(--line)] px-3 py-2"
                  value={answers[q.key] ?? ""}
                  onChange={(e) =>
                    setAnswers((prev) => ({ ...prev, [q.key]: e.target.value }))
                  }
                />
              </label>
            ))}
            <button
              type="submit"
              className="w-fit rounded bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white"
            >
              Save answers &amp; score
            </button>
          </form>
        ) : null}

        {score ? (
          <div className="rounded border border-[var(--line)] bg-white p-4 text-sm">
            <p>
              Coverage {score.covered_count}/{score.mandatory_total} (
              {String(score.percentage)}%)
              {score.meets_threshold ? " — ready for brief" : ""}
            </p>
            {score.gap_question_keys.length > 0 ? (
              <button
                type="button"
                className="mt-3 rounded border border-[var(--line)] px-3 py-2"
                onClick={() => void onCreateGaps()}
              >
                Create clarifications for gaps
              </button>
            ) : can(session.variant, "approve") || can(session.variant, "create") ? (
              <button
                type="button"
                className="mt-3 rounded border border-[var(--line)] px-3 py-2"
                onClick={() => void onBrief()}
              >
                Create &amp; approve brief
              </button>
            ) : null}
          </div>
        ) : null}

        <section aria-label="Briefs">
          <h3 className="font-display text-xl">Briefs</h3>
          {briefs.length === 0 ? (
            <EmptyState title="No briefs yet" body="Complete the questionnaire to draft a brief." />
          ) : (
            <ul className="mt-3 divide-y divide-[var(--line)] rounded border border-[var(--line)] bg-white">
              {briefs.map((b) => (
                <li key={b.id} className="px-4 py-3 text-sm">
                  <span className="font-medium">
                    {b.title} v{b.version_number}
                  </span>
                  <span className="ml-2 text-[var(--muted)]">{b.status}</span>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </AppShell>
  );
}
