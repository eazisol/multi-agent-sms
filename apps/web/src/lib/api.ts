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
