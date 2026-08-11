import type { ActorKind, GovVariant } from "@/lib/roles";

export type SessionState = {
  organizationId: string;
  actorId: string;
  actorKind: ActorKind;
  variant: GovVariant;
};

export type ProblemDetails = {
  code: string;
  message: string;
  correlation_id?: string | null;
  details?: Array<Record<string, unknown>> | null;
};

export type PageMeta = {
  limit: number;
  offset: number;
  total: number;
  has_more: boolean;
};

export type Baseline = {
  id: string;
  organization_id: string;
  baseline_key: string;
  title: string;
  artifact_path: string;
  document_version: string;
  classification: string;
  approval_status: string;
  version: number;
  created_at: string;
  updated_at: string;
};

export type BaselinePage = {
  items: Baseline[];
  page: PageMeta;
};

export type AuditEvent = {
  id: string;
  organization_id: string;
  actor_id: string;
  actor_kind: string;
  action: string;
  entity_type: string;
  entity_id: string;
  entity_version: number | null;
  reason: string | null;
  source: string;
  correlation_id: string;
  created_at: string;
};

export type AuditEventPage = {
  items: AuditEvent[];
  page: PageMeta;
};

export class ApiError extends Error {
  readonly status: number;
  readonly problem: ProblemDetails;

  constructor(status: number, problem: ProblemDetails) {
    super(problem.message);
    this.status = status;
    this.problem = problem;
  }
}

function apiBase(): string {
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
}

function headers(session: SessionState): HeadersInit {
  return {
    "Content-Type": "application/json",
    "X-Organization-Id": session.organizationId,
    "X-Actor-Id": session.actorId,
    "X-Actor-Kind": session.actorKind,
    "X-Correlation-Id": crypto.randomUUID(),
    "X-Actor-Name": `web:${session.variant}`,
  };
}

async function parse<T>(response: Response): Promise<T> {
  if (response.ok) {
    if (response.status === 204) {
      return undefined as T;
    }
    return (await response.json()) as T;
  }
  let problem: ProblemDetails = {
    code: "http_error",
    message: `Request failed (${response.status})`,
  };
  try {
    problem = (await response.json()) as ProblemDetails;
  } catch {
    // keep fallback
  }
  throw new ApiError(response.status, problem);
}

