"use client";

import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import { Plus, Search, Sparkles } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Select, Textarea } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows, StatusBanner } from "@/components/ui-states";
import {
  ApiError,
  approveRequirementsBrief,
  computeCompleteness,
  createClarification,
  createQuestionnaire,
  createQuestionnaireVersion,
  createRequirementsBrief,
  formatUtc,
  getPublishedQuestionnaireVersion,
  listQueries,
  listQuestionnaires,
  listRequirementAnswers,
  listRequirementsBriefs,
  publishQuestionnaireVersion,
  upsertRequirementAnswer,
  type ClientQuery,
  type CompletenessScore,
  type Questionnaire,
  type QuestionnaireVersion,
  type RequirementsBrief,
} from "@/lib/api";
import { can } from "@/lib/roles";
import {
  getWorkspaceProjectId,
  getWorkspaceQueryId,
  getWorkspaceQuestionnaireId,
  setWorkspaceQueryId,
  setWorkspaceQuestionnaireId,
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
  const [loading, setLoading] = useState(true);
  const [showBootstrap, setShowBootstrap] = useState(false);
  const [code, setCode] = useState("intake");
  const [title, setTitle] = useState("Discovery intake");
  const [search, setSearch] = useState("");
  const [questionnaires, setQuestionnaires] = useState<Questionnaire[]>([]);
  const [questionnaireId, setQuestionnaireId] = useState<string | null>(null);
  const [version, setVersion] = useState<QuestionnaireVersion | null>(null);
  const [queries, setQueries] = useState<ClientQuery[]>([]);
  const [entityId, setEntityId] = useState("");
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [score, setScore] = useState<CompletenessScore | null>(null);
  const [briefs, setBriefs] = useState<RequirementsBrief[]>([]);

  const questions = useMemo(
    () => (version?.questions_json?.length ? version.questions_json : DEFAULT_QUESTIONS),
    [version],
  );

  const loadQuestionnaires = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const rows = await listQuestionnaires(session, {
        q: search.trim() || undefined,
        limit: 100,
      });
      setQuestionnaires(rows);
      const workspaceId = getWorkspaceQuestionnaireId();
      setQuestionnaireId((prev) => {
        if (prev && rows.some((r) => r.id === prev)) return prev;
        if (workspaceId && rows.some((r) => r.id === workspaceId)) return workspaceId;
        return rows[0]?.id ?? null;
      });
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Unable to load questionnaires");
      setQuestionnaires([]);
    } finally {
      setLoading(false);
    }
  }, [session, search]);

  useEffect(() => {
    void loadQuestionnaires();
  }, [loadQuestionnaires]);

  useEffect(() => {
    void (async () => {
      try {
        const rows = await listQueries(session, { limit: 100 });
        setQueries(rows);
        const workspaceQuery = getWorkspaceQueryId();
        setEntityId((prev) => {
          if (prev && rows.some((r) => r.id === prev)) return prev;
          if (workspaceQuery && rows.some((r) => r.id === workspaceQuery)) return workspaceQuery;
          return rows[0]?.id ?? getWorkspaceProjectId();
        });
      } catch {
        setQueries([]);
        setEntityId(getWorkspaceQueryId() || getWorkspaceProjectId());
      }
    })();
  }, [session]);

  const currentQuestionnaire = useMemo(
    () => questionnaires.find((item) => item.id === questionnaireId) ?? null,
    [questionnaires, questionnaireId],
  );

  const relatedEntityType = useMemo(() => {
    if (entityId && queries.some((q) => q.id === entityId)) return "crm_query";
    if (entityId && entityId === getWorkspaceProjectId()) return "project";
    return entityId ? "crm_query" : "";
  }, [entityId, queries]);

  useEffect(() => {
    if (!questionnaireId) {
      setVersion(null);
      return;
    }
    void (async () => {
      try {
        const published = await getPublishedQuestionnaireVersion(session, questionnaireId);
        setVersion(published);
      } catch {
        setVersion(null);
      }
    })();
  }, [questionnaireId, session]);

  const refreshAnswers = useCallback(async () => {
    if (!version || !entityId || !relatedEntityType) {
      setAnswers({});
      return;
    }
    try {
      const rows = await listRequirementAnswers(session, {
        questionnaire_version_id: version.id,
        related_entity_type: relatedEntityType,
        related_entity_id: entityId,
      });
      const next: Record<string, string> = {};
      for (const q of questions) next[q.key] = "";
      for (const row of rows) {
        if (row.answer_text) next[row.question_key] = row.answer_text;
      }
      setAnswers(next);
    } catch {
      const next: Record<string, string> = {};
      for (const q of questions) next[q.key] = "";
      setAnswers(next);
    }
  }, [session, version, entityId, relatedEntityType, questions]);

  useEffect(() => {
    void refreshAnswers();
  }, [refreshAnswers]);

  const refreshBriefs = useCallback(async () => {
    try {
      if (entityId && relatedEntityType) {
        setBriefs(
          await listRequirementsBriefs(session, {
            related_entity_type: relatedEntityType,
            related_entity_id: entityId,
            limit: 100,
          }),
        );
      } else {
        setBriefs(await listRequirementsBriefs(session, { limit: 100 }));
      }
    } catch {
      setBriefs([]);
    }
  }, [entityId, relatedEntityType, session]);

  useEffect(() => {
    void refreshBriefs();
  }, [refreshBriefs]);

  function selectQuestionnaire(id: string) {
    setQuestionnaireId(id);
    setWorkspaceQuestionnaireId(id);
    setScore(null);
  }

  function selectEntity(id: string) {
    setEntityId(id);
    if (queries.some((q) => q.id === id)) setWorkspaceQueryId(id);
    setScore(null);
  }

  async function onBootstrap(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setOk(null);
    try {
      const questionnaire = await createQuestionnaire(session, {
        code: code.trim().toLowerCase(),
        title: title.trim(),
      });
      const createdVersion = await createQuestionnaireVersion(session, {
        questionnaire_id: questionnaire.id,
        questions: DEFAULT_QUESTIONS,
      });
      const published = await publishQuestionnaireVersion(session, createdVersion.id);
      setWorkspaceQuestionnaireId(questionnaire.id);
      setQuestionnaireId(questionnaire.id);
      setVersion(published);
      setOk(`“${questionnaire.title}” is ready for answers`);
      setShowBootstrap(false);
      await loadQuestionnaires();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not publish questionnaire");
    }
  }

  async function onSaveAnswers(event: FormEvent) {
    event.preventDefault();
    if (!version || !entityId || !relatedEntityType) {
      setError("Select a linked inquiry (or project) before saving answers");
      return;
    }
    setError(null);
    setOk(null);
    try {
      const projectId = getWorkspaceProjectId();
      for (const q of questions) {
        const text = answers[q.key]?.trim();
        if (!text) continue;
        await upsertRequirementAnswer(session, {
          questionnaire_version_id: version.id,
          related_entity_type: relatedEntityType,
          related_entity_id: entityId,
          question_key: q.key,
          answer_text: text,
          project_id: projectId || undefined,
        });
      }
      const computed = await computeCompleteness(session, {
        questionnaire_version_id: version.id,
        related_entity_type: relatedEntityType,
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
    if (!version || !entityId || !relatedEntityType || !score) return;
    setError(null);
    setOk(null);
    try {
      for (const key of score.gap_question_keys) {
        const q = questions.find((item) => item.key === key);
        await createClarification(session, {
          questionnaire_version_id: version.id,
          related_entity_type: relatedEntityType,
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
    if (!version || !entityId || !relatedEntityType) return;
    setError(null);
    setOk(null);
    try {
      const brief = await createRequirementsBrief(session, {
        related_entity_type: relatedEntityType,
        related_entity_id: entityId,
        title: `${currentQuestionnaire?.title ?? title} brief`,
        summary: "Draft brief from discovery answers",
        questionnaire_version_id: version.id,
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
          can(session.variant, "create") ? (
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

      <div className="grid gap-4 lg:grid-cols-[minmax(280px,340px)_1fr]">
        <Card>
          <CardHeader>
            <h2 className="font-display text-lg">Questionnaires</h2>
            <p className="text-sm text-[var(--muted)]">Loaded from the organization database.</p>
            <div className="relative mt-3">
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--muted)]" />
              <Input
                className="pl-9"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search code or title"
                aria-label="Search questionnaires"
              />
            </div>
          </CardHeader>
          {loading ? (
            <SkeletonRows />
          ) : questionnaires.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No questionnaires yet"
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
            </CardBody>
          ) : (
            <ul className="divide-y divide-[var(--line)]">
              {questionnaires.map((item) => (
                <li key={item.id}>
                  <button
                    type="button"
                    onClick={() => selectQuestionnaire(item.id)}
                    className={`w-full px-5 py-3 text-left transition hover:bg-[var(--surface-muted)]/70 ${
                      item.id === questionnaireId ? "bg-[var(--accent-soft)]" : ""
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span className="font-medium">{item.title}</span>
                      <StatusBadge status={item.status} />
                    </div>
                    <p className="mt-1 text-sm text-[var(--muted)]">{item.code}</p>
                    {item.created_at ? (
                      <p className="mt-1 text-xs text-[var(--muted)]">{formatUtc(item.created_at)}</p>
                    ) : null}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </Card>

        <div className="space-y-4">
          {currentQuestionnaire ? (
            <Card>
              <CardHeader>
                <h2 className="font-display text-xl">{currentQuestionnaire.title}</h2>
                <p className="text-sm text-[var(--muted)]">
                  Answers and briefs attach to a linked inquiry from Queries (preferred) or the
                  workspace project.
                </p>
              </CardHeader>
              <CardBody>
                <Field
                  label="Linked inquiry"
                  hint={
                    queries.length === 0
                      ? "Create an inquiry on Queries, or ensure a workspace project is selected."
                      : "Discovery work stays scoped to this crm_query record."
                  }
                >
                  <Select
                    value={entityId}
                    onChange={(e) => selectEntity(e.target.value)}
                    aria-label="Linked inquiry"
                  >
                    <option value="">Select inquiry…</option>
                    {queries.map((q) => (
                      <option key={q.id} value={q.id}>
                        {q.subject}
                      </option>
                    ))}
                    {getWorkspaceProjectId() &&
                    !queries.some((q) => q.id === getWorkspaceProjectId()) ? (
                      <option value={getWorkspaceProjectId()}>
                        Workspace project ({getWorkspaceProjectId().slice(0, 8)}…)
                      </option>
                    ) : null}
                  </Select>
                </Field>
                {!version ? (
                  <StatusBanner kind="warning">
                    This questionnaire has no published version yet.
                  </StatusBanner>
                ) : null}
              </CardBody>
            </Card>
          ) : null}

          {version && can(session.variant, "create") ? (
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">
                  {currentQuestionnaire?.title ?? title} · v{version.version_number}
                </h2>
                <p className="text-sm text-[var(--muted)]">
                  Answer the discovery questions. Completeness is scored against mandatory items.
                </p>
              </CardHeader>
              <CardBody>
                <form
                  onSubmit={onSaveAnswers}
                  className="grid gap-4"
                  aria-label="Answer questionnaire"
                >
                  {questions.map((q) => (
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
            <Card>
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
                {entityId
                  ? "Briefs for the selected inquiry / project."
                  : "Approved briefs across the organization."}
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
        </div>
      </div>
    </AppShell>
  );
}
