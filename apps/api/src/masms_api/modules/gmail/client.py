"""Gmail simulation and sandbox HTTP clients."""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from email.message import EmailMessage
from typing import Any, Protocol

import httpx
from pydantic import BaseModel, ValidationError

from masms_api.config import get_settings
from masms_api.modules.gmail import domain
from masms_api.modules.gmail.models import GmailConnection, GmailDraftReview
from masms_api.platform.secrets import SecretBackend, SecretBackendError

GMAIL_API = "https://gmail.googleapis.com/gmail/v1"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"


@dataclass(frozen=True, slots=True)
class GmailSendResult:
    external_send_id: str
    message_id: str
    thread_id: str


@dataclass(frozen=True, slots=True)
class GmailInboundMessage:
    message_id: str
    thread_id: str
    history_id: str | None
    subject: str
    from_email: str
    snippet: str | None


class GmailClient(Protocol):
    def send_message(
        self,
        *,
        connection: GmailConnection,
        draft: GmailDraftReview,
        thread_id: str | None,
    ) -> GmailSendResult: ...

    def list_inbound(
        self,
        *,
        connection: GmailConnection,
        history_id: str | None,
        limit: int,
    ) -> list[GmailInboundMessage]: ...


class SimulatedGmailClient:
    def send_message(
        self,
        *,
        connection: GmailConnection,
        draft: GmailDraftReview,
        thread_id: str | None,
    ) -> GmailSendResult:
        _ = connection
        external_id = domain.simulate_external_send_id()
        return GmailSendResult(
            external_send_id=external_id,
            message_id=f"outbound-{external_id}",
            thread_id=thread_id or f"thread-{draft.draft_id}",
        )

    def list_inbound(
        self,
        *,
        connection: GmailConnection,
        history_id: str | None,
        limit: int,
    ) -> list[GmailInboundMessage]:
        _ = (connection, history_id, limit)
        return []


