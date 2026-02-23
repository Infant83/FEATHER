# Federnett Auth Operations (Root/Admin/User)

Last updated: 2026-02-22

## 1) Scope
- This document defines operational auth policy for Federnett control-plane APIs.
- Covers `root unlock`, `session auth`, role handling, bootstrap, and revoke.

## 2) Auth Layers
- `Session auth`:
  - Env: `FEDERNETT_AUTH_ACCOUNTS_JSON`
  - API: `POST /api/auth/session/login`, `POST /api/auth/session/logout`, `GET /api/auth/session/status`
  - Token header: `X-Federnett-Session-Token`
- `Root unlock`:
  - Env: `FEDERNETT_ROOT_PASSWORD`
  - API: `POST /api/auth/root/unlock`, `POST /api/auth/root/lock`, `GET /api/auth/root/status`
  - Token header: `X-Federnett-Root-Token`

## 3) Roles and Effective Privilege
- `user`: standard operator; no builtin profile write.
- `admin|owner|superuser|root`: treated as session-root.
  - Built-in profile write is allowed by session role, even when root token is absent.
- Root unlock token:
  - Enables built-in profile write for non-root session users.
  - TTL is controlled by `FEDERNETT_ROOT_TOKEN_TTL_SEC` (bounded in server).

## 4) Bootstrap Checklist
1. Set session account env:
   - `FEDERNETT_AUTH_ACCOUNTS_JSON='[{"username":"root","password":"change-me","role":"root","display_name":"Root Admin"}]'`
2. (Optional) set root password env:
   - `FEDERNETT_ROOT_PASSWORD='change-me-too'`
3. Start Federnett and verify:
   - `GET /api/auth/session/status`
   - `GET /api/auth/root/status`
4. In UI, sign in first; use root unlock only when built-in edits are required.

## 5) Revoke / Incident Response
- Session revoke:
  - Call `POST /api/auth/session/logout` with current session token.
  - Rotating `FEDERNETT_AUTH_ACCOUNTS_JSON` credentials invalidates future logins.
- Root revoke:
  - Call `POST /api/auth/root/lock` with current root token.
  - Rotating `FEDERNETT_ROOT_PASSWORD` invalidates future unlock attempts.
- Emergency:
  - Restart Federnett with updated env secrets to reset in-memory token state.

## 6) Audit and UI Signals
- UI badges expose:
  - `Session auth: <display> (<role>)`
  - `Root auth: locked/unlocked/session-root`
- Report Hub approval mutation is guarded by root/session-root policy.
- Built-in profile save path is blocked unless root condition is satisfied.

## 7) Recommended Policy
- Day-to-day: session role-based operation (`admin/user`) and keep root unlock disabled.
- Use root unlock as short-lived exception for builtin edits.
- Keep account JSON in secret store; do not commit credentials into repo.
