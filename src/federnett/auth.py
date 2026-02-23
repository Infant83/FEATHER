from __future__ import annotations

import hmac
import os
import secrets
import time
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from threading import Lock
from typing import Any


def _utc_iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


@dataclass(frozen=True)
class RootAuthStatus:
    enabled: bool
    unlocked: bool
    expires_at: str | None
    token: str | None = None


class RootAuthManager:
    """Small token-based root unlock manager for Federnett control-plane APIs."""

    def __init__(
        self,
        *,
        password_env: str = "FEDERNETT_ROOT_PASSWORD",
        ttl_env: str = "FEDERNETT_ROOT_TOKEN_TTL_SEC",
        default_ttl_sec: int = 60 * 60 * 8,
    ) -> None:
        self._password = str(os.getenv(password_env) or "").strip()
        ttl_raw = str(os.getenv(ttl_env) or "").strip()
        ttl = default_ttl_sec
        if ttl_raw:
            try:
                ttl = int(ttl_raw)
            except Exception:
                ttl = default_ttl_sec
        self._ttl_sec = max(300, min(ttl, 60 * 60 * 24 * 14))
        self._tokens: dict[str, float] = {}
        self._lock = Lock()

    @property
    def enabled(self) -> bool:
        return bool(self._password)

    def _cleanup_locked(self, now: float) -> None:
        stale = [token for token, exp in self._tokens.items() if exp <= now]
        for token in stale:
            self._tokens.pop(token, None)

    def _is_unlocked_locked(self, token: str | None, now: float) -> tuple[bool, float | None]:
        if not token:
            return False, None
        exp = self._tokens.get(token)
        if exp is None:
            return False, None
        if exp <= now:
            self._tokens.pop(token, None)
            return False, None
        return True, exp

    def unlock(self, password: str) -> RootAuthStatus:
        if not self.enabled:
            raise ValueError("Root auth is disabled. Set FEDERNETT_ROOT_PASSWORD first.")
        candidate = str(password or "")
        if not hmac.compare_digest(candidate, self._password):
            raise ValueError("Invalid root password.")
        token = secrets.token_urlsafe(36)
        now = time.time()
        expires = now + self._ttl_sec
        with self._lock:
            self._cleanup_locked(now)
            self._tokens[token] = expires
        return RootAuthStatus(enabled=True, unlocked=True, expires_at=_utc_iso(expires), token=token)

    def lock(self, token: str | None) -> RootAuthStatus:
        if not self.enabled:
            return RootAuthStatus(enabled=False, unlocked=False, expires_at=None)
        key = str(token or "").strip()
        with self._lock:
            if key:
                self._tokens.pop(key, None)
        return RootAuthStatus(enabled=True, unlocked=False, expires_at=None)

    def is_unlocked(self, token: str | None) -> bool:
        if not self.enabled:
            return False
        now = time.time()
        key = str(token or "").strip()
        with self._lock:
            self._cleanup_locked(now)
            unlocked, _exp = self._is_unlocked_locked(key, now)
        return unlocked

    def status(self, token: str | None) -> RootAuthStatus:
        if not self.enabled:
            return RootAuthStatus(enabled=False, unlocked=False, expires_at=None)
        now = time.time()
        key = str(token or "").strip()
        with self._lock:
            self._cleanup_locked(now)
            unlocked, exp = self._is_unlocked_locked(key, now)
        return RootAuthStatus(
            enabled=True,
            unlocked=unlocked,
            expires_at=_utc_iso(exp) if exp else None,
        )


@dataclass(frozen=True)
class SessionAuthStatus:
    enabled: bool
    authenticated: bool
    username: str | None
    display_name: str | None
    role: str | None
    expires_at: str | None
    token: str | None = None


