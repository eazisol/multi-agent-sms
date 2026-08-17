"""Jira simulation and sandbox HTTP clients."""

from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any, Protocol
from uuid import UUID

import httpx
from pydantic import BaseModel, ValidationError

from masms_api.config import get_settings
from masms_api.modules.jira import domain
from masms_api.platform.secrets import SecretBackend, SecretBackendError


class JiraClient(Protocol):
    def create_issue(
        self,
        *,
        internal_ticket_id: UUID,
        summary: str,
        simulated_key: str | None = None,
    ) -> str: ...

    def add_comment(self, *, issue_key: str, comment_text: str) -> None: ...

    def verify_webhook(self, *, body: bytes, signature: str | None) -> None: ...


class SimulatedJiraClient:
    def create_issue(
        self,
        *,
        internal_ticket_id: UUID,
        summary: str,
        simulated_key: str | None = None,
    ) -> str:
        _ = (internal_ticket_id, summary)
        return simulated_key or domain.simulate_jira_key()

    def add_comment(self, *, issue_key: str, comment_text: str) -> None:
        _ = (issue_key, comment_text)

    def verify_webhook(self, *, body: bytes, signature: str | None) -> None:
        _ = (body, signature)


class JiraCredentials(BaseModel):
    email: str
    api_token: str
    webhook_secret: str | None = None


class LiveJiraClient:
    def __init__(
        self,
        *,
        base_url: str,
        project_key: str,
        credential_ref: str,
        secrets: SecretBackend,
        timeout_seconds: float = 20.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.project_key = project_key
        self.credential_ref = credential_ref
        self.secrets = secrets
        self.timeout_seconds = timeout_seconds

    def _credentials(self) -> JiraCredentials:
        try:
            payload = json.loads(self.secrets.get_secret(self.credential_ref))
            return JiraCredentials.model_validate(payload)
        except (json.JSONDecodeError, ValidationError) as exc:
            raise SecretBackendError("Jira credential reference contains invalid JSON") from exc

    def _request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any],
        operation: str,
    ) -> dict[str, Any]:
        credentials = self._credentials()
        response = httpx.request(
            method,
            f"{self.base_url}{path}",
            auth=(credentials.email, credentials.api_token),
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            json=payload,
            timeout=self.timeout_seconds,
        )
        if not response.is_success:
            raise RuntimeError(f"{operation} failed with HTTP {response.status_code}")
        if not response.content:
            return {}
        data = response.json()
        if not isinstance(data, dict):
            raise RuntimeError(f"{operation} returned an invalid response")
        return data

    def create_issue(
        self,
        *,
        internal_ticket_id: UUID,
        summary: str,
        simulated_key: str | None = None,
    ) -> str:
        _ = simulated_key
        result = self._request(
            "POST",
            "/rest/api/3/issue",
            payload={
                "fields": {
                    "project": {"key": self.project_key},
                    "summary": summary,
                    "issuetype": {"name": "Task"},
                },
                "properties": [
                    {
                        "key": "masmsInternalTicketId",
                        "value": str(internal_ticket_id),
                    }
                ],
            },
            operation="Jira issue create",
        )
        issue_key = result.get("key")
        if not isinstance(issue_key, str) or not issue_key:
            raise RuntimeError("Jira issue create response is missing key")
        return issue_key

    def add_comment(self, *, issue_key: str, comment_text: str) -> None:
        self._request(
            "POST",
            f"/rest/api/3/issue/{issue_key}/comment",
            payload={
                "body": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": comment_text}],
                        }
                    ],
                }
            },
            operation="Jira comment sync",
        )

    def verify_webhook(self, *, body: bytes, signature: str | None) -> None:
        secret = self._credentials().webhook_secret
        if not secret:
            raise SecretBackendError("Jira webhook_secret is not configured")
        if not signature:
            raise PermissionError("Jira webhook signature is required")
        digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        provided = signature.removeprefix("sha256=")
        if not hmac.compare_digest(digest, provided):
            raise PermissionError("Invalid Jira webhook signature")


def get_jira_client() -> JiraClient:
    settings = get_settings()
    if settings.jira_mode != "live":
        return SimulatedJiraClient()
    if not (
        settings.jira_base_url
        and settings.jira_project_key
        and settings.jira_credential_ref
    ):
        raise RuntimeError(
            "Live Jira requires MASMS_JIRA_BASE_URL, MASMS_JIRA_PROJECT_KEY, "
            "and MASMS_JIRA_CREDENTIAL_REF"
        )
    return LiveJiraClient(
        base_url=settings.jira_base_url,
        project_key=settings.jira_project_key,
        credential_ref=settings.jira_credential_ref,
        secrets=settings.secret_provider(),
    )
