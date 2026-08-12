import type { ActorKind, GovVariant } from "@/lib/roles";
import { newId } from "@/lib/id";

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

export type ListPage<T> = {
  items: T[];
  page: PageMeta;
};

export const EMPTY_PAGE_META: PageMeta = {
  limit: 20,
  offset: 0,
  total: 0,
  has_more: false,
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
  // Browser default: same-origin Next rewrite → FastAPI (avoids CORS).
  // Opt into cross-origin only with NEXT_PUBLIC_API_USE_DIRECT=true.
  if (typeof window !== "undefined") {
    const useDirect = process.env.NEXT_PUBLIC_API_USE_DIRECT === "true";
    if (!useDirect) {
      return "";
    }
  }
  const configured = process.env.NEXT_PUBLIC_API_BASE_URL?.trim();
  if (configured) {
    return configured.replace(/\/$/, "");
  }
  // Server components / SSR (or explicit browser direct mode).
  return (
    process.env.MASMS_API_ORIGIN?.replace(/\/$/, "") ||
    process.env.NEXT_PUBLIC_API_ORIGIN?.replace(/\/$/, "") ||
    "http://127.0.0.1:8000"
  );
}

function headers(session: SessionState): HeadersInit {
  return {
    "Content-Type": "application/json",
    "X-Organization-Id": session.organizationId,
    "X-Actor-Id": session.actorId,
    "X-Actor-Kind": session.actorKind,
    "X-Correlation-Id": newId(),
    "X-Actor-Name": `web:${session.variant}`,
  };
}

async function apiFetch(input: string, init?: RequestInit): Promise<Response> {
  try {
    return await fetch(input, init);
  } catch {
    throw new ApiError(0, {
      code: "network_error",
      message:
        "Cannot reach the MASMS API. Ensure uvicorn is running on port 8000, then refresh.",
    });
  }
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
  const response = await apiFetch(`${apiBase()}/api/v1/governance/baselines?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<BaselinePage>(response);
}

export async function getBaseline(session: SessionState, id: string): Promise<Baseline> {
  const response = await apiFetch(`${apiBase()}/api/v1/governance/baselines/${id}`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/governance/baselines`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/governance/baselines/${id}`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/governance/baselines/${id}/transitions`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/governance/baselines/${id}/history`, {
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

export async function listQueries(
  session: SessionState,
  params: {
    status?: string;
    sla_status?: string;
    q?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<ListPage<ClientQuery>> {
  const query = new URLSearchParams();
  if (params.status) query.set("status", params.status);
  if (params.sla_status) query.set("sla_status", params.sla_status);
  if (params.q) query.set("q", params.q);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/queries?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<ClientQuery>>(response);
}

export async function getQuery(
  session: SessionState,
  queryId: string,
): Promise<ClientQuery> {
  const response = await apiFetch(`${apiBase()}/api/v1/queries/${queryId}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ClientQuery>(response);
}

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
  project_id?: string | null;
  created_at?: string;
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
  params: { q?: string; status?: string; limit?: number; offset?: number } = {},
): Promise<ClientPage> {
  const query = new URLSearchParams();
  if (params.q) query.set("q", params.q);
  if (params.status) query.set("status", params.status);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/clients?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ClientPage>(response);
}

