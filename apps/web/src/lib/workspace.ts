/** Shared workspace IDs persisted locally (CRUD-lite APIs often lack list endpoints). */

const PROJECT_KEY = "masms.workspace.projectId";
const QUERY_KEY = "masms.workspace.queryId";
const DOCUMENT_KEY = "masms.workspace.documentId";

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
