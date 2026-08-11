/** Shared workspace IDs persisted locally (CRUD-lite APIs often lack list endpoints). */

const PROJECT_KEY = "masms.workspace.projectId";
const QUERY_KEY = "masms.workspace.queryId";
const DOCUMENT_KEY = "masms.workspace.documentId";
const CONVERSATION_KEY = "masms.workspace.conversationId";
const TICKET_KEY = "masms.workspace.ticketId";
const REQUIREMENT_ENTITY_KEY = "masms.workspace.requirementEntityId";

function read(key: string): string {
  if (typeof window === "undefined") return "";
  return window.localStorage.getItem(key) ?? "";
}

function write(key: string, value: string) {
  if (typeof window === "undefined") return;
  if (value) window.localStorage.setItem(key, value);
  else window.localStorage.removeItem(key);
}

export function getWorkspaceProjectId(): string {
  return read(PROJECT_KEY);
}

export function setWorkspaceProjectId(id: string) {
  write(PROJECT_KEY, id);
}

export function getWorkspaceQueryId(): string {
  return read(QUERY_KEY);
}

export function setWorkspaceQueryId(id: string) {
  write(QUERY_KEY, id);
}

export function getWorkspaceDocumentId(): string {
  return read(DOCUMENT_KEY);
}

export function setWorkspaceDocumentId(id: string) {
  write(DOCUMENT_KEY, id);
}

export function getWorkspaceConversationId(): string {
  return read(CONVERSATION_KEY);
}

export function setWorkspaceConversationId(id: string) {
  write(CONVERSATION_KEY, id);
}

export function getWorkspaceTicketId(): string {
  return read(TICKET_KEY);
}

export function setWorkspaceTicketId(id: string) {
  write(TICKET_KEY, id);
}

export function getWorkspaceRequirementEntityId(): string {
  return read(REQUIREMENT_ENTITY_KEY);
}

export function setWorkspaceRequirementEntityId(id: string) {
  write(REQUIREMENT_ENTITY_KEY, id);
}