export async function createClient(
  session: SessionState,
  body: { code: string; legal_name: string; trading_name?: string; industry?: string },
): Promise<Client> {
  const response = await apiFetch(`${apiBase()}/api/v1/clients`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/queries/sources`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/queries`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/queries/${queryId}/transitions`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<ClientQuery>(response);
}

export async function listProjects(
  session: SessionState,
  params: {
    status?: string;
    q?: string;
    client_id?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<ListPage<Project>> {
  const query = new URLSearchParams();
  if (params.status) query.set("status", params.status);
  if (params.q) query.set("q", params.q);
  if (params.client_id) query.set("client_id", params.client_id);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/projects?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<Project>>(response);
}

export async function createProject(
  session: SessionState,
  body: { code: string; title: string; client_id?: string },
): Promise<Project> {
  const response = await apiFetch(`${apiBase()}/api/v1/projects`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/projects/requirements`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/projects/${projectId}/requirements`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/projects/requirement-versions`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/projects/acceptance-criteria`, {
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
  const response = await apiFetch(
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
  const response = await apiFetch(`${apiBase()}/api/v1/projects/srs-baselines`, {
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
  const response = await apiFetch(
    `${apiBase()}/api/v1/projects/srs-baselines/${baselineId}/approve`,
    { method: "POST", headers: headers(session) },
  );
  return parse<SrsBaseline>(response);
}

export async function listDocuments(
  session: SessionState,
  params: {
    status?: string;
    q?: string;
    project_id?: string;
    classification?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<ListPage<DocumentRecord>> {
  const query = new URLSearchParams();
  if (params.status) query.set("status", params.status);
  if (params.q) query.set("q", params.q);
  if (params.project_id) query.set("project_id", params.project_id);
  if (params.classification) query.set("classification", params.classification);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/documents?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<DocumentRecord>>(response);
}

export async function createDocument(
  session: SessionState,
  body: { title: string; classification?: string; project_id?: string },
): Promise<DocumentRecord> {
  const response = await apiFetch(`${apiBase()}/api/v1/documents`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/documents/versions`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/documents/scan-results`, {
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
  const response = await apiFetch(
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
  const response = await apiFetch(`${apiBase()}/api/v1/roadmap/phases`, {
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
  const response = await apiFetch(
    `${apiBase()}/api/v1/roadmap/projects/${projectId}/phases`,
    { headers: headers(session), cache: "no-store" },
  );
  return parse<Phase[]>(response);
}

export async function listMilestones(
  session: SessionState,
  projectId: string,
  params: { phase_id?: string } = {},
): Promise<Milestone[]> {
  const query = new URLSearchParams();
  if (params.phase_id) query.set("phase_id", params.phase_id);
  const qs = query.toString();
  const response = await apiFetch(
    `${apiBase()}/api/v1/roadmap/projects/${projectId}/milestones${qs ? `?${qs}` : ""}`,
    { headers: headers(session), cache: "no-store" },
  );
  return parse<Milestone[]>(response);
}

export async function completePhase(
  session: SessionState,
  phaseId: string,
): Promise<Phase> {
  const response = await apiFetch(`${apiBase()}/api/v1/roadmap/phases/${phaseId}/complete`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/roadmap/milestones`, {
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
  const response = await apiFetch(
    `${apiBase()}/api/v1/roadmap/milestones/${milestoneId}/approve`,
    { method: "POST", headers: headers(session) },
  );
  return parse<Milestone>(response);
}

export async function completeMilestone(
  session: SessionState,
  milestoneId: string,
): Promise<Milestone> {
  const response = await apiFetch(
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
  created_at?: string;
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
  published_at?: string | null;
  created_at?: string;
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
  related_entity_type?: string;
  related_entity_id?: string;
  created_at?: string;
};

export type RequirementAnswer = {
  id: string;
  question_key: string;
  answer_text: string | null;
  questionnaire_version_id: string;
  related_entity_type: string;
  related_entity_id: string;
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

export async function listConversations(
  session: SessionState,
  params: {
    status?: string;
    q?: string;
    project_id?: string;
    classification?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<ListPage<Conversation>> {
  const query = new URLSearchParams();
  if (params.status) query.set("status", params.status);
  if (params.q) query.set("q", params.q);
  if (params.project_id) query.set("project_id", params.project_id);
  if (params.classification) query.set("classification", params.classification);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/comms/conversations?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<Conversation>>(response);
}

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
  const response = await apiFetch(`${apiBase()}/api/v1/comms/conversations`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/comms/messages`, {
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
  const response = await apiFetch(
    `${apiBase()}/api/v1/comms/conversations/${conversationId}/messages`,
    { headers: headers(session), cache: "no-store" },
  );
  return parse<CommsMessage[]>(response);
}

export async function addMessageRecipient(
  session: SessionState,
  body: { message_id: string; address: string; role?: string },
): Promise<{ id: string }> {
  const response = await apiFetch(`${apiBase()}/api/v1/comms/recipients`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/comms/messages/${messageId}/approve`, {
    method: "POST",
    headers: headers(session),
  });
  return parse<CommsMessage>(response);
}

export async function sendCommsMessage(
  session: SessionState,
  messageId: string,
): Promise<CommsMessage> {
  const response = await apiFetch(`${apiBase()}/api/v1/comms/messages/${messageId}/send`, {
    method: "POST",
    headers: headers(session),
  });
  return parse<CommsMessage>(response);
}

export async function listQuestionnaires(
  session: SessionState,
  params: {
    status?: string;
    q?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<ListPage<Questionnaire>> {
  const query = new URLSearchParams();
  if (params.status) query.set("status", params.status);
  if (params.q) query.set("q", params.q);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/requirements/questionnaires?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<Questionnaire>>(response);
}

export async function getPublishedQuestionnaireVersion(
  session: SessionState,
  questionnaireId: string,
): Promise<QuestionnaireVersion> {
  const response = await apiFetch(
    `${apiBase()}/api/v1/requirements/questionnaires/${questionnaireId}/published-version`,
    { headers: headers(session), cache: "no-store" },
  );
  return parse<QuestionnaireVersion>(response);
}

export async function listRequirementAnswers(
  session: SessionState,
  params: {
    questionnaire_version_id: string;
    related_entity_type: string;
    related_entity_id: string;
  },
): Promise<RequirementAnswer[]> {
  const query = new URLSearchParams({
    questionnaire_version_id: params.questionnaire_version_id,
    related_entity_type: params.related_entity_type,
    related_entity_id: params.related_entity_id,
  });
  const response = await apiFetch(`${apiBase()}/api/v1/requirements/answers?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<RequirementAnswer[]>(response);
}

export async function createQuestionnaire(
  session: SessionState,
  body: { code: string; title: string },
): Promise<Questionnaire> {
  const response = await apiFetch(`${apiBase()}/api/v1/requirements/questionnaires`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/requirements/questionnaire-versions`, {
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
  const response = await apiFetch(
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
  const response = await apiFetch(`${apiBase()}/api/v1/requirements/answers`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/requirements/completeness-scores`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/requirements/clarifications`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/requirements/briefs`, {
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
  const response = await apiFetch(
    `${apiBase()}/api/v1/requirements/briefs/${briefId}/approve`,
    { method: "POST", headers: headers(session) },
  );
  return parse<RequirementsBrief>(response);
}

export async function listRequirementsBriefs(
  session: SessionState,
  params: {
    related_entity_type?: string;
    related_entity_id?: string;
    status?: string;
    q?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<ListPage<RequirementsBrief>> {
  const query = new URLSearchParams();
  if (params.related_entity_type) query.set("related_entity_type", params.related_entity_type);
  if (params.related_entity_id) query.set("related_entity_id", params.related_entity_id);
  if (params.status) query.set("status", params.status);
  if (params.q) query.set("q", params.q);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/requirements/briefs?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<RequirementsBrief>>(response);
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
  const response = await apiFetch(`${apiBase()}/api/v1/tickets`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Ticket>(response);
}

export async function listTickets(
  session: SessionState,
  projectId: string,
  params: {
    status?: string;
    q?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<ListPage<Ticket>> {
  const query = new URLSearchParams();
  if (params.status) query.set("status", params.status);
  if (params.q) query.set("q", params.q);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(
    `${apiBase()}/api/v1/tickets/projects/${projectId}?${query}`,
    {
      headers: headers(session),
      cache: "no-store",
    },
  );
  return parse<ListPage<Ticket>>(response);
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
  const response = await apiFetch(`${apiBase()}/api/v1/tickets/${ticketId}`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/tickets/${ticketId}/transitions`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/tickets/${ticketId}/reopen`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/tickets/requirement-links`, {
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
  const response = await apiFetch(`${apiBase()}/api/v1/tickets/evidence`, {
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
  const response = await apiFetch(
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
  const response = await apiFetch(
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
  const response = await apiFetch(`${apiBase()}/api/v1/tickets/${ticketId}/done-checks`, {
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
  const response = await apiFetch(
    `${apiBase()}/api/v1/tickets/done-checks/${checkId}/satisfy`,
    {
      method: "POST",
      headers: headers(session),
      body: JSON.stringify({ notes }),
    },
  );
  return parse<TicketCheck>(response);
}

/* ---- Approvals (MOD-330) / Follow-ups (MOD-340) ---- */

export type ApprovalRequest = {
  id: string;
  action_code: string;
  title: string;
  target_entity_type: string;
  target_entity_id: string;
  target_version: number;
  status: string;
  current_step_order: number;
  version: number;
  project_id: string | null;
  owner_actor_id: string;
  created_at: string;
  decided_at: string | null;
};

export type ApprovalStep = {
  id: string;
  approval_id: string;
  step_order: number;
  role_code: string;
  status: string;
  assignee_actor_id: string | null;
};

export type ApprovalDecision = {
  id: string;
  approval_id: string;
  decision: string;
  actor_id: string;
  reason: string | null;
  decided_at: string;
};

export type FollowUp = {
  id: string;
  title: string;
  direction: string;
  source_entity_type: string;
  source_entity_id: string;
  recipient_actor_id: string;
  owner_actor_id: string;
  required_response: string;
  closure_condition: string;
  status: string;
  due_at: string;
  sla_paused: boolean;
  project_id: string | null;
  reminder_offset_hours: number;
  escalation_after_hours: number;
  created_at: string;
  closed_at: string | null;
};

export type FollowUpReminder = {
  id: string;
  scheduled_for: string;
  status: string;
  channel: string;
  triggered_at: string | null;
};

export type FollowUpEscalation = {
  id: string;
  escalate_to_role_code: string;
  reason: string;
  status: string;
  triggered_at: string;
};

export async function listApprovals(
  session: SessionState,
  params: {
    status?: string;
    action_code?: string;
    q?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<ListPage<ApprovalRequest>> {
  const query = new URLSearchParams();
  if (params.status) query.set("status", params.status);
  if (params.action_code) query.set("action_code", params.action_code);
  if (params.q) query.set("q", params.q);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/approvals?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<ApprovalRequest>>(response);
}

export async function getApproval(
  session: SessionState,
  approvalId: string,
): Promise<ApprovalRequest> {
  const response = await apiFetch(`${apiBase()}/api/v1/approvals/${approvalId}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ApprovalRequest>(response);
}

export async function createApproval(
  session: SessionState,
  body: {
    action_code: string;
    title: string;
    target_entity_type: string;
    target_entity_id: string;
    target_version: number;
    project_id?: string;
    steps?: Array<{ role_code: string; order?: number; assignee_actor_id?: string }>;
  },
): Promise<ApprovalRequest> {
  const response = await apiFetch(`${apiBase()}/api/v1/approvals`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<ApprovalRequest>(response);
}

export async function listApprovalSteps(
  session: SessionState,
  approvalId: string,
): Promise<ApprovalStep[]> {
  const response = await apiFetch(`${apiBase()}/api/v1/approvals/${approvalId}/steps`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ApprovalStep[]>(response);
}

export async function listApprovalDecisions(
  session: SessionState,
  approvalId: string,
): Promise<ApprovalDecision[]> {
  const response = await apiFetch(`${apiBase()}/api/v1/approvals/${approvalId}/decisions`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ApprovalDecision[]>(response);
}

export async function decideApproval(
  session: SessionState,
  approvalId: string,
  body: { decision: "approve" | "reject" | "withdraw"; reason?: string; expected_version?: number },
): Promise<ApprovalDecision> {
  const response = await apiFetch(`${apiBase()}/api/v1/approvals/${approvalId}/decisions`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<ApprovalDecision>(response);
}

export async function addApprovalEvidence(
  session: SessionState,
  approvalId: string,
  body: { evidence_ref: string; evidence_type?: string; note?: string },
): Promise<{ id: string }> {
  const response = await apiFetch(`${apiBase()}/api/v1/approvals/${approvalId}/evidence`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<{ id: string }>(response);
}

export async function listFollowUps(
  session: SessionState,
  params: {
    status?: string;
    q?: string;
    project_id?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<ListPage<FollowUp>> {
  const query = new URLSearchParams();
  if (params.status) query.set("status", params.status);
  if (params.q) query.set("q", params.q);
  if (params.project_id) query.set("project_id", params.project_id);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/follow-ups?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<FollowUp>>(response);
}

/** Open follow-ups only (API default status=open). Prefer `listFollowUps` for desks. */
export async function listOpenFollowUps(
  session: SessionState,
  params: { limit?: number; offset?: number; q?: string; project_id?: string } = {},
): Promise<ListPage<FollowUp>> {
  return listFollowUps(session, { status: "open", ...params });
}

export async function createFollowUp(
  session: SessionState,
  body: {
    title: string;
    source_entity_type: string;
    source_entity_id: string;
    recipient_actor_id: string;
    owner_actor_id: string;
    required_response: string;
    closure_condition: string;
    due_offset_hours?: number;
    project_id?: string;
    rule_version_id?: string;
    reminder_offset_hours?: number;
    escalation_after_hours?: number;
  },
): Promise<FollowUp> {
  const response = await apiFetch(`${apiBase()}/api/v1/follow-ups`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<FollowUp>(response);
}

export async function addFollowUpClosureEvidence(
  session: SessionState,
  followUpId: string,
  body: { evidence_ref: string; evidence_type?: string; note?: string },
): Promise<{ id: string }> {
  const response = await apiFetch(`${apiBase()}/api/v1/follow-ups/${followUpId}/closure-evidence`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<{ id: string }>(response);
}

export async function closeFollowUp(
  session: SessionState,
  followUpId: string,
): Promise<FollowUp> {
  const response = await apiFetch(`${apiBase()}/api/v1/follow-ups/${followUpId}/close`, {
    method: "POST",
    headers: headers(session),
  });
  return parse<FollowUp>(response);
}

export async function processFollowUpOverdue(
  session: SessionState,
  followUpId: string,
): Promise<{ followup_id: string; reminders_created: number; escalations_created: number }> {
  const response = await apiFetch(`${apiBase()}/api/v1/follow-ups/${followUpId}/process-overdue`, {
    method: "POST",
    headers: headers(session),
  });
  return parse(response);
}

export async function listFollowUpReminders(
  session: SessionState,
  followUpId: string,
): Promise<FollowUpReminder[]> {
  const response = await apiFetch(`${apiBase()}/api/v1/follow-ups/${followUpId}/reminders`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<FollowUpReminder[]>(response);
}

export async function listFollowUpEscalations(
  session: SessionState,
  followUpId: string,
): Promise<FollowUpEscalation[]> {
  const response = await apiFetch(`${apiBase()}/api/v1/follow-ups/${followUpId}/escalations`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<FollowUpEscalation[]>(response);
}

export const ORCHESTRATOR_WORKFLOW_CODES = [
  "query_intake",
  "requirement_clarification",
  "project_handover",
  "assignment_ack",
  "blocker_resolution",
  "qa_rejection_loop",
  "client_status_report",
  "change_request_flow",
  "deployment_approval",
  "project_closure",
  "approval_gate_wait",
  "followup_escalation",
] as const;

export type WorkflowInstance = {
  id: string;
  organization_id: string;
  project_id: string | null;
  workflow_code: string;
  workflow_version_id: string;
  related_entity_type: string;
  related_entity_id: string;
  status: string;
  temporal_run_id: string | null;
  temporal_workflow_id: string | null;
  owner_actor_id: string;
  correlation_id: string;
  version: number;
  created_at: string;
  updated_at: string;
  closed_at: string | null;
};

export async function listWorkflowInstances(
  session: SessionState,
  params: {
    status?: string;
    q?: string;
    workflow_code?: string;
    project_id?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<ListPage<WorkflowInstance>> {
  const query = new URLSearchParams();
  if (params.status) query.set("status", params.status);
  if (params.q) query.set("q", params.q);
  if (params.workflow_code) query.set("workflow_code", params.workflow_code);
  if (params.project_id) query.set("project_id", params.project_id);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/orchestrator/instances?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<WorkflowInstance>>(response);
}

export async function startWorkflowInstance(
  session: SessionState,
  body: {
    workflow_code: string;
    related_entity_type: string;
    related_entity_id: string;
    project_id?: string;
    owner_actor_id?: string;
    input_json?: Record<string, unknown>;
    workflow_version_id?: string;
  },
): Promise<WorkflowInstance> {
  const response = await apiFetch(`${apiBase()}/api/v1/orchestrator/instances`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<WorkflowInstance>(response);
}

export const AGENT_RUNTIME_CODES = [
  "query_intake_agent",
  "requirements_clarifier",
  "roadmap_planner",
  "ticket_triage_agent",
  "qa_review_assistant",
  "status_report_drafter",
] as const;

export type AgentDefinition = {
  id: string;
  organization_id: string;
  code: string;
  title: string;
  description: string | null;
  status: string;
  department_code: string;
  authority_level: string;
  supervisor_actor_id: string | null;
  created_at: string;
};

export type AgentRun = {
  id: string;
  organization_id: string;
  project_id: string | null;
  definition_id: string;
  agent_code: string;
  prompt_version_id: string;
  related_entity_type: string;
  related_entity_id: string;
  status: string;
  langgraph_run_id: string | null;
  model_name: string;
  prompt_version_number: number;
  confidence: number | null;
  review_required: boolean;
  owner_actor_id: string;
  version: number;
  created_at: string;
  updated_at: string;
};

export async function listAgentDefinitions(session: SessionState): Promise<AgentDefinition[]> {
  const response = await apiFetch(`${apiBase()}/api/v1/agent-runtime/definitions`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<AgentDefinition[]>(response);
}

export async function listAgentRuns(
  session: SessionState,
  params: {
    status?: string;
    q?: string;
    agent_code?: string;
    project_id?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<ListPage<AgentRun>> {
  const query = new URLSearchParams();
  if (params.status) query.set("status", params.status);
  if (params.q) query.set("q", params.q);
  if (params.agent_code) query.set("agent_code", params.agent_code);
  if (params.project_id) query.set("project_id", params.project_id);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/agent-runtime/runs?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<AgentRun>>(response);
}

export async function startAgentRun(
  session: SessionState,
  body: {
    agent_code: string;
    related_entity_type: string;
    related_entity_id: string;
    project_id?: string;
    owner_actor_id?: string;
    input_json?: Record<string, unknown>;
    prompt_version_id?: string;
    idempotency_key?: string;
  },
): Promise<AgentRun> {
  const response = await apiFetch(`${apiBase()}/api/v1/agent-runtime/runs`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<AgentRun>(response);
}

export type KnowledgeItem = {
  id: string;
  organization_id: string;
  project_id: string | null;
  code: string;
  title: string;
  description: string | null;
  status: string;
  classification: string;
  owner_actor_id: string;
  created_at: string;
  updated_at: string;
};

export type KnowledgeVersion = {
  id: string;
  item_id: string;
  version_number: number;
  status: string;
  body_text: string;
  version: number;
};

export type KnowledgeCitation = {
  item_id: string;
  item_code: string;
  item_title: string;
  version_id: string;
  version_number: number;
  chunk_id: string;
  chunk_index: number;
  content_text: string;
  score: number;
  project_id: string | null;
  source_citation: string;
};

export async function listKnowledgeItems(
  session: SessionState,
  params: {
    status?: string;
    project_id?: string;
    q?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<ListPage<KnowledgeItem>> {
  const query = new URLSearchParams();
  if (params.status) query.set("status", params.status);
  if (params.project_id) query.set("project_id", params.project_id);
  if (params.q) query.set("q", params.q);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/knowledge/items?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<KnowledgeItem>>(response);
}

export async function createKnowledgeItem(
  session: SessionState,
  body: {
    code: string;
    title: string;
    description?: string;
    project_id?: string;
    classification?: string;
  },
): Promise<KnowledgeItem> {
  const response = await apiFetch(`${apiBase()}/api/v1/knowledge/items`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<KnowledgeItem>(response);
}

export async function createKnowledgeVersion(
  session: SessionState,
  itemId: string,
  body: { body_text: string; change_summary?: string },
): Promise<KnowledgeVersion> {
  const response = await apiFetch(`${apiBase()}/api/v1/knowledge/items/${itemId}/versions`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<KnowledgeVersion>(response);
}

export async function activateKnowledgeVersion(
  session: SessionState,
  versionId: string,
  expectedVersion?: number,
): Promise<KnowledgeVersion> {
  const response = await apiFetch(`${apiBase()}/api/v1/knowledge/versions/${versionId}/activate`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify({ expected_version: expectedVersion }),
  });
  return parse<KnowledgeVersion>(response);
}

export async function searchKnowledge(
  session: SessionState,
  body: { query: string; project_id?: string; limit?: number },
): Promise<{ query: string; items: KnowledgeCitation[]; stub: boolean }> {
  const response = await apiFetch(`${apiBase()}/api/v1/knowledge/search`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<{ query: string; items: KnowledgeCitation[]; stub: boolean }>(response);
}

export type TestCase = {
  id: string;
  organization_id: string;
  project_id: string | null;
  code: string;
  title: string;
  description: string | null;
  case_type: string;
  priority: string;
  status: string;
  preconditions: string | null;
  expected_result: string | null;
  owner_actor_id: string;
  version: number;
  created_at: string;
  updated_at: string;
};

export type TestRun = {
  id: string;
  organization_id: string;
  project_id: string | null;
  case_id: string;
  plan_id: string | null;
  status: string;
  environment_code: string;
  build_ref: string | null;
  result_summary: string | null;
  executed_by_actor_id: string;
  version: number;
  started_at: string | null;
  finished_at: string | null;
  created_at: string;
  updated_at: string;
};

export type CoverageSummary = {
  must_have_total: number;
  must_have_covered: number;
  permission_negative_cases: number;
  uncovered_must_have_requirement_ids: string[];
};

export async function listTestCases(
  session: SessionState,
  params: {
    status?: string;
    case_type?: string;
    project_id?: string;
    q?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<ListPage<TestCase>> {
  const query = new URLSearchParams();
  if (params.status) query.set("status", params.status);
  if (params.case_type) query.set("case_type", params.case_type);
  if (params.project_id) query.set("project_id", params.project_id);
  if (params.q) query.set("q", params.q);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/test-cases/cases?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<TestCase>>(response);
}

export async function createTestCase(
  session: SessionState,
  body: {
    code: string;
    title: string;
    description?: string;
    project_id?: string;
    case_type?: string;
    priority?: string;
    preconditions?: string;
    expected_result?: string;
    steps?: { step_number: number; action_text: string; expected_text?: string }[];
  },
): Promise<TestCase> {
  const response = await apiFetch(`${apiBase()}/api/v1/test-cases/cases`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<TestCase>(response);
}

export async function approveTestCase(
  session: SessionState,
  caseId: string,
  expectedVersion?: number,
): Promise<TestCase> {
  const response = await apiFetch(`${apiBase()}/api/v1/test-cases/cases/${caseId}/approve`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify({ expected_version: expectedVersion }),
  });
  return parse<TestCase>(response);
}

export async function linkTestCoverage(
  session: SessionState,
  caseId: string,
  body: {
    requirement_id: string;
    requirement_priority?: string;
    coverage_notes?: string;
  },
): Promise<{ id: string; case_id: string; requirement_id: string }> {
  const response = await apiFetch(`${apiBase()}/api/v1/test-cases/cases/${caseId}/coverage`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<{ id: string; case_id: string; requirement_id: string }>(response);
}

export async function startTestRun(
  session: SessionState,
  body: {
    case_id: string;
    plan_id?: string;
    project_id?: string;
    environment_code?: string;
    build_ref?: string;
  },
): Promise<TestRun> {
  const response = await apiFetch(`${apiBase()}/api/v1/test-cases/runs`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<TestRun>(response);
}

export async function completeTestRun(
  session: SessionState,
  runId: string,
  body: {
    status: string;
    result_summary?: string;
    expected_version?: number;
    evidence_title?: string;
    evidence_body?: string;
  },
): Promise<TestRun> {
  const response = await apiFetch(`${apiBase()}/api/v1/test-cases/runs/${runId}/complete`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<TestRun>(response);
}

export async function summarizeTestCoverage(
  session: SessionState,
  body: { must_have_requirement_ids?: string[] } = {},
): Promise<CoverageSummary> {
  const response = await apiFetch(`${apiBase()}/api/v1/test-cases/coverage/summary`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<CoverageSummary>(response);
}

export type Bug = {
  id: string;
  organization_id: string;
  project_id: string | null;
  code: string;
  title: string;
  description: string | null;
  severity: string;
  status: string;
  blocks_release: boolean;
  rejection_reason: string | null;
  rejection_evidence: string | null;
  reopen_reason: string | null;
  owner_actor_id: string;
  assignee_actor_id: string | null;
  version: number;
  created_at: string;
  updated_at: string;
};

export type ReleaseGate = {
  project_id: string | null;
  release_allowed: boolean;
  blocking_bug_ids: string[];
  blocking_codes: string[];
};

export async function listBugs(
  session: SessionState,
  params: {
    status?: string;
    severity?: string;
    project_id?: string;
    q?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<ListPage<Bug>> {
  const query = new URLSearchParams();
  if (params.status) query.set("status", params.status);
  if (params.severity) query.set("severity", params.severity);
  if (params.project_id) query.set("project_id", params.project_id);
  if (params.q) query.set("q", params.q);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/bugs?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<Bug>>(response);
}

export async function createBug(
  session: SessionState,
  body: {
    code: string;
    title: string;
    description?: string;
    project_id?: string;
    severity?: string;
    blocks_release?: boolean;
    links?: { link_type: string; linked_entity_id: string; notes?: string }[];
  },
): Promise<Bug> {
  const response = await apiFetch(`${apiBase()}/api/v1/bugs`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Bug>(response);
}

export async function rejectBug(
  session: SessionState,
  bugId: string,
  body: { reason: string; evidence: string; expected_version?: number },
): Promise<Bug> {
  const response = await apiFetch(`${apiBase()}/api/v1/bugs/${bugId}/reject`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Bug>(response);
}

export async function reopenBug(
  session: SessionState,
  bugId: string,
  body: { reason: string; expected_version?: number },
): Promise<Bug> {
  const response = await apiFetch(`${apiBase()}/api/v1/bugs/${bugId}/reopen`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Bug>(response);
}

export async function getBugReleaseGate(
  session: SessionState,
  projectId?: string,
): Promise<ReleaseGate> {
  const query = new URLSearchParams();
  if (projectId) query.set("project_id", projectId);
  const suffix = query.toString() ? `?${query}` : "";
  const response = await apiFetch(`${apiBase()}/api/v1/bugs/release-gate${suffix}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ReleaseGate>(response);
}

export type ChangeRequest = {
  id: string;
  organization_id: string;
  project_id: string | null;
  code: string;
  title: string;
  description: string | null;
  change_type: string;
  status: string;
  rationale: string | null;
  decision_evidence: string | null;
  owner_actor_id: string;
  version: number;
  created_at: string;
  updated_at: string;
};

export type DevelopmentGate = {
  change_request_id: string;
  status: string;
  allowed: boolean;
  reason: string;
};

export async function listChangeRequests(
  session: SessionState,
  params: {
    status?: string;
    project_id?: string;
    q?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<ListPage<ChangeRequest>> {
  const query = new URLSearchParams();
  if (params.status) query.set("status", params.status);
  if (params.project_id) query.set("project_id", params.project_id);
  if (params.q) query.set("q", params.q);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/change-control/change-requests?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<ChangeRequest>>(response);
}

export async function createChangeRequest(
  session: SessionState,
  body: {
    code: string;
    title: string;
    description?: string;
    project_id?: string;
    change_type?: string;
    rationale?: string;
  },
): Promise<ChangeRequest> {
  const response = await apiFetch(`${apiBase()}/api/v1/change-control/change-requests`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<ChangeRequest>(response);
}

export async function addChangeImpact(
  session: SessionState,
  crId: string,
  body: {
    summary: string;
    affected_areas?: string[];
    estimated_effort_hours?: number;
    expected_version?: number;
  },
): Promise<{ id: string }> {
  const response = await apiFetch(`${apiBase()}/api/v1/change-control/change-requests/${crId}/impacts`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<{ id: string }>(response);
}

export async function submitChangeRequest(
  session: SessionState,
  crId: string,
  expectedVersion?: number,
): Promise<ChangeRequest> {
  const response = await apiFetch(`${apiBase()}/api/v1/change-control/change-requests/${crId}/submit`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify({ expected_version: expectedVersion }),
  });
  return parse<ChangeRequest>(response);
}

export async function decideChangeRequest(
  session: SessionState,
  crId: string,
  body: {
    decision: string;
    rationale: string;
    evidence?: string;
    expected_version?: number;
  },
): Promise<{ id: string; decision: string }> {
  const response = await apiFetch(
    `${apiBase()}/api/v1/change-control/change-requests/${crId}/approvals`,
    {
      method: "POST",
      headers: headers(session),
      body: JSON.stringify(body),
    },
  );
  return parse<{ id: string; decision: string }>(response);
}

export async function getChangeDevelopmentGate(
  session: SessionState,
  crId: string,
): Promise<DevelopmentGate> {
  const response = await apiFetch(
    `${apiBase()}/api/v1/change-control/change-requests/${crId}/development-gate`,
    {
      headers: headers(session),
      cache: "no-store",
    },
  );
  return parse<DevelopmentGate>(response);
}

export type Release = {
  id: string;
  organization_id: string;
  project_id: string | null;
  code: string;
  title: string;
  description: string | null;
  status: string;
  version_label: string;
  approval_evidence: string | null;
  approved_by_actor_id: string | null;
  approved_at: string | null;
  owner_actor_id: string;
  version: number;
  created_at: string;
  updated_at: string;
};

export async function listReleases(
  session: SessionState,
  params: {
    status?: string;
    project_id?: string;
    q?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<ListPage<Release>> {
  const query = new URLSearchParams();
  if (params.status) query.set("status", params.status);
  if (params.project_id) query.set("project_id", params.project_id);
  if (params.q) query.set("q", params.q);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/releases?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<Release>>(response);
}

export async function createRelease(
  session: SessionState,
  body: {
    code: string;
    title: string;
    description?: string;
    project_id?: string;
    version_label?: string;
    items?: { link_type: string; linked_entity_id: string; notes?: string }[];
  },
): Promise<Release> {
  const response = await apiFetch(`${apiBase()}/api/v1/releases`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Release>(response);
}

export async function submitRelease(
  session: SessionState,
  releaseId: string,
  expectedVersion?: number,
): Promise<Release> {
  const response = await apiFetch(`${apiBase()}/api/v1/releases/${releaseId}/submit`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify({ expected_version: expectedVersion }),
  });
  return parse<Release>(response);
}

export async function approveRelease(
  session: SessionState,
  releaseId: string,
  body: { evidence: string; expected_version?: number },
): Promise<Release> {
  const response = await apiFetch(`${apiBase()}/api/v1/releases/${releaseId}/approve`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Release>(response);
}

export type Notification = {
  id: string;
  organization_id: string;
  project_id: string | null;
  recipient_actor_id: string;
  notification_type: string;
  channel: string;
  title: string;
  body: string;
  related_entity_type: string | null;
  related_entity_id: string | null;
  priority: string;
  status: string;
  scheduled_at: string | null;
  sent_at: string | null;
  delivered_at: string | null;
  read_at: string | null;
  failure_reason: string | null;
  retry_count: number;
  idempotency_key: string | null;
  version: number;
  created_at: string;
  updated_at: string;
};

export type NotificationPreference = {
  id: string;
  organization_id: string;
  actor_id: string;
  channel: string;
  notification_type: string;
  enabled: boolean;
  quiet_hours_start: string | null;
  quiet_hours_end: string | null;
  version: number;
  created_at: string;
  updated_at: string;
};

export async function listNotifications(
  session: SessionState,
  params: {
    status?: string;
    channel?: string;
    recipient_actor_id?: string;
    q?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<ListPage<Notification>> {
  const query = new URLSearchParams();
  if (params.status) query.set("status", params.status);
  if (params.channel) query.set("channel", params.channel);
  if (params.recipient_actor_id) query.set("recipient_actor_id", params.recipient_actor_id);
  if (params.q) query.set("q", params.q);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/notifications?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<Notification>>(response);
}

export async function createNotification(
  session: SessionState,
  body: {
    title: string;
    body: string;
    recipient_actor_id: string;
    notification_type: string;
    channel?: string;
    priority?: string;
    project_id?: string;
    related_entity_type?: string;
    related_entity_id?: string;
    idempotency_key?: string;
  },
): Promise<Notification> {
  const response = await apiFetch(`${apiBase()}/api/v1/notifications`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Notification>(response);
}

export async function markNotificationRead(
  session: SessionState,
  notificationId: string,
  expectedVersion?: number,
): Promise<Notification> {
  const response = await apiFetch(
    `${apiBase()}/api/v1/notifications/${notificationId}/mark-read`,
    {
      method: "POST",
      headers: headers(session),
      body: JSON.stringify({ expected_version: expectedVersion }),
    },
  );
  return parse<Notification>(response);
}

export async function deliverNotification(
  session: SessionState,
  notificationId: string,
  body: { succeed: boolean; error_message?: string },
): Promise<Notification> {
  const response = await apiFetch(
    `${apiBase()}/api/v1/notifications/${notificationId}/deliver`,
    {
      method: "POST",
      headers: headers(session),
      body: JSON.stringify(body),
    },
  );
  return parse<Notification>(response);
}

export async function retryNotification(
  session: SessionState,
  notificationId: string,
): Promise<Notification> {
  const response = await apiFetch(
    `${apiBase()}/api/v1/notifications/${notificationId}/retry`,
    {
      method: "POST",
      headers: headers(session),
    },
  );
  return parse<Notification>(response);
}

export async function listNotificationPreferences(
  session: SessionState,
  actorId?: string,
): Promise<NotificationPreference[]> {
  const query = new URLSearchParams();
  if (actorId) query.set("actor_id", actorId);
  const suffix = query.toString() ? `?${query}` : "";
  const response = await apiFetch(`${apiBase()}/api/v1/notifications/preferences${suffix}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<NotificationPreference[]>(response);
}

export async function upsertNotificationPreference(
  session: SessionState,
  body: {
    actor_id: string;
    channel: string;
    notification_type: string;
    enabled: boolean;
    quiet_hours_start?: string;
    quiet_hours_end?: string;
    expected_version?: number;
  },
): Promise<NotificationPreference> {
  const response = await apiFetch(`${apiBase()}/api/v1/notifications/preferences`, {
    method: "PUT",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<NotificationPreference>(response);
}

/* —— MOD-450 Insights —— */

export type InsightsDashboardSnapshot = {
  id: string;
  organization_id: string;
  scope_key: string;
  project_id: string | null;
  metrics: Record<string, unknown>;
  source_hash: string | null;
  computed_at: string;
  refreshed_at: string;
  is_fresh: boolean;
  version: number;
  created_at: string;
  updated_at: string;
};

export type InsightsSearchDocument = {
  id: string;
  organization_id: string;
  project_id: string | null;
  entity_type: string;
  entity_id: string;
  title: string;
  body_preview: string;
  classification: string;
  indexed_at: string;
  created_at: string;
};

export type InsightsActivityEvent = {
  id: string;
  organization_id: string;
  project_id: string | null;
  actor_id: string;
  event_type: string;
  entity_type: string;
  entity_id: string | null;
  summary: string;
  occurred_at: string;
  created_at: string;
};

export type InsightsSavedFilter = {
  id: string;
  organization_id: string;
  owner_actor_id: string;
  name: string;
  module_key: string;
  filter_json: string;
  is_shared: boolean;
  version: number;
  created_at: string;
  updated_at: string;
};

export type InsightsExport = {
  id: string;
  organization_id: string;
  report_id: string | null;
  export_format: string;
  status: string;
  payload_preview: string | null;
  row_count: number;
  requested_by_actor_id: string;
  completed_at: string | null;
  failure_reason: string | null;
  created_at: string;
  updated_at: string;
};

export async function getInsightsDashboard(
  session: SessionState,
  projectId?: string,
): Promise<InsightsDashboardSnapshot> {
  const query = new URLSearchParams();
  if (projectId) query.set("project_id", projectId);
  const suffix = query.toString() ? `?${query}` : "";
  const response = await apiFetch(`${apiBase()}/api/v1/insights/dashboard${suffix}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<InsightsDashboardSnapshot>(response);
}

export async function refreshInsightsDashboard(
  session: SessionState,
  body: { project_id?: string } = {},
): Promise<InsightsDashboardSnapshot> {
  const response = await apiFetch(`${apiBase()}/api/v1/insights/dashboard/refresh`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<InsightsDashboardSnapshot>(response);
}

export async function globalSearch(
  session: SessionState,
  params: { q: string; limit?: number; offset?: number },
): Promise<ListPage<InsightsSearchDocument>> {
  const query = new URLSearchParams();
  query.set("q", params.q);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/insights/search?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<InsightsSearchDocument>>(response);
}

export async function listInsightsActivity(
  session: SessionState,
  params: { project_id?: string; limit?: number; offset?: number } = {},
): Promise<ListPage<InsightsActivityEvent>> {
  const query = new URLSearchParams();
  if (params.project_id) query.set("project_id", params.project_id);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/insights/activity?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<InsightsActivityEvent>>(response);
}

export async function createSavedFilter(
  session: SessionState,
  body: {
    name: string;
    module_key: string;
    filter_json: string;
    is_shared?: boolean;
  },
): Promise<InsightsSavedFilter> {
  const response = await apiFetch(`${apiBase()}/api/v1/insights/saved-filters`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<InsightsSavedFilter>(response);
}

export async function listSavedFilters(
  session: SessionState,
  params: { limit?: number; offset?: number } = {},
): Promise<ListPage<InsightsSavedFilter>> {
  const query = new URLSearchParams();
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/insights/saved-filters?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<InsightsSavedFilter>>(response);
}

export async function listInsightsExports(
  session: SessionState,
  params: { limit?: number; offset?: number } = {},
): Promise<ListPage<InsightsExport>> {
  const query = new URLSearchParams();
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/insights/exports?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<InsightsExport>>(response);
}

export async function createInsightsExport(
  session: SessionState,
  body: {
    export_format?: string;
    report_id?: string;
    include_dashboard_metrics?: boolean;
  } = {},
): Promise<InsightsExport> {
  const response = await apiFetch(`${apiBase()}/api/v1/insights/exports`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<InsightsExport>(response);
}

export type MustHaveRequirement = {
  id: string;
  organization_id: string;
  project_id: string | null;
  requirement_id: string;
  requirement_code: string;
  title: string;
  created_by_actor_id: string;
  created_at: string;
};

export type TraceabilityCoverage = {
  organization_id: string;
  project_id: string | null;
  total_must_haves: number;
  complete_count: number;
  incomplete_count: number;
  coverage_pct: number;
  release_ready: boolean;
  incomplete_requirement_ids: string[];
};

export type AuditCoverageReport = {
  organization_id: string;
  action_count: number;
  audited_count: number;
  coverage_pct: number;
  complete: boolean;
};

export type EvidenceManifest = {
  id: string;
  organization_id: string;
  project_id: string | null;
  code: string;
  title: string;
  status: string;
  item_count: number;
  checksum: string | null;
  sealed_at: string | null;
  version: number;
  created_by_actor_id: string;
  updated_by_actor_id: string;
  created_at: string;
  updated_at: string;
};

export type EvidenceExport = {
  id: string;
  organization_id: string;
  manifest_id: string;
  export_format: string;
  status: string;
  payload_preview: string | null;
  reconciliation_hash: string | null;
  requested_by_actor_id: string;
  completed_at: string | null;
  failure_reason: string | null;
  created_at: string;
};

export async function registerMustHave(
  session: SessionState,
  body: {
    requirement_id: string;
    requirement_code: string;
    title: string;
    project_id?: string;
  },
): Promise<MustHaveRequirement> {
  const response = await apiFetch(`${apiBase()}/api/v1/traceability/must-haves`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<MustHaveRequirement>(response);
}

export async function listMustHaves(
  session: SessionState,
  params: { project_id?: string; limit?: number; offset?: number } = {},
): Promise<ListPage<MustHaveRequirement>> {
  const query = new URLSearchParams();
  if (params.project_id) query.set("project_id", params.project_id);
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/traceability/must-haves?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<MustHaveRequirement>>(response);
}

export async function createRequirementTicketLink(
  session: SessionState,
  body: { requirement_id: string; ticket_id: string; notes?: string },
): Promise<unknown> {
  const response = await apiFetch(
    `${apiBase()}/api/v1/traceability/links/requirement-tickets`,
    {
      method: "POST",
      headers: headers(session),
      body: JSON.stringify(body),
    },
  );
  return parse(response);
}

export async function getTraceabilityCoverage(
  session: SessionState,
  projectId?: string,
): Promise<TraceabilityCoverage> {
  const query = new URLSearchParams();
  if (projectId) query.set("project_id", projectId);
  const suffix = query.toString() ? `?${query}` : "";
  const response = await apiFetch(`${apiBase()}/api/v1/traceability/coverage${suffix}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<TraceabilityCoverage>(response);
}

export async function getAuditCoverage(
  session: SessionState,
): Promise<AuditCoverageReport> {
  const response = await apiFetch(`${apiBase()}/api/v1/traceability/audit-coverage`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<AuditCoverageReport>(response);
}

export async function createEvidenceManifest(
  session: SessionState,
  body: { code: string; title: string; project_id?: string },
): Promise<EvidenceManifest> {
  const response = await apiFetch(`${apiBase()}/api/v1/traceability/manifests`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<EvidenceManifest>(response);
}

export async function listEvidenceManifests(
  session: SessionState,
  params: { limit?: number; offset?: number } = {},
): Promise<ListPage<EvidenceManifest>> {
  const query = new URLSearchParams();
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/traceability/manifests?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<EvidenceManifest>>(response);
}

export async function addManifestItem(
  session: SessionState,
  manifestId: string,
  body: { item_type: string; item_id: string; label?: string },
): Promise<unknown> {
  const response = await apiFetch(
    `${apiBase()}/api/v1/traceability/manifests/${manifestId}/items`,
    {
      method: "POST",
      headers: headers(session),
      body: JSON.stringify(body),
    },
  );
  return parse(response);
}

export async function sealEvidenceManifest(
  session: SessionState,
  manifestId: string,
  body: { expected_version?: number } = {},
): Promise<EvidenceManifest> {
  const response = await apiFetch(
    `${apiBase()}/api/v1/traceability/manifests/${manifestId}/seal`,
    {
      method: "POST",
      headers: headers(session),
      body: JSON.stringify(body),
    },
  );
  return parse<EvidenceManifest>(response);
}

export async function createEvidenceExport(
  session: SessionState,
  body: { manifest_id: string; export_format?: string },
): Promise<EvidenceExport> {
  const response = await apiFetch(`${apiBase()}/api/v1/traceability/exports`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<EvidenceExport>(response);
}

export async function listEvidenceExports(
  session: SessionState,
  params: { limit?: number; offset?: number } = {},
): Promise<ListPage<EvidenceExport>> {
  const query = new URLSearchParams();
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  const response = await apiFetch(`${apiBase()}/api/v1/traceability/exports?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<ListPage<EvidenceExport>>(response);
}