export async function listBaselines(
  session: SessionState,
  params: { limit?: number; offset?: number; q?: string; status?: string; sort?: string } = {},
): Promise<BaselinePage> {
  const query = new URLSearchParams();
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  if (params.q) query.set("q", params.q);
  if (params.status) query.set("status", params.status);
  if (params.sort) query.set("sort", params.sort);
  const response = await fetch(`${apiBase()}/api/v1/governance/baselines?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<BaselinePage>(response);
}

export async function getBaseline(session: SessionState, id: string): Promise<Baseline> {
  const response = await fetch(`${apiBase()}/api/v1/governance/baselines/${id}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<Baseline>(response);
}

export async function createBaseline(
  session: SessionState,
  body: {
    baseline_key: string;
    title: string;
    artifact_path: string;
    document_version: string;
    classification?: string;
  },
): Promise<Baseline> {
  const response = await fetch(`${apiBase()}/api/v1/governance/baselines`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Baseline>(response);
}

export async function updateBaseline(
  session: SessionState,
  id: string,
  body: { title: string; expected_version: number },
): Promise<Baseline> {
  const response = await fetch(`${apiBase()}/api/v1/governance/baselines/${id}`, {
    method: "PATCH",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Baseline>(response);
}

export async function transitionBaseline(
  session: SessionState,
  id: string,
  body: { target_status: string; expected_version: number; reason?: string },
): Promise<Baseline> {
  const response = await fetch(`${apiBase()}/api/v1/governance/baselines/${id}/transitions`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Baseline>(response);
}

export async function listBaselineHistory(
  session: SessionState,
  id: string,
): Promise<AuditEventPage> {
  const response = await fetch(`${apiBase()}/api/v1/governance/baselines/${id}/history`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<AuditEventPage>(response);
}

export function formatUtc(iso: string): string {
  const date = new Date(iso);
  return new Intl.DateTimeFormat("en-GB", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "UTC",
  }).format(date) + " UTC";
}

/* ---- Phase 2 desks (MOD-200 … MOD-260) ---- */

export type Client = {
  id: string;
  organization_id: string;
  code: string;
  legal_name: string;
  trading_name: string | null;
  status: string;
  owner_actor_id: string;
  industry: string | null;
  website: string | null;
  version: number;
  created_at: string;
};

export type ClientPage = {
  items: Client[];
  page: PageMeta;
};

export type QuerySource = {
  id: string;
  code: string;
  title: string;
  channel: string;
  status: string;
};

export type ClientQuery = {
  id: string;
  subject: string;
  summary: string;
  status: string;
  sla_status: string;
  client_id: string | null;
  project_id: string | null;
  source_id: string | null;
  created_at: string;
};

export type Project = {
  id: string;
  code: string;
  title: string;
  status: string;
  owner_actor_id: string;
  client_id: string | null;
  created_at: string;
};

export type ProjectRequirement = {
  id: string;
  project_id: string;
  requirement_code: string;
  title: string;
  status: string;
  current_version_id: string | null;
};

export type RequirementVersion = {
  id: string;
  requirement_id: string;
  version_number: number;
  statement: string;
  status: string;
  approved_by_actor_id: string | null;
};

export type SrsBaseline = {
  id: string;
  project_id: string;
  version_number: number;
  title: string;
  status: string;
  approved_by_actor_id: string | null;
};

export type DocumentRecord = {
  id: string;
  title: string;
  classification: string;
  status: string;
  owner_actor_id: string;
  current_version_id: string | null;
};

export type DocumentVersion = {
  id: string;
  document_id: string;
  version_number: number;
  status: string;
  filename: string;
  storage_key: string;
  effective_at: string | null;
  indexing_allowed: boolean;
};

export type Phase = {
  id: string;
  project_id: string;
  code: string;
  title: string;
  sequence: number;
  status: string;
  owner_actor_id: string;
  completed_at: string | null;
};

export type Milestone = {
  id: string;
  phase_id: string;
  code: string;
  title: string;
  owner_actor_id: string;
  target_date: string;
  status: string;
  requires_approval: boolean;
  approved_by_actor_id: string | null;
};

export async function listClients(
  session: SessionState,
  params: { limit?: number; offset?: number } = {},
): Promise<ClientPage> {
  const query = new URLSearchParams();
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await fetch(`${apiBase()}/api/v1/clients?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ClientPage>(response);
}

export async function createClient(
  session: SessionState,
  body: { code: string; legal_name: string; trading_name?: string; industry?: string },
): Promise<Client> {
  const response = await fetch(`${apiBase()}/api/v1/clients`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Client>(response);
}

export async function createQuerySource(
  session: SessionState,
  body: { code: string; title: string; channel?: string },
): Promise<QuerySource> {
  const response = await fetch(`${apiBase()}/api/v1/queries/sources`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<QuerySource>(response);
}

export async function createQuery(
  session: SessionState,
  body: {
    subject: string;
    summary: string;
    original_message?: string;
    source_id?: string;
    client_id?: string;
  },
): Promise<ClientQuery> {
  const response = await fetch(`${apiBase()}/api/v1/queries`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<ClientQuery>(response);
}

export async function transitionQuery(
  session: SessionState,
  queryId: string,
  body: { next_status: string; classification?: string; reason?: string },
): Promise<ClientQuery> {
  const response = await fetch(`${apiBase()}/api/v1/queries/${queryId}/transitions`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<ClientQuery>(response);
}

export async function createProject(
  session: SessionState,
  body: { code: string; title: string; client_id?: string },
): Promise<Project> {
  const response = await fetch(`${apiBase()}/api/v1/projects`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Project>(response);
}

export async function createRequirement(
  session: SessionState,
  body: { project_id: string; requirement_code: string; title: string },
): Promise<ProjectRequirement> {
  const response = await fetch(`${apiBase()}/api/v1/projects/requirements`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<ProjectRequirement>(response);
}

export async function listRequirements(
  session: SessionState,
  projectId: string,
): Promise<ProjectRequirement[]> {
  const response = await fetch(`${apiBase()}/api/v1/projects/${projectId}/requirements`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ProjectRequirement[]>(response);
}

export async function createRequirementVersion(
  session: SessionState,
  body: {
    requirement_id: string;
    statement: string;
    priority?: string;
    change_reason?: string;
  },
): Promise<RequirementVersion> {
  const response = await fetch(`${apiBase()}/api/v1/projects/requirement-versions`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<RequirementVersion>(response);
}

export async function addAcceptanceCriterion(
  session: SessionState,
  body: { requirement_version_id: string; criterion_code: string; text: string },
): Promise<{ id: string }> {
  const response = await fetch(`${apiBase()}/api/v1/projects/acceptance-criteria`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<{ id: string }>(response);
}

export async function approveRequirementVersion(
  session: SessionState,
  versionId: string,
): Promise<RequirementVersion> {
  const response = await fetch(
    `${apiBase()}/api/v1/projects/requirement-versions/${versionId}/approve`,
    { method: "POST", headers: headers(session) },
  );
  return parse<RequirementVersion>(response);
}

export async function createSrsBaseline(
  session: SessionState,
  body: {
    project_id: string;
    title: string;
    summary: string;
    requirement_version_ids: string[];
    change_reason?: string;
  },
): Promise<SrsBaseline> {
  const response = await fetch(`${apiBase()}/api/v1/projects/srs-baselines`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<SrsBaseline>(response);
}

export async function approveSrsBaseline(
  session: SessionState,
  baselineId: string,
): Promise<SrsBaseline> {
  const response = await fetch(
    `${apiBase()}/api/v1/projects/srs-baselines/${baselineId}/approve`,
    { method: "POST", headers: headers(session) },
  );
  return parse<SrsBaseline>(response);
}

export async function createDocument(
  session: SessionState,
  body: { title: string; classification?: string; project_id?: string },
): Promise<DocumentRecord> {
  const response = await fetch(`${apiBase()}/api/v1/documents`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<DocumentRecord>(response);
}

export async function createDocumentVersion(
  session: SessionState,
  body: {
    document_id: string;
    storage_key: string;
    filename: string;
    content_type?: string;
    size_bytes?: number;
  },
): Promise<DocumentVersion> {
  const response = await fetch(`${apiBase()}/api/v1/documents/versions`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<DocumentVersion>(response);
}

export async function recordDocumentScan(
  session: SessionState,
  body: { document_version_id: string; verdict: string; detail?: string },
): Promise<{ id: string; verdict: string }> {
  const response = await fetch(`${apiBase()}/api/v1/documents/scan-results`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<{ id: string; verdict: string }>(response);
}

export async function markDocumentAvailable(
  session: SessionState,
  versionId: string,
  body: { effective_at: string },
): Promise<DocumentVersion> {
  const response = await fetch(
    `${apiBase()}/api/v1/documents/versions/${versionId}/available`,
    {
      method: "POST",
      headers: headers(session),
      body: JSON.stringify(body),
    },
  );
  return parse<DocumentVersion>(response);
}

export async function createPhase(
  session: SessionState,
  body: {
    project_id: string;
    code: string;
    title: string;
    sequence?: number;
  },
): Promise<Phase> {
  const response = await fetch(`${apiBase()}/api/v1/roadmap/phases`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Phase>(response);
}

export async function listPhases(
  session: SessionState,
  projectId: string,
): Promise<Phase[]> {
  const response = await fetch(
    `${apiBase()}/api/v1/roadmap/projects/${projectId}/phases`,
    { headers: headers(session), cache: "no-store" },
  );
  return parse<Phase[]>(response);
}

export async function completePhase(
  session: SessionState,
  phaseId: string,
): Promise<Phase> {
  const response = await fetch(`${apiBase()}/api/v1/roadmap/phases/${phaseId}/complete`, {
    method: "POST",
    headers: headers(session),
  });
  return parse<Phase>(response);
}

export async function createMilestone(
  session: SessionState,
  body: {
    phase_id: string;
    code: string;
    title: string;
    owner_actor_id: string;
    target_date: string;
    requires_approval?: boolean;
  },
): Promise<Milestone> {
  const response = await fetch(`${apiBase()}/api/v1/roadmap/milestones`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Milestone>(response);
}

export async function approveMilestone(
  session: SessionState,
  milestoneId: string,
): Promise<Milestone> {
  const response = await fetch(
    `${apiBase()}/api/v1/roadmap/milestones/${milestoneId}/approve`,
    { method: "POST", headers: headers(session) },
  );
  return parse<Milestone>(response);
}

export async function completeMilestone(
  session: SessionState,
  milestoneId: string,
): Promise<Milestone> {
  const response = await fetch(
    `${apiBase()}/api/v1/roadmap/milestones/${milestoneId}/complete`,
    { method: "POST", headers: headers(session) },
  );
  return parse<Milestone>(response);
}

/* ---- Comms / Requirements / Tickets desks (MOD-220, 230, 300) ---- */

export type Conversation = {
  id: string;
  subject: string;
  channel: string;
  related_entity_type: string;
  related_entity_id: string;
  status: string;
  classification: string;
  created_at: string;
};

export type CommsMessage = {
  id: string;
  conversation_id: string;
  body: string;
  status: string;
  classification: string;
  requires_approval: boolean;
  approved_by_actor_id: string | null;
  sent_at: string | null;
  revision_number: number;
  created_at: string;
};

export type Questionnaire = {
  id: string;
  code: string;
  title: string;
  status: string;
};

export type QuestionnaireVersion = {
  id: string;
  questionnaire_id: string;
  version_number: number;
  status: string;
  questions_json: Array<{
    key: string;
    text: string;
    mandatory: boolean;
    answer_type: string;
  }>;
};

export type CompletenessScore = {
  id: string;
  percentage: string | number;
  meets_threshold: boolean;
  mandatory_total: number;
  covered_count: number;
  gap_question_keys: string[];
};

export type RequirementsBrief = {
  id: string;
  title: string;
  summary: string;
  status: string;
  version_number: number;
  approved_by_actor_id: string | null;
};

export type Ticket = {
  id: string;
  project_id: string;
  phase_id: string | null;
  code: string;
  title: string;
  description: string | null;
  status: string;
  priority: string;
  owner_actor_id: string | null;
  queue_code: string | null;
  estimate_points: string | number | null;
  acceptance_criteria: string | null;
  definition_of_done: string | null;
  version: number;
  reopen_reason: string | null;
  created_at: string;
};

export type TicketCheck = {
  id: string;
  check_code: string;
  label: string;
  is_required: boolean;
  is_satisfied: boolean;
};

export type TicketEvidence = {
  id: string;
  evidence_type: string;
  title: string;
  created_at: string;
};

export async function createConversation(
  session: SessionState,
  body: {
    subject: string;
    related_entity_type: string;
    related_entity_id: string;
    channel?: string;
    classification?: string;
    project_id?: string;
  },
): Promise<Conversation> {
  const response = await fetch(`${apiBase()}/api/v1/comms/conversations`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Conversation>(response);
}

export async function createCommsMessage(
  session: SessionState,
  body: { conversation_id: string; body: string; classification?: string },
): Promise<CommsMessage> {
  const response = await fetch(`${apiBase()}/api/v1/comms/messages`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<CommsMessage>(response);
}

export async function listConversationMessages(
  session: SessionState,
  conversationId: string,
): Promise<CommsMessage[]> {
  const response = await fetch(
    `${apiBase()}/api/v1/comms/conversations/${conversationId}/messages`,
    { headers: headers(session), cache: "no-store" },
  );
  return parse<CommsMessage[]>(response);
}

export async function addMessageRecipient(
  session: SessionState,
  body: { message_id: string; address: string; role?: string },
): Promise<{ id: string }> {
  const response = await fetch(`${apiBase()}/api/v1/comms/recipients`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<{ id: string }>(response);
}

export async function approveCommsMessage(
  session: SessionState,
  messageId: string,
): Promise<CommsMessage> {
  const response = await fetch(`${apiBase()}/api/v1/comms/messages/${messageId}/approve`, {
    method: "POST",
    headers: headers(session),
  });
  return parse<CommsMessage>(response);
}

export async function sendCommsMessage(
  session: SessionState,
  messageId: string,
): Promise<CommsMessage> {
  const response = await fetch(`${apiBase()}/api/v1/comms/messages/${messageId}/send`, {
    method: "POST",
    headers: headers(session),
  });
  return parse<CommsMessage>(response);
}

export async function createQuestionnaire(
  session: SessionState,
  body: { code: string; title: string },
): Promise<Questionnaire> {
  const response = await fetch(`${apiBase()}/api/v1/requirements/questionnaires`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Questionnaire>(response);
}

export async function createQuestionnaireVersion(
  session: SessionState,
  body: {
    questionnaire_id: string;
    questions: Array<{
      key: string;
      text: string;
      mandatory?: boolean;
      answer_type?: string;
    }>;
  },
): Promise<QuestionnaireVersion> {
  const response = await fetch(`${apiBase()}/api/v1/requirements/questionnaire-versions`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<QuestionnaireVersion>(response);
}

export async function publishQuestionnaireVersion(
  session: SessionState,
  versionId: string,
): Promise<QuestionnaireVersion> {
  const response = await fetch(
    `${apiBase()}/api/v1/requirements/questionnaire-versions/${versionId}/publish`,
    { method: "POST", headers: headers(session) },
  );
  return parse<QuestionnaireVersion>(response);
}

export async function upsertRequirementAnswer(
  session: SessionState,
  body: {
    questionnaire_version_id: string;
    related_entity_type: string;
    related_entity_id: string;
    question_key: string;
    answer_text?: string;
    project_id?: string;
  },
): Promise<{ id: string }> {
  const response = await fetch(`${apiBase()}/api/v1/requirements/answers`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<{ id: string }>(response);
}

export async function computeCompleteness(
  session: SessionState,
  body: {
    questionnaire_version_id: string;
    related_entity_type: string;
    related_entity_id: string;
  },
): Promise<CompletenessScore> {
  const response = await fetch(`${apiBase()}/api/v1/requirements/completeness-scores`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<CompletenessScore>(response);
}

export async function createClarification(
  session: SessionState,
  body: {
    questionnaire_version_id: string;
    related_entity_type: string;
    related_entity_id: string;
    question_key: string;
    question_text: string;
    owner_actor_id: string;
  },
): Promise<{ id: string }> {
  const response = await fetch(`${apiBase()}/api/v1/requirements/clarifications`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<{ id: string }>(response);
}

export async function createRequirementsBrief(
  session: SessionState,
  body: {
    related_entity_type: string;
    related_entity_id: string;
    title: string;
    summary: string;
    questionnaire_version_id?: string;
    completeness_score_id?: string;
    project_id?: string;
  },
): Promise<RequirementsBrief> {
  const response = await fetch(`${apiBase()}/api/v1/requirements/briefs`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<RequirementsBrief>(response);
}

export async function approveRequirementsBrief(
  session: SessionState,
  briefId: string,
): Promise<RequirementsBrief> {
  const response = await fetch(
    `${apiBase()}/api/v1/requirements/briefs/${briefId}/approve`,
    { method: "POST", headers: headers(session) },
  );
  return parse<RequirementsBrief>(response);
}

export async function listRequirementsBriefs(
  session: SessionState,
  relatedEntityType: string,
  relatedEntityId: string,
): Promise<RequirementsBrief[]> {
  const query = new URLSearchParams({
    related_entity_type: relatedEntityType,
    related_entity_id: relatedEntityId,
  });
  const response = await fetch(`${apiBase()}/api/v1/requirements/briefs?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<RequirementsBrief[]>(response);
}

export async function createTicket(
  session: SessionState,
  body: {
    project_id: string;
    code: string;
    title: string;
    description?: string;
    ticket_type?: string;
    priority?: string;
    phase_id?: string;
    owner_actor_id?: string;
    queue_code?: string;
    estimate_points?: string;
    acceptance_criteria?: string;
    definition_of_done?: string;
    requirement_id?: string;
  },
): Promise<Ticket> {
  const response = await fetch(`${apiBase()}/api/v1/tickets`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Ticket>(response);
}

export async function listTickets(
  session: SessionState,
  projectId: string,
): Promise<Ticket[]> {
  const response = await fetch(`${apiBase()}/api/v1/tickets/projects/${projectId}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<Ticket[]>(response);
}

export async function updateTicket(
  session: SessionState,
  ticketId: string,
  body: {
    title?: string;
    description?: string;
    priority?: string;
    phase_id?: string;
    owner_actor_id?: string;
    queue_code?: string;
    estimate_points?: string;
    acceptance_criteria?: string;
    definition_of_done?: string;
    expected_version: number;
  },
): Promise<Ticket> {
  const response = await fetch(`${apiBase()}/api/v1/tickets/${ticketId}`, {
    method: "PATCH",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Ticket>(response);
}

export async function transitionTicket(
  session: SessionState,
  ticketId: string,
  body: {
    next_status: string;
    reason?: string;
    blocked_reason?: string;
    expected_version: number;
  },
): Promise<Ticket> {
  const response = await fetch(`${apiBase()}/api/v1/tickets/${ticketId}/transitions`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Ticket>(response);
}

export async function reopenTicket(
  session: SessionState,
  ticketId: string,
  body: {
    reason: string;
    evidence_id: string;
    next_status?: string;
    expected_version: number;
  },
): Promise<Ticket> {
  const response = await fetch(`${apiBase()}/api/v1/tickets/${ticketId}/reopen`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Ticket>(response);
}

export async function linkTicketRequirement(
  session: SessionState,
  body: { ticket_id: string; requirement_id: string },
): Promise<{ id: string }> {
  const response = await fetch(`${apiBase()}/api/v1/tickets/requirement-links`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<{ id: string }>(response);
}

export async function addTicketEvidence(
  session: SessionState,
  body: {
    ticket_id: string;
    evidence_type: string;
    title: string;
    summary?: string;
  },
): Promise<TicketEvidence> {
  const response = await fetch(`${apiBase()}/api/v1/tickets/evidence`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<TicketEvidence>(response);
}

export async function listReadinessChecks(
  session: SessionState,
  ticketId: string,
): Promise<TicketCheck[]> {
  const response = await fetch(
    `${apiBase()}/api/v1/tickets/${ticketId}/readiness-checks`,
    { headers: headers(session), cache: "no-store" },
  );
  return parse<TicketCheck[]>(response);
}

export async function satisfyReadinessCheck(
  session: SessionState,
  checkId: string,
  notes?: string,
): Promise<TicketCheck> {
  const response = await fetch(
    `${apiBase()}/api/v1/tickets/readiness-checks/${checkId}/satisfy`,
    {
      method: "POST",
      headers: headers(session),
      body: JSON.stringify({ notes }),
    },
  );
  return parse<TicketCheck>(response);
}

export async function listDoneChecks(
  session: SessionState,
  ticketId: string,
): Promise<TicketCheck[]> {
  const response = await fetch(`${apiBase()}/api/v1/tickets/${ticketId}/done-checks`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<TicketCheck[]>(response);
}

export async function satisfyDoneCheck(
  session: SessionState,
  checkId: string,
  notes?: string,
): Promise<TicketCheck> {
  const response = await fetch(
    `${apiBase()}/api/v1/tickets/done-checks/${checkId}/satisfy`,
    {
      method: "POST",
      headers: headers(session),
      body: JSON.stringify({ notes }),
    },
  );
  return parse<TicketCheck>(response);
}