class GmailCredentials(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
    client_id: str | None = None
    client_secret: str | None = None


class LiveGmailClient:
    def __init__(self, *, secrets: SecretBackend, timeout_seconds: float = 20.0) -> None:
        self.secrets = secrets
        self.timeout_seconds = timeout_seconds

    def _credentials(self, connection: GmailConnection) -> GmailCredentials:
        if not connection.credential_ref:
            raise SecretBackendError("Gmail connection has no credential_ref")
        try:
            payload = json.loads(self.secrets.get_secret(connection.credential_ref))
            return GmailCredentials.model_validate(payload)
        except (json.JSONDecodeError, ValidationError) as exc:
            raise SecretBackendError("Gmail credential reference contains invalid JSON") from exc

    def _access_token(self, connection: GmailConnection) -> str:
        credentials = self._credentials(connection)
        if credentials.refresh_token and credentials.client_id and credentials.client_secret:
            response = httpx.post(
                GOOGLE_TOKEN_URL,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": credentials.refresh_token,
                    "client_id": credentials.client_id,
                    "client_secret": credentials.client_secret,
                },
                timeout=self.timeout_seconds,
            )
            data = _json_response(response, operation="Gmail OAuth refresh")
            token = data.get("access_token")
            if isinstance(token, str) and token:
                return token
            raise RuntimeError("Gmail OAuth refresh returned no access token")
        if credentials.access_token:
            return credentials.access_token
        raise SecretBackendError("Gmail credentials require an access token or refresh-token set")

    def _headers(self, connection: GmailConnection) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._access_token(connection)}"}

    def send_message(
        self,
        *,
        connection: GmailConnection,
        draft: GmailDraftReview,
        thread_id: str | None,
    ) -> GmailSendResult:
        message = EmailMessage()
        message["To"] = draft.to_addresses
        message["From"] = connection.email_address
        message["Subject"] = draft.subject
        message.set_content(draft.body_preview or "")
        body: dict[str, str] = {
            "raw": base64.urlsafe_b64encode(message.as_bytes()).decode("ascii").rstrip("=")
        }
        if thread_id:
            body["threadId"] = thread_id
        response = httpx.post(
            f"{GMAIL_API}/users/me/messages/send",
            headers=self._headers(connection),
            json=body,
            timeout=self.timeout_seconds,
        )
        data = _json_response(response, operation="Gmail send")
        message_id = data.get("id")
        result_thread_id = data.get("threadId")
        if not isinstance(message_id, str) or not isinstance(result_thread_id, str):
            raise RuntimeError("Gmail send response is missing message or thread id")
        return GmailSendResult(
            external_send_id=message_id,
            message_id=message_id,
            thread_id=result_thread_id,
        )

    def list_inbound(
        self,
        *,
        connection: GmailConnection,
        history_id: str | None,
        limit: int,
    ) -> list[GmailInboundMessage]:
        headers = self._headers(connection)
        message_ids = self._list_message_ids(
            headers=headers,
            history_id=history_id,
            limit=limit,
        )
        messages: list[GmailInboundMessage] = []
        for message_id in message_ids[:limit]:
            response = httpx.get(
                f"{GMAIL_API}/users/me/messages/{message_id}",
                headers=headers,
                params={
                    "format": "metadata",
                    "metadataHeaders": ["From", "Subject"],
                },
                timeout=self.timeout_seconds,
            )
            payload = _json_response(response, operation="Gmail message read")
            parsed = _parse_inbound(payload)
            if parsed is not None:
                messages.append(parsed)
        return messages

    def _list_message_ids(
        self,
        *,
        headers: dict[str, str],
        history_id: str | None,
        limit: int,
    ) -> list[str]:
        if history_id:
            response = httpx.get(
                f"{GMAIL_API}/users/me/history",
                headers=headers,
                params={
                    "startHistoryId": history_id,
                    "historyTypes": "messageAdded",
                    "maxResults": limit,
                },
                timeout=self.timeout_seconds,
            )
            payload = _json_response(response, operation="Gmail history list")
            result: list[str] = []
            for history in payload.get("history", []):
                if not isinstance(history, dict):
                    continue
                for added in history.get("messagesAdded", []):
                    if isinstance(added, dict) and isinstance(added.get("message"), dict):
                        message_id = added["message"].get("id")
                        if isinstance(message_id, str):
                            result.append(message_id)
            return list(dict.fromkeys(result))
        response = httpx.get(
            f"{GMAIL_API}/users/me/messages",
            headers=headers,
            params={"q": "in:inbox", "maxResults": limit},
            timeout=self.timeout_seconds,
        )
        payload = _json_response(response, operation="Gmail message list")
        return [
            row["id"]
            for row in payload.get("messages", [])
            if isinstance(row, dict) and isinstance(row.get("id"), str)
        ]


def _parse_inbound(payload: dict[str, Any]) -> GmailInboundMessage | None:
    message_id = payload.get("id")
    thread_id = payload.get("threadId")
    if not isinstance(message_id, str) or not isinstance(thread_id, str):
        return None
    header_values: dict[str, str] = {}
    nested = payload.get("payload")
    if isinstance(nested, dict):
        for header in nested.get("headers", []):
            if not isinstance(header, dict):
                continue
            name = header.get("name")
            value = header.get("value")
            if isinstance(name, str) and isinstance(value, str):
                header_values[name.lower()] = value
    return GmailInboundMessage(
        message_id=message_id,
        thread_id=thread_id,
        history_id=str(payload["historyId"]) if payload.get("historyId") else None,
        subject=header_values.get("subject", ""),
        from_email=header_values.get("from", "unknown@example.invalid"),
        snippet=str(payload["snippet"]) if payload.get("snippet") else None,
    )


def _json_response(response: httpx.Response, *, operation: str) -> dict[str, Any]:
    if not response.is_success:
        raise RuntimeError(f"{operation} failed with HTTP {response.status_code}")
    payload = response.json()
    if not isinstance(payload, dict):
        raise RuntimeError(f"{operation} returned an invalid response")
    return payload


def get_gmail_client() -> GmailClient:
    settings = get_settings()
    if settings.gmail_mode == "live":
        return LiveGmailClient(secrets=settings.secret_provider())
    return SimulatedGmailClient()
