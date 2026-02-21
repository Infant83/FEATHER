# Playwright / MCP Troubleshooting

Last updated: 2026-02-21

## 1) 문제 증상
- Codex extension 시작 시 다음 유형 오류가 발생할 수 있음:
  - `resources/templates/list failed: Method not found (-32601)`
  - `Codex process is not available`

## 2) 의미
- 이 오류는 보통 **클라이언트(확장)**와 **MCP 서버(@playwright/mcp)** 사이의
  프로토콜/버전 호환이 맞지 않을 때 발생한다.
- 즉, 확장이 호출하는 MCP 메서드를 서버가 지원하지 못하는 상태다.

## 3) 현재 권장 운영
- Codex MCP `playwright`는 비활성화하고, UI 검증은 Python Playwright 스모크로 수행.
- `C:\Users\angpa\.codex\config.toml`에 Playwright MCP를 비활성화한 주석이 유지된 상태면 정상.

## 4) 재시도 절차 (MCP 재활성화 전)
1. 버전 확인
```powershell
npx @playwright/mcp@latest --version
```

2. 잠금/고아 프로세스 정리
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\playwright_mcp_recover.ps1 -PruneTempProfiles
```

3. Codex extension reload
4. MCP handshake 재확인
5. 동일 오류 재발 시 다시 비활성화

## 5) config 예시 (재활성화 시)
```toml
[mcp_servers.playwright]
command = "npx"
args = ["@playwright/mcp@latest", "--headless", "--isolated"]
```

노트:
- `--headless`, `--isolated`는 세션 충돌/락파일 문제를 줄이는 데 유리하다.
- 확장 버전이 낮거나 MCP 스펙이 다른 경우 위 설정으로도 실패할 수 있다.

## 6) Python Playwright 대체 검증
MCP가 불안정한 환경에서는 아래 방식으로 UI 회귀를 계속 수행할 수 있다.

```powershell
@'
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://127.0.0.1:8767/", wait_until="domcontentloaded")
    assert page.locator("#live-ask-thread").count() > 0
    browser.close()
'@ | python -
```

## 7) Node Playwright vs MCP Playwright
- `@playwright/test`: 테스트 프레임워크 (사용자 스크립트 실행)
- `@playwright/mcp`: MCP 서버 (Codex/에이전트 도구 호출용)

둘은 목적이 다르며, 하나가 정상이어도 다른 하나가 실패할 수 있다.

