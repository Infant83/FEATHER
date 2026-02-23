from __future__ import annotations

import json

import pytest

import federnett.routes as routes_mod
from federnett.auth import SessionAuthManager


def test_session_auth_login_status_logout(monkeypatch) -> None:
    monkeypatch.setenv(
        "FEDERNETT_AUTH_ACCOUNTS_JSON",
        json.dumps(
            [
                {
                    "username": "root",
                    "password": "pw123",
                    "role": "root",
                    "display_name": "Root Operator",
                }
            ]
        ),
    )
    manager = SessionAuthManager()
    assert manager.enabled is True

    logged_in = manager.login("root", "pw123")
    assert logged_in.authenticated is True
    assert logged_in.token
    assert logged_in.role == "root"

    status = manager.status(logged_in.token)
    assert status.enabled is True
    assert status.authenticated is True
    assert status.username == "root"
    assert status.display_name == "Root Operator"
    assert status.role == "root"

    principal = manager.principal(logged_in.token)
    assert principal is not None
    assert principal.get("username") == "root"
    assert principal.get("role") == "root"

    logged_out = manager.logout(logged_in.token)
    assert logged_out.authenticated is False
    assert manager.status(logged_in.token).authenticated is False


def test_session_auth_rejects_invalid_credentials(monkeypatch) -> None:
    monkeypatch.setenv(
        "FEDERNETT_AUTH_ACCOUNTS_JSON",
        json.dumps([{"username": "user", "password": "pw"}]),
    )
    manager = SessionAuthManager()
    with pytest.raises(ValueError):
        manager.login("user", "wrong-password")


class _SessionOnlyHandler:
    def __init__(self, manager: SessionAuthManager, token: str) -> None:
        self._manager = manager
        self.headers = {"X-Federnett-Session-Token": token}

    def _session_auth(self) -> SessionAuthManager:
        return self._manager

    def _root_auth(self):
        return None


def test_session_root_role_grants_builtin_profile_edit_access(monkeypatch) -> None:
    monkeypatch.setenv(
        "FEDERNETT_AUTH_ACCOUNTS_JSON",
        json.dumps([{"username": "root", "password": "pw123", "role": "root"}]),
    )
    manager = SessionAuthManager()
    login = manager.login("root", "pw123")
    handler = _SessionOnlyHandler(manager, str(login.token or ""))

    root_status = routes_mod._root_auth_status_payload(handler)
    assert root_status["enabled"] is False
    assert root_status["unlocked"] is True
    assert root_status["session_root"] is True
    assert routes_mod._is_root_unlocked(handler) is True


def test_non_root_session_role_does_not_unlock_builtin_edit(monkeypatch) -> None:
    monkeypatch.setenv(
        "FEDERNETT_AUTH_ACCOUNTS_JSON",
        json.dumps([{"username": "user", "password": "pw", "role": "user"}]),
    )
    manager = SessionAuthManager()
    login = manager.login("user", "pw")
    handler = _SessionOnlyHandler(manager, str(login.token or ""))

    root_status = routes_mod._root_auth_status_payload(handler)
    assert root_status["enabled"] is False
    assert root_status["unlocked"] is False
    assert root_status["session_root"] is False
    assert routes_mod._is_root_unlocked(handler) is False