class SessionAuthManager:
    """Simple token-based session auth for Federnett UI/API."""

    def __init__(
        self,
        *,
        accounts_env: str = "FEDERNETT_AUTH_ACCOUNTS_JSON",
        ttl_env: str = "FEDERNETT_AUTH_SESSION_TTL_SEC",
        default_ttl_sec: int = 60 * 60 * 12,
    ) -> None:
        self._accounts = self._load_accounts(str(os.getenv(accounts_env) or ""))
        ttl_raw = str(os.getenv(ttl_env) or "").strip()
        ttl = default_ttl_sec
        if ttl_raw:
            try:
                ttl = int(ttl_raw)
            except Exception:
                ttl = default_ttl_sec
        self._ttl_sec = max(300, min(ttl, 60 * 60 * 24 * 14))
        self._sessions: dict[str, dict[str, Any]] = {}
        self._lock = Lock()

    @property
    def enabled(self) -> bool:
        return bool(self._accounts)

    @staticmethod
    def _load_accounts(raw: str) -> dict[str, dict[str, str]]:
        text = str(raw or "").strip()
        if not text:
            return {}
        try:
            payload = json.loads(text)
        except Exception:
            return {}
        out: dict[str, dict[str, str]] = {}
        entries: list[dict[str, Any]] = []
        if isinstance(payload, list):
            entries = [row for row in payload if isinstance(row, dict)]
        elif isinstance(payload, dict):
            for username, row in payload.items():
                if isinstance(row, dict):
                    item = dict(row)
                    item.setdefault("username", username)
                    entries.append(item)
        for row in entries:
            username = str(row.get("username") or "").strip().lower()
            password = str(row.get("password") or "").strip()
            if not username or not password:
                continue
            role = str(row.get("role") or "user").strip().lower() or "user"
            display_name = str(row.get("display_name") or row.get("name") or username).strip() or username
            out[username] = {
                "password": password,
                "role": role,
                "display_name": display_name,
            }
        return out

    def _cleanup_locked(self, now: float) -> None:
        stale = [token for token, row in self._sessions.items() if float(row.get("expires", 0.0)) <= now]
        for token in stale:
            self._sessions.pop(token, None)

    def login(self, username: str, password: str) -> SessionAuthStatus:
        if not self.enabled:
            raise ValueError("Session auth is disabled. Set FEDERNETT_AUTH_ACCOUNTS_JSON first.")
        user_key = str(username or "").strip().lower()
        candidate = str(password or "")
        record = self._accounts.get(user_key)
        if not record or not hmac.compare_digest(candidate, str(record.get("password") or "")):
            raise ValueError("Invalid username or password.")
        now = time.time()
        expires = now + self._ttl_sec
        token = secrets.token_urlsafe(36)
        with self._lock:
            self._cleanup_locked(now)
            self._sessions[token] = {
                "username": user_key,
                "display_name": str(record.get("display_name") or user_key),
                "role": str(record.get("role") or "user"),
                "expires": expires,
            }
        return SessionAuthStatus(
            enabled=True,
            authenticated=True,
            username=user_key,
            display_name=str(record.get("display_name") or user_key),
            role=str(record.get("role") or "user"),
            expires_at=_utc_iso(expires),
            token=token,
        )

    def logout(self, token: str | None) -> SessionAuthStatus:
        if not self.enabled:
            return SessionAuthStatus(
                enabled=False,
                authenticated=False,
                username=None,
                display_name=None,
                role=None,
                expires_at=None,
            )
        key = str(token or "").strip()
        with self._lock:
            if key:
                self._sessions.pop(key, None)
        return SessionAuthStatus(
            enabled=True,
            authenticated=False,
            username=None,
            display_name=None,
            role=None,
            expires_at=None,
        )

    def principal(self, token: str | None) -> dict[str, str] | None:
        if not self.enabled:
            return None
        now = time.time()
        key = str(token or "").strip()
        with self._lock:
            self._cleanup_locked(now)
            row = self._sessions.get(key)
            if not row:
                return None
            exp = float(row.get("expires", 0.0))
            if exp <= now:
                self._sessions.pop(key, None)
                return None
            return {
                "username": str(row.get("username") or ""),
                "display_name": str(row.get("display_name") or row.get("username") or ""),
                "role": str(row.get("role") or "user"),
                "expires_at": _utc_iso(exp),
            }

    def status(self, token: str | None) -> SessionAuthStatus:
        principal = self.principal(token)
        if not self.enabled:
            return SessionAuthStatus(
                enabled=False,
                authenticated=False,
                username=None,
                display_name=None,
                role=None,
                expires_at=None,
            )
        if not principal:
            return SessionAuthStatus(
                enabled=True,
                authenticated=False,
                username=None,
                display_name=None,
                role=None,
                expires_at=None,
            )
        return SessionAuthStatus(
            enabled=True,
            authenticated=True,
            username=principal.get("username") or None,
            display_name=principal.get("display_name") or None,
            role=principal.get("role") or None,
            expires_at=principal.get("expires_at") or None,
        )
