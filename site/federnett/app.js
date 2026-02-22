const $ = (sel) => document.querySelector(sel);

const state = {
  info: null,
  runs: [],
  templates: [],
  templateDetails: {},
  templateStyles: [],
  templateStyleContent: {},
  templateBuilder: {
    meta: {},
    sections: [],
    guides: {},
    writerGuidance: [],
    css: "",
  },
  runSummary: null,
  instructionFiles: {},
  filePreview: {
    path: "",
    content: "",
    dirty: false,
    canEdit: false,
    mode: "text",
    objectUrl: "",
    htmlDoc: "",
  },
  previewPopup: {
    open: true,
    maximized: false,
  },
  saveAs: {
    open: false,
    path: "",
    entries: [],
    mode: "preview",
  },
  runPicker: {
    items: [],
    filtered: [],
    selected: "",
    root: "",
    query: "",
  },
  instructionModal: {
    items: [],
    filtered: [],
    selectedPath: "",
    runRel: "",
    mode: "feather",
  },
  activeJobId: null,
  activeJobKind: null,
  activeJobPending: false,
  activeSource: null,
  jobs: [],
  jobsExpanded: false,
  historyLogs: {},
  logsCollapsed: false,
  logMode: "markdown",
  logRenderPending: false,
  logAutoScrollRequested: false,
  logAutoFollow: true,
  logBuffer: [],
  pipeline: {
    order: [],
    selected: new Set(),
    draggingId: null,
    activeStageId: null,
  },
  workflow: {
    kind: "",
    running: false,
    historyMode: false,
    historySourcePath: "",
    resumeStage: "",
    resumePromptPath: "",
    resumePromptStage: "",
    resumePromptAt: "",
    historyStageStatus: {},
    historyFailedStage: "",
    selectedStages: new Set(),
    stageOrder: [],
    autoStages: new Set(),
    autoStageReasons: {},
    passMetrics: [],
    activeStep: "",
    completedSteps: new Set(),
    hasError: false,
    statusText: "Idle",
    mainStatusText: "Idle",
    runRel: "",
    resultPath: "",
    spots: [],
    spotSeq: 0,
    spotTimers: {},
    lastMainStageIndex: -1,
    loopbackCount: 0,
    loopbackPulse: false,
    loopbackTimer: null,
    qualityMenuOpen: false,
    studioOpen: false,
    studioFocusStage: "overview",
    runtimeNoticeDigest: "",
    stageOverrides: {},
    stageOverrideWarnings: {},
    stageOverrideStage: "scout",
    stageOverrideSyncTimer: null,
    stageOverridePath: "",
  },
  templateGen: {
    log: "",
    active: false,
  },
  agentProfiles: {
    list: [],
    activeId: "",
    activeSource: "",
    activeProfile: null,
    memoryText: "",
    readOnly: false,
    rootAuth: {
      enabled: false,
      unlocked: false,
      session_root: false,
      token: "",
      expires_at: "",
    },
    sessionAuth: {
      enabled: false,
      authenticated: false,
      username: "",
      display_name: "",
      role: "",
      token: "",
      expires_at: "",
    },
  },
  canvas: {
    open: false,
    runRel: "",
    basePath: "",
    baseRel: "",
    outputPath: "",
    updatePath: "",
    selection: "",
    reportText: "",
    reportHtml: "",
  },
  ask: {
    open: false,
    busy: false,
    history: [],
    runRel: "",
    profileId: "",
    agentOverride: "",
    historyProfileId: "",
    scopeKey: "",
    threads: [],
    activeThreadId: "",
    selectionText: "",
    pendingAction: null,
    lastAction: null,
    lastAnswer: "",
    lastSources: [],
    pendingSources: [],
    pendingQuestion: "",
    liveAnswer: "",
    threadPopoverOpen: false,
    llmBackend: "openai_api",
    runtimeMode: "auto",
    reasoningEffort: "off",
    actionMode: "plan",
    allowArtifactWrites: false,
    capabilities: null,
    activity: {},
    activityTimeline: [],
    activityStatus: "대기",
    capabilityRegistry: null,
    capabilityManagerOpen: false,
    traceShowHistory: false,
    autoFollowAnswer: true,
    capabilityDetailOpen: false,
    selectionDragging: false,
  },
  liveAsk: {
    busy: false,
    scopeKey: "",
    history: [],
    pendingQuestion: "",
    liveAnswer: "",
    pendingSources: [],
    lastSources: [],
    lastAction: null,
    lastAnswer: "",
    streamLogBuffer: "",
    streamChunksLogged: 0,
    autoFollowThread: true,
    autoLogContext: true,
    autoLogChars: 2200,
    abortController: null,
    activeLogStartIndex: -1,
    jobLogStartIndex: -1,
    lastJobLogStartIndex: -1,
    sourceFoldState: {},
    inlineSourceFoldState: {},
    processFoldState: {},
  },
  workspace: {
    open: false,
    tab: "templates",
  },
  workspaceSettings: {
    effective: null,
    stored: null,
    path: "",
    canEdit: false,
  },
  runFiles: {
    view: "core",
    filter: "",
    filterLoaded: false,
  },
  modelCatalog: {
    all: [],
    openai: [],
    codex: [],
  },
  modelPolicy: {
    lock: true,
    backend: "openai_api",
    model: "",
    checkModel: "",
    visionModel: "",
    reasoningEffort: "off",
    federhavRuntimeMode: "auto",
    liveAutoLogContext: true,
    liveAutoLogChars: 2200,
  },
};

const LOG_LINE_LIMIT = 1400;
const LOG_LINE_MAX_CHARS = 3200;
const LOG_MD_MAX_CHARS = 120000;
const LOG_MD_TAIL_CHARS = 60000;
const MERMAID_CDN = "https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.1/mermaid.min.js";
const WORKFLOW_PREF_STORAGE_KEY = "federnett-workflow-pref-v1";
const AGENT_PROFILE_STORAGE_KEY = "federnett-active-agent-profile-v1";
const AGENT_ROOT_TOKEN_KEY = "federnett-root-token-v1";
const AGENT_SESSION_TOKEN_KEY = "federnett-session-token-v1";
const ASK_DEFAULT_THREAD_ID = "main";
const ASK_DEFAULT_THREAD_TITLE = "FederHav 기본 대화";
const ASK_THREAD_LIMIT = 24;
const ASK_ACTION_PREF_KEY = askStorageKey("action-pref-v1");
const ASK_GEOM_KEY = askStorageKey("geom-v2");
const LIVE_ASK_DRAFT_KEY = askStorageKey("live-draft-v1");
const LIVE_ASK_PREF_KEY = askStorageKey("live-pref-v1");
const LIVE_ASK_LOG_TAIL_CHOICES = [1200, 2200, 3600, 5200];
const LIVE_ASK_LOG_TAIL_DEFAULT = 2200;
const LIVE_ASK_PROCESS_MAX_LINES = 84;
const LIVE_ASK_PROCESS_MAX_CHARS = 9000;
const LIVE_ASK_GLOBAL_LOG_TAIL_LINES = 84;
const LIVE_ASK_PROCESS_INLINE_LINES = 14;
const PREVIEW_POPUP_OPEN_KEY = "federnett-preview-popup-open-v1";
const PREVIEW_POPUP_GEOM_KEY = "federnett-preview-popup-geom-v1";
const PREVIEW_POPUP_MAX_KEY = "federnett-preview-popup-max-v1";
const LOGS_MAXIMIZED_KEY = "federnett-logs-maximized-v1";
const WORKFLOW_STUDIO_OPEN_KEY = "federnett-workflow-studio-open-v1";
const CONTROL_PANEL_COLLAPSE_KEY = "federnett-control-panel-collapsed-v1";
const CONTROL_PANEL_WIDTH_KEY = "federnett-control-panel-width-v1";
const WORKFLOW_STAGE_OVERRIDE_KEY = "federnett-workflow-stage-overrides-v1";
const RUN_FILE_VIEW_KEY = "federnett-run-file-view-v1";
const RUN_FILE_FILTER_KEY = "federnett-run-file-filter-v1";
const GLOBAL_MODEL_POLICY_KEY = "federnett-global-model-policy-v1";
const ASK_CAPABILITY_FALLBACK = {
  term: "Capability Packs",
  tools: [
    { id: "source_index", label: "Source Index", description: "코드/문서/런 인덱스 검색" },
    { id: "web_research", label: "Web Search", description: "웹 보강 검색", enabled: false },
    { id: "llm_generate", label: "LLM Generate", description: "최종 답변 생성" },
  ],
  skills: [
    { id: "action_runner", label: "Action Runner", description: "안전 실행 제안/미리보기" },
  ],
  mcp: [],
  packs: [],
};
const AGENT_APPLY_TARGETS = [
  { id: "writer", label: "Writer", hint: "최종 보고서 본문 생성" },
  { id: "critic", label: "Critic", hint: "문장/논리 품질 비평" },
  { id: "reviser", label: "Reviser", hint: "비평 반영 재작성" },
  { id: "planner", label: "Planner", hint: "보고서 구조/작업 계획 수립" },
  { id: "alignment", label: "Alignment", hint: "목표/정책 일치성 점검" },
  { id: "scout", label: "Scout", hint: "초기 스캔/핵심 대상 선별" },
  { id: "evidence", label: "Evidence", hint: "인용 가능한 근거 추출" },
  { id: "quality", label: "Quality", hint: "최종 품질 루프 점검" },
];
const mermaidState = {
  loading: null,
  ready: false,
};
let workflowDismissBound = false;
let askScrollRafId = 0;
let askGeomMemory = null;
let liveAskComposerResizeObserver = null;
let liveAskStatusClearTimer = null;
let globalModelSyncGuard = false;
let overlayEscapeBound = false;
let popupDragBindingsBound = false;
let modalOpenSequence = 0;

const STAGE_DEFS = [
  {
    id: "scout",
    label: "Scout",
    desc:
      "아카이브 지형도를 빠르게 훑고 핵심 읽기 대상을 고릅니다. 전체 맥락을 잡는 탐색 단계입니다.",
  },
  {
    id: "plan",
    label: "Plan",
    desc:
      "Scout 결과를 실행 가능한 작업 순서로 정리합니다. 단계 의사결정을 명시적으로 남길 때 유용합니다.",
  },
  {
    id: "evidence",
    label: "Evidence",
    desc:
      "핵심 원문을 읽고 인용 가능한 근거를 뽑아 구조화합니다. 문서 수집과 Writer를 연결하는 핵심 단계입니다.",
  },
  {
    id: "writer",
    label: "Writer",
    desc:
      "근거를 바탕으로 보고서 본문을 작성합니다. 템플릿/깊이/언어 제약을 적용해 완성도를 맞춥니다.",
  },
  {
    id: "quality",
    label: "Quality",
    desc:
      "비평/수정 루프를 돌려 품질을 다듬습니다. 완성도는 올라가지만 시간과 토큰 사용량이 늘 수 있습니다.",
  },
];

const STAGE_INDEX = Object.fromEntries(STAGE_DEFS.map((s, i) => [s.id, i]));
const WORKFLOW_STAGE_ORDER = STAGE_DEFS.map((s) => s.id);
const WORKFLOW_NODE_ORDER = ["federhav", "feather", ...WORKFLOW_STAGE_ORDER, "result"];
const WORKFLOW_LABELS = {
  federhav: "FederHav",
  feather: "Feather",
  scout: "Scout",
  plan: "Plan",
  evidence: "Evidence",
  writer: "Writer",
  quality: "Quality",
  result: "Result",
};
const WORKFLOW_SPOT_LABELS = {
  prompt: "Prompt Generate",
  template: "Template Generate",
  generate_prompt: "Prompt Generate",
  job: "Extra Process",
};
const WORKFLOW_SPOT_TTL_MS = 7000;
const WORKFLOW_LOOPBACK_PULSE_MS = 1200;
const STAGE_TOOL_TOKEN_RE = /^[a-zA-Z][a-zA-Z0-9_:.+-]*$/;
const MODEL_PRESET_OPTIONS = [
  "$OPENAI_MODEL",
  "$CODEX_MODEL",
  "gpt-5.3-codex",
  "gpt-5.3-codex-spark",
  "gpt-5.2-codex",
  "gpt-5.1-codex-max",
  "gpt-5.2",
  "gpt-5.1-codex-mini",
  "gpt-4o-mini",
  "gpt-4o",
];
const ASK_REASONING_EFFORT_CHOICES = new Set(["off", "low", "medium", "high", "extra_high"]);
const ASK_WRITE_ACTION_TYPES = new Set([
  "run_feather",
  "run_federlicht",
  "run_feather_then_federlicht",
  "create_run_folder",
]);
const ASK_RUN_TARGET_ACTION_TYPES = new Set([
  "run_feather",
  "run_federlicht",
  "run_feather_then_federlicht",
  "switch_run",
]);
const ASK_INSTRUCTION_CONFIRM_ACTION_TYPES = new Set([
  "run_feather",
  "run_feather_then_federlicht",
]);
const ASK_PLAN_INSTANT_ACTION_TYPES = new Set([
  "switch_run",
  "preset_resume_stage",
  "focus_editor",
  "set_action_mode",
]);
const ASK_SAFE_CAPABILITY_EFFECTS = new Set([
  "open_path",
  "open_url",
  "set_inline_prompt",
  "mcp_ping",
  "none",
  "done",
]);
const RUN_SCOPED_DIR_PREFIXES = [
  "archive/",
  "instruction/",
  "report_notes/",
  "report/",
  "output/",
  "tmp/",
  "final_report/",
  "large_tool_results/",
  "supporting/",
];
const RUN_HINT_BLOCKED_TOKENS = new Set([
  "run",
  "runs",
  "site",
  "folder",
  "runfolder",
  "run-folder",
  "폴더",
  "런",
  "federnett",
  "federlicht",
  "federhav",
  "feather",
  "plan",
  "act",
  "mode",
  "current",
  "selected",
  "target",
  "default",
  "지금",
  "현재",
  "선택",
  "선택된",
  "대상",
  "대상에서",
  "기준",
  "기반",
  "현재run",
  "선택된run",
  "run대상",
  "run대상에서",
  "에서",
  "사용법",
  "방법",
  "설명",
  "요약",
  "가이드",
  "알려",
  "알려줘",
  "짧게",
  "how",
  "guide",
  "usage",
  "from",
  "to",
  "as",
  "set",
  "use",
  "open",
  "switch",
]);
const WORKFLOW_EVENT_RE =
  /\[workflow\]\s+stage=([a-z_]+)\s+status=([a-z_]+)(?:\s+detail=([^\n]+))?/i;
const WORKFLOW_STATUS_PRIORITY = {
  ran: 60,
  cached: 55,
  skipped: 50,
  pending: 40,
  running: 40,
  in_progress: 40,
  complete: 35,
  done: 35,
  disabled: 10,
  error: -20,
  failed: -20,
};

const FIELD_HELP = {
  "feather-download-pdf": "Download arXiv/web PDFs when available and extract text for archive indexing.",
  "feather-openalex": "Search OpenAlex for additional open-access papers related to the instruction queries.",
  "feather-youtube": "Run YouTube search for matching queries or explicit YouTube hints.",
  "feather-yt-transcript": "Fetch YouTube transcripts (requires youtube-transcript-api).",
  "feather-update-run": "Reuse the same run folder and append new artifacts instead of creating _01, _02 folders.",
  "feather-agentic-search":
    "Enable iterative LLM-guided source expansion. Feather plans follow-up search/extract actions.",
  "feather-lang": "Soft language preference for search results (for example en or ko).",
  "feather-days": "Lookback window in days for recent paper/search heuristics.",
  "feather-max-results": "Maximum results per search step.",
  "feather-yt-order": "YouTube ordering: relevance, date, viewCount, rating.",
  "feather-model": "Model used for agentic planning turns. Supports $ENV style values.",
  "feather-max-iter": "Maximum planning iterations in agentic mode.",
  "federlicht-template-rigidity":
    "How strongly the writer follows template structure and style guidance.",
  "federlicht-free-format":
    "Write without template scaffolding. When enabled, template and rigidity controls are ignored.",
  "federlicht-style-pack":
    "Visual preset for free-format HTML reports. Applied only when Free Format is enabled.",
  "federlicht-temperature-level": "Preset creativity/variance level for report agents.",
  "federlicht-reasoning-effort":
    "Reasoning effort preset for reasoning-capable models (low/medium/high/extra_high).",
  "ask-reasoning-effort":
    "FederHav 답변 추론 강도 (low/medium/high/extra_high). Codex/OpenAI 추론형 모델에서 반영됩니다.",
  "federlicht-quality-iterations": "Number of quality loop passes (critic/reviser/evaluator).",
  "federlicht-web-search":
    "Enable Federlicht supporting web research stage. This is separate from Feather YouTube/OpenAlex collection.",
  "agent-config-overrides":
    "Profile-level Federlicht config overrides (same schema as agent_config.json > config).",
  "agent-agent-overrides":
    "Profile-level per-agent overrides (same schema as agent_config.json > agents).",
};

function isFederlichtActive() {
  return document.body?.dataset?.tab === "federlicht";
}

function applyFieldTooltips() {
  Object.entries(FIELD_HELP).forEach(([id, text]) => {
    const el = document.getElementById(id);
    if (!el || !text) return;
    el.setAttribute("title", text);
    const label = el.closest("label");
    if (label) {
      label.setAttribute("title", text);
      label.setAttribute("data-help", text);
    }
  });
}

function isMissingFileError(err) {
  const msg = String(err?.message ?? err ?? "").toLowerCase();
  return msg.includes("404") && msg.includes("not found");
}

function applyTheme(theme) {
  const normalizedTheme = String(theme || "").trim().toLowerCase() || "white";
  const nextTheme = normalizedTheme === "default" ? "white" : normalizedTheme;
  const root = document.documentElement;
  root.setAttribute("data-theme", nextTheme);
  localStorage.setItem("federnett-theme", nextTheme);
  const select = $("#theme-select");
  if (select && select.value !== nextTheme) {
    select.value = nextTheme;
  }
}

function initTheme() {
  const savedRaw = String(localStorage.getItem("federnett-theme") || "").trim().toLowerCase();
  const saved = !savedRaw || savedRaw === "default" ? "white" : savedRaw;
  applyTheme(saved);
  $("#theme-select")?.addEventListener("change", (e) => {
    applyTheme(e.target.value);
  });
}

function loadRootAuthToken() {
  try {
    return String(localStorage.getItem(AGENT_ROOT_TOKEN_KEY) || "").trim();
  } catch (err) {
    return "";
  }
}

function persistRootAuthToken(token) {
  const value = String(token || "").trim();
  try {
    if (value) {
      localStorage.setItem(AGENT_ROOT_TOKEN_KEY, value);
    } else {
      localStorage.removeItem(AGENT_ROOT_TOKEN_KEY);
    }
  } catch (err) {
    // ignore storage failures
  }
}

function activeRootAuthToken() {
  const runtime = String(state.agentProfiles?.rootAuth?.token || "").trim();
  if (runtime) return runtime;
  return loadRootAuthToken();
}

function loadSessionAuthToken() {
  try {
    return String(localStorage.getItem(AGENT_SESSION_TOKEN_KEY) || "").trim();
  } catch (err) {
    return "";
  }
}

function persistSessionAuthToken(token) {
  const value = String(token || "").trim();
  try {
    if (value) {
      localStorage.setItem(AGENT_SESSION_TOKEN_KEY, value);
    } else {
      localStorage.removeItem(AGENT_SESSION_TOKEN_KEY);
    }
  } catch (err) {
    // ignore storage failures
  }
}

function activeSessionAuthToken() {
  const runtime = String(state.agentProfiles?.sessionAuth?.token || "").trim();
  if (runtime) return runtime;
  return loadSessionAuthToken();
}

async function fetchJSON(path, opts) {
  const requestOpts = { ...(opts || {}) };
  const headers = new Headers(requestOpts.headers || {});
  const rootToken = activeRootAuthToken();
  if (rootToken && !headers.has("X-Federnett-Root-Token")) {
    headers.set("X-Federnett-Root-Token", rootToken);
  }
  const sessionToken = activeSessionAuthToken();
  if (sessionToken && !headers.has("X-Federnett-Session-Token")) {
    headers.set("X-Federnett-Session-Token", sessionToken);
  }
  requestOpts.headers = headers;
  const res = await fetch(path, requestOpts);
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    const err = new Error(`${res.status} ${res.statusText} ${text}`.trim());
    err.status = res.status;
    err.statusText = res.statusText;
    err.body = text;
    if (text) {
      try {
        err.payload = JSON.parse(text);
      } catch (_parseError) {
        err.payload = null;
      }
    } else {
      err.payload = null;
    }
    throw err;
  }
  return res.json();
}

function joinPath(a, b) {
  if (!a) return b || "";
  if (!b) return a;
  const left = a.replace(/[\\/]+$/, "");
  const right = b.replace(/^[\\/]+/, "");
  return `${left}/${right}`;
}

function toFileUrl(absPath) {
  const posix = absPath.replace(/\\/g, "/");
  return `file:///${posix}`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function isElementInViewport(el) {
  if (!el) return false;
  const rect = el.getBoundingClientRect();
  const viewHeight = window.innerHeight || document.documentElement.clientHeight;
  return rect.top >= 0 && rect.bottom <= viewHeight;
}

function focusPanel(selector) {
  const el = document.querySelector(selector);
  if (!el) return;
  if (!isElementInViewport(el)) {
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

function previewPopupElement() {
  const byId = $("#preview-popup");
  if (byId) return byId;
  const fallback = $(".preview-block");
  if (!fallback) return null;
  if (!fallback.id) fallback.id = "preview-popup";
  if (!fallback.classList.contains("preview-block")) {
    fallback.classList.add("preview-block");
  }
  return fallback;
}

function ensurePreviewPopupLayer() {
  let layer = $("#preview-popup-layer");
  if (layer) return layer;
  layer = document.createElement("div");
  layer.id = "preview-popup-layer";
  document.body.appendChild(layer);
  return layer;
}

function mountPreviewPopupToLayer() {
  const popup = previewPopupElement();
  if (!popup) return null;
  const layer = ensurePreviewPopupLayer();
  if (popup.parentElement !== layer) {
    layer.appendChild(popup);
  }
  return popup;
}

function clampPreviewPopupPosition() {
  const popup = previewPopupElement();
  if (!popup) return;
  if (state.previewPopup.maximized || popup.classList.contains("is-maximized")) return;
  const rect = popup.getBoundingClientRect();
  const width = rect.width || popup.offsetWidth || 0;
  const height = rect.height || popup.offsetHeight || 0;
  const maxLeft = Math.max(8, window.innerWidth - width - 8);
  const maxTop = Math.max(8, window.innerHeight - height - 8);
  const nextLeft = Math.min(Math.max(rect.left, 8), maxLeft);
  const nextTop = Math.min(Math.max(rect.top, 8), maxTop);
  popup.style.left = `${Math.round(nextLeft)}px`;
  popup.style.top = `${Math.round(nextTop)}px`;
  popup.style.right = "auto";
  popup.style.bottom = "auto";
}

function savePreviewPopupGeometry() {
  const popup = previewPopupElement();
  if (!popup) return;
  if (state.previewPopup.maximized || popup.classList.contains("is-maximized")) return;
  const rect = popup.getBoundingClientRect();
  const payload = {
    left: Math.round(rect.left),
    top: Math.round(rect.top),
    width: Math.round(rect.width),
    height: Math.round(rect.height),
  };
  try {
    localStorage.setItem(PREVIEW_POPUP_GEOM_KEY, JSON.stringify(payload));
  } catch (err) {
    // ignore
  }
}

function restorePreviewPopupGeometry() {
  const popup = previewPopupElement();
  if (!popup) return;
  if (state.previewPopup.maximized || popup.classList.contains("is-maximized")) return;
  try {
    const raw = localStorage.getItem(PREVIEW_POPUP_GEOM_KEY);
    if (!raw) return;
    const parsed = JSON.parse(raw);
    const left = Number(parsed?.left);
    const top = Number(parsed?.top);
    const width = Number(parsed?.width);
    const height = Number(parsed?.height);
    if (Number.isFinite(left) && Number.isFinite(top)) {
      popup.style.left = `${Math.round(left)}px`;
      popup.style.top = `${Math.round(top)}px`;
      popup.style.right = "auto";
      popup.style.bottom = "auto";
    }
    if (Number.isFinite(width) && width > 280) {
      popup.style.width = `${Math.round(width)}px`;
    }
    if (Number.isFinite(height) && height > 220) {
      popup.style.height = `${Math.round(height)}px`;
    }
    clampPreviewPopupPosition();
  } catch (err) {
    // ignore
  }
}

function resetPreviewPopupGeometry() {
  const popup = previewPopupElement();
  if (!popup) return;
  popup.style.removeProperty("left");
  popup.style.removeProperty("top");
  popup.style.removeProperty("right");
  popup.style.removeProperty("bottom");
  popup.style.removeProperty("width");
  popup.style.removeProperty("height");
  try {
    localStorage.removeItem(PREVIEW_POPUP_GEOM_KEY);
  } catch (err) {
    // ignore
  }
}

function setPreviewPopupOpen(open, { persist = true, focus = false } = {}) {
  const popup = previewPopupElement();
  if (!popup) return;
  state.previewPopup.open = Boolean(open);
  popup.classList.toggle("is-open", state.previewPopup.open);
  popup.setAttribute("aria-hidden", state.previewPopup.open ? "false" : "true");
  const toggleBtn = $("#preview-popup-toggle");
  if (toggleBtn) {
    toggleBtn.classList.toggle("is-active", state.previewPopup.open);
    toggleBtn.textContent = state.previewPopup.open ? "Preview 숨기기" : "Preview Popup";
  }
  if (persist) {
    try {
      localStorage.setItem(PREVIEW_POPUP_OPEN_KEY, state.previewPopup.open ? "true" : "false");
    } catch (err) {
      // ignore
    }
  }
  if (state.previewPopup.open) {
    if (focus) {
      window.setTimeout(() => {
        popup.focus({ preventScroll: true });
      }, 0);
    }
    window.requestAnimationFrame(() => {
      if (!state.previewPopup.maximized) {
        clampPreviewPopupPosition();
      }
    });
  }
}

function hasUnsavedPreviewChanges() {
  return Boolean(state.filePreview?.dirty && state.filePreview?.canEdit);
}

function requestClosePreviewPopup({ persist = true, reason = "dismiss", force = false } = {}) {
  if (!state.previewPopup.open) return true;
  if (!force && hasUnsavedPreviewChanges()) {
    const ok = window.confirm(
      "프리뷰에 저장되지 않은 변경사항이 있습니다.\n저장하지 않고 닫을까요?",
    );
    if (!ok) return false;
  }
  setPreviewPopupOpen(false, { persist });
  if (reason === "escape") {
    setAskStatus("Preview 패널을 닫았습니다.");
  }
  return true;
}

function setPreviewPopupMaximized(maximized, { persist = true } = {}) {
  const popup = previewPopupElement();
  if (!popup) return;
  const next = Boolean(maximized);
  if (next && !state.previewPopup.maximized) {
    savePreviewPopupGeometry();
  }
  state.previewPopup.maximized = next;
  popup.classList.toggle("is-maximized", next);
  if (!next) {
    restorePreviewPopupGeometry();
    clampPreviewPopupPosition();
  }
  const maxBtn = $("#preview-popup-maximize");
  if (maxBtn) {
    maxBtn.textContent = next ? "복원" : "최대화";
    maxBtn.setAttribute("aria-pressed", next ? "true" : "false");
  }
  if (persist) {
    try {
      localStorage.setItem(PREVIEW_POPUP_MAX_KEY, next ? "true" : "false");
    } catch (err) {
      // ignore
    }
  }
}

function isPreviewPopupTriggerTarget(target) {
  if (!(target instanceof Element)) return false;
  const selector = [
    "[data-file-open]",
    "[data-file]",
    "[data-figure-open-preview]",
    "[data-figure-open-select]",
    "[data-figure-id]",
    "[data-ask-open]",
    ".ask-inline-source-open",
    "[data-source-path]",
    "[data-workflow-open]",
    "#preview-popup-close",
    "#preview-popup-reset",
    "#preview-popup-maximize",
    "#preview-popup-toggle",
  ].join(",");
  return Boolean(target.closest(selector));
}

const TEXT_PREVIEW_EXTS = new Set([
  ".txt",
  ".md",
  ".json",
  ".jsonl",
  ".yml",
  ".yaml",
  ".csv",
  ".tsv",
  ".html",
  ".css",
  ".js",
  ".ts",
  ".py",
  ".tex",
  ".log",
]);
const INSTRUCTION_EXTS = new Set([
  ".txt",
  ".md",
  ".text",
  ".prompt",
  ".instruct",
  ".instruction",
]);

function isTextPreviewable(path) {
  if (!path) return false;
  const lower = path.toLowerCase();
  const dot = lower.lastIndexOf(".");
  if (dot === -1) return true;
  return TEXT_PREVIEW_EXTS.has(lower.slice(dot));
}

function hasFileExtension(value) {
  const cleaned = normalizePathString(value);
  if (!cleaned) return false;
  const last = cleaned.split("/").pop() || "";
  const dot = last.lastIndexOf(".");
  if (dot <= 0) return false;
  const ext = last.slice(dot).toLowerCase();
  return INSTRUCTION_EXTS.has(ext) || Boolean(ext);
}

function rootAbs() {
  return state.info?.root_abs || "";
}

function toAbsPath(relPath) {
  const root = rootAbs();
  if (!root || !relPath) return "";
  return joinPath(root, relPath);
}

function toFileUrlFromRel(relPath) {
  const abs = toAbsPath(relPath);
  return abs ? toFileUrl(abs) : "";
}

function apiRawUrl(relPath) {
  if (!relPath) return "";
  return `/api/raw?path=${encodeURIComponent(relPath)}`;
}

function rawFileUrl(relPath) {
  const cleaned = String(relPath || "")
    .trim()
    .replaceAll("\\", "/")
    .replace(/^\//, "");
  if (!cleaned) return "";
  const encoded = cleaned
    .split("/")
    .map((part) => encodeURIComponent(part))
    .join("/");
  return `/raw/${encoded}`;
}

function openPath(relPath) {
  const url = toFileUrlFromRel(relPath);
  if (url) {
    window.open(url, "_blank");
  } else if (relPath) {
    appendLog(`[open] unable to resolve ${relPath}\n`);
  }
}

function modalElementById(modalId) {
  const token = String(modalId || "").trim().replace(/^#/, "");
  if (!token) return null;
  return document.getElementById(token);
}

function modalCardElement(modalOrId) {
  const modal = typeof modalOrId === "string" ? modalElementById(modalOrId) : modalOrId;
  if (!(modal instanceof Element)) return null;
  return modal.querySelector(".modal-card");
}

function readDragOffset(surface) {
  if (!(surface instanceof Element)) return { x: 0, y: 0 };
  const x = Number(surface.dataset.dragX || 0);
  const y = Number(surface.dataset.dragY || 0);
  return {
    x: Number.isFinite(x) ? x : 0,
    y: Number.isFinite(y) ? y : 0,
  };
}

function writeDragOffset(surface, x = 0, y = 0) {
  if (!(surface instanceof Element)) return;
  const nx = Math.round(Number.isFinite(Number(x)) ? Number(x) : 0);
  const ny = Math.round(Number.isFinite(Number(y)) ? Number(y) : 0);
  surface.dataset.dragX = String(nx);
  surface.dataset.dragY = String(ny);
  surface.style.setProperty("--drag-x", `${nx}px`);
  surface.style.setProperty("--drag-y", `${ny}px`);
}

function resetDragOffset(surface) {
  if (!(surface instanceof Element)) return;
  delete surface.dataset.dragX;
  delete surface.dataset.dragY;
  surface.style.removeProperty("--drag-x");
  surface.style.removeProperty("--drag-y");
}

function clampDragOffset(surface, nextX, nextY) {
  if (!(surface instanceof Element)) return { x: nextX, y: nextY };
  const rect = surface.getBoundingClientRect();
  const current = readDragOffset(surface);
  let x = Number.isFinite(Number(nextX)) ? Number(nextX) : current.x;
  let y = Number.isFinite(Number(nextY)) ? Number(nextY) : current.y;
  const dx = x - current.x;
  const dy = y - current.y;
  let left = rect.left + dx;
  let right = rect.right + dx;
  let top = rect.top + dy;
  let bottom = rect.bottom + dy;
  const pad = 10;
  const maxRight = window.innerWidth - pad;
  const maxBottom = window.innerHeight - pad;
  if (left < pad) {
    const shift = pad - left;
    x += shift;
    left += shift;
    right += shift;
  }
  if (right > maxRight) {
    const shift = right - maxRight;
    x -= shift;
    right -= shift;
    left -= shift;
  }
  if (top < pad) {
    const shift = pad - top;
    y += shift;
    top += shift;
    bottom += shift;
  }
  if (bottom > maxBottom) {
    const shift = bottom - maxBottom;
    y -= shift;
    bottom -= shift;
    top -= shift;
  }
  return { x: Math.round(x), y: Math.round(y) };
}

function bindDraggableSurface(surface, handle) {
  if (!(surface instanceof HTMLElement) || !(handle instanceof HTMLElement)) return;
  if (handle.dataset.dragBound === "true") return;
  handle.dataset.dragBound = "true";
  let dragging = false;
  let pointerId = null;
  let startX = 0;
  let startY = 0;
  let startOffset = { x: 0, y: 0 };
  const move = (ev) => {
    if (!dragging) return;
    const deltaX = ev.clientX - startX;
    const deltaY = ev.clientY - startY;
    const rawX = startOffset.x + deltaX;
    const rawY = startOffset.y + deltaY;
    const clamped = clampDragOffset(surface, rawX, rawY);
    writeDragOffset(surface, clamped.x, clamped.y);
  };
  const stop = () => {
    if (!dragging) return;
    dragging = false;
    surface.classList.remove("is-dragging");
    window.removeEventListener("pointermove", move);
    window.removeEventListener("pointerup", stop);
    window.removeEventListener("pointercancel", stop);
    window.removeEventListener("blur", stop);
  };
  handle.addEventListener(
    "pointerdown",
    (ev) => {
      if (ev.button !== 0) return;
      const target = ev.target;
      if (target instanceof Element) {
        const interactive = target.closest(
          "button,select,input,textarea,a,label,summary,[contenteditable='true']",
        );
        if (interactive) return;
      }
      dragging = true;
      pointerId = ev.pointerId;
      startX = ev.clientX;
      startY = ev.clientY;
      startOffset = readDragOffset(surface);
      surface.classList.add("is-dragging");
      try {
        handle.setPointerCapture(pointerId);
      } catch (err) {
        // ignore
      }
      window.addEventListener("pointermove", move, { passive: true });
      window.addEventListener("pointerup", stop, { passive: true });
      window.addEventListener("pointercancel", stop, { passive: true });
      window.addEventListener("blur", stop, { passive: true });
      ev.preventDefault();
    },
    { passive: false },
  );
  window.addEventListener(
    "resize",
    () => {
      if (surface.getClientRects().length <= 0) return;
      const current = readDragOffset(surface);
      const clamped = clampDragOffset(surface, current.x, current.y);
      if (clamped.x !== current.x || clamped.y !== current.y) {
        writeDragOffset(surface, clamped.x, clamped.y);
      }
    },
    { passive: true },
  );
}

function initPopupDragBindings() {
  if (popupDragBindingsBound) return;
  popupDragBindingsBound = true;
  document.querySelectorAll(".modal .modal-card").forEach((card) => {
    const handle = card.querySelector(".modal-header");
    if (handle instanceof HTMLElement) {
      bindDraggableSurface(card, handle);
    }
  });
  const workspacePanel = $("#workspace-panel");
  const workspaceHead = workspacePanel?.querySelector(".workspace-panel-head");
  if (workspacePanel instanceof HTMLElement && workspaceHead instanceof HTMLElement) {
    bindDraggableSurface(workspacePanel, workspaceHead);
  }
  const workflowPanel = $("#workflow-studio-panel");
  const workflowHead = workflowPanel?.querySelector(".workflow-studio-head");
  if (workflowPanel instanceof HTMLElement && workflowHead instanceof HTMLElement) {
    bindDraggableSurface(workflowPanel, workflowHead);
  }
}

function openOverlayModal(modalId) {
  const modal = modalElementById(modalId);
  if (!modal) return false;
  modal.classList.add("open");
  modal.setAttribute("aria-hidden", "false");
  modal.dataset.modalOpenSeq = String(++modalOpenSequence);
  resetDragOffset(modalCardElement(modal));
  return true;
}

function closeOverlayModal(modalId) {
  const modal = modalElementById(modalId);
  if (!modal) return false;
  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");
  delete modal.dataset.modalOpenSeq;
  resetDragOffset(modalCardElement(modal));
  return true;
}

function isOverlayModalOpen(modalId) {
  const modal = modalElementById(modalId);
  return Boolean(modal && modal.classList.contains("open"));
}

function closeKnownModalById(modalId) {
  const token = String(modalId || "").trim();
  if (!token) return false;
  if (token === "ask-action-modal") {
    closeAskActionModal();
    return true;
  }
  if (token === "instruction-modal") {
    closeInstructionModal();
    return true;
  }
  if (token === "run-picker-modal") {
    closeRunPickerModal();
    return true;
  }
  if (token === "model-policy-modal") {
    closeModelPolicyModal();
    return true;
  }
  if (token === "jobs-modal") {
    closeJobsModal();
    return true;
  }
  if (token === "template-modal") {
    closeTemplateModal();
    return true;
  }
  if (token === "saveas-modal") {
    closeSaveAsModal();
    return true;
  }
  if (token === "help-modal") {
    closeHelpModal();
    return true;
  }
  return closeOverlayModal(token);
}

function topOpenModalElement() {
  const openModals = [...document.querySelectorAll(".modal.open")];
  if (!openModals.length) return null;
  openModals.sort((a, b) => {
    const seqA = Number(a.dataset.modalOpenSeq || 0);
    const seqB = Number(b.dataset.modalOpenSeq || 0);
    return seqB - seqA;
  });
  return openModals[0] || null;
}

function closeTopOverlayLayer() {
  const topModal = topOpenModalElement();
  if (topModal?.id) {
    return closeKnownModalById(topModal.id);
  }
  if (state.previewPopup.open) {
    return requestClosePreviewPopup({ persist: true, reason: "escape" });
  }
  if (state.workflow.studioOpen) {
    setWorkflowStudioOpen(false);
    return true;
  }
  if (state.workspace.open) {
    setWorkspacePanelOpen(false);
    return true;
  }
  if (state.ask.open) {
    setAskOpen(false, { persist: true });
    return true;
  }
  const wrap = $("#logs-wrap");
  if (wrap?.classList.contains("is-maximized")) {
    setLogsMaximized(false, { persist: true });
    return true;
  }
  return false;
}

function bindGlobalOverlayEscape() {
  if (overlayEscapeBound) return;
  overlayEscapeBound = true;
  document.addEventListener(
    "keydown",
    (ev) => {
      if (ev.key !== "Escape") return;
      const closed = closeTopOverlayLayer();
      if (!closed) return;
      ev.preventDefault();
      ev.stopPropagation();
    },
    true,
  );
}

function isWheelEditableTarget(target) {
  if (!(target instanceof Element)) return false;
  return Boolean(
    target.closest(
      "textarea,input,select,option,[contenteditable='true'],.cm-editor,.monaco-editor,pre code",
    ),
  );
}

function isVerticallyScrollable(el) {
  if (!(el instanceof HTMLElement)) return false;
  const style = window.getComputedStyle(el);
  const overflowY = style.overflowY || style.overflow;
  const allow = /(auto|scroll|overlay)/i.test(overflowY);
  return allow && el.scrollHeight > el.clientHeight + 2;
}

function canScrollByDelta(el, deltaY) {
  if (!(el instanceof HTMLElement)) return false;
  const current = Number(el.scrollTop || 0);
  const max = Math.max(0, Number(el.scrollHeight || 0) - Number(el.clientHeight || 0));
  if (max <= 0) return false;
  if (deltaY > 0) return current < max - 1;
  if (deltaY < 0) return current > 1;
  return false;
}

function nearestScrollableElement(target, stopAt) {
  let node = target instanceof Element ? target : null;
  while (node && node !== stopAt && node !== document.body) {
    if (node instanceof HTMLElement && isVerticallyScrollable(node)) {
      return node;
    }
    node = node.parentElement;
  }
  if (stopAt instanceof HTMLElement && isVerticallyScrollable(stopAt)) {
    return stopAt;
  }
  return null;
}

function bindWheelScrollAssist(rootSelector, fallbackSelector) {
  const root = typeof rootSelector === "string" ? document.querySelector(rootSelector) : rootSelector;
  if (!(root instanceof HTMLElement)) return;
  if (root.dataset.wheelAssistBound === "true") return;
  root.dataset.wheelAssistBound = "true";
  root.addEventListener(
    "wheel",
    (ev) => {
      if (ev.defaultPrevented || ev.ctrlKey || ev.metaKey) return;
      const target = ev.target;
      if (!(target instanceof Element)) return;
      if (isWheelEditableTarget(target)) return;
      const scroller = nearestScrollableElement(target, root);
      if (scroller && canScrollByDelta(scroller, ev.deltaY)) return;
      const fallback = fallbackSelector
        ? root.querySelector(fallbackSelector)
        : root;
      if (!(fallback instanceof HTMLElement) || !isVerticallyScrollable(fallback)) return;
      if (!canScrollByDelta(fallback, ev.deltaY)) return;
      fallback.scrollTop += ev.deltaY;
      ev.preventDefault();
    },
    { passive: false },
  );
}

function openSaveAsModal(initialPath, mode = "preview") {
  const modal = $("#saveas-modal");
  const list = $("#saveas-list");
  const pathInput = $("#saveas-path");
  const filenameInput = $("#saveas-filename");
  if (!modal || !list || !pathInput || !filenameInput) return;
  state.saveAs.mode = mode || "preview";
  state.saveAs.open = true;
  if (initialPath) {
    state.saveAs.path = initialPath.replace(/\/[^/]*$/, "");
  } else {
    state.saveAs.path = "";
  }
  openOverlayModal("saveas-modal");
  loadSaveAsDir(state.saveAs.path || "");
  filenameInput.value = "";
}

function closeSaveAsModal() {
  closeOverlayModal("saveas-modal");
  state.saveAs.open = false;
  state.saveAs.mode = "preview";
}

function openHelpModal() {
  openOverlayModal("help-modal");
}

function closeHelpModal() {
  closeOverlayModal("help-modal");
}

function compactLiveAskStatus(message) {
  const text = String(message || "").trim();
  if (!text) return "";
  if (text.startsWith("답변 생성 중")) return "답변 생성 중...";
  if (text.startsWith("코드/문서를 분석 중")) return "분석 중...";
  if (text.startsWith("완료(fallback)")) return "완료(fallback)";
  if (text.startsWith("완료 ·")) return "완료";
  return text.length > 120 ? `${text.slice(0, 116)}...` : text;
}

function setAskStatus(message) {
  const el = $("#ask-status");
  if (el) {
    el.textContent = message || "";
  }
  const live = $("#live-ask-status");
  if (live) {
    const full = String(message || "");
    const compact = compactLiveAskStatus(full);
    if (liveAskStatusClearTimer) {
      window.clearTimeout(liveAskStatusClearTimer);
      liveAskStatusClearTimer = null;
    }
    if (!compact || compact === "Ready.") {
      live.textContent = "";
      live.title = "";
    } else {
      live.textContent = compact;
      live.title = full;
      const sticky = /(error|failed|실패|중단|취소|권한|forbidden|unauthorized)/i.test(full);
      if (!sticky) {
        liveAskStatusClearTimer = window.setTimeout(() => {
          const node = $("#live-ask-status");
          if (!node) return;
          node.textContent = "";
          node.title = "";
          liveAskStatusClearTimer = null;
        }, 9000);
      }
    }
  }
}

function setLogsMaximized(maximized, { persist = true } = {}) {
  const wrap = $("#logs-wrap");
  if (!wrap) return;
  const next = Boolean(maximized);
  wrap.classList.toggle("is-maximized", next);
  document.body.classList.toggle("logs-maximized", next);
  const btn = $("#log-maximize");
  if (btn) {
    btn.textContent = next ? "복원" : "최대화";
    btn.setAttribute("aria-pressed", next ? "true" : "false");
    btn.classList.toggle("is-active", next);
  }
  if (persist) {
    try {
      localStorage.setItem(LOGS_MAXIMIZED_KEY, next ? "true" : "false");
    } catch (err) {
      // ignore
    }
  }
}

function workflowStudioScopeForStage(stageId) {
  const token = String(stageId || "").trim().toLowerCase();
  if (token === "overview" || token === "all") return { feather: true, federlicht: true, quality: true };
  if (token === "federhav") return { feather: true, federlicht: true, quality: true };
  if (token === "feather") return { feather: true, federlicht: false, quality: false };
  if (token === "quality") return { feather: false, federlicht: true, quality: true };
  if (WORKFLOW_STAGE_ORDER.includes(token) || token === "result") {
    return { feather: false, federlicht: true, quality: false };
  }
  return { feather: true, federlicht: true, quality: true };
}

function normalizeStageOverrideEntry(raw) {
  if (!raw || typeof raw !== "object") {
    return { enabled: true, system_prompt: "", tools: "" };
  }
  return {
    enabled: raw.enabled !== false,
    system_prompt: String(raw.system_prompt || "").trim(),
    tools: String(raw.tools || "").trim(),
  };
}

function normalizeWorkflowStageToolsInput(rawText) {
  const raw = String(rawText || "");
  const tokens = raw
    .split(/[,\n]/)
    .map((token) => String(token || "").trim())
    .filter(Boolean);
  const unique = [];
  const seen = new Set();
  const invalid = [];
  for (const token of tokens) {
    const normalized = token.toLowerCase();
    if (!STAGE_TOOL_TOKEN_RE.test(normalized)) {
      invalid.push(token);
      continue;
    }
    if (seen.has(normalized)) continue;
    seen.add(normalized);
    unique.push(normalized);
  }
  return {
    value: unique.join(","),
    tokens: unique,
    invalidTokens: invalid,
  };
}

function loadWorkflowStageOverrides() {
  try {
    const raw = localStorage.getItem(WORKFLOW_STAGE_OVERRIDE_KEY);
    if (!raw) return;
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object") return;
    const next = {};
    Object.entries(parsed).forEach(([stageId, value]) => {
      const token = String(stageId || "").trim().toLowerCase();
      if (!WORKFLOW_STAGE_ORDER.includes(token)) return;
      next[token] = normalizeStageOverrideEntry(value);
    });
    state.workflow.stageOverrides = next;
  } catch (err) {
    state.workflow.stageOverrides = {};
  }
}

function saveWorkflowStageOverrides() {
  try {
    localStorage.setItem(
      WORKFLOW_STAGE_OVERRIDE_KEY,
      JSON.stringify(state.workflow.stageOverrides || {}),
    );
  } catch (err) {
    // ignore
  }
}

function activeWorkflowStageForOverrides() {
  const preferred = String(state.workflow.stageOverrideStage || "").trim().toLowerCase();
  if (WORKFLOW_STAGE_ORDER.includes(preferred)) return preferred;
  const token = String(state.pipeline.activeStageId || state.workflow.resumeStage || "scout").trim().toLowerCase();
  if (WORKFLOW_STAGE_ORDER.includes(token)) {
    state.workflow.stageOverrideStage = token;
    return token;
  }
  state.workflow.stageOverrideStage = "scout";
  return "scout";
}

function summarizeStageOverrideStatus(entry) {
  const normalized = normalizeStageOverrideEntry(entry || {});
  const parts = [];
  if (!normalized.enabled) parts.push("stage disabled");
  if (normalized.tools) parts.push("tools override");
  if (normalized.system_prompt) parts.push("prompt override");
  return parts.length ? parts.join(" · ") : "기본 에이전트 설정 사용";
}

function renderWorkflowStageSelector(selectedStage = "") {
  const selectEl = $("#wf-stage-select");
  if (!selectEl) return;
  const token = String(selectedStage || activeWorkflowStageForOverrides()).trim().toLowerCase();
  const options = STAGE_DEFS.map((def) => `<option value="${escapeHtml(def.id)}">${escapeHtml(def.label)} (${escapeHtml(def.id)})</option>`).join("");
  if (selectEl.innerHTML !== options) {
    selectEl.innerHTML = options;
  }
  if (WORKFLOW_STAGE_ORDER.includes(token)) {
    selectEl.value = token;
  }
}

function renderWorkflowStageOverrideContext(stageId, entry, warningText = "") {
  const host = $("#wf-stage-context");
  if (!host) return;
  const token = String(stageId || "").trim().toLowerCase();
  const def = STAGE_DEFS.find((item) => item.id === token);
  const normalized = normalizeStageOverrideEntry(entry || {});
  const enabledChip = normalized.enabled
    ? '<span class="workflow-stage-chip is-on">enabled</span>'
    : '<span class="workflow-stage-chip is-off">disabled</span>';
  host.innerHTML = `
    <div class="workflow-stage-context-head">
      <strong>${escapeHtml(def?.label || token || "stage")}</strong>
      ${enabledChip}
    </div>
    <div class="workflow-stage-context-desc">${escapeHtml(def?.desc || "선택된 stage에 대한 세부 override를 설정합니다.")}</div>
    <div class="workflow-stage-context-state">${escapeHtml(summarizeStageOverrideStatus(normalized))}</div>
    <div class="workflow-stage-context-priority">priority: global settings → stage override → runtime temp</div>
    ${warningText ? `<div class="workflow-stage-context-warning">${escapeHtml(warningText)}</div>` : ""}
  `;
  const selectedPill = $("#wf-selected-stage-pill");
  if (selectedPill) {
    selectedPill.textContent = `selected: ${def?.label || token || "-"}`;
  }
  const activePill = $("#wf-active-stage-pill");
  if (activePill) {
    const activeToken = String(
      state.pipeline.activeStageId
      || state.workflow.activeStep
      || state.workflow.focusHintStage
      || "",
    )
      .trim()
      .toLowerCase();
    const activeDef = STAGE_DEFS.find((item) => item.id === activeToken);
    activePill.textContent = `pipeline focus: ${activeDef?.label || activeToken || "-"}`;
  }
}

function renderWorkflowStagePromptPreview(stageId, entry) {
  const host = $("#wf-stage-prompt-preview");
  if (!host) return;
  const token = String(stageId || "").trim().toLowerCase();
  const def = STAGE_DEFS.find((item) => item.id === token);
  const normalized = normalizeStageOverrideEntry(entry || {});
  const lines = [
    "[prompt chain]",
    `1) stage: ${def?.label || token} (${token || "-"})`,
    `2) base intent: ${def?.desc || "runtime stage policy"}`,
    "3) baseline prompt source: federlicht runtime/profile 기본 prompt",
    "",
    "[override]",
    normalized.system_prompt || "(none)",
    "",
    "[effective]",
    !normalized.enabled
      ? "stage disabled: 이 stage는 실행 대상에서 제외됩니다."
      : (normalized.system_prompt
        ? "override prompt가 stage system prompt를 대체합니다."
        : "기본 system prompt가 그대로 사용됩니다."),
  ];
  host.textContent = lines.join("\n");
}

function readWorkflowStageOverrideControls() {
  const stageId = activeWorkflowStageForOverrides();
  const entry = normalizeStageOverrideEntry(state.workflow.stageOverrides?.[stageId] || {});
  entry.enabled = Boolean($("#wf-stage-enabled")?.checked ?? entry.enabled);
  entry.system_prompt = String($("#wf-stage-prompt")?.value || "").trim();
  const toolsEl = $("#wf-stage-tools");
  const parsedTools = normalizeWorkflowStageToolsInput(toolsEl?.value || "");
  entry.tools = parsedTools.value;
  if (toolsEl && String(toolsEl.value || "") !== entry.tools) {
    toolsEl.value = entry.tools;
  }
  state.workflow.stageOverrideWarnings = state.workflow.stageOverrideWarnings || {};
  const warningText = parsedTools.invalidTokens.length
    ? `무시된 도구 토큰: ${parsedTools.invalidTokens.slice(0, 5).join(", ")}`
    : "";
  if (warningText) {
    state.workflow.stageOverrideWarnings[stageId] = warningText;
  } else {
    delete state.workflow.stageOverrideWarnings[stageId];
  }
  state.workflow.stageOverrides = state.workflow.stageOverrides || {};
  const isDefault = entry.enabled && !entry.system_prompt && !entry.tools;
  if (isDefault) {
    delete state.workflow.stageOverrides[stageId];
  } else {
    state.workflow.stageOverrides[stageId] = entry;
  }
  saveWorkflowStageOverrides();
  renderWorkflowStageOverrideContext(stageId, entry, warningText);
  renderWorkflowStagePromptPreview(stageId, entry);
  return { stageId, entry };
}

function applyWorkflowStageOverrideControls(stageId) {
  const token = String(stageId || "").trim().toLowerCase();
  const normalized = WORKFLOW_STAGE_ORDER.includes(token) ? token : "scout";
  state.workflow.stageOverrideStage = normalized;
  const entry = normalizeStageOverrideEntry(state.workflow.stageOverrides?.[normalized] || {});
  const enabledEl = $("#wf-stage-enabled");
  const promptEl = $("#wf-stage-prompt");
  const toolsEl = $("#wf-stage-tools");
  if (enabledEl) enabledEl.checked = entry.enabled;
  if (promptEl) promptEl.value = entry.system_prompt;
  if (toolsEl) toolsEl.value = entry.tools;
  const warningText = String(state.workflow.stageOverrideWarnings?.[normalized] || "").trim();
  renderWorkflowStageSelector(normalized);
  renderWorkflowStageOverrideContext(normalized, entry, warningText);
  renderWorkflowStagePromptPreview(normalized, entry);
}

function resetWorkflowStageOverrideControls(stageId = "") {
  const token = String(stageId || activeWorkflowStageForOverrides()).trim().toLowerCase();
  const normalized = WORKFLOW_STAGE_ORDER.includes(token) ? token : activeWorkflowStageForOverrides();
  const enabledEl = $("#wf-stage-enabled");
  const promptEl = $("#wf-stage-prompt");
  const toolsEl = $("#wf-stage-tools");
  if (enabledEl) enabledEl.checked = true;
  if (promptEl) promptEl.value = "";
  if (toolsEl) toolsEl.value = "";
  if (state.workflow.stageOverrideWarnings) {
    delete state.workflow.stageOverrideWarnings[normalized];
  }
  state.workflow.stageOverrideStage = normalized;
  readWorkflowStageOverrideControls();
  queueWorkflowStageOverrideSync();
}

function focusWorkflowStageOverrideToActive() {
  const activeToken = String(
    state.pipeline.activeStageId
    || state.workflow.activeStep
    || state.workflow.focusHintStage
    || "",
  )
    .trim()
    .toLowerCase();
  if (!WORKFLOW_STAGE_ORDER.includes(activeToken)) return false;
  state.workflow.stageOverrideStage = activeToken;
  state.pipeline.activeStageId = activeToken;
  renderStageDetail(activeToken);
  applyWorkflowStageOverrideControls(activeToken);
  return true;
}

function hasWorkflowStageOverrides() {
  const bag = state.workflow.stageOverrides || {};
  return Object.values(bag).some((entry) => {
    const normalized = normalizeStageOverrideEntry(entry);
    return !normalized.enabled || normalized.system_prompt || normalized.tools;
  });
}

function buildWorkflowStageOverrideConfig() {
  const overrides = state.workflow.stageOverrides || {};
  const agents = {};
  const toolMapping = {};
  WORKFLOW_STAGE_ORDER.forEach((stageId) => {
    const entry = normalizeStageOverrideEntry(overrides[stageId] || {});
    if (!entry.enabled || entry.system_prompt) {
      agents[stageId] = pruneEmpty({
        enabled: entry.enabled,
        system_prompt: entry.system_prompt,
      });
    }
    if (entry.tools) {
      toolMapping[stageId] = entry.tools
        .split(/[,\n]/)
        .map((token) => String(token || "").trim())
        .filter(Boolean);
    }
  });
  return {
    config: {},
    agents,
    metadata: {
      tool_mapping: toolMapping,
      source: "workflow_studio",
      updated_at: new Date().toISOString(),
    },
  };
}

async function syncWorkflowStageOverridesToRun() {
  const runRel = normalizePathString($("#run-select")?.value || selectedRunRel() || "");
  if (!runRel || !hasWorkflowStageOverrides()) {
    const hidden = $("#federlicht-agent-config");
    if (hidden) hidden.value = "";
    state.workflow.stageOverridePath = "";
    return;
  }
  const path = `${runRel}/report_notes/workflow_stage_overrides.json`;
  const payload = buildWorkflowStageOverrideConfig();
  await fetchJSON("/api/files", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      path,
      content: `${JSON.stringify(payload, null, 2)}\n`,
    }),
  });
  const hidden = $("#federlicht-agent-config");
  if (hidden) hidden.value = path;
  state.workflow.stageOverridePath = path;
}

function queueWorkflowStageOverrideSync() {
  readWorkflowStageOverrideControls();
  if (state.workflow.stageOverrideSyncTimer) {
    window.clearTimeout(state.workflow.stageOverrideSyncTimer);
  }
  state.workflow.stageOverrideSyncTimer = window.setTimeout(() => {
    syncWorkflowStageOverridesToRun().catch((err) => {
      appendLog(`[workflow] stage override sync failed: ${err}\n`);
    });
  }, 260);
}

function setWorkflowStudioOpen(open, { stageId = "" } = {}) {
  const panel = $("#workflow-studio-panel");
  const toggleButtons = [
    $("#workflow-studio-toggle"),
    $("#workflow-studio-toggle-global"),
  ].filter(Boolean);
  const wrap = $("#logs-wrap");
  if (!panel || !wrap) return;
  const wasOpen = Boolean(state.workflow.studioOpen);
  const next = Boolean(open);
  state.workflow.studioOpen = next;
  if (next && !wasOpen) {
    panel.hidden = false;
    resetDragOffset(panel);
  }
  panel.classList.toggle("open", next);
  panel.setAttribute("aria-hidden", next ? "false" : "true");
  if ("inert" in panel) {
    panel.inert = !next;
  }
  if (!next && wasOpen) {
    panel.hidden = true;
    resetDragOffset(panel);
  }
  wrap.classList.toggle("workflow-studio-open", next);
  toggleButtons.forEach((toggleBtn) => {
    toggleBtn.textContent = next ? "Studio 닫기" : "Workflow Studio";
    toggleBtn.classList.toggle("is-active", next);
    toggleBtn.setAttribute("aria-pressed", next ? "true" : "false");
  });
  if (next) {
    const stage = String(
      stageId
      || state.workflow.focusHintStage
      || state.pipeline.activeStageId
      || "overview",
    )
      .trim()
      .toLowerCase() || "overview";
    if (stage && stage !== "overview" && stage !== "all") {
      state.workflow.focusHintStage = stage;
    }
    state.workflow.studioFocusStage = "overview";
    renderWorkflowStudioPanel("overview");
  }
  try {
    localStorage.setItem(WORKFLOW_STUDIO_OPEN_KEY, next ? "true" : "false");
  } catch (err) {
    // ignore
  }
}

function syncWorkflowStudioBindings() {
  const panel = $("#workflow-studio-panel");
  if (!panel) return;
  panel.querySelectorAll("[data-bind-target]").forEach((el) => {
    const bindEl = el;
    const targetSel = bindEl.getAttribute("data-bind-target") || "";
    const target = $(targetSel);
    if (!target) return;
    const copyOptions = bindEl.getAttribute("data-bind-copy-options") === "true";
    if (copyOptions && bindEl instanceof HTMLSelectElement && target instanceof HTMLSelectElement) {
      const prior = bindEl.value;
      bindEl.innerHTML = target.innerHTML;
      if (Array.from(bindEl.options).some((opt) => opt.value === prior)) {
        bindEl.value = prior;
      }
    }
    if (bindEl instanceof HTMLInputElement && bindEl.type === "checkbox" && target instanceof HTMLInputElement) {
      bindEl.checked = Boolean(target.checked);
      return;
    }
    if ("value" in bindEl && "value" in target) {
      bindEl.value = target.value;
    }
  });
  const profileEl = $("#wf-feder-profile");
  if (profileEl) {
    const profile = resolveActiveAgentProfileItem();
    profileEl.textContent = profile
      ? `${profile.label || profile.id} (${profile.id}/${profile.source || "builtin"})`
      : "default";
  }
  const caps = normalizeAskCapabilities(state.ask.capabilities || ASK_CAPABILITY_FALLBACK);
  const enabledCaps = [...(caps.tools || []), ...(caps.skills || []), ...(caps.mcp || [])]
    .filter((entry) => entry?.enabled !== false)
    .map((entry) => ({
      id: String(entry?.id || "").trim(),
      label: String(entry?.label || entry?.id || "").trim(),
      description: String(entry?.description || "").trim(),
    }))
    .filter((entry) => Boolean(entry.id || entry.label));
  const toolsEl = $("#wf-feder-tools");
  if (toolsEl) {
    const labels = enabledCaps
      .map((entry) => String(entry.label || entry.id || "").trim())
      .filter(Boolean)
      .slice(0, 6);
    toolsEl.textContent = labels.length ? labels.join(", ") : "runtime tools (auto)";
  }
  const knownToolsEl = $("#wf-stage-tools-known");
  if (knownToolsEl) {
    const ids = Array.from(new Set(enabledCaps.map((entry) => entry.id).filter(Boolean))).slice(0, 12);
    knownToolsEl.textContent = ids.length
      ? `사용 가능 도구: ${ids.join(", ")}`
      : "사용 가능 도구: 현재 활성화된 런타임 도구가 없습니다.";
  }
  const toolHelpEl = $("#wf-stage-tool-help");
  if (toolHelpEl) {
    const rows = enabledCaps
      .filter((entry) => entry.id || entry.label)
      .slice(0, 12)
      .map((entry) => {
        const label = String(entry.label || entry.id || "").trim();
        const desc = String(entry.description || "").trim();
        return `
          <div class="workflow-studio-tool-item" title="${escapeHtml(desc || label)}">
            <code>${escapeHtml(entry.id || label)}</code>
            <span>${escapeHtml(desc || label)}</span>
          </div>
        `;
      });
    toolHelpEl.innerHTML = rows.join("");
    toolHelpEl.classList.toggle("is-empty", rows.length === 0);
  }
  const datalist = $("#wf-stage-tool-suggestions");
  if (datalist) {
    const options = Array.from(new Set(enabledCaps.map((entry) => entry.id).filter(Boolean))).slice(0, 30);
    datalist.innerHTML = options.map((id) => `<option value="${escapeHtml(id)}"></option>`).join("");
  }
  const qualitySelect = $("#wf-quality-iterations");
  if (qualitySelect instanceof HTMLSelectElement) {
    const current = String(getQualityIterations());
    if (qualitySelect.value !== current) {
      qualitySelect.value = current;
    }
    const qualitySelected = workflowIsStageSelected("quality");
    qualitySelect.disabled = Boolean(state.workflow.running);
    qualitySelect.title = qualitySelected
      ? "Quality stage 반복 횟수(critic/reviser/evaluator)를 설정합니다."
      : "Quality stage가 비활성화되어 현재 값은 저장되며 활성화 시 적용됩니다.";
  }
}

function renderWorkflowStudioPanel(stageId = "") {
  const panel = $("#workflow-studio-panel");
  if (!panel) return;
  const requestedStage = String(stageId || "").trim().toLowerCase();
  if (requestedStage && requestedStage !== "overview" && requestedStage !== "all") {
    state.workflow.focusHintStage = requestedStage;
  }
  const activeStageToken = String(
    state.pipeline.activeStageId
    || state.workflow.activeStep
    || state.workflow.focusHintStage
    || "overview",
  )
    .trim()
    .toLowerCase() || "overview";
  if (activeStageToken && activeStageToken !== "overview" && activeStageToken !== "all") {
    state.workflow.focusHintStage = activeStageToken;
  }
  state.workflow.studioFocusStage = "overview";
  const spotlightStage = String(state.workflow.focusHintStage || activeStageToken || "overview")
    .trim()
    .toLowerCase() || "overview";
  const overrideStage = WORKFLOW_STAGE_ORDER.includes(spotlightStage)
    ? spotlightStage
    : activeWorkflowStageForOverrides();
  const focusDef = STAGE_DEFS.find((item) => item.id === spotlightStage);
  let focusNodeLabel = "전체 파이프라인";
  if (spotlightStage === "federhav") {
    focusNodeLabel = `${currentAskAgentDisplayName()} (governing agent)`;
  } else if (spotlightStage === "feather") {
    focusNodeLabel = "Feather (수집/정리)";
  } else if (spotlightStage === "result") {
    focusNodeLabel = "Result (산출물)";
  } else if (focusDef) {
    focusNodeLabel = `${focusDef.label} (${focusDef.id})`;
  }
  const stageHeader = `Workflow Studio · ${focusNodeLabel}`;
  setText("#stage-detail-title", stageHeader);
  const focusHint = $("#wf-focus-hint");
  if (focusHint) {
    const focusHelp = focusDef
      ? focusDef.desc
      : (spotlightStage === "federhav"
        ? `${currentAskAgentDisplayName()}는 user 요청을 해석해 run/workflow/action 제안을 조율합니다.`
        : (spotlightStage === "feather"
          ? "Feather 단계에서 입력/검색/아카이브 수집 옵션을 조정하고 실행합니다."
          : (spotlightStage === "result"
            ? "Result 단계는 현재 산출 파일 확인/재실행 전략 선택 지점입니다."
            : "전체 파이프라인을 한 화면에서 조정합니다.")));
    focusHint.innerHTML = `<strong>현재 선택 노드:</strong> ${escapeHtml(focusNodeLabel)} <span class="workflow-focus-sep">·</span> ${escapeHtml(focusHelp)}`;
  }
  panel.querySelectorAll("[data-stage-scope]").forEach((section) => {
    const token = section.getAttribute("data-stage-scope") || "";
    const focused = token === "feather"
      ? spotlightStage === "feather"
      : token === "federlicht"
        ? (WORKFLOW_STAGE_ORDER.includes(spotlightStage) || spotlightStage === "result")
        : token === "quality"
          ? spotlightStage === "quality"
          : false;
    section.classList.remove("is-hidden");
    section.classList.toggle("is-focus", focused);
  });
  renderWorkflowStageSelector(overrideStage);
  applyWorkflowStageOverrideControls(overrideStage);
  syncWorkflowStudioBindings();
}

function setCapabilityStudioStatus(message) {
  const el = $("#cap-studio-status");
  if (el) {
    el.textContent = String(message || "Ready.");
  }
}

function askStorageKey(key) {
  return `federnett-ask-${key}`;
}

function normalizeAskLlmBackend(value) {
  const token = String(value || "").trim().toLowerCase();
  if (token === "codex_cli" || token === "codex-cli" || token === "codex" || token === "cli") {
    return "codex_cli";
  }
  return "openai_api";
}

function normalizeAskRuntimeMode(value) {
  const token = String(value || "").trim().toLowerCase();
  if (token === "deepagent" || token === "agentic" || token === "on" || token === "true" || token === "1") {
    return "deepagent";
  }
  if (token === "off" || token === "false" || token === "0" || token === "disabled" || token === "none") {
    return "off";
  }
  return "auto";
}

function normalizeAskReasoningEffort(value, fallback = "off") {
  const next = String(value || "").trim().toLowerCase();
  if (ASK_REASONING_EFFORT_CHOICES.has(next)) return next;
  const fallbackToken = String(fallback || "").trim().toLowerCase();
  if (ASK_REASONING_EFFORT_CHOICES.has(fallbackToken)) return fallbackToken;
  return "off";
}

function normalizeAskReasoningEffortOptional(value) {
  const next = String(value || "").trim().toLowerCase();
  return ASK_REASONING_EFFORT_CHOICES.has(next) ? next : "";
}

function normalizeModelToken(value) {
  return String(value || "").trim();
}

function normalizeCodexModelToken(value) {
  const token = normalizeModelToken(value);
  if (!token) return "";
  const lowered = token.toLowerCase();
  if (
    lowered === "$openai_model"
    || lowered === "${openai_model}"
    || lowered === "%openai_model%"
    || lowered === "$openai_model_vision"
    || lowered === "${openai_model_vision}"
  ) {
    return token;
  }
  if (token.startsWith("$") || (token.startsWith("${") && token.endsWith("}"))) {
    return token;
  }
  if (token.startsWith("%") && token.endsWith("%")) {
    return token;
  }
  return lowered;
}

function isCodexModelToken(value) {
  const token = String(value || "").trim().toLowerCase();
  return Boolean(token) && token.includes("codex");
}

function llmDefaults() {
  const defaults = state.info?.llm_defaults;
  return defaults && typeof defaults === "object" ? defaults : {};
}

function isOpenaiModelToken(value) {
  const token = normalizeModelToken(value).toLowerCase();
  return token === "$openai_model" || token === "${openai_model}" || token === "%openai_model%";
}

function isOpenaiVisionModelToken(value) {
  const token = normalizeModelToken(value).toLowerCase();
  return token === "$openai_model_vision" || token === "${openai_model_vision}";
}

function isCodexModelPlaceholderToken(value) {
  const token = normalizeModelToken(value).toLowerCase();
  return token === "$codex_model" || token === "${codex_model}" || token === "%codex_model%";
}

function openaiModelHint() {
  const hint = normalizeModelToken(
    llmDefaults().openai_model
    || window?.FEDERNETT_OPENAI_MODEL_HINT
    || "",
  );
  if (!hint || isCodexModelToken(hint)) return "gpt-4o-mini";
  return hint;
}

function openaiVisionModelHint() {
  const hint = normalizeModelToken(
    llmDefaults().openai_model_vision
    || window?.FEDERNETT_OPENAI_MODEL_VISION_HINT
    || openaiModelHint(),
  );
  if (!hint || isCodexModelToken(hint)) return openaiModelHint();
  return hint;
}

function codexModelHint() {
  const hint = normalizeCodexModelToken(
    llmDefaults().codex_model
    || window?.FEDERNETT_CODEX_MODEL_HINT
    || "$CODEX_MODEL",
  );
  return hint || "$CODEX_MODEL";
}

function uniqueTokens(values) {
  const out = [];
  const seen = new Set();
  (values || []).forEach((item) => {
    const token = String(item || "").trim();
    if (!token) return;
    if (seen.has(token)) return;
    seen.add(token);
    out.push(token);
  });
  return out;
}

function openaiModelPresetOptions() {
  const defaults = [openaiModelHint(), openaiVisionModelHint(), "$OPENAI_MODEL", "$OPENAI_MODEL_VISION"];
  const presets = MODEL_PRESET_OPTIONS.filter((token) => {
    const normalized = normalizeModelToken(token).toLowerCase();
    if (!normalized) return false;
    if (normalized.includes("codex")) return false;
    return true;
  });
  return uniqueTokens([...defaults, ...presets]);
}

function codexModelPresetOptions() {
  const codexDefaults = [
    codexModelHint(),
    "$CODEX_MODEL",
    "${CODEX_MODEL}",
    "%CODEX_MODEL%",
  ];
  const codexPresets = MODEL_PRESET_OPTIONS.filter((token) => {
    const normalized = normalizeModelToken(token).toLowerCase();
    return Boolean(normalized && normalized.includes("codex"));
  });
  const codexFromInfo = Array.isArray(state.info?.llm_defaults?.codex_model_options)
    ? state.info.llm_defaults.codex_model_options
    : [];
  return uniqueTokens(
    [...codexDefaults, ...codexFromInfo, ...codexPresets].map((token) => {
      const raw = normalizeModelToken(token);
      if (!raw) return "";
      if (raw.startsWith("$") || (raw.startsWith("%") && raw.endsWith("%"))) return raw;
      return normalizeCodexModelToken(raw);
    }),
  );
}

function modelCatalogForBackend(backend) {
  const resolved = normalizeAskLlmBackend(backend);
  if (resolved === "codex_cli") {
    return state.modelCatalog.codex?.length
      ? state.modelCatalog.codex
      : codexModelPresetOptions();
  }
  return state.modelCatalog.openai?.length
    ? state.modelCatalog.openai
    : openaiModelPresetOptions();
}

function bindModelInputCatalog(inputEl, backend) {
  if (!inputEl) return;
  const resolved = normalizeAskLlmBackend(backend);
  const listId = resolved === "codex_cli" ? "codex-model-options" : "openai-model-options";
  inputEl.setAttribute("list", listId);
  const defaultPlaceholder = resolved === "codex_cli" ? "$CODEX_MODEL" : "$OPENAI_MODEL";
  inputEl.placeholder = defaultPlaceholder;
}

function normalizeGlobalModelPolicy(raw = {}, fallbackBackend = "openai_api") {
  const backend = normalizeAskLlmBackend(raw.backend || fallbackBackend || "openai_api");
  const normalizeByBackend = (value) =>
    backend === "codex_cli" ? normalizeCodexModelToken(value) : normalizeModelToken(value);
  const runtimeDefault = normalizeAskRuntimeMode(llmDefaults().federhav_runtime_mode || "auto");
  const policy = {
    lock: raw.lock !== false,
    backend,
    model: normalizeByBackend(raw.model),
    checkModel: normalizeByBackend(raw.checkModel ?? raw.check_model),
    visionModel: normalizeByBackend(raw.visionModel ?? raw.vision_model),
    reasoningEffort: normalizeAskReasoningEffort(
      raw.reasoningEffort ?? raw.reasoning_effort,
      "off",
    ),
    federhavRuntimeMode: normalizeAskRuntimeMode(
      raw.federhavRuntimeMode ?? raw.federhav_runtime_mode ?? runtimeDefault,
    ),
    liveAutoLogContext: (raw.liveAutoLogContext ?? raw.live_auto_log_context) !== false,
    liveAutoLogChars: normalizeLiveAskLogTailChars(
      raw.liveAutoLogChars ?? raw.live_auto_log_chars,
      LIVE_ASK_LOG_TAIL_DEFAULT,
    ),
  };
  return policy;
}

function persistGlobalModelPolicy() {
  try {
    localStorage.setItem(
      GLOBAL_MODEL_POLICY_KEY,
      JSON.stringify({
        lock: Boolean(state.modelPolicy.lock),
        backend: state.modelPolicy.backend,
        model: state.modelPolicy.model,
        checkModel: state.modelPolicy.checkModel,
        visionModel: state.modelPolicy.visionModel,
        reasoningEffort: state.modelPolicy.reasoningEffort || "off",
        federhavRuntimeMode: state.modelPolicy.federhavRuntimeMode || "auto",
        liveAutoLogContext: state.modelPolicy.liveAutoLogContext !== false,
        liveAutoLogChars: normalizeLiveAskLogTailChars(
          state.modelPolicy.liveAutoLogChars,
          LIVE_ASK_LOG_TAIL_DEFAULT,
        ),
      }),
    );
  } catch (err) {
    // ignore
  }
}

function loadGlobalModelPolicy() {
  let stored = null;
  try {
    const raw = localStorage.getItem(GLOBAL_MODEL_POLICY_KEY);
    stored = raw ? JSON.parse(raw) : null;
  } catch (err) {
    stored = null;
  }
  const backendFallback = normalizeAskLlmBackend(state.modelPolicy.backend || "openai_api");
  state.modelPolicy = normalizeGlobalModelPolicy(stored || state.modelPolicy, backendFallback);
}

function renderGlobalModelPolicyControls() {
  const backendEl = $("#global-llm-backend");
  const modelEl = $("#global-model");
  const checkEl = $("#global-check-model");
  const visionEl = $("#global-vision-model");
  const reasoningEl = $("#global-reasoning-effort");
  const runtimeEl = $("#global-federhav-runtime-mode");
  const autoLogEl = $("#global-live-auto-log");
  const logTailEl = $("#global-live-log-tail-size");
  const lockEl = $("#global-model-lock");
  if (backendEl) backendEl.value = state.modelPolicy.backend;
  if (modelEl && modelEl.value !== state.modelPolicy.model) modelEl.value = state.modelPolicy.model || "";
  if (checkEl && checkEl.value !== state.modelPolicy.checkModel) checkEl.value = state.modelPolicy.checkModel || "";
  if (visionEl && visionEl.value !== state.modelPolicy.visionModel) visionEl.value = state.modelPolicy.visionModel || "";
  if (reasoningEl) reasoningEl.value = state.modelPolicy.reasoningEffort || "off";
  if (runtimeEl) runtimeEl.value = normalizeAskRuntimeMode(state.modelPolicy.federhavRuntimeMode || "auto");
  if (autoLogEl) autoLogEl.checked = state.modelPolicy.liveAutoLogContext !== false;
  if (logTailEl) {
    const token = String(
      normalizeLiveAskLogTailChars(state.modelPolicy.liveAutoLogChars, LIVE_ASK_LOG_TAIL_DEFAULT),
    );
    if (logTailEl.value !== token) logTailEl.value = token;
  }
  if (lockEl) lockEl.checked = Boolean(state.modelPolicy.lock);
  syncModelInputCatalogBindings();
}

function readGlobalModelPolicyControls() {
  return normalizeGlobalModelPolicy(
    {
      lock: $("#global-model-lock")?.checked ?? state.modelPolicy.lock,
      backend: $("#global-llm-backend")?.value || state.modelPolicy.backend,
      model: $("#global-model")?.value || "",
      checkModel: $("#global-check-model")?.value || "",
      visionModel: $("#global-vision-model")?.value || "",
      reasoningEffort: $("#global-reasoning-effort")?.value || "off",
      federhavRuntimeMode: $("#global-federhav-runtime-mode")?.value || state.modelPolicy.federhavRuntimeMode || "auto",
      liveAutoLogContext: $("#global-live-auto-log")?.checked ?? state.modelPolicy.liveAutoLogContext,
      liveAutoLogChars: $("#global-live-log-tail-size")?.value ?? state.modelPolicy.liveAutoLogChars,
    },
    state.modelPolicy.backend,
  );
}

function policySnapshotFromSource(source = "") {
  const token = String(source || "").trim().toLowerCase();
  if (token === "ask") {
    return normalizeGlobalModelPolicy(
      {
        ...state.modelPolicy,
        backend: normalizeAskLlmBackend(state.modelPolicy.backend || "openai_api"),
        model: normalizeModelToken(state.modelPolicy.model || ""),
        reasoningEffort: normalizeAskReasoningEffort(state.modelPolicy.reasoningEffort || "off", "off"),
      },
      state.modelPolicy.backend,
    );
  }
  return normalizeGlobalModelPolicy(
    {
      ...state.modelPolicy,
      backend: normalizeAskLlmBackend(state.modelPolicy.backend || "openai_api"),
      model: normalizeModelToken(state.modelPolicy.model || ""),
      checkModel: normalizeModelToken(state.modelPolicy.checkModel || ""),
      visionModel: normalizeModelToken(state.modelPolicy.visionModel || ""),
      reasoningEffort: normalizeAskReasoningEffort(state.modelPolicy.reasoningEffort || "off", "off"),
    },
    state.modelPolicy.backend,
  );
}

function applyGlobalModelPolicy(rawPolicy = {}, options = {}) {
  if (globalModelSyncGuard) return state.modelPolicy;
  const persist = options.persist !== false;
  const announce = Boolean(options.announce);
  const next = normalizeGlobalModelPolicy(rawPolicy, state.modelPolicy.backend);
  globalModelSyncGuard = true;
  try {
    state.modelPolicy = next;
    if (persist) persistGlobalModelPolicy();
    renderGlobalModelPolicyControls();

    const featherBackend = $("#feather-llm-backend");
    const featherModel = $("#feather-model");
    if (featherBackend) featherBackend.value = next.backend;
    if (featherModel) featherModel.value = next.model || "";
    bindModelInputCatalog(featherModel, next.backend);
    $("#feather-agentic-policy-note")?.classList.remove("is-error");

    const federBackend = $("#federlicht-llm-backend");
    const federModel = $("#federlicht-model");
    const federCheck = $("#federlicht-check-model");
    const federVision = $("#federlicht-model-vision");
    const federReasoning = $("#federlicht-reasoning-effort");
    if (federBackend) federBackend.value = next.backend;
    if (federModel) federModel.value = next.model || "";
    if (federCheck) federCheck.value = next.checkModel || "";
    if (federVision) federVision.value = next.visionModel || "";
    if (federReasoning) federReasoning.value = next.reasoningEffort || "off";
    syncFederlichtModelControls({ announce: false });

    state.ask.llmBackend = next.backend;
    state.ask.reasoningEffort = next.reasoningEffort || "off";
    state.ask.runtimeMode = normalizeAskRuntimeMode(next.federhavRuntimeMode || "auto");
    state.liveAsk.autoLogContext = next.liveAutoLogContext !== false;
    state.liveAsk.autoLogChars = normalizeLiveAskLogTailChars(
      next.liveAutoLogChars,
      LIVE_ASK_LOG_TAIL_DEFAULT,
    );
    setAskModelInputValue(next.model || "");
    saveAskActionPrefs();
    saveLiveAskPrefs();
    syncLiveAskPrefsInputs();
    syncAskActionPolicyInputs();

    syncModelInputCatalogBindings();
    document.dispatchEvent(new CustomEvent("federnett:model-policy-updated"));
    if (announce) {
      appendLog(
        `[model-policy] applied backend=${next.backend} model=${next.model || "-"} lock=${next.lock ? "on" : "off"}\n`,
      );
    }
    return state.modelPolicy;
  } finally {
    globalModelSyncGuard = false;
  }
}

function maybeSyncGlobalModelPolicyFromSource(source = "") {
  if (!state.modelPolicy.lock) return;
  if (globalModelSyncGuard) return;
  const snapshot = policySnapshotFromSource(source);
  applyGlobalModelPolicy(snapshot, { persist: true, announce: false });
}

function isCommonOpenaiDefaultModel(value) {
  const token = normalizeModelToken(value).toLowerCase();
  return token === "gpt-4o-mini"
    || token === "gpt-4o"
    || token === "gpt-4.1-mini"
    || token === "gpt-4.1";
}

function openaiReasoningApiSupported() {
  const raw = llmDefaults().openai_reasoning_api;
  if (typeof raw === "boolean") return raw;
  // Safe default for older/partial backends that don't expose compatibility metadata.
  return false;
}

function supportsReasoningEffortForModel(modelToken, backend) {
  const normalizedBackend = normalizeAskLlmBackend(backend);
  if (normalizedBackend === "codex_cli") return true;
  if (normalizedBackend === "openai_api" && !openaiReasoningApiSupported()) return false;
  let token = normalizeModelToken(modelToken).toLowerCase();
  if (!token) return false;
  if (isOpenaiModelToken(token)) {
    token = openaiModelHint().toLowerCase();
  }
  if (isOpenaiVisionModelToken(token)) {
    token = openaiVisionModelHint().toLowerCase();
  }
  if (isCodexModelPlaceholderToken(token)) {
    return false;
  }
  if (isCodexModelToken(token)) {
    return false;
  }
  if (!token) return false;
  return token.startsWith("gpt-5")
    || token.startsWith("o1")
    || token.startsWith("o3")
    || token.startsWith("o4")
    || token.includes("reason");
}

function resolveAskReasoningPolicy({ backend, modelToken, reasoningEffort }) {
  const normalizedBackend = normalizeAskLlmBackend(backend);
  const requested = normalizeAskReasoningEffort(reasoningEffort, "off");
  const resolvedModelToken = normalizeModelToken(modelToken)
    || (normalizedBackend === "codex_cli" ? "$CODEX_MODEL" : openaiModelHint());
  const compatible = supportsReasoningEffortForModel(resolvedModelToken, normalizedBackend);
  if (!requested || requested === "off") {
    return {
      requestEffort: "",
      displayEffort: "off",
      compatible,
    };
  }
  if (!compatible) {
    return {
      requestEffort: "",
      displayEffort: "off",
      compatible: false,
    };
  }
  return {
    requestEffort: requested,
    displayEffort: requested,
    compatible: true,
  };
}

function sanitizeFederlichtModelConfig(raw = {}) {
  const backend = normalizeAskLlmBackend(raw.backend || "openai_api");
  let model = normalizeModelToken(raw.model);
  let checkModel = normalizeModelToken(raw.checkModel);
  let visionModel = normalizeModelToken(raw.visionModel);
  let reasoningEffort = normalizeAskReasoningEffortOptional(raw.reasoningEffort);
  const notes = [];
  const defaultOpenaiModel = openaiModelHint();
  const defaultOpenaiVision = openaiVisionModelHint();
  const defaultCodexModel = codexModelHint();
  const gatewayReasoningSupported = backend === "codex_cli" || openaiReasoningApiSupported();

  if (backend === "openai_api") {
    if (!model || isOpenaiModelToken(model)) {
      model = defaultOpenaiModel;
      notes.push(`OpenAI backend model resolved -> ${defaultOpenaiModel}`);
    } else if (isCodexModelToken(model) || isCodexModelPlaceholderToken(model)) {
      model = defaultOpenaiModel;
      notes.push(`OpenAI backend에서는 Codex 계열 모델을 사용할 수 없어 ${defaultOpenaiModel}로 고정했습니다.`);
    }
    if (!checkModel || isOpenaiModelToken(checkModel)) {
      checkModel = model || defaultOpenaiModel;
      notes.push(`OpenAI backend check model resolved -> ${checkModel}`);
    } else if (isCodexModelToken(checkModel) || isCodexModelPlaceholderToken(checkModel)) {
      checkModel = model || defaultOpenaiModel;
      notes.push(`OpenAI backend check model을 ${checkModel}로 자동 조정했습니다.`);
    }
    if (isOpenaiVisionModelToken(visionModel)) {
      visionModel = defaultOpenaiVision;
      notes.push(`OpenAI backend vision model resolved -> ${defaultOpenaiVision}`);
    } else if (isCodexModelToken(visionModel) || isCodexModelPlaceholderToken(visionModel)) {
      visionModel = defaultOpenaiVision;
      notes.push(`OpenAI backend vision model을 ${defaultOpenaiVision}로 자동 조정했습니다.`);
    }
  } else {
    const modelBefore = model;
    const checkBefore = checkModel;
    const visionBefore = visionModel;
    model = normalizeCodexModelToken(model);
    checkModel = normalizeCodexModelToken(checkModel);
    visionModel = normalizeCodexModelToken(visionModel);
    if (model && modelBefore && model !== modelBefore) {
      notes.push(`Codex backend model normalized -> ${model}`);
    }
    if (checkModel && checkBefore && checkModel !== checkBefore) {
      notes.push(`Codex backend check model normalized -> ${checkModel}`);
    }
    if (visionModel && visionBefore && visionModel !== visionBefore) {
      notes.push(`Codex backend vision model normalized -> ${visionModel}`);
    }
    if (
      !model
      || isOpenaiModelToken(model)
      || isCommonOpenaiDefaultModel(model)
      || model === "${OPENAI_MODEL}"
      || model === "%OPENAI_MODEL%"
    ) {
      model = defaultCodexModel;
      notes.push(`Codex backend model resolved -> ${defaultCodexModel}`);
    }
    if (!checkModel || isOpenaiModelToken(checkModel) || isCommonOpenaiDefaultModel(checkModel)) {
      checkModel = model;
      notes.push(`Codex backend check model resolved -> ${checkModel}`);
    }
    if (visionModel && (isOpenaiVisionModelToken(visionModel) || isCommonOpenaiDefaultModel(visionModel))) {
      visionModel = openaiVisionModelHint();
      notes.push(`Codex backend vision model은 ${visionModel}로 유지됩니다.`);
    }
  }

  const reasoningTarget = checkModel || model;
  const reasoningCompatible = supportsReasoningEffortForModel(reasoningTarget, backend);
  const reasoningRequested = Boolean(reasoningEffort && reasoningEffort !== "off");
  if (!gatewayReasoningSupported && reasoningRequested) {
    notes.push("공식 OpenAI endpoint가 아니면 reasoning_effort를 기본 비활성화합니다.");
  }
  if (reasoningRequested && !reasoningCompatible) {
    reasoningEffort = "";
    notes.push("현재 모델/백엔드 조합은 reasoning_effort를 지원하지 않아 자동으로 비활성화했습니다.");
  }

  return {
    backend,
    model,
    checkModel,
    visionModel,
    reasoningEffort,
    reasoningCompatible,
    gatewayReasoningSupported,
    notes,
  };
}

function latestActiveToolHint() {
  const timeline = Array.isArray(state.ask.activityTimeline) ? state.ask.activityTimeline : [];
  const ignored = new Set(["source_index", "web_research", "llm_generate"]);
  for (let idx = timeline.length - 1; idx >= 0; idx -= 1) {
    const event = timeline[idx] || {};
    const status = String(event.status || "").trim().toLowerCase();
    if (status !== "running" && status !== "done") continue;
    const id = String(event.id || "").trim().toLowerCase();
    if (!id || ignored.has(id)) continue;
    const message = String(event.message || "").trim();
    return {
      id,
      label: id.length > 24 ? `${id.slice(0, 24)}...` : id,
      message,
    };
  }
  return null;
}

function renderWorkflowRuntimeConfig(configOverride = null) {
  const host = $("#workflow-runtime");
  if (!host) return;
  const current = configOverride || sanitizeFederlichtModelConfig({
    backend: $("#federlicht-llm-backend")?.value || state.modelPolicy.backend,
    model: $("#federlicht-model")?.value || state.modelPolicy.model,
    checkModel: $("#federlicht-check-model")?.value || state.modelPolicy.checkModel,
    visionModel: $("#federlicht-model-vision")?.value || state.modelPolicy.visionModel,
    reasoningEffort: $("#federlicht-reasoning-effort")?.value || state.modelPolicy.reasoningEffort,
  });
  const chip = (label, value, extraClass = "") =>
    `<span class="workflow-runtime-chip ${extraClass}"><strong>${escapeHtml(label)}</strong>${escapeHtml(value || "-")}</span>`;
  const reasoningLabel = current.reasoningEffort || "off";
  const modelLabel = current.model || openaiModelHint();
  const checkLabel = current.checkModel || modelLabel;
  const visionLabel = current.visionModel || openaiVisionModelHint();
  const gatewayLabel = current.backend === "openai_api"
    ? (current.gatewayReasoningSupported ? "openai-api" : "compat-safe")
    : "codex-cli";
  const chips = [
    chip("backend", current.backend),
    chip("model", modelLabel),
    chip("reasoning", reasoningLabel, current.reasoningCompatible ? "" : "is-warning"),
  ];
  if (checkLabel && checkLabel !== modelLabel) {
    chips.push(chip("check", checkLabel));
  }
  if (visionLabel && visionLabel !== modelLabel) {
    chips.push(chip("vision", visionLabel));
  }
  if (!current.gatewayReasoningSupported) {
    chips.push(chip("gateway", gatewayLabel, "is-warning"));
  }
  const toolHint = latestActiveToolHint();
  if (toolHint) {
    chips.push(chip("tool", toolHint.label));
  }
  const hasSignal = Boolean(chips.length)
    && (
      Boolean(current.notes?.length)
      || Boolean(state.workflow.running)
      || Boolean(state.workflow.hasError)
      || Boolean(toolHint)
    );
  if (!hasSignal) {
    host.classList.add("is-empty");
    host.innerHTML = "";
    return;
  }
  host.classList.remove("is-empty");
  host.innerHTML = chips.join("");
}

function renderFederlichtRuntimeSummary(configOverride = null) {
  const host = $("#federlicht-runtime-summary");
  const notesHost = $("#federlicht-runtime-notes");
  const gatewayChip = $("#federlicht-runtime-gateway");
  if (!host) return;
  const current = configOverride || sanitizeFederlichtModelConfig({
    backend: $("#federlicht-llm-backend")?.value || state.modelPolicy.backend,
    model: $("#federlicht-model")?.value || state.modelPolicy.model,
    checkModel: $("#federlicht-check-model")?.value || state.modelPolicy.checkModel,
    visionModel: $("#federlicht-model-vision")?.value || state.modelPolicy.visionModel,
    reasoningEffort: $("#federlicht-reasoning-effort")?.value || state.modelPolicy.reasoningEffort,
  });
  const chip = (label, value, extraClass = "") =>
    `<span class="runtime-summary-chip ${extraClass}"><strong>${escapeHtml(label)}</strong>${escapeHtml(value || "-")}</span>`;
  const reasoningLabel = current.reasoningEffort || "off";
  const gatewayLabel = current.backend === "openai_api"
    ? (current.gatewayReasoningSupported ? "openai-api" : "compat-safe")
    : "codex-cli";
  host.innerHTML = `
    ${chip("backend", current.backend)}
    ${chip("model", current.model || openaiModelHint())}
    ${chip("check", current.checkModel || current.model || openaiModelHint())}
    ${chip("vision", current.visionModel || openaiVisionModelHint())}
    ${chip("reasoning", reasoningLabel, current.reasoningCompatible ? "" : "is-warning")}
  `;
  if (gatewayChip) {
    gatewayChip.textContent = `gateway: ${gatewayLabel}`;
    gatewayChip.classList.toggle("is-warning", !current.gatewayReasoningSupported);
  }
  if (notesHost) {
    const notes = Array.isArray(current.notes) ? current.notes.filter(Boolean) : [];
    const sticky = String(state.workflow.runtimeNoticeSticky || "").trim();
    if (notes.length) {
      const noteText = notes.join(" | ");
      state.workflow.runtimeNoticeSticky = noteText;
      notesHost.textContent = noteText;
    } else if (sticky) {
      notesHost.textContent = sticky;
    } else {
      notesHost.textContent = "실행 전에 backend/model/check/reasoning 자동 조정 결과를 확인하세요.";
    }
  }
}

function syncFederlichtModelControls(options = {}) {
  const announce = Boolean(options.announce);
  const forceBackendDefaults = Boolean(options.forceBackendDefaults);
  const backendEl = $("#federlicht-llm-backend");
  const modelEl = $("#federlicht-model");
  const checkModelEl = $("#federlicht-check-model");
  const visionModelEl = $("#federlicht-model-vision");
  const reasoningEl = $("#federlicht-reasoning-effort");
  const policyFallback = normalizeGlobalModelPolicy(state.modelPolicy, state.modelPolicy.backend);
  const rawModel = normalizeModelToken(modelEl?.value);
  const rawCheckModel = normalizeModelToken(checkModelEl?.value);
  const rawVisionModel = normalizeModelToken(visionModelEl?.value);
  const next = sanitizeFederlichtModelConfig({
    backend: backendEl?.value || policyFallback.backend,
    model: modelEl?.value || policyFallback.model,
    checkModel: checkModelEl?.value || policyFallback.checkModel,
    visionModel: visionModelEl?.value || policyFallback.visionModel,
    reasoningEffort: reasoningEl?.value || policyFallback.reasoningEffort,
  });
  if (backendEl && backendEl.value !== next.backend) backendEl.value = next.backend;
  const keepModelBlank = !forceBackendDefaults && !rawModel;
  const keepCheckBlank = !forceBackendDefaults && !rawCheckModel;
  const keepVisionBlank = !forceBackendDefaults && !rawVisionModel;
  if (modelEl && !(keepModelBlank && next.model) && modelEl.value !== next.model) modelEl.value = next.model;
  if (checkModelEl && !(keepCheckBlank && next.checkModel) && checkModelEl.value !== next.checkModel) {
    checkModelEl.value = next.checkModel;
  }
  if (visionModelEl && !(keepVisionBlank && next.visionModel) && visionModelEl.value !== next.visionModel) {
    visionModelEl.value = next.visionModel;
  }
  if (forceBackendDefaults) {
    if (next.backend === "codex_cli") {
      const forcedCodex = codexModelHint();
      if (modelEl && modelEl.value !== forcedCodex) {
        modelEl.value = forcedCodex;
        next.model = forcedCodex;
      }
      if (checkModelEl && (!checkModelEl.value || isCommonOpenaiDefaultModel(checkModelEl.value))) {
        checkModelEl.value = forcedCodex;
        next.checkModel = forcedCodex;
      }
    } else {
      const forcedOpenai = openaiModelHint();
      if (modelEl && (isCodexModelToken(modelEl.value) || isCodexModelPlaceholderToken(modelEl.value))) {
        modelEl.value = forcedOpenai;
        next.model = forcedOpenai;
      }
      if (checkModelEl && (isCodexModelToken(checkModelEl.value) || isCodexModelPlaceholderToken(checkModelEl.value))) {
        checkModelEl.value = forcedOpenai;
        next.checkModel = forcedOpenai;
      }
    }
  }
  bindModelInputCatalog(modelEl, next.backend);
  bindModelInputCatalog(checkModelEl, next.backend);
  bindModelInputCatalog(visionModelEl, next.backend);
  if (reasoningEl) {
    reasoningEl.disabled = !next.reasoningCompatible;
    reasoningEl.title = next.reasoningCompatible
      ? "Reasoning effort (off/low/medium/high/extra_high). off는 reasoning_effort 인자를 전송하지 않습니다."
      : "현재 모델/백엔드 조합에서는 reasoning_effort가 비활성화됩니다.";
    if (next.reasoningEffort) {
      reasoningEl.value = next.reasoningEffort;
    } else if (!next.reasoningCompatible) {
      reasoningEl.value = "off";
    }
  }
  renderWorkflowRuntimeConfig(next);
  renderFederlichtRuntimeSummary(next);
  const digest = next.notes.join(" | ");
  if (announce && digest && digest !== state.workflow.runtimeNoticeDigest) {
    next.notes.forEach((line) => appendLog(`[federlicht:model] ${line}\n`));
  }
  if (digest) {
    state.workflow.runtimeNoticeDigest = digest;
  } else if (!String(state.workflow.runtimeNoticeSticky || "").trim()) {
    state.workflow.runtimeNoticeDigest = "";
  }
  return next;
}

function normalizeAskProfileToken(value) {
  const raw = String(value || "").trim();
  if (!raw) return "";
  const cleaned = raw.replace(/[^a-zA-Z0-9_-]/g, "");
  return cleaned.slice(0, 80);
}

function normalizeAskAgentToken(value) {
  const raw = String(value || "").trim();
  if (!raw) return "";
  const cleaned = raw.replace(/[^a-zA-Z0-9_.-]/g, "");
  return cleaned.slice(0, 80);
}

function resolveAskAgentLabel() {
  const override = normalizeAskAgentToken(state.ask.agentOverride || "");
  if (override) return override;
  return resolveActiveAgentProfileItem()?.id || "federhav";
}

function currentAskAgentDisplayName() {
  const override = normalizeAskAgentToken(state.ask.agentOverride || "");
  if (override) return override;
  const active = resolveActiveAgentProfileItem();
  const preferred = String(active?.name || active?.label || active?.id || "").trim();
  if (preferred) return preferred;
  const fallback = String(resolveAskAgentLabel() || "").trim();
  if (!fallback) return "FederHav";
  if (fallback.toLowerCase() === "federhav") return "FederHav";
  return fallback;
}

function refreshLiveAskAgentLabel() {
  const agentName = currentAskAgentDisplayName();
  const label = $("#live-ask-label");
  if (label) {
    label.textContent = `${agentName}에게 요청`;
  }
  updateLiveAskInputMeta();
}

function parseAskProfileSelectorToken(raw) {
  const text = String(raw || "").trim();
  if (!text) return { id: "", source: "" };
  let source = "";
  let id = text;
  const parts = text.split(":");
  if (parts.length === 2) {
    const sourceCandidate = String(parts[0] || "").trim().toLowerCase();
    if (sourceCandidate === "site" || sourceCandidate === "builtin") {
      source = sourceCandidate;
      id = String(parts[1] || "").trim();
    }
  }
  return {
    id: normalizeAskProfileToken(id),
    source,
  };
}

function findAgentProfileByToken(raw) {
  const { id, source } = parseAskProfileSelectorToken(raw);
  if (!id) return null;
  const list = Array.isArray(state.agentProfiles.list) ? state.agentProfiles.list : [];
  let match = list.find((item) => item.id === id && (!source || item.source === source));
  if (match) return match;
  const lowered = id.toLowerCase();
  match = list.find(
    (item) => String(item.id || "").toLowerCase() === lowered && (!source || item.source === source),
  );
  return match || null;
}

function parseAskControlCommand(raw) {
  const text = String(raw || "").trim();
  if (!text.startsWith("/")) {
    return { type: "", question: text };
  }
  const modeMatch = text.match(/^\/(plan|act)\b(?:\s+([\s\S]+))?$/i);
  if (modeMatch) {
    return {
      type: String(modeMatch[1] || "").toLowerCase(),
      question: String(modeMatch[2] || "").trim(),
    };
  }
  const profileMatch = text.match(/^\/profile\b(?:\s+(.+))?$/i);
  if (profileMatch) {
    return {
      type: "profile",
      token: String(profileMatch[1] || "").trim(),
      question: "",
    };
  }
  const agentMatch = text.match(/^\/agent\b(?:\s+(.+))?$/i);
  if (agentMatch) {
    return {
      type: "agent",
      token: String(agentMatch[1] || "").trim(),
      question: "",
    };
  }
  const runtimeMatch = text.match(/^\/runtime\b(?:\s+(.+))?$/i);
  if (runtimeMatch) {
    return {
      type: "runtime",
      token: String(runtimeMatch[1] || "").trim(),
      question: "",
    };
  }
  if (/^\/help\b/i.test(text)) {
    return {
      type: "help",
      question: "",
    };
  }
  return { type: "", question: text };
}

async function applyAskControlCommand(raw) {
  const parsed = parseAskControlCommand(raw);
  const type = String(parsed.type || "").toLowerCase();
  if (!type) {
    return { handled: false, question: String(parsed.question || "").trim() };
  }
  if (type === "plan" || type === "act") {
    setAskActionMode(type, { persist: true });
    const inlineQuestion = String(parsed.question || "").trim();
    if (!inlineQuestion) {
      setAskStatus(
        `실행 모드 변경: ${type}${type === "act" ? ` · 파일쓰기허용=${state.ask.allowArtifactWrites ? "on" : "off"}` : ""}`,
      );
      return { handled: true, question: "" };
    }
    return { handled: false, question: inlineQuestion };
  }
  if (type === "profile") {
    const token = String(parsed.token || "").trim();
    if (!token) {
      setAskStatus(`현재 profile=${ensureAskProfileId()}`);
      return { handled: true, question: "" };
    }
    const target = findAgentProfileByToken(token);
    if (!target) {
      setAskStatus(`프로필을 찾을 수 없습니다: ${token} (예: /profile default 또는 /profile site:123456)`);
      return { handled: true, question: "" };
    }
    if (state.agentProfiles.activeId === target.id && state.agentProfiles.activeSource === target.source) {
      maybeReloadAskHistory();
    } else {
      await openAgentProfile(target.id, target.source);
    }
    renderAskHistory();
    renderLiveAskThread();
    refreshLiveAskAgentLabel();
    setAskStatus(`profile 변경: ${target.id} (${target.source})`);
    return { handled: true, question: "" };
  }
  if (type === "agent") {
    const token = String(parsed.token || "").trim();
    if (!token) {
      setAskStatus(`현재 agent=${resolveAskAgentLabel()}`);
      return { handled: true, question: "" };
    }
    const lower = token.toLowerCase();
    if (lower === "-" || lower === "default" || lower === "profile") {
      state.ask.agentOverride = "";
      saveAskActionPrefs();
      renderAskHistory();
      refreshLiveAskAgentLabel();
      setAskStatus(`agent override 해제 · profile 기반(${resolveAskAgentLabel()})`);
      return { handled: true, question: "" };
    }
    const nextAgent = normalizeAskAgentToken(token);
    if (!nextAgent) {
      setAskStatus("agent 토큰이 비어 있습니다. 영문/숫자/._- 조합으로 입력하세요.");
      return { handled: true, question: "" };
    }
    state.ask.agentOverride = nextAgent;
    saveAskActionPrefs();
    renderAskHistory();
    refreshLiveAskAgentLabel();
    setAskStatus(`agent 변경: ${nextAgent}`);
    return { handled: true, question: "" };
  }
  if (type === "help") {
    setAskStatus(
      "운영 명령: /plan [질문], /act [질문], /profile <id|source:id>, /agent <id|default>, /runtime <auto|deepagent|off>, /help",
    );
    return { handled: true, question: "" };
  }
  if (type === "runtime") {
    const token = String(parsed.token || "").trim();
    if (!token) {
      setAskStatus(`현재 runtime=${normalizeAskRuntimeMode(state.ask.runtimeMode || "auto")}`);
      return { handled: true, question: "" };
    }
    const next = normalizeAskRuntimeMode(token);
    setAskRuntimeMode(next, { persist: true });
    setAskStatus(`runtime 변경: ${next}`);
    return { handled: true, question: "" };
  }
  return { handled: false, question: String(parsed.question || "").trim() };
}

function loadAskActionPrefs() {
  try {
    const raw = localStorage.getItem(ASK_ACTION_PREF_KEY);
    if (!raw) return;
    const parsed = JSON.parse(raw);
    const mode = String(parsed?.mode || "").trim().toLowerCase();
    if (mode === "act" || mode === "plan") {
      state.ask.actionMode = mode;
    }
    state.ask.allowArtifactWrites = Boolean(parsed?.allow_artifacts);
    state.ask.llmBackend = normalizeAskLlmBackend(parsed?.llm_backend);
    state.ask.runtimeMode = normalizeAskRuntimeMode(parsed?.runtime_mode);
    state.ask.reasoningEffort = normalizeAskReasoningEffort(parsed?.reasoning_effort, "off");
    state.ask.agentOverride = normalizeAskAgentToken(parsed?.agent_override);
  } catch (err) {
    // ignore invalid local storage payload
  }
}

function saveAskActionPrefs() {
  localStorage.setItem(
    ASK_ACTION_PREF_KEY,
    JSON.stringify({
      mode: state.ask.actionMode || "plan",
      allow_artifacts: Boolean(state.ask.allowArtifactWrites),
      llm_backend: normalizeAskLlmBackend(state.ask.llmBackend),
      runtime_mode: normalizeAskRuntimeMode(state.ask.runtimeMode),
      reasoning_effort: normalizeAskReasoningEffort(state.ask.reasoningEffort, "off"),
      agent_override: normalizeAskAgentToken(state.ask.agentOverride || ""),
    }),
  );
}

function setAskActionMode(mode, { persist = true } = {}) {
  const next = String(mode || "").trim().toLowerCase() === "act" ? "act" : "plan";
  state.ask.actionMode = next;
  if (persist) saveAskActionPrefs();
  syncAskActionPolicyInputs();
}

function setAskLlmBackend(backend, { persist = true } = {}) {
  state.ask.llmBackend = normalizeAskLlmBackend(backend);
  if (persist) saveAskActionPrefs();
  syncAskActionPolicyInputs();
  if (persist && !state.ask.busy && !state.liveAsk.busy) {
    if (state.ask.llmBackend === "codex_cli") {
      setAskStatus("Codex CLI Auth는 로컬 codex 로그인 세션을 사용합니다. ChatGPT 구독 상태는 앱에서 직접 조회할 수 없습니다.");
    } else {
      setAskStatus("OpenAI API backend를 사용합니다. 모델/요금은 API 설정 기준입니다.");
    }
  }
}

function setAskRuntimeMode(mode, { persist = true } = {}) {
  state.ask.runtimeMode = normalizeAskRuntimeMode(mode);
  if (persist) saveAskActionPrefs();
  syncAskActionPolicyInputs();
  if (persist && !state.ask.busy && !state.liveAsk.busy) {
    setAskStatus(`FederHav 런타임 모드: ${state.ask.runtimeMode}`);
  }
}

function setAskReasoningEffort(value, { persist = true } = {}) {
  state.ask.reasoningEffort = normalizeAskReasoningEffort(value, state.ask.reasoningEffort);
  if (persist) saveAskActionPrefs();
  syncAskActionPolicyInputs();
  if (persist && !state.ask.busy && !state.liveAsk.busy) {
    setAskStatus(`FederHav 추론 강도: ${state.ask.reasoningEffort}`);
  }
}

function askBackendInputValue() {
  return normalizeAskLlmBackend(
    state.modelPolicy.backend
    || state.ask.llmBackend
    || "openai_api",
  );
}

function askModelInputValue() {
  return String(
    state.modelPolicy.model
    || "",
  ).trim();
}

function askRuntimeModeInputValue() {
  return normalizeAskRuntimeMode(
    $("#live-ask-runtime-mode")?.value
    || state.ask.runtimeMode
    || llmDefaults().federhav_runtime_mode
    || "auto",
  );
}

function askReasoningInputValue() {
  return normalizeAskReasoningEffort(
    state.modelPolicy.reasoningEffort
    || state.ask.reasoningEffort,
    state.ask.reasoningEffort,
  );
}

function setAskModelInputValue(value) {
  const next = String(value || "").trim();
  const askModel = $("#ask-model");
  const liveModel = $("#live-ask-model");
  if (askModel && askModel.value !== next) askModel.value = next;
  if (liveModel && liveModel.value !== next) liveModel.value = next;
}

function normalizeAskCapabilities(payload) {
  const source = payload && typeof payload === "object" ? payload : ASK_CAPABILITY_FALLBACK;
  const term = String(source.term || ASK_CAPABILITY_FALLBACK.term || "Capability Packs");
  const normalizeList = (rawList, group) => {
    if (!Array.isArray(rawList)) return [];
    return rawList
      .map((item, idx) => {
        const id = String(item?.id || "").trim().toLowerCase() || `${group}_${idx + 1}`;
        const label = String(item?.label || id).trim();
        const description = String(item?.description || "").trim();
        const enabled = item?.enabled === false ? false : true;
        return { id, label, description, enabled, group };
      })
      .filter((item) => Boolean(item.id));
  };
  const tools = normalizeList(source.tools || [], "tools");
  const skills = normalizeList(source.skills || [], "skills");
  let mcp = normalizeList(source.mcp || [], "mcp");
  if (!mcp.length) {
    mcp = [
      {
        id: "mcp_none",
        label: "MCP 없음",
        description: "등록된 MCP 서버가 없습니다.",
        enabled: false,
        group: "mcp",
      },
    ];
  }
  const packs = Array.isArray(source.packs)
    ? source.packs
      .map((pack, idx) => {
        const id = String(pack?.id || `pack_${idx + 1}`).trim();
        const label = String(pack?.label || id).trim();
        const description = String(pack?.description || "").trim();
        const items = Array.isArray(pack?.items)
          ? pack.items.map((item) => String(item || "").trim()).filter(Boolean).slice(0, 18)
          : [];
        if (!id || !label) return null;
        return { id, label, description, items };
      })
      .filter(Boolean)
    : [];
  return { term, tools, skills, mcp, packs };
}

function normalizeCapabilityRegistry(payload) {
  const source = payload && typeof payload === "object" ? payload : {};
  const normalizeKeywords = (raw) => {
    const sourceList = Array.isArray(raw) ? raw : [raw];
    const out = [];
    const seen = new Set();
    sourceList.forEach((item) => {
      String(item || "")
        .split(/[,/\n]+/)
        .map((token) => token.trim().toLowerCase())
        .filter(Boolean)
        .forEach((token) => {
          if (seen.has(token)) return;
          seen.add(token);
          out.push(token.slice(0, 48));
        });
    });
    return out.slice(0, 16);
  };
  const normalize = (list, kind) => {
    if (!Array.isArray(list)) return [];
    return list
      .map((item, idx) => {
        const id = String(item?.id || `${kind}_${idx + 1}`).trim().toLowerCase();
        const label = String(item?.label || id).trim();
        const description = String(item?.description || "").trim();
        const enabled = item?.enabled === false ? false : true;
        const endpoint = String(item?.endpoint || "").trim();
        const transport = String(item?.transport || "").trim();
        const keywords = normalizeKeywords(item?.keywords || item?.trigger_keywords || []);
        const actionRaw = item?.action && typeof item.action === "object" ? item.action : {};
        const actionKind = String(actionRaw.kind || actionRaw.type || "none").trim().toLowerCase();
        const actionTarget = String(actionRaw.target || "").trim();
        const actionConfirm = actionRaw.confirm === false ? false : true;
        if (!id) return null;
        return {
          id,
          label,
          description,
          enabled,
          endpoint,
          transport,
          keywords,
          action: {
            kind: actionKind,
            target: actionTarget,
            confirm: actionConfirm,
          },
        };
      })
      .filter(Boolean);
  };
  return {
    tools: normalize(source.tools || [], "tool"),
    skills: normalize(source.skills || [], "skill"),
    mcp_servers: normalize(source.mcp_servers || [], "mcp"),
  };
}

function askCapabilityEntries() {
  const cap = normalizeAskCapabilities(state.ask.capabilities);
  return [...cap.tools, ...cap.skills, ...cap.mcp];
}

function capabilityKindClass(entry) {
  const group = String(entry?.group || "").trim().toLowerCase();
  if (group === "tools" || group === "tool") return "is-kind-tools";
  if (group === "skills" || group === "skill") return "is-kind-skills";
  if (group === "mcp") return "is-kind-mcp";
  return "";
}

function capabilityChipHtml(entry, status) {
  const classes = ["ask-cap-chip"];
  const kindClass = capabilityKindClass(entry);
  if (kindClass) classes.push(kindClass);
  if (status === "running") classes.push("is-running");
  else if (status === "done") classes.push("is-done");
  else if (status === "disabled" || entry.enabled === false) classes.push("is-disabled");
  else if (status === "error") classes.push("is-error");
  const titleParts = [];
  if (entry.group) titleParts.push(entry.group.toUpperCase());
  if (entry.description) titleParts.push(entry.description);
  const title = titleParts.join(" · ");
  return `<span class="${classes.join(" ")}" title="${escapeHtml(title)}">${escapeHtml(entry.label)}</span>`;
}

function resetAskActivityState() {
  const entries = askCapabilityEntries();
  const next = {};
  entries.forEach((entry) => {
    next[entry.id] = entry.enabled === false ? "disabled" : "idle";
  });
  state.ask.activity = next;
  state.ask.activityTimeline = [];
  state.ask.traceShowHistory = false;
  state.ask.activityStatus = "대기";
  renderAskCapabilities();
}

function setAskActivity(id, status, message = "", meta = null) {
  const token = String(id || "").trim().toLowerCase();
  if (!token) return;
  const normalizedStatus = String(status || "idle").trim().toLowerCase();
  const metaObj = meta && typeof meta === "object" ? meta : {};
  const traceId = String(metaObj?.trace_id || "").trim();
  const toolId = String(metaObj?.tool_id || "").trim();
  const durationRaw = Number(metaObj?.duration_ms);
  const tokenRaw = Number(metaObj?.token_est);
  const durationMs = Number.isFinite(durationRaw) && durationRaw >= 0 ? Math.round(durationRaw) : null;
  const tokenEst = Number.isFinite(tokenRaw) && tokenRaw >= 0 ? Math.round(tokenRaw) : null;
  const hasCacheHit = Object.prototype.hasOwnProperty.call(metaObj, "cache_hit");
  const cacheHit = hasCacheHit ? Boolean(metaObj?.cache_hit) : null;
  state.ask.activity[token] = normalizedStatus || "idle";
  if (message) {
    state.ask.activityStatus = String(message);
  } else {
    state.ask.activityStatus =
      normalizedStatus === "running" ? "작업 실행 중..." : normalizedStatus === "done" ? "완료" : "대기";
  }
  state.ask.activityTimeline = [...(Array.isArray(state.ask.activityTimeline) ? state.ask.activityTimeline : []), {
    id: token,
    status: normalizedStatus || "idle",
    message: String(message || "").trim(),
    at: new Date().toISOString(),
    trace_id: traceId,
    tool_id: toolId || token,
    duration_ms: durationMs,
    token_est: tokenEst,
    cache_hit: cacheHit,
  }].slice(-140);
  renderAskCapabilities();
  renderWorkflowRuntimeConfig();
}

function askTraceMetaText(event) {
  if (!event || typeof event !== "object") return "";
  const parts = [];
  const traceId = String(event.trace_id || "").trim();
  const toolId = String(event.tool_id || "").trim();
  const durationRaw = Number(event.duration_ms);
  const tokenRaw = Number(event.token_est);
  const hasCacheHit = Object.prototype.hasOwnProperty.call(event, "cache_hit");
  if (traceId) parts.push(`trace=${traceId}`);
  if (toolId) parts.push(`tool=${toolId}`);
  if (Number.isFinite(durationRaw) && durationRaw >= 0) parts.push(`dur=${Math.round(durationRaw)}ms`);
  if (Number.isFinite(tokenRaw) && tokenRaw >= 0) parts.push(`tok~${Math.round(tokenRaw)}`);
  if (hasCacheHit) parts.push(`cache=${event.cache_hit ? "hit" : "miss"}`);
  return parts.join(" · ");
}

function applyAskTraceTimeline(result, options = {}) {
  const trace = result && typeof result === "object" && result.trace && typeof result.trace === "object"
    ? result.trace
    : null;
  const steps = Array.isArray(trace?.steps) ? trace.steps : [];
  if (!steps.length) return false;
  if (options?.reset) {
    resetAskActivityState();
  }
  const traceId = String(trace?.trace_id || "").trim();
  steps.forEach((step) => {
    if (!step || typeof step !== "object") return;
    const id = String(step.id || step.step || "").trim().toLowerCase();
    if (!id) return;
    const status = String(step.status || "done").trim().toLowerCase();
    const message = String(step.message || "").trim();
    setAskActivity(id, status, message, {
      ...step,
      trace_id: String(step.trace_id || traceId || "").trim(),
      tool_id: String(step.tool_id || id).trim(),
    });
  });
  return true;
}

function renderAskCapabilities() {
  const host = $("#ask-capability-grid");
  const statusEl = $("#ask-activity-status");
  const entries = askCapabilityEntries();
  if (host) {
    if (!entries.length) {
      host.innerHTML = '<span class="muted">표시할 도구 정보가 없습니다.</span>';
    } else {
      host.innerHTML = entries
        .map((entry) => {
          const status = String(state.ask.activity?.[entry.id] || (entry.enabled === false ? "disabled" : "idle"));
          return capabilityChipHtml(entry, status);
        })
        .join("");
    }
  }
  if (statusEl) {
    statusEl.textContent = state.ask.activityStatus || "대기";
    const hasRunning = Object.values(state.ask.activity || {}).some((value) => value === "running");
    statusEl.classList.toggle("is-active", hasRunning);
  }
  renderAskCapabilityDetail();
  renderAskSourcesTrace();
  renderCapabilityStudio();
}

function renderAskCapabilityDetail() {
  const host = $("#ask-capability-detail");
  if (!host) return;
  const cap = normalizeAskCapabilities(state.ask.capabilities);
  const packs = Array.isArray(cap.packs) ? cap.packs : [];
  if (!packs.length) {
    host.innerHTML = `<p class="muted">${escapeHtml(cap.term || "Capability Packs")} 정보가 아직 없습니다.</p>`;
    return;
  }
  host.innerHTML = packs
    .map((pack) => {
      const items = Array.isArray(pack.items) ? pack.items : [];
      return `
        <article class="ask-cap-pack">
          <strong>${escapeHtml(pack.label || pack.id)}</strong>
          ${pack.description ? `<p>${escapeHtml(pack.description)}</p>` : ""}
          ${items.length ? `<code>${escapeHtml(items.slice(0, 8).join(", "))}${items.length > 8 ? " ..." : ""}</code>` : ""}
        </article>
      `;
    })
    .join("");
}

function setAskCapabilityDetailOpen(open) {
  state.ask.capabilityDetailOpen = Boolean(open);
  const host = $("#ask-capability-detail");
  if (!host) return;
  host.classList.toggle("open", state.ask.capabilityDetailOpen);
  host.setAttribute("aria-hidden", state.ask.capabilityDetailOpen ? "false" : "true");
  $("#ask-cap-pack-help")?.classList.toggle("is-active", state.ask.capabilityDetailOpen);
}

function setAskCapabilityManagerOpen(open) {
  state.ask.capabilityManagerOpen = Boolean(open);
  const panel = $("#ask-capability-manager");
  if (!panel) return;
  panel.classList.toggle("open", state.ask.capabilityManagerOpen);
  panel.setAttribute("aria-hidden", state.ask.capabilityManagerOpen ? "false" : "true");
  $("#ask-cap-manage-toggle")?.classList.toggle("is-active", state.ask.capabilityManagerOpen);
  if (state.ask.capabilityManagerOpen) {
    setAskCapabilityDetailOpen(false);
  }
}

function renderAskCapabilityManager() {
  const host = $("#ask-cap-manager-list");
  if (!host) return;
  const registry = normalizeCapabilityRegistry(state.ask.capabilityRegistry || {});
  const groups = [
    { key: "tools", label: "Custom Tools" },
    { key: "skills", label: "Custom Skills" },
    { key: "mcp_servers", label: "Custom MCP Servers" },
  ];
  host.innerHTML = groups
    .map((group) => {
      const entries = Array.isArray(registry[group.key]) ? registry[group.key] : [];
      const itemsHtml = entries.length
        ? entries
          .map((entry) => `
              <div class="ask-cap-entry">
                <div class="meta">
                  <strong>${escapeHtml(entry.label || entry.id)}</strong>
                  <span>
                    ${escapeHtml(entry.id)}
                    ${entry.action?.kind ? ` · action:${escapeHtml(entry.action.kind)}` : ""}
                    ${entry.endpoint ? ` · ${escapeHtml(entry.endpoint)}` : ""}
                  </span>
                  ${entry.keywords?.length ? `<span>keywords: ${escapeHtml(entry.keywords.join(", "))}</span>` : ""}
                </div>
                <button type="button" class="ghost mini" data-cap-remove-kind="${escapeHtml(group.key)}" data-cap-remove-id="${escapeHtml(entry.id)}">삭제</button>
              </div>
            `)
          .join("")
        : '<p class="muted">등록된 항목이 없습니다.</p>';
      return `
        <section class="ask-cap-manager-group">
          <h4>${escapeHtml(group.label)}</h4>
          <div class="ask-cap-manager-items">${itemsHtml}</div>
        </section>
      `;
    })
    .join("");
  host.querySelectorAll("[data-cap-remove-kind][data-cap-remove-id]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const kind = btn.getAttribute("data-cap-remove-kind") || "";
      const id = btn.getAttribute("data-cap-remove-id") || "";
      if (!kind || !id) return;
      const next = normalizeCapabilityRegistry(state.ask.capabilityRegistry || {});
      const list = Array.isArray(next[kind]) ? next[kind] : [];
      next[kind] = list.filter((entry) => String(entry.id || "") !== id);
      try {
        await saveAskCapabilityRegistry(next);
        setAskStatus(`Capability removed: ${id}`);
      } catch (err) {
        setAskStatus(`Capability remove failed: ${err}`);
      }
    });
  });
}

function renderCapabilityStudio() {
  const runtimeHost = $("#cap-studio-runtime-grid");
  if (runtimeHost) {
    const entries = askCapabilityEntries();
    runtimeHost.innerHTML = entries.length
      ? entries
        .map((entry) => {
          const status = String(state.ask.activity?.[entry.id] || (entry.enabled === false ? "disabled" : "idle"));
          return capabilityChipHtml(entry, status);
        })
        .join("")
      : '<span class="muted">표시할 도구 정보가 없습니다.</span>';
  }
  const packHost = $("#cap-studio-pack-detail");
  if (packHost) {
    const cap = normalizeAskCapabilities(state.ask.capabilities);
    const packs = Array.isArray(cap.packs) ? cap.packs : [];
    packHost.innerHTML = packs.length
      ? packs
        .map((pack) => {
          const items = Array.isArray(pack.items) ? pack.items : [];
          return `
            <article class="ask-cap-pack">
              <strong>${escapeHtml(pack.label || pack.id)}</strong>
              ${pack.description ? `<p>${escapeHtml(pack.description)}</p>` : ""}
              ${items.length ? `<code>${escapeHtml(items.slice(0, 8).join(", "))}${items.length > 8 ? " ..." : ""}</code>` : ""}
            </article>
          `;
        })
        .join("")
      : '<p class="muted">Capability Pack 정보가 아직 없습니다.</p>';
  }
  const host = $("#cap-studio-list");
  if (!host) return;
  const registry = normalizeCapabilityRegistry(state.ask.capabilityRegistry || {});
  const groups = [
    { key: "tools", label: "Custom Tools" },
    { key: "skills", label: "Custom Skills" },
    { key: "mcp_servers", label: "Custom MCP Servers" },
  ];
  host.innerHTML = groups
    .map((group) => {
      const entries = Array.isArray(registry[group.key]) ? registry[group.key] : [];
      const itemsHtml = entries.length
        ? entries
          .map((entry) => `
              <div class="ask-cap-entry">
                <div class="meta">
                  <strong>${escapeHtml(entry.label || entry.id)}</strong>
                  <span>
                    ${escapeHtml(entry.id)}
                    ${entry.action?.kind ? ` · action:${escapeHtml(entry.action.kind)}` : ""}
                    ${entry.endpoint ? ` · ${escapeHtml(entry.endpoint)}` : ""}
                  </span>
                  ${entry.keywords?.length ? `<span>keywords: ${escapeHtml(entry.keywords.join(", "))}</span>` : ""}
                </div>
                <button type="button" class="ghost mini" data-cap-studio-remove-kind="${escapeHtml(group.key)}" data-cap-studio-remove-id="${escapeHtml(entry.id)}">삭제</button>
              </div>
            `)
          .join("")
        : '<p class="muted">등록된 항목이 없습니다.</p>';
      return `
        <section class="ask-cap-manager-group">
          <h4>${escapeHtml(group.label)}</h4>
          <div class="ask-cap-manager-items">${itemsHtml}</div>
        </section>
      `;
    })
    .join("");
  host.querySelectorAll("[data-cap-studio-remove-kind][data-cap-studio-remove-id]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const kind = btn.getAttribute("data-cap-studio-remove-kind") || "";
      const id = btn.getAttribute("data-cap-studio-remove-id") || "";
      if (!kind || !id) return;
      const next = normalizeCapabilityRegistry(state.ask.capabilityRegistry || {});
      const list = Array.isArray(next[kind]) ? next[kind] : [];
      next[kind] = list.filter((entry) => String(entry.id || "") !== id);
      try {
        await saveAskCapabilityRegistry(next);
        setCapabilityStudioStatus(`Capability removed: ${id}`);
        setAskStatus(`Capability removed: ${id}`);
      } catch (err) {
        setCapabilityStudioStatus(`Capability remove failed: ${err}`);
        setAskStatus(`Capability remove failed: ${err}`);
      }
    });
  });
}

async function loadAskCapabilityRegistry(opts = {}) {
  const silent = Boolean(opts?.silent);
  try {
    const webSearch = Boolean($("#federlicht-web-search")?.checked);
    const payload = await fetchJSON(`/api/capabilities?web_search=${webSearch ? "1" : "0"}`);
    state.ask.capabilityRegistry = normalizeCapabilityRegistry(payload?.registry || {});
    if (payload?.runtime) {
      state.ask.capabilities = normalizeAskCapabilities(payload.runtime);
      resetAskActivityState();
    }
    renderAskCapabilityManager();
    renderCapabilityStudio();
    if (!silent) {
      setAskStatus("Capability registry loaded.");
      setCapabilityStudioStatus("Capability registry loaded.");
    }
  } catch (err) {
    if (!silent) {
      setAskStatus(`Capability registry load failed: ${err}`);
      setCapabilityStudioStatus(`Capability registry load failed: ${err}`);
    }
  }
}

async function saveAskCapabilityRegistry(registryPayload) {
  const webSearch = Boolean($("#federlicht-web-search")?.checked);
  const payload = await fetchJSON("/api/capabilities/save", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      registry: registryPayload,
      web_search: webSearch,
    }),
  });
  state.ask.capabilityRegistry = normalizeCapabilityRegistry(payload?.registry || {});
  if (payload?.runtime) {
    state.ask.capabilities = normalizeAskCapabilities(payload.runtime);
    resetAskActivityState();
  }
  renderAskCapabilityManager();
  renderCapabilityStudio();
}

async function addCapabilityFromStudio() {
  const kind = String($("#cap-studio-kind")?.value || "tool").trim().toLowerCase();
  const id = String($("#cap-studio-id")?.value || "").trim();
  const label = String($("#cap-studio-label")?.value || "").trim() || id;
  const description = String($("#cap-studio-desc")?.value || "").trim();
  const keywords = String($("#cap-studio-keywords")?.value || "")
    .split(/[,/\n]+/)
    .map((token) => token.trim().toLowerCase())
    .filter(Boolean)
    .slice(0, 16);
  const actionKind = String($("#cap-studio-action-kind")?.value || "none").trim().toLowerCase();
  const actionTarget = String($("#cap-studio-action-target")?.value || "").trim();
  const endpoint = String($("#cap-studio-endpoint")?.value || "").trim();
  const enabled = Boolean($("#cap-studio-enabled")?.checked);
  if (!id) {
    setCapabilityStudioStatus("Capability ID를 입력하세요.");
    setAskStatus("Capability ID를 입력하세요.");
    return;
  }
  const next = normalizeCapabilityRegistry(state.ask.capabilityRegistry || {});
  if (kind === "mcp") {
    const mcpActionKind = actionKind === "none" ? "mcp_ping" : actionKind;
    next.mcp_servers = (next.mcp_servers || []).filter((entry) => String(entry.id || "") !== id);
    next.mcp_servers.push({
      id,
      label,
      description,
      endpoint,
      enabled,
      transport: "http",
      keywords,
      action: {
        kind: mcpActionKind,
        target: actionTarget || endpoint,
        confirm: true,
      },
    });
  } else if (kind === "skill") {
    next.skills = (next.skills || []).filter((entry) => String(entry.id || "") !== id);
    next.skills.push({
      id,
      label,
      description,
      enabled,
      keywords,
      action: {
        kind: actionKind || "none",
        target: actionTarget,
        confirm: true,
      },
    });
  } else {
    next.tools = (next.tools || []).filter((entry) => String(entry.id || "") !== id);
    next.tools.push({
      id,
      label,
      description,
      enabled,
      keywords,
      action: {
        kind: actionKind || "none",
        target: actionTarget,
        confirm: true,
      },
    });
  }
  try {
    await saveAskCapabilityRegistry(next);
    const effectiveAction = kind === "mcp"
      ? (actionKind === "none" ? "mcp_ping" : actionKind)
      : (actionKind || "none");
    const statusMessage = effectiveAction === "none"
      ? `Capability saved: ${id} (메타 등록만 완료)`
      : `Capability saved: ${id} (action=${effectiveAction})`;
    setCapabilityStudioStatus(statusMessage);
    setAskStatus(statusMessage);
    if ($("#cap-studio-id")) $("#cap-studio-id").value = "";
    if ($("#cap-studio-label")) $("#cap-studio-label").value = "";
    if ($("#cap-studio-desc")) $("#cap-studio-desc").value = "";
    if ($("#cap-studio-keywords")) $("#cap-studio-keywords").value = "";
    if ($("#cap-studio-action-target")) $("#cap-studio-action-target").value = "";
    if ($("#cap-studio-endpoint")) $("#cap-studio-endpoint").value = "";
  } catch (err) {
    setCapabilityStudioStatus(`Capability save failed: ${err}`);
    setAskStatus(`Capability save failed: ${err}`);
  }
}

function syncAskActionPolicyInputs() {
  const modeInput = $("#ask-action-mode");
  const mode = state.ask.actionMode === "act" ? "act" : "plan";
  if (modeInput && modeInput.value !== mode) {
    modeInput.value = mode;
  }
  const modeHint = $("#ask-action-mode-hint");
  if (modeHint) {
    modeHint.textContent = mode === "act"
      ? "Act: FederHav 제안 자동실행(안전범위). 사이드바 Run 버튼과 독립."
      : "Plan: FederHav 제안 확인 후 실행. 사이드바 Run 버튼은 항상 직접 실행 가능.";
  }
  const modeSwitch = $("#ask-action-mode-switch");
  if (modeSwitch) {
    modeSwitch.querySelectorAll("[data-ask-mode]").forEach((btn) => {
      const token = btn.getAttribute("data-ask-mode") || "";
      btn.classList.toggle("is-on", token === mode);
      btn.setAttribute("aria-pressed", token === mode ? "true" : "false");
    });
  }
  const liveModeHint = $("#live-ask-mode-hint");
  if (liveModeHint) {
    liveModeHint.textContent = mode === "act"
      ? "Act: FederHav 제안 자동실행(안전범위). 사이드바 Run과 독립."
      : "Plan: FederHav 제안 확인 후 실행. 사이드바 Run은 직접 실행 가능.";
  }
  const modePolicyHint = mode === "act"
    ? "Act: FederHav suggested actions may auto-run in safe scope. Sidebar Run buttons are always direct."
    : "Plan: FederHav suggested actions require confirmation. Sidebar Run buttons are always direct.";
  if (modeSwitch) {
    modeSwitch.title = modePolicyHint;
  }
  const liveModeSwitch = $("#live-ask-mode-switch");
  if (liveModeSwitch) {
    liveModeSwitch.title = modePolicyHint;
    liveModeSwitch.querySelectorAll("[data-ask-mode]").forEach((btn) => {
      const token = btn.getAttribute("data-ask-mode") || "";
      btn.classList.toggle("is-on", token === mode);
      btn.setAttribute("aria-pressed", token === mode ? "true" : "false");
    });
  }
  const allowCheck = $("#ask-allow-artifacts");
  const allowWrap = $("#ask-artifact-policy") || allowCheck?.closest("label");
  const liveAllowCheck = $("#live-ask-allow-artifacts");
  const liveAllowWrap = $("#live-ask-artifact-policy") || liveAllowCheck?.closest("label");
  const showAllowPolicy = mode === "act";
  if (allowWrap) {
    allowWrap.classList.toggle("is-hidden", !showAllowPolicy);
    allowWrap.setAttribute("aria-hidden", showAllowPolicy ? "false" : "true");
  }
  if (liveAllowWrap) {
    liveAllowWrap.classList.toggle("is-hidden", !showAllowPolicy);
    liveAllowWrap.setAttribute("aria-hidden", showAllowPolicy ? "false" : "true");
  }
  if (allowCheck && allowCheck.checked !== Boolean(state.ask.allowArtifactWrites)) {
    allowCheck.checked = Boolean(state.ask.allowArtifactWrites);
  }
  if (liveAllowCheck && liveAllowCheck.checked !== Boolean(state.ask.allowArtifactWrites)) {
    liveAllowCheck.checked = Boolean(state.ask.allowArtifactWrites);
  }
  const runRel = ensureAskRunRel();
  const runLabel = runRel ? (stripSiteRunsPrefix(runRel) || runRel) : "현재 선택 run";
  const writeHint = `파일쓰기허용 시 run=${runLabel} 하위 경로에서만 쓰기 작업이 허용됩니다.`;
  if (allowCheck) {
    allowCheck.disabled = !showAllowPolicy;
    allowCheck.title = writeHint;
    allowCheck.setAttribute("aria-label", writeHint);
    if (allowWrap) {
      allowWrap.title = writeHint;
      allowWrap.setAttribute("aria-label", writeHint);
    }
  }
  if (liveAllowCheck) {
    liveAllowCheck.disabled = !showAllowPolicy;
    liveAllowCheck.title = writeHint;
    liveAllowCheck.setAttribute("aria-label", writeHint);
  }
  if (liveAllowWrap) {
    liveAllowWrap.title = writeHint;
    liveAllowWrap.setAttribute("aria-label", writeHint);
  }
  const globalPolicy = normalizeGlobalModelPolicy(state.modelPolicy, state.modelPolicy.backend);
  const backend = normalizeAskLlmBackend(globalPolicy.backend || "openai_api");
  state.ask.llmBackend = backend;
  const globalModelToken = normalizeModelToken(globalPolicy.model || "")
    || (backend === "codex_cli" ? codexModelHint() : openaiModelHint());
  setAskModelInputValue(globalModelToken);
  state.ask.reasoningEffort = normalizeAskReasoningEffort(globalPolicy.reasoningEffort || "off", "off");
  const runtimeMode = normalizeAskRuntimeMode(state.ask.runtimeMode);
  state.ask.runtimeMode = runtimeMode;
  const backendSelect = $("#ask-backend");
  const liveBackendSelect = $("#live-ask-backend");
  const liveRuntimeModeSelect = $("#live-ask-runtime-mode");
  if (backendSelect && backendSelect.value !== backend) {
    backendSelect.value = backend;
  }
  if (liveBackendSelect && liveBackendSelect.value !== backend) {
    liveBackendSelect.value = backend;
  }
  if (liveRuntimeModeSelect && liveRuntimeModeSelect.value !== runtimeMode) {
    liveRuntimeModeSelect.value = runtimeMode;
  }
  if (liveRuntimeModeSelect) {
    liveRuntimeModeSelect.title = "auto=deepagent 우선(fallback 포함), deepagent=강제, off=기본 help-agent 경로";
  }
  const modelTokenRaw = askModelInputValue();
  if (backend === "openai_api" && (isCodexModelToken(modelTokenRaw) || isCodexModelPlaceholderToken(modelTokenRaw))) {
    const fallback = openaiModelHint();
    if (modelTokenRaw !== fallback) {
      setAskModelInputValue(fallback);
      appendLog(`[ask:model] openai backend fallback -> ${fallback}\n`);
      setAskStatus(`OpenAI backend에서는 Codex 계열 모델을 사용할 수 없어 ${fallback}로 자동 전환했습니다.`);
    }
  } else if (
    backend === "codex_cli"
    && (isOpenaiModelToken(modelTokenRaw) || isOpenaiVisionModelToken(modelTokenRaw))
    && modelTokenRaw !== "$CODEX_MODEL"
  ) {
    setAskModelInputValue("$CODEX_MODEL");
  }
  const modelToken = normalizeModelToken(askModelInputValue())
    || (backend === "codex_cli" ? "$CODEX_MODEL" : openaiModelHint());
  const reasoningSelect = $("#ask-reasoning-effort");
  const liveReasoningSelect = $("#live-ask-reasoning-effort");
  const requestedReasoning = normalizeAskReasoningEffort(state.ask.reasoningEffort, "off");
  const policy = resolveAskReasoningPolicy({
    backend,
    modelToken,
    reasoningEffort: state.ask.reasoningEffort,
  });
  state.ask.reasoningEffort = policy.displayEffort;
  if (reasoningSelect) {
    if (reasoningSelect.value !== policy.displayEffort) {
      reasoningSelect.value = policy.displayEffort;
    }
    reasoningSelect.disabled = !policy.compatible;
    reasoningSelect.title = policy.compatible
      ? "FederHav 답변 추론 강도 (off/low/medium/high/extra_high). off는 reasoning_effort 인자를 전송하지 않습니다."
      : "현재 모델/백엔드 조합에서는 reasoning_effort가 비활성화됩니다.";
  }
  if (liveReasoningSelect) {
    if (liveReasoningSelect.value !== policy.displayEffort) {
      liveReasoningSelect.value = policy.displayEffort;
    }
    liveReasoningSelect.disabled = !policy.compatible;
    liveReasoningSelect.title = policy.compatible
      ? "FederHav 답변 추론 강도 (off/low/medium/high/extra_high). off는 reasoning_effort 인자를 전송하지 않습니다."
      : "현재 모델/백엔드 조합에서는 reasoning_effort가 비활성화됩니다.";
  }
  const askModelInput = $("#ask-model");
  const liveModelInput = $("#live-ask-model");
  const applyModelInputUi = (modelInput) => {
    if (!modelInput) return;
    bindModelInputCatalog(modelInput, backend);
    if (backend === "codex_cli") {
      modelInput.placeholder = "$CODEX_MODEL";
      modelInput.title = "Codex CLI Auth: 프리셋/직접입력 모두 가능합니다. 비워두면 로컬 Codex 기본 모델을 사용합니다.";
    } else {
      modelInput.placeholder = "$OPENAI_MODEL";
      modelInput.title = "OpenAI API model override (optional)";
    }
  };
  applyModelInputUi(askModelInput);
  applyModelInputUi(liveModelInput);
  const liveRuntimeNote = $("#live-ask-runtime-note");
  if (liveRuntimeNote) {
    const reasoningLabel = policy.displayEffort || "off";
    const modelLabel = modelToken || (backend === "codex_cli" ? "$CODEX_MODEL" : openaiModelHint());
    const reasoningToken = policy.compatible ? reasoningLabel : "off";
    liveRuntimeNote.textContent = `runtime=${runtimeMode} · backend=${backend} · model=${modelLabel} · reasoning=${reasoningToken}`;
    liveRuntimeNote.title = "runtime=auto는 deepagent 우선 + 실패 시 기본 경로로 fallback합니다.";
    liveRuntimeNote.hidden = false;
  }
  const runtimeFold = $("#live-ask-runtime-fold");
  if (
    runtimeFold instanceof HTMLDetailsElement
    && requestedReasoning !== "off"
    && !policy.compatible
  ) {
    runtimeFold.open = true;
  }
  renderLiveAskContextChips();
}

function askScopeValues() {
  const runRel = ensureAskRunRel();
  const profileId = ensureAskProfileId() || "default";
  const runKey = normalizePathString(runRel || "global") || "global";
  const profileKey = slugifyLabel(profileId) || "default";
  return {
    runRel,
    profileId,
    scopeKey: `${runKey}::${profileKey}`,
  };
}

function askThreadsStorageKey(scopeKey) {
  return askStorageKey(`threads-${encodeURIComponent(scopeKey || "global::default")}`);
}

function normalizeAskThreadId(value) {
  const cleaned = String(value || "")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9_-]+/g, "_")
    .replace(/^_+|_+$/g, "");
  return cleaned.slice(0, 32);
}

function createAskThread(seedTitle = "") {
  const title = String(seedTitle || "").trim().slice(0, 48) || ASK_DEFAULT_THREAD_TITLE;
  const id = normalizeAskThreadId(`t_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 6)}`);
  return {
    id: id || `t_${Date.now().toString(36)}`,
    title,
    preview: "",
    updated_at: new Date().toISOString(),
  };
}

function loadAskThreadMeta(scopeKey) {
  const raw = localStorage.getItem(askThreadsStorageKey(scopeKey));
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed
      .map((entry) => {
        const id = normalizeAskThreadId(entry?.id);
        if (!id) return null;
        return {
          id,
          title: String(entry?.title || ASK_DEFAULT_THREAD_TITLE).trim().slice(0, 48),
          preview: String(entry?.preview || "").trim().slice(0, 96),
          updated_at: String(entry?.updated_at || ""),
        };
      })
      .filter(Boolean)
      .slice(0, ASK_THREAD_LIMIT);
  } catch (err) {
    return [];
  }
}

function saveAskThreadMeta() {
  localStorage.setItem(
    askThreadsStorageKey(state.ask.scopeKey),
    JSON.stringify((state.ask.threads || []).slice(0, ASK_THREAD_LIMIT)),
  );
}

function activeAskThread() {
  return (state.ask.threads || []).find((item) => item.id === state.ask.activeThreadId) || null;
}

function renderAskThreadList() {
  const host = $("#ask-thread-list");
  if (!host) return;
  const items = Array.isArray(state.ask.threads) ? state.ask.threads : [];
  if (!items.length) {
    host.innerHTML = '<p class="muted">스레드가 없습니다.</p>';
    syncAskThreadActions();
    return;
  }
  host.innerHTML = items
    .map((item) => {
      const active = item.id === state.ask.activeThreadId;
      const title = item.title || ASK_DEFAULT_THREAD_TITLE;
      const preview = item.preview || "새 대화를 시작하세요.";
      const updated = item.updated_at ? formatDate(item.updated_at) : "-";
      return `
        <button type="button" class="ask-thread-item ${active ? "active" : ""}" data-ask-thread="${escapeHtml(item.id)}">
          <strong>${escapeHtml(title)}</strong>
          <span>${escapeHtml(preview)}</span>
          <span>${escapeHtml(updated)}</span>
        </button>
      `;
    })
    .join("");
  host.querySelectorAll("[data-ask-thread]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const threadId = btn.getAttribute("data-ask-thread") || "";
      if (!threadId || threadId === state.ask.activeThreadId) return;
      setAskActiveThread(threadId).catch((err) => setAskStatus(`스레드 전환 실패: ${err}`));
    });
  });
  syncAskThreadActions();
}

function setAskThreadPopoverOpen(open) {
  state.ask.threadPopoverOpen = Boolean(open);
  const panel = $("#ask-thread-popover");
  if (panel) {
    panel.classList.toggle("open", state.ask.threadPopoverOpen);
    panel.setAttribute("aria-hidden", state.ask.threadPopoverOpen ? "false" : "true");
  }
  $("#ask-thread-toggle")?.classList.toggle("is-active", state.ask.threadPopoverOpen);
}

function syncAskThreadActions() {
  const delBtn = $("#ask-thread-delete");
  if (!delBtn) return;
  const count = Array.isArray(state.ask.threads) ? state.ask.threads.length : 0;
  delBtn.disabled = count <= 0;
}

function askHistoryProfileId() {
  return askHistoryProfileIdForThread(state.ask.activeThreadId || ASK_DEFAULT_THREAD_ID);
}

function askHistoryProfileIdForThread(threadId) {
  const scope = askScopeValues();
  const base = normalizeAskThreadId(scope.profileId) || "default";
  const normalizedThread = normalizeAskThreadId(threadId || ASK_DEFAULT_THREAD_ID) || ASK_DEFAULT_THREAD_ID;
  return `${base}__th_${normalizedThread}`;
}

function askCurrentThreadLabel() {
  const thread = activeAskThread();
  return thread?.title || ASK_DEFAULT_THREAD_TITLE;
}

function ensureAskThreadScope(force = false) {
  const scope = askScopeValues();
  if (!force && state.ask.scopeKey === scope.scopeKey && Array.isArray(state.ask.threads) && state.ask.threads.length) {
    applyLiveAskScope(scope.scopeKey, { fallbackHistory: state.ask.history });
    return;
  }
  const previousThreadId = force ? "" : state.ask.activeThreadId;
  state.ask.runRel = scope.runRel;
  state.ask.profileId = scope.profileId;
  state.ask.scopeKey = scope.scopeKey;
  const stored = loadAskThreadMeta(scope.scopeKey);
  let threads = stored.length ? stored : [];
  if (!threads.find((item) => item.id === ASK_DEFAULT_THREAD_ID)) {
    threads.unshift({
      id: ASK_DEFAULT_THREAD_ID,
      title: ASK_DEFAULT_THREAD_TITLE,
      preview: "",
      updated_at: "",
    });
  }
  threads = threads.slice(0, ASK_THREAD_LIMIT);
  state.ask.threads = threads;
  const nextThread =
    threads.find((item) => item.id === previousThreadId)?.id
    || threads[0]?.id
    || ASK_DEFAULT_THREAD_ID;
  state.ask.activeThreadId = nextThread;
  state.ask.historyProfileId = askHistoryProfileId();
  renderAskThreadList();
  applyLiveAskScope(scope.scopeKey, { force: true, fallbackHistory: state.ask.history });
}

async function setAskActiveThread(threadId) {
  const normalized = normalizeAskThreadId(threadId);
  if (!normalized) return;
  if (!(state.ask.threads || []).find((item) => item.id === normalized)) {
    return;
  }
  state.ask.activeThreadId = normalized;
  state.ask.historyProfileId = askHistoryProfileId();
  state.ask.pendingQuestion = "";
  setAskThreadPopoverOpen(false);
  renderAskThreadList();
  await loadAskHistory(ensureAskRunRel());
}

async function createNewAskThread() {
  ensureAskThreadScope(false);
  const newThread = createAskThread("새 대화");
  state.ask.threads = [newThread, ...(state.ask.threads || [])]
    .filter((item, idx, arr) => arr.findIndex((candidate) => candidate.id === item.id) === idx)
    .slice(0, ASK_THREAD_LIMIT);
  state.ask.activeThreadId = newThread.id;
  state.ask.history = [];
  state.ask.historyProfileId = askHistoryProfileId();
  state.ask.lastAction = null;
  state.ask.lastAnswer = "";
  state.ask.lastSources = [];
  state.ask.pendingSources = [];
  state.ask.pendingQuestion = "";
  state.ask.liveAnswer = "";
  setAskThreadPopoverOpen(false);
  saveAskThreadMeta();
  renderAskThreadList();
  renderAskHistory();
  renderAskAnswer("");
  renderAskSources([]);
  renderAskActions(null, "", []);
  setAskStatus("새 스레드를 시작했습니다.");
}

async function deleteActiveAskThread() {
  ensureAskThreadScope(false);
  const current = activeAskThread();
  if (!current) {
    setAskStatus("삭제할 스레드가 없습니다.");
    return;
  }
  const count = Array.isArray(state.ask.threads) ? state.ask.threads.length : 0;
  const ok = window.confirm(
    `현재 스레드를 삭제할까요?\n- ${current.title || current.id}\n- 저장된 대화 이력 파일도 함께 삭제됩니다.`,
  );
  if (!ok) return;
  const profileForThread = askHistoryProfileIdForThread(current.id);
  try {
    await fetchJSON("/api/help/history/clear", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ run: ensureAskRunRel(), profile_id: profileForThread }),
    });
  } catch (err) {
    appendLog(`[ask] thread history clear failed: ${err}\n`);
  }
  state.ask.threads = (state.ask.threads || []).filter((item) => item.id !== current.id);
  if (!state.ask.threads.length) {
    state.ask.threads = [{
      id: ASK_DEFAULT_THREAD_ID,
      title: ASK_DEFAULT_THREAD_TITLE,
      preview: "",
      updated_at: "",
    }];
  }
  const next = state.ask.threads[0] || null;
  state.ask.activeThreadId = next?.id || ASK_DEFAULT_THREAD_ID;
  state.ask.historyProfileId = askHistoryProfileId();
  state.ask.pendingQuestion = "";
  setAskThreadPopoverOpen(false);
  saveAskThreadMeta();
  renderAskThreadList();
  if (count <= 1) {
    state.ask.history = [];
    state.ask.pendingQuestion = "";
    state.ask.lastAnswer = "";
    state.ask.lastSources = [];
    state.ask.pendingSources = [];
    state.ask.liveAnswer = "";
    renderAskHistory();
    renderAskAnswer("");
    renderAskSources([]);
    renderAskActions(null, "", []);
    setAskStatus("스레드를 삭제하고 기본 스레드를 다시 만들었습니다.");
    return;
  }
  await loadAskHistory(ensureAskRunRel());
  setAskStatus("스레드를 삭제했습니다.");
}

function updateActiveThreadMeta(nextValues = {}) {
  const thread = activeAskThread();
  if (!thread) return;
  if (nextValues.title) {
    thread.title = String(nextValues.title).trim().slice(0, 48) || thread.title;
  }
  if (nextValues.preview !== undefined) {
    thread.preview = String(nextValues.preview || "").trim().slice(0, 96);
  }
  thread.updated_at = String(nextValues.updated_at || new Date().toISOString());
  state.ask.threads = (state.ask.threads || []).sort((a, b) => {
    return String(b.updated_at || "").localeCompare(String(a.updated_at || ""));
  });
  saveAskThreadMeta();
  renderAskThreadList();
}

function renderAskHistory(_pendingTurn = null) {
  const host = $("#ask-history");
  const count = Array.isArray(state.ask.history) ? state.ask.history.length : 0;
  const liveRows = Array.isArray(state.liveAsk.history) ? state.liveAsk.history : [];
  const liveCount = liveRows.length || count;
  const runRel = ensureAskRunRel();
  const profileId = ensureAskProfileId();
  const threadLabel = askCurrentThreadLabel();
  const initialUserTurns = (Array.isArray(state.ask.history) ? state.ask.history : [])
    .filter((entry) => entry.role === "user" && String(entry.content || "").trim())
    .slice(0, 3)
    .map((entry) => String(entry.content || "").replace(/\s+/g, " ").trim())
    .filter(Boolean);
  const summaryRaw = initialUserTurns.length ? initialUserTurns.join(" / ") : threadLabel;
  const summary = summaryRaw.length > 46 ? `${summaryRaw.slice(0, 45)}…` : summaryRaw;
  const liveUserTurns = liveRows
    .filter((entry) => entry.role === "user" && String(entry.content || "").trim())
    .slice(0, 3)
    .map((entry) => String(entry.content || "").replace(/\s+/g, " ").trim())
    .filter(Boolean);
  const liveSummaryRaw = liveUserTurns.length ? liveUserTurns.join(" / ") : summaryRaw;
  const liveSummary = liveSummaryRaw.length > 46 ? `${liveSummaryRaw.slice(0, 45)}…` : liveSummaryRaw;
  const runLabel = runRel ? (stripSiteRunsPrefix(runRel) || runRel) : "";
  const agentLabel = resolveAskAgentLabel();
  const fullSummary = `스레드: ${summary} · 이력 ${count}개`;
  const tooltipSummary = `스레드: ${summaryRaw} · 이력 ${count}개${runLabel ? ` · run=${runLabel}` : ""}${profileId ? ` · profile=${profileId}` : ""}${agentLabel ? ` · agent=${agentLabel}` : ""}`;
  const liveFullSummary = liveCount > 0 ? `최근 대화 ${liveCount}개` : "대화 준비";
  const liveTooltipSummary = `스레드: ${liveSummaryRaw} · 이력 ${liveCount}개${runLabel ? ` · run=${runLabel}` : ""}${profileId ? ` · profile=${profileId}` : ""}${agentLabel ? ` · agent=${agentLabel}` : ""}`;
  if (host) {
    host.classList.add("has-content");
    host.innerHTML = `
      <span class="hint">
        ${escapeHtml(fullSummary)}
      </span>
    `;
    host.title = tooltipSummary;
    host.setAttribute("aria-label", tooltipSummary);
  }
  const liveContext = $("#live-ask-context");
  if (liveContext) {
    liveContext.textContent = liveFullSummary;
    liveContext.title = liveTooltipSummary;
    liveContext.setAttribute("aria-label", liveTooltipSummary);
  }
  renderLiveAskContextChips();
  syncAskActionPolicyInputs();
}

function renderLiveAskContextChips() {
  const runChip = $("#live-ask-chip-run");
  const modeChip = $("#live-ask-chip-mode");
  const profileChip = $("#live-ask-chip-profile");
  const agentChip = $("#live-ask-chip-agent");
  const logChip = $("#live-ask-chip-log");
  if (!runChip && !modeChip && !profileChip && !agentChip && !logChip) return;
  const runRel = normalizePathString(ensureAskRunRel() || selectedRunRel() || "");
  const runLabel = runRel ? (stripSiteRunsPrefix(runRel) || runRel) : "-";
  const profileId = ensureAskProfileId() || "default";
  const agentLabel = resolveAskAgentLabel();
  const overrideOn = Boolean(normalizeAskAgentToken(state.ask.agentOverride || ""));
  const mode = state.ask.actionMode === "act" ? "act" : "plan";
  const backend = normalizeAskLlmBackend(state.ask.llmBackend || "openai_api");
  const reasoning = normalizeAskReasoningEffort(state.ask.reasoningEffort, "off");
  const logChars = normalizeLiveAskLogTailChars(
    state.liveAsk.autoLogChars,
    LIVE_ASK_LOG_TAIL_DEFAULT,
  ).toLocaleString();
  if (runChip) {
    runChip.textContent = `run: ${runLabel}`;
    runChip.title = runRel || "선택된 run이 없습니다.";
  }
  if (modeChip) {
    const write = mode === "act" ? (state.ask.allowArtifactWrites ? "write:on" : "write:off") : "confirm";
    modeChip.textContent = `mode: ${mode} · ${write}`;
    modeChip.title = `backend=${backend} · reasoning=${reasoning}`;
  }
  if (profileChip) {
    profileChip.textContent = `profile: ${profileId}`;
    profileChip.title = "이력/메모리 스코프";
  }
  if (agentChip) {
    agentChip.textContent = overrideOn ? `agent: ${agentLabel} (override)` : `agent: ${agentLabel}`;
    agentChip.title = overrideOn ? "수동 agent 라벨 적용됨 (/agent ...)" : "활성 프로필 id를 agent 라벨로 사용";
  }
  if (logChip) {
    logChip.textContent = state.liveAsk.autoLogContext ? `context-tail: ${logChars}` : "context-tail: off";
    logChip.title = state.liveAsk.autoLogContext
      ? `state-memory + 보조로그 요약 ${logChars}자`
      : "보조로그 요약 비활성화";
  }
  refreshLiveAskAgentLabel();
}

function setAskRunButtonState(runButton, busy) {
  if (!runButton) return;
  const isLiveButton = runButton.id === "live-ask-run";
  if (isLiveButton) {
    runButton.disabled = false;
    runButton.dataset.busy = busy ? "1" : "0";
    runButton.classList.toggle("is-running", Boolean(busy));
    runButton.classList.toggle("is-stop", Boolean(busy));
    runButton.innerHTML = busy
      ? '<span class="ask-run-icon" aria-hidden="true">■</span><span class="ask-run-spinner" aria-hidden="true"></span>'
      : '<span class="ask-run-icon" aria-hidden="true">➤</span><span class="ask-run-spinner" aria-hidden="true"></span>';
    runButton.title = busy ? "진행 중... (클릭 시 중단)" : "질문 실행";
    runButton.setAttribute("aria-pressed", busy ? "true" : "false");
    return;
  }
  runButton.disabled = Boolean(busy);
  if (busy) {
    runButton.classList.add("is-running");
    runButton.innerHTML = "<span>질문 중...</span><small>처리 중</small>";
    return;
  }
  runButton.classList.remove("is-running");
  runButton.innerHTML = "<span>질문 실행</span><small>Ctrl+Enter</small>";
}

function syncLiveAskBusyControls() {
  const stopBtn = $("#live-ask-stop");
  const busy = Boolean(state.liveAsk.busy);
  const abortable = Boolean(state.liveAsk.abortController);
  if (stopBtn) {
    stopBtn.disabled = !(busy && abortable);
    stopBtn.classList.toggle("is-active", busy && abortable);
  }
  const liveBtn = $("#live-ask-run");
  if (liveBtn) {
    liveBtn.classList.toggle("is-abortable", busy && abortable);
  }
}

function isLiveAskAbortError(err) {
  const text = String(err || "").toLowerCase();
  return text.includes("abort") || text.includes("cancel") || text.includes("timeout");
}

function cancelLiveAskQuestion() {
  const controller = state.liveAsk.abortController;
  if (!controller) {
    setAskStatus("중단할 스트림이 없습니다.");
    return;
  }
  try {
    controller.abort("live_ask_user_cancelled");
    setAskStatus("질문 스트림 중단 요청을 보냈습니다...");
  } catch (err) {
    setAskStatus(`중단 요청 실패: ${err}`);
  }
}

function saveAskGeometry() {
  const panel = $("#ask-panel");
  if (!panel || !state.ask.open) return;
  clampAskPanelPosition();
  const rect = panel.getBoundingClientRect();
  const payload = {
    left: Math.max(0, Math.round(rect.left)),
    top: Math.max(0, Math.round(rect.top)),
    width: Math.max(640, Math.round(rect.width)),
    height: Math.max(340, Math.round(rect.height)),
  };
  askGeomMemory = payload;
}

function clampAskPanelPosition() {
  const panel = $("#ask-panel");
  if (!panel) return;
  const viewportW = Math.max(320, window.innerWidth);
  const viewportH = Math.max(280, window.innerHeight);
  const maxWidth = Math.max(320, viewportW - 24);
  const maxHeight = Math.max(280, viewportH - 84);
  const minWidth = Math.min(640, maxWidth);
  const minHeight = Math.min(340, maxHeight);
  const currentRect = panel.getBoundingClientRect();
  const nextWidth = Math.max(minWidth, Math.min(maxWidth, Math.round(currentRect.width)));
  const nextHeight = Math.max(minHeight, Math.min(maxHeight, Math.round(currentRect.height)));
  if (Math.abs(nextWidth - currentRect.width) > 1) {
    panel.style.width = `${nextWidth}px`;
  }
  if (Math.abs(nextHeight - currentRect.height) > 1) {
    panel.style.height = `${nextHeight}px`;
  }
  const rect = panel.getBoundingClientRect();
  const maxLeft = Math.max(12, window.innerWidth - rect.width - 12);
  const maxTop = Math.max(70, window.innerHeight - rect.height - 12);
  const left = Math.max(12, Math.min(rect.left, maxLeft));
  const top = Math.max(70, Math.min(rect.top, maxTop));
  panel.style.left = `${left}px`;
  panel.style.top = `${top}px`;
  panel.style.right = "auto";
}

function restoreAskGeometry(anchor) {
  const panel = $("#ask-panel");
  if (!panel) return;
  let restored = false;
  const fromMemory = askGeomMemory;
  const fromStorageRaw = localStorage.getItem(ASK_GEOM_KEY);
  if (fromStorageRaw) {
    localStorage.removeItem(ASK_GEOM_KEY);
  }
  if (fromMemory) {
    try {
      const parsed = fromMemory;
      if (parsed && Number(parsed.width) > 100 && Number(parsed.height) > 100) {
        const maxWidth = Math.max(320, window.innerWidth - 24);
        const maxHeight = Math.max(280, window.innerHeight - 84);
        const minWidth = Math.min(640, maxWidth);
        const minHeight = Math.min(340, maxHeight);
        const width = Math.max(minWidth, Math.min(maxWidth, Math.round(parsed.width)));
        const height = Math.max(minHeight, Math.min(maxHeight, Math.round(parsed.height)));
        panel.style.width = `${width}px`;
        panel.style.height = `${height}px`;
      }
      if (parsed && Number.isFinite(parsed.left) && Number.isFinite(parsed.top)) {
        panel.style.left = `${Math.round(parsed.left)}px`;
        panel.style.top = `${Math.round(parsed.top)}px`;
        panel.style.right = "auto";
        restored = true;
      }
    } catch (err) {
      // ignore invalid memory geometry values
    }
  }
  if (!restored && anchor && Number.isFinite(anchor.x) && Number.isFinite(anchor.y)) {
    const rect = panel.getBoundingClientRect();
    const targetLeft = Math.max(12, Math.min(anchor.x - rect.width + 40, window.innerWidth - rect.width - 12));
    const targetTop = Math.max(70, Math.min(anchor.y + 8, window.innerHeight - rect.height - 12));
    panel.style.left = `${Math.round(targetLeft)}px`;
    panel.style.top = `${Math.round(targetTop)}px`;
    panel.style.right = "auto";
  }
  clampAskPanelPosition();
}

function resetAskGeometry() {
  const panel = $("#ask-panel");
  askGeomMemory = null;
  localStorage.removeItem(ASK_GEOM_KEY);
  if (!panel) return;
  panel.style.removeProperty("left");
  panel.style.removeProperty("top");
  panel.style.removeProperty("right");
  panel.style.removeProperty("width");
  panel.style.removeProperty("height");
  window.requestAnimationFrame(() => {
    if (!state.ask.open) return;
    clampAskPanelPosition();
    saveAskGeometry();
  });
}

function ensureAskRunRel() {
  return selectedRunRel() || state.ask.runRel || "";
}

function ensureAskProfileId() {
  const active = resolveActiveAgentProfileItem();
  return active?.id || state.ask.profileId || "default";
}

async function loadAskHistory(runRel) {
  ensureAskThreadScope(false);
  const resolvedRun = runRel || "";
  const profileId = ensureAskProfileId();
  const scopedProfileId = askHistoryProfileId();
  try {
    let payload = await fetchJSON(
      `/api/help/history?run=${encodeURIComponent(resolvedRun)}&profile_id=${encodeURIComponent(scopedProfileId)}`,
    );
    let migratedLegacy = false;
    if (
      (!Array.isArray(payload?.items) || !payload.items.length)
      && state.ask.activeThreadId === ASK_DEFAULT_THREAD_ID
      && scopedProfileId !== profileId
    ) {
      try {
        const legacy = await fetchJSON(
          `/api/help/history?run=${encodeURIComponent(resolvedRun)}&profile_id=${encodeURIComponent(profileId)}`,
        );
        if (Array.isArray(legacy?.items) && legacy.items.length) {
          payload = legacy;
          migratedLegacy = true;
        }
      } catch (err) {
        // ignore legacy fallback errors
      }
    }
    const items = Array.isArray(payload?.items) ? payload.items : [];
    state.ask.history = items
      .map((item) => ({
        role: item?.role === "assistant" ? "assistant" : "user",
        content: String(item?.content || "").slice(0, 4000),
        ts: item?.ts || new Date().toISOString(),
      }))
      .slice(-40);
    state.ask.runRel = payload?.run_rel || resolvedRun;
    state.ask.profileId = profileId;
    state.ask.historyProfileId = scopedProfileId;
    state.ask.lastAction = null;
    state.ask.lastAnswer = "";
    state.ask.lastSources = [];
    state.ask.pendingSources = [];
    state.ask.liveAnswer = "";
    if (!Array.isArray(state.liveAsk.history) || !state.liveAsk.history.length) {
      state.liveAsk.history = normalizeLiveAskStoredHistory(state.ask.history, 80);
      if (state.liveAsk.history.length) {
        saveLiveAskHistory();
      }
    }
    if (state.ask.history.length) {
      const latestUser = [...state.ask.history]
        .reverse()
        .find((item) => item.role === "user" && String(item.content || "").trim());
      updateActiveThreadMeta({
        title: latestUser ? String(latestUser.content).trim().slice(0, 34) : askCurrentThreadLabel(),
        preview: latestUser ? String(latestUser.content).trim().slice(0, 72) : "",
      });
    } else {
      updateActiveThreadMeta({
        preview: "",
      });
    }
    renderAskHistory();
    renderAskAnswer("");
    renderAskThreadList();
    renderAskSources([]);
    renderAskActions(null, "", []);
    renderLiveAskThread();
    renderLiveAskActions();
    if (migratedLegacy) {
      setAskStatus(`이력 불러옴(legacy) · ${state.ask.history.length}개`);
    } else {
      setAskStatus(state.ask.history.length ? `이력 불러옴 · ${state.ask.history.length}개` : "Ready.");
    }
  } catch (err) {
    state.ask.history = [];
    state.ask.runRel = resolvedRun;
    state.ask.profileId = profileId;
    state.ask.historyProfileId = scopedProfileId;
    state.ask.lastAction = null;
    state.ask.lastAnswer = "";
    state.ask.lastSources = [];
    state.ask.pendingSources = [];
    state.ask.liveAnswer = "";
    renderAskHistory();
    renderAskAnswer("");
    renderAskThreadList();
    renderAskSources([]);
    renderAskActions(null, "", []);
    renderLiveAskThread();
    renderLiveAskActions();
    setAskStatus(`이력 로드 실패: ${err}`);
  }
}

async function saveAskHistory() {
  try {
    ensureAskThreadScope(false);
    await fetchJSON("/api/help/history", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        run: ensureAskRunRel(),
        profile_id: askHistoryProfileId(),
        items: state.ask.history.slice(-80),
      }),
    });
    updateActiveThreadMeta({
      preview: state.ask.history
        .filter((entry) => entry.role === "user")
        .slice(-1)[0]?.content || "",
    });
  } catch (err) {
    appendLog(`[ask] history save failed: ${err}\n`);
  }
}

async function clearAskHistoryAndUi() {
  try {
    ensureAskThreadScope(false);
    await fetchJSON("/api/help/history/clear", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ run: ensureAskRunRel(), profile_id: askHistoryProfileId() }),
    });
  } catch (err) {
    appendLog(`[ask] history clear failed: ${err}\n`);
  }
  state.ask.history = [];
  state.ask.lastAction = null;
  state.ask.lastAnswer = "";
  state.ask.lastSources = [];
  state.ask.pendingSources = [];
  state.ask.pendingQuestion = "";
  state.ask.liveAnswer = "";
  state.ask.selectionText = "";
  state.ask.selectionDragging = false;
  state.liveAsk.history = [];
  state.liveAsk.pendingQuestion = "";
  state.liveAsk.liveAnswer = "";
  state.liveAsk.pendingSources = [];
  state.liveAsk.lastSources = [];
  state.liveAsk.lastAction = null;
  state.liveAsk.lastAnswer = "";
  state.liveAsk.activeLogStartIndex = -1;
  state.liveAsk.jobLogStartIndex = -1;
  state.liveAsk.lastJobLogStartIndex = -1;
  saveLiveAskHistory();
  renderAskHistory();
  renderAskAnswer("");
  renderAskSources([]);
  renderAskActions(null, "", []);
  renderLiveAskThread();
  renderLiveAskActions();
  resetAskActivityState();
  updateActiveThreadMeta({ preview: "" });
  setAskStatus("현재 스레드 이력을 초기화했습니다. (스레드 카드는 유지)");
}

function setAskPanelOpen(open, opts = {}) {
  const panel = $("#ask-panel");
  if (!panel) return;
  state.ask.open = Boolean(open);
  panel.classList.toggle("open", state.ask.open);
  panel.setAttribute("aria-hidden", state.ask.open ? "false" : "true");
  const button = $("#ask-button");
  if (button) {
    button.classList.toggle("is-active", state.ask.open);
  }
  if (state.ask.open) {
    restoreAskGeometry(opts.anchor || null);
    ensureAskThreadScope(false);
    renderAskThreadList();
    syncAskActionPolicyInputs();
    renderAskCapabilityManager();
    renderCapabilityStudio();
    setAskThreadPopoverOpen(false);
    setAskCapabilityManagerOpen(false);
    setAskCapabilityDetailOpen(false);
    loadAskCapabilityRegistry({ silent: true }).catch(() => {});
    loadAskHistory(ensureAskRunRel()).catch((err) => {
      setAskStatus(`이력 로드 실패: ${err}`);
    });
    window.setTimeout(() => {
      $("#ask-input")?.focus();
    }, 0);
  } else {
    state.ask.selectionDragging = false;
    setAskThreadPopoverOpen(false);
    setAskCapabilityDetailOpen(false);
    closeAskActionModal();
  }
}

function normalizeAskSourceList(sources) {
  if (!Array.isArray(sources)) return [];
  return sources
    .map((src, idx) => {
      const id = String(src?.id || `S${idx + 1}`).trim() || `S${idx + 1}`;
      const path = String(src?.path || "").trim();
      const start = Number(src?.start_line || 0);
      const end = Number(src?.end_line || 0);
      return {
        id,
        path,
        start_line: Number.isFinite(start) ? start : 0,
        end_line: Number.isFinite(end) ? end : 0,
      };
    })
    .filter((src) => Boolean(src.path))
    .slice(0, 12);
}

function hashFoldToken(raw) {
  const text = String(raw || "");
  let hash = 0;
  for (let idx = 0; idx < text.length; idx += 1) {
    hash = ((hash * 31) + text.charCodeAt(idx)) >>> 0;
  }
  return hash.toString(36);
}

function makeAskSourceFoldKey(items) {
  const rows = Array.isArray(items) ? items : [];
  const raw = rows
    .map((src) => {
      const path = normalizePathString(src?.path || "");
      const start = Number(src?.start_line || 0);
      const end = Number(src?.end_line || 0);
      const lineToken = start > 0
        ? `${start}-${end > start ? end : start}`
        : "-";
      return `${path}|${lineToken}`;
    })
    .filter(Boolean)
    .sort((a, b) => a.localeCompare(b))
    .join("||");
  return `src:${rows.length}:${hashFoldToken(raw)}`;
}

function renderAskMessageSources(sources) {
  const list = normalizeAskSourceList(sources);
  if (!list.length) return "";
  const lineTextOf = (src) => {
    const start = Number(src.start_line || 0);
    const end = Number(src.end_line || 0);
    return start > 0 && end >= start ? `${start}-${end}` : (start > 0 ? `${start}` : "-");
  };
  const makeLinks = (items) => items
    .map((src) => {
      const start = Number(src.start_line || 0);
      const end = Number(src.end_line || 0);
      const lineText = lineTextOf(src);
      return `
        <button
          type="button"
          class="ghost mini ask-inline-source-open"
          data-source-path="${escapeHtml(src.path)}"
          data-source-start="${start}"
          data-source-end="${end}"
          title="${escapeHtml(`${src.path}:${lineText}`)}"
        >
          ${escapeHtml(`[${src.id}] ${src.path}:${lineText}`)}
        </button>
      `;
    })
    .join("");
  const allLinks = makeLinks(list);
  const first = list[0] || {};
  const firstPath = String(first.path || "");
  const firstBaseName = firstPath.split("/").filter(Boolean).slice(-1)[0] || firstPath;
  const firstLabel = `[${first.id}] ${firstBaseName}:${lineTextOf(first)}`;
  const summaryText = list.length > 1
    ? `${firstLabel} 외 ${list.length - 1}개의 근거 확인하기`
    : `${firstLabel} 근거 확인하기`;
  const foldKey = makeAskSourceFoldKey(list);
  const opened = Boolean(state.liveAsk.sourceFoldState?.[foldKey]);
  const openAttr = opened ? " open" : "";
  return `
    <div class="ask-message-sources">
      <details class="ask-message-fold ask-message-source-fold" data-source-fold-key="${escapeHtml(foldKey)}"${openAttr}>
        <summary>${escapeHtml(summaryText)}</summary>
        <div class="ask-message-source-links">${allLinks}</div>
      </details>
    </div>
  `;
}

function renderAskMessageActions(action, answerText = "", sources = [], options = {}) {
  const buttons = buildAskActionButtons(action, answerText, sources, options);
  if (!buttons.length) return "";
  const folded = buttons.length > 3;
  const primary = folded ? buttons.slice(0, 3) : buttons;
  const secondary = folded ? buttons.slice(3) : [];
  return `
    <div class="ask-message-actions">
      <strong>FederHav 제안/작업</strong>
      <div class="ask-message-action-buttons">${primary.join("")}</div>
      ${secondary.length ? `
        <details class="ask-message-fold">
          <summary>추가 제안 ${secondary.length}개 펼치기</summary>
          <div class="ask-message-action-buttons">${secondary.join("")}</div>
        </details>
      ` : ""}
    </div>
  `;
}

function bindAskInlineSourceButtons(root) {
  if (!root) return;
  root.querySelectorAll(".ask-message-source-fold[data-source-fold-key]").forEach((details) => {
    details.addEventListener("toggle", () => {
      const key = String(details.getAttribute("data-source-fold-key") || "").trim();
      if (!key) return;
      if (!state.liveAsk.sourceFoldState || typeof state.liveAsk.sourceFoldState !== "object") {
        state.liveAsk.sourceFoldState = {};
      }
      state.liveAsk.sourceFoldState[key] = Boolean(details.open);
      saveLiveAskPrefs();
    });
  });
  root.querySelectorAll(".ask-inline-source-open").forEach((btn) => {
    btn.addEventListener("click", async (ev) => {
      ev.preventDefault();
      ev.stopPropagation();
      const fold = btn.closest(".ask-message-source-fold[data-source-fold-key]");
      if (fold instanceof Element) {
        const key = String(fold.getAttribute("data-source-fold-key") || "").trim();
        if (key) {
          if (!state.liveAsk.sourceFoldState || typeof state.liveAsk.sourceFoldState !== "object") {
            state.liveAsk.sourceFoldState = {};
          }
          state.liveAsk.sourceFoldState[key] = true;
          saveLiveAskPrefs();
        }
      }
      const sourcePath = btn.getAttribute("data-source-path") || "";
      const startLine = Number(btn.getAttribute("data-source-start") || "0");
      const endLine = Number(btn.getAttribute("data-source-end") || `${startLine}`);
      if (!sourcePath) return;
      await loadFilePreview(sourcePath, {
        focusLine: startLine,
        endLine,
        readOnly: true,
      });
      appendLog(`[help] source opened: ${sourcePath}:${startLine}-${endLine}\n`);
    });
  });
}

function renderAskAnswer(answerText) {
  const answerEl = $("#ask-answer");
  if (!answerEl) return;
  const pendingQuestion = String(state.ask.pendingQuestion || "").trim();
  const pendingAnswer = String(answerText || "").trim();
  state.ask.liveAnswer = pendingAnswer;
  const historyItems = Array.isArray(state.ask.history) ? state.ask.history.slice(-40) : [];
  const rows = historyItems.map((entry) => ({
    role: entry.role === "assistant" ? "assistant" : "user",
    content: String(entry.content || "").trim(),
    pending: false,
  }));
  if (pendingQuestion) {
    rows.push({ role: "user", content: pendingQuestion, pending: true });
  }
  if (pendingAnswer) {
    rows.push({ role: "assistant", content: pendingAnswer, pending: true });
  }
  if (!rows.length) {
    answerEl.innerHTML = '<p class="muted">아직 답변이 없습니다.</p>';
    scheduleAskScrollToBottom(true);
    state.ask.autoFollowAnswer = true;
    syncAskJumpLatestVisibility();
    return;
  }
  const nearBottom = isNearBottom(answerEl, 140);
  if (nearBottom) {
    state.ask.autoFollowAnswer = true;
  }
  let lastAssistantIndex = -1;
  rows.forEach((row, idx) => {
    if (row.role === "assistant") lastAssistantIndex = idx;
  });
  answerEl.innerHTML = rows
    .map((row, idx) => {
      const roleLabel = row.role === "assistant" ? "답변" : "질문";
      const badge = row.pending ? '<span class="ask-badge">streaming</span>' : "";
      const body = row.role === "assistant"
        ? renderMarkdown(row.content || "")
        : escapeHtml(row.content || "").replace(/\n/g, "<br />");
      const sourceList = row.role === "assistant" && idx === lastAssistantIndex
        ? (row.pending ? state.ask.pendingSources : state.ask.lastSources)
        : [];
      const sourceBlock = renderAskMessageSources(sourceList);
      const actionBlock = row.role === "assistant" && idx === lastAssistantIndex && !row.pending
        ? renderAskMessageActions(state.ask.lastAction, state.ask.lastAnswer || row.content, state.ask.lastSources)
        : "";
      return `
        <article class="ask-message ${row.role}">
          <div class="ask-message-head">
            <strong>${escapeHtml(roleLabel)}</strong>
            ${badge}
          </div>
          <div class="ask-message-body">${body}</div>
          ${sourceBlock}
          ${actionBlock}
        </article>
      `;
    })
    .join("");
  bindAskInlineSourceButtons(answerEl);
  bindAskActionButtons(answerEl);
  hydrateMarkdownBlocks(answerEl);
  if (state.ask.autoFollowAnswer) {
    scheduleAskScrollToBottom(true);
  } else {
    syncAskJumpLatestVisibility();
  }
}

function renderAskSources(sources) {
  const normalized = normalizeAskSourceList(sources);
  if (state.ask.busy) {
    state.ask.pendingSources = normalized;
  } else {
    state.ask.lastSources = normalized;
  }
  renderAskSourcesTrace();
  renderAskAnswer(state.ask.liveAnswer || "");
}

function loadLiveAskDraft() {
  try {
    return String(localStorage.getItem(LIVE_ASK_DRAFT_KEY) || "");
  } catch (err) {
    return "";
  }
}

function saveLiveAskDraft(text) {
  try {
    const value = String(text || "");
    if (!value.trim()) {
      localStorage.removeItem(LIVE_ASK_DRAFT_KEY);
      return;
    }
    localStorage.setItem(LIVE_ASK_DRAFT_KEY, value.slice(0, 12000));
  } catch (err) {
    // ignore
  }
}

function normalizeLiveAskLogTailChars(value, fallback = LIVE_ASK_LOG_TAIL_DEFAULT) {
  const parsed = Number.parseInt(String(value ?? "").trim(), 10);
  if (Number.isFinite(parsed) && LIVE_ASK_LOG_TAIL_CHOICES.includes(parsed)) {
    return parsed;
  }
  const fallbackInt = Number.parseInt(String(fallback ?? "").trim(), 10);
  if (Number.isFinite(fallbackInt) && LIVE_ASK_LOG_TAIL_CHOICES.includes(fallbackInt)) {
    return fallbackInt;
  }
  return LIVE_ASK_LOG_TAIL_DEFAULT;
}

function loadLiveAskPrefs() {
  try {
    const raw = localStorage.getItem(LIVE_ASK_PREF_KEY);
    if (!raw) return;
    const parsed = JSON.parse(raw);
    state.liveAsk.autoLogContext = parsed?.auto_log_context !== false;
    state.liveAsk.autoLogChars = normalizeLiveAskLogTailChars(
      parsed?.auto_log_chars,
      LIVE_ASK_LOG_TAIL_DEFAULT,
    );
    const sourceFold = parsed?.source_fold_state;
    if (sourceFold && typeof sourceFold === "object") {
      state.liveAsk.sourceFoldState = Object.fromEntries(
        Object.entries(sourceFold)
          .filter(([key, value]) => String(key || "").trim() && Boolean(value))
          .slice(0, 280),
      );
    }
    const inlineFold = parsed?.inline_source_fold_state;
    if (inlineFold && typeof inlineFold === "object") {
      state.liveAsk.inlineSourceFoldState = Object.fromEntries(
        Object.entries(inlineFold)
          .filter(([key, value]) => String(key || "").trim() && Boolean(value))
          .slice(0, 480),
      );
    }
    const processFold = parsed?.process_fold_state;
    if (processFold && typeof processFold === "object") {
      state.liveAsk.processFoldState = Object.fromEntries(
        Object.entries(processFold)
          .filter(([key, value]) => String(key || "").trim() && Boolean(value))
          .slice(0, 280),
      );
    }
  } catch (err) {
    state.liveAsk.autoLogContext = true;
    state.liveAsk.autoLogChars = LIVE_ASK_LOG_TAIL_DEFAULT;
  }
}

function saveLiveAskPrefs() {
  try {
    localStorage.setItem(
      LIVE_ASK_PREF_KEY,
      JSON.stringify({
        auto_log_context: Boolean(state.liveAsk.autoLogContext),
        auto_log_chars: normalizeLiveAskLogTailChars(
          state.liveAsk.autoLogChars,
          LIVE_ASK_LOG_TAIL_DEFAULT,
        ),
        source_fold_state: Object.fromEntries(
          Object.entries(state.liveAsk.sourceFoldState || {})
            .filter(([key, value]) => String(key || "").trim() && Boolean(value))
            .slice(0, 280),
        ),
        inline_source_fold_state: Object.fromEntries(
          Object.entries(state.liveAsk.inlineSourceFoldState || {})
            .filter(([key, value]) => String(key || "").trim() && Boolean(value))
            .slice(0, 480),
        ),
        process_fold_state: Object.fromEntries(
          Object.entries(state.liveAsk.processFoldState || {})
            .filter(([key, value]) => String(key || "").trim() && Boolean(value))
            .slice(0, 280),
        ),
      }),
    );
  } catch (err) {
    // ignore
  }
}

function syncLiveAskPrefsInputs() {
  const autoLog = $("#live-ask-auto-log");
  if (autoLog) {
    autoLog.checked = Boolean(state.liveAsk.autoLogContext);
  }
  const sizeSelect = $("#live-ask-log-tail-size");
  if (sizeSelect) {
    const token = String(
      normalizeLiveAskLogTailChars(state.liveAsk.autoLogChars, LIVE_ASK_LOG_TAIL_DEFAULT),
    );
    if (sizeSelect.value !== token) {
      sizeSelect.value = token;
    }
  }
  renderLiveAskContextChips();
  updateLiveAskInputMeta();
}

function liveAskHistoryStorageKey(scopeKey) {
  return askStorageKey(`live-history-${encodeURIComponent(scopeKey || "global::default")}`);
}

function normalizeLiveAskMeta(meta) {
  if (!meta || typeof meta !== "object") return null;
  const backend = String(meta.backend || "").trim();
  const model = String(meta.model || "").trim();
  const reasoningRaw = String(meta.reasoning || "").trim();
  const reasoningToken = reasoningRaw.toLowerCase().replace(/[\s-]+/g, "_");
  const reasoning = ["", "off", "none", "false", "0", "disabled", "disable"].includes(reasoningToken)
    ? ""
    : reasoningRaw;
  const indexed = Number(meta.indexed || 0);
  const traceId = String(meta.trace_id || meta.traceId || "").trim();
  const traceStepsRaw = Number(meta.trace_steps || meta.traceSteps || meta.tool_steps || 0);
  const traceSteps = Number.isFinite(traceStepsRaw) ? Math.max(0, Math.round(traceStepsRaw)) : 0;
  const error = String(meta.error || "").trim();
  const payload = {
    backend,
    model,
    reasoning,
    indexed: Number.isFinite(indexed) ? indexed : 0,
    trace_id: traceId,
    trace_steps: traceSteps,
    error,
  };
  if (
    !payload.backend
    && !payload.model
    && !payload.reasoning
    && !payload.indexed
    && !payload.trace_id
    && !payload.trace_steps
    && !payload.error
  ) {
    return null;
  }
  return payload;
}

function normalizeLiveAskAction(action) {
  if (!action || typeof action !== "object") return null;
  const type = String(action.type || "").trim();
  if (!type) return null;
  const runHint = normalizeRunHint(action.run_hint || action.run_name_hint || "");
  const sanitizedRunHint = !runHint || isInvalidRunHint(runHint) ? "" : runHint;
  if (type === "switch_run" && !sanitizedRunHint) {
    return null;
  }
  const normalized = {
    ...action,
    type,
  };
  if (sanitizedRunHint) {
    normalized.run_hint = sanitizedRunHint;
  } else {
    delete normalized.run_hint;
  }
  if (normalized.run_name_hint && isInvalidRunHint(normalized.run_name_hint)) {
    delete normalized.run_name_hint;
  }
  return normalized;
}

function normalizeLiveAskProcessLog(rawText, options = {}) {
  const dropRunAgentEcho = options?.dropRunAgentEcho !== false;
  const maxLines = Number.isFinite(Number(options?.maxLines))
    ? Math.max(20, Number(options.maxLines))
    : LIVE_ASK_PROCESS_MAX_LINES;
  const maxChars = Number.isFinite(Number(options?.maxChars))
    ? Math.max(1200, Number(options.maxChars))
    : LIVE_ASK_PROCESS_MAX_CHARS;
  const lines = String(rawText || "")
    .replace(/\r\n/g, "\n")
    .replace(/\r/g, "\n")
    .split("\n");
  const compact = [];
  for (const rawLine of lines) {
    const line = String(rawLine || "").trimEnd();
    const trimmed = line.trim();
    const deSymbolized = trimmed.replace(/^[\s>▸▾▶▷►•·\-–—:]+/, "").trim();
    const condensed = trimmed.replace(/\s+/g, "");
    const condensedKorean = condensed.replace(/[()[\]{}]/g, "");
    const compactDeSymbolized = deSymbolized.replace(/\s+/g, "");
    if (!trimmed) continue;
    if (
      /실시간\s*(파이프라인\s*)?로그/i.test(deSymbolized)
      || /^realtime\s*logs?/i.test(deSymbolized)
      || /^live\s*logs?/i.test(deSymbolized)
    ) {
      continue;
    }
    if (
      (/실시간/.test(deSymbolized) && /로그/.test(deSymbolized) && /\d+\s*줄/.test(deSymbolized))
      || /^실시간로그\d+줄(?:확인하기)?$/i.test(compactDeSymbolized)
      || compactDeSymbolized.includes("실시간로그")
    ) {
      continue;
    }
    if (
      /^실시간\s*(파이프라인\s*)?로그\s*[:\-]?\s*\d+\s*줄(?:\s*\(.*\))?$/i.test(trimmed)
      || /^실시간\s*로그\s*[:\-]?\s*\d+\s*줄(?:\s*\(.*\))?$/i.test(trimmed)
      || /^실시간로그\s*[:\-]?\s*\d+\s*줄(?:\s*\(.*\))?$/i.test(trimmed)
      || /^real[-\s]*time\s*logs?\s*[:\-]?\s*\d+/i.test(trimmed)
      || /^>?[:\-\s]*실시간\s*(파이프라인\s*)?로그\s*[:\-]?\s*\d+\s*줄/i.test(trimmed)
      || /^>?[:\-\s]*realtime\s*logs?\s*[:\-]?\s*\d+/i.test(trimmed)
      || /^실시간\s*(파이프라인\s*)?로그(?:\s*확인하기)?$/i.test(trimmed)
      || /실시간\s*(파이프라인\s*)?로그\s*[:\-]?\s*\d+\s*줄.*확인하기/i.test(trimmed)
      || /^실시간(?:파이프라인)?로그\d+줄(?:확인하기)?$/i.test(condensedKorean)
      || (/실시간/.test(trimmed) && /로그/.test(trimmed) && /\d+\s*줄/.test(trimmed))
      || (/실시간/.test(deSymbolized) && /로그/.test(deSymbolized) && /\d+\s*줄/.test(deSymbolized))
      || /^실시간\s*(파이프라인\s*)?로그(?:\s*확인하기)?$/i.test(deSymbolized)
      || (/^>?\s*로그/.test(trimmed) && /\d+\s*줄/.test(trimmed) && !/[a-z0-9_./\\-]/i.test(condensed))
    ) {
      continue;
    }
    if (/^\[?\s*turn\s*\d+\s*\]?$/i.test(trimmed)) {
      continue;
    }
    if (/^(내부|작업)\s*로그\s*[:\-]?\s*\d+\s*줄(?:\s*\(.*\))?$/i.test(trimmed)) {
      continue;
    }
    if (dropRunAgentEcho && /^\[run-agent:(user|assistant|sources)\]/i.test(trimmed)) {
      continue;
    }
    if (compact.length && compact[compact.length - 1] === line && line.length < 220) {
      continue;
    }
    compact.push(line);
  }
  if (!compact.length) return "";
  let tail = compact.slice(-maxLines).join("\n");
  if (tail.length > maxChars) {
    tail = tail.slice(-maxChars).trimStart();
  }
  return tail.trim();
}

function extractLiveAskProcessLog(startIndex = 0, endIndex = null) {
  const start = Number.isFinite(Number(startIndex)) ? Math.max(0, Number(startIndex)) : 0;
  const resolvedEnd = Number.isFinite(Number(endIndex))
    ? Math.max(start, Math.min(state.logBuffer.length, Number(endIndex)))
    : state.logBuffer.length;
  if (resolvedEnd <= start) return "";
  const raw = reflowLogTextForDisplay(state.logBuffer.slice(start, resolvedEnd).join(""));
  return normalizeLiveAskProcessLog(raw, {
    maxLines: LIVE_ASK_PROCESS_MAX_LINES,
    maxChars: LIVE_ASK_PROCESS_MAX_CHARS,
  });
}

function normalizeLiveAskStoredHistory(items, limit = 80) {
  if (!Array.isArray(items)) return [];
  return items
    .map((item) => {
      let role = "user";
      if (item?.role === "assistant") role = "assistant";
      if (item?.role === "system") role = "system";
      const content = String(item?.content || "").slice(0, 12000);
      const row = {
        role,
        content,
        ts: String(item?.ts || ""),
      };
      if (role === "assistant" || role === "system") {
        const sources = normalizeAskSourceList(item?.sources || []);
        const action = normalizeLiveAskAction(item?.action || null);
        const meta = normalizeLiveAskMeta(item?.meta || null);
        const processLog = normalizeLiveAskProcessLog(item?.process_log || item?.processLog || "", {
          maxLines: LIVE_ASK_PROCESS_MAX_LINES,
          maxChars: LIVE_ASK_PROCESS_MAX_CHARS,
        });
        if (sources.length) row.sources = sources;
        if (action) row.action = action;
        if (meta) row.meta = meta;
        if (processLog) row.process_log = processLog;
      }
      return row;
    })
    .filter((item) => String(item.content || "").trim())
    .slice(-Math.max(1, limit));
}

function loadLiveAskHistoryForScope(scopeKey) {
  try {
    const key = liveAskHistoryStorageKey(scopeKey);
    const raw = localStorage.getItem(key);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return normalizeLiveAskStoredHistory(parsed, 80);
  } catch (err) {
    return [];
  }
}

function saveLiveAskHistory() {
  try {
    const scopeKey = state.liveAsk.scopeKey || askScopeValues().scopeKey || "global::default";
    const key = liveAskHistoryStorageKey(scopeKey);
    localStorage.setItem(
      key,
      JSON.stringify(normalizeLiveAskStoredHistory(state.liveAsk.history, 80)),
    );
  } catch (err) {
    // ignore
  }
}

function applyLiveAskScope(scopeKey, options = {}) {
  const force = Boolean(options?.force);
  const normalizedScope = String(scopeKey || askScopeValues().scopeKey || "global::default");
  if (!force && state.liveAsk.scopeKey === normalizedScope) return false;
  state.liveAsk.scopeKey = normalizedScope;
  state.liveAsk.history = loadLiveAskHistoryForScope(normalizedScope);
  if (!state.liveAsk.history.length && Array.isArray(options?.fallbackHistory)) {
    state.liveAsk.history = normalizeLiveAskStoredHistory(options.fallbackHistory, 80);
    if (state.liveAsk.history.length) {
      saveLiveAskHistory();
    }
  }
  state.liveAsk.pendingQuestion = "";
  state.liveAsk.liveAnswer = "";
  state.liveAsk.pendingSources = [];
  state.liveAsk.lastSources = [];
  state.liveAsk.lastAction = null;
  state.liveAsk.lastAnswer = "";
  state.liveAsk.activeLogStartIndex = -1;
  state.liveAsk.jobLogStartIndex = -1;
  state.liveAsk.lastJobLogStartIndex = -1;
  state.liveAsk.autoFollowThread = true;
  state.liveAsk.sourceFoldState = {};
  state.liveAsk.inlineSourceFoldState = {};
  state.liveAsk.processFoldState = {};
  saveLiveAskPrefs();
  renderLiveAskThread();
  renderLiveAskActions();
  renderAskHistory();
  return true;
}

function buildLiveAskLogTail(chars = state.liveAsk.autoLogChars) {
  const merged = reflowLogTextForDisplay(state.logBuffer.join("")).trim();
  if (!merged) return "";
  const limit = normalizeLiveAskLogTailChars(chars, LIVE_ASK_LOG_TAIL_DEFAULT);
  return merged.slice(-limit);
}

function estimateLiveAskHistoryChars(limit = 14) {
  const rows = normalizeLiveAskHistoryForPayload(limit);
  return rows.reduce((acc, item) => acc + String(item?.content || "").length, 0);
}

function resolveLiveAskEffectiveLogChars(requested = state.liveAsk.autoLogChars) {
  const configured = normalizeLiveAskLogTailChars(requested, LIVE_ASK_LOG_TAIL_DEFAULT);
  const historyChars = estimateLiveAskHistoryChars(14);
  const contextBudget = 18000;
  const reserve = 2800;
  const available = Math.max(0, contextBudget - historyChars - reserve);
  return Math.max(0, Math.min(configured, available));
}

function liveAskContextPolicyText() {
  const tailChars = normalizeLiveAskLogTailChars(
    state.liveAsk.autoLogChars,
    LIVE_ASK_LOG_TAIL_DEFAULT,
  );
  if (!state.liveAsk.autoLogContext) return "state-memory only";
  return `state-memory + 보조로그 적응형 요약(최대 ${tailChars.toLocaleString()}자)`;
}

function updateLiveAskThreadInset() {
  const thread = $("#live-ask-thread");
  const composer = document.querySelector("#live-ask-dock .live-ask-composer");
  if (!(thread instanceof HTMLElement) || !(composer instanceof HTMLElement)) return;
  const composerStyle = window.getComputedStyle(composer);
  const isOverlayComposer = composerStyle.position === "absolute" || composerStyle.position === "fixed";
  let inset = 28;
  if (isOverlayComposer) {
    const rect = composer.getBoundingClientRect();
    const measured = Number.isFinite(rect.height) ? rect.height : composer.offsetHeight;
    inset = Math.max(88, Math.min(420, Math.round(measured + 22)));
  }
  thread.style.setProperty("--live-ask-thread-bottom-inset", `${inset}px`);
}

function ensureLiveAskLayoutObserver() {
  const composer = document.querySelector("#live-ask-dock .live-ask-composer");
  const thread = $("#live-ask-thread");
  if (!(composer instanceof HTMLElement) || !(thread instanceof HTMLElement)) return;
  if (typeof ResizeObserver !== "undefined" && !liveAskComposerResizeObserver) {
    liveAskComposerResizeObserver = new ResizeObserver(() => {
      window.requestAnimationFrame(() => updateLiveAskThreadInset());
    });
    liveAskComposerResizeObserver.observe(composer);
    liveAskComposerResizeObserver.observe(thread);
  }
  window.requestAnimationFrame(() => updateLiveAskThreadInset());
}

function updateLiveAskInputMeta() {
  const input = $("#live-ask-input");
  const meta = $("#live-ask-input-meta");
  const runtimeNote = $("#live-ask-runtime-note");
  if (!input || !meta) return;
  const len = String(input.value || "").length;
  const contextHint = liveAskContextPolicyText();
  meta.textContent = `${len.toLocaleString()}자 · Enter 실행 · Shift+Enter 줄바꿈`;
  meta.title = `컨텍스트 정책: ${contextHint}`;
  const agentName = currentAskAgentDisplayName();
  input.placeholder = `${agentName}에게 질문하거나 작업을 요청하세요. 예: QC 핵심 이슈를 표로 요약해줘`;
  if (runtimeNote instanceof HTMLElement) {
    runtimeNote.hidden = false;
    runtimeNote.textContent = `컨텍스트 정책: ${contextHint}`;
  }
  window.requestAnimationFrame(() => updateLiveAskThreadInset());
}

function recentMeaningfulUserPrompts(limit = 5) {
  const cap = Math.max(1, Math.min(10, Number(limit) || 5));
  const out = [];
  const seen = new Set();
  const pushRows = (rows) => {
    if (!Array.isArray(rows)) return;
    [...rows].reverse().forEach((entry) => {
      if (out.length >= cap) return;
      if (String(entry?.role || "").trim() !== "user") return;
      const text = String(entry?.content || "").replace(/\s+/g, " ").trim();
      if (!text || isGenericExecutionPrompt(text)) return;
      const key = text.toLowerCase();
      if (seen.has(key)) return;
      seen.add(key);
      out.push(text);
    });
  };
  pushRows(state.liveAsk.history);
  pushRows(state.ask.history);
  return out.slice(0, cap);
}

function buildAutoInstructionDraft(runRel, seedQuery, hints = []) {
  const runLabel = stripSiteRunsPrefix(normalizePathString(runRel || "")) || normalizePathString(runRel || "") || "current run";
  const language = String($("#federlicht-lang")?.value || "ko").trim() || "ko";
  const topic = String(seedQuery || "").replace(/\s+/g, " ").trim();
  if (!topic || isGenericExecutionPrompt(topic)) return "";
  const promptHints = hints
    .map((item) => `- ${item}`)
    .join("\n");
  const hintBlock = promptHints
    ? `\n참고할 사용자 요구 맥락:\n${promptHints}\n`
    : "";
  return (
    `# FederHav Auto Instruction\n`
    + `Run: ${runLabel}\n`
    + `Language: ${language}\n\n`
    + `주제/목표:\n${topic}\n\n`
    + `요청사항:\n`
    + `1. 주제를 3~6개의 핵심 질문으로 분해하세요.\n`
    + `2. 신뢰 가능한 근거를 수집하고 claim-evidence 형태로 연결하세요.\n`
    + `3. 근거가 약한 항목은 gap_finder에 우선순위와 함께 정리하세요.\n`
    + `4. 결과물(report/run_overview.md, report_notes/claim_map.md, report_notes/gap_finder.md)을 업데이트하세요.\n`
    + hintBlock
    + `산출물은 과도한 일반론보다 실행 가능한 요약과 근거 중심으로 작성합니다.\n`
  );
}

function isInstructionContentMeaningful(content) {
  const text = String(content || "").replace(/\r\n/g, "\n").trim();
  if (!text) return false;
  if (text.length < 60) return false;
  if (/no report prompt provided/i.test(text)) return false;
  if (isGenericExecutionPrompt(text)) return false;
  const lineCount = text.split("\n").filter((line) => String(line || "").trim()).length;
  const topicSignals = /(question|scope|source|instruction|주제|목표|범위|근거|분석|보고서|리스크|전망|evidence)/i.test(text);
  return lineCount >= 4 || topicSignals;
}

async function readInstructionTextSafe(pathRel) {
  const target = normalizePathString(pathRel || "");
  if (!target) return "";
  try {
    const payload = await fetchJSON(`/api/files?path=${encodeURIComponent(target)}`);
    return String(payload?.content || "");
  } catch (err) {
    return "";
  }
}

async function ensureAutoInstructionDraft(runRelForAction = "", seedQuery = "", options = {}) {
  const runRel = normalizePathString(runRelForAction || selectedRunRel() || "");
  if (!runRel) return "";
  const instructionPath = defaultInstructionPath(runRel);
  if (!instructionPath) return "";
  const forceRewrite = Boolean(options?.forceRewrite);
  const hints = recentMeaningfulUserPrompts(5);
  const topicHint = String(options?.topicHint || "").trim();
  const query = String(topicHint || seedQuery || hints[0] || "").trim();
  const content = buildAutoInstructionDraft(runRel, query, hints);
  if (!content) return "";
  if (!forceRewrite) {
    const current = await readInstructionTextSafe(instructionPath);
    if (isInstructionContentMeaningful(current)) {
      return instructionPath;
    }
  }
  try {
    await fetchJSON("/api/files", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        path: instructionPath,
        content,
      }),
    });
    appendLog(`[instruction:auto] generated ${instructionPath}\n`);
    return instructionPath;
  } catch (err) {
    appendLog(`[instruction:auto] failed: ${err}\n`);
    return "";
  }
}

async function ensureFeatherActionHasMeaningfulInput(runRelForAction = "", options = {}) {
  const inputField = $("#feather-input");
  const queryField = $("#feather-query");
  const hasInput = Boolean(String(inputField?.value || "").trim());
  const hasQuery = Boolean(String(queryField?.value || "").trim());
  const forceAutoDraft = Boolean(options?.forceAutoDraft);
  const topicHint = String(options?.topicHint || "").trim();
  const meaningfulFallbackQuery = latestAskFallbackQuery({ skipGeneric: true });
  if (!hasInput && !hasQuery && queryField && meaningfulFallbackQuery) {
    queryField.value = meaningfulFallbackQuery;
  }
  if (!String(inputField?.value || "").trim()) {
    const currentQuery = String(queryField?.value || "").trim();
    if (isGenericExecutionPrompt(currentQuery)) {
      const effectiveRunRel = normalizePathString(runRelForAction || selectedRunRel() || "");
      const instructionPath = defaultInstructionPath(effectiveRunRel);
      const hasInstruction = instructionPath ? await instructionPathExists(instructionPath) : null;
      if (hasInstruction && inputField) {
        const instructionText = await readInstructionTextSafe(instructionPath);
        if (isInstructionContentMeaningful(instructionText) && !forceAutoDraft) {
          inputField.value = instructionPath;
          if (queryField) queryField.value = "";
          appendLog(`[run-agent:action] weak query detected; using instruction ${instructionPath}\n`);
          return true;
        }
        appendLog("[run-agent:action] existing instruction is weak; generating auto instruction draft\n");
      }
      const autoInstruction = await ensureAutoInstructionDraft(
        effectiveRunRel,
        topicHint || meaningfulFallbackQuery || currentQuery,
        {
          topicHint,
          forceRewrite: forceAutoDraft || !Boolean(hasInstruction),
        },
      );
      if (autoInstruction && inputField) {
        inputField.value = autoInstruction;
        if (queryField) queryField.value = "";
        setAskStatus("실행 요청이 짧아 FederHav가 instruction 초안을 점검/자동 보정했습니다.");
        return true;
      }
      if (meaningfulFallbackQuery && queryField) {
        queryField.value = meaningfulFallbackQuery;
        appendLog("[run-agent:action] weak query replaced by recent meaningful context\n");
        return true;
      }
      setAskStatus("실행 요청이 너무 짧습니다. Feather Instruction을 먼저 작성/선택해 주세요.");
      document.querySelector('[data-tab="feather"]')?.click();
      inputField?.focus();
      return false;
    }
  }
  return true;
}

function setLiveAskInputValue(text, options = {}) {
  const input = $("#live-ask-input");
  if (!input) return;
  const append = Boolean(options && options.append);
  const focus = options?.focus !== false;
  const next = String(text || "");
  if (append && input.value.trim()) {
    input.value = `${String(input.value || "").trim()}\n\n${next}`;
  } else {
    input.value = next;
  }
  saveLiveAskDraft(input.value);
  updateLiveAskInputMeta();
  if (focus) {
    input.focus();
    input.setSelectionRange(input.value.length, input.value.length);
  }
}

function syncLiveAskJumpLatestVisibility() {
  const btn = $("#live-ask-jump-latest");
  const host = $("#live-ask-thread");
  if (!btn || !host) return;
  const hasMessages = host.childElementCount > 0 && !host.classList.contains("is-empty");
  btn.classList.toggle("is-hidden", !hasMessages || state.liveAsk.autoFollowThread);
}

function updateLiveAskAutoFollowState() {
  const host = $("#live-ask-thread");
  if (!host) return;
  state.liveAsk.autoFollowThread = isNearBottom(host, 140);
  syncLiveAskJumpLatestVisibility();
}

function scrollLiveAskThreadToLatest() {
  const host = $("#live-ask-thread");
  if (!host) return;
  host.scrollTop = host.scrollHeight;
  state.liveAsk.autoFollowThread = true;
  syncLiveAskJumpLatestVisibility();
}

function buildLiveAskTranscript(limit = 80) {
  const rows = Array.isArray(state.liveAsk.history) ? state.liveAsk.history.slice(-Math.max(1, limit)) : [];
  const lines = rows
    .map((entry) => {
      const role = entry.role === "assistant"
        ? currentAskAgentDisplayName()
        : (entry.role === "system" ? "System" : "User");
      const text = String(entry.content || "").trim();
      if (!text) return "";
      return `${role}: ${text}`;
    })
    .filter(Boolean);
  return lines.join("\n\n").trim();
}

async function copyLiveAskTranscript() {
  const transcript = buildLiveAskTranscript(100);
  if (!transcript) {
    setAskStatus("복사할 대화가 없습니다.");
    return;
  }
  try {
    if (navigator?.clipboard?.writeText) {
      await navigator.clipboard.writeText(transcript);
    } else {
      const ta = document.createElement("textarea");
      ta.value = transcript;
      ta.setAttribute("readonly", "true");
      ta.style.position = "fixed";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      ta.remove();
    }
    setAskStatus("Live 대화를 클립보드에 복사했습니다.");
  } catch (err) {
    setAskStatus(`대화 복사 실패: ${err}`);
  }
}

function clearLiveAskConversation() {
  state.liveAsk.history = [];
  state.liveAsk.pendingQuestion = "";
  state.liveAsk.liveAnswer = "";
  state.liveAsk.pendingSources = [];
  state.liveAsk.lastSources = [];
  state.liveAsk.lastAction = null;
  state.liveAsk.lastAnswer = "";
  state.liveAsk.activeLogStartIndex = -1;
  state.liveAsk.jobLogStartIndex = -1;
  state.liveAsk.lastJobLogStartIndex = -1;
  state.liveAsk.autoFollowThread = true;
  state.liveAsk.sourceFoldState = {};
  state.liveAsk.inlineSourceFoldState = {};
  state.liveAsk.processFoldState = {};
  saveLiveAskPrefs();
  saveLiveAskHistory();
  renderAskHistory();
  renderLiveAskThread();
  renderLiveAskActions();
  setAskStatus("Live 대화를 초기화했습니다.");
}

function useRecentLogsAsLiveAskPrompt() {
  const tail = buildLiveAskLogTail(state.liveAsk.autoLogChars);
  if (!tail) {
    setAskStatus("최근 로그가 없어 첨부할 수 없습니다.");
    return;
  }
  const prompt = [
    "최근 로그를 바탕으로 지금 상태를 진단해줘.",
    "핵심 상태 요약 + 다음 실행 2개를 제안해줘.",
    "",
    "```log",
    tail,
    "```",
  ].join("\n");
  setLiveAskInputValue(prompt, { append: false, focus: true });
  setAskStatus("최근 로그를 질문 입력창에 첨부했습니다.");
}

function appendLiveAskSystemEntry(content, options = {}) {
  const text = String(content || "").trim();
  if (!text) return;
  const row = {
    role: "system",
    content: text.slice(0, 12000),
    ts: new Date().toISOString(),
  };
  const meta = normalizeLiveAskMeta(options.meta || null);
  if (meta) {
    row.meta = meta;
  }
  const processLog = normalizeLiveAskProcessLog(options.processLog || options.process_log || "", {
    maxLines: LIVE_ASK_PROCESS_MAX_LINES,
    maxChars: LIVE_ASK_PROCESS_MAX_CHARS,
  });
  if (processLog) {
    row.process_log = processLog;
  }
  const sources = normalizeAskSourceList(options.sources || []);
  if (sources.length) {
    row.sources = sources;
  }
  state.liveAsk.history.push(row);
  if (state.liveAsk.history.length > 80) {
    state.liveAsk.history = state.liveAsk.history.slice(-80);
  }
  saveLiveAskHistory();
  renderLiveAskThread();
  renderLiveAskActions();
}

function compactHistorySnippet(text, maxChars = 180) {
  const normalized = String(text || "")
    .replace(/\r\n/g, "\n")
    .replace(/\r/g, "\n")
    .replace(/\n{2,}/g, "\n")
    .trim();
  if (!normalized) return "";
  if (normalized.length <= maxChars) return normalized;
  return `${normalized.slice(0, Math.max(1, maxChars - 1)).trim()}…`;
}

function buildAskHistoryPayload(historyRows, options = {}) {
  const rows = Array.isArray(historyRows) ? historyRows : [];
  const recentTurns = Math.max(1, Number.parseInt(String(options?.recentTurns || 14), 10) || 14);
  const summaryTurns = Math.max(4, Number.parseInt(String(options?.summaryTurns || 20), 10) || 20);
  const summaryMaxChars = Math.max(280, Number.parseInt(String(options?.summaryMaxChars || 1800), 10) || 1800);
  const normalized = rows
    .map((entry) => ({
      role: (entry?.role === "assistant" || entry?.role === "system") ? "assistant" : "user",
      content: String(entry?.content || "").trim(),
    }))
    .filter((entry) => Boolean(entry.content));
  if (!normalized.length) return [];
  const recent = normalized.slice(-recentTurns);
  const older = normalized.slice(0, Math.max(0, normalized.length - recent.length));
  if (!older.length) return recent;
  const summarized = older.slice(-summaryTurns);
  const lines = summarized
    .map((entry) => {
      const role = entry.role === "assistant" ? currentAskAgentDisplayName() : "User";
      return `- ${role}: ${compactHistorySnippet(entry.content, 180)}`;
    })
    .filter(Boolean);
  if (!lines.length) return recent;
  let summaryText = [
    `[context-compress] 이전 대화 ${older.length}개를 요약했습니다.`,
    ...lines,
  ].join("\n");
  if (summaryText.length > summaryMaxChars) {
    summaryText = `${summaryText.slice(0, Math.max(1, summaryMaxChars - 1)).trim()}…`;
  }
  return [{ role: "assistant", content: summaryText }, ...recent];
}

function trimStateMemoryPayload(payload, maxChars = 3200) {
  const limit = Math.max(1200, Number.parseInt(String(maxChars || 3200), 10) || 3200);
  const draft = payload && typeof payload === "object" ? { ...payload } : {};
  const serializedLength = () => {
    try {
      return JSON.stringify(draft).length;
    } catch (err) {
      return limit + 1;
    }
  };
  if (serializedLength() <= limit) return draft;
  if (Array.isArray(draft.dialogue_state)) {
    draft.dialogue_state = draft.dialogue_state.slice(-8);
  }
  if (serializedLength() <= limit) return draft;
  if (Array.isArray(draft.recent_sources)) {
    draft.recent_sources = draft.recent_sources.slice(0, 6);
  }
  if (serializedLength() <= limit) return draft;
  if (draft.run && typeof draft.run === "object") {
    const run = { ...draft.run };
    if (Array.isArray(run.recent_reports)) run.recent_reports = run.recent_reports.slice(0, 4);
    if (Array.isArray(run.recent_indexes)) run.recent_indexes = run.recent_indexes.slice(0, 3);
    if (Array.isArray(run.recent_instructions)) run.recent_instructions = run.recent_instructions.slice(0, 3);
    draft.run = run;
  }
  if (serializedLength() <= limit) return draft;
  if (draft.workflow && typeof draft.workflow === "object") {
    draft.workflow = {
      kind: draft.workflow.kind || "",
      status: draft.workflow.status || "",
      active_stage: draft.workflow.active_stage || "",
    };
  }
  if (serializedLength() <= limit) return draft;
  if (Array.isArray(draft.dialogue_state)) {
    draft.dialogue_state = draft.dialogue_state.slice(-4);
  }
  if (serializedLength() <= limit) return draft;
  if (draft.run && typeof draft.run === "object") {
    draft.run = {
      run_rel: draft.run.run_rel || "",
      latest_report: draft.run.latest_report || "",
    };
  }
  return draft;
}

function buildAskStateMemory(options = {}) {
  const maxChars = Math.max(1600, Number.parseInt(String(options?.maxChars || 3000), 10) || 3000);
  const runRel = normalizePathString(
    options?.runRel || selectedRunRel() || state.runSummary?.run_rel || state.workflow?.runRel || "",
  );
  const runSummary = state.runSummary && typeof state.runSummary === "object" ? state.runSummary : null;
  const selectedStages = selectedStagesInOrder().slice(0, 8);
  const recentSources = normalizeAskSourceList(
    state.liveAsk.lastSources || state.ask.lastSources || [],
  )
    .slice(0, 8)
    .map((src) => ({
      id: src.id || "",
      path: String(src.path || ""),
      start_line: Number(src.start_line || 0),
      end_line: Number(src.end_line || 0),
    }));
  const dialogueState = buildAskHistoryPayload(state.liveAsk.history, {
    recentTurns: 10,
    summaryTurns: 18,
    summaryMaxChars: 1600,
  })
    .slice(-10)
    .map((row) => ({
      role: row.role === "assistant" ? "assistant" : "user",
      content: compactHistorySnippet(String(row.content || ""), 220),
    }))
    .filter((row) => row.content);
  const runCounts = runSummary?.counts && typeof runSummary.counts === "object"
    ? {
      pdf: Number(runSummary.counts.pdf || 0),
      pptx: Number(runSummary.counts.pptx || 0),
      text: Number(runSummary.counts.text || 0),
      extracts: Number(runSummary.counts.extracts || 0),
      logs: Number(runSummary.counts.logs || 0),
      report: Number(runSummary.counts.report || 0),
      instruction: Number(runSummary.counts.instruction || 0),
    }
    : null;
  const stateMemory = {
    schema: "federnett.state-memory.v1",
    generated_at: new Date().toISOString(),
    scope: {
      run_rel: runRel || "",
      profile_id: askHistoryProfileId(),
      agent: resolveAskAgentLabel(),
      execution_mode: state.ask.actionMode === "act" ? "act" : "plan",
      allow_artifacts: state.ask.actionMode === "act" ? Boolean(state.ask.allowArtifactWrites) : false,
    },
    workflow: {
      kind: String(state.workflow.kind || ""),
      status: String(state.workflow.statusText || state.workflow.mainStatusText || ""),
      active_stage: String(state.workflow.activeStep || state.pipeline.activeStageId || ""),
      selected_stages: selectedStages,
      has_error: Boolean(state.workflow.hasError),
      running: Boolean(state.workflow.running),
    },
    run: {
      run_rel: runSummary?.run_rel || runRel || "",
      latest_report: runSummary?.latest_report_rel || state.workflow.resultPath || "",
      counts: runCounts || undefined,
      recent_reports: Array.isArray(runSummary?.report_files) ? runSummary.report_files.slice(-6) : [],
      recent_indexes: Array.isArray(runSummary?.index_files) ? runSummary.index_files.slice(0, 4) : [],
      recent_instructions: (
        (state.instructionFiles?.[runRel] || [])
          .map((item) => normalizePathString(item?.path || ""))
          .filter(Boolean)
          .slice(0, 4)
      ),
    },
    recent_sources: recentSources,
    dialogue_state: dialogueState,
  };
  return trimStateMemoryPayload(stateMemory, maxChars);
}

function normalizeLiveAskHistoryForPayload(limit = 14) {
  return buildAskHistoryPayload(state.liveAsk.history, {
    recentTurns: limit,
    summaryTurns: 24,
    summaryMaxChars: 2200,
  });
}

function renderLiveAskMetaChips(meta) {
  const normalized = normalizeLiveAskMeta(meta || null);
  if (!normalized) return "";
  const chips = [
    normalized.backend ? `<span class="live-ask-meta-chip">backend=${escapeHtml(normalized.backend)}</span>` : "",
    normalized.model ? `<span class="live-ask-meta-chip">model=${escapeHtml(normalized.model)}</span>` : "",
    normalized.reasoning ? `<span class="live-ask-meta-chip">reasoning=${escapeHtml(normalized.reasoning)}</span>` : "",
    normalized.indexed > 0 ? `<span class="live-ask-meta-chip">indexed=${normalized.indexed}</span>` : "",
    normalized.trace_id ? `<span class="live-ask-meta-chip">trace=${escapeHtml(normalized.trace_id)}</span>` : "",
    normalized.trace_steps > 0 ? `<span class="live-ask-meta-chip">tools=${normalized.trace_steps}</span>` : "",
    normalized.error ? `<span class="live-ask-meta-chip is-error">error=${escapeHtml(normalized.error)}</span>` : "",
  ]
    .filter(Boolean)
    .join("");
  if (!chips) return "";
  const open = normalized.error ? " open" : "";
  const summaryLabel = normalized.error ? "실행 메타 (오류 포함)" : "실행 메타";
  return `
    <details class="live-ask-meta-fold"${open}>
      <summary>${escapeHtml(summaryLabel)}</summary>
      <div class="live-ask-turn-meta">${chips}</div>
    </details>
  `;
}

function summarizeLiveAskProcess(processLog) {
  const lines = String(processLog || "")
    .split("\n")
    .map((line) => String(line || "").trim())
    .filter(Boolean);
  if (!lines.length) {
    return { total: 0, commands: 0, workflow: 0, actions: 0, activity: 0, errors: 0 };
  }
  const commands = lines.filter((line) => line.startsWith("$ ")).length;
  const workflow = lines.filter((line) => /^\[workflow\]/i.test(line)).length;
  const actions = lines.filter((line) => /^\[(run-agent:action|ask-action|capability)\]/i.test(line)).length;
  const activity = lines.filter((line) => /^\[run-agent:activity\]/i.test(line)).length;
  const errors = lines.filter((line) => /(error|failed|exception)/i.test(line)).length;
  return { total: lines.length, commands, workflow, actions, activity, errors };
}

function renderLiveAskProcessFold(processLog, options = {}) {
  const normalized = normalizeLiveAskProcessLog(processLog, {
    maxLines: options?.maxLines || LIVE_ASK_PROCESS_MAX_LINES,
    maxChars: options?.maxChars || LIVE_ASK_PROCESS_MAX_CHARS,
    dropRunAgentEcho: options?.dropRunAgentEcho !== false,
  });
  if (!normalized) return "";
  const summary = summarizeLiveAskProcess(normalized);
  const lines = normalized
    .split("\n")
    .map((line) => String(line || "").trim())
    .filter(Boolean);
  const lineCount = lines.length;
  const hasError = summary.errors > 0 || /(error|failed|exception)/i.test(normalized);
  const foldKey = `proc:${hashFoldToken(normalized.slice(0, 4200))}`;
  const storedOpen = Object.prototype.hasOwnProperty.call(state.liveAsk.processFoldState || {}, foldKey)
    ? Boolean(state.liveAsk.processFoldState?.[foldKey])
    : null;
  const defaultOpen = Boolean(options?.open || hasError || lineCount <= LIVE_ASK_PROCESS_INLINE_LINES);
  const opened = storedOpen === null ? defaultOpen : storedOpen;
  const chips = [
    summary.commands ? `<span class="live-ask-process-chip">cmd ${summary.commands}</span>` : "",
    summary.workflow ? `<span class="live-ask-process-chip">workflow ${summary.workflow}</span>` : "",
    summary.actions ? `<span class="live-ask-process-chip">action ${summary.actions}</span>` : "",
    summary.activity ? `<span class="live-ask-process-chip">tool ${summary.activity}</span>` : "",
    summary.errors ? `<span class="live-ask-process-chip is-error">error ${summary.errors}</span>` : "",
  ]
    .filter(Boolean)
    .join("");
  const summaryPrefix = String(options?.summaryPrefix || "").trim();
  const summaryPrefixCompact = summaryPrefix
    ? `${summaryPrefix.slice(0, 42)}${summaryPrefix.length > 42 ? "..." : ""}`
    : "";
  const showChips = options?.showChips === true;
  const oneLine = Boolean(options?.oneLine);
  const forceFold = Boolean(options?.forceFold);
  const firstCommand = lines.find((line) => line.startsWith("$ "));
  const compactCommand = firstCommand
    ? firstCommand.slice(2).replace(/\s+/g, " ").trim()
    : "";
  const baseSummaryLabel = compactCommand
    ? `Ran ${compactCommand.slice(0, 96)}${compactCommand.length > 96 ? "..." : ""}`
    : `작업 로그 ${lineCount}줄`;
  const explicitToolCountRaw = Number(options?.toolCount || 0);
  const explicitToolCount = Number.isFinite(explicitToolCountRaw) ? Math.max(0, Math.round(explicitToolCountRaw)) : 0;
  const toolToken = explicitToolCount > 0
    ? `tool ${explicitToolCount}`
    : (summary.activity > 0 ? `tool ${summary.activity}` : "");
  const summaryParts = [];
  if (summaryPrefixCompact) summaryParts.push(summaryPrefixCompact);
  if (toolToken) summaryParts.push(toolToken);
  summaryParts.push(baseSummaryLabel);
  const oneLineBaseLabel = compactCommand
    ? `Ran ${compactCommand.slice(0, 78)}${compactCommand.length > 78 ? "..." : ""}`
    : `log ${lineCount} lines`;
  const summaryLabel = oneLine
    ? [summaryPrefixCompact, toolToken, oneLineBaseLabel].filter(Boolean).join(" · ")
    : summaryParts.join(" · ");
  const summaryTitle = [summaryPrefix, compactCommand || `lines=${lineCount}`, summary.errors ? `errors=${summary.errors}` : ""]
    .filter(Boolean)
    .join(" | ");
  if (!oneLine && !forceFold && lineCount <= 4 && !hasError) {
    const plainRows = lines
      .map((line) => `<div class="live-ask-process-line">${renderRawLineWithLinks(line)}</div>`)
      .join("");
    return `
      <section class="live-ask-process-wrap is-inline is-plain">
        <div class="live-ask-process-plain">${plainRows}</div>
        ${chips ? `<div class="live-ask-process-chips">${chips}</div>` : ""}
      </section>
    `;
  }
  return `
    <section class="live-ask-process-wrap is-inline ${oneLine ? "is-one-line" : ""}">
      <details class="live-ask-process-fold ${options?.compact ? "is-compact" : ""} ${oneLine ? "is-one-line" : ""}" data-process-fold="${escapeHtml(foldKey)}"${opened ? " open" : ""}>
        <summary title="${escapeHtml(summaryTitle || summaryLabel)}">
          <span>${escapeHtml(summaryLabel)}</span>
          ${showChips && chips ? `<span class="live-ask-process-chips">${chips}</span>` : ""}
        </summary>
        <div class="live-ask-process-body is-inline">
          <div class="live-ask-process-actions">
            <button type="button" class="ghost mini live-ask-process-collapse" data-process-fold-close="${escapeHtml(foldKey)}" aria-label="로그 브릿지 접기">접기</button>
          </div>
          ${renderStructuredLog(normalized)}
          <div class="live-ask-process-actions is-tail">
            <button type="button" class="ghost mini live-ask-process-collapse" data-process-fold-close="${escapeHtml(foldKey)}" aria-label="로그 브릿지 접기">접기</button>
          </div>
        </div>
      </details>
    </section>
  `;
}

function buildLiveAskTurnsForRender() {
  const history = normalizeLiveAskStoredHistory(state.liveAsk.history, 80);
  const turns = [];
  let current = null;
  const flush = () => {
    if (!current) return;
    turns.push(current);
    current = null;
  };
  for (const entry of history) {
    const role = entry.role === "assistant"
      ? "assistant"
      : (entry.role === "system" ? "system" : "user");
    if (role === "user") {
      flush();
      current = { user: { ...entry, pending: false }, assistant: null, pending: false };
      continue;
    }
    if (role === "system") {
      flush();
      turns.push({ user: null, assistant: { ...entry, pending: false }, pending: false });
      continue;
    }
    if (!current) {
      current = { user: null, assistant: { ...entry, pending: false }, pending: false };
      continue;
    }
    if (current.assistant) {
      flush();
      current = { user: null, assistant: { ...entry, pending: false }, pending: false };
      continue;
    }
    current.assistant = { ...entry, pending: false };
  }
  flush();

  const pendingQuestion = String(state.liveAsk.pendingQuestion || "").trim();
  const pendingAnswer = String(state.liveAsk.liveAnswer || "").trim();
  const pendingProcess = state.liveAsk.busy
    ? extractLiveAskProcessLog(state.liveAsk.activeLogStartIndex)
    : "";
  if (pendingQuestion || pendingAnswer || pendingProcess) {
    turns.push({
      user: pendingQuestion ? { role: "user", content: pendingQuestion, ts: "", pending: true } : null,
      assistant: pendingAnswer
        ? {
          role: "assistant",
          content: pendingAnswer,
          ts: "",
          pending: true,
          sources: normalizeAskSourceList(state.liveAsk.pendingSources || []),
        }
        : null,
      pending: true,
      process_log: pendingProcess,
    });
  }
  return turns.slice(-20);
}

function renderLiveAskSystemLogCard() {
  const raw = reflowLogTextForDisplay(state.logBuffer.join(""));
  if (!raw.trim()) return "";
  const lines = raw
    .split("\n")
    .map((line) => String(line || "").trimEnd())
    .filter((line) => Boolean(line.trim()));
  if (!lines.length) return "";
  const activeStart = Number.isFinite(Number(state.liveAsk.jobLogStartIndex)) && state.liveAsk.jobLogStartIndex >= 0
    ? Math.floor(state.liveAsk.jobLogStartIndex)
    : -1;
  const recentStart = Number.isFinite(Number(state.liveAsk.lastJobLogStartIndex)) && state.liveAsk.lastJobLogStartIndex >= 0
    ? Math.floor(state.liveAsk.lastJobLogStartIndex)
    : -1;
  let normalized = "";
  let sourceLabel = "";
  if (activeStart >= 0) {
    normalized = extractLiveAskProcessLog(activeStart);
    if (normalized) sourceLabel = "active";
  }
  if (!normalized && recentStart >= 0) {
    normalized = extractLiveAskProcessLog(recentStart);
    if (normalized) sourceLabel = "recent";
  }
  if (!normalized) {
    const tail = lines.slice(-LIVE_ASK_GLOBAL_LOG_TAIL_LINES).join("\n");
    normalized = normalizeLiveAskProcessLog(tail, {
      maxLines: LIVE_ASK_GLOBAL_LOG_TAIL_LINES,
      maxChars: 9000,
      dropRunAgentEcho: false,
    });
  }
  if (!normalized) return "";
  const summary = summarizeLiveAskProcess(normalized);
  const activeKind = String(state.activeJobKind || state.workflow?.kind || "").trim().toLowerCase();
  const agentName = currentAskAgentDisplayName();
  let stageLabel = "Pipeline";
  if (sourceLabel === "active") {
    stageLabel = activeKind === "federlicht"
      ? "Federlicht"
      : (activeKind === "feather" ? "Feather" : "Pipeline");
  } else if (sourceLabel === "recent") {
    stageLabel = "최근 작업";
  } else if (state.liveAsk.busy || state.ask.busy) {
    stageLabel = agentName;
  }
  const badgeLabel = sourceLabel === "active" ? "실행 프로세스" : "로그 브릿지";
  const processBlock = renderLiveAskProcessFold(normalized, {
    open: Boolean(sourceLabel === "active" && (state.liveAsk.busy || state.ask.busy || state.activeJobId)),
    summaryPrefix: `${stageLabel} ${badgeLabel}`,
    toolCount: summary.activity,
    compact: true,
    showChips: false,
    oneLine: true,
    forceFold: true,
  });
  return `
    <section class="live-ask-turn live-ask-turn-system">
      <article class="live-ask-message system is-log-only">
        ${processBlock}
      </article>
    </section>
  `;
}

function bindLiveAskProcessFolds(root) {
  if (!(root instanceof HTMLElement)) return;
  root.querySelectorAll("details[data-process-fold]").forEach((detailsEl) => {
    if (!(detailsEl instanceof HTMLDetailsElement)) return;
    const key = String(detailsEl.getAttribute("data-process-fold") || "").trim();
    if (!key) return;
    detailsEl.addEventListener("toggle", () => {
      if (!state.liveAsk.processFoldState || typeof state.liveAsk.processFoldState !== "object") {
        state.liveAsk.processFoldState = {};
      }
      state.liveAsk.processFoldState[key] = Boolean(detailsEl.open);
      saveLiveAskPrefs();
    });
  });
  root.querySelectorAll("button[data-process-fold-close]").forEach((btn) => {
    btn.addEventListener("click", (ev) => {
      ev.preventDefault();
      ev.stopPropagation();
      const detailsEl = btn.closest("details[data-process-fold]");
      if (!(detailsEl instanceof HTMLDetailsElement)) return;
      const key = String(detailsEl.getAttribute("data-process-fold") || "").trim();
      detailsEl.open = false;
      if (!key) return;
      if (!state.liveAsk.processFoldState || typeof state.liveAsk.processFoldState !== "object") {
        state.liveAsk.processFoldState = {};
      }
      state.liveAsk.processFoldState[key] = false;
      saveLiveAskPrefs();
    });
  });
}

function renderLiveAskThread() {
  const host = $("#live-ask-thread");
  if (!host) return;
  const nearBottom = isNearBottom(host, 140);
  if (nearBottom) state.liveAsk.autoFollowThread = true;

  const turns = buildLiveAskTurnsForRender();
  const globalLogCard = renderLiveAskSystemLogCard();
  const hasTurnProcessLog = turns.some((turn) => String(turn?.process_log || "").trim());
  const showGlobalLogCard = Boolean(globalLogCard) && !hasTurnProcessLog && turns.length === 0;
  if (!turns.length && !globalLogCard) {
    host.classList.add("is-empty");
    host.classList.remove("is-short");
    host.innerHTML = "아직 대화가 없습니다. Live Logs/결과를 바탕으로 질문해보세요.";
    state.liveAsk.autoFollowThread = true;
    syncLiveAskJumpLatestVisibility();
    return;
  }

  host.classList.remove("is-empty");
  host.classList.toggle("is-short", turns.length <= 2 && !state.liveAsk.busy);
  let lastAssistantTurnIndex = -1;
  turns.forEach((turn, idx) => {
    if (turn?.assistant && !turn.pending) lastAssistantTurnIndex = idx;
  });
  const agentRoleLabel = currentAskAgentDisplayName();

  const turnHtml = turns
    .map((turn, idx) => {
      const user = turn?.user || null;
      const assistant = turn?.assistant || null;
      const stamp = assistant?.ts || user?.ts || "";
      const ts = stamp ? formatDate(stamp) : "";
      const userBlock = user
        ? `
          <article class="live-ask-message user ${user.pending ? "is-pending" : ""}">
            <div class="live-ask-message-head">
              <strong class="live-ask-role">User</strong>
              <div class="live-ask-meta">
                ${ts ? `<time>${escapeHtml(ts)}</time>` : ""}
                ${user.pending ? '<span class="ask-badge">queued</span>' : ""}
              </div>
            </div>
            <div class="live-ask-message-body">${escapeHtml(user.content || "").replace(/\n/g, "<br />")}</div>
          </article>
        `
        : "";

      const isLegacyLast = idx === lastAssistantTurnIndex;
      const assistantSources = normalizeAskSourceList(
        assistant?.sources
        || (assistant?.pending ? state.liveAsk.pendingSources : (isLegacyLast ? state.liveAsk.lastSources : [])),
      );
      const assistantAction = assistant?.action || (isLegacyLast ? state.liveAsk.lastAction : null);
      const assistantMeta = assistant?.meta || null;
      const isSystemAssistant = assistant?.role === "system";
      const assistantRoleLabel = isSystemAssistant ? "System" : agentRoleLabel;
      const assistantClass = [
        "live-ask-message",
        "assistant",
        assistant?.pending ? "is-pending" : "",
        isSystemAssistant ? "is-system" : "",
      ]
        .filter(Boolean)
        .join(" ");
      const processLog = String(assistant?.process_log || turn?.process_log || "").trim();
      const assistantText = String(assistant?.content || "").trim();
      const isLogOnlyAssistant = Boolean(assistant && processLog && !assistantText && !assistant?.pending);
      const processSummaryPrefix = `${assistantRoleLabel} 로그 브릿지`;
      const perTurnProcessBlock = renderLiveAskProcessFold(processLog, {
        open: Boolean((turn?.pending && !assistant) || /(error|failed|exception)/i.test(processLog)),
        summaryPrefix: processSummaryPrefix,
        toolCount: Number(assistantMeta?.trace_steps || 0),
        compact: true,
        showChips: false,
        oneLine: true,
        forceFold: true,
      });
      const assistantBody = assistant?.pending
        ? escapeHtml(assistant?.content || "").replace(/\n/g, "<br />")
        : renderMarkdown(assistant?.content || "");
      const assistantBlock = assistant
        ? (isLogOnlyAssistant
          ? `
            <article class="${assistantClass} is-log-only">
              ${perTurnProcessBlock}
            </article>
          `
          : `
            <article class="${assistantClass}">
              <div class="live-ask-message-head">
                <strong class="live-ask-role">${escapeHtml(assistantRoleLabel)}</strong>
                <div class="live-ask-meta">
                  ${ts ? `<time>${escapeHtml(ts)}</time>` : ""}
                  ${assistant?.pending ? '<span class="ask-badge">streaming</span>' : ""}
                </div>
              </div>
              ${renderLiveAskMetaChips(assistantMeta)}
              <div class="live-ask-message-body">${assistantBody}</div>
              ${isSystemAssistant ? "" : renderAskMessageSources(assistantSources)}
              ${perTurnProcessBlock || ""}
              ${assistant?.pending
      ? ""
      : isSystemAssistant
        ? ""
      : renderAskMessageActions(
        assistantAction,
        assistant?.content || "",
        assistantSources,
        { includeSelection: false, includeDerivedPaths: false },
      )}
            </article>
          `)
        : "";
      const pendingProcessOnlyBlock = !assistant && perTurnProcessBlock
        ? `
            <article class="live-ask-message system is-log-inline">
              ${perTurnProcessBlock}
            </article>
          `
        : "";
      return `
        <section class="live-ask-turn ${turn?.pending ? "is-pending" : ""}">
          ${userBlock}
          ${assistantBlock}
          ${pendingProcessOnlyBlock}
        </section>
      `;
    })
    .join("");

  if (showGlobalLogCard) {
    host.innerHTML = `${turnHtml}${globalLogCard}`;
  } else {
    host.innerHTML = turnHtml;
  }
  bindAskInlineSourceButtons(host);
  bindLiveAskProcessFolds(host);
  bindAskActionButtons(host);
  hydrateMarkdownBlocks(host);
  updateLiveAskThreadInset();
  if (state.liveAsk.autoFollowThread) {
    host.scrollTop = host.scrollHeight;
  }
  syncLiveAskJumpLatestVisibility();
}

function renderLiveAskActions() {
  const host = $("#live-ask-actions");
  if (!host) return;
  // Actions are now rendered inline in each assistant message to reduce layout density.
  host.classList.add("is-empty");
  host.innerHTML = "";
}

function renderLiveAskSources(sources) {
  const normalized = normalizeAskSourceList(sources);
  if (state.liveAsk.busy) {
    state.liveAsk.pendingSources = normalized;
  } else {
    state.liveAsk.lastSources = normalized;
  }
  renderLiveAskThread();
  renderLiveAskActions();
}

function resetLiveAskLogStreamState() {
  state.liveAsk.streamLogBuffer = "";
  state.liveAsk.streamChunksLogged = 0;
}

function appendLiveAskTurnStartToLog(question) {
  const q = String(question || "").trim();
  if (!q) return;
  appendLog(`\n[run-agent:user]\n${q}\n`);
  appendLog("[run-agent:assistant] 답변 생성 시작\n");
}

function appendLiveAskActivityToLog(activityId, status, message = "", meta = null) {
  const id = String(activityId || "").trim().toLowerCase() || "tool";
  const stateToken = String(status || "running").trim().toLowerCase() || "running";
  const note = String(message || "").replace(/\s+/g, " ").trim();
  const metaText = askTraceMetaText(meta && typeof meta === "object" ? meta : {});
  const parts = [`id=${id}`, `status=${stateToken}`];
  if (metaText) parts.push(metaText);
  if (note) parts.push(`msg=${note}`);
  appendLog(`[run-agent:activity] ${parts.join(" | ")}\n`);
}

function appendLiveAskDeltaToLog(delta) {
  const chunk = String(delta || "");
  if (!chunk) return;
  const chunkTarget = 96;
  const minBoundary = 18;
  state.liveAsk.streamLogBuffer = `${state.liveAsk.streamLogBuffer || ""}${chunk}`;
  const flushChunk = (text) => {
    const value = String(text || "").replace(/\r\n/g, "\n").replace(/\r/g, "\n");
    if (!value.trim()) return;
    if (value.includes("\n")) {
      appendLog(`[run-agent:assistant]\n${value}\n`);
    } else {
      appendLog(`[run-agent:assistant] ${value}\n`);
    }
    state.liveAsk.streamChunksLogged = Number(state.liveAsk.streamChunksLogged || 0) + 1;
  };
  while (state.liveAsk.streamLogBuffer.includes("\n")) {
    const idx = state.liveAsk.streamLogBuffer.indexOf("\n");
    const part = state.liveAsk.streamLogBuffer.slice(0, idx);
    state.liveAsk.streamLogBuffer = state.liveAsk.streamLogBuffer.slice(idx + 1);
    flushChunk(part);
  }
  if (state.liveAsk.streamLogBuffer.length >= chunkTarget) {
    const buf = state.liveAsk.streamLogBuffer;
    const boundary = Math.max(
      buf.lastIndexOf(" ", chunkTarget),
      buf.lastIndexOf(".", chunkTarget),
      buf.lastIndexOf(",", chunkTarget),
      buf.lastIndexOf("!", chunkTarget),
      buf.lastIndexOf("?", chunkTarget),
      buf.lastIndexOf(";", chunkTarget),
      buf.lastIndexOf(":", chunkTarget),
    );
    const cut = boundary > minBoundary ? boundary + 1 : chunkTarget;
    const emit = buf.slice(0, cut);
    state.liveAsk.streamLogBuffer = buf.slice(cut);
    flushChunk(emit);
  }
}

function flushLiveAskDeltaLog(force = false) {
  const rest = String(state.liveAsk.streamLogBuffer || "");
  if (!rest.trim()) {
    state.liveAsk.streamLogBuffer = "";
    return;
  }
  if (force || rest.length >= 10) {
    if (rest.includes("\n")) {
      appendLog(`[run-agent:assistant]\n${rest}\n`);
    } else {
      appendLog(`[run-agent:assistant] ${rest}\n`);
    }
    state.liveAsk.streamChunksLogged = Number(state.liveAsk.streamChunksLogged || 0) + 1;
    state.liveAsk.streamLogBuffer = "";
  }
}

function appendLiveAskTurnDoneToLog({
  answer,
  sources,
  backend,
  model,
  indexed,
  error,
  reasoningEffort,
  traceId,
  traceSteps,
}) {
  const answerText = String(answer || "").trim();
  if (answerText && Number(state.liveAsk.streamChunksLogged || 0) === 0) {
    appendLog(`[run-agent:assistant]\n${answerText}\n`);
  }
  const normalizedSources = normalizeAskSourceList(sources || []);
  if (normalizedSources.length) {
    const sourceLabel = normalizedSources
      .map((src) => {
        const start = Number(src.start_line || 0);
        const end = Number(src.end_line || 0);
        const lineText = start > 0 && end >= start ? `${start}-${end}` : (start > 0 ? `${start}` : "-");
        return `[${src.id}] ${src.path}:${lineText}`;
      })
      .join(" ; ");
    appendLog(`[run-agent:sources] ${sourceLabel}\n`);
  }
  const backendLabel = String(backend || "");
  const modelLabel = String(model || "").trim() || "configured default";
  const reasoningLabel = normalizeAskReasoningEffort(reasoningEffort || "off", "");
  const indexedCount = Number(indexed || 0);
  const suffix = String(error || "").trim();
  const traceToken = String(traceId || "").trim();
  const toolCountRaw = Number(traceSteps || 0);
  const toolCount = Number.isFinite(toolCountRaw) && toolCountRaw > 0 ? Math.round(toolCountRaw) : 0;
  appendLog(
    `[run-agent:done] backend=${backendLabel || "-"} model=${modelLabel}${reasoningLabel ? ` reasoning=${reasoningLabel}` : ""} indexed=${indexedCount}${traceToken ? ` trace=${traceToken}` : ""}${toolCount > 0 ? ` tools=${toolCount}` : ""}${suffix ? ` error=${suffix}` : ""}\n`,
  );
}

async function runLiveAskQuestionWithStream(payload) {
  let answerText = "";
  let finalResult = null;
  let sources = [];
  let doneSeen = false;
  const controller = new AbortController();
  state.liveAsk.abortController = controller;
  syncLiveAskBusyControls();
  const timeoutId = window.setTimeout(() => {
    controller.abort("live_ask_stream_timeout");
  }, 240000);
  const streamRes = await fetch("/api/help/ask/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    signal: controller.signal,
  });
  if (!streamRes.ok) {
    window.clearTimeout(timeoutId);
    throw new Error(`${streamRes.status} ${streamRes.statusText}`);
  }
  try {
    await consumeSseResponse(streamRes, (eventName, data) => {
      if (eventName === "meta") {
        const indexed = Number(data?.indexed_files || 0);
        const backend = String(data?.llm_backend || "openai_api");
        const runtimeMode = normalizeAskRuntimeMode(data?.runtime_mode || state.ask.runtimeMode || "auto");
        const defaultModelToken = backend === "codex_cli" ? "$CODEX_MODEL" : "$OPENAI_MODEL";
        const requested = String(data?.requested_model || payload.model || defaultModelToken);
        const logChars = Number(data?.live_log_chars || 0);
        const reasoning = normalizeAskReasoningEffortOptional(data?.reasoning_effort)
          || normalizeAskReasoningEffortOptional(payload.reasoning_effort)
          || "off";
        state.ask.runtimeMode = runtimeMode;
        if (data?.capabilities) {
          state.ask.capabilities = normalizeAskCapabilities(data.capabilities);
          renderAskCapabilities();
        }
        setAskStatus(
          `답변 생성 중 · runtime=${runtimeMode} · backend=${backend} · model=${requested} · reasoning=${reasoning} · indexed=${indexed}${logChars > 0 ? ` · logs=${logChars}` : ""}`,
        );
        return false;
      }
      if (eventName === "activity") {
        const activityId = String(data?.id || "").trim();
        const status = String(data?.status || "running").trim();
        const message = String(data?.message || "").trim();
        if (activityId) {
          setAskActivity(activityId, status, message, data);
          appendLiveAskActivityToLog(activityId, status, message, data);
        }
        return false;
      }
      if (eventName === "delta") {
        const chunk = String(data?.text || "");
        if (!chunk) return false;
        answerText += chunk;
        appendLiveAskDeltaToLog(chunk);
        state.liveAsk.liveAnswer = answerText;
        renderLiveAskThread();
        return false;
      }
      if (eventName === "sources") {
        sources = Array.isArray(data?.sources) ? data.sources : [];
        renderLiveAskSources(sources);
        return false;
      }
      if (eventName === "error") {
        const msg = String(data?.error || data?.message || "stream error");
        throw new Error(msg);
      }
      if (eventName === "done") {
        doneSeen = true;
        finalResult = data && typeof data === "object" ? data : {};
        if (finalResult?.capabilities) {
          state.ask.capabilities = normalizeAskCapabilities(finalResult.capabilities);
          renderAskCapabilities();
        }
        if (!answerText) {
          answerText = String(finalResult.answer || "");
          appendLiveAskDeltaToLog(answerText);
          state.liveAsk.liveAnswer = answerText;
          renderLiveAskThread();
        }
        if (!sources.length) {
          sources = Array.isArray(finalResult.sources) ? finalResult.sources : [];
          renderLiveAskSources(sources);
        }
        return true;
      }
      return false;
    });
    if (!doneSeen) {
      throw new Error("stream ended before done event");
    }
    return {
      ...(finalResult || {}),
      answer: answerText || String(finalResult?.answer || ""),
      sources,
    };
  } finally {
    window.clearTimeout(timeoutId);
    if (state.liveAsk.abortController === controller) {
      state.liveAsk.abortController = null;
    }
    syncLiveAskBusyControls();
  }
}

async function runLiveAskQuestion() {
  if (state.ask.busy || state.liveAsk.busy) {
    setAskStatus("이미 질문을 처리 중입니다. 완료되면 다시 실행하세요.");
    return;
  }
  ensureAskThreadScope(false);
  const liveInput = $("#live-ask-input");
  const rawInput = String(liveInput?.value || "").trim();
  if (!rawInput) {
    setAskStatus("질문을 입력하세요.");
    return;
  }
  const controlResult = await applyAskControlCommand(rawInput);
  if (controlResult.handled) {
    if (liveInput) {
      liveInput.value = "";
      saveLiveAskDraft("");
      updateLiveAskInputMeta();
    }
    return;
  }
  const question = String(controlResult.question || "").trim();
  if (!question) {
    setAskStatus("질문을 입력하세요.");
    return;
  }
  const explicitExecutionIntent = hasExplicitExecutionIntent(question);
  if (liveInput) {
    liveInput.value = "";
    saveLiveAskDraft("");
    updateLiveAskInputMeta();
  }
  if (await tryRunExplicitExecutionShortcut(question)) {
    return;
  }
  const model = askModelInputValue();
  const backend = askBackendInputValue();
  const runtimeMode = askRuntimeModeInputValue();
  const reasoningEffort = askReasoningInputValue();
  const effectiveActionMode = explicitExecutionIntent ? "act" : state.ask.actionMode;
  if (explicitExecutionIntent && state.ask.actionMode !== "act") {
    appendLog("[run-agent:mode] explicit execution intent detected -> temporary act for this turn\n");
  }
  const modelToken = model || (backend === "codex_cli" ? "$CODEX_MODEL" : openaiModelHint());
  const reasoningPolicy = resolveAskReasoningPolicy({
    backend,
    modelToken,
    reasoningEffort,
  });
  if (reasoningEffort !== "off" && !reasoningPolicy.requestEffort) {
    appendLog("[ask:model] reasoning_effort auto-disabled for current model/backend.\n");
  }
  state.ask.reasoningEffort = reasoningPolicy.displayEffort;
  setAskLlmBackend(backend, { persist: false });
  state.ask.busy = true;
  state.liveAsk.busy = true;
  state.liveAsk.pendingQuestion = question;
  state.liveAsk.liveAnswer = "";
  state.liveAsk.pendingSources = [];
  state.liveAsk.lastSources = [];
  state.liveAsk.lastAction = null;
  state.liveAsk.lastAnswer = "";
  state.liveAsk.autoFollowThread = true;
  setAskRunButtonState($("#ask-run"), true);
  setAskRunButtonState($("#live-ask-run"), true);
  syncLiveAskBusyControls();
  const currentRunRel = ensureAskRunRel();
  const historyPayload = normalizeLiveAskHistoryForPayload(14);
  const stateMemoryPayload = buildAskStateMemory({
    runRel: currentRunRel,
    maxChars: 3200,
  });
  const effectiveAutoLogChars = resolveLiveAskEffectiveLogChars(state.liveAsk.autoLogChars);
  const liveLogTail = state.liveAsk.autoLogContext ? buildLiveAskLogTail(effectiveAutoLogChars) : "";
  setAskStatus("코드/문서를 분석 중입니다...");
  resetAskActivityState();
  setAskActivity("source_index", "running", "근거 탐색 준비 중...");
  resetLiveAskLogStreamState();
  state.liveAsk.activeLogStartIndex = state.logBuffer.length;
  renderLiveAskActions();
  appendLiveAskTurnStartToLog(question);
  renderLiveAskThread();
  let usedLegacyFallback = false;
  try {
    const runRel = currentRunRel;
    if (state.ask.runRel !== runRel) {
      await loadAskHistory(runRel);
    }
    renderAskHistory();
    const requestPayload = {
      question,
      agent: resolveAskAgentLabel(),
      execution_mode: effectiveActionMode === "act" ? "act" : "plan",
      model: model || undefined,
      llm_backend: backend,
      runtime_mode: runtimeMode,
      reasoning_effort: reasoningPolicy.requestEffort || undefined,
      strict_model: Boolean(model),
      max_sources: 12,
      history: historyPayload,
      run: runRel || undefined,
      profile_id: askHistoryProfileId(),
      web_search: Boolean($("#federlicht-web-search")?.checked),
      allow_artifacts: effectiveActionMode === "act"
        ? Boolean(state.ask.allowArtifactWrites || explicitExecutionIntent)
        : false,
      live_log_tail: liveLogTail || undefined,
      state_memory: stateMemoryPayload,
    };
    let result;
    try {
      result = await runLiveAskQuestionWithStream(requestPayload);
    } catch (streamErr) {
      if (isLiveAskAbortError(streamErr)) {
        throw streamErr;
      }
      appendLog(`[ask] stream fallback: ${streamErr}\n`);
      usedLegacyFallback = true;
      result = await runAskQuestionLegacy(requestPayload);
      if (result?.capabilities) {
        state.ask.capabilities = normalizeAskCapabilities(result.capabilities);
        renderAskCapabilities();
      }
    }
    const answer = enforceExecutionModeAdviceGuard(String(result?.answer || ""), result);
    const sources = Array.isArray(result?.sources) ? result.sources : [];
    if (usedLegacyFallback) {
      const appliedTrace = applyAskTraceTimeline(result, { reset: true });
      if (!appliedTrace) {
        setAskActivity("source_index", "done", `근거 후보 ${Number(result?.indexed_files || 0)}개`);
        if (requestPayload.web_search) {
          const webNote = String(result?.web_search_note || "");
          const webStatus = webNote.toLowerCase().includes("skipped") ? "skipped" : "done";
          setAskActivity("web_research", webStatus, webNote || "웹 검색 처리 완료");
        } else {
          setAskActivity("web_research", "disabled", "web_search 옵션 꺼짐");
        }
        setAskActivity("llm_generate", result?.used_llm ? "done" : "error", result?.error || "완료");
      }
    }
    state.liveAsk.pendingQuestion = "";
    state.liveAsk.liveAnswer = "";
    state.liveAsk.pendingSources = [];
    const normalizedSources = normalizeAskSourceList(sources);
    state.liveAsk.lastSources = normalizedSources;
    state.liveAsk.lastAction = result?.action || null;
    state.liveAsk.lastAnswer = answer;
    renderLiveAskThread();
    renderLiveAskActions();
    const backendLabel = String(result?.llm_backend || backend || "openai_api");
    const runtimeLabel = normalizeAskRuntimeMode(result?.runtime_mode || runtimeMode || state.ask.runtimeMode || "auto");
    state.ask.runtimeMode = runtimeLabel;
    const indexed = Number(result?.indexed_files || 0);
    const usedReasoning = normalizeAskReasoningEffort(
      normalizeAskReasoningEffortOptional(result?.reasoning_effort) || "off",
      "off",
    );
    const modelLabel = String(
      result?.model
      || result?.requested_model
      || model
      || (backendLabel === "codex_cli" ? "codex-cli-default" : "$OPENAI_MODEL"),
    );
    const liveLogChars = Number(result?.live_log_chars || 0);
    flushLiveAskDeltaLog(true);
    appendLiveAskTurnDoneToLog({
      answer,
      sources,
      backend: backendLabel,
      model: modelLabel,
      reasoningEffort: usedReasoning,
      indexed,
      traceId: result?.trace?.trace_id || "",
      traceSteps: Array.isArray(result?.trace?.steps) ? result.trace.steps.length : 0,
      error: result?.error || "",
    });
    const liveProcessLog = extractLiveAskProcessLog(state.liveAsk.activeLogStartIndex);
    const liveStamp = new Date().toISOString();
    const liveMeta = normalizeLiveAskMeta({
      backend: backendLabel,
      model: modelLabel,
      reasoning: usedReasoning,
      indexed,
      trace_id: String(result?.trace?.trace_id || "").trim(),
      trace_steps: Array.isArray(result?.trace?.steps) ? result.trace.steps.length : 0,
      error: result?.error || "",
    });
    state.liveAsk.history.push({ role: "user", content: question, ts: liveStamp });
    state.liveAsk.history.push({
      role: "assistant",
      content: answer.slice(0, 12000),
      ts: liveStamp,
      sources: normalizedSources,
      action: result?.action || null,
      meta: liveMeta,
      process_log: liveProcessLog,
    });
    if (state.liveAsk.history.length > 80) {
      state.liveAsk.history = state.liveAsk.history.slice(-80);
    }
    saveLiveAskHistory();
    renderLiveAskThread();
    setAskStatus(
      `완료 · runtime=${runtimeLabel} · backend=${backendLabel} · model=${modelLabel} · reasoning=${usedReasoning} · indexed=${indexed}${liveLogChars > 0 ? ` · logs=${liveLogChars}` : ""}`,
    );
    state.ask.lastAction = result?.action || null;
    state.ask.lastAnswer = answer;
    state.ask.lastSources = sources;
    state.ask.pendingSources = [];
    state.ask.pendingQuestion = "";
    state.ask.liveAnswer = "";
    const askStamp = new Date().toISOString();
    state.ask.history.push({ role: "user", content: question, ts: askStamp });
    state.ask.history.push({ role: "assistant", content: answer.slice(0, 12000), ts: askStamp });
    if (state.ask.history.length > 40) {
      state.ask.history = state.ask.history.slice(-40);
    }
    updateActiveThreadMeta({
      title: question.slice(0, 34),
      preview: question.slice(0, 72),
      updated_at: askStamp,
    });
    renderAskHistory();
    const suggestedAction = String(result?.action?.type || "").trim().toLowerCase();
    if (suggestedAction) {
      appendLog(`[run-agent:action] suggested=${suggestedAction}\n`);
      const isWriteAction = isAskWriteActionType(suggestedAction);
      const requiresRunTargetConfirm = isRunTargetActionType(suggestedAction);
      const actionOverride = normalizeAskActionOverride(suggestedAction, result?.action || null);
      const requiresInstructionConfirm = actionRequiresInstructionConfirm(suggestedAction, actionOverride);
      const instructionConfirmReason = actionInstructionConfirmReason(suggestedAction, actionOverride);
      const requiresClarification = Boolean(actionOverride?.clarify_required);
      const bypassRunTargetConfirm = explicitExecutionIntent;
      const bypassInstructionConfirm =
        explicitExecutionIntent
        && instructionConfirmReason === "short_generic_request";
      const canAutoRun =
        (state.ask.actionMode === "act" || explicitExecutionIntent)
        && (!requiresRunTargetConfirm || bypassRunTargetConfirm)
        && (!requiresInstructionConfirm || bypassInstructionConfirm)
        && !requiresClarification
        && (!isWriteAction || state.ask.allowArtifactWrites || explicitExecutionIntent);
      if (canAutoRun) {
        const autoReason = explicitExecutionIntent && state.ask.actionMode !== "act"
          ? "explicit_execute_intent"
          : "act_mode";
        appendLog(`[run-agent:action] auto-run=${suggestedAction} (${autoReason})\n`);
        await executeAskSuggestedAction(suggestedAction, {
          allowWhileBusy: true,
          actionOverride,
          instructionConfirmed: bypassInstructionConfirm,
        });
      } else if (state.ask.actionMode === "act" && (requiresRunTargetConfirm || requiresInstructionConfirm)) {
        const reasons = [
          requiresRunTargetConfirm ? "run-target" : "",
          requiresInstructionConfirm ? "instruction" : "",
        ].filter(Boolean).join("+");
        appendLog(`[run-agent:action] deferred=${suggestedAction} (${reasons} confirmation required)\n`);
        setAskStatus(
          requiresInstructionConfirm
            ? "Instruction 확인이 필요해 확인 모달을 열었습니다."
            : "Run 대상 확인이 필요해 확인 모달을 열었습니다.",
        );
        await runAskSuggestedAction(suggestedAction, { actionOverride });
      } else if (state.ask.actionMode === "act" && requiresClarification) {
        appendLog(`[run-agent:action] deferred=${suggestedAction} (clarification required)\n`);
        setAskStatus("실행 전 주제 보강 질문이 필요합니다. 제안 버튼의 '질의 보강하기'를 사용하세요.");
      } else if (state.ask.actionMode === "act" && isWriteAction && !state.ask.allowArtifactWrites) {
        appendLog("[run-agent:action] skipped: 파일쓰기허용 비활성\n");
      }
    }
    await saveAskHistory();
  } catch (err) {
    const aborted = isLiveAskAbortError(err);
    const errorText = aborted ? "질문이 중단되었습니다." : `질문 실패: ${err}`;
    flushLiveAskDeltaLog(true);
    appendLiveAskTurnDoneToLog({
      answer: "",
      sources: [],
      backend,
      model: model || (backend === "codex_cli" ? "codex-cli-default" : "$OPENAI_MODEL"),
      reasoningEffort: "off",
      indexed: 0,
      traceId: "",
      traceSteps: 0,
      error: aborted ? "live_ask_aborted" : String(err),
    });
    const errorProcessLog = extractLiveAskProcessLog(state.liveAsk.activeLogStartIndex);
    const errorStamp = new Date().toISOString();
    const errorMeta = normalizeLiveAskMeta({
      backend,
      model: model || (backend === "codex_cli" ? "codex-cli-default" : "$OPENAI_MODEL"),
      reasoning: "off",
      indexed: 0,
      error: aborted ? "live_ask_aborted" : String(err),
    });
    state.liveAsk.history.push({ role: "user", content: question, ts: errorStamp });
    state.liveAsk.history.push({
      role: "assistant",
      content: errorText.slice(0, 12000),
      ts: errorStamp,
      sources: [],
      action: null,
      meta: errorMeta,
      process_log: errorProcessLog,
    });
    if (state.liveAsk.history.length > 80) {
      state.liveAsk.history = state.liveAsk.history.slice(-80);
    }
    saveLiveAskHistory();
    if (aborted) {
      setAskStatus("질문이 중단되었습니다.");
    } else {
      setAskStatus(`질문 실패: ${err}`);
    }
    setAskActivity("llm_generate", "error", aborted ? "질문이 중단되었습니다." : `질문 실패: ${err}`);
    state.liveAsk.pendingQuestion = "";
    state.liveAsk.liveAnswer = errorText;
    state.liveAsk.pendingSources = [];
    state.liveAsk.lastAction = null;
    state.liveAsk.lastAnswer = "";
    renderLiveAskThread();
    renderLiveAskActions();
  } finally {
    state.liveAsk.activeLogStartIndex = -1;
    state.ask.busy = false;
    state.liveAsk.busy = false;
    setAskRunButtonState($("#ask-run"), false);
    setAskRunButtonState($("#live-ask-run"), false);
    syncLiveAskBusyControls();
  }
}

async function runAskQuestion() {
  if (state.ask.busy) return;
  ensureAskThreadScope(false);
  setAskThreadPopoverOpen(false);
  const askInput = $("#ask-input");
  const rawInput = String(askInput?.value || "").trim();
  const model = askModelInputValue();
  const backend = askBackendInputValue();
  const runtimeMode = askRuntimeModeInputValue();
  const reasoningEffort = askReasoningInputValue();
  const modelToken = model || (backend === "codex_cli" ? "$CODEX_MODEL" : openaiModelHint());
  const reasoningPolicy = resolveAskReasoningPolicy({
    backend,
    modelToken,
    reasoningEffort,
  });
  if (reasoningEffort !== "off" && !reasoningPolicy.requestEffort) {
    appendLog("[ask:model] reasoning_effort auto-disabled for current model/backend.\n");
  }
  state.ask.reasoningEffort = reasoningPolicy.displayEffort;
  setAskLlmBackend(backend, { persist: false });
  if (!rawInput) {
    setAskStatus("질문을 입력하세요.");
    return;
  }
  const controlResult = await applyAskControlCommand(rawInput);
  if (controlResult.handled) {
    if (askInput) {
      askInput.value = "";
    }
    return;
  }
  const question = String(controlResult.question || "").trim();
  if (!question) {
    setAskStatus("질문을 입력하세요.");
    return;
  }
  const explicitExecutionIntent = hasExplicitExecutionIntent(question);
  if (askInput) {
    askInput.value = "";
  }
  const effectiveActionMode = explicitExecutionIntent ? "act" : state.ask.actionMode;
  if (explicitExecutionIntent && state.ask.actionMode !== "act") {
    appendLog("[ask:mode] explicit execution intent detected -> temporary act for this turn\n");
  }
  state.ask.busy = true;
  state.ask.lastAction = null;
  state.ask.lastAnswer = "";
  state.ask.lastSources = [];
  state.ask.pendingSources = [];
  state.ask.pendingQuestion = question;
  state.ask.liveAnswer = "";
  state.ask.selectionText = "";
  state.ask.autoFollowAnswer = true;
  syncAskJumpLatestVisibility();
  const runButton = $("#ask-run");
  setAskRunButtonState(runButton, true);
  setAskStatus("코드/문서를 분석 중입니다...");
  resetAskActivityState();
  setAskActivity("source_index", "running", "근거 탐색 준비 중...");
  renderAskActions(null, "", []);
  renderAskAnswer("");
  renderAskSources([]);
  try {
    const runRel = ensureAskRunRel();
    if (state.ask.runRel !== runRel) {
      await loadAskHistory(runRel);
    }
    renderAskHistory();
    const requestPayload = {
      question,
      agent: resolveAskAgentLabel(),
      execution_mode: effectiveActionMode === "act" ? "act" : "plan",
      model: model || undefined,
      llm_backend: backend,
      runtime_mode: runtimeMode,
      reasoning_effort: reasoningPolicy.requestEffort || undefined,
      strict_model: Boolean(model),
      max_sources: 12,
      history: buildAskHistoryPayload(state.ask.history, {
        recentTurns: 14,
        summaryTurns: 24,
        summaryMaxChars: 2200,
      }),
      run: runRel || undefined,
      profile_id: askHistoryProfileId(),
      web_search: Boolean($("#federlicht-web-search")?.checked),
      allow_artifacts: effectiveActionMode === "act"
        ? Boolean(state.ask.allowArtifactWrites || explicitExecutionIntent)
        : false,
      state_memory: buildAskStateMemory({
        runRel,
        maxChars: 3200,
      }),
    };
    let result;
    try {
      result = await runAskQuestionWithStream(requestPayload);
    } catch (streamErr) {
      appendLog(`[ask] stream fallback: ${streamErr}\n`);
      result = await runAskQuestionLegacy(requestPayload);
      state.ask.capabilities = normalizeAskCapabilities(result?.capabilities || ASK_CAPABILITY_FALLBACK);
      const appliedTrace = applyAskTraceTimeline(result, { reset: true });
      if (!appliedTrace) {
        setAskActivity("source_index", "done", `근거 후보 ${Number(result?.indexed_files || 0)}개`);
        if (requestPayload.web_search) {
          const webNote = String(result?.web_search_note || "");
          const webStatus = webNote.toLowerCase().includes("skipped") ? "skipped" : "done";
          setAskActivity("web_research", webStatus, webNote || "웹 검색 처리 완료");
        } else {
          setAskActivity("web_research", "disabled", "web_search 옵션 꺼짐");
        }
        setAskActivity("llm_generate", result?.used_llm ? "done" : "error", result?.error || "완료");
      }
    }
    const guardedAnswer = enforceExecutionModeAdviceGuard(String(result?.answer || ""), result);
    renderAskAnswer(guardedAnswer);
    renderAskSources(result.sources || []);
    renderAskActions(result.action || null, guardedAnswer, result.sources || []);
    state.ask.lastAction = result.action || null;
    state.ask.lastAnswer = guardedAnswer;
    state.ask.lastSources = Array.isArray(result.sources) ? result.sources : [];
    state.ask.pendingSources = [];
    if (result?.capabilities) {
      state.ask.capabilities = normalizeAskCapabilities(result.capabilities);
      renderAskCapabilities();
    }
    const stamp = new Date().toISOString();
    state.ask.history.push({ role: "user", content: question, ts: stamp });
    state.ask.history.push({
      role: "assistant",
      content: guardedAnswer.slice(0, 12000),
      ts: stamp,
    });
    if (state.ask.history.length > 40) {
      state.ask.history = state.ask.history.slice(-40);
    }
    state.liveAsk.history = normalizeLiveAskStoredHistory(state.ask.history, 80);
    saveLiveAskHistory();
    renderLiveAskThread();
    state.ask.pendingQuestion = "";
    renderAskAnswer("");
    updateActiveThreadMeta({
      title: question.slice(0, 34),
      preview: question.slice(0, 72),
      updated_at: stamp,
    });
    renderAskHistory();
    renderAskThreadList();
    await saveAskHistory();
    const defaultModelToken = backend === "codex_cli" ? "$CODEX_MODEL" : "$OPENAI_MODEL";
    const modelLabel = result.model || (model || defaultModelToken);
    const requestedModel = result.requested_model || model || defaultModelToken;
    const backendLabel = String(result.llm_backend || "openai_api");
    const runtimeLabel = normalizeAskRuntimeMode(result?.runtime_mode || runtimeMode || state.ask.runtimeMode || "auto");
    state.ask.runtimeMode = runtimeLabel;
    const usedReasoning = normalizeAskReasoningEffort(
      normalizeAskReasoningEffortOptional(result.reasoning_effort) || "off",
      "off",
    );
    const showRequested = Boolean(model || result.model_fallback);
    const indexed = Number(result.indexed_files || 0);
    if (result.used_llm) {
      if (showRequested) {
        setAskStatus(
          `완료 · runtime=${runtimeLabel} · backend=${backendLabel} · model=${modelLabel} (requested=${requestedModel}) · reasoning=${usedReasoning} · indexed=${indexed}`,
        );
      } else {
        setAskStatus(`완료 · runtime=${runtimeLabel} · backend=${backendLabel} · model=${modelLabel} · reasoning=${usedReasoning} · indexed=${indexed}`);
      }
    } else if (result.error) {
      setAskStatus(
        `완료(fallback) · runtime=${runtimeLabel} · backend=${backendLabel} · reasoning=${usedReasoning} · indexed=${indexed} · ${result.error}`,
      );
    } else {
      setAskStatus(`완료(fallback) · runtime=${runtimeLabel} · backend=${backendLabel} · reasoning=${usedReasoning} · indexed=${indexed}`);
    }
  } catch (err) {
    setAskStatus(`질문 실패: ${err}`);
    renderAskAnswer(`질문 실패: ${err}`);
    renderAskSources([]);
    renderAskActions(null, "", []);
    setAskActivity("llm_generate", "error", `질문 실패: ${err}`);
    state.ask.pendingQuestion = "";
    state.ask.pendingSources = [];
  } finally {
    state.ask.busy = false;
    state.ask.pendingQuestion = "";
    setAskRunButtonState(runButton, false);
  }
}

function handleAskPanel() {
  const panel = $("#ask-panel");
  if (!panel) return;
  loadAskActionPrefs();
  loadLiveAskPrefs();
  ensureAskThreadScope(true);
  renderAskHistory();
  renderAskThreadList();
  renderAskAnswer("");
  renderAskSources([]);
  renderLiveAskThread();
  renderLiveAskActions();
  renderAskActions(null, "", []);
  renderAskSourcesTrace();
  state.ask.capabilities = normalizeAskCapabilities(ASK_CAPABILITY_FALLBACK);
  state.ask.capabilityRegistry = normalizeCapabilityRegistry({});
  state.ask.autoFollowAnswer = true;
  resetAskActivityState();
  renderAskCapabilityManager();
  renderCapabilityStudio();
  syncAskActionPolicyInputs();
  syncAskJumpLatestVisibility();
  setAskThreadPopoverOpen(false);
  setAskCapabilityManagerOpen(false);
  setAskCapabilityDetailOpen(false);
  setAskStatus("Ready.");
  setCapabilityStudioStatus("Ready.");
  setAskRunButtonState($("#ask-run"), false);
  setAskRunButtonState($("#live-ask-run"), false);
  syncLiveAskBusyControls();
  const liveInput = $("#live-ask-input");
  if (liveInput) {
    const draft = loadLiveAskDraft();
    if (draft) liveInput.value = draft;
  }
  syncLiveAskPrefsInputs();
  updateLiveAskInputMeta();
  ensureLiveAskLayoutObserver();
  const threadToggle = $("#ask-thread-toggle");
  const threadPopover = $("#ask-thread-popover");
  $("#ask-button")?.addEventListener("click", (ev) => {
    ev.preventDefault();
    ev.stopPropagation();
    if (state.ask.open) {
      setAskPanelOpen(false);
      return;
    }
    const anchor = { x: ev.clientX || window.innerWidth - 80, y: ev.clientY || 80 };
    setAskPanelOpen(true, { anchor });
  });
  $("#ask-close")?.addEventListener("click", () => setAskPanelOpen(false));
  $("#ask-open-llm-settings")?.addEventListener("click", () => {
    openModelPolicyModal();
  });
  $("#ask-reset")?.addEventListener("click", () => {
    clearAskHistoryAndUi().catch((err) => {
      setAskStatus(`Reset failed: ${err}`);
    });
  });
  $("#ask-geometry-reset")?.addEventListener("click", () => {
    resetAskGeometry();
    setAskStatus("패널 위치/크기를 초기화했습니다.");
  });
  $("#ask-thread-new")?.addEventListener("click", () => {
    createNewAskThread().catch((err) => {
      setAskStatus(`새 스레드 생성 실패: ${err}`);
    });
  });
  $("#ask-thread-delete")?.addEventListener("click", () => {
    deleteActiveAskThread().catch((err) => {
      setAskStatus(`스레드 삭제 실패: ${err}`);
    });
  });
  threadToggle?.addEventListener("click", (ev) => {
    ev.preventDefault();
    ev.stopPropagation();
    setAskThreadPopoverOpen(!state.ask.threadPopoverOpen);
  });
  $("#ask-action-mode-switch")?.addEventListener("click", (ev) => {
    const button = ev.target instanceof Element ? ev.target.closest("[data-ask-mode]") : null;
    if (!button) return;
    const mode = button.getAttribute("data-ask-mode") || "plan";
    setAskActionMode(mode, { persist: true });
  });
  $("#live-ask-mode-switch")?.addEventListener("click", (ev) => {
    const button = ev.target instanceof Element ? ev.target.closest("[data-ask-mode]") : null;
    if (!button) return;
    const mode = button.getAttribute("data-ask-mode") || "plan";
    setAskActionMode(mode, { persist: true });
  });
  $("#ask-backend")?.addEventListener("change", (ev) => {
    setAskLlmBackend(ev?.target?.value, { persist: true });
    maybeSyncGlobalModelPolicyFromSource("ask");
  });
  $("#live-ask-backend")?.addEventListener("change", (ev) => {
    setAskLlmBackend(ev?.target?.value, { persist: true });
    maybeSyncGlobalModelPolicyFromSource("ask");
  });
  $("#live-ask-runtime-mode")?.addEventListener("change", (ev) => {
    setAskRuntimeMode(ev?.target?.value, { persist: true });
  });
  $("#ask-model")?.addEventListener("input", () => {
    syncAskActionPolicyInputs();
    maybeSyncGlobalModelPolicyFromSource("ask");
  });
  $("#ask-model")?.addEventListener("change", () => {
    syncAskActionPolicyInputs();
    maybeSyncGlobalModelPolicyFromSource("ask");
  });
  $("#live-ask-model")?.addEventListener("input", () => {
    syncAskActionPolicyInputs();
    maybeSyncGlobalModelPolicyFromSource("ask");
  });
  $("#live-ask-model")?.addEventListener("change", () => {
    syncAskActionPolicyInputs();
    maybeSyncGlobalModelPolicyFromSource("ask");
  });
  $("#ask-reasoning-effort")?.addEventListener("change", (ev) => {
    setAskReasoningEffort(ev?.target?.value, { persist: true });
    maybeSyncGlobalModelPolicyFromSource("ask");
  });
  $("#live-ask-reasoning-effort")?.addEventListener("change", (ev) => {
    setAskReasoningEffort(ev?.target?.value, { persist: true });
    maybeSyncGlobalModelPolicyFromSource("ask");
  });
  $("#ask-allow-artifacts")?.addEventListener("change", (ev) => {
    state.ask.allowArtifactWrites = Boolean(ev?.target?.checked);
    saveAskActionPrefs();
    syncAskActionPolicyInputs();
  });
  $("#live-ask-allow-artifacts")?.addEventListener("change", (ev) => {
    state.ask.allowArtifactWrites = Boolean(ev?.target?.checked);
    saveAskActionPrefs();
    syncAskActionPolicyInputs();
  });
  $("#live-ask-auto-log")?.addEventListener("change", (ev) => {
    state.liveAsk.autoLogContext = Boolean(ev?.target?.checked);
    saveLiveAskPrefs();
    updateLiveAskInputMeta();
  });
  $("#live-ask-log-tail-size")?.addEventListener("change", (ev) => {
    state.liveAsk.autoLogChars = normalizeLiveAskLogTailChars(ev?.target?.value, state.liveAsk.autoLogChars);
    saveLiveAskPrefs();
    updateLiveAskInputMeta();
  });
  $("#ask-run")?.addEventListener("click", () => runAskQuestion());
  $("#live-ask-run")?.addEventListener("click", () => {
    if (state.liveAsk.busy) {
      cancelLiveAskQuestion();
      return;
    }
    runLiveAskQuestion();
  });
  $("#live-ask-stop")?.addEventListener("click", () => cancelLiveAskQuestion());
  $("#live-ask-copy")?.addEventListener("click", () => {
    copyLiveAskTranscript().catch((err) => setAskStatus(`대화 복사 실패: ${err}`));
  });
  $("#live-ask-clear")?.addEventListener("click", () => {
    clearLiveAskConversation();
  });
  $("#live-ask-settings-open")?.addEventListener("click", () => {
    setWorkspacePanelOpen(true, "agents");
  });
  $("#live-ask-use-log")?.addEventListener("click", () => {
    useRecentLogsAsLiveAskPrompt();
  });
  $("#live-ask-jump-latest")?.addEventListener("click", () => {
    scrollLiveAskThreadToLatest();
  });
  document.querySelectorAll("[data-live-ask-prompt]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const prompt = btn.getAttribute("data-live-ask-prompt") || "";
      if (!prompt) return;
      setLiveAskInputValue(prompt, { append: false, focus: true });
      setAskStatus("빠른 프롬프트를 입력창에 넣었습니다.");
    });
  });
  $("#ask-input")?.addEventListener("keydown", (ev) => {
    if ((ev.ctrlKey || ev.metaKey) && ev.key === "Enter") {
      ev.preventDefault();
      runAskQuestion();
    }
  });
  $("#live-ask-input")?.addEventListener("keydown", (ev) => {
    if (ev.isComposing || ev.keyCode === 229) return;
    if (ev.key === "Enter" && !ev.shiftKey) {
      ev.preventDefault();
      runLiveAskQuestion();
    }
  });
  $("#live-ask-input")?.addEventListener("input", () => {
    saveLiveAskDraft($("#live-ask-input")?.value || "");
    updateLiveAskInputMeta();
  });
  $("#live-ask-runtime-fold")?.addEventListener("toggle", () => {
    syncAskActionPolicyInputs();
    window.requestAnimationFrame(() => updateLiveAskThreadInset());
  });
  window.addEventListener("resize", () => {
    window.requestAnimationFrame(() => updateLiveAskThreadInset());
  });
  const answerEl = $("#ask-answer");
  if (answerEl) {
    answerEl.addEventListener("scroll", () => {
      updateAskAutoFollowState();
      syncAskJumpLatestVisibility();
    });
    answerEl.addEventListener("mousedown", (ev) => {
      if (ev.button !== 0) return;
      state.ask.selectionDragging = true;
    });
    answerEl.addEventListener("mouseup", () => {
      state.ask.selectionDragging = false;
      window.setTimeout(() => updateAskSelectionState({ refreshUi: true, forceRender: true }), 0);
    });
    answerEl.addEventListener("keyup", () => {
      window.setTimeout(() => updateAskSelectionState({ refreshUi: true }), 0);
    });
  }
  $("#ask-jump-latest")?.addEventListener("click", () => {
    state.ask.autoFollowAnswer = true;
    scheduleAskScrollToBottom(true);
    syncAskJumpLatestVisibility();
  });
  $("#live-ask-thread")?.addEventListener("scroll", () => {
    updateLiveAskAutoFollowState();
  });
  $("#ask-trace-toggle")?.addEventListener("click", () => {
    state.ask.traceShowHistory = !state.ask.traceShowHistory;
    renderAskSourcesTrace();
  });
  document.addEventListener("mouseup", () => {
    if (!state.ask.open || !state.ask.selectionDragging) return;
    state.ask.selectionDragging = false;
    window.setTimeout(() => updateAskSelectionState({ refreshUi: true, forceRender: true }), 0);
  });
  document.addEventListener("selectionchange", () => {
    if (!state.ask.open) return;
    if (state.ask.selectionDragging) return;
    updateAskSelectionState({ refreshUi: true });
  });
  document.querySelectorAll("[data-askaction-close]").forEach((node) => {
    node.addEventListener("click", () => closeAskActionModal());
  });
  $("#ask-action-confirm")?.addEventListener("click", async () => {
    const pending = state.ask.pendingAction;
    const actionType = pending?.type || "";
    const actionOverride = collectAskActionRunTargetOverride();
    if (!actionType) {
      closeAskActionModal();
      return;
    }
    if (isAskActionInstructionConfirmRequired() && !isAskActionInstructionConfirmChecked()) {
      setAskStatus("Instruction 초안 확인 체크를 완료한 뒤 실행하세요.");
      updateAskActionInstructionConfirmNote();
      updateAskActionRunTargetNote();
      return;
    }
    if (isRunTargetActionType(actionType)) {
      const runHint = normalizeRunHint(actionOverride?.run_hint || "");
      if (normalizeAskActionType(actionType) === "switch_run" && !runHint) {
        setAskStatus("Run 전환은 대상 run 이름/경로를 지정해야 합니다.");
        updateAskActionRunTargetNote();
        return;
      }
    }
    closeAskActionModal();
    await executeAskSuggestedAction(actionType, {
      actionOverride,
      instructionConfirmed: true,
    });
  });
  $("#ask-action-run-target")?.addEventListener("input", () => {
    const input = $("#ask-action-run-target");
    if (input) {
      const raw = String(input.value || "");
      const normalized = raw.replace(/\s+/g, "_").replace(/_+/g, "_");
      if (raw !== normalized) {
        input.value = normalized;
      }
    }
    const box = $("#ask-action-run-target-box");
    const confirmCheck = $("#ask-action-run-target-confirm");
    if (box?.dataset?.requireRunConfirm === "1" && confirmCheck) {
      confirmCheck.checked = false;
    }
    updateAskActionRunTargetNote();
  });
  $("#ask-action-run-target")?.addEventListener("change", () => {
    const input = $("#ask-action-run-target");
    const createCheck = $("#ask-action-run-create");
    if (!input || !createCheck?.checked) {
      updateAskActionRunTargetNote();
      return;
    }
    const hinted = normalizeRunHint(input.value || "");
    const resolved = hinted ? resolveRunRelFromHint(hinted, { strict: true }) : "";
    if (!resolved && hinted) {
      const sanitized = sanitizeRunNameHint(hinted);
      if (sanitized) {
        input.value = sanitized;
      }
    }
    updateAskActionRunTargetNote();
  });
  $("#ask-action-run-create")?.addEventListener("change", () => {
    const box = $("#ask-action-run-target-box");
    const confirmCheck = $("#ask-action-run-target-confirm");
    if (box?.dataset?.requireRunConfirm === "1" && confirmCheck) {
      confirmCheck.checked = false;
    }
    updateAskActionRunTargetNote();
  });
  $("#ask-action-run-target-confirm")?.addEventListener("change", () => {
    updateAskActionRunTargetNote();
  });
  $("#ask-action-instruction-confirm")?.addEventListener("change", () => {
    updateAskActionInstructionConfirmNote();
    updateAskActionRunTargetNote();
  });
  $("#ask-action-use-suggested-run")?.addEventListener("click", () => {
    const input = $("#ask-action-run-target");
    const box = $("#ask-action-run-target-box");
    const confirmCheck = $("#ask-action-run-target-confirm");
    const suggested = normalizeRunHint(box?.dataset?.suggestedRun || "");
    if (!input || !suggested) return;
    input.value = suggested;
    if (box?.dataset?.requireRunConfirm === "1" && confirmCheck) {
      confirmCheck.checked = true;
    }
    updateAskActionRunTargetNote();
    input.focus();
    input.select();
  });
  $("#ask-action-use-current-run")?.addEventListener("click", () => {
    const input = $("#ask-action-run-target");
    const box = $("#ask-action-run-target-box");
    const confirmCheck = $("#ask-action-run-target-confirm");
    const selected = stripSiteRunsPrefix(normalizePathString(selectedRunRel() || "")) || "";
    if (!input) return;
    input.value = selected;
    if (box?.dataset?.requireRunConfirm === "1" && confirmCheck) {
      confirmCheck.checked = true;
    }
    updateAskActionRunTargetNote();
    input.focus();
    input.select();
  });
  $("#ask-action-clear-run-target")?.addEventListener("click", () => {
    const input = $("#ask-action-run-target");
    const confirmCheck = $("#ask-action-run-target-confirm");
    if (!input) return;
    input.value = "";
    if (confirmCheck) confirmCheck.checked = false;
    updateAskActionRunTargetNote();
    input.focus();
  });
  panel.addEventListener("click", (ev) => {
    ev.stopPropagation();
    const target = ev.target;
    if (!(target instanceof Element)) return;
    if (state.ask.threadPopoverOpen) {
      if (target.closest("#ask-thread-popover")) return;
      if (target.closest("#ask-thread-toggle")) return;
      setAskThreadPopoverOpen(false);
    }
  });
  threadPopover?.addEventListener("click", (ev) => {
    ev.stopPropagation();
  });
  document.addEventListener("click", () => {
    if (!state.ask.threadPopoverOpen) return;
    setAskThreadPopoverOpen(false);
  });
  $("#federlicht-web-search")?.addEventListener("change", () => {
    loadAskCapabilityRegistry({ silent: true }).catch(() => {});
  });
  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape" && isAskActionModalOpen()) {
      closeAskActionModal();
      return;
    }
    if (ev.key === "Escape" && state.ask.open) {
      setAskPanelOpen(false);
    }
  });
  const head = panel.querySelector(".ask-panel-head");
  if (head) {
    let dragOffsetX = 0;
    let dragOffsetY = 0;
    let dragging = false;
    const move = (ev) => {
      if (!dragging) return;
      panel.style.left = `${Math.round(ev.clientX - dragOffsetX)}px`;
      panel.style.top = `${Math.round(ev.clientY - dragOffsetY)}px`;
      panel.style.right = "auto";
      clampAskPanelPosition();
    };
    const end = () => {
      if (!dragging) return;
      dragging = false;
      document.removeEventListener("pointermove", move);
      document.removeEventListener("pointerup", end);
      saveAskGeometry();
    };
    head.addEventListener("pointerdown", (ev) => {
      const target = ev.target;
      if (!(target instanceof Element)) return;
      if (target.closest("button") || target.closest("input") || target.closest("textarea")) return;
      const rect = panel.getBoundingClientRect();
      dragOffsetX = ev.clientX - rect.left;
      dragOffsetY = ev.clientY - rect.top;
      dragging = true;
      document.addEventListener("pointermove", move);
      document.addEventListener("pointerup", end);
    });
  }
  if (typeof ResizeObserver !== "undefined") {
    const observer = new ResizeObserver(() => {
      if (!state.ask.open) return;
      window.requestAnimationFrame(() => {
        clampAskPanelPosition();
      });
    });
    observer.observe(panel);
  }
  window.addEventListener("resize", () => {
    if (!state.ask.open) return;
    clampAskPanelPosition();
  });
}

async function runAskQuestionLegacy(payload) {
  return fetchJSON("/api/help/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

async function consumeSseResponse(response, onEvent) {
  if (!response.body) {
    throw new Error("stream body is empty");
  }
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  const flushChunk = (rawChunk) => {
    const chunk = String(rawChunk || "").trim();
    if (!chunk) return false;
    let eventName = "message";
    const dataLines = [];
    chunk.split(/\r?\n/).forEach((line) => {
      if (line.startsWith("event:")) {
        eventName = line.slice(6).trim() || "message";
      } else if (line.startsWith("data:")) {
        dataLines.push(line.slice(5).trimStart());
      }
    });
    if (!dataLines.length) return false;
    const rawData = dataLines.join("\n");
    let payload;
    try {
      payload = JSON.parse(rawData);
    } catch (err) {
      payload = { raw: rawData };
    }
    const maybeStop = onEvent(eventName, payload);
    return maybeStop === true;
  };
  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true }).replace(/\r\n/g, "\n");
      let sep = buffer.indexOf("\n\n");
      while (sep >= 0) {
        const part = buffer.slice(0, sep);
        buffer = buffer.slice(sep + 2);
        if (flushChunk(part)) {
          reader.cancel().catch(() => {});
          return;
        }
        sep = buffer.indexOf("\n\n");
      }
    }
    buffer += decoder.decode().replace(/\r\n/g, "\n");
    flushChunk(buffer);
  } finally {
    reader.releaseLock();
  }
}

async function runAskQuestionWithStream(payload) {
  let answerText = "";
  let finalResult = null;
  let sources = [];
  let doneSeen = false;
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => {
    controller.abort("ask_stream_timeout");
  }, 240000);
  const streamRes = await fetch("/api/help/ask/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    signal: controller.signal,
  });
  if (!streamRes.ok) {
    window.clearTimeout(timeoutId);
    throw new Error(`${streamRes.status} ${streamRes.statusText}`);
  }
  try {
    await consumeSseResponse(streamRes, (eventName, data) => {
      if (eventName === "meta") {
        const indexed = Number(data?.indexed_files || 0);
        const backend = String(data?.llm_backend || "openai_api");
        const runtimeMode = normalizeAskRuntimeMode(data?.runtime_mode || state.ask.runtimeMode || "auto");
        const defaultModelToken = backend === "codex_cli" ? "$CODEX_MODEL" : "$OPENAI_MODEL";
        const requested = String(data?.requested_model || payload.model || defaultModelToken);
        const reasoning = normalizeAskReasoningEffortOptional(data?.reasoning_effort)
          || normalizeAskReasoningEffortOptional(payload.reasoning_effort)
          || "off";
        state.ask.runtimeMode = runtimeMode;
        if (data?.capabilities) {
          state.ask.capabilities = normalizeAskCapabilities(data.capabilities);
          renderAskCapabilities();
        }
        setAskActivity("source_index", "done", `근거 후보 ${indexed}개`);
        if (payload.web_search) {
          const webNote = String(data?.web_search_note || "");
          if (webNote.toLowerCase().includes("skipped")) {
            setAskActivity("web_research", "skipped", webNote || "웹 검색 생략");
          }
        } else {
          setAskActivity("web_research", "disabled", "web_search 옵션 꺼짐");
        }
        setAskStatus(
          `답변 생성 중 · runtime=${runtimeMode} · backend=${backend} · model=${requested} · reasoning=${reasoning} · indexed=${indexed}`,
        );
        return false;
      }
      if (eventName === "activity") {
        const activityId = String(data?.id || "").trim();
        const status = String(data?.status || "running").trim();
        const message = String(data?.message || "").trim();
        if (activityId) {
          setAskActivity(activityId, status, message, data);
        }
        return false;
      }
      if (eventName === "delta") {
        const chunk = String(data?.text || "");
        if (!chunk) return false;
        answerText += chunk;
        renderAskAnswer(answerText);
        if (state.ask.autoFollowAnswer) {
          scheduleAskScrollToBottom(true);
        }
        return false;
      }
      if (eventName === "sources") {
        const next = Array.isArray(data?.sources) ? data.sources : [];
        sources = next;
        renderAskSources(sources);
        return false;
      }
      if (eventName === "error") {
        const msg = String(data?.error || data?.message || "stream error");
        throw new Error(msg);
      }
      if (eventName === "done") {
        doneSeen = true;
        finalResult = data && typeof data === "object" ? data : {};
        if (finalResult?.capabilities) {
          state.ask.capabilities = normalizeAskCapabilities(finalResult.capabilities);
          renderAskCapabilities();
        }
        setAskActivity(
          "llm_generate",
          finalResult?.used_llm ? "done" : "error",
          finalResult?.error ? String(finalResult.error) : "답변 생성 완료",
        );
        if (!answerText) {
          answerText = String(finalResult.answer || "");
          renderAskAnswer(answerText);
        }
        if (!sources.length) {
          const src = Array.isArray(finalResult.sources) ? finalResult.sources : [];
          sources = src;
          renderAskSources(sources);
        }
        return true;
      }
      return false;
    });
    if (!doneSeen) {
      throw new Error("stream ended before done event");
    }
    return {
      ...(finalResult || {}),
      answer: answerText || String(finalResult?.answer || ""),
      sources,
    };
  } finally {
    window.clearTimeout(timeoutId);
  }
}

function setWorkspaceTab(tabKey) {
  const resolved = tabKey === "agents" || tabKey === "capabilities" ? tabKey : "templates";
  state.workspace.tab = resolved;
  document.querySelectorAll("[data-workspace-tab]").forEach((btn) => {
    const active = btn.getAttribute("data-workspace-tab") === resolved;
    btn.classList.toggle("active", active);
    btn.setAttribute("aria-selected", active ? "true" : "false");
  });
  document.querySelectorAll("[data-workspace-pane]").forEach((pane) => {
    const active = pane.getAttribute("data-workspace-pane") === resolved;
    pane.classList.toggle("active", active);
  });
  $("#workspace-open-settings")?.classList.toggle("is-active", state.workspace.open);
  $("#live-ask-settings-open")?.classList.toggle("is-active", state.workspace.open && resolved === "agents");
  if (resolved === "capabilities") {
    renderCapabilityStudio();
    setCapabilityStudioStatus("Capability Studio ready.");
    loadAskCapabilityRegistry({ silent: true }).catch(() => {});
  }
}

function setWorkspacePanelOpen(open, tabKey) {
  const panel = $("#workspace-panel");
  if (!panel) return;
  state.workspace.open = Boolean(open);
  panel.classList.toggle("open", state.workspace.open);
  panel.setAttribute("aria-hidden", state.workspace.open ? "false" : "true");
  panel.style.display = state.workspace.open ? "block" : "none";
  if (state.workspace.open) {
    resetDragOffset(panel);
    setWorkspaceTab(tabKey || state.workspace.tab || "templates");
  } else {
    $("#workspace-open-settings")?.classList.remove("is-active");
    $("#live-ask-settings-open")?.classList.remove("is-active");
    resetDragOffset(panel);
  }
}

function scrollAskAnswerToBottom(force = false) {
  const answerEl = $("#ask-answer");
  if (!answerEl) return;
  const targetEl = answerEl;
  const shouldScroll = force || Boolean(state.ask.autoFollowAnswer) || isNearBottom(targetEl, 140);
  if (!shouldScroll) return;
  if (force) {
    state.ask.autoFollowAnswer = true;
  }
  targetEl.scrollTop = targetEl.scrollHeight;
  const last = answerEl.lastElementChild;
  if (last && typeof last.scrollIntoView === "function") {
    last.scrollIntoView({ block: "end", inline: "nearest" });
  }
}

function updateAskAutoFollowState() {
  const answerEl = $("#ask-answer");
  const targetEl = answerEl;
  if (!targetEl) return;
  state.ask.autoFollowAnswer = isNearBottom(targetEl, 140);
}

function scheduleAskScrollToBottom(force = false) {
  const run = () => {
    askScrollRafId = 0;
    scrollAskAnswerToBottom(force);
    updateAskAutoFollowState();
    syncAskJumpLatestVisibility();
  };
  if (askScrollRafId) {
    window.cancelAnimationFrame(askScrollRafId);
  }
  askScrollRafId = window.requestAnimationFrame(() => {
    window.requestAnimationFrame(run);
  });
}

function syncAskJumpLatestVisibility() {
  const btn = $("#ask-jump-latest");
  if (!btn) return;
  const hidden = Boolean(state.ask.autoFollowAnswer);
  btn.style.visibility = hidden ? "hidden" : "visible";
  btn.style.pointerEvents = hidden ? "none" : "auto";
}

function updateAskSelectionState({ refreshUi = true, forceRender = false } = {}) {
  const answerEl = $("#ask-answer");
  if (!answerEl) return;
  const selection = window.getSelection();
  let text = "";
  if (selection && selection.rangeCount > 0 && !selection.isCollapsed) {
    const range = selection.getRangeAt(0);
    const node = range.commonAncestorContainer;
    if (answerEl.contains(node)) {
      text = selection.toString().trim();
    }
  }
  const normalized = String(text || "").replace(/\s+/g, " ").trim().slice(0, 900);
  if (!forceRender && state.ask.selectionText === normalized) return;
  state.ask.selectionText = normalized;
  if (refreshUi) {
    renderAskActions(state.ask.lastAction, state.ask.lastAnswer, state.ask.lastSources);
  }
}

function useAskSelectionAsFollowup() {
  const selected = String(state.ask.selectionText || "").trim();
  if (!selected) {
    setAskStatus("먼저 답변에서 텍스트를 선택하세요.");
    return;
  }
  const input = $("#ask-input");
  if (!input) return;
  const block = `선택된 맥락:\n"""\n${selected}\n"""\n\n이 선택 내용을 바탕으로 바로 이어서 설명해줘.`;
  const prev = String(input.value || "").trim();
  input.value = prev ? `${prev}\n\n${block}` : block;
  input.focus();
  input.setSelectionRange(input.value.length, input.value.length);
  setAskStatus("선택 내용을 질문 입력창에 추가했습니다.");
}

function useAskPromptAsFollowup(promptText) {
  const prompt = String(promptText || "").trim();
  if (!prompt) return;
  const input = $("#ask-input");
  if (!input) return;
  const prev = String(input.value || "").trim();
  input.value = prev ? `${prev}\n\n${prompt}` : prompt;
  input.focus();
  input.setSelectionRange(input.value.length, input.value.length);
  setAskStatus("보강 질문 템플릿을 입력창에 반영했습니다.");
}

function extractAskPathCandidates(answerText, sources = []) {
  const out = [];
  const seen = new Set();
  const addPath = (rawValue) => {
    const normalized = normalizeLogPathCandidate(rawValue);
    if (!normalized) return;
    if (seen.has(normalized)) return;
    seen.add(normalized);
    out.push(normalized);
  };
  if (Array.isArray(sources)) {
    sources.forEach((src) => {
      if (src && src.path) addPath(src.path);
    });
  }
  const text = String(answerText || "");
  const regex =
    /(?:\.\/)?(?:site\/runs\/[^\s`"'<>()]+|(?:report_notes|instruction|report|archive|output|supporting)\/[^\s`"'<>()]+)/gi;
  let match = regex.exec(text);
  while (match) {
    addPath(match[0]);
    if (out.length >= 8) break;
    match = regex.exec(text);
  }
  return out.slice(0, 8);
}

function buildAskActionButtons(action, answerText = "", sources = [], options = {}) {
  const actionObj = action && typeof action === "object" ? action : null;
  const includeSelection = options?.includeSelection !== false;
  const includeDerivedPaths = options?.includeDerivedPaths !== false;
  const buttons = [];
  const pushActionButton = (type, labelText, payloadAction = null) => {
    const actionType = normalizeAskActionType(type);
    if (!actionType) return;
    const payload = encodeAskActionPayload(actionType, payloadAction || actionObj || { type: actionType });
    const payloadAttr = payload ? ` data-ask-action-payload="${escapeHtml(payload)}"` : "";
    buttons.push(
      `<button type="button" class="ghost" data-ask-action="${escapeHtml(actionType)}"${payloadAttr}>${escapeHtml(labelText)}</button>`,
    );
  };
  const pathCandidates = includeDerivedPaths ? extractAskPathCandidates(answerText, sources) : [];
  if (actionObj?.type) {
    const label = String(actionObj.label || "").trim();
    const clarifyRequired = Boolean(actionObj.clarify_required);
    const clarifyQuestion = String(actionObj.clarify_question || "").trim();
    const rawRunHint = normalizeRunHint(actionObj.run_hint || actionObj.run_name_hint || "");
    const runHint = rawRunHint && !isInvalidRunHint(rawRunHint) ? rawRunHint : "";
    const resolvedRunFromHint = runHint ? resolveRunRelFromHint(runHint, { strict: true }) : "";
    const withRunLabel = (base) => (runHint ? `${base} · ${runHint}` : base);
    if (actionObj.type === "run_feather") {
      pushActionButton("run_feather", label || withRunLabel("Feather 실행"), actionObj);
    } else if (actionObj.type === "run_federlicht") {
      pushActionButton("run_federlicht", label || withRunLabel("Federlicht 실행"), actionObj);
    } else if (actionObj.type === "run_feather_then_federlicht") {
      pushActionButton(
        "run_feather_then_federlicht",
        label || withRunLabel("Feather → Federlicht 실행"),
        actionObj,
      );
      pushActionButton(
        "run_federlicht",
        "Federlicht만 실행",
        {
          ...actionObj,
          type: "run_federlicht",
          label: "",
        },
      );
    } else if (actionObj.type === "create_run_folder") {
      pushActionButton("create_run_folder", label || withRunLabel("새 Run Folder 생성"), actionObj);
    } else if (actionObj.type === "switch_run") {
      if (runHint) {
        const hint = runHint;
        const defaultLabel = hint ? `Run 전환: ${hint}` : "Run 전환";
        pushActionButton("switch_run", label || defaultLabel, actionObj);
      }
    } else if (actionObj.type === "preset_resume_stage") {
      const stage = String(actionObj.stage || "").trim().toLowerCase();
      const defaultLabel = stage ? `${workflowLabel(stage)}부터 재시작` : "재시작 단계 프리셋";
      pushActionButton("preset_resume_stage", label || defaultLabel, actionObj);
    } else if (actionObj.type === "focus_editor") {
      const target = String(actionObj.target || "").trim().toLowerCase();
      const defaultLabel = target === "feather_instruction" ? "Feather Instruction 열기" : "Inline Prompt 열기";
      pushActionButton("focus_editor", label || defaultLabel, actionObj);
    } else if (actionObj.type === "set_action_mode") {
      const mode = String(actionObj.mode || "").trim().toLowerCase();
      const defaultLabel = mode === "act" ? "Act 모드로 전환" : "Plan 모드로 전환";
      pushActionButton("set_action_mode", label || defaultLabel, actionObj);
    } else if (actionObj.type === "run_capability") {
      const capId = String(actionObj.capability_id || "").trim();
      if (capId) {
        const token = `capability:${capId}`;
        pushActionButton(token, label || `Capability 실행 (${capId})`, actionObj);
      }
    }
    if (resolvedRunFromHint) {
      const shortRun = stripSiteRunsPrefix(resolvedRunFromHint) || resolvedRunFromHint;
      buttons.push(
        `<button type="button" class="ghost" data-ask-open="${escapeHtml(resolvedRunFromHint)}" data-ask-open-kind="run">Run 열기: ${escapeHtml(shortRun)}</button>`,
      );
    }
    if (clarifyRequired && clarifyQuestion) {
      buttons.push(
        `<button type="button" class="ghost" data-ask-followup-prompt="${escapeHtml(clarifyQuestion)}">질의 보강하기</button>`,
      );
    }
  }
  if (includeSelection && state.ask.selectionText) {
    buttons.push(
      '<button type="button" class="ghost" data-ask-followup="selection">선택 내용으로 후속 질문</button>',
    );
  }
  if (includeDerivedPaths) {
    pathCandidates.slice(0, 5).forEach((path) => {
      const shortLabel = stripSiteRunsPrefix(path) || path;
      buttons.push(
        `<button type="button" class="ghost" data-ask-open="${escapeHtml(path)}">열기: ${escapeHtml(shortLabel)}</button>`,
      );
    });
  }
  return buttons;
}

function resolveRunRelFromPathCandidate(pathValue) {
  const normalized = normalizePathString(pathValue);
  if (!normalized) return "";
  const runRels = (Array.isArray(state.runs) ? state.runs : [])
    .map((item) => normalizePathString(item?.run_rel || ""))
    .filter(Boolean)
    .sort((a, b) => b.length - a.length);
  const stripped = stripSiteRunsPrefix(normalized);
  const candidates = [normalized, stripped].filter(Boolean);
  for (const candidate of candidates) {
    const hit = runRels.find((runRel) => candidate === runRel || candidate.startsWith(`${runRel}/`));
    if (hit) return hit;
  }
  const strippedHead = stripped.includes("/") ? stripped.split("/")[0] : stripped;
  const normalizedHead = normalized.includes("/") ? normalized.split("/")[0] : normalized;
  const hintCandidates = [normalized, stripped, strippedHead, normalizedHead].filter(Boolean);
  for (const hint of hintCandidates) {
    const resolved = resolveRunRelFromHint(hint, { strict: true });
    if (resolved) return normalizePathString(resolved);
  }
  return "";
}

function bindAskActionButtons(container) {
  if (!container) return;
  container.querySelectorAll("[data-ask-followup]").forEach((btn) => {
    btn.addEventListener("click", () => {
      useAskSelectionAsFollowup();
    });
  });
  container.querySelectorAll("[data-ask-followup-prompt]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const prompt = btn.getAttribute("data-ask-followup-prompt") || "";
      useAskPromptAsFollowup(prompt);
    });
  });
  container.querySelectorAll("[data-ask-open]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const rawPath = btn.getAttribute("data-ask-open") || "";
      const path = normalizePathString(rawPath);
      if (!path) return;
      const openKind = String(btn.getAttribute("data-ask-open-kind") || "").trim().toLowerCase();
      const looksLikeFile = isLikelyPreviewFilePath(path);
      try {
        if (openKind === "run" || !looksLikeFile) {
          const runRel = resolveRunRelFromPathCandidate(path);
          if (!runRel) {
            setAskStatus(`열기 실패: run을 찾지 못했습니다 (${path})`);
            appendLog(`[ask-action] open failed: unresolved run path=${path}\n`);
            return;
          }
          await applyRunSelection(runRel);
          appendLog(`[ask-action] opened run: ${runRel}\n`);
          const label = stripSiteRunsPrefix(runRel) || runRel;
          setAskStatus(`Run 열기 완료: ${label}`);
          return;
        }
        await loadFilePreview(path, { readOnly: true });
        appendLog(`[ask-action] opened: ${path}\n`);
      } catch (err) {
        appendLog(`[ask-action] open failed: ${err}\n`);
        setAskStatus(`열기 실패: ${err}`);
      }
    });
  });
  container.querySelectorAll("[data-ask-action]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const type = btn.getAttribute("data-ask-action") || "";
      if (!type) return;
      const rawPayload = btn.getAttribute("data-ask-action-payload") || "";
      const actionOverride = decodeAskActionPayload(rawPayload, type);
      await runAskSuggestedAction(type, { actionOverride });
    });
  });
}

function renderAskSourcesTrace() {
  const toggleBtn = $("#ask-trace-toggle");
  if (toggleBtn) {
    toggleBtn.textContent = state.ask.traceShowHistory ? "현재 보기" : "이력 보기";
  }
  const traceHost = $("#ask-sources-trace");
  const capHost = $("#ask-sources-cap-grid");
  if (!capHost || !traceHost) return;
  let historyHost = $("#ask-trace-history");
  if (!historyHost) {
    historyHost = document.createElement("div");
    historyHost.id = "ask-trace-history";
    historyHost.className = "ask-trace-history";
    traceHost.appendChild(historyHost);
  }
  const entries = askCapabilityEntries();
  const activeTokens = new Set(["running", "done", "error", "skipped"]);
  const timeline = Array.isArray(state.ask.activityTimeline) ? state.ask.activityTimeline : [];
  const latestEventById = new Map();
  timeline.forEach((event, idx) => {
    const eventId = String(event?.id || "").trim().toLowerCase();
    if (!eventId) return;
    latestEventById.set(eventId, {
      index: idx,
      message: String(event?.message || "").trim(),
      at: String(event?.at || ""),
      status: String(event?.status || "").trim().toLowerCase(),
      trace_id: String(event?.trace_id || "").trim(),
      tool_id: String(event?.tool_id || "").trim(),
      duration_ms: Number(event?.duration_ms),
      token_est: Number(event?.token_est),
      cache_hit: Object.prototype.hasOwnProperty.call(event || {}, "cache_hit")
        ? Boolean(event?.cache_hit)
        : null,
    });
  });
  const statusOrder = { running: 0, error: 1, done: 2, skipped: 3 };
  const activeEntries = entries
    .map((entry) => {
      const status = String(state.ask.activity?.[entry.id] || (entry.enabled === false ? "disabled" : "idle"));
      const event = latestEventById.get(String(entry.id || "").trim().toLowerCase()) || null;
      return { entry, status, event };
    })
    .filter((item) => activeTokens.has(item.status))
    .sort((left, right) => {
      const leftRank = Number.isFinite(statusOrder[left.status]) ? statusOrder[left.status] : 9;
      const rightRank = Number.isFinite(statusOrder[right.status]) ? statusOrder[right.status] : 9;
      if (leftRank !== rightRank) return leftRank - rightRank;
      const leftIdx = Number(left.event?.index ?? -1);
      const rightIdx = Number(right.event?.index ?? -1);
      return rightIdx - leftIdx;
    });
  if (state.ask.traceShowHistory) {
    capHost.style.display = "none";
    const historyItems = timeline.slice(-48);
    historyHost.innerHTML = historyItems.length
      ? historyItems
        .map((event) => {
          const at = event.at ? formatDate(event.at) : "-";
          const status = String(event.status || "idle").toLowerCase();
          const label = String(event.id || "tool");
          const message = String(event.message || "").trim();
          const metaText = askTraceMetaText(event);
          const statusLabel = status === "running"
            ? "진행중"
            : status === "done"
              ? "완료"
              : status === "error"
                ? "오류"
                : status === "skipped"
                  ? "건너뜀"
                  : status;
          return `
            <div class="ask-trace-step-row">
              <article class="ask-trace-entry is-${escapeHtml(status || "idle")}">
                <strong>${escapeHtml(label)}</strong>
                <span class="ask-trace-state">${escapeHtml(statusLabel)}</span>
                ${message ? `<span class="ask-trace-note">${escapeHtml(message)}</span>` : ""}
                ${metaText ? `<span class="ask-trace-meta">${escapeHtml(metaText)}</span>` : ""}
                <span class="ask-trace-time">${escapeHtml(at)}</span>
              </article>
            </div>
          `;
        })
        .join("")
      : '<p class="muted">기록된 실행 이력이 없습니다.</p>';
    historyHost.scrollTop = historyHost.scrollHeight;
    return;
  }
  historyHost.innerHTML = "";
  capHost.style.display = "";
  capHost.innerHTML = activeEntries.length
    ? activeEntries
      .map((item, idx) => {
        const status = String(item.status || "idle").toLowerCase();
        const statusLabel = status === "running"
          ? "진행중"
          : status === "done"
            ? "완료"
            : status === "error"
              ? "오류"
              : status === "skipped"
                ? "건너뜀"
                : status;
        const titleParts = [];
        if (item.entry.group) titleParts.push(String(item.entry.group || "").toUpperCase());
        if (item.entry.description) titleParts.push(String(item.entry.description || ""));
        if (item.event?.message) titleParts.push(String(item.event.message || ""));
        const metaText = askTraceMetaText(item.event || {});
        if (metaText) titleParts.push(metaText);
        const title = titleParts.join(" · ");
        return `
          <div class="ask-trace-step-row">
            ${idx ? '<span class="ask-trace-arrow" aria-hidden="true">↳</span>' : ""}
            <article class="ask-trace-live-entry is-${escapeHtml(status)}" title="${escapeHtml(title)}">
              <span class="ask-trace-live-label">${escapeHtml(item.entry.label)}</span>
              <span class="ask-trace-live-status">${escapeHtml(statusLabel)}</span>
              ${item.event?.message ? `<span class="ask-trace-live-note">${escapeHtml(item.event.message)}</span>` : ""}
              ${metaText ? `<span class="ask-trace-meta">${escapeHtml(metaText)}</span>` : ""}
            </article>
          </div>
        `;
      })
      .join("")
    : '<span class="muted">현재 활성 도구 없음</span>';
}

function isRunTargetActionType(actionType) {
  return ASK_RUN_TARGET_ACTION_TYPES.has(normalizeAskActionType(actionType));
}

function isInstructionConfirmActionType(actionType) {
  return ASK_INSTRUCTION_CONFIRM_ACTION_TYPES.has(normalizeAskActionType(actionType));
}

function actionRequiresInstructionConfirm(actionType, actionOverride = null) {
  const type = normalizeAskActionType(actionType);
  if (!isInstructionConfirmActionType(type)) return false;
  const action = resolveAskActionContext(type, actionOverride);
  return Boolean(action?.require_instruction_confirm);
}

function actionInstructionConfirmReason(actionType, actionOverride = null) {
  const type = normalizeAskActionType(actionType);
  if (!isInstructionConfirmActionType(type)) return "";
  const action = resolveAskActionContext(type, actionOverride);
  return String(action?.instruction_confirm_reason || "").trim().toLowerCase();
}

function isAskActionInstructionConfirmRequired() {
  const box = $("#ask-action-instruction-confirm-box");
  return box?.dataset?.required === "1";
}

function isAskActionInstructionConfirmChecked() {
  if (!isAskActionInstructionConfirmRequired()) return true;
  return Boolean($("#ask-action-instruction-confirm")?.checked);
}

function syncAskActionRunTargetOptions() {
  const listEl = $("#ask-action-run-target-options");
  if (!listEl) return;
  const runs = Array.isArray(state.runs) ? state.runs : [];
  const values = runs
    .map((item) => stripSiteRunsPrefix(normalizePathString(item?.run_rel || "")) || "")
    .filter(Boolean);
  const deduped = Array.from(new Set(values)).sort((a, b) => a.localeCompare(b));
  listEl.innerHTML = deduped
    .map((value) => `<option value="${escapeHtml(value)}"></option>`)
    .join("");
}

function setAskActionRunTargetVisualState(stateToken = "default") {
  const box = $("#ask-action-run-target-box");
  if (!box) return;
  box.classList.remove("is-valid", "is-warning", "is-error");
  if (stateToken === "valid") {
    box.classList.add("is-valid");
  } else if (stateToken === "warning") {
    box.classList.add("is-warning");
  } else if (stateToken === "error") {
    box.classList.add("is-error");
  }
}

function setAskActionConfirmEnabled(enabled) {
  const confirmBtn = $("#ask-action-confirm");
  if (!confirmBtn) return;
  confirmBtn.disabled = !enabled;
}

function resetAskActionInstructionConfirmUi() {
  const box = $("#ask-action-instruction-confirm-box");
  const context = $("#ask-action-instruction-confirm-context");
  const check = $("#ask-action-instruction-confirm");
  const label = $("#ask-action-instruction-confirm-label");
  const note = $("#ask-action-instruction-confirm-note");
  if (!box) return;
  box.classList.add("is-hidden");
  box.setAttribute("aria-hidden", "true");
  box.dataset.required = "";
  box.dataset.reason = "";
  if (context) {
    context.textContent = "";
  }
  if (check) {
    check.checked = false;
  }
  if (label) {
    label.textContent = "Instruction 초안을 확인했습니다.";
  }
  if (note) {
    note.textContent = "";
  }
}

function resetAskActionRunTargetConfirmUi() {
  const box = $("#ask-action-run-target-box");
  const confirmWrap = $("#ask-action-run-target-confirm-wrap");
  const confirmCheck = $("#ask-action-run-target-confirm");
  const confirmLabel = $("#ask-action-run-target-confirm-label");
  if (box) {
    box.dataset.requireRunConfirm = "";
  }
  if (confirmWrap) {
    confirmWrap.classList.remove("is-required");
    confirmWrap.classList.add("is-hidden");
  }
  if (confirmCheck) {
    confirmCheck.checked = false;
  }
  if (confirmLabel) {
    confirmLabel.textContent = "실행 대상을 확인했습니다.";
  }
}

function showAskActionInstructionConfirmBox(plan) {
  const box = $("#ask-action-instruction-confirm-box");
  const context = $("#ask-action-instruction-confirm-context");
  const check = $("#ask-action-instruction-confirm");
  const label = $("#ask-action-instruction-confirm-label");
  if (!box || !check || !label) return;
  const type = normalizeAskActionType(plan?.type || "");
  const override = normalizeAskActionOverride(type, plan?.actionOverride);
  const required = actionRequiresInstructionConfirm(type, override);
  if (!required) {
    resetAskActionInstructionConfirmUi();
    return;
  }
  const reason = actionInstructionConfirmReason(type, override);
  const reasonLabel = reason === "short_generic_request"
    ? "질문이 짧거나 모호해 instruction 보정이 필요합니다."
    : "FederHav가 instruction 자동 보정이 필요하다고 판단했습니다.";
  box.classList.remove("is-hidden");
  box.setAttribute("aria-hidden", "false");
  box.dataset.required = "1";
  box.dataset.reason = reason;
  if (check) {
    check.checked = false;
  }
  label.textContent = "Instruction 초안 확인 후 실행합니다.";
  if (context) {
    context.textContent = reasonLabel;
  }
}

function updateAskActionInstructionConfirmNote() {
  const note = $("#ask-action-instruction-confirm-note");
  if (!note) return;
  if (!isAskActionInstructionConfirmRequired()) {
    note.textContent = "";
    return;
  }
  note.textContent = isAskActionInstructionConfirmChecked()
    ? "Instruction 확인 완료."
    : "Instruction 확인 체크를 완료해야 실행할 수 있습니다.";
}

function showAskActionRunTargetBox(plan) {
  const box = $("#ask-action-run-target-box");
  const input = $("#ask-action-run-target");
  const createWrap = $("#ask-action-run-create-wrap");
  const createCheck = $("#ask-action-run-create");
  const contextNote = $("#ask-action-run-target-context");
  const useSuggestedBtn = $("#ask-action-use-suggested-run");
  const confirmWrap = $("#ask-action-run-target-confirm-wrap");
  const confirmCheck = $("#ask-action-run-target-confirm");
  const confirmLabel = $("#ask-action-run-target-confirm-label");
  if (!box || !input || !createWrap || !createCheck) return;
  syncAskActionRunTargetOptions();
  const type = normalizeAskActionType(plan?.type || "");
  const enabled = isRunTargetActionType(type);
  box.classList.toggle("is-hidden", !enabled);
  box.setAttribute("aria-hidden", enabled ? "false" : "true");
  if (!enabled) {
    setAskActionRunTargetVisualState("default");
    setAskActionConfirmEnabled(true);
    input.value = "";
    createCheck.checked = false;
    box.dataset.suggestedRun = "";
    box.dataset.requireRunConfirm = "";
    if (contextNote) contextNote.textContent = "";
    if (useSuggestedBtn) useSuggestedBtn.classList.add("is-hidden");
    resetAskActionRunTargetConfirmUi();
    return;
  }
  const override = normalizeAskActionOverride(type, plan?.actionOverride);
  const context = resolveAskActionContext(type, override);
  const preflight = context?.execution_handoff?.preflight
    && typeof context.execution_handoff.preflight === "object"
    ? context.execution_handoff.preflight
    : null;
  const preflightResolvedRun = normalizePathString(preflight?.resolved_run_rel || "");
  const preflightStatus = String(preflight?.status || "").trim().toLowerCase();
  const fallbackRun = stripSiteRunsPrefix(normalizePathString(selectedRunRel() || "")) || "";
  const suggestedRun = normalizeRunHint(
    override?.run_hint
    || context?.run_hint
    || "",
  );
  const preflightRunHint = normalizeRunHint(preflight?.run_hint || preflightResolvedRun || "");
  const hinted = normalizeRunHint(
    suggestedRun || preflightRunHint || (type === "switch_run" ? fallbackRun : ""),
  );
  input.value = hinted || fallbackRun || "";
  box.dataset.suggestedRun = suggestedRun;
  const requireExplicitConfirm = type === "switch_run" || Boolean(suggestedRun);
  box.dataset.requireRunConfirm = requireExplicitConfirm ? "1" : "";
  if (confirmWrap) {
    confirmWrap.classList.remove("is-hidden");
    confirmWrap.classList.toggle("is-required", requireExplicitConfirm);
  }
  if (confirmCheck) {
    confirmCheck.checked = !requireExplicitConfirm;
  }
  if (confirmLabel) {
    confirmLabel.textContent = requireExplicitConfirm
      ? "요청 대상 run을 확인 후 실행합니다."
      : "현재 선택 run 기준으로 바로 실행합니다.";
  }
  if (useSuggestedBtn) {
    useSuggestedBtn.classList.toggle("is-hidden", !suggestedRun);
  }
  if (contextNote) {
    const selectedLabel = fallbackRun || "-";
    if (suggestedRun) {
      contextNote.textContent = `FederHav 제안 run: ${suggestedRun} · 현재 선택 run: ${selectedLabel}`;
    } else if (preflightResolvedRun) {
      const resolvedLabel = stripSiteRunsPrefix(preflightResolvedRun) || preflightResolvedRun;
      const statusLabel = preflightStatus ? ` (${preflightStatus})` : "";
      contextNote.textContent = `Planner preflight run: ${resolvedLabel}${statusLabel} · 현재 선택 run: ${selectedLabel}`;
    } else {
      contextNote.textContent = `현재 선택 run: ${selectedLabel}`;
    }
  }
  const createIfMissing = Object.prototype.hasOwnProperty.call(override || {}, "create_if_missing")
    ? Boolean(override?.create_if_missing)
    : Boolean(context?.create_if_missing);
  createCheck.checked = createIfMissing;
}

function updateAskActionRunTargetNote() {
  const box = $("#ask-action-run-target-box");
  const note = $("#ask-action-run-target-note");
  const input = $("#ask-action-run-target");
  const createCheck = $("#ask-action-run-create");
  const confirmWrap = $("#ask-action-run-target-confirm-wrap");
  const confirmCheck = $("#ask-action-run-target-confirm");
  const pending = state.ask.pendingAction;
  if (!box || !note || !input || !createCheck || !pending) return;
  const requiresConfirm = box.dataset.requireRunConfirm === "1";
  if (confirmWrap) {
    confirmWrap.classList.toggle("is-required", requiresConfirm);
  }
  const type = normalizeAskActionType(pending?.type || "");
  if (!isRunTargetActionType(type)) {
    setAskActionRunTargetVisualState("default");
    setAskActionConfirmEnabled(true);
    note.textContent = "";
    return;
  }
  const hinted = normalizeRunHint(input.value || "");
  if (!hinted && type === "switch_run") {
    setAskActionRunTargetVisualState("error");
    setAskActionConfirmEnabled(false);
    note.textContent = "Run 전환은 대상 run 이름/경로가 필요합니다.";
    return;
  }
  const hintAnalysis = hinted ? analyzeRunRelHint(hinted, { strict: true }) : null;
  const resolved = hintAnalysis?.resolved || "";
  const selected = normalizePathString(selectedRunRel() || "");
  const selectedLabel = selected ? (stripSiteRunsPrefix(selected) || selected) : "-";
  let canProceed = true;
  let stateToken = "valid";
  let noteText = "";
  if (hintAnalysis?.ambiguous) {
    const candidates = Array.isArray(hintAnalysis.candidates) ? hintAnalysis.candidates.slice(0, 4) : [];
    const labels = candidates
      .map((item) => stripSiteRunsPrefix(normalizePathString(item)) || normalizePathString(item))
      .filter(Boolean);
    const suffix = (hintAnalysis.candidates?.length || 0) > labels.length
      ? ` 외 ${(hintAnalysis.candidates?.length || 0) - labels.length}개`
      : "";
    canProceed = false;
    stateToken = "error";
    noteText = labels.length
      ? `여러 run 후보가 일치합니다: ${labels.join(", ")}${suffix}. 정확한 run 이름/경로를 입력하세요.`
      : "여러 run 후보가 일치합니다. 정확한 run 이름/경로를 입력하세요.";
  } else if (resolved) {
    const resolvedLabel = stripSiteRunsPrefix(resolved) || resolved;
    stateToken = "valid";
    const byHint = hinted && hinted !== resolvedLabel
      ? ` · 입력 힌트: ${hinted}`
      : "";
    noteText = `확정 대상: ${resolvedLabel}${resolved === selected ? " (현재 선택 run)" : ""}${byHint}`;
  } else if (createCheck.checked && hinted) {
    const sanitized = sanitizeRunNameHint(hinted);
    stateToken = "warning";
    noteText = `현재 일치 run 없음 · 실행 시 "${sanitized || hinted}" run을 생성 후 진행합니다.`;
  } else if (hinted) {
    canProceed = false;
    stateToken = "error";
    noteText = `일치 run 없음 · 생성 옵션을 켜거나 run 힌트를 수정하세요. (현재 run: ${selectedLabel})`;
  } else {
    stateToken = "valid";
    noteText = `현재 선택 run 기준으로 실행됩니다: ${selectedLabel}`;
  }
  if (requiresConfirm && canProceed && !(confirmCheck?.checked)) {
    canProceed = false;
    noteText = `${noteText} · 실행 전 대상 확인 체크를 완료하세요.`;
  }
  if (canProceed && !isAskActionInstructionConfirmChecked()) {
    canProceed = false;
    noteText = noteText
      ? `${noteText} · instruction 확인 체크를 완료하세요.`
      : "Instruction 확인 체크를 완료하세요.";
  }
  setAskActionRunTargetVisualState(stateToken);
  setAskActionConfirmEnabled(canProceed);
  note.textContent = noteText;
}

function collectAskActionRunTargetOverride() {
  const pending = state.ask.pendingAction || null;
  const type = normalizeAskActionType(pending?.type || "");
  const baseOverride = normalizeAskActionOverride(type, pending?.actionOverride);
  if (!isRunTargetActionType(type)) return baseOverride;
  const base = {
    ...(resolveAskActionContext(type, baseOverride) || {}),
    ...(baseOverride || {}),
    type,
  };
  const input = $("#ask-action-run-target");
  const createCheck = $("#ask-action-run-create");
  const rawHint = normalizeRunHint(input?.value || "");
  const resolvedFromHint = rawHint ? resolveRunRelFromHint(rawHint, { strict: true }) : "";
  const shouldCreate = Boolean(createCheck?.checked);
  const hinted = (!resolvedFromHint && shouldCreate) ? sanitizeRunNameHint(rawHint) : rawHint;
  if (input && hinted && input.value !== hinted && shouldCreate && !resolvedFromHint) {
    input.value = hinted;
  }
  if (hinted) {
    const resolved = resolveRunRelFromHint(hinted, { strict: true });
    base.run_hint = stripSiteRunsPrefix(resolved) || resolved || hinted;
  } else {
    delete base.run_hint;
  }
  if (createCheck) {
    base.create_if_missing = Boolean(createCheck.checked);
  }
  return normalizeAskActionOverride(type, base);
}

function openAskActionModal(plan) {
  const modal = $("#ask-action-modal");
  if (!modal) return;
  const titleEl = $("#ask-action-title");
  const metaEl = $("#ask-action-meta");
  const previewEl = $("#ask-action-preview");
  const confirmBtn = $("#ask-action-confirm");
  state.ask.pendingAction = plan || null;
  if (titleEl) titleEl.textContent = plan?.title || "Action Preview";
  if (metaEl) metaEl.textContent = plan?.meta || "실행 전에 파라미터를 확인하세요.";
  if (previewEl) previewEl.textContent = String(plan?.preview || "No preview.");
  showAskActionInstructionConfirmBox(plan || {});
  showAskActionRunTargetBox(plan || {});
  updateAskActionInstructionConfirmNote();
  updateAskActionRunTargetNote();
  if (confirmBtn) {
    const type = normalizeAskActionType(plan?.type || "");
    const override = normalizeAskActionOverride(type, plan?.actionOverride);
    const needsInstructionConfirm = actionRequiresInstructionConfirm(type, override);
    confirmBtn.textContent = needsInstructionConfirm
      ? "Instruction 확인 후 실행"
      : (isRunTargetActionType(type) ? "Run 대상 확정 후 실행" : "확인 후 실행");
    if (isRunTargetActionType(type)) {
      window.setTimeout(() => {
        $("#ask-action-run-target")?.focus();
      }, 0);
    }
  }
  openOverlayModal("ask-action-modal");
}

function closeAskActionModal() {
  const modal = $("#ask-action-modal");
  if (!modal) return;
  closeOverlayModal("ask-action-modal");
  const box = $("#ask-action-run-target-box");
  const note = $("#ask-action-run-target-note");
  const contextNote = $("#ask-action-run-target-context");
  const input = $("#ask-action-run-target");
  const createCheck = $("#ask-action-run-create");
  const options = $("#ask-action-run-target-options");
  const useSuggestedBtn = $("#ask-action-use-suggested-run");
  const confirmCheck = $("#ask-action-run-target-confirm");
  if (box) {
    box.classList.add("is-hidden");
    box.setAttribute("aria-hidden", "true");
    box.dataset.suggestedRun = "";
    box.dataset.requireRunConfirm = "";
  }
  setAskActionRunTargetVisualState("default");
  setAskActionConfirmEnabled(true);
  if (note) note.textContent = "";
  if (contextNote) contextNote.textContent = "";
  if (input) input.value = "";
  if (createCheck) createCheck.checked = false;
  if (confirmCheck) confirmCheck.checked = false;
  if (options) options.innerHTML = "";
  if (useSuggestedBtn) useSuggestedBtn.classList.add("is-hidden");
  resetAskActionRunTargetConfirmUi();
  resetAskActionInstructionConfirmUi();
  state.ask.pendingAction = null;
}

function isAskActionModalOpen() {
  return isOverlayModalOpen("ask-action-modal");
}

function renderAskActions(action, answerText = "", sources = []) {
  state.ask.lastAction = action && typeof action === "object" ? action : null;
  if (answerText && !state.ask.busy) {
    state.ask.lastAnswer = String(answerText || "");
  }
  if (!state.ask.busy && Array.isArray(sources)) {
    state.ask.lastSources = normalizeAskSourceList(sources);
  }
  renderAskSourcesTrace();
  renderAskAnswer(state.ask.liveAnswer || "");
}

function latestAskActionForType(actionType) {
  const type = String(actionType || "").trim().toLowerCase();
  if (!type) return null;
  const askAction = state.ask.lastAction && typeof state.ask.lastAction === "object"
    ? state.ask.lastAction
    : null;
  if (askAction && String(askAction.type || "").trim().toLowerCase() === type) {
    return askAction;
  }
  const liveAction = state.liveAsk.lastAction && typeof state.liveAsk.lastAction === "object"
    ? state.liveAsk.lastAction
    : null;
  if (liveAction && String(liveAction.type || "").trim().toLowerCase() === type) {
    return liveAction;
  }
  return null;
}

function normalizeAskActionOverride(actionType, actionOverride) {
  if (!actionOverride || typeof actionOverride !== "object") return null;
  const expectedType = normalizeAskActionType(actionType);
  const resolvedType = normalizeAskActionType(actionOverride.type || actionType);
  if (!resolvedType) return null;
  if (expectedType && resolvedType !== expectedType) return null;
  return {
    ...actionOverride,
    type: resolvedType,
  };
}

function resolveAskActionContext(actionType, actionOverride = null) {
  const override = normalizeAskActionOverride(actionType, actionOverride);
  if (override) return override;
  return latestAskActionForType(actionType);
}

function encodeAskActionPayload(actionType, actionObj) {
  const normalized = normalizeAskActionOverride(actionType, actionObj);
  if (!normalized) return "";
  try {
    return encodeURIComponent(JSON.stringify(normalized));
  } catch (err) {
    return "";
  }
}

function decodeAskActionPayload(rawPayload, actionType) {
  const raw = String(rawPayload || "").trim();
  if (!raw) return null;
  try {
    const parsed = JSON.parse(decodeURIComponent(raw));
    return normalizeAskActionOverride(actionType, parsed);
  } catch (err) {
    return null;
  }
}

function isGenericExecutionPrompt(value) {
  const raw = String(value || "").trim();
  if (!raw) return false;
  const compact = raw
    .toLowerCase()
    .replace(/[`"'“”‘’]/g, "")
    .replace(/[.!?~…]/g, "")
    .replace(/\s+/g, " ")
    .trim();
  if (!compact) return false;
  const direct = new Set([
    "run",
    "start",
    "go",
    "retry",
    "execute",
    "실행",
    "실행해줘",
    "실행 해줘",
    "실행해주세요",
    "실행 해주세요",
    "시작",
    "시작해줘",
    "시작 해줘",
    "시작해주세요",
    "해줘",
    "해 줘",
    "해주세요",
    "해 주세요",
    "다시 실행",
    "다시 실행해줘",
    "돌려줘",
    "진행해줘",
  ]);
  if (direct.has(compact)) return true;
  if (compact.length <= 18 && /^(run|start|execute|retry|go)\b/.test(compact)) return true;
  if (compact.length <= 18 && /^(실행|시작|돌려|진행)(해줘|해주세요)?$/.test(compact)) return true;
  return false;
}

function latestAskFallbackQuery(options = {}) {
  const skipGeneric = options?.skipGeneric !== false;
  const cap = Math.max(120, Number.parseInt(String(options?.maxChars || 1200), 10) || 1200);
  const candidates = [];
  const pending = String(state.liveAsk.pendingQuestion || state.ask.pendingQuestion || "").trim();
  if (pending) candidates.push(pending);
  const pushHistoryCandidates = (rows) => {
    if (!Array.isArray(rows)) return;
    [...rows]
      .reverse()
      .forEach((entry) => {
        if (entry?.role !== "user") return;
        const text = String(entry?.content || "").trim();
        if (!text) return;
        candidates.push(text);
      });
  };
  pushHistoryCandidates(state.liveAsk.history);
  pushHistoryCandidates(state.ask.history);
  const deduped = [];
  const seen = new Set();
  candidates.forEach((item) => {
    const key = item.replace(/\s+/g, " ").trim();
    if (!key || seen.has(key)) return;
    seen.add(key);
    deduped.push(key);
  });
  const meaningful = deduped.find((item) => !isGenericExecutionPrompt(item));
  if (meaningful) return meaningful.slice(0, cap);
  if (skipGeneric) return "";
  const fallback = deduped[0] || "";
  return fallback.slice(0, cap);
}

function sanitizeRunNameHint(rawValue) {
  let token = normalizeRunHint(rawValue);
  if (!token) return "";
  const base = token.split("/").filter(Boolean).pop() || token;
  return String(base || "")
    .replace(/[<>:"/\\|?*\x00-\x1f]/g, " ")
    .replace(/\s+/g, "_")
    .replace(/_+/g, "_")
    .replace(/^[_\-.]+|[_\-.]+$/g, "")
    .slice(0, 96);
}

function syncFeatherRunTargetFields(runRel) {
  const normalized = normalizePathString(runRel || "");
  if (!normalized) return;
  const runName = runBaseName(normalized);
  const runNameInput = $("#feather-run-name");
  const outputInput = $("#feather-output");
  const instructionInput = $("#feather-input");
  if (runNameInput) runNameInput.value = runName;
  if (outputInput) {
    outputInput.value = normalized;
    featherOutputTouched = false;
  }
  if (instructionInput && !featherInputTouched) {
    instructionInput.value = `${normalized}/instruction/${runName}.txt`;
  }
  syncFeatherOutputHint();
}

async function applyRunSelection(runRel) {
  const normalized = normalizePathString(runRel || "");
  if (!normalized) return "";
  if ($("#run-select")) $("#run-select").value = normalized;
  if ($("#prompt-run-select")) $("#prompt-run-select").value = normalized;
  if ($("#instruction-run-select")) $("#instruction-run-select").value = normalized;
  refreshRunDependentFields();
  // Keep Live Ask context label in sync immediately after run switch actions.
  renderAskHistory();
  await updateRunStudio(normalized).catch(() => {});
  return normalized;
}

async function resolveActionRunTarget(actionType, options = {}) {
  const action = resolveAskActionContext(actionType, options?.actionOverride);
  const runHint = normalizeRunHint(action?.run_hint || "");
  if (!runHint) {
    return {
      runHint: "",
      runRel: normalizePathString(selectedRunRel() || ""),
      created: false,
    };
  }
  const allowCreate = options.createIfMissing ?? Boolean(action?.create_if_missing);
  const strictResolve = options?.strict !== false;
  let runRel = resolveRunRelFromHint(runHint, { strict: strictResolve });
  let created = false;
  if (!runRel && allowCreate) {
    const runName = sanitizeRunNameHint(runHint);
    if (runName) {
      const createdRun = await fetchJSON("/api/runs/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          run_name: runName,
          topic: runName,
        }),
      });
      runRel = normalizePathString(createdRun?.run_rel || "");
      created = Boolean(runRel);
      if (created) {
        await loadRuns().catch(() => {});
      }
    }
  }
  if (runRel) {
    await applyRunSelection(runRel);
  }
  return {
    runHint,
    runRel: normalizePathString(runRel || ""),
    created,
  };
}

function normalizeAskActionType(actionType) {
  return String(actionType || "").trim().toLowerCase();
}

function shouldGuardExecutionModeAdvice(answerText, result) {
  const answer = String(answerText || "");
  if (!answer.trim()) return false;
  const issueContext = [
    String(result?.error || ""),
    String(result?.web_search_note || ""),
    answer,
  ].join("\n");
  if (!/(reasoning(?:[._\s-]?effort)?|badrequest|unauthorized|forbidden|access denied|does not exist|deployment|model)/i.test(issueContext)) {
    return false;
  }
  return /(execution_mode|\/plan|\/act|plan.*act|act.*plan)/i.test(answer);
}

function enforceExecutionModeAdviceGuard(answerText, result) {
  const answer = String(answerText || "");
  if (!shouldGuardExecutionModeAdvice(answer, result)) return answer;
  if (/제안 액션에만 적용|sidebar.*run/i.test(answer)) return answer;
  return `${answer}\n\n참고: Plan/Act(execution_mode)는 FederHav 제안 액션 실행 정책만 제어하며, 사이드바 Run Feather/Run Federlicht 오류 해결 수단은 아닙니다. 모델/백엔드/reasoning 설정을 먼저 조정하세요.`;
}

function isAskWriteActionType(actionType) {
  return ASK_WRITE_ACTION_TYPES.has(normalizeAskActionType(actionType));
}

function isAskPlanInstantActionType(actionType) {
  return ASK_PLAN_INSTANT_ACTION_TYPES.has(normalizeAskActionType(actionType));
}

function hasExplicitExecutionIntent(text) {
  const raw = String(text || "").trim().toLowerCase();
  if (!raw) return false;
  const compact = raw.replace(/\s+/g, "");
  const directTokens = [
    "작업하자",
    "실행하자",
    "진행하자",
    "바로실행",
    "지금실행",
    "실행해",
    "실행해줘",
    "진행해",
    "진행해줘",
    "돌려줘",
    "run it",
    "run now",
    "execute",
    "go ahead",
  ];
  if (directTokens.some((token) => compact.includes(token.replace(/\s+/g, "")))) {
    return true;
  }
  const hasRunVerb = /(실행|진행|돌려|run|execute|start)/i.test(raw);
  const hasExplainVerb = /(설명|차이|이유|왜|방법|가이드|how|what|difference)/i.test(raw);
  return hasRunVerb && !hasExplainVerb;
}

function isAskExecutableActionType(actionType) {
  const type = normalizeAskActionType(actionType);
  if (!type) return false;
  if (type.startsWith("capability:")) return true;
  if (isAskWriteActionType(type)) return true;
  if (isRunTargetActionType(type)) return true;
  if (isAskPlanInstantActionType(type)) return true;
  return type === "set_action_mode";
}

function latestExecutableLiveAskAction() {
  const seen = new Set();
  const candidates = [];
  const pushCandidate = (action) => {
    const normalized = normalizeLiveAskAction(action);
    if (!normalized) return;
    const actionType = normalizeAskActionType(normalized.type);
    if (!isAskExecutableActionType(actionType)) return;
    const key = `${actionType}|${String(normalized.run_hint || "").trim().toLowerCase()}`;
    if (seen.has(key)) return;
    seen.add(key);
    candidates.push(normalized);
  };
  pushCandidate(state.liveAsk.lastAction);
  pushCandidate(state.ask.lastAction);
  const pending = state.ask.pendingAction;
  if (pending && typeof pending === "object") {
    pushCandidate(normalizeAskActionOverride(pending.type || "", pending.actionOverride || pending));
  }
  const history = Array.isArray(state.liveAsk.history) ? state.liveAsk.history : [];
  for (let idx = history.length - 1; idx >= 0 && candidates.length < 8; idx -= 1) {
    const row = history[idx];
    if (!row || row.role !== "assistant") continue;
    pushCandidate(row.action);
  }
  const preferred = candidates.find((action) => {
    const type = normalizeAskActionType(action?.type || "");
    return type.startsWith("capability:") || isAskWriteActionType(type) || isRunTargetActionType(type);
  });
  return preferred || candidates[0] || null;
}

async function tryRunExplicitExecutionShortcut(question) {
  if (!hasExplicitExecutionIntent(question)) return false;
  const action = latestExecutableLiveAskAction();
  if (!action) return false;
  const actionType = normalizeAskActionType(action.type);
  if (!actionType) return false;
  const needsInstructionConfirm = actionRequiresInstructionConfirm(actionType, action);
  const instructionReason = actionInstructionConfirmReason(actionType, action);
  const canBypassInstructionConfirm =
    needsInstructionConfirm
    && instructionReason === "short_generic_request";
  appendLog(`[run-agent:action] shortcut-execute=${actionType} (explicit_execute_intent)\n`);
  appendLiveAskSystemEntry(
    `[시스템] 명시 실행 요청을 감지해 최근 제안 액션(${actionType})을 바로 실행합니다.`,
  );
  await executeAskSuggestedAction(actionType, {
    allowWhileBusy: true,
    actionOverride: action,
    instructionConfirmed: canBypassInstructionConfirm,
  });
  const stamp = new Date().toISOString();
  state.liveAsk.history.push({ role: "user", content: question, ts: stamp });
  state.liveAsk.history.push({
    role: "assistant",
    content: "명시 실행 요청을 확인하여 최근 제안 액션을 즉시 실행했습니다. 진행 로그는 시스템 메시지에서 확인하세요.",
    ts: stamp,
    action,
    meta: normalizeLiveAskMeta({
      backend: askBackendInputValue(),
      model: askModelInputValue() || "",
      reasoning: state.ask.reasoningEffort || "off",
    }),
  });
  if (state.liveAsk.history.length > 80) {
    state.liveAsk.history = state.liveAsk.history.slice(-80);
  }
  saveLiveAskHistory();
  renderLiveAskThread();
  setAskStatus("명시 실행 요청에 따라 최근 제안 액션을 바로 실행했습니다.");
  return true;
}

function shouldAutoRunCapabilityInPlan(plan) {
  const delegated = normalizeAskActionType(plan?.delegatedActionType);
  if (delegated) return isAskPlanInstantActionType(delegated);
  const effect = normalizeAskActionType(plan?.effect);
  return ASK_SAFE_CAPABILITY_EFFECTS.has(effect);
}

function normalizeActionExecutionHandoff(raw) {
  if (!raw || typeof raw !== "object") return null;
  const handoff = {};
  const planner = String(raw.planner || "").trim().toLowerCase();
  if (planner) handoff.planner = planner;
  const intent = String(raw.intent || "").trim().toLowerCase();
  if (intent) handoff.intent = intent;
  const rationale = String(raw.intent_rationale || raw.rationale || "").trim();
  if (rationale) handoff.intent_rationale = rationale.slice(0, 320);
  const confidenceRaw = Number(raw.confidence);
  if (Number.isFinite(confidenceRaw)) {
    handoff.confidence = Math.max(0, Math.min(1, confidenceRaw));
  }
  const preflightRaw = raw.preflight;
  if (preflightRaw && typeof preflightRaw === "object") {
    const preflight = {};
    const status = String(preflightRaw.status || "").trim().toLowerCase();
    if (["ok", "missing_run", "missing_instruction", "needs_confirmation"].includes(status)) {
      preflight.status = status;
    }
    ["ready_for_execute", "run_exists", "create_if_missing", "requires_run_confirmation", "requires_instruction_confirm"]
      .forEach((key) => {
        if (typeof preflightRaw[key] === "boolean") preflight[key] = Boolean(preflightRaw[key]);
      });
    ["run_rel", "run_hint", "resolved_run_rel"].forEach((key) => {
      const token = String(preflightRaw[key] || "").trim();
      if (token) preflight[key] = token.slice(0, 220);
    });
    const instructionRaw = preflightRaw.instruction;
    if (instructionRaw && typeof instructionRaw === "object") {
      const instruction = {};
      if (typeof instructionRaw.required === "boolean") instruction.required = Boolean(instructionRaw.required);
      if (typeof instructionRaw.available === "boolean") instruction.available = Boolean(instructionRaw.available);
      const selected = String(instructionRaw.selected || "").trim();
      if (selected) instruction.selected = selected.slice(0, 240);
      if (Array.isArray(instructionRaw.candidates)) {
        const candidates = instructionRaw.candidates
          .map((item) => String(item || "").trim())
          .filter(Boolean)
          .slice(0, 8);
        if (candidates.length) instruction.candidates = candidates;
      }
      if (Object.keys(instruction).length) preflight.instruction = instruction;
    }
    if (Array.isArray(preflightRaw.notes)) {
      const notes = preflightRaw.notes.map((item) => String(item || "").trim()).filter(Boolean).slice(0, 8);
      if (notes.length) preflight.notes = notes;
    }
    if (Object.keys(preflight).length) handoff.preflight = preflight;
  }
  return Object.keys(handoff).length ? handoff : null;
}

function enrichAskActionPlanWithPlannerMeta(plan, action) {
  const out = plan && typeof plan === "object" ? { ...plan } : {};
  const actionObj = action && typeof action === "object" ? action : null;
  if (!actionObj) return out;
  const planner = String(actionObj.planner || "").trim().toLowerCase();
  const confidenceRaw = Number(actionObj.confidence);
  const confidence = Number.isFinite(confidenceRaw) ? Math.max(0, Math.min(1, confidenceRaw)) : null;
  const rationale = String(actionObj.intent_rationale || "").trim();
  const handoff = normalizeActionExecutionHandoff(actionObj.execution_handoff);
  const metaParts = [];
  if (planner) metaParts.push(`planner=${planner}`);
  if (confidence !== null) metaParts.push(`confidence=${confidence.toFixed(2)}`);
  if (handoff?.preflight?.status) metaParts.push(`preflight=${handoff.preflight.status}`);
  if (rationale) metaParts.push(`rationale=${rationale.length > 90 ? `${rationale.slice(0, 89)}…` : rationale}`);
  if (metaParts.length) {
    const baseMeta = String(out.meta || "").trim();
    out.meta = [baseMeta, metaParts.join(" · ")].filter(Boolean).join(" · ");
  }
  try {
    const previewObj = JSON.parse(String(out.preview || "{}"));
    if (previewObj && typeof previewObj === "object") {
      previewObj.planner = planner || undefined;
      previewObj.confidence = confidence === null ? undefined : confidence;
      previewObj.intent_rationale = rationale || undefined;
      previewObj.execution_handoff = handoff || undefined;
      out.preview = JSON.stringify(previewObj, null, 2);
    }
  } catch (_err) {
    // Keep original preview text if not JSON.
  }
  out.planner = planner || "";
  out.confidence = confidence === null ? undefined : confidence;
  out.intent_rationale = rationale || "";
  out.execution_handoff = handoff;
  return out;
}

async function buildAskActionPlan(actionType, options = {}) {
  if (String(actionType || "").startsWith("capability:")) {
    const action = resolveAskActionContext(actionType, options?.actionOverride);
    const capId = String(actionType || "").slice("capability:".length).trim();
    if (!capId) throw new Error("capability id is required");
    const runRel = selectedRunRel();
    const payload = await fetchJSON("/api/capabilities/execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id: capId,
        dry_run: true,
        run: runRel || undefined,
      }),
    });
    return enrichAskActionPlanWithPlannerMeta({
      type: actionType,
      title: `${payload?.label || capId} 미리보기`,
      meta: `Capability action: ${payload?.action_kind || "none"}`,
      preview: String(payload?.preview || JSON.stringify(payload || {}, null, 2)),
      effect: String(payload?.effect || "").trim().toLowerCase(),
      delegatedActionType: String(payload?.action_type || "").trim().toLowerCase(),
      actionKind: String(payload?.action_kind || "").trim().toLowerCase(),
    }, action);
  }
  if (actionType === "run_feather") {
    const action = resolveAskActionContext(actionType, options?.actionOverride);
    const runHint = normalizeRunHint(action?.run_hint || "");
    const resolvedRun = runHint ? resolveRunRelFromHint(runHint, { strict: true }) : "";
    const createRunName = sanitizeRunNameHint(runHint);
    const payload = buildFeatherPayload({ fallbackQuery: latestAskFallbackQuery() });
    if (resolvedRun) {
      payload.output = resolvedRun;
    } else if (runHint) {
      payload.output = joinPath(siteRunsPrefix(), createRunName || runHint);
    }
    const runMeta = runHint
      ? (resolvedRun
        ? `대상 run=${stripSiteRunsPrefix(resolvedRun) || resolvedRun}`
        : `대상 run=${runHint} (없으면 생성 예정)`)
      : "현재 Feather 폼 값을 사용해 수집 작업을 시작합니다.";
    return enrichAskActionPlanWithPlannerMeta({
      type: actionType,
      title: "Feather 실행 미리보기",
      meta: runMeta,
      preview: JSON.stringify(
        {
          endpoint: "/api/feather/start",
          payload,
          target_run_hint: runHint || undefined,
          target_run_resolved: resolvedRun || undefined,
          create_if_missing: Boolean(action?.create_if_missing),
          auto_instruction: Boolean(action?.auto_instruction),
          require_instruction_confirm: Boolean(action?.require_instruction_confirm),
          instruction_confirm_reason: String(action?.instruction_confirm_reason || "").trim() || undefined,
          topic_hint: String(action?.topic_hint || "").trim() || undefined,
        },
        null,
        2,
      ),
    }, action);
  }
  if (actionType === "run_federlicht") {
    const action = resolveAskActionContext(actionType, options?.actionOverride);
    const runHint = normalizeRunHint(action?.run_hint || "");
    const resolvedRun = runHint ? resolveRunRelFromHint(runHint, { strict: true }) : "";
    const payload = buildFederlichtPayload();
    if (resolvedRun) {
      payload.run = resolvedRun;
      payload.output = ensureOutputPathForRun(payload.output, resolvedRun);
    }
    await applyFederlichtOutputSuggestionToPayload(payload, { syncInput: false });
    const runMeta = runHint
      ? (resolvedRun
        ? `대상 run=${stripSiteRunsPrefix(resolvedRun) || resolvedRun}`
        : `대상 run=${runHint} (없으면 생성 예정)`)
      : "현재 Federlicht 폼 값을 사용해 보고서 생성을 시작합니다.";
    return enrichAskActionPlanWithPlannerMeta({
      type: actionType,
      title: "Federlicht 실행 미리보기",
      meta: runMeta,
      preview: JSON.stringify(
        {
          endpoint: "/api/federlicht/start",
          payload,
          target_run_hint: runHint || undefined,
          target_run_resolved: resolvedRun || undefined,
          create_if_missing: Boolean(action?.create_if_missing),
        },
        null,
        2,
      ),
    }, action);
  }
  if (actionType === "run_feather_then_federlicht") {
    const action = resolveAskActionContext(actionType, options?.actionOverride);
    const runHint = normalizeRunHint(action?.run_hint || "");
    const resolvedRun = runHint ? resolveRunRelFromHint(runHint, { strict: true }) : "";
    const createRunName = sanitizeRunNameHint(runHint);
    const featherPayload = buildFeatherPayload({ fallbackQuery: latestAskFallbackQuery() });
    if (resolvedRun) {
      featherPayload.output = resolvedRun;
    } else if (runHint) {
      featherPayload.output = joinPath(siteRunsPrefix(), createRunName || runHint);
    }
    const federPayload = buildFederlichtPayload();
    if (resolvedRun) {
      federPayload.run = resolvedRun;
      federPayload.output = ensureOutputPathForRun(federPayload.output, resolvedRun);
    }
    await applyFederlichtOutputSuggestionToPayload(federPayload, { syncInput: false });
    const runMeta = runHint
      ? (resolvedRun
        ? `대상 run=${stripSiteRunsPrefix(resolvedRun) || resolvedRun}`
        : `대상 run=${runHint} (없으면 생성 후 실행)`)
      : "1) Feather 수집 완료 후 2) 동일 run에서 Federlicht를 자동 실행합니다.";
    return enrichAskActionPlanWithPlannerMeta({
      type: actionType,
      title: "Feather -> Federlicht 실행 미리보기",
      meta: runMeta,
      preview: JSON.stringify(
        {
          sequence: [
            { endpoint: "/api/feather/start", payload: featherPayload },
            { endpoint: "/api/federlicht/start", payload: federPayload },
          ],
          target_run_hint: runHint || undefined,
          target_run_resolved: resolvedRun || undefined,
          create_if_missing: Boolean(action?.create_if_missing),
          auto_instruction: Boolean(action?.auto_instruction),
          require_instruction_confirm: Boolean(action?.require_instruction_confirm),
          instruction_confirm_reason: String(action?.instruction_confirm_reason || "").trim() || undefined,
          topic_hint: String(action?.topic_hint || "").trim() || undefined,
        },
        null,
        2,
      ),
    }, action);
  }
  if (actionType === "create_run_folder") {
    const fallbackTopic = String(state.ask.pendingQuestion || state.liveAsk.pendingQuestion || "").trim();
    const action = resolveAskActionContext(actionType, options?.actionOverride);
    const topicHint = String(action?.topic_hint || fallbackTopic || "").trim();
    const runNameHint = String(action?.run_name_hint || action?.run_hint || "").trim();
    const runName = sanitizeRunNameHint(runNameHint || topicHint);
    return enrichAskActionPlanWithPlannerMeta({
      type: actionType,
      title: "새 Run Folder 생성 미리보기",
      meta: `${siteRunsPrefix()} 하위에 run 폴더를 만들고 instruction 초안을 생성합니다.`,
      preview: JSON.stringify(
        {
          endpoint: "/api/runs/create",
          payload: {
            run_name: runName || undefined,
            topic: topicHint || undefined,
          },
          run_name_hint: runNameHint || undefined,
        },
        null,
        2,
      ),
    }, action);
  }
  if (actionType === "switch_run") {
    const action = resolveAskActionContext(actionType, options?.actionOverride);
    const runHint = normalizeRunHint(action?.run_hint || "");
    if (!runHint) {
      throw new Error("run_hint not found");
    }
    const allowCreate = Boolean(action?.create_if_missing);
    const resolvedRunRel = resolveRunRelFromHint(runHint, { strict: true });
    return enrichAskActionPlanWithPlannerMeta({
      type: actionType,
      title: "Run 전환 미리보기",
      meta: resolvedRunRel
        ? "대상 run을 선택하고 Workspace 상태를 동기화합니다."
        : (
          allowCreate
            ? "일치 run이 없으면 동일 이름 run을 생성한 뒤 전환합니다."
            : "일치하는 run을 찾지 못했습니다. run 이름을 더 구체적으로 지정하세요."
        ),
      preview: JSON.stringify(
        {
          effect: "switch_run",
          run_hint: runHint,
          resolved_run: resolvedRunRel || null,
          create_if_missing: allowCreate,
        },
        null,
        2,
      ),
    }, action);
  }
  if (actionType === "preset_resume_stage") {
    const action = resolveAskActionContext(actionType, options?.actionOverride);
    const stage = String(action?.stage || "").trim().toLowerCase();
    if (!WORKFLOW_STAGE_ORDER.includes(stage)) {
      throw new Error("stage hint is missing");
    }
    const ordered = workflowStageOrder();
    const activeSet = new Set(state.workflow.selectedStages);
    activeSet.add(stage);
    const selectedOrdered = ordered.filter((id) => activeSet.has(id));
    const startIdx = selectedOrdered.indexOf(stage);
    const resumeStages = startIdx >= 0 ? selectedOrdered.slice(startIdx) : [stage];
    return enrichAskActionPlanWithPlannerMeta({
      type: actionType,
      title: `${workflowLabel(stage)}부터 재시작 미리보기`,
      meta: "Federlicht stages/skip_stages 프리셋을 재구성합니다.",
      preview: JSON.stringify(
        {
          effect: "preset_resume_stage",
          resume_stage: stage,
          stages: resumeStages.join(","),
          skip_stages: "",
        },
        null,
        2,
      ),
    }, action);
  }
  if (actionType === "focus_editor") {
    const action = resolveAskActionContext(actionType, options?.actionOverride);
    const target = String(action?.target || "federlicht_prompt").trim().toLowerCase();
    const resolvedTarget = target === "feather_instruction" ? "feather_instruction" : "federlicht_prompt";
    const editorSelector = resolvedTarget === "feather_instruction" ? "#feather-query" : "#federlicht-prompt";
    return enrichAskActionPlanWithPlannerMeta({
      type: actionType,
      title: "편집기 포커스 이동 미리보기",
      meta: "실행 없이 입력 편집기로 이동합니다.",
      preview: JSON.stringify(
        {
          effect: "focus_editor",
          target: resolvedTarget,
          tab: resolvedTarget === "feather_instruction" ? "feather" : "federlicht",
          editor: editorSelector,
        },
        null,
        2,
      ),
    }, action);
  }
  if (actionType === "set_action_mode") {
    const action = resolveAskActionContext(actionType, options?.actionOverride);
    const mode = String(action?.mode || "").trim().toLowerCase() === "act" ? "act" : "plan";
    const allowArtifacts = action && Object.prototype.hasOwnProperty.call(action, "allow_artifacts")
      ? Boolean(action.allow_artifacts)
      : undefined;
    return enrichAskActionPlanWithPlannerMeta({
      type: actionType,
      title: "Ask 실행 정책 미리보기",
      meta: "FederHav Plan/Act 모드 정책을 변경합니다.",
      preview: JSON.stringify(
        {
          effect: "set_action_mode",
          mode,
          allow_artifacts: allowArtifacts,
        },
        null,
        2,
      ),
    }, action);
  }
  throw new Error(`unsupported action: ${actionType}`);
}

async function executeAskSuggestedAction(actionType, options = {}) {
  const allowWhileBusy = Boolean(options && options.allowWhileBusy);
  const actionOverride = normalizeAskActionOverride(actionType, options?.actionOverride);
  const needsInstructionConfirm = actionRequiresInstructionConfirm(actionType, actionOverride);
  const instructionConfirmed = Boolean(options?.instructionConfirmed);
  if (needsInstructionConfirm && !instructionConfirmed) {
    appendLog(`[run-agent:action] blocked=${normalizeAskActionType(actionType)} (instruction confirmation required)\n`);
    setAskStatus("Instruction 확인이 필요합니다. 확인 모달에서 체크 후 실행하세요.");
    if (!isAskActionModalOpen()) {
      try {
        const plan = await buildAskActionPlan(actionType, { actionOverride });
        openAskActionModal({
          ...plan,
          actionOverride: actionOverride || undefined,
        });
      } catch (err) {
        appendLog(`[run-agent:action] instruction confirmation modal build failed: ${err}\n`);
      }
    } else {
      updateAskActionInstructionConfirmNote();
      updateAskActionRunTargetNote();
    }
    return;
  }
  if (state.activeJobId) {
    setAskStatus("이미 실행 중인 작업이 있습니다. 현재 작업 종료 후 다시 시도하세요.");
    return;
  }
  if (state.ask.busy && !allowWhileBusy) {
    setAskStatus("현재 답변 생성 중입니다. 완료 후 실행하세요.");
    return;
  }
  if (actionType === "run_feather") {
    const runOverride = resolveActionOverrideWithRunHint(actionType, actionOverride);
    const createIfMissing = Boolean(runOverride.actionOverride?.create_if_missing);
    if (runOverride.inferredRunHint) {
      appendLog(`[run-agent:action] run_feather inferred run_hint=${runOverride.inferredRunHint}\n`);
    }
    const targetRun = await resolveActionRunTarget(actionType, {
      createIfMissing,
      actionOverride: runOverride.actionOverride,
    });
    if (targetRun.runHint && !targetRun.runRel) {
      setAskStatus(`실행 대상 run을 찾지 못했습니다: ${targetRun.runHint}`);
      appendLog(`[run-agent:action] run_feather unresolved run_hint=${targetRun.runHint}\n`);
      return;
    }
    if (targetRun.runRel) {
      syncFeatherRunTargetFields(targetRun.runRel);
    }
    if (targetRun.created) {
      appendLog(`[run-agent:action] run target created -> ${targetRun.runRel}\n`);
    }
    const runRelForAction = normalizePathString(targetRun.runRel || selectedRunRel() || "");
    const ok = await ensureFeatherActionHasMeaningfulInput(runRelForAction, {
      forceAutoDraft: Boolean(runOverride.actionOverride?.auto_instruction),
      topicHint: String(runOverride.actionOverride?.topic_hint || ""),
    });
    if (!ok) {
      return;
    }
    appendLog(`[run-agent:action] run_feather -> ${normalizePathString(targetRun.runRel || selectedRunRel() || "-")}\n`);
    document.querySelector('[data-tab="feather"]')?.click();
    $("#feather-form")?.requestSubmit();
    return;
  }
  if (actionType === "run_federlicht") {
    const runOverride = resolveActionOverrideWithRunHint(actionType, actionOverride);
    const createIfMissing = Boolean(runOverride.actionOverride?.create_if_missing);
    if (runOverride.inferredRunHint) {
      appendLog(`[run-agent:action] run_federlicht inferred run_hint=${runOverride.inferredRunHint}\n`);
    }
    const targetRun = await resolveActionRunTarget(actionType, {
      createIfMissing,
      actionOverride: runOverride.actionOverride,
    });
    if (targetRun.runHint && !targetRun.runRel) {
      setAskStatus(`실행 대상 run을 찾지 못했습니다: ${targetRun.runHint}`);
      appendLog(`[run-agent:action] run_federlicht unresolved run_hint=${targetRun.runHint}\n`);
      return;
    }
    if (targetRun.created) {
      appendLog(`[run-agent:action] run target created -> ${targetRun.runRel}\n`);
    }
    const runLabel = normalizePathString(targetRun.runRel || selectedRunRel() || "");
    if (runLabel) {
      await applyRunSelection(runLabel);
      const outputInput = $("#federlicht-output");
      if (outputInput) {
        const nextOutput = ensureOutputPathForRun(outputInput.value, runLabel);
        const fieldPath = toFederlichtOutputFieldPath(nextOutput);
        if (fieldPath && outputInput.value !== fieldPath) {
          outputInput.value = fieldPath;
          reportOutputTouched = true;
          appendLog(`[run-agent:action] run_federlicht output -> ${fieldPath}\n`);
        }
      }
      appendLog(`[run-agent:action] run_federlicht -> ${runLabel}\n`);
      setAskStatus(`Federlicht 실행 대상 run: ${stripSiteRunsPrefix(runLabel) || runLabel}`);
    }
    document.querySelector('[data-tab="federlicht"]')?.click();
    $("#federlicht-form")?.requestSubmit();
    return;
  }
  if (actionType === "run_feather_then_federlicht") {
    try {
      const runOverride = resolveActionOverrideWithRunHint(actionType, actionOverride);
      const createIfMissing = Boolean(runOverride.actionOverride?.create_if_missing);
      if (runOverride.inferredRunHint) {
        appendLog(`[run-agent:action] run_pipeline inferred run_hint=${runOverride.inferredRunHint}\n`);
      }
      const targetRun = await resolveActionRunTarget(actionType, {
        createIfMissing,
        actionOverride: runOverride.actionOverride,
      });
      if (targetRun.runHint && !targetRun.runRel) {
        setAskStatus(`실행 대상 run을 찾지 못했습니다: ${targetRun.runHint}`);
        appendLog(`[run-agent:action] run_pipeline unresolved run_hint=${targetRun.runHint}\n`);
        return;
      }
      if (targetRun.runRel) {
        syncFeatherRunTargetFields(targetRun.runRel);
      }
      if (targetRun.created) {
        appendLog(`[run-agent:action] run target created -> ${targetRun.runRel}\n`);
      }
      const runRelForAction = normalizePathString(targetRun.runRel || selectedRunRel() || "");
      const ok = await ensureFeatherActionHasMeaningfulInput(runRelForAction, {
        forceAutoDraft: Boolean(runOverride.actionOverride?.auto_instruction),
        topicHint: String(runOverride.actionOverride?.topic_hint || ""),
      });
      if (!ok) {
        return;
      }
      const featherPayload = buildFeatherPayload({ fallbackQuery: latestAskFallbackQuery() });
      const runRel = featherPayload.output;
      await startJob("/api/feather/start", featherPayload, {
        kind: "feather",
        onSuccess: async () => {
          await loadRuns().catch(() => {});
          if (runRel && $("#run-select")) {
            $("#run-select").value = runRel;
            if ($("#prompt-run-select")) $("#prompt-run-select").value = runRel;
            if ($("#instruction-run-select")) $("#instruction-run-select").value = runRel;
            refreshRunDependentFields();
            await updateRunStudio(runRel).catch(() => {});
          }
          try {
            document.querySelector('[data-tab="federlicht"]')?.click();
            const federPayload = buildFederlichtPayload();
            if (runRel) {
              federPayload.run = runRel;
              federPayload.output = ensureOutputPathForRun(federPayload.output, runRel);
            }
            await applyFederlichtOutputSuggestionToPayload(federPayload, { syncInput: true });
            const reportRunRel = federPayload.run;
            await startJob("/api/federlicht/start", federPayload, {
              kind: "federlicht",
              onSuccess: async () => {
                await loadRuns().catch(() => {});
                if (reportRunRel && $("#run-select")) {
                  $("#run-select").value = reportRunRel;
                  if ($("#instruction-run-select")) $("#instruction-run-select").value = reportRunRel;
                  refreshRunDependentFields();
                  await updateRunStudio(reportRunRel).catch(() => {});
                }
              },
            });
          } catch (err) {
            appendLog(`[ask-action] federlicht auto-start failed: ${err}\n`);
            setAskStatus(`Feather 완료 후 Federlicht 자동 실행 실패: ${err}`);
          }
        },
      });
      setAskStatus("Feather 실행 시작. 완료 후 Federlicht 자동 실행 예정입니다.");
    } catch (err) {
      appendLog(`[ask-action] ${err}\n`);
      setAskStatus(`실행 실패: ${err}`);
    }
  }
  if (actionType === "create_run_folder") {
    try {
      const fallbackTopic = String(state.ask.pendingQuestion || state.liveAsk.pendingQuestion || "").trim();
      const action = resolveAskActionContext(actionType, actionOverride);
      const topicHint = String(action?.topic_hint || fallbackTopic || "").trim();
      const runNameHint = String(action?.run_name_hint || action?.run_hint || "").trim();
      const runName = sanitizeRunNameHint(runNameHint || topicHint);
      const created = await fetchJSON("/api/runs/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          run_name: runName || undefined,
          topic: topicHint || undefined,
        }),
      });
      const runRel = String(created?.run_rel || "").trim();
      const instructionPath = String(created?.instruction_path || "").trim();
      await loadRuns().catch(() => {});
      if (runRel) await applyRunSelection(runRel);
      const label = runRel ? (stripSiteRunsPrefix(runRel) || runRel) : "-";
      setAskStatus(`새 run folder 생성 완료: ${label}`);
      appendLog(`[run-agent:action] create_run_folder -> ${runRel || "-"}\n`);
      if (instructionPath) {
        appendLog(`[run-agent:action] instruction -> ${instructionPath}\n`);
      }
      return;
    } catch (err) {
      appendLog(`[ask-action] create_run_folder failed: ${err}\n`);
      setAskStatus(`새 run folder 생성 실패: ${err}`);
      return;
    }
  }
  if (actionType === "switch_run") {
    const runOverride = resolveActionOverrideWithRunHint(actionType, actionOverride);
    if (runOverride.inferredRunHint) {
      appendLog(`[run-agent:action] switch_run inferred run_hint=${runOverride.inferredRunHint}\n`);
    }
    const action = resolveAskActionContext(actionType, runOverride.actionOverride);
    const runHint = normalizeRunHint(action?.run_hint || "");
    if (!runHint) {
      setAskStatus("전환할 run 힌트를 찾지 못했습니다.");
      return;
    }
    const allowCreate = Boolean(action?.create_if_missing);
    const targetRun = await resolveActionRunTarget(actionType, {
      createIfMissing: allowCreate,
      actionOverride: runOverride.actionOverride,
    });
    const resolvedRunRel = normalizePathString(targetRun.runRel || "");
    if (!resolvedRunRel) {
      setAskStatus(`일치하는 run을 찾지 못했습니다: ${runHint}`);
      appendLog(`[run-agent:action] switch_run unresolved hint=${runHint}\n`);
      return;
    }
    const label = stripSiteRunsPrefix(resolvedRunRel) || resolvedRunRel;
    if (targetRun.created) {
      appendLog(`[run-agent:action] switch_run created run=${resolvedRunRel}\n`);
    }
    setAskStatus(`Run 전환 완료: ${label}`);
    appendLog(`[run-agent:action] switch_run -> ${resolvedRunRel}\n`);
    return;
  }
  if (actionType === "preset_resume_stage") {
    const action = resolveAskActionContext(actionType, actionOverride);
    const stage = String(action?.stage || "").trim().toLowerCase();
    if (!WORKFLOW_STAGE_ORDER.includes(stage)) {
      setAskStatus("재시작할 stage 정보를 찾지 못했습니다.");
      return;
    }
    document.querySelector('[data-tab="federlicht"]')?.click();
    const ok = applyResumeStagesFromStage(stage);
    if (!ok) {
      setAskStatus(`재시작 프리셋 적용 실패: ${stage}`);
      return;
    }
    setWorkflowStudioOpen(true, { stageId: stage });
    setAskStatus(`재시작 프리셋 적용: ${workflowLabel(stage)}부터`);
    appendLog(`[run-agent:action] preset_resume_stage -> ${stage}\n`);
    return;
  }
  if (actionType === "focus_editor") {
    const action = resolveAskActionContext(actionType, actionOverride);
    const target = String(action?.target || "federlicht_prompt").trim().toLowerCase();
    if (target === "feather_instruction") {
      document.querySelector('[data-tab="feather"]')?.click();
      const editor = $("#feather-query");
      if (!editor) {
        setAskStatus("Feather instruction 편집기를 찾지 못했습니다.");
        return;
      }
      editor.focus();
      editor.setSelectionRange(editor.value.length, editor.value.length);
      setAskStatus("Feather instruction 편집기로 이동했습니다.");
      appendLog("[run-agent:action] focus_editor -> feather_instruction\n");
      return;
    }
    document.querySelector('[data-tab="federlicht"]')?.click();
    const promptEditor = $("#federlicht-prompt");
    if (!promptEditor) {
      setAskStatus("Federlicht inline prompt 편집기를 찾지 못했습니다.");
      return;
    }
    promptEditor.focus();
    promptEditor.setSelectionRange(promptEditor.value.length, promptEditor.value.length);
    setAskStatus("Federlicht inline prompt 편집기로 이동했습니다.");
    appendLog("[run-agent:action] focus_editor -> federlicht_prompt\n");
    return;
  }
  if (actionType === "set_action_mode") {
    const action = resolveAskActionContext(actionType, actionOverride);
    const mode = String(action?.mode || "").trim().toLowerCase() === "act" ? "act" : "plan";
    setAskActionMode(mode, { persist: true });
    if (action && Object.prototype.hasOwnProperty.call(action, "allow_artifacts")) {
      state.ask.allowArtifactWrites = Boolean(action.allow_artifacts);
    }
    syncAskActionPolicyInputs();
    saveAskActionPrefs();
    const allowText = mode === "act" ? ` · 파일쓰기허용=${state.ask.allowArtifactWrites ? "on" : "off"}` : "";
    setAskStatus(`FederHav 모드 전환: ${mode.toUpperCase()}${allowText}`);
    appendLog(
      `[run-agent:action] set_action_mode -> ${mode} allow_artifacts=${state.ask.allowArtifactWrites ? "1" : "0"}\n`,
    );
    return;
  }
  if (String(actionType || "").startsWith("capability:")) {
    const capId = String(actionType || "").slice("capability:".length).trim();
    if (!capId) {
      setAskStatus("Capability ID가 비어 있습니다.");
      return;
    }
    const runRel = selectedRunRel();
    const payload = await fetchJSON("/api/capabilities/execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id: capId,
        dry_run: false,
        run: runRel || undefined,
      }),
    });
    const effect = String(payload?.effect || "").trim().toLowerCase();
    if (effect === "open_path" && payload?.path) {
      await loadFilePreview(String(payload.path), { readOnly: true });
      setAskStatus(`Capability 실행 완료: ${capId} · 파일 열기`);
      appendLog(`[capability] ${capId} -> open_path ${payload.path}\n`);
      return;
    }
    if (effect === "open_url" && payload?.url) {
      window.open(String(payload.url), "_blank");
      setAskStatus(`Capability 실행 완료: ${capId} · URL 열기`);
      appendLog(`[capability] ${capId} -> open_url ${payload.url}\n`);
      return;
    }
    if (effect === "set_inline_prompt" && payload?.prompt_text) {
      const prompt = $("#federlicht-prompt");
      if (prompt) {
        const text = String(payload.prompt_text || "");
        prompt.value = text;
        prompt.focus();
        prompt.setSelectionRange(text.length, text.length);
      }
      setAskStatus(`Capability 실행 완료: ${capId} · Inline Prompt 반영`);
      appendLog(`[capability] ${capId} -> set_inline_prompt\n`);
      return;
    }
    if (effect === "delegate" && payload?.action_type) {
      await executeAskSuggestedAction(String(payload.action_type));
      return;
    }
    if (effect === "mcp_ping") {
      const ok = payload?.ok === false ? "failed" : "ok";
      setAskStatus(`Capability 실행 완료: ${capId} · mcp_ping(${ok})`);
      appendLog(`[capability] ${capId} -> mcp_ping ${payload?.endpoint || ""} status=${payload?.http_status || "-"}\n`);
      return;
    }
    setAskStatus(`Capability 실행 완료: ${capId}`);
    appendLog(`[capability] ${capId} -> ${effect || "done"}\n`);
    return;
  }
}

async function runAskSuggestedAction(actionType, options = {}) {
  try {
    const normalizedActionType = normalizeAskActionType(actionType);
    const actionOverride = normalizeAskActionOverride(actionType, options?.actionOverride);
    const runTargetOverride = isRunTargetActionType(normalizedActionType)
      ? resolveActionOverrideWithRunHint(normalizedActionType, actionOverride)
      : { actionOverride, inferredRunHint: "" };
    const effectiveOverride = normalizeAskActionOverride(
      actionType,
      runTargetOverride?.actionOverride || actionOverride,
    );
    if (runTargetOverride?.inferredRunHint) {
      appendLog(`[run-agent:action] inferred run_hint=${runTargetOverride.inferredRunHint}\n`);
    }
    const mode = normalizeAskActionType(state.ask.actionMode || "plan");
    const plan = await buildAskActionPlan(actionType, { actionOverride: effectiveOverride });
    const isRunAction = isAskWriteActionType(normalizedActionType) || isRunTargetActionType(normalizedActionType);
    const needsInstructionConfirm = actionRequiresInstructionConfirm(normalizedActionType, effectiveOverride);
    if (isRunAction) {
      openAskActionModal({
        ...plan,
        actionOverride: effectiveOverride || undefined,
      });
      setAskStatus(
        needsInstructionConfirm
          ? "Run 대상과 instruction 확인을 완료한 뒤 실행하세요."
          : "Run 대상과 생성 정책을 확인한 뒤 실행하세요.",
      );
      return;
    }
    if (mode === "plan" && isAskPlanInstantActionType(normalizedActionType)) {
      setAskStatus("Plan mode: 즉시 반영 가능한 제안을 바로 실행합니다.");
      await executeAskSuggestedAction(actionType, { actionOverride: effectiveOverride });
      return;
    }
    const canInstantInPlan = mode === "plan"
      && !isRunAction
      && normalizedActionType.startsWith("capability:")
      && shouldAutoRunCapabilityInPlan(plan);
    if (canInstantInPlan) {
      setAskStatus("Plan mode: 안전한 capability 제안을 바로 실행합니다.");
      await executeAskSuggestedAction(actionType, { actionOverride: effectiveOverride });
      return;
    }
    const canAutoRun = mode === "act" && !needsInstructionConfirm && (!isRunAction || state.ask.allowArtifactWrites);
    if (canAutoRun) {
      setAskStatus("Act mode: 안전 규칙에 따라 제안을 바로 실행합니다.");
      await executeAskSuggestedAction(actionType, { actionOverride: effectiveOverride });
      return;
    }
    if (mode === "act" && isRunAction && !state.ask.allowArtifactWrites) {
      setAskStatus("Act 모드지만 파일쓰기허용이 꺼져 있어 확인 후 실행 모드로 전환합니다.");
    }
    openAskActionModal({
      ...plan,
      actionOverride: effectiveOverride || undefined,
    });
  } catch (err) {
    setAskStatus(`실행 미리보기 생성 실패: ${err}`);
  }
}

function handleWorkspacePanel() {
  const panel = $("#workspace-panel");
  if (!panel) return;
  panel.style.display = "none";
  setWorkspaceTab("templates");
  $("#workspace-open-settings")?.addEventListener("click", (ev) => {
    ev.preventDefault();
    ev.stopPropagation();
    if (state.workspace.open) {
      setWorkspacePanelOpen(false);
      return;
    }
    setWorkspacePanelOpen(true, "agents");
  });
  $("#cap-studio-refresh")?.addEventListener("click", () => {
    loadAskCapabilityRegistry({ silent: false }).catch((err) => {
      setCapabilityStudioStatus(`Capability registry load failed: ${err}`);
      setAskStatus(`Capability registry load failed: ${err}`);
    });
  });
  $("#cap-studio-kind")?.addEventListener("change", () => {
    const kind = String($("#cap-studio-kind")?.value || "tool").trim().toLowerCase();
    const actionSelect = $("#cap-studio-action-kind");
    if (!actionSelect) return;
    if (kind === "mcp" && String(actionSelect.value || "").trim().toLowerCase() === "none") {
      actionSelect.value = "mcp_ping";
    }
  });
  $("#cap-studio-add")?.addEventListener("click", () => {
    addCapabilityFromStudio().catch((err) => {
      setCapabilityStudioStatus(`Capability save failed: ${err}`);
      setAskStatus(`Capability save failed: ${err}`);
    });
  });
  $("#workspace-close")?.addEventListener("click", () => setWorkspacePanelOpen(false));
  panel.querySelectorAll("[data-workspace-tab]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const tabKey = btn.getAttribute("data-workspace-tab") || "templates";
      setWorkspaceTab(tabKey);
    });
  });
  panel.addEventListener("click", (ev) => ev.stopPropagation());
  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape" && state.workspace.open) {
      setWorkspacePanelOpen(false);
    }
  });
}

function openJobsModal() {
  const modal = $("#jobs-modal");
  if (!modal) return;
  const runRel = selectedRunRel();
  if (!runRel) return;
  openOverlayModal("jobs-modal");
  const subtitle = $("#jobs-modal-subtitle");
  if (subtitle) {
    subtitle.textContent = runRel
      ? `Latest activity for ${runBaseName(runRel)}.`
      : "Select a run folder to view activity.";
  }
  renderJobs();
}

function closeJobsModal() {
  closeOverlayModal("jobs-modal");
}

async function loadSaveAsDir(relPath) {
  const list = $("#saveas-list");
  const pathInput = $("#saveas-path");
  if (!list || !pathInput) return;
  list.innerHTML = `<div class="modal-item muted">Loading...</div>`;
  try {
    const data = await fetchJSON(`/api/fs?path=${encodeURIComponent(relPath || "")}`);
    state.saveAs.path = data.path || "";
    pathInput.value = data.path || "";
    list.innerHTML = "";
    for (const entry of data.entries || []) {
      const item = document.createElement("button");
      item.type = "button";
      item.className = "modal-item";
      item.innerHTML = `<strong>${escapeHtml(entry.name)}</strong><small>${entry.is_dir ? "folder" : "file"}</small>`;
      item.addEventListener("click", () => {
        if (entry.is_dir) {
          loadSaveAsDir(entry.path);
        } else {
          const filenameInput = $("#saveas-filename");
          if (filenameInput) filenameInput.value = entry.name;
        }
      });
      list.appendChild(item);
    }
  } catch (err) {
    list.innerHTML = `<div class="modal-item muted">Failed to load folder: ${escapeHtml(String(err))}</div>`;
  }
}

function flashElement(el) {
  if (!el) return;
  el.classList.add("flash");
  window.setTimeout(() => el.classList.remove("flash"), 1200);
}

function formatDate(isoString) {
  if (!isoString) return "-";
  const date = new Date(isoString);
  if (Number.isNaN(date.getTime())) return isoString;
  return date.toLocaleString();
}

function setText(selector, value) {
  const el = $(selector);
  if (el) el.textContent = value ?? "";
}

function updateHeroStats() {
  const selected = selectedRunRel();
  const badge = selected ? runBaseName(selected) : "-";
  setText("#run-roots-badge", badge);
  renderRunContextSummary();
  updateRecentJobsCard();
}

function updateRecentJobsCard() {
  const runRel = selectedRunRel();
  const subtitle = $("#recent-jobs-subtitle");
  if (subtitle) {
    subtitle.textContent = runRel
      ? `Latest activity for ${runBaseName(runRel)}.`
      : "Select a run folder to view activity.";
  }
  updateRecentJobsSummary();
}

function buildRecentJobs(runRel) {
  const history = runRel ? state.historyLogs[runRel] || [] : [];
  const historyJobs = history.map((entry) => ({
    job_id: `history:${entry.path}`,
    kind: entry.kind || "log",
    status: entry.status || "history",
    updated_at: entry.updated_at,
    run_rel: entry.run_rel,
    log_path: entry.path,
    label: entry.name || entry.path,
    source: "history",
  }));
  const liveJobs = state.jobs
    .filter((job) => !job.run_rel || !runRel || job.run_rel === runRel)
    .map((job) => ({ ...job, source: "live" }));
  return [...liveJobs, ...historyJobs].sort((a, b) => {
    const ta = a.updated_at ? Date.parse(a.updated_at) : a.started_at || 0;
    const tb = b.updated_at ? Date.parse(b.updated_at) : b.started_at || 0;
    return tb - ta;
  });
}

function updateRecentJobsSummary() {
  const runRel = selectedRunRel();
  const countEl = $("#recent-jobs-count");
  const lastEl = $("#recent-jobs-last");
  const openBtn = $("#jobs-open");
  if (!countEl || !lastEl) return;
  if (!runRel) {
    countEl.textContent = "0";
    lastEl.textContent = "No run selected.";
    if (openBtn) openBtn.disabled = true;
    return;
  }
  const jobs = buildRecentJobs(runRel);
  countEl.textContent = String(jobs.length || 0);
  if (!jobs.length) {
    lastEl.textContent = "No recent jobs.";
    if (openBtn) openBtn.disabled = true;
    return;
  }
  const top = jobs[0];
  const label = top.label || top.kind || "job";
  const status = top.status || "";
  lastEl.textContent = status ? `${label} · ${status}` : label;
  if (openBtn) openBtn.disabled = false;
}

function runFolderContextLabel() {
  const selected = normalizePathString(selectedRunRel() || "");
  if (selected) return stripSiteRunsPrefix(selected) || selected;
  const recent = normalizePathString(state.runs?.[0]?.run_rel || "");
  if (recent) return stripSiteRunsPrefix(recent) || recent;
  return "-";
}

function renderRunContextSummary() {
  if (!state.info) return;
  const strip = $("#meta-strip");
  const { run_roots: runRoots } = state.info;
  const runRootsLabel = formatRunRoots(runRoots || []);
  const pills = [];
  if (runRootsLabel && runRootsLabel !== "." && runRootsLabel !== "-") {
    pills.push(`workspace: ${runRootsLabel}`);
  }
  const hub = normalizePathString(state.info?.report_hub_root || "");
  const siteRoot = normalizePathString(state.info?.site_root || "");
  if (hub && hub !== siteRoot) {
    pills.push(`report hub: ${hub}`);
  }
  pills.push(`run folder: ${runFolderContextLabel()}`);
  if (strip) {
    strip.innerHTML = pills.map((p) => `<span class="meta-pill">${p}</span>`).join("");
    strip.classList.toggle("is-empty", pills.length === 0);
  }
  const sidebarSummary = $("#sidebar-run-context-text");
  if (sidebarSummary) {
    sidebarSummary.textContent = pills.join(" · ");
    sidebarSummary.title = pills.join(" | ");
  }
}

function setMetaStrip() {
  renderRunContextSummary();
}

function setWorkspaceSettingsStatus(message, isError = false) {
  const el = $("#workspace-settings-status");
  if (!el) return;
  el.textContent = String(message || "");
  el.classList.toggle("is-error", Boolean(isError));
}

function parseRunRootsInputValue(rawValue) {
  return String(rawValue || "")
    .split(",")
    .map((token) => normalizePathString(token))
    .filter(Boolean);
}

function appendRunRootTokenToWorkspaceInput(rootToken) {
  const input = $("#workspace-run-roots");
  if (!input) return false;
  const root = normalizePathString(rootToken || "");
  if (!root) return false;
  const merged = uniqueTokens([
    ...parseRunRootsInputValue(input.value || ""),
    root,
  ]);
  input.value = merged.join(", ");
  return true;
}

function applyWorkspaceSettingsEffectiveToInfo(effective) {
  if (!state.info || !effective || typeof effective !== "object") return;
  const runRoots = Array.isArray(effective.run_roots)
    ? effective.run_roots.map((item) => normalizePathString(item)).filter(Boolean)
    : [];
  if (runRoots.length) {
    state.info.run_roots = runRoots;
  }
  const siteRoot = normalizePathString(effective.site_root || "");
  const hubRoot = normalizePathString(effective.report_hub_root || "");
  if (siteRoot) state.info.site_root = siteRoot;
  if (hubRoot) state.info.report_hub_root = hubRoot;
}

function renderWorkspaceSettingsControls(payload = null) {
  const runRootsInput = $("#workspace-run-roots");
  const siteRootInput = $("#workspace-site-root");
  const hubRootInput = $("#workspace-report-hub-root");
  const saveBtn = $("#workspace-settings-save");
  const data = payload || state.workspaceSettings || {};
  const effective = data.effective && typeof data.effective === "object"
    ? data.effective
    : {};
  const runRoots = Array.isArray(effective.run_roots) ? effective.run_roots : [];
  if (runRootsInput) runRootsInput.value = runRoots.join(", ");
  if (siteRootInput) siteRootInput.value = String(effective.site_root || state.info?.site_root || "site");
  if (hubRootInput) {
    hubRootInput.value = String(
      effective.report_hub_root
      || state.info?.report_hub_root
      || reportHubBase(),
    );
  }
  const canEdit = data.can_edit !== undefined ? Boolean(data.can_edit) : Boolean(state.workspaceSettings.canEdit);
  state.workspaceSettings.canEdit = canEdit;
  if (saveBtn) {
    saveBtn.disabled = !canEdit;
    saveBtn.title = canEdit
      ? "Workspace root settings를 저장합니다."
      : "Root unlock 후 저장할 수 있습니다.";
  }
  if (!canEdit) {
    setWorkspaceSettingsStatus("workspace settings: root unlock required for save");
  }
}

async function loadWorkspaceSettings() {
  try {
    const payload = await fetchJSON("/api/workspace/settings");
    state.workspaceSettings = {
      effective: payload?.effective || null,
      stored: payload?.stored || null,
      path: String(payload?.path || ""),
      canEdit: Boolean(payload?.can_edit),
    };
    applyWorkspaceSettingsEffectiveToInfo(payload?.effective || {});
    renderWorkspaceSettingsControls(payload);
    const pathLabel = String(payload?.path || "site/federnett/workspace_settings.json");
    setWorkspaceSettingsStatus(`workspace settings loaded · ${pathLabel}`);
    setMetaStrip();
    syncFeatherOutputHint();
    return payload;
  } catch (err) {
    setWorkspaceSettingsStatus(`workspace settings load failed: ${err}`, true);
    throw err;
  }
}

async function saveWorkspaceSettingsFromControls() {
  const runRootsRaw = String($("#workspace-run-roots")?.value || "").trim();
  const siteRoot = String($("#workspace-site-root")?.value || "").trim();
  const reportHubRoot = String($("#workspace-report-hub-root")?.value || "").trim();
  const runRoots = runRootsRaw ? parseRunRootsInputValue(runRootsRaw) : null;
  const payload = pruneEmpty({
    run_roots: runRoots || undefined,
    site_root: siteRoot || undefined,
    report_hub_root: reportHubRoot || undefined,
  });
  const saved = await fetchJSON("/api/workspace/settings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  applyWorkspaceSettingsEffectiveToInfo(saved?.effective || {});
  setMetaStrip();
  await loadRuns();
  await loadWorkspaceSettings();
  appendLog("[workspace] settings saved and runs reloaded\n");
}

function bindHeroCards() {
  if (!state.info) return;
  const runRootsCard = $("#hero-card-run-roots");
  const runRoots = state.info.run_roots || [];
  const openRuns = () => {
    openRunPickerModal();
    loadRunPickerItems();
  };

  if (runRootsCard) {
    runRootsCard.addEventListener("click", () => {
      openRuns();
      if (runRoots.length > 1) {
        appendLog(`[run-roots] available: ${runRoots.join(", ")}\n`);
      }
    });
  }
}

async function loadInfo() {
  state.info = await fetchJSON("/api/info");
  const defaults = llmDefaults();
  window.FEDERNETT_OPENAI_MODEL_HINT = normalizeModelToken(defaults.openai_model || "");
  window.FEDERNETT_OPENAI_MODEL_VISION_HINT = normalizeModelToken(defaults.openai_model_vision || "");
  window.FEDERNETT_CODEX_MODEL_HINT = normalizeModelToken(defaults.codex_model || "");
  window.FEDERNETT_OPENAI_REASONING_API = Boolean(defaults.openai_reasoning_api);
  const runtimeDefault = normalizeAskRuntimeMode(defaults.federhav_runtime_mode || "auto");
  if (!state.ask.runtimeMode || state.ask.runtimeMode === "auto") {
    state.ask.runtimeMode = runtimeDefault;
  }
  if (state.info?.root_auth && typeof state.info.root_auth === "object") {
    applyRootAuthPayload(state.info.root_auth);
  }
  if (state.info?.session_auth && typeof state.info.session_auth === "object") {
    applySessionAuthPayload(state.info.session_auth);
  }
  const siteOutputInput = $("#federlicht-site-output");
  if (siteOutputInput && !String(siteOutputInput.value || "").trim()) {
    siteOutputInput.value = reportHubBase();
  }
  await loadWorkspaceSettings().catch(() => {
    setMetaStrip();
  });
  syncFeatherOutputHint();
}

function sortRuns(runs) {
  return [...runs].sort((a, b) => {
    const da = Date.parse(a.updated_at || "") || 0;
    const db = Date.parse(b.updated_at || "") || 0;
    return db - da;
  });
}

function makeRunOption(run) {
  const runRel = normalizePathString(run?.run_rel || "");
  const runName = String(run?.run_name || runBaseName(runRel) || "run");
  const stripRuns = stripSiteRunsPrefix(runRel) || runRel;
  const label = runName && stripRuns && runName !== stripRuns
    ? `${runName} · ${stripRuns}`
    : (stripRuns || runName || "run");
  const report = String(run?.latest_report_name || "").trim();
  const updated = run?.updated_at ? formatDate(run.updated_at) : "";
  const title = [runRel, report ? `latest report: ${report}` : "", updated ? `updated: ${updated}` : ""]
    .filter(Boolean)
    .join(" | ");
  return `<option value="${escapeHtml(runRel)}" title="${escapeHtml(title)}">${escapeHtml(label)}</option>`;
}

function ensureRunSelection(selectEl, fallbackRel) {
  if (!selectEl) return;
  const current = selectEl.value;
  const exists = state.runs.some((r) => r.run_rel === current);
  if (exists) return;
  const preferred =
    fallbackRel && state.runs.some((r) => r.run_rel === fallbackRel)
      ? fallbackRel
      : state.runs[0]?.run_rel;
  if (preferred) selectEl.value = preferred;
}

function defaultReportPath(runRel) {
  if (!runRel) return "";
  const normalizedRun = normalizePathString(runRel);
  if (!normalizedRun) return "";
  return `${normalizedRun}/report_full.html`;
}

function defaultPromptPath(runRel) {
  if (!runRel) return "";
  const normalizedRun = normalizePathString(runRel);
  if (!normalizedRun) return "";
  const runName = runBaseName(normalizedRun);
  return `${normalizedRun}/instruction/generated_prompt_${runName}.txt`;
}

function siteRunsBase() {
  const roots = Array.isArray(state.info?.run_roots) ? state.info.run_roots : [];
  const normalizedRoots = roots
    .map((entry) => normalizePathString(entry))
    .filter(Boolean);
  if (normalizedRoots.length) return normalizedRoots[0].replace(/\/+$/, "");
  const siteRoot = state.info?.site_root ? String(state.info.site_root) : "";
  if (!siteRoot) return "runs";
  return `${siteRoot.replace(/\/+$/, "")}/runs`;
}

function reportHubBase() {
  const hub = normalizePathString(state.info?.report_hub_root || "");
  if (hub) return hub;
  const siteRoot = normalizePathString(state.info?.site_root || "site");
  return siteRoot || "site";
}

function siteRunsPrefix() {
  return siteRunsBase().replace(/\/+$/, "");
}

function runRootFromRunRel(runRel) {
  const normalizedRun = normalizePathString(runRel || "");
  if (!normalizedRun) return "";
  const parent = parentPath(normalizedRun);
  return normalizePathString(parent || "");
}

function preferredRunRoot(options = {}) {
  const explicitRun = normalizePathString(options?.runRel || "");
  if (explicitRun) {
    const root = runRootFromRunRel(explicitRun);
    if (root) return root;
  }
  const selected = normalizePathString(selectedRunRel() || "");
  if (selected) {
    const root = runRootFromRunRel(selected);
    if (root) return root;
  }
  const promptRun = normalizePathString($("#prompt-run-select")?.value || "");
  if (promptRun) {
    const root = runRootFromRunRel(promptRun);
    if (root) return root;
  }
  const instructionRun = normalizePathString($("#instruction-run-select")?.value || "");
  if (instructionRun) {
    const root = runRootFromRunRel(instructionRun);
    if (root) return root;
  }
  return siteRunsPrefix();
}

function expandSiteRunsPath(value, options = {}) {
  const cleaned = normalizePathString(value);
  if (!cleaned) return "";
  const base = preferredRunRoot(options);
  if (cleaned.startsWith(`${base}/`)) return cleaned;
  const blockedPrefixes = ["site/", "examples/", "runs/", "instruction/"];
  if (blockedPrefixes.some((prefix) => cleaned.startsWith(prefix))) return cleaned;
  return `${base}/${cleaned}`;
}

function stripSiteRunsPrefix(value) {
  const cleaned = normalizePathString(value);
  if (!cleaned) return "";
  const roots = uniqueTokens([
    siteRunsPrefix(),
    ...(Array.isArray(state.info?.run_roots) ? state.info.run_roots : []),
  ].map((token) => normalizePathString(token)));
  for (const base of roots) {
    if (!base) continue;
    if (cleaned === base) return "";
    if (cleaned.startsWith(`${base}/`)) return cleaned.slice(base.length + 1);
  }
  return cleaned;
}

function inferRunRelFromPayload(payload) {
  if (!payload) return "";
  if (payload.run) {
    const rel = stripSiteRunsPrefix(payload.run);
    return rel || payload.run;
  }
  if (payload.output) {
    const rel = stripSiteRunsPrefix(payload.output);
    if (!rel) return "";
    return rel.replace(/\/[^/]+$/, "");
  }
  return "";
}

function formatRunRoots(runRoots) {
  if (!runRoots || runRoots.length === 0) return "-";
  const base = normalizePathString(siteRunsPrefix());
  const normalized = runRoots.map((root) => {
    const cleaned = normalizePathString(root);
    return cleaned === base ? "." : root;
  });
  if (normalized.length === 1 && normalized[0] === ".") return ".";
  return normalized.join(", ");
}

function runBaseName(runRel) {
  if (!runRel) return "run";
  const parts = runRel.split(/[\\/]/).filter(Boolean);
  return parts[parts.length - 1] || "run";
}

function findRunSummary(runRel) {
  const normalized = normalizePathString(runRel || "");
  if (!normalized) return null;
  const list = Array.isArray(state.runs) ? state.runs : [];
  return list.find((item) => normalizePathString(item?.run_rel || "") === normalized) || null;
}

function syncRunSelectionHint() {
  const hint = $("#federlicht-run-hint");
  const display = $("#federlicht-run-display");
  if (!hint) return;
  const runRel = normalizePathString($("#run-select")?.value || "");
  if (!runRel) {
    hint.textContent = "선택된 run: -";
    hint.removeAttribute("title");
    if (display) {
      display.value = "";
      display.removeAttribute("title");
    }
    return;
  }
  const summary = findRunSummary(runRel);
  const runLabel = stripSiteRunsPrefix(runRel) || runRel;
  const reportLabel = String(summary?.latest_report_name || "").trim();
  const textParts = [`선택된 run: ${runLabel}`];
  if (reportLabel) textParts.push(`report: ${reportLabel}`);
  if (summary?.updated_at) textParts.push(`updated: ${formatDate(summary.updated_at)}`);
  const titleParts = [runRel];
  if (summary?.latest_report_rel) titleParts.push(`report: ${summary.latest_report_rel}`);
  if (summary?.latest_report_name && !summary?.latest_report_rel) titleParts.push(`report: ${summary.latest_report_name}`);
  if (summary?.updated_at) titleParts.push(`updated: ${formatDate(summary.updated_at)}`);
  hint.textContent = textParts.join(" | ");
  hint.setAttribute("title", titleParts.join("\n"));
  if (display) {
    display.value = runRel;
    display.setAttribute("title", runRel);
  }
}

function inferRunHintFromText(text) {
  const raw = String(text || "").trim();
  if (!raw) return "";
  const patterns = [
    /(?:^|[\s([,{])run\s*(?:folder|name|폴더)?\s*(?:를|을|은|는|to|as|=|:)?\s*([^\s"'`<>|?*]{2,120})/iu,
    /(?:^|[\s([,{])output\s*(?:folder|run)?\s*(?:를|을|은|는|to|as|=|:)?\s*([^\s"'`<>|?*]{2,120})/iu,
    /([\p{L}\p{N}][\p{L}\p{N}._/-]{1,120}?)\s*(?:으로|로)\s*(?:federlicht|feather|run|실행|생성|작성|시작)/iu,
    /[`"'“”‘’]([\p{L}\p{N}][\p{L}\p{N}._/-]{1,120})[`"'“”‘’]/u,
  ];
  for (const pattern of patterns) {
    const match = raw.match(pattern);
    const token = normalizeRunHint(match?.[1] || "");
    if (!token) continue;
    if (isInvalidRunHint(token)) continue;
    const lowered = token.toLowerCase();
    if (["run", "runs", "folder", "output", "report", "federlicht", "feather", "으로", "로"].includes(lowered)) {
      continue;
    }
    return token;
  }
  return "";
}

function inferRunHintFromRecentContext() {
  const candidates = [];
  const pendingLive = String(state.liveAsk.pendingQuestion || "").trim();
  const pendingAsk = String(state.ask.pendingQuestion || "").trim();
  if (pendingLive) candidates.push(pendingLive);
  if (pendingAsk) candidates.push(pendingAsk);
  const pickRecentUserRows = (rows) => {
    const list = Array.isArray(rows) ? rows : [];
    return [...list]
      .reverse()
      .filter((entry) => entry?.role === "user" && String(entry?.content || "").trim())
      .slice(0, 4)
      .map((entry) => String(entry.content || "").trim());
  };
  candidates.push(...pickRecentUserRows(state.liveAsk.history));
  candidates.push(...pickRecentUserRows(state.ask.history));
  for (const text of candidates) {
    const hint = inferRunHintFromText(text);
    if (hint) return hint;
  }
  return "";
}

function resolveActionOverrideWithRunHint(actionType, actionOverride) {
  const context = resolveAskActionContext(actionType, actionOverride);
  const explicitHint = normalizeRunHint(context?.run_hint || "");
  if (explicitHint && !isInvalidRunHint(explicitHint)) return { actionOverride, inferredRunHint: "" };
  const preflight = context?.execution_handoff?.preflight
    && typeof context.execution_handoff.preflight === "object"
    ? context.execution_handoff.preflight
    : null;
  const handoffHint = normalizeRunHint(preflight?.run_hint || preflight?.resolved_run_rel || "");
  if (handoffHint && !isInvalidRunHint(handoffHint)) {
    const mergedFromHandoff = normalizeAskActionOverride(actionType, {
      ...(context || {}),
      run_hint: handoffHint,
      create_if_missing: typeof preflight?.create_if_missing === "boolean"
        ? Boolean(preflight.create_if_missing)
        : Boolean(context?.create_if_missing),
    });
    return { actionOverride: mergedFromHandoff, inferredRunHint: handoffHint };
  }
  const inferredRunHint = inferRunHintFromRecentContext();
  if (!inferredRunHint) return { actionOverride, inferredRunHint: "" };
  const merged = normalizeAskActionOverride(actionType, {
    ...(context || {}),
    run_hint: inferredRunHint,
    create_if_missing: true,
  });
  return { actionOverride: merged, inferredRunHint };
}

function normalizeRunHint(value) {
  let token = String(value || "").trim();
  if (!token) return "";
  token = token.replaceAll("\\", "/").replace(/^["'`]+|["'`]+$/g, "");
  token = token.replace(/[.,;:!?]+$/g, "").trim();
  token = normalizePathString(token);
  if (!token) return "";
  const lowered = token.toLowerCase();
  const runRoots = Array.isArray(state.info?.run_roots) ? state.info.run_roots : [];
  const prefixes = [...new Set(
    [...runRoots, "runs", "site/runs"]
      .map((entry) => normalizePathString(entry).replace(/^\/+|\/+$/g, "").toLowerCase())
      .filter(Boolean),
  )]
    .sort((a, b) => b.length - a.length);
  for (const prefix of prefixes) {
    if (lowered === prefix) {
      token = "";
      break;
    }
    if (lowered.startsWith(`${prefix}/`)) {
      token = token.slice(prefix.length + 1);
      break;
    }
  }
  return token.replace(/^\/+|\/+$/g, "");
}

function isInvalidRunHint(value) {
  const token = normalizeRunHint(value);
  if (!token) return true;
  const lowered = token.toLowerCase();
  const merged = lowered.replace(/\s+/g, "");
  if (RUN_HINT_BLOCKED_TOKENS.has(lowered) || RUN_HINT_BLOCKED_TOKENS.has(merged)) {
    return true;
  }
  if (merged.startsWith("run") && merged.length <= 9) {
    return true;
  }
  if (merged.endsWith("대상") || merged.endsWith("대상에서")) {
    return true;
  }
  return false;
}

function analyzeRunRelHint(hint, options = {}) {
  const token = normalizeRunHint(hint);
  const strict = Boolean(options?.strict);
  if (!token) {
    return {
      token: "",
      resolved: "",
      matchedBy: "",
      ambiguous: false,
      candidates: [],
    };
  }
  const rows = Array.isArray(state.runs) ? state.runs : [];
  const dedupe = (items) => {
    const seen = new Set();
    const out = [];
    for (const item of items || []) {
      const rel = normalizePathString(item?.run_rel || "");
      if (!rel || seen.has(rel)) continue;
      seen.add(rel);
      out.push(rel);
    }
    return out;
  };
  if (!rows.length) {
    return {
      token,
      resolved: "",
      matchedBy: "",
      ambiguous: false,
      candidates: [],
    };
  }
  const loweredToken = token.toLowerCase();
  const baseToken = token.split("/").filter(Boolean).pop() || token;
  const loweredBase = baseToken.toLowerCase();
  const exact = dedupe(rows.filter((item) => normalizePathString(item?.run_rel || "").toLowerCase() === loweredToken));
  const tail = dedupe(rows.filter((item) => normalizePathString(item?.run_rel || "").toLowerCase().endsWith(`/${loweredToken}`)));
  const base = dedupe(rows.filter((item) => runBaseName(normalizePathString(item?.run_rel || "")).toLowerCase() === loweredBase));
  const contains = dedupe(rows.filter((item) => {
    const rel = normalizePathString(item?.run_rel || "").toLowerCase();
    return rel.includes(loweredBase);
  }));
  const pickOne = (items) => (items.length === 1 ? items[0] : "");
  let resolved = "";
  let matchedBy = "";
  if (pickOne(exact)) {
    resolved = pickOne(exact);
    matchedBy = "exact";
  } else if (pickOne(tail)) {
    resolved = pickOne(tail);
    matchedBy = "tail";
  } else if (pickOne(base)) {
    resolved = pickOne(base);
    matchedBy = "base";
  } else if (!strict && pickOne(contains)) {
    resolved = pickOne(contains);
    matchedBy = "contains";
  }
  const firstNonEmpty = [exact, tail, base, contains].find((items) => items.length) || [];
  const hasAmbiguousSet = [exact, tail, base].some((items) => items.length > 1)
    || contains.length > 1
    || (strict && !resolved && contains.length > 0);
  return {
    token,
    resolved,
    matchedBy,
    ambiguous: !resolved && hasAmbiguousSet,
    candidates: firstNonEmpty,
    sets: { exact, tail, base, contains },
  };
}

function resolveRunRelFromHint(hint, options = {}) {
  return analyzeRunRelHint(hint, options).resolved || "";
}

function defaultInstructionPath(runRel) {
  if (!runRel) return "";
  const base = runBaseName(runRel);
  const normalizedRun = runRel.replaceAll("\\", "/");
  return `${normalizedRun}/instruction/${base}.txt`;
}

function ensureOutputPathForRun(rawOutputPath, runRel, fallbackLeaf = "report_full.html") {
  const normalizedRun = normalizePathString(runRel || "");
  const expanded = normalizePathString(
    expandSiteRunsPath(rawOutputPath || "", { runRel: normalizedRun }),
  );
  if (!normalizedRun) return expanded;
  const leafRaw =
    (expanded ? expanded.split("/").filter(Boolean).pop() : "")
    || String(rawOutputPath || "").trim()
    || String(fallbackLeaf || "").trim()
    || "report_full.html";
  const leafNormalized = normalizePathString(leafRaw);
  const leaf = (leafNormalized ? leafNormalized.split("/").filter(Boolean).pop() : "")
    || "report_full.html";
  return normalizePathString(`${normalizedRun}/${leaf}`);
}

let reportOutputTouched = false;
let promptOutputTouched = false;
let featherOutputTouched = false;
let featherInputTouched = false;
let promptFileTouched = false;
let promptInlineTouched = false;
let federlichtOutputHintSeq = 0;

function toFederlichtOutputFieldPath(rawPath) {
  const normalized = normalizePathString(rawPath);
  if (!normalized) return "";
  return normalized.split("/").filter(Boolean).pop() || normalized;
}

async function fetchFederlichtOutputSuggestion(rawOutputPath, runRel = "") {
  const outputPath = normalizePathString(rawOutputPath);
  if (!outputPath) return null;
  const params = new URLSearchParams();
  params.set("output", outputPath);
  const normalizedRun = normalizePathString(runRel || "");
  if (normalizedRun) params.set("run", normalizedRun);
  try {
    return await fetchJSON(`/api/federlicht/output-suggestion?${params.toString()}`);
  } catch (err) {
    return null;
  }
}

async function refreshFederlichtOutputHint(options = {}) {
  const input = $("#federlicht-output");
  const hint = $("#federlicht-output-hint");
  if (!input || !hint) return null;
  const requestId = ++federlichtOutputHintSeq;
  const entered = normalizePathString(input.value || "");
  if (!entered) {
    hint.innerHTML =
      "동일 파일이 있으면 자동으로 <code>_1</code>, <code>_2</code>가 붙습니다.";
    if (!state.workflow.running && state.workflow.kind !== "federlicht") {
      state.workflow.resultPath = "";
      renderWorkflow();
    }
    return null;
  }
  const runRel = normalizePathString($("#run-select")?.value || "");
  const expanded = expandSiteRunsPath(entered, { runRel });
  const suggestion = await fetchFederlichtOutputSuggestion(expanded, runRel);
  if (requestId !== federlichtOutputHintSeq) return suggestion;
  if (!suggestion) {
    hint.innerHTML =
      "출력 파일명을 확인할 수 없습니다. 실행 시 충돌이 있으면 자동으로 접미사가 붙습니다.";
    return null;
  }
  const requestedField = toFederlichtOutputFieldPath(suggestion.requested_output || expanded);
  const suggestedField = toFederlichtOutputFieldPath(suggestion.suggested_output || expanded);
  const changed = Boolean(suggestion.changed) && requestedField !== suggestedField;
  if (changed) {
    hint.innerHTML = `이미 존재: 실행 시 <code>${escapeHtml(
      suggestedField,
    )}</code> 로 저장됩니다.`;
  } else {
    hint.innerHTML = `예정 출력: <code>${escapeHtml(suggestedField)}</code>`;
  }
  if (options.applyToInput && suggestedField) {
    input.value = suggestedField;
    reportOutputTouched = true;
  }
  if (!state.workflow.running) {
    state.workflow.resultPath = normalizeWorkflowResultPath(suggestion.suggested_output || expanded);
    renderWorkflow();
  }
  return suggestion;
}

async function applyFederlichtOutputSuggestionToPayload(payload, options = {}) {
  if (!payload || !payload.output) return payload;
  const runRel = normalizePathString(payload.run || $("#run-select")?.value || "");
  const suggestion = await fetchFederlichtOutputSuggestion(payload.output, runRel);
  if (!suggestion || !suggestion.suggested_output) return payload;
  const suggested = normalizePathString(suggestion.suggested_output);
  if (!suggested) return payload;
  if (normalizePathString(payload.output) !== suggested) {
    payload.output = suggested;
    const outputFieldPath = toFederlichtOutputFieldPath(suggested);
    if (options.syncInput !== false) {
      const input = $("#federlicht-output");
      if (input) {
        input.value = outputFieldPath;
        reportOutputTouched = true;
      }
    }
    appendLog(`[federlicht] output exists; using ${outputFieldPath}\n`);
  }
  await refreshFederlichtOutputHint().catch(() => {});
  return payload;
}

function syncFieldTitle(selector) {
  const el = $(selector);
  if (!el) return;
  const value = String(el.value || "").trim();
  if (!value) {
    el.removeAttribute("title");
    return;
  }
  el.setAttribute("title", value);
}

function syncFieldPathHint(selector, hintSelector, prefix = "") {
  const hint = $(hintSelector);
  if (!hint) return;
  const el = $(selector);
  const value = String(el?.value || "").trim();
  if (!value) {
    hint.textContent = `${prefix || "path"}: -`;
    hint.removeAttribute("title");
    return;
  }
  const normalized = normalizePathString(value) || value;
  hint.textContent = `${prefix || "path"}: ${normalized}`;
  hint.setAttribute("title", normalized);
}

function syncFederlichtFieldTitles() {
  syncFieldTitle("#run-select");
  syncFieldTitle("#federlicht-output");
  syncFieldTitle("#federlicht-prompt-file");
  syncRunSelectionHint();
  syncFieldPathHint("#federlicht-prompt-file", "#federlicht-prompt-file-hint", "프롬프트 파일");
}

function refreshRunDependentFields() {
  const runRel = $("#run-select")?.value;
  const promptRunRel = $("#prompt-run-select")?.value;
  const output = $("#federlicht-output");
  const promptOutput = $("#prompt-output");
  const promptFile = $("#federlicht-prompt-file");
  if (runRel) {
    const featherOutput = normalizePathString($("#feather-output")?.value || "");
    if (!featherOutput || !featherOutputTouched) {
      syncFeatherRunTargetFields(runRel);
    }
  }
  if (runRel && output && !reportOutputTouched) {
    output.value = toFederlichtOutputFieldPath(defaultReportPath(runRel));
  }
  if (runRel && promptFile && !promptFileTouched) {
    promptFile.value = defaultPromptPath(runRel);
  }
  if (promptRunRel && promptOutput && !promptOutputTouched) {
    promptOutput.value = defaultPromptPath(promptRunRel);
  }
  if (runRel && isFederlichtActive()) {
    syncPromptFromFile(false).catch((err) => {
      if (!isMissingFileError(err)) {
        appendLog(`[prompt] failed to load: ${err}\n`);
      }
    });
  }
  refreshFederlichtOutputHint().catch(() => {});
  syncFederlichtFieldTitles();
  renderWorkflowStudioPanel();
}

function maybeReloadAskHistory() {
  ensureAskThreadScope(true);
  renderAskThreadList();
  applyLiveAskScope(state.ask.scopeKey, { force: true, fallbackHistory: state.ask.history });
  if (!state.ask.open) {
    renderAskHistory();
    return;
  }
  loadAskHistory(ensureAskRunRel()).catch((err) => {
    setAskStatus(`이력 로드 실패: ${err}`);
  });
}

function refreshRunSelectors() {
  const runSelect = $("#run-select");
  const promptRunSelect = $("#prompt-run-select");
  const instructionRunSelect = $("#instruction-run-select");
  if (!runSelect && !promptRunSelect && !instructionRunSelect) return;
  const currentRun = runSelect?.value;
  const currentPromptRun = promptRunSelect?.value;
  const currentInstructionRun = instructionRunSelect?.value;
  const options = state.runs.map(makeRunOption).join("");
  if (runSelect) runSelect.innerHTML = options;
  if (promptRunSelect) promptRunSelect.innerHTML = options;
  if (instructionRunSelect) instructionRunSelect.innerHTML = options;
  if (runSelect) ensureRunSelection(runSelect, currentRun);
  if (promptRunSelect) {
    ensureRunSelection(promptRunSelect, currentPromptRun || runSelect?.value);
    if (!promptRunSelect.value && runSelect?.value) {
      promptRunSelect.value = runSelect.value;
    }
  }
  if (instructionRunSelect) {
    ensureRunSelection(instructionRunSelect, currentInstructionRun || runSelect?.value);
    if (!instructionRunSelect.value && runSelect?.value) {
      instructionRunSelect.value = runSelect.value;
    }
  }
  refreshRunDependentFields();
}

async function loadRuns() {
  const runs = await fetchJSON("/api/runs");
  state.runs = sortRuns(runs);
  refreshRunSelectors();
  renderWorkflowStudioPanel();
  updateHeroStats();
  renderRunHistory();
  const runRel = selectedRunRel();
  if (runRel) {
    await updateRunStudio(runRel).catch((err) => {
      appendLog(`[studio] failed to update run studio: ${err}\n`);
    });
  }
  appendLog(`[runs] loaded ${state.runs.length} run folders\n`);
}

function selectedRunRel() {
  return $("#run-select")?.value || "";
}

function setStudioMeta(runRel, updatedAt) {
  setText("#studio-run-rel", runRel || "-");
  setText("#studio-updated", updatedAt ? `updated ${formatDate(updatedAt)}` : "-");
}

function updateFilePreviewState(patch) {
  state.filePreview = { ...state.filePreview, ...patch };
  renderFilePreview();
}

function revokePreviewObjectUrl() {
  if (state.filePreview.objectUrl) {
    URL.revokeObjectURL(state.filePreview.objectUrl);
  }
}

function canSaveReadOnlyPreviewAsCopy() {
  const mode = String(state.filePreview.mode || "text").toLowerCase();
  if (state.filePreview.canEdit) return false;
  if (mode !== "text") return false;
  return Boolean(String(state.filePreview.content || "").trim().length);
}

function renderFilePreview() {
  const pathEl = $("#file-preview-path");
  const statusEl = $("#file-preview-status");
  const editor = $("#file-preview-editor");
  const markdown = $("#file-preview-markdown");
  const frame = $("#file-preview-frame");
  const image = $("#file-preview-image");
  const saveBtn = $("#file-preview-save");
  const downloadBtn = $("#file-preview-saveas");
  const exportPdfBtn = $("#file-preview-export-pdf");
  const canvasBtn = $("#file-preview-canvas");
  if (pathEl) pathEl.textContent = state.filePreview.path || "No file selected";
  if (statusEl) {
    if (!state.filePreview.canEdit) {
      statusEl.textContent = "read-only";
    } else {
      statusEl.textContent = state.filePreview.dirty ? "modified" : "";
    }
  }
  if (saveBtn) saveBtn.disabled = !state.filePreview.canEdit;
  if (saveBtn && canSaveReadOnlyPreviewAsCopy()) {
    saveBtn.disabled = false;
    saveBtn.title = "read-only 파일입니다. Save를 누르면 Save As로 저장합니다.";
  } else if (saveBtn) {
    saveBtn.title = state.filePreview.canEdit ? "현재 파일에 저장" : "read-only 파일은 Save가 비활성화됩니다.";
  }
  if (downloadBtn) {
    const hasPath = Boolean(String(state.filePreview.path || "").trim());
    const hasInline =
      Boolean(String(state.filePreview.content || "").length)
      || Boolean(String(state.filePreview.htmlDoc || "").length);
    downloadBtn.disabled = !(hasPath || hasInline);
    if (exportPdfBtn) exportPdfBtn.disabled = !(hasPath || hasInline);
  } else if (exportPdfBtn) {
    const hasPath = Boolean(String(state.filePreview.path || "").trim());
    const hasInline =
      Boolean(String(state.filePreview.content || "").length)
      || Boolean(String(state.filePreview.htmlDoc || "").length);
    exportPdfBtn.disabled = !(hasPath || hasInline);
  }
  if (canvasBtn) {
    const mode = state.filePreview.mode || "text";
    const canCanvas =
      !!state.filePreview.path && (mode === "html" || mode === "markdown" || mode === "text");
    canvasBtn.disabled = !canCanvas;
  }
  if (!editor || !markdown || !frame || !image) return;
  const mode = state.filePreview.mode || "text";
  editor.style.display = "none";
  markdown.style.display = "none";
  frame.style.display = "none";
  image.style.display = "none";
  if (mode === "markdown") {
    setRenderedMarkdown(markdown, state.filePreview.content || "");
    markdown.style.display = "block";
  } else if (mode === "html" || mode === "pdf") {
    frame.removeAttribute("srcdoc");
    if (state.filePreview.htmlDoc && mode === "html") {
      frame.removeAttribute("src");
      frame.srcdoc = state.filePreview.htmlDoc;
    } else {
      frame.src = rawFileUrl(state.filePreview.path);
    }
    frame.style.display = "block";
  } else if (mode === "image") {
    image.src = rawFileUrl(state.filePreview.path);
    image.style.display = "block";
  } else if (mode === "binary") {
    markdown.innerHTML =
      "<p><strong>Unsupported preview format.</strong> Use Open to download or open the file in another app.</p>";
    markdown.style.display = "block";
  } else {
    editor.value = state.filePreview.content || "";
    editor.readOnly = !state.filePreview.canEdit;
    editor.wrap = "soft";
    editor.style.display = "block";
  }
}

function appendTemplateGenLog(text) {
  const el = $("#template-gen-log");
  if (!el) return;
  const line = String(text || "");
  state.templateGen.log = (state.templateGen.log + line).slice(-4000);
  el.textContent = state.templateGen.log || "Ready.";
  el.scrollTop = el.scrollHeight;
}

function renderMarkdown(text) {
  const lines = String(text || "").replace(/\r\n/g, "\n").split("\n");
  let html = "";
  let inList = false;
  let listTag = "ul";
  let inCode = false;
  let codeLang = "";
  let codeBuffer = [];
  let fenceToken = "";
  let inTable = false;
  const closeList = () => {
    if (!inList) return;
    html += `</${listTag}>`;
    inList = false;
    listTag = "ul";
  };
  const closeTable = () => {
    if (!inTable) return;
    html += "</tbody></table>";
    inTable = false;
  };
  const closeCode = () => {
    if (!inCode) return;
    const body = codeBuffer.join("\n");
    if (codeLang === "mermaid") {
      html += `<div class="md-mermaid" data-mermaid-source="${encodeURIComponent(body)}"><pre><code class="language-mermaid">${escapeHtml(body)}</code></pre></div>`;
    } else if ((codeLang === "markdown" || codeLang === "md") && /(^|\n)\|.*\|/.test(body)) {
      // Some LLM replies wrap markdown tables in ```markdown fences. Render table-friendly markdown instead of raw code.
      html += `<div class="md-fenced-markdown">${renderMarkdown(body)}</div>`;
    } else {
      const langClass = codeLang ? ` class="language-${escapeHtml(codeLang)}"` : "";
      html += `<pre><code${langClass}>${escapeHtml(body)}</code></pre>`;
    }
    inCode = false;
    codeLang = "";
    codeBuffer = [];
    fenceToken = "";
  };
  const parseTableCells = (value) => {
    const trimmed = value.trim().replace(/^\|/, "").replace(/\|$/, "");
    return trimmed.split("|").map((cell) => inline(cell.trim()));
  };
  const parseTabTableCells = (value) => String(value || "")
    .split("\t")
    .map((cell) => inline(String(cell || "").trim()));
  const tabTableColumnCount = (value) => String(value || "")
    .split("\t")
    .map((cell) => String(cell || "").trim())
    .filter(Boolean)
    .length;
  const isTabTableRow = (value) => tabTableColumnCount(value) >= 2;
  const parseSpaceTableCells = (value) => String(value || "")
    .trim()
    .split(/\s{2,}/)
    .map((cell) => inline(String(cell || "").trim()));
  const spaceTableColumnCount = (value) => String(value || "")
    .trim()
    .split(/\s{2,}/)
    .map((cell) => String(cell || "").trim())
    .filter(Boolean)
    .length;
  const isSpaceTableRow = (value) => /\s{2,}/.test(String(value || "").trim()) && spaceTableColumnCount(value) >= 2;
  const isTableSeparator = (value) => /^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$/.test(value.trim());
  const inline = (value) => {
    const rawValue = String(value ?? "");
    if (!/[`*_#[\]()]/.test(rawValue)) {
      return renderRawLineWithLinks(rawValue);
    }
    let out = escapeHtml(rawValue);
    out = out.replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g, (match, altRaw, href) => {
      const alt = String(altRaw || "").trim();
      const rawHref = String(href || "").trim();
      if (!rawHref) return match;
      const decodedHref = (() => {
        try {
          return decodeURIComponent(rawHref);
        } catch (err) {
          return rawHref;
        }
      })();
      if (/^https?:\/\//i.test(decodedHref)) {
        return `<figure class="md-inline-figure"><img class="md-inline-image" src="${escapeHtml(decodedHref)}" alt="${escapeHtml(alt)}" loading="lazy" /></figure>`;
      }
      const normalizedPath = normalizeLogPathCandidate(decodedHref);
      if (!normalizedPath || !/\.(png|jpe?g|gif|svg|webp|bmp)$/i.test(normalizedPath)) {
        return match;
      }
      return `<figure class="md-inline-figure"><a href="#" class="log-link md-inline-image-link" data-log-path="${escapeHtml(
        normalizedPath,
      )}" title="Open in File Preview"><img class="md-inline-image" src="${escapeHtml(
        apiRawUrl(normalizedPath),
      )}" alt="${escapeHtml(alt || normalizedPath)}" loading="lazy" /></a></figure>`;
    });
    out = out.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (match, label, href) => {
      const safeLabel = String(label || "");
      const rawHref = String(href || "").trim();
      if (!rawHref) return safeLabel;
      const decodedHref = (() => {
        try {
          return decodeURIComponent(rawHref);
        } catch (err) {
          return rawHref;
        }
      })();
      if (/^https?:\/\//i.test(decodedHref)) {
        return `<a href="${decodedHref}" class="log-link" data-log-url="${decodedHref}" target="_blank" rel="noopener noreferrer">${safeLabel}</a>`;
      }
      const lineRangeMatch = String(decodedHref || "").match(/:(\d+)(?:-(\d+)|:(\d+))?$/);
      const lineStart = Number(lineRangeMatch?.[1] || 0);
      const lineEnd = Number(lineRangeMatch?.[2] || lineRangeMatch?.[3] || lineRangeMatch?.[1] || 0);
      const normalizedPath = normalizeLogPathCandidate(decodedHref);
      if (isLikelyPreviewFilePath(normalizedPath)) {
        return `<a href="#" class="log-link" data-log-path="${escapeHtml(
          normalizedPath,
        )}" data-log-start="${lineStart > 0 ? lineStart : ""}" data-log-end="${
          lineEnd > 0 ? lineEnd : ""
        }" title="Open in File Preview">${safeLabel}</a>`;
      }
      return match;
    });
    out = out.replace(/`([^`]+)`/g, "<code>$1</code>");
    out = out.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    out = out.replace(/\*([^*]+)\*/g, "<em>$1</em>");
    return out;
  };
  for (let i = 0; i < lines.length; i += 1) {
    const raw = lines[i];
    const line = raw.trimEnd();
    const lineTrim = raw.trim();
    const fenceMatch = lineTrim.match(/^(```+|~~~+)(.*)$/);
    if (fenceMatch) {
      const token = fenceMatch[1] || "```";
      const fenceLang = String(fenceMatch[2] || "").trim().split(/\s+/)[0]?.toLowerCase() || "";
      if (!inCode) {
        closeList();
        closeTable();
        inCode = true;
        fenceToken = token;
        codeLang = fenceLang;
        codeBuffer = [];
      } else {
        if (!fenceToken || token.startsWith(fenceToken[0])) {
          closeCode();
        } else {
          codeBuffer.push(raw);
        }
      }
      continue;
    }
    if (inCode) {
      codeBuffer.push(raw);
      continue;
    }
    if (!line) {
      closeList();
      closeTable();
      continue;
    }
    if (!inTable && isTabTableRow(raw)) {
      const baseCols = tabTableColumnCount(raw);
      const rows = [raw];
      let cursor = i + 1;
      while (cursor < lines.length) {
        const candidate = String(lines[cursor] || "");
        if (!isTabTableRow(candidate)) break;
        const cols = tabTableColumnCount(candidate);
        if (cols < 2 || cols !== baseCols) break;
        rows.push(candidate);
        cursor += 1;
      }
      if (rows.length >= 2) {
        closeList();
        closeTable();
        const headerCells = parseTabTableCells(rows[0]);
        html += "<table><thead><tr>";
        headerCells.forEach((cell) => {
          html += `<th>${cell}</th>`;
        });
        html += "</tr></thead><tbody>";
        rows.slice(1).forEach((row) => {
          const rowCells = parseTabTableCells(row);
          html += "<tr>";
          rowCells.forEach((cell) => {
            html += `<td>${cell}</td>`;
          });
          html += "</tr>";
        });
        html += "</tbody></table>";
        i = cursor - 1;
        continue;
      }
    }
    if (!inTable && isSpaceTableRow(raw)) {
      const baseCols = spaceTableColumnCount(raw);
      const rows = [raw];
      let cursor = i + 1;
      while (cursor < lines.length) {
        const candidate = String(lines[cursor] || "");
        if (!isSpaceTableRow(candidate)) break;
        const cols = spaceTableColumnCount(candidate);
        if (cols < 2 || cols !== baseCols) break;
        rows.push(candidate);
        cursor += 1;
      }
      if (rows.length >= 2) {
        closeList();
        closeTable();
        const headerCells = parseSpaceTableCells(rows[0]);
        html += "<table><thead><tr>";
        headerCells.forEach((cell) => {
          html += `<th>${cell}</th>`;
        });
        html += "</tr></thead><tbody>";
        rows.slice(1).forEach((row) => {
          const rowCells = parseSpaceTableCells(row);
          html += "<tr>";
          rowCells.forEach((cell) => {
            html += `<td>${cell}</td>`;
          });
          html += "</tr>";
        });
        html += "</tbody></table>";
        i = cursor - 1;
        continue;
      }
    }
    if (line.includes("|")) {
      const next = i + 1 < lines.length ? String(lines[i + 1] || "").trim() : "";
      if (!inTable && next && isTableSeparator(next)) {
        closeList();
        const headerCells = parseTableCells(line);
        html += "<table><thead><tr>";
        headerCells.forEach((cell) => {
          html += `<th>${cell}</th>`;
        });
        html += "</tr></thead><tbody>";
        inTable = true;
        i += 1;
        continue;
      }
      if (inTable) {
        const rowCells = parseTableCells(line);
        html += "<tr>";
        rowCells.forEach((cell) => {
          html += `<td>${cell}</td>`;
        });
        html += "</tr>";
        continue;
      }
    } else {
      closeTable();
    }
    if (line.startsWith("#")) {
      closeList();
      closeTable();
      const level = Math.min(line.match(/^#+/)[0].length, 3);
      const text = line.replace(/^#+\s*/, "");
      html += `<h${level}>${inline(text)}</h${level}>`;
      continue;
    }
    const unorderedMatch = line.match(/^[-*]\s+(.+)$/);
    const orderedMatch = line.match(/^\d+\.\s+(.+)$/);
    if (unorderedMatch || orderedMatch) {
      const nextTag = orderedMatch ? "ol" : "ul";
      const payload = orderedMatch ? orderedMatch[1] : unorderedMatch[1];
      if (!inList || listTag !== nextTag) {
        closeList();
        html += `<${nextTag}>`;
        inList = true;
        listTag = nextTag;
      }
      html += `<li>${inline(payload)}</li>`;
      continue;
    }
    closeList();
    closeTable();
    html += `<p>${inline(line)}</p>`;
  }
  closeList();
  closeTable();
  if (inCode) closeCode();
  return html;
}

function decodeMermaidSource(token) {
  const raw = String(token || "");
  if (!raw) return "";
  try {
    return decodeURIComponent(raw);
  } catch (err) {
    return raw;
  }
}

function ensureMermaidLoaded() {
  if (window.mermaid && typeof window.mermaid.render === "function") {
    if (!window.__federnettMermaidConfigured) {
      window.mermaid.initialize({
        startOnLoad: false,
        securityLevel: "loose",
        theme: "dark",
      });
      window.__federnettMermaidConfigured = true;
    }
    mermaidState.ready = true;
    return Promise.resolve(window.mermaid);
  }
  if (mermaidState.loading) return mermaidState.loading;
  mermaidState.loading = new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = MERMAID_CDN;
    script.async = true;
    script.onload = () => {
      if (!window.mermaid || typeof window.mermaid.render !== "function") {
        reject(new Error("mermaid unavailable"));
        return;
      }
      if (!window.__federnettMermaidConfigured) {
        window.mermaid.initialize({
          startOnLoad: false,
          securityLevel: "loose",
          theme: "dark",
        });
        window.__federnettMermaidConfigured = true;
      }
      mermaidState.ready = true;
      resolve(window.mermaid);
    };
    script.onerror = () => {
      mermaidState.loading = null;
      mermaidState.ready = false;
      reject(new Error("failed to load mermaid"));
    };
    document.head.appendChild(script);
  });
  return mermaidState.loading;
}

async function renderMermaidBlocks(host, token = "") {
  if (!host) return;
  const blocks = Array.from(host.querySelectorAll(".md-mermaid[data-mermaid-source]"));
  if (!blocks.length) return;
  let mermaid;
  try {
    mermaid = await ensureMermaidLoaded();
  } catch (err) {
    return;
  }
  if (!mermaid || typeof mermaid.render !== "function") return;
  for (let idx = 0; idx < blocks.length; idx += 1) {
    if (!host.isConnected) return;
    if (token && host instanceof HTMLElement && host.dataset.mdToken !== token) return;
    const block = blocks[idx];
    if (!(block instanceof HTMLElement)) continue;
    const source = decodeMermaidSource(block.getAttribute("data-mermaid-source")).trim();
    if (!source) continue;
    const renderId = `federnett-mermaid-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}-${idx}`;
    try {
      const rendered = await mermaid.render(renderId, source);
      const svg = typeof rendered === "string" ? rendered : rendered?.svg;
      if (svg) {
        block.innerHTML = `<div class="md-mermaid-svg">${svg}</div>`;
        block.setAttribute("data-mermaid-rendered", "true");
      }
    } catch (err) {
      block.setAttribute("data-mermaid-error", "true");
    }
  }
}

function setRenderedMarkdown(host, markdownText) {
  if (!host) return;
  const token = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  if (host instanceof HTMLElement) host.dataset.mdToken = token;
  host.innerHTML = renderMarkdown(markdownText);
  renderMermaidBlocks(host, token).catch(() => {});
}

function hydrateMarkdownBlocks(root) {
  if (!(root instanceof Element)) return;
  root.querySelectorAll(".ask-message-body, .live-ask-message-body").forEach((el) => {
    if (!(el instanceof HTMLElement)) return;
    if (!el.querySelector(".md-mermaid[data-mermaid-source]")) return;
    const token = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
    el.dataset.mdToken = token;
    renderMermaidBlocks(el, token).catch(() => {});
  });
}

function previewModeForPath(relPath) {
  const lower = String(relPath || "").toLowerCase();
  if (lower.endsWith(".pdf")) return "pdf";
  if (lower.endsWith(".html") || lower.endsWith(".htm")) return "html";
  if (lower.endsWith(".md")) return "markdown";
  if (lower.match(/\.(png|jpg|jpeg|gif|svg)$/)) return "image";
  if (isTextPreviewable(relPath)) return "text";
  return "binary";
}

async function fetchRawPreviewBlob(relPath) {
  const res = await fetch(apiRawUrl(relPath));
  const contentType = res.headers.get("content-type") || "";
  if (!res.ok) {
    let detail = `${res.status} ${res.statusText}`;
    if (contentType.includes("application/json")) {
      try {
        const payload = await res.json();
        if (payload?.error) detail = payload.error;
      } catch (err) {
        // ignore
      }
    }
    throw new Error(detail);
  }
  if (contentType.includes("application/json")) {
    const payload = await res.json();
    throw new Error(payload?.error || "unknown_endpoint");
  }
  const blob = await res.blob();
  return { blob, contentType };
}

function focusFilePreviewLines(startLine, endLine) {
  const editor = $("#file-preview-editor");
  if (!editor || editor.style.display === "none") return;
  const lines = String(editor.value || "").replace(/\r\n/g, "\n").split("\n");
  const start = Math.max(1, Number(startLine) || 1);
  const end = Math.max(start, Number(endLine) || start);
  let startOffset = 0;
  for (let i = 0; i < start - 1 && i < lines.length; i += 1) {
    startOffset += lines[i].length + 1;
  }
  let endOffset = startOffset;
  for (let i = start - 1; i < end && i < lines.length; i += 1) {
    endOffset += lines[i].length;
    if (i < lines.length - 1) endOffset += 1;
  }
  try {
    editor.focus();
    editor.setSelectionRange(startOffset, Math.max(startOffset, endOffset));
  } catch (err) {
    // no-op
  }
  const lineHeight = Number.parseFloat(getComputedStyle(editor).lineHeight) || 20;
  editor.scrollTop = Math.max((start - 3) * lineHeight, 0);
}

function scheduleFilePreviewLineFocus(startLine, endLine) {
  if (!startLine || Number(startLine) < 1) return;
  window.requestAnimationFrame(() => {
    window.requestAnimationFrame(() => {
      focusFilePreviewLines(startLine, endLine);
    });
  });
}

async function loadFilePreview(relPath, options = {}) {
  if (!relPath) return;
  revokePreviewObjectUrl();
  const requestedLine = Number(options.focusLine || 0);
  const requestedEndLine = Number(options.endLine || requestedLine || 0);
  const forceReadOnly = Boolean(options.readOnly || options.forceReadOnly);
  const shouldFocusPreview = options.focusPanel !== false;
  const originalMode = previewModeForPath(relPath);
  const mode = originalMode;
  if (mode === "pdf" || mode === "html" || mode === "image") {
    updateFilePreviewState({
      path: relPath,
      content: "",
      canEdit: false,
      dirty: false,
      mode,
      objectUrl: "",
      htmlDoc: "",
    });
    setPreviewPopupOpen(true, { focus: shouldFocusPreview });
    return;
  }
  if (mode === "binary") {
    try {
      const data = await fetchJSON(`/api/files?path=${encodeURIComponent(relPath)}`);
      updateFilePreviewState({
        path: data.path || relPath,
        content: data.content || "",
        canEdit: false,
        dirty: false,
        mode: "text",
        objectUrl: "",
        htmlDoc: "",
      });
      setPreviewPopupOpen(true, { focus: shouldFocusPreview });
      if (requestedLine > 0) {
        scheduleFilePreviewLineFocus(requestedLine, requestedEndLine);
      }
      return;
    } catch (err) {
      updateFilePreviewState({
        path: relPath,
        content: `파일을 텍스트로 미리보기할 수 없습니다: ${err}`,
        canEdit: false,
        dirty: false,
        mode: "text",
        objectUrl: "",
        htmlDoc: "",
      });
      setPreviewPopupOpen(true, { focus: shouldFocusPreview });
      return;
    }
  }
  try {
    const data = await fetchJSON(`/api/files?path=${encodeURIComponent(relPath)}`);
    const canEdit = originalMode === "text" && !forceReadOnly;
    updateFilePreviewState({
      path: data.path || relPath,
      content: data.content || "",
      canEdit,
      dirty: false,
      mode,
      objectUrl: "",
      htmlDoc: "",
    });
    setPreviewPopupOpen(true, { focus: shouldFocusPreview });
    if (requestedLine > 0) {
      scheduleFilePreviewLineFocus(requestedLine, requestedEndLine);
    }
  } catch (err) {
    updateFilePreviewState({
      path: relPath,
      content: `Failed to load file: ${err}`,
      canEdit: false,
      dirty: false,
      mode: "text",
      objectUrl: "",
      htmlDoc: "",
    });
    setPreviewPopupOpen(true, { focus: shouldFocusPreview });
  }
}

function stripRunPrefix(pathValue, runRel) {
  const cleaned = normalizePathString(pathValue);
  const runPath = normalizePathString(runRel);
  if (runPath && cleaned.startsWith(`${runPath}/`)) {
    return cleaned.slice(runPath.length + 1);
  }
  return cleaned;
}

function inferRunRelFromPath(relPath) {
  const cleaned = normalizePathString(relPath);
  const runRoots = state.info?.run_roots || [];
  for (const root of runRoots) {
    const prefix = normalizePathString(root);
    if (!prefix) continue;
    if (cleaned.startsWith(`${prefix}/`)) {
      const rest = cleaned.slice(prefix.length + 1);
      const head = rest.split("/")[0];
      if (head) return `${prefix}/${head}`;
    }
  }
  return selectedRunRel();
}

function extractTextFromHtml(html) {
  const temp = document.createElement("div");
  temp.innerHTML = html || "";
  let text = temp.textContent || "";
  text = text.replace(/\r\n/g, "\n").replace(/\n{3,}/g, "\n\n").trim();
  return text;
}

function truncateSelection(text, maxChars = 4000) {
  if (!text) return "";
  if (text.length <= maxChars) return text;
  return `${text.slice(0, maxChars - 1)}…`;
}

function guessNextReportPathFromBase(basePath) {
  if (!basePath) return "";
  const cleaned = normalizePathString(basePath);
  const match = cleaned.match(/^(.*\/)?report_full(?:_(\d+))?\.html$/);
  if (!match) return "";
  const prefix = match[1] || "";
  const idx = Number.parseInt(match[2] || "0", 10);
  const next = Number.isFinite(idx) ? idx + 1 : 1;
  return `${prefix}report_full_${next}.html`;
}

function setCanvasStatus(text) {
  const el = $("#canvas-status");
  if (el) el.textContent = text || "";
}

function updateCanvasFields() {
  const baseInput = $("#canvas-base-path");
  const outputInput = $("#canvas-output-path");
  const updatePathInput = $("#canvas-update-path");
  const selection = $("#canvas-selection");
  const textArea = $("#canvas-report-text");
  const runPill = $("#canvas-run-rel");
  const basePill = $("#canvas-base-rel");
  const frame = $("#canvas-preview-frame");
  if (baseInput) baseInput.value = state.canvas.basePath || "";
  if (outputInput && state.canvas.outputPath) outputInput.value = state.canvas.outputPath;
  if (updatePathInput && state.canvas.updatePath) updatePathInput.value = state.canvas.updatePath;
  if (selection) selection.value = state.canvas.selection || "";
  if (textArea) textArea.value = state.canvas.reportText || "";
  if (runPill) runPill.textContent = state.canvas.runRel ? `run: ${state.canvas.runRel}` : "-";
  if (basePill) {
    basePill.textContent = state.canvas.baseRel ? `base: ${state.canvas.baseRel}` : "-";
  }
  if (frame && state.canvas.basePath) {
    frame.src = rawFileUrl(state.canvas.basePath);
  }
}

async function loadCanvasReport(relPath) {
  if (!relPath) return;
  setCanvasStatus("Loading report...");
  try {
    const data = await fetchJSON(`/api/files?path=${encodeURIComponent(relPath)}`);
    const content = data.content || "";
    const mode = previewModeForPath(relPath);
    let text = content;
    if (mode === "html") {
      text = extractTextFromHtml(content);
    }
    state.canvas.reportText = text;
    state.canvas.reportHtml = content;
    updateCanvasFields();
    setCanvasStatus("Ready");
  } catch (err) {
    setCanvasStatus(`Failed to load report: ${err}`);
  }
}

async function nextUpdateRequestPath(runRel) {
  if (!runRel) return "";
  const now = new Date();
  const stamp = `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, "0")}${String(
    now.getDate(),
  ).padStart(2, "0")}`;
  const dir = joinPath(runRel, "report_notes");
  let existing = [];
  try {
    const listing = await fetchJSON(`/api/fs?path=${encodeURIComponent(dir)}`);
    existing = (listing.entries || []).map((entry) => entry.name);
  } catch (err) {
    existing = [];
  }
  let name = `update_request_${stamp}.txt`;
  if (existing.includes(name)) {
    let idx = 1;
    while (existing.includes(`update_request_${stamp}_${idx}.txt`)) {
      idx += 1;
    }
    name = `update_request_${stamp}_${idx}.txt`;
  }
  return `${dir}/${name}`;
}

function buildUpdatePromptContent({ updateText, secondPrompt, baseRel, selection }) {
  const lines = ["Update request:"];
  if (updateText) lines.push(updateText.trim());
  if (selection) {
    lines.push("");
    lines.push("Target excerpt:");
    lines.push("<<<");
    lines.push(selection.trim());
    lines.push(">>>");
  }
  if (secondPrompt) {
    lines.push("");
    lines.push("Second prompt:");
    lines.push(secondPrompt.trim());
  }
  lines.push("");
  lines.push(`Base report: ${baseRel || ""}`);
  lines.push("");
  lines.push("Instructions:");
  lines.push("- Read the base report file and keep its structure unless the update requests a change.");
  lines.push("- Apply only the requested edits; avoid rewriting everything from scratch.");
  lines.push("- Preserve citations and update them only if you change the referenced content.");
  if (selection) {
    lines.push("- Limit edits to the target excerpt unless the update requests broader changes.");
  }
  return lines.join("\n");
}

async function openCanvasModal(relPath) {
  const modal = $("#canvas-modal");
  if (!modal) return;
  const basePath = relPath || state.filePreview.path;
  if (!basePath) {
    appendLog("[canvas] select a report file first.\n");
    return;
  }
  const runRel = inferRunRelFromPath(basePath);
  if (runRel && $("#run-select") && $("#run-select").value !== runRel) {
    $("#run-select").value = runRel;
    refreshRunDependentFields();
    await updateRunStudio(runRel).catch(() => {});
  }
  const baseRel = stripRunPrefix(basePath, runRel);
  const outputPath =
    nextReportPath(state.runSummary) ||
    guessNextReportPathFromBase(basePath) ||
    joinPath(runRel, "report_full.html");
  state.canvas = {
    ...state.canvas,
    open: true,
    runRel: runRel || "",
    basePath,
    baseRel,
    outputPath,
    selection: "",
    updatePath: "",
  };
  modal.classList.add("open");
  modal.setAttribute("aria-hidden", "false");
  setCanvasStatus("Ready");
  updateCanvasFields();
  await loadCanvasReport(basePath);
  state.canvas.updatePath = await nextUpdateRequestPath(runRel);
  updateCanvasFields();
}

function closeCanvasModal() {
  const modal = $("#canvas-modal");
  if (!modal) return;
  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");
  state.canvas.open = false;
}

function syncCanvasSelection() {
  const textArea = $("#canvas-report-text");
  if (!textArea) return;
  const start = textArea.selectionStart || 0;
  const end = textArea.selectionEnd || 0;
  if (start === end) {
    appendLog("[canvas] select text in the report area first.\n");
    return;
  }
  const raw = textArea.value.slice(start, end);
  const trimmed = truncateSelection(raw.trim());
  state.canvas.selection = trimmed;
  updateCanvasFields();
}

async function runCanvasUpdate() {
  const updateText = $("#canvas-update")?.value?.trim();
  if (!updateText) {
    appendLog("[canvas] update instructions are required.\n");
    return;
  }
  const secondPrompt = $("#canvas-second")?.value?.trim();
  const selection = $("#canvas-selection")?.value?.trim();
  const baseRel = state.canvas.baseRel || "";
  const runRel = state.canvas.runRel || selectedRunRel();
  if (!runRel) {
    appendLog("[canvas] run folder not resolved.\n");
    return;
  }
  let outputPath = $("#canvas-output-path")?.value?.trim() || state.canvas.outputPath;
  if (!outputPath) {
    outputPath = nextReportPath(state.runSummary);
  }
  if (!outputPath) {
    appendLog("[canvas] output path is required.\n");
    return;
  }
  let updatePath = $("#canvas-update-path")?.value?.trim() || state.canvas.updatePath;
  if (!updatePath) {
    updatePath = await nextUpdateRequestPath(runRel);
  }
  if (!updatePath) {
    appendLog("[canvas] update prompt path is required.\n");
    return;
  }
  const content = buildUpdatePromptContent({
    updateText,
    secondPrompt,
    baseRel,
    selection,
  });
  try {
    await fetchJSON("/api/files", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ path: updatePath, content }),
    });
    state.canvas.updatePath = updatePath;
    updateCanvasFields();
    setCanvasStatus("Update prompt saved.");
  } catch (err) {
    appendLog(`[canvas] failed to write update prompt: ${err}\n`);
    return;
  }
  const payload = buildFederlichtPayload();
  payload.run = runRel;
  payload.output = expandSiteRunsPath(outputPath);
  payload.prompt_file = expandSiteRunsPath(updatePath);
  delete payload.prompt;
  await applyFederlichtOutputSuggestionToPayload(payload, { syncInput: true });
  const cleanPayload = pruneEmpty(payload);
  setCanvasStatus("Running update...");
  await startJob("/api/federlicht/start", cleanPayload, {
    kind: "federlicht",
    onSuccess: async () => {
      await loadRuns().catch(() => {});
      if (runRel && $("#run-select")) {
        $("#run-select").value = runRel;
        refreshRunDependentFields();
        await updateRunStudio(runRel).catch(() => {});
      }
      setCanvasStatus("Update started.");
    },
    onDone: () => {
      setCanvasStatus("Ready");
    },
  });
}

async function saveFilePreview(targetPath) {
  const normalizedCurrent = normalizePathString(state.filePreview.path || "");
  const relPath = normalizePathString(targetPath || state.filePreview.path || "");
  const editor = $("#file-preview-editor");
  if (!relPath) return;
  const savingToCurrent = normalizedCurrent && relPath === normalizedCurrent;
  if (savingToCurrent && !state.filePreview.canEdit) return;
  let content = "";
  if (editor && editor.style.display !== "none") {
    content = editor.value || "";
  } else {
    content = String(state.filePreview.content || "");
  }
  const payload = { path: relPath, content };
  await fetchJSON("/api/files", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  updateFilePreviewState({ path: relPath, content, dirty: false, canEdit: true, mode: "text" });
  await loadRunSummary(selectedRunRel());
}

function runRelForFile(summary, relPath) {
  const runRel = normalizePathString(summary?.run_rel || "");
  const normalized = normalizePathString(relPath || "");
  if (!runRel || !normalized.startsWith(`${runRel}/`)) return "";
  return normalized.slice(runRel.length + 1);
}

function isRunFileDeletable(summary, relPath, groupId = "") {
  const inRun = runRelForFile(summary, relPath);
  if (!inRun) return false;
  const normalized = inRun.toLowerCase();
  if (groupId === "instruction") {
    return normalized.startsWith("instruction/");
  }
  if (groupId === "reports") {
    return /^report_full(?:_[0-9]+)?\.(html|md|tex)$/i.test(inRun);
  }
  return false;
}

async function deleteRunFile(relPath) {
  const normalized = normalizePathString(relPath);
  if (!normalized) return;
  const ok = window.confirm(`파일을 삭제할까요?\n${normalized}`);
  if (!ok) return;
  const result = await fetchJSON("/api/files/delete", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path: normalized }),
  });
  appendLog(`[files] deleted ${result?.path || normalized}\n`);
  if (normalizePathString(state.filePreview.path || "") === normalized) {
    updateFilePreviewState({
      path: "",
      content: "선택한 파일이 삭제되었습니다.",
      canEdit: false,
      dirty: false,
      mode: "text",
      objectUrl: "",
      htmlDoc: "",
    });
  }
  await loadRunSummary(selectedRunRel());
}

function renderRunFiles(summary) {
  const host = $("#run-file-list");
  if (!host) return;
  const runRelPrefix = normalizePathString(summary?.run_rel || "");
  const normalizePathEntries = (entries, { reverse = false } = {}) => {
    const mapped = (Array.isArray(entries) ? entries : [])
      .map((entry) => String(entry?.path || entry || "").trim())
      .filter(Boolean)
      .map((path) => ({ path }));
    if (reverse) mapped.reverse();
    return mapped;
  };
  const groups = [
    {
      id: "reports",
      label: "Reports",
      section: "output",
      sectionKind: "essential",
      sectionKindLabel: "필수",
      desc: "최종/중간 보고서 산출물",
      files: normalizePathEntries(summary?.report_files || [], { reverse: true }),
    },
    {
      id: "index",
      label: "Index Files",
      section: "output",
      sectionKind: "essential",
      sectionKindLabel: "필수",
      desc: "탐색/검색 인덱스 및 메타",
      files: normalizePathEntries(summary?.index_files || [], { reverse: true }),
    },
    {
      id: "instruction",
      label: "Instructions",
      section: "input",
      sectionKind: "essential",
      sectionKindLabel: "필수",
      desc: "실행 입력 프롬프트/지시문",
      files: normalizePathEntries(summary?.instruction_files || [], { reverse: true }),
    },
    {
      id: "pdf",
      label: "Archive PDFs",
      section: "evidence",
      sectionKind: "evidence",
      sectionKindLabel: "근거",
      desc: "수집된 원문 PDF",
      files: normalizePathEntries(summary?.pdf_files || []),
    },
    {
      id: "pptx",
      label: "Archive PPTX",
      section: "evidence",
      sectionKind: "evidence",
      sectionKindLabel: "근거",
      desc: "수집된 발표 자료",
      files: normalizePathEntries(summary?.pptx_files || []),
    },
    {
      id: "extract",
      label: "Web Extracts",
      section: "evidence",
      sectionKind: "evidence",
      sectionKindLabel: "근거",
      desc: "웹 추출 텍스트",
      files: normalizePathEntries(summary?.extract_files || []),
    },
    {
      id: "text",
      label: "Archive Texts",
      section: "evidence",
      sectionKind: "evidence",
      sectionKindLabel: "근거",
      desc: "아카이브 텍스트 변환본",
      files: normalizePathEntries(summary?.text_files || []),
    },
    {
      id: "jsonl",
      label: "Archive JSONL",
      section: "evidence",
      sectionKind: "evidence",
      sectionKindLabel: "근거",
      desc: "구조화 데이터/메타",
      files: normalizePathEntries(summary?.jsonl_files || []),
    },
    {
      id: "logs",
      label: "Logs",
      section: "debug",
      sectionKind: "debug",
      sectionKindLabel: "진단",
      desc: "실행 로그/오류 추적",
      files: normalizePathEntries(summary?.log_files || [], { reverse: true }),
    },
  ];
  const sectionMeta = [
    { id: "input", title: "입력 파일", desc: "실행에 필요한 instruction/prompt" },
    { id: "output", title: "결과 파일", desc: "보고서/인덱스 등 주요 산출물" },
    { id: "evidence", title: "근거/소스", desc: "아카이브 자료 및 추출물" },
    { id: "debug", title: "로그/디버그", desc: "실행 기록 및 진단 파일" },
  ];
  const activeGroups = groups.filter((group) => group.files && group.files.length);
  const hasAny = activeGroups.length > 0;
  if (!hasAny) {
    host.innerHTML = `<span class="muted">No files to preview.</span>`;
    return;
  }
  if (!["core", "evidence", "all", "essential"].includes(String(state.runFiles?.view || ""))) {
    let preferred = "core";
    try {
      const stored = String(localStorage.getItem(RUN_FILE_VIEW_KEY) || "").trim().toLowerCase();
      if (stored === "all" || stored === "evidence" || stored === "core") preferred = stored;
      if (stored === "essential") preferred = "core";
    } catch (err) {
      preferred = "core";
    }
    state.runFiles.view = preferred;
  }
  let fileView = String(state.runFiles.view || "").trim().toLowerCase();
  if (fileView === "essential") fileView = "core";
  if (!["core", "evidence", "all"].includes(fileView)) fileView = "core";
  const coreSections = new Set(["input", "output"]);
  const evidenceSections = new Set(["evidence", "debug"]);
  const scopedGroups = fileView === "all"
    ? activeGroups
    : fileView === "evidence"
      ? activeGroups.filter((group) => evidenceSections.has(group.section))
      : activeGroups.filter((group) => coreSections.has(group.section));
  const hiddenGroupCount = Math.max(0, activeGroups.length - scopedGroups.length);
  if (!state.runFiles.filterLoaded) {
    let preferred = "";
    try {
      preferred = String(localStorage.getItem(RUN_FILE_FILTER_KEY) || "");
    } catch (err) {
      preferred = "";
    }
    state.runFiles.filter = preferred;
    state.runFiles.filterLoaded = true;
  }
  const fileFilter = String(state.runFiles.filter || "").trim().toLowerCase();
  const fileMatchesFilter = (pathValue) => {
    if (!fileFilter) return true;
    const normalizedPath = normalizePathString(pathValue || "").toLowerCase();
    if (!normalizedPath) return false;
    const rel = runRelPrefix && normalizedPath.startsWith(`${runRelPrefix}/`)
      ? normalizedPath.slice(runRelPrefix.length + 1)
      : normalizedPath;
    const name = normalizedPath.split("/").pop() || normalizedPath;
    return normalizedPath.includes(fileFilter)
      || rel.includes(fileFilter)
      || name.includes(fileFilter);
  };
  const visibleGroups = scopedGroups
    .map((group) => ({
      ...group,
      files: (Array.isArray(group.files) ? group.files : []).filter((entry) =>
        fileMatchesFilter(entry?.path || "")
      ),
    }))
    .filter((group) => group.files.length > 0);
  const hiddenByFilter = fileFilter
    ? Math.max(
      0,
      scopedGroups.reduce((sum, group) => sum + (Array.isArray(group.files) ? group.files.length : 0), 0)
        - visibleGroups.reduce((sum, group) => sum + (Array.isArray(group.files) ? group.files.length : 0), 0),
    )
    : 0;

  const latestPath = (entries) => {
    const arr = normalizePathEntries(entries || []);
    if (!arr.length) return "";
    return arr[arr.length - 1]?.path || "";
  };

  const overviewRows = [
    { label: "Latest Report", path: latestPath(summary?.report_files || []) || summary?.latest_report_rel || "" },
    { label: "Latest Instruction", path: latestPath(summary?.instruction_files || []) },
    { label: "Latest Index", path: latestPath(summary?.index_files || []) },
    { label: "Latest Log", path: latestPath(summary?.log_files || []) },
  ].filter((row) => Boolean(String(row.path || "").trim()));
  const buildHierarchyRows = () => {
    const tree = new Map();
    const classifyRootFile = (name) => {
      const file = String(name || "").trim().toLowerCase();
      if (!file) return "run root";
      if (file.endsWith(".html")) return "report/html";
      if (file.endsWith("-index.md")) return "report/index";
      if (file.endsWith(".md")) return "report/markdown";
      if (file.endsWith(".txt")) {
        if (file.includes("prompt") || file.includes("instruction")) return "instruction/input";
        if (file.includes("_log")) return "logs";
        return "report/text";
      }
      if (file.endsWith(".log")) return "logs";
      return "run root";
    };
    const classifyHierarchyKey = (relPath) => {
      const normalized = normalizePathString(relPath || "");
      if (!normalized) return "run root";
      const rel = runRelPrefix && normalized.startsWith(`${runRelPrefix}/`)
        ? normalized.slice(runRelPrefix.length + 1)
        : normalized;
      const parts = rel.split("/").filter(Boolean);
      if (!parts.length) return "run root";
      if (parts.length === 1) return classifyRootFile(parts[0]);
      const head = String(parts[0] || "").trim().toLowerCase();
      if (head === "archive") {
        const child = String(parts[1] || "").trim().toLowerCase();
        if (!child) return "archive";
        if (child.endsWith(".log") || child.includes("_log")) return "logs/archive";
        if (child.endsWith(".md")) return "archive/index";
        if (child.endsWith(".jsonl")) return "archive/structured";
        return `archive/${child}`;
      }
      if (head === "report_notes") {
        const child = String(parts[1] || "").trim().toLowerCase();
        if (!child) return "report_notes";
        if (child === "cache") return "report_notes/cache";
        if (child === "tool_cache") return "report_notes/tool_cache";
        return `report_notes/${child}`;
      }
      if (head === "instruction") {
        const last = String(parts[parts.length - 1] || "").trim().toLowerCase();
        if (last.startsWith("generated_prompt_") || last.startsWith("update_request_")) {
          return "instruction/prompts";
        }
        return "instruction/input";
      }
      if (head === "report") {
        const last = String(parts[parts.length - 1] || "").trim().toLowerCase();
        if (last.endsWith(".html")) return "report/html";
        if (last.endsWith(".md")) return "report/markdown";
        if (last.endsWith(".txt")) return "report/text";
        return "report";
      }
      return head;
    };
    const hierarchyMeta = (key) => {
      if (key === "instruction/input") return { label: "필수 입력 · instruction", kind: "essential", rank: 0 };
      if (key === "instruction/prompts") return { label: "자동 생성 프롬프트", kind: "essential", rank: 1 };
      if (key === "report/html") return { label: "핵심 결과 · report/html", kind: "output", rank: 2 };
      if (key === "report/markdown") return { label: "결과 초안 · report/md", kind: "output", rank: 3 };
      if (key === "report/index") return { label: "결과 인덱스", kind: "output", rank: 4 };
      if (key === "report/text") return { label: "결과 텍스트", kind: "output", rank: 5 };
      if (key === "logs" || key === "logs/archive") return { label: "실행 로그", kind: "debug", rank: 6 };
      if (key === "archive/index") return { label: "아카이브 인덱스", kind: "support", rank: 7 };
      if (key === "archive/structured") return { label: "아카이브 구조화 데이터", kind: "support", rank: 8 };
      if (key.startsWith("archive/")) {
        return {
          label: `근거 아카이브 · ${key.slice("archive/".length)}`,
          kind: "evidence",
          rank: 9,
        };
      }
      if (key === "report_notes/cache") return { label: "보조 노트 · cache", kind: "support", rank: 10 };
      if (key === "report_notes/tool_cache") return { label: "보조 노트 · tool_cache", kind: "support", rank: 11 };
      if (key.startsWith("report_notes/")) {
        return {
          label: `보조 노트 · ${key.slice("report_notes/".length)}`,
          kind: "support",
          rank: 12,
        };
      }
      return { label: key, kind: "support", rank: 13 };
    };
    visibleGroups.forEach((group) => {
      (Array.isArray(group.files) ? group.files : []).forEach((entry) => {
        const relPath = String(entry?.path || "").trim();
        if (!relPath) return;
        const key = classifyHierarchyKey(relPath);
        tree.set(key, (tree.get(key) || 0) + 1);
      });
    });
    return Array.from(tree.entries())
      .map(([key, count]) => ({ key, count, ...hierarchyMeta(key) }))
      .sort((a, b) => a.rank - b.rank || b.count - a.count || a.label.localeCompare(b.label))
      .slice(0, 10);
  };
  const trimMiddle = (text, max = 42) => {
    const raw = String(text || "").trim();
    if (!raw || raw.length <= max) return raw;
    const keep = Math.max(8, Math.floor((max - 1) / 2));
    return `${raw.slice(0, keep)}…${raw.slice(-keep)}`;
  };
  const trimTail = (text, max = 120) => {
    const raw = String(text || "").trim();
    if (!raw || raw.length <= max) return raw;
    return `${raw.slice(0, Math.max(24, max - 1))}…`;
  };
  const sectionCounts = new Map(sectionMeta.map((section) => [section.id, 0]));
  visibleGroups.forEach((group) => {
    const current = Number(sectionCounts.get(group.section) || 0);
    sectionCounts.set(group.section, current + (Array.isArray(group.files) ? group.files.length : 0));
  });
  const relativeParent = (relPath) => {
    const normalized = normalizePathString(relPath || "");
    if (!normalized) return "";
    const parts = normalized.split("/");
    parts.pop();
    if (!parts.length) return "";
    const parent = parts.join("/");
    if (runRelPrefix && parent === runRelPrefix) {
      return "";
    }
    if (runRelPrefix && parent.startsWith(`${runRelPrefix}/`)) {
      return parent.slice(runRelPrefix.length + 1);
    }
    return parent;
  };
  const compactPathLabel = (text, max = 56) => {
    const raw = String(text || "").trim();
    if (!raw) return raw;
    return trimMiddle(raw, max);
  };
  const renderFileChip = (group, relPath) => {
    const rel = String(relPath || "").trim();
    if (!rel) return "";
    const name = trimTail(rel.split("/").pop() || rel, 58);
    const parent = compactPathLabel(relativeParent(rel), 56);
    const canDelete = isRunFileDeletable(summary, rel, group.id);
    return `
      <span class="file-chip is-rich">
        <button type="button" data-file-open="${escapeHtml(rel)}" title="${escapeHtml(rel)}">
          <span class="file-chip-name">${escapeHtml(name)}</span>
          <span class="file-chip-path">${escapeHtml(parent || "run root")}</span>
        </button>
        ${canDelete
          ? `<button type="button" class="file-chip-delete" data-file-delete="${escapeHtml(rel)}" aria-label="Delete file" title="Delete">×</button>`
          : ""}
      </span>
    `;
  };
  const renderOverview = () => {
    if (!overviewRows.length) return "";
    const hierarchyRows = buildHierarchyRows();
    const sectionSummaryRows = sectionMeta
      .map((section) => ({
        ...section,
        count: Number(sectionCounts.get(section.id) || 0),
      }))
      .filter((row) => row.count > 0);
    const requiredRows = [
      { id: "instruction", label: "Instruction", ok: activeGroups.some((group) => group.id === "instruction") },
      { id: "reports", label: "Report", ok: activeGroups.some((group) => group.id === "reports") },
      { id: "index", label: "Index", ok: activeGroups.some((group) => group.id === "index") },
    ];
    return `
      <section class="run-file-overview">
        <div class="run-file-overview-head">
          <strong>Run Map</strong>
          <span class="run-file-overview-count">${escapeHtml(String(visibleGroups.length))} groups</span>
        </div>
        <div class="run-file-required-grid" aria-label="Essential file checklist">
          ${requiredRows
      .map((row) =>
        `<span class="run-file-required-chip ${row.ok ? "is-ok" : "is-missing"}">${escapeHtml(
          `${row.label}: ${row.ok ? "ok" : "missing"}`,
        )}</span>`,
      )
      .join("")}
        </div>
        ${sectionSummaryRows.length
      ? `<div class="run-file-scope-grid">
            ${sectionSummaryRows
              .map((row) =>
                `<span class="run-file-scope-chip is-${escapeHtml(row.id)}">${escapeHtml(row.title)} · ${escapeHtml(String(row.count))}</span>`,
              )
              .join("")}
          </div>`
      : ""}
        ${hierarchyRows.length
      ? `
            <div class="run-file-tree" aria-label="Run hierarchy">
              ${hierarchyRows
          .map((item) =>
            `<button type="button" class="run-file-tree-chip is-${escapeHtml(item.kind || "support")}" data-run-folder-filter="${escapeHtml(item.key)}" title="${escapeHtml(item.key)} 필터 적용">${escapeHtml(
              `${compactPathLabel(item.label || item.key, 44)} (${item.count})`,
            )}</button>`,
          )
          .join("")}
            </div>
          `
      : ""}
        <div class="run-file-view-tools">
          <div class="run-file-view-toggle" role="group" aria-label="Run file view filter">
            <button
              type="button"
              class="ghost mini ${fileView === "core" ? "is-active" : ""}"
              data-run-file-view="core"
            >
              입력/결과
            </button>
            <button
              type="button"
              class="ghost mini ${fileView === "evidence" ? "is-active" : ""}"
              data-run-file-view="evidence"
            >
              근거/로그
            </button>
            <button
              type="button"
              class="ghost mini ${fileView === "all" ? "is-active" : ""}"
              data-run-file-view="all"
            >
              전체
            </button>
          </div>
          <label class="run-file-filter">
            <span>파일 필터</span>
            <input
              type="search"
              data-run-file-filter
              value="${escapeHtml(fileFilter)}"
              placeholder="파일명/경로 검색"
            />
          </label>
          ${fileFilter
      ? '<button type="button" class="ghost mini" data-run-file-filter-clear>필터 해제</button>'
      : ""}
        </div>
        ${fileView !== "all" && hiddenGroupCount > 0
      ? `<p class="run-file-view-note muted">현재 보기에서 제외된 ${hiddenGroupCount}개 그룹은 <strong>전체</strong> 보기에서 확인할 수 있습니다.</p>`
      : ""}
        ${fileFilter && hiddenByFilter > 0
      ? `<p class="run-file-view-note muted">필터로 ${hiddenByFilter.toLocaleString()}개 파일이 숨겨져 있습니다.</p>`
      : ""}
        <div class="run-file-overview-grid">
          ${overviewRows
            .map((row) => `
              <div class="run-file-overview-item">
                <strong>${escapeHtml(row.label)}</strong>
                <button type="button" data-file-open="${escapeHtml(row.path)}" title="${escapeHtml(row.path)}">
                  ${escapeHtml(compactPathLabel(String(row.path || ""), 96))}
                </button>
              </div>
            `)
            .join("")}
        </div>
      </section>
    `;
  };
  const bindRunFileOverviewControls = () => {
    host.querySelectorAll("button[data-run-file-view]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const next = String(btn.getAttribute("data-run-file-view") || "").trim().toLowerCase();
        if (next !== "all" && next !== "core" && next !== "evidence") return;
        state.runFiles.view = next;
        try {
          localStorage.setItem(RUN_FILE_VIEW_KEY, next);
        } catch (err) {
          // ignore storage quota/private mode failures
        }
        renderRunFiles(summary);
      });
    });
    const filterInput = host.querySelector("input[data-run-file-filter]");
    if (filterInput) {
      filterInput.addEventListener("input", () => {
        state.runFiles.filter = String(filterInput.value || "");
        try {
          localStorage.setItem(RUN_FILE_FILTER_KEY, state.runFiles.filter);
        } catch (err) {
          // ignore storage quota/private mode failures
        }
        renderRunFiles(summary);
      });
      filterInput.addEventListener("search", () => {
        state.runFiles.filter = String(filterInput.value || "");
        try {
          localStorage.setItem(RUN_FILE_FILTER_KEY, state.runFiles.filter);
        } catch (err) {
          // ignore storage quota/private mode failures
        }
        renderRunFiles(summary);
      });
    }
    host.querySelectorAll("button[data-run-folder-filter]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const token = String(btn.getAttribute("data-run-folder-filter") || "").trim();
        if (!token) return;
        state.runFiles.filter = token;
        try {
          localStorage.setItem(RUN_FILE_FILTER_KEY, state.runFiles.filter);
        } catch (err) {
          // ignore storage quota/private mode failures
        }
        renderRunFiles(summary);
      });
    });
    host.querySelectorAll("button[data-run-file-filter-clear]").forEach((btn) => {
      btn.addEventListener("click", () => {
        state.runFiles.filter = "";
        try {
          localStorage.setItem(RUN_FILE_FILTER_KEY, "");
        } catch (err) {
          // ignore storage quota/private mode failures
        }
        renderRunFiles(summary);
      });
    });
  };
  const bindRunFileOpenButtons = () => {
    host.querySelectorAll("button[data-file-open]").forEach((btn) => {
      btn.addEventListener("click", () => loadFilePreview(btn.dataset.fileOpen, { focusPanel: false }));
    });
  };
  const bindRunFileDeleteButtons = () => {
    host.querySelectorAll("button[data-file-delete]").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const relPath = btn.getAttribute("data-file-delete") || "";
        if (!relPath) return;
        try {
          await deleteRunFile(relPath);
        } catch (err) {
          appendLog(`[files] delete failed: ${err}\n`);
        }
      });
    });
  };
  if (!visibleGroups.length) {
    host.innerHTML = `
      ${renderOverview()}
      <p class="run-file-view-note muted run-file-empty-filter">
        조건에 맞는 파일이 없습니다. 필터를 지우거나 <strong>전체</strong> 보기로 전환하세요.
      </p>
    `;
    bindRunFileOpenButtons();
    bindRunFileOverviewControls();
    return;
  }
  const renderGroup = (group) => {
    const files = Array.isArray(group.files) ? group.files : [];
    const previewLimit = coreSections.has(group.section) ? 4 : 2;
    const preview = files.slice(0, previewLimit);
    const overflow = files.slice(previewLimit);
    const openByDefault = coreSections.has(group.section) ? " open" : "";
    const folderMap = new Map();
    files.forEach((file) => {
      const parent = relativeParent(file.path) || "run root";
      folderMap.set(parent, (folderMap.get(parent) || 0) + 1);
    });
    const folders = Array.from(folderMap.entries())
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .map(([path, count]) => ({ path, count }));
    const folderPreview = folders.slice(0, 3);
    const folderOverflow = Math.max(0, folders.length - folderPreview.length);
    return `
      <details class="file-group-fold" data-file-group="${escapeHtml(group.id)}"${openByDefault}>
        <summary class="file-group-summary">
          <span class="file-group-summary-left">
            <span class="file-group-kind is-${escapeHtml(group.sectionKind || "essential")}">${escapeHtml(
      group.sectionKindLabel || "필수",
    )}</span>
            <strong class="file-group-title">${escapeHtml(group.label)}</strong>
            <span class="file-group-help">${escapeHtml(group.desc || "")}</span>
          </span>
          <span class="file-group-count">${escapeHtml(String(files.length))}</span>
        </summary>
        ${folderPreview.length
      ? `
            <div class="file-group-folders" aria-label="${escapeHtml(`${group.label} folder hierarchy`)}">
              ${folderPreview
                  .map((folder) =>
            `<span class="file-group-folder-chip" title="${escapeHtml(folder.path)}">${escapeHtml(
              `${compactPathLabel(folder.path, 54)} (${folder.count})`,
            )}</span>`,
          )
                  .join("")}
              ${folderOverflow ? `<span class="file-group-folder-chip is-muted">+${folderOverflow} more</span>` : ""}
            </div>
          `
      : ""}
        <div class="file-group-items is-preview">
          ${preview.map((file) => renderFileChip(group, file.path)).join("")}
        </div>
        ${overflow.length
      ? `
            <details class="file-group-more">
              <summary>추가 ${overflow.length}개 펼치기</summary>
              <div class="file-group-items is-rest">
                ${overflow.map((file) => renderFileChip(group, file.path)).join("")}
              </div>
            </details>
          `
      : ""}
      </details>
    `;
  };
  const visibleSections = sectionMeta.filter((section) =>
    visibleGroups.some((group) => group.section === section.id)
  );
  host.innerHTML = `${renderOverview()}${visibleSections
    .map((section) => {
      const groupsInSection = visibleGroups.filter((group) => group.section === section.id);
      if (!groupsInSection.length) return "";
      const count = groupsInSection.reduce((acc, group) => acc + group.files.length, 0);
      const openByDefault = section.id === "input" || section.id === "output";
      return `
        <details class="run-file-section-fold" data-run-file-section="${escapeHtml(section.id)}"${openByDefault ? " open" : ""}>
          <summary class="run-file-section-head">
            <div>
              <strong>${escapeHtml(section.title)}</strong>
              <p>${escapeHtml(section.desc)}</p>
            </div>
            <span class="run-file-section-count">${escapeHtml(String(count))}</span>
          </summary>
          <div class="run-file-section-groups">
            ${groupsInSection.map((group) => renderGroup(group)).join("")}
          </div>
        </details>
      `;
    })
    .join("")}`;
  bindRunFileOpenButtons();
  bindRunFileOverviewControls();
  bindRunFileDeleteButtons();
}

function parseJsonlObjects(content, maxItems = 120) {
  const out = [];
  const lines = String(content || "").split(/\r?\n/);
  for (const rawLine of lines) {
    const line = String(rawLine || "").trim();
    if (!line) continue;
    try {
      const parsed = JSON.parse(line);
      if (parsed && typeof parsed === "object") {
        out.push(parsed);
      }
    } catch (err) {
      continue;
    }
    if (out.length >= maxItems) break;
  }
  return out;
}

function parseFigureSelectionIds(content) {
  const lines = String(content || "").split(/\r?\n/);
  const ids = new Set();
  lines.forEach((rawLine) => {
    const line = String(rawLine || "").trim();
    if (!line || line.startsWith("#")) return;
    const [id] = line.split("|", 1);
    const cleaned = String(id || "").trim();
    if (cleaned) ids.add(cleaned);
  });
  return ids;
}

function buildFigureSelectionText(ids) {
  const sorted = Array.from(ids).map((v) => String(v || "").trim()).filter(Boolean).sort();
  return [
    "# Add one candidate_id per line (e.g., fig-001)",
    "# Optional: add a custom caption after | (e.g., fig-001 | My caption)",
    "# Lines starting with '#' are ignored.",
    ...sorted,
    "",
  ].join("\n");
}

function figureLocationLabel(entry) {
  const asFiniteInt = (value) => {
    const num = Number.parseInt(String(value ?? "").trim(), 10);
    return Number.isFinite(num) ? num : null;
  };
  const slide = asFiniteInt(entry?.slide ?? entry?.slide_no);
  if (slide !== null) return `slide ${slide}`;
  const page = asFiniteInt(entry?.page ?? entry?.page_number ?? entry?.pdf_page);
  if (page !== null) return `p.${page}`;
  const idx = asFiniteInt(entry?.index ?? entry?.chunk_index);
  if (idx !== null) return `idx ${idx}`;
  return "";
}

function formatFigureSelectionPreview(ids) {
  const sorted = Array.from(ids).map((v) => String(v || "").trim()).filter(Boolean).sort();
  if (!sorted.length) {
    return "선택된 figure가 없습니다.";
  }
  return sorted.map((id) => `- ${id}`).join("\n");
}

async function saveFigureSelection(pathRel, ids) {
  await fetchJSON("/api/files", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path: pathRel, content: buildFigureSelectionText(ids) }),
  });
}

function setFiguresSelectPath(pathRel) {
  const input = $("#federlicht-figures-select");
  if (!input || !pathRel) return;
  input.value = pathRel;
}

async function renderRunFigureTools(summary) {
  const host = $("#run-figure-tools");
  if (!host) return;
  host.classList.add("is-empty");
  host.innerHTML = "";
  const runRel = normalizePathString(summary?.run_rel || "");
  if (!runRel) return;
  const candidatesPath = `${runRel}/report_notes/figures_candidates.jsonl`;
  const selectedPath = `${runRel}/report_notes/figures_selected.txt`;
  const previewPath = `${runRel}/report_views/figures_preview.html`;
  const listDirEntries = async (dirPath) => {
    try {
      const payload = await fetchJSON(`/api/fs?path=${encodeURIComponent(dirPath)}`);
      const entries = Array.isArray(payload?.entries) ? payload.entries : [];
      const files = new Set(
        entries
          .filter((entry) => String(entry?.type || "").toLowerCase() === "file")
          .map((entry) => String(entry?.name || "").trim())
          .filter(Boolean),
      );
      const dirs = new Set(
        entries
          .filter((entry) => String(entry?.type || "").toLowerCase() === "dir")
          .map((entry) => String(entry?.name || "").trim())
          .filter(Boolean),
      );
      return { files, dirs };
    } catch (err) {
      return { files: new Set(), dirs: new Set() };
    }
  };
  const runRootEntries = await listDirEntries(runRel);
  const hasReportNotes = runRootEntries.dirs.has("report_notes");
  const hasReportViews = runRootEntries.dirs.has("report_views");
  const reportNotesFiles = hasReportNotes
    ? (await listDirEntries(`${runRel}/report_notes`)).files
    : new Set();
  const reportViewsFiles = hasReportViews
    ? (await listDirEntries(`${runRel}/report_views`)).files
    : new Set();
  const candidatesExists = reportNotesFiles.has("figures_candidates.jsonl");
  let selectedExists = reportNotesFiles.has("figures_selected.txt");
  const previewExists = reportViewsFiles.has("figures_preview.html");
  let candidates = [];
  if (candidatesExists) {
    try {
      const payload = await fetchJSON(`/api/files?path=${encodeURIComponent(candidatesPath)}`);
      candidates = parseJsonlObjects(payload?.content || "", 48);
    } catch (err) {
      candidates = [];
    }
  }
  let selectedIds = new Set();
  if (selectedExists) {
    try {
      const payload = await fetchJSON(`/api/files?path=${encodeURIComponent(selectedPath)}`);
      selectedIds = parseFigureSelectionIds(payload?.content || "");
    } catch (err) {
      selectedIds = new Set();
      selectedExists = false;
    }
  }
  if (!candidates.length && !previewExists && !selectedExists) {
    return;
  }
  const chips = candidates
    .map((entry) => {
      const id = String(entry?.candidate_id || "").trim();
      if (!id) return "";
      const source = String(entry?.source_file || entry?.pdf_path || entry?.pptx_path || "").trim();
      const sourceTail = source ? source.split("/").pop() : "";
      const locationLabel = figureLocationLabel(entry);
      const pageLabel = locationLabel ? ` · ${locationLabel}` : "";
      const recommended = String(entry?.vision_recommended || "").trim().toLowerCase() === "true";
      const selected = selectedIds.has(id) ? "is-selected" : "";
      const label = `${recommended ? "★ " : ""}${id}${sourceTail ? ` · ${sourceTail}` : ""}${pageLabel}`;
      const imagePath = normalizePathString(entry?.image_path || "");
      const title = [source || id, locationLabel ? `location: ${locationLabel}` : ""]
        .filter(Boolean)
        .join("\n");
      return `<button
        type="button"
        class="run-figure-chip ${selected}"
        data-figure-id="${escapeHtml(id)}"
        data-figure-image="${escapeHtml(imagePath)}"
        data-figure-source="${escapeHtml(sourceTail || source || "")}"
        data-figure-location="${escapeHtml(locationLabel)}"
        title="${escapeHtml(title)}"
      >${escapeHtml(label)}</button>`;
    })
    .filter(Boolean)
    .join("");
  const selectedCount = selectedIds.size;
  host.classList.remove("is-empty");
  host.innerHTML = `
    <div class="run-figure-tools-head">
      <strong>Figure Candidates</strong>
      <span>${escapeHtml(String(candidates.length))} candidates · selected ${escapeHtml(String(selectedCount))}</span>
    </div>
    <div class="run-figure-tools-actions">
      <button type="button" class="ghost" data-figure-open-preview ${previewExists ? "" : "disabled"}>Open figures preview</button>
      <button type="button" class="ghost" data-figure-open-select>Open selected list</button>
      <button type="button" class="ghost" data-figure-apply-select>Use in Figures Select</button>
    </div>
    ${chips ? `<div class="run-figure-list">${chips}</div>` : `<div class="run-figure-meta">아직 후보 카드가 없습니다. 먼저 Federlicht를 --figures로 실행해 후보를 생성하세요.</div>`}
    <div class="run-figure-selected">
      <div class="run-figure-selected-head">
        <strong>Selected Figures</strong>
        <span><code>${escapeHtml(selectedPath)}</code></span>
      </div>
      <pre class="run-figure-selected-body" data-figure-selected-body>${escapeHtml(formatFigureSelectionPreview(selectedIds))}</pre>
    </div>
    <div class="run-figure-hover-preview" data-figure-hover-preview hidden>
      <div class="run-figure-hover-meta" data-figure-hover-meta></div>
      <img class="run-figure-hover-image" data-figure-hover-image alt="Figure preview" />
    </div>
    <div class="run-figure-meta">칩 클릭: 선택/해제 · Hover: 빠른 이미지 미리보기 · Shift+클릭: File Preview에서 열기</div>
    <div class="run-figure-meta">표기 안내: <code>p.</code>=PDF page, <code>slide</code>=PPT slide, <code>idx</code>=추출 인덱스</div>
  `;
  const countText = host.querySelector(".run-figure-tools-head span");
  const selectedBody = host.querySelector("[data-figure-selected-body]");
  const hoverCard = host.querySelector("[data-figure-hover-preview]");
  const hoverMeta = host.querySelector("[data-figure-hover-meta]");
  const hoverImage = host.querySelector("[data-figure-hover-image]");
  let hoverActiveBtn = null;
  const updateSelectionUi = () => {
    if (countText) {
      countText.textContent = `${candidates.length} candidates · selected ${selectedIds.size}`;
    }
    if (selectedBody) {
      selectedBody.textContent = formatFigureSelectionPreview(selectedIds);
    }
  };
  const hideHoverPreview = () => {
    if (hoverCard) hoverCard.setAttribute("hidden", "");
    if (hoverActiveBtn) hoverActiveBtn.classList.remove("is-hover-preview");
    hoverActiveBtn = null;
  };
  const showHoverPreview = (btn, ev) => {
    if (!hoverCard || !hoverMeta || !hoverImage) return;
    const imagePath = btn.getAttribute("data-figure-image") || "";
    if (!imagePath) {
      hideHoverPreview();
      return;
    }
    if (hoverActiveBtn && hoverActiveBtn !== btn) {
      hoverActiveBtn.classList.remove("is-hover-preview");
    }
    hoverActiveBtn = btn;
    hoverActiveBtn.classList.add("is-hover-preview");
    const id = btn.getAttribute("data-figure-id") || "";
    const source = btn.getAttribute("data-figure-source") || "";
    const location = btn.getAttribute("data-figure-location") || "";
    hoverMeta.textContent = [id, source, location].filter(Boolean).join(" · ");
    const previewSrc = rawFileUrl(imagePath);
    if (hoverImage.getAttribute("src") !== previewSrc) {
      hoverImage.setAttribute("src", previewSrc);
    }
    hoverCard.removeAttribute("hidden");
    const viewportWidth = window.innerWidth || document.documentElement.clientWidth || 0;
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight || 0;
    const offsetX = 16;
    const offsetY = 14;
    const cardRect = hoverCard.getBoundingClientRect();
    let left = (ev?.clientX || 0) + offsetX;
    let top = (ev?.clientY || 0) + offsetY;
    if (left + cardRect.width > viewportWidth - 10) {
      left = Math.max(10, viewportWidth - cardRect.width - 10);
    }
    if (top + cardRect.height > viewportHeight - 10) {
      top = Math.max(10, viewportHeight - cardRect.height - 10);
    }
    hoverCard.style.left = `${left}px`;
    hoverCard.style.top = `${top}px`;
  };
  host.querySelector("[data-figure-open-preview]")?.addEventListener("click", async () => {
    await loadFilePreview(previewPath, { focusPanel: false }).catch((err) => {
      appendLog(`[figures] preview open failed: ${err}\n`);
    });
  });
  host.querySelector("[data-figure-open-select]")?.addEventListener("click", async () => {
    if (!selectedExists) {
      await saveFigureSelection(selectedPath, selectedIds).catch((err) => {
        appendLog(`[figures] create selected list failed: ${err}\n`);
      });
      selectedExists = true;
    }
    await loadFilePreview(selectedPath, { focusPanel: false }).catch((err) => {
      appendLog(`[figures] selected list open failed: ${err}\n`);
    });
  });
  host.querySelector("[data-figure-apply-select]")?.addEventListener("click", () => {
    setFiguresSelectPath(selectedPath);
    appendLog(`[figures] figures_select set to ${selectedPath}\n`);
  });
  host.querySelectorAll("[data-figure-id]").forEach((btn) => {
    btn.addEventListener("mouseenter", (ev) => {
      showHoverPreview(btn, ev);
    });
    btn.addEventListener("mousemove", (ev) => {
      showHoverPreview(btn, ev);
    });
    btn.addEventListener("mouseleave", () => {
      hideHoverPreview();
    });
    btn.addEventListener("click", async (ev) => {
      const id = btn.getAttribute("data-figure-id") || "";
      if (!id) return;
      const imagePath = btn.getAttribute("data-figure-image") || "";
      if (ev.shiftKey && imagePath) {
        await loadFilePreview(imagePath, { focusPanel: false }).catch((err) => {
          appendLog(`[figures] image preview failed: ${err}\n`);
        });
        return;
      }
      if (selectedIds.has(id)) {
        selectedIds.delete(id);
      } else {
        selectedIds.add(id);
      }
      btn.classList.toggle("is-selected", selectedIds.has(id));
      await saveFigureSelection(selectedPath, selectedIds).catch((err) => {
        appendLog(`[figures] save selection failed: ${err}\n`);
      });
      updateSelectionUi();
      setFiguresSelectPath(selectedPath);
    });
  });
  host.addEventListener("mouseleave", () => {
    hideHoverPreview();
  });
}

function syncWorkflowResultPathFromSummary(summary) {
  if (!summary || state.workflow.kind !== "federlicht") return false;
  const latest = normalizePathString(summary.latest_report_rel || "");
  if (!latest) return false;
  const summaryRun = normalizePathString(summary.run_rel || "");
  const workflowRun = normalizePathString(state.workflow.runRel || "");
  const sameRun =
    !workflowRun
    || !summaryRun
    || workflowRun === summaryRun
    || summaryRun.endsWith(`/${workflowRun}`)
    || workflowRun.endsWith(`/${summaryRun}`);
  if (!sameRun) return false;
  if (workflowRun && !summaryRun && !latest.startsWith(`${workflowRun}/`)) return false;
  if (normalizePathString(state.workflow.resultPath || "") === latest) return false;
  state.workflow.resultPath = latest;
  if (!workflowRun && summaryRun) {
    state.workflow.runRel = summaryRun;
  }
  return true;
}

function renderRunSummary(summary) {
  state.runSummary = summary;
  if (syncWorkflowResultPathFromSummary(summary)) {
    renderWorkflow();
  }
  setStudioMeta(summary?.run_rel, summary?.updated_at);
  const trashBtn = $("#run-trash");
  if (trashBtn) {
    trashBtn.disabled = !summary?.run_rel;
    trashBtn.onclick = () => {
      if (!summary?.run_rel) return;
      trashRun(summary.run_rel);
    };
  }
  const publishBtn = $("#run-publish-hub");
  if (publishBtn) {
    const canPublish = Boolean(summary?.run_rel && summary?.latest_report_rel);
    publishBtn.disabled = !canPublish;
    publishBtn.textContent = "Publish to Report Hub";
    publishBtn.onclick = () => {
      if (!canPublish) return;
      publishRunToHub(summary, publishBtn);
    };
  }
  const linesHost = $("#run-summary-lines");
  if (linesHost) {
    const counts = summary?.counts && typeof summary.counts === "object"
      ? summary.counts
      : null;
    const rows = counts
      ? [
          ["Archive PDFs", counts.pdf ?? 0],
          ["Archive PPTX", counts.pptx ?? 0],
          ["Archive texts", counts.text ?? 0],
          ["Web extracts", counts.extracts ?? 0],
          ["Logs", counts.logs ?? 0],
          ["Reports", counts.report ?? 0],
          ["Instructions", counts.instruction ?? 0],
        ]
      : (summary?.summary_lines || []).map((line) => {
          const parts = String(line || "").split(":");
          if (parts.length < 2) return [String(line || "").trim(), "-"];
          const key = parts.shift() || "";
          const value = parts.join(":").trim();
          return [key.trim(), value];
        });
    linesHost.innerHTML = `
      <table class="summary-table" role="table" aria-label="Run summary counts">
        <tbody>
          ${rows
            .map(([label, value]) => `
              <tr>
                <th scope="row">${escapeHtml(String(label))}</th>
                <td>${escapeHtml(String(value))}</td>
              </tr>
            `)
            .join("")}
        </tbody>
      </table>
    `;
  }
  const linksHost = $("#run-summary-links");
  if (linksHost) {
    const links = [];
    if (summary?.run_rel) {
      const url = toFileUrlFromRel(summary.run_rel);
      if (url) links.push(`<a href="${url}" target="_blank" rel="noreferrer">Run Folder</a>`);
    }
    const hubIndexRel = joinPath(reportHubBase(), "index.html");
    const hubUrl = toFileUrlFromRel(hubIndexRel);
    if (hubUrl) {
      links.push(`<a href="${hubUrl}" target="_blank" rel="noreferrer">Report Hub</a>`);
    }
    if (summary?.latest_report_rel) {
      const name = summary.latest_report_rel.split("/").pop() || summary.latest_report_rel;
      links.push(
        `<button type="button" class="summary-chip" data-file="${escapeHtml(summary.latest_report_rel)}">${escapeHtml(
          `Latest Report (${name})`,
        )}</button>`,
      );
    }
    linksHost.innerHTML = links.join("");
    linksHost.querySelectorAll("button[data-file]").forEach((btn) => {
      btn.addEventListener("click", () => loadFilePreview(btn.dataset.file, { focusPanel: false }));
    });
  }
  const reportsHost = $("#run-summary-reports");
  if (reportsHost) {
    const reportLinks = (summary?.report_files || []).slice(-8).reverse();
    const indexLinks = (summary?.index_files || []).slice(0, 6);
    const parts = [];
    if (reportLinks.length) {
      const items = reportLinks
        .map((rel) => {
          const name = rel.split("/").pop() || rel;
          return `<button type="button" class="summary-chip" data-file="${escapeHtml(
            rel,
          )}">${escapeHtml(name)}</button>`;
        })
        .join("");
      parts.push(`<div class="summary-reports">${items}</div>`);
    }
    if (indexLinks.length) {
      const items = indexLinks
        .map((rel) => {
          const name = rel.split("/").pop() || rel;
          return `<button type="button" class="summary-chip" data-file="${escapeHtml(
            rel,
          )}">${escapeHtml(name)}</button>`;
        })
        .join("");
      parts.push(`<div class="summary-links">${items}</div>`);
    }
    reportsHost.innerHTML = parts.join("");
    reportsHost.querySelectorAll("button[data-file]").forEach((btn) => {
      btn.addEventListener("click", () => loadFilePreview(btn.dataset.file, { focusPanel: false }));
    });
  }
  renderRunFiles(summary);
  renderRunFigureTools(summary).catch((err) => {
    appendLog(`[figures] failed to load candidates: ${err}\n`);
  });
  applyRunSettings(summary);
}

async function trashRun(runRel) {
  if (!runRel) return;
  const ok = confirm(`Move run folder to trash?\n${runRel}`);
  if (!ok) return;
  try {
    const payload = { run: runRel };
    const result = await fetchJSON("/api/runs/trash", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    appendLog(`[runs] trashed ${runRel} -> ${result?.trash_rel || "trash"}\n`);
    await loadRuns();
  } catch (err) {
    appendLog(`[runs] trash failed: ${err}\n`);
  }
}

function nextReportPath(summary) {
  const runRel = summary?.run_rel;
  if (!runRel) return "";
  const files = summary?.report_files || [];
  let maxIndex = -1;
  let hasBase = false;
  files.forEach((rel) => {
    const name = rel.split("/").pop() || "";
    if (name === "report_full.html") {
      hasBase = true;
      maxIndex = Math.max(maxIndex, 0);
      return;
    }
    const match = name.match(/^report_full_(\d+)\.html$/);
    if (match) {
      const idx = Number.parseInt(match[1], 10);
      if (Number.isFinite(idx)) maxIndex = Math.max(maxIndex, idx);
    }
  });
  if (!hasBase && maxIndex < 0) {
    return `${runRel}/report_full.html`;
  }
  const next = maxIndex + 1;
  return `${runRel}/report_full_${next}.html`;
}

async function loadRunSummary(runRel) {
  if (!runRel) return;
  const summary = await fetchJSON(`/api/run-summary?run=${encodeURIComponent(runRel)}`);
  renderRunSummary(summary);
}

async function loadRunLogs(runRel) {
  if (!runRel) return;
  const logs = await fetchJSON(`/api/run-logs?run=${encodeURIComponent(runRel)}`);
  state.historyLogs[runRel] = Array.isArray(logs) ? logs : [];
  renderJobs();
}

function renderInstructionFiles(runRel) {
  const files = state.instructionFiles[runRel] || [];
  const fileSelect = $("#instruction-file-select");
  if (!fileSelect) return;
  const current = fileSelect.value;
  const defaultPath = defaultInstructionPath(runRel);
  const existingPaths = files.map((f) => f.path);
  const hasDefault = defaultPath && files.some((f) => f.path === defaultPath);
  const scopedLabel = (f) => {
    const scope = f.scope ? `[${f.scope}] ` : "";
    const tail = f.path || f.name || "";
    return `${scope}${tail}`;
  };
  const opts = files.map(
    (f) => `<option value="${f.path}">${escapeHtml(scopedLabel(f))}</option>`,
  );
  if (defaultPath && !hasDefault) {
    opts.unshift(
      `<option value="${defaultPath}">[new] ${escapeHtml(defaultPath)}</option>`,
    );
  }
  fileSelect.innerHTML = opts.join("");
  if (existingPaths.includes(current)) {
    fileSelect.value = current;
  }
  if (!fileSelect.value) {
    const preferred =
      files.find((f) => f.scope === "run")?.path || files[0]?.path || "";
    if (preferred) {
      fileSelect.value = preferred;
    } else if (defaultPath) {
      fileSelect.value = defaultPath;
    }
  }
}

async function loadInstructionFiles(runRel) {
  if (!runRel) return;
  const files = await fetchRunInstructionFiles(runRel, { refresh: true });
  renderInstructionFiles(runRel);
  const newPath = $("#instruction-new-path");
  if (newPath && !newPath.value.trim()) {
    newPath.value = defaultInstructionPath(runRel);
  }
  const selectedPath = $("#instruction-file-select")?.value;
  const exists = files.some((f) => f.path === selectedPath);
  if (selectedPath && exists) {
    await loadInstructionContent(selectedPath).catch((err) => {
      appendLog(`[instruction] failed to load content: ${err}\n`);
    });
  } else {
    const editor = $("#instruction-editor");
    if (editor) {
      editor.value = "";
      editor.dataset.path = "";
    }
  }
}

async function publishRunToHub(summary, button) {
  const runRel = String(summary?.run_rel || "").trim();
  const reportRel = String(summary?.latest_report_rel || "").trim();
  if (!runRel || !reportRel) {
    appendLog("[hub] publish skipped: run/report not selected.\n");
    return;
  }
  const targetBtn = button || $("#run-publish-hub");
  const idleLabel = "Publish to Report Hub";
  if (targetBtn) {
    targetBtn.disabled = true;
    targetBtn.textContent = "Publishing...";
  }
  try {
    const result = await fetchJSON("/api/report-hub/publish", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        run: runRel,
        report: reportRel,
        include_linked_assets: true,
        copy_overview: true,
        copy_workflow: true,
        overwrite: true,
      }),
    });
    const published = String(result?.published_report_rel || reportRel);
    const assetCount = Array.isArray(result?.published_asset_rels)
      ? result.published_asset_rels.length
      : 0;
    const skippedCount = Array.isArray(result?.skipped_asset_refs)
      ? result.skipped_asset_refs.length
      : 0;
    appendLog(
      `[hub] published ${published} (linked assets: ${assetCount}, skipped refs: ${skippedCount})\n`,
    );
    if (result?.index_rel) {
      appendLog(`[hub] index refreshed: ${result.index_rel}\n`);
    }
  } catch (err) {
    appendLog(`[hub] publish failed: ${err}\n`);
  } finally {
    if (targetBtn) {
      targetBtn.disabled = !(summary?.run_rel && summary?.latest_report_rel);
      targetBtn.textContent = idleLabel;
    }
  }
}

async function fetchRunInstructionFiles(runRel, options = {}) {
  const normalizedRun = normalizePathString(runRel || "");
  if (!normalizedRun) return [];
  const refresh = Boolean(options.refresh);
  const cached = state.instructionFiles[normalizedRun];
  if (!refresh && Array.isArray(cached)) {
    return cached;
  }
  const files = await fetchJSON(
    `/api/run-instructions?run=${encodeURIComponent(normalizedRun)}`,
  );
  const normalizedFiles = Array.isArray(files) ? files : [];
  state.instructionFiles[normalizedRun] = normalizedFiles;
  return normalizedFiles;
}

function resolveInstructionPathMeta(pathRel) {
  const expanded = normalizePathString(expandSiteRunsPath(pathRel || ""));
  if (!expanded) return null;
  const marker = "/instruction/";
  const markerIdx = expanded.indexOf(marker);
  if (markerIdx <= 0) return null;
  const runToken = normalizePathString(expanded.slice(0, markerIdx));
  const instructionLeaf = normalizePathString(expanded.slice(markerIdx + marker.length));
  const runRel = normalizePathString(resolveRunRelFromHint(runToken) || runToken);
  if (!runRel || !instructionLeaf) return null;
  const relPath = `${runRel}${marker}${instructionLeaf}`;
  return { runRel, relPath };
}

async function instructionPathExists(pathRel, options = {}) {
  const meta = resolveInstructionPathMeta(pathRel);
  if (!meta) return null;
  try {
    const files = await fetchRunInstructionFiles(meta.runRel, { refresh: Boolean(options.refresh) });
    return files.some((item) => normalizePathString(item?.path || "") === meta.relPath);
  } catch (err) {
    return null;
  }
}

async function loadInstructionContent(pathRel) {
  if (!pathRel) return;
  const payload = await fetchJSON(`/api/files?path=${encodeURIComponent(pathRel)}`);
  const editor = $("#instruction-editor");
  if (editor) {
    editor.value = payload.content || "";
    editor.dataset.path = payload.path || pathRel;
  }
}

async function loadFeatherInstructionContent(pathRel) {
  if (!pathRel) return;
  const payload = await fetchJSON(`/api/files?path=${encodeURIComponent(pathRel)}`);
  const editor = $("#feather-query");
  if (editor) {
    editor.value = payload.content || "";
    editor.dataset.path = payload.path || pathRel;
    editor.dataset.original = payload.content || "";
  }
}

async function loadFederlichtPromptContent(pathRel, opts = {}) {
  if (!pathRel) return;
  const force = Boolean(opts.force);
  if (!force && isPromptDirty()) return;
  const writePromptEditor = (path, content) => {
    const editor = $("#federlicht-prompt");
    if (!editor) return;
    editor.value = content || "";
    editor.dataset.path = path || "";
    editor.dataset.original = content || "";
    promptInlineTouched = false;
  };
  const exists = await instructionPathExists(pathRel, { refresh: force });
  if (exists === false) {
    writePromptEditor(pathRel, "");
    return;
  }
  let payload;
  try {
    payload = await fetchJSON(`/api/files?path=${encodeURIComponent(pathRel)}`);
  } catch (err) {
    if (isMissingFileError(err)) {
      writePromptEditor(pathRel, "");
      return;
    }
    throw err;
  }
  writePromptEditor(payload.path || pathRel, payload.content || "");
}

function isFeatherInstructionDirty() {
  const editor = $("#feather-query");
  if (!editor) return false;
  const original = editor.dataset.original ?? "";
  return (editor.value || "") !== original;
}

function setFeatherInstructionSnapshot(pathRel, content) {
  const editor = $("#feather-query");
  if (!editor) return;
  editor.dataset.path = pathRel || "";
  editor.dataset.original = content || "";
}

function isPromptDirty() {
  const editor = $("#federlicht-prompt");
  if (!editor) return false;
  const original = editor.dataset.original ?? "";
  return (editor.value || "") !== original;
}

function setPromptSnapshot(pathRel, content) {
  const editor = $("#federlicht-prompt");
  if (!editor) return;
  editor.dataset.path = pathRel || "";
  editor.dataset.original = content || "";
  promptInlineTouched = false;
}

function normalizePromptPath(rawPath, options = {}) {
  const runRel = options?.runRel || $("#run-select")?.value;
  if (runRel) return expandSiteRunsPath(normalizeInstructionPath(runRel, rawPath || ""), { runRel });
  let cleaned = (rawPath || "").trim().replaceAll("\\", "/");
  if (!cleaned) cleaned = "instruction/prompt.txt";
  cleaned = cleaned.replace(/^\/+/, "");
  if (cleaned.endsWith("/")) cleaned = `${cleaned}prompt.txt`;
  if (!hasFileExtension(cleaned)) cleaned = `${cleaned}.txt`;
  return expandSiteRunsPath(cleaned);
}

async function savePromptContent(pathRel, content) {
  if (!pathRel) throw new Error("Prompt path is required.");
  await fetchJSON("/api/files", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path: pathRel, content: content || "" }),
  });
  appendLog(`[prompt] saved ${pathRel}\n`);
  setPromptSnapshot(pathRel, content || "");
}

async function syncPromptFromFile(force = false) {
  const rawPath = $("#federlicht-prompt-file")?.value?.trim();
  const pathRel = rawPath ? expandSiteRunsPath(rawPath) : rawPath;
  if (!pathRel) return;
  if (!force && promptInlineTouched) return;
  await loadFederlichtPromptContent(pathRel, { force });
}

async function hydrateGeneratedPromptInline(outputPath) {
  const normalizedPath = normalizePathString(outputPath);
  if (!normalizedPath) return;
  const promptField = $("#federlicht-prompt-file");
  const displayPath = stripSiteRunsPrefix(normalizedPath) || normalizedPath;
  if (promptField) {
    promptField.value = displayPath;
    promptFileTouched = true;
  }
  const attemptDelays = [0, 220, 360, 520, 760, 980];
  let lastErr = null;
  for (let idx = 0; idx < attemptDelays.length; idx += 1) {
    const waitMs = attemptDelays[idx];
    if (waitMs > 0) {
      await new Promise((resolve) => window.setTimeout(resolve, waitMs));
    }
    try {
      await loadFederlichtPromptContent(normalizedPath, { force: true });
      return;
    } catch (err) {
      lastErr = err;
      if (!isMissingFileError(err)) break;
    }
  }
  if (lastErr && !isMissingFileError(lastErr)) {
    throw lastErr;
  }
}

function normalizeInstructionPath(runRel, rawPath) {
  const base = runBaseName(runRel);
  const fallback = defaultInstructionPath(runRel) || `instruction/${base}.txt`;
  let cleaned = (rawPath || "").trim().replaceAll("\\", "/");
  if (!cleaned) cleaned = fallback;
  cleaned = cleaned.replace(/^\/+/, "");
  if (cleaned.endsWith("/")) {
    cleaned = `${cleaned}${base}.txt`;
  }
  const last = cleaned.split("/").pop() || "";
  if (last && !hasFileExtension(last)) cleaned = `${cleaned}.txt`;
  return cleaned;
}

function pickInstructionRunRel() {
  const selected = $("#run-select")?.value;
  if (selected) return selected;
  const explicit = $("#feather-output")?.value?.trim();
  if (explicit) return normalizePathString(explicit);
  return state.runs[0]?.run_rel || "";
}

function normalizeFeatherInstructionPath(rawPath) {
  const runRel = pickInstructionRunRel();
  if (runRel) return expandSiteRunsPath(normalizeInstructionPath(runRel, rawPath), { runRel });
  let cleaned = (rawPath || "").trim().replaceAll("\\", "/");
  if (!cleaned) cleaned = "instruction/new_instruction.txt";
  cleaned = cleaned.replace(/^\/+/, "");
  if (cleaned.endsWith("/")) cleaned = `${cleaned}instruction.txt`;
  if (!hasFileExtension(cleaned)) cleaned = `${cleaned}.txt`;
  return expandSiteRunsPath(cleaned);
}

function normalizePathString(value) {
  return (value || "").trim().replaceAll("\\", "/").replace(/\/+$/, "");
}

function parentPath(value) {
  const cleaned = normalizePathString(value);
  if (!cleaned || !cleaned.includes("/")) return "";
  return cleaned.split("/").slice(0, -1).join("/");
}

async function saveInstructionContent(pathRel, content) {
  if (!pathRel) throw new Error("Instruction path is required.");
  await fetchJSON("/api/files", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path: pathRel, content: content || "" }),
  });
  appendLog(`[instruction] saved ${pathRel}\n`);
}

function openInstructionModal(mode = "feather") {
  state.instructionModal.mode = mode;
  openOverlayModal("instruction-modal");
}

function openRunPickerModal() {
  openOverlayModal("run-picker-modal");
}

function closeRunPickerModal() {
  closeOverlayModal("run-picker-modal");
}

function openModelPolicyModal() {
  renderGlobalModelPolicyControls();
  openOverlayModal("model-policy-modal");
}

function closeModelPolicyModal() {
  closeOverlayModal("model-policy-modal");
}

function closeInstructionModal() {
  closeOverlayModal("instruction-modal");
}

function renderInstructionModalList() {
  const host = $("#instruction-list");
  if (!host) return;
  const items = state.instructionModal.filtered.length
    ? state.instructionModal.filtered
    : state.instructionModal.items;
  if (!items.length) {
    host.innerHTML = `<div class="modal-item"><strong>No instruction files</strong><small>Create a new path below.</small></div>`;
    return;
  }
  host.innerHTML = items
    .map((item) => {
      const active = item.path === state.instructionModal.selectedPath ? "active" : "";
      const scope = item.scope ? `[${item.scope}] ` : "";
      return `
        <div class="modal-item ${active}" data-instruction-item="${item.path}">
          <strong>${escapeHtml(scope + item.name)}</strong>
          <small>${escapeHtml(item.path)}</small>
        </div>
      `;
    })
    .join("");
  host.querySelectorAll("[data-instruction-item]").forEach((el) => {
    el.addEventListener("click", () => {
      const path = el.getAttribute("data-instruction-item");
      if (!path) return;
      state.instructionModal.selectedPath = path;
      const saveAs = $("#instruction-saveas");
      if (saveAs) saveAs.value = path;
      renderInstructionModalList();
    });
  });
}

function runPickerItems() {
  const all = Array.isArray(state.runs) ? state.runs : [];
  const root = normalizePathString(state.runPicker.root || $("#run-picker-root")?.value || "");
  if (!root) return all;
  return all.filter((item) => {
    const runRoot = normalizePathString(item?.run_root_rel || "");
    if (runRoot) return runRoot === root;
    const runRel = normalizePathString(item?.run_rel || "");
    return runRootFromRunRel(runRel) === root;
  });
}

function renderRunPickerList() {
  const host = $("#run-picker-list");
  if (!host) return;
  const useFiltered = Boolean(String(state.runPicker.query || "").trim());
  const items = useFiltered ? state.runPicker.filtered : state.runPicker.items;
  if (!items.length) {
    const rootLabel = state.runPicker.root || siteRunsPrefix();
    host.innerHTML = `<div class="modal-item"><strong>No runs found</strong><small>Use Feather to create a run in ${escapeHtml(rootLabel)}.</small></div>`;
    return;
  }
  host.innerHTML = items
    .map((item) => {
      const isActive = item.run_rel === state.runPicker.selected;
      const active = isActive ? "active is-selected" : "";
      const label = item.run_rel || item.run_name || "";
      const root = normalizePathString(item?.run_root_rel || "");
      const badge = isActive ? `<span class="modal-item-badge">Selected</span>` : "";
      return `
        <div class="modal-item ${active}" data-runpicker-item="${label}" role="option" aria-selected="${isActive ? "true" : "false"}">
          <strong>${escapeHtml(item.run_name || label)}${badge}</strong>
          <small>${escapeHtml(label)}${root ? ` · root=${escapeHtml(root)}` : ""}</small>
        </div>
      `;
    })
    .join("");
  host.querySelectorAll("[data-runpicker-item]").forEach((el) => {
    el.addEventListener("click", () => {
      const rel = el.getAttribute("data-runpicker-item");
      if (!rel) return;
      state.runPicker.selected = rel;
      renderRunPickerList();
    });
  });
}

async function loadRunPickerItems() {
  const rootSelect = $("#run-picker-root");
  const availableRoots = uniqueTokens([
    ...(Array.isArray(state.info?.run_roots) ? state.info.run_roots : []),
    ...(Array.isArray(state.runs) ? state.runs.map((item) => item.run_root_rel) : []),
    ...parseRunRootsInputValue($("#workspace-run-roots")?.value || ""),
  ].map((item) => normalizePathString(item || "")));
  if (!availableRoots.length) {
    availableRoots.push(siteRunsPrefix());
  }
  if (rootSelect) {
    rootSelect.innerHTML = availableRoots
      .map((root) => `<option value="${escapeHtml(root)}">${escapeHtml(root)}</option>`)
      .join("");
    const inferredRoot = runRootFromRunRel(selectedRunRel() || "");
    const preferredRoot = normalizePathString(state.runPicker.root || inferredRoot || availableRoots[0] || "");
    if (preferredRoot) {
      rootSelect.value = preferredRoot;
      state.runPicker.root = preferredRoot;
    }
  }
  state.runPicker.items = runPickerItems();
  state.runPicker.filtered = [];
  state.runPicker.query = "";
  const search = $("#run-picker-search");
  if (search) search.value = "";
  const current = normalizePathString(selectedRunRel() || "");
  if (current && state.runPicker.items.some((item) => item.run_rel === current)) {
    state.runPicker.selected = current;
  } else {
    state.runPicker.selected = state.runPicker.items[0]?.run_rel || "";
  }
  renderWorkspaceSettingsControls();
  renderRunPickerList();
}

async function loadInstructionModalItems() {
  const mode = state.instructionModal.mode || "feather";
  const runRel =
    mode === "prompt" ? $("#run-select")?.value || "" : pickInstructionRunRel();
  state.instructionModal.runRel = runRel;
  if (!runRel) {
    state.instructionModal.items = [];
    renderInstructionModalList();
    return;
  }
  try {
    const items = await fetchJSON(
      `/api/run-instructions?run=${encodeURIComponent(runRel)}`,
    );
    state.instructionModal.items = items || [];
    state.instructionModal.filtered = [];
    state.instructionModal.selectedPath = items?.[0]?.path || "";
    const saveAs = $("#instruction-saveas");
    if (saveAs && !saveAs.value.trim()) {
      saveAs.value =
        mode === "prompt" ? defaultPromptPath(runRel) : defaultInstructionPath(runRel);
    }
    renderInstructionModalList();
  } catch (err) {
    appendLog(`[instruction] modal load failed: ${err}\n`);
    state.instructionModal.items = [];
    state.instructionModal.filtered = [];
    renderInstructionModalList();
  }
}

async function saveInstruction(runRel) {
  const editor = $("#instruction-editor");
  if (!editor) return;
  const basePath = editor.dataset.path || "";
  const newPathRaw = $("#instruction-new-path")?.value;
  const targetPath = normalizeInstructionPath(runRel, newPathRaw || basePath);
  if (!targetPath) {
    throw new Error("Instruction path is required.");
  }
  await saveInstructionContent(targetPath, editor.value || "");
  const newPath = $("#instruction-new-path");
  if (newPath) newPath.value = targetPath;
  await loadInstructionFiles(runRel);
  await loadRunSummary(runRel);
}

async function updateRunStudio(runRel) {
  await Promise.all([loadRunSummary(runRel), loadInstructionFiles(runRel), loadRunLogs(runRel)]);
}


function refreshTemplateSelectors() {
  const templateSelect = $("#template-select");
  const promptTemplateSelect = $("#prompt-template-select");
  if (!templateSelect && !promptTemplateSelect) return;
  const currentTemplate = templateSelect?.value;
  const currentPromptTemplate = promptTemplateSelect?.value;
  const options = state.templates
    .map((t) => {
      const label = t.includes("/custom_templates/") ? `custom:${t.split("/").pop()?.replace(/\\.md$/, "")}` : t;
      return `<option value="${escapeHtml(t)}">${escapeHtml(label || t)}</option>`;
    })
    .join("");
  if (templateSelect) templateSelect.innerHTML = options;
  if (promptTemplateSelect) promptTemplateSelect.innerHTML = options;
  if (templateSelect && state.templates.includes(currentTemplate || "")) {
    templateSelect.value = currentTemplate || "";
  }
  if (promptTemplateSelect && state.templates.includes(currentPromptTemplate || "")) {
    promptTemplateSelect.value = currentPromptTemplate || "";
  }
  if (templateSelect && !templateSelect.value && state.templates[0]) {
    templateSelect.value = state.templates[0];
  }
  if (promptTemplateSelect && !promptTemplateSelect.value && templateSelect?.value) {
    promptTemplateSelect.value = templateSelect.value;
  }
}

function renderTemplatesPanel() {
  const host = $("#templates-grid");
  if (!host) return;
  if (!state.templates.length) {
    host.innerHTML = `<div class="template-card"><h3>No templates</h3><p>Templates are loaded from <code>src/federlicht/templates</code>.</p></div>`;
    return;
  }
  const currentTemplate = $("#template-select")?.value || "";
  host.innerHTML = state.templates
    .map((name) => {
      const detail = state.templateDetails[name];
      const displayName = name.includes("/custom_templates/")
        ? `custom:${name.split("/").pop()?.replace(/\\.md$/, "")}`
        : name;
      const meta = detail?.meta || {};
      const pills = [meta.tone, meta.audience, meta.description]
        .filter(Boolean)
        .slice(0, 3)
        .map((v) => `<span class="template-pill">${escapeHtml(v)}</span>`)
        .join("");
      const sections = (detail?.sections || [])
        .slice(0, 12)
        .map((s) => `<span class="template-section">${escapeHtml(s)}</span>`)
        .join("");
      const active = currentTemplate === name ? "active" : "";
      return `
        <article class="template-card ${active}" data-template="${escapeHtml(name)}">
          <h3>${escapeHtml(displayName)}</h3>
          <div class="template-meta">${pills || "<span class=\"template-pill\">template</span>"}</div>
          <div class="template-sections">${sections || "<span class=\"template-section\">No sections parsed</span>"}</div>
          <div class="template-actions">
            <button type="button" class="ghost" data-template-use="${escapeHtml(name)}">Use</button>
            <button type="button" class="ghost" data-template-preview="${escapeHtml(name)}">Preview</button>
          </div>
        </article>
      `;
    })
    .join("");
  host.querySelectorAll("[data-template-use]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const name = btn.getAttribute("data-template-use");
      if (name) applyTemplateSelection(name, { loadBase: true });
    });
  });
  host.querySelectorAll("[data-template-preview]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const name = btn.getAttribute("data-template-preview");
      if (name) openTemplateModal(name);
    });
  });
}

function normalizeTemplateName(raw) {
  const cleaned = String(raw || "")
    .trim()
    .replace(/\s+/g, "_")
    .replace(/[^a-zA-Z0-9_-]/g, "");
  if (!cleaned) return "";
  return cleaned.startsWith("custom_") ? cleaned : `custom_${cleaned}`;
}

function templateStoreChoice() {
  return $("#template-store-site")?.checked ? "site" : "run";
}

function templateEditorTargetPath(name) {
  if (!name) return "";
  const useSite = $("#template-store-site")?.checked;
  const runRel = $("#run-select")?.value;
  if (useSite || !runRel) {
    return `site/custom_templates/${name}.md`;
  }
  return `${runRel}/custom_templates/${name}.md`;
}

function slugifyLabel(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9_-]+/g, "_")
    .replace(/_{2,}/g, "_")
    .replace(/^_+|_+$/g, "");
}

function stripFrontmatter(text) {
  const raw = String(text || "");
  if (!raw.startsWith("---")) {
    return { frontmatter: "", body: raw };
  }
  const parts = raw.split("\n");
  let endIndex = -1;
  for (let i = 1; i < parts.length; i += 1) {
    if (parts[i].trim() === "---") {
      endIndex = i;
      break;
    }
  }
  if (endIndex === -1) {
    return { frontmatter: "", body: raw };
  }
  const body = parts.slice(endIndex + 1).join("\n").trimStart();
  return { frontmatter: parts.slice(0, endIndex + 1).join("\n"), body };
}

function buildFrontmatter(meta, sections, guides, writerGuidance) {
  const lines = ["---"];
  const metaEntries = Object.entries(meta || {}).filter(([, v]) => v !== undefined && v !== "");
  metaEntries.forEach(([key, value]) => {
    lines.push(`${key}: ${value}`);
  });
  (sections || []).forEach((section) => {
    if (section) lines.push(`section: ${section}`);
  });
  Object.entries(guides || {}).forEach(([section, guide]) => {
    if (section && guide) lines.push(`guide ${section}: ${guide}`);
  });
  (writerGuidance || []).forEach((note) => {
    if (note) lines.push(`writer_guidance: ${note}`);
  });
  lines.push("---", "");
  return lines.join("\n");
}

function collectTemplateBuilderData() {
  const cssSelect = $("#template-style-select");
  const writerBox = $("#template-writer-guidance");
  const rows = [...document.querySelectorAll(".template-section-row")];
  const sections = [];
  const guides = {};
  rows.forEach((row) => {
    const nameInput = row.querySelector("[data-section-name]");
    const guideInput = row.querySelector("[data-section-guide]");
    const name = String(nameInput?.value || "").trim();
    const guide = String(guideInput?.value || "").trim();
    if (name) {
      sections.push(name);
      if (guide) guides[name] = guide;
    }
  });
  const writerGuidance = String(writerBox?.value || "")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
  return {
    css: cssSelect?.value || "",
    sections,
    guides,
    writerGuidance,
  };
}

function resolveStyleOption(cssName) {
  if (!cssName) return "";
  if (state.templateStyles.includes(cssName)) return cssName;
  const match = state.templateStyles.find((entry) => entry.endsWith(`/${cssName}`) || entry === cssName);
  return match || cssName;
}

function renderTemplateSections(rows) {
  const host = $("#template-sections-list");
  if (!host) return;
  host.innerHTML = rows
    .map(
      (row, idx) => `
      <div class="template-section-row" data-section-index="${idx}">
        <input class="ghost-input" data-section-name value="${escapeHtml(row.name || "")}" placeholder="Section name" />
        <input class="ghost-input" data-section-guide value="${escapeHtml(row.guide || "")}" placeholder="Guidance (optional)" />
        <div class="template-section-actions">
          <button type="button" class="ghost" data-section-move="up">↑</button>
          <button type="button" class="ghost" data-section-move="down">↓</button>
          <button type="button" class="ghost" data-section-move="remove">✕</button>
        </div>
      </div>
    `,
    )
    .join("");
  host.querySelectorAll("[data-section-move]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const row = btn.closest(".template-section-row");
      if (!row) return;
      const index = Number(row.dataset.sectionIndex || "0");
      const action = btn.getAttribute("data-section-move");
      const list = [...host.querySelectorAll(".template-section-row")].map((el) => ({
        name: el.querySelector("[data-section-name]")?.value || "",
        guide: el.querySelector("[data-section-guide]")?.value || "",
      }));
      if (action === "remove") {
        list.splice(index, 1);
      } else if (action === "up" && index > 0) {
        [list[index - 1], list[index]] = [list[index], list[index - 1]];
      } else if (action === "down" && index < list.length - 1) {
        [list[index + 1], list[index]] = [list[index], list[index + 1]];
      }
      renderTemplateSections(list);
    });
  });
}

function applyBuilderToEditor() {
  const body = $("#template-editor-body");
  if (!body) return;
  const { css, sections, guides, writerGuidance } = collectTemplateBuilderData();
  const { body: rawBody } = stripFrontmatter(body.value || "");
  const meta = { ...(state.templateBuilder.meta || {}) };
  const nameInput = $("#template-editor-name");
  const nameValue = String(nameInput?.value || "").trim();
  if (nameValue) {
    meta.name = nameValue;
  }
  if (css) {
    const cssValue = css.includes("/custom_templates/") ? css.split("/").pop() : css;
    meta.css = cssValue || css;
  }
  const frontmatter = buildFrontmatter(meta, sections, guides, writerGuidance);
  body.value = frontmatter + rawBody;
}

async function refreshTemplatePreview() {
  const frame = $("#template-preview-frame");
  if (!frame) return;
  const nameInput = $("#template-editor-name");
  const title = String(nameInput?.value || state.templateBuilder.meta?.name || "Template Preview").trim();
  const data = collectTemplateBuilderData();
  try {
    const payload = await fetchJSON("/api/template-preview", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: slugifyLabel(title || "template"),
        title,
        css: data.css,
        sections: data.sections,
        guides: data.guides,
        writer_guidance: data.writerGuidance,
      }),
    });
    frame.srcdoc = payload.html || "<p>Preview unavailable.</p>";
  } catch (err) {
    appendLog(`[templates] preview failed: ${err}\n`);
  }
}

function refreshTemplateEditorOptions() {
  const select = $("#template-editor-base");
  if (!select) return;
  const current = select.value;
  select.innerHTML = state.templates.map((t) => `<option value="${t}">${t}</option>`).join("");
  if (state.templates.includes(current)) {
    select.value = current;
  }
}

function updateTemplateEditorPath() {
  const input = $("#template-editor-name");
  const pathField = $("#template-editor-path");
  if (!input || !pathField) return;
  const name = normalizeTemplateName(input.value);
  pathField.value = templateEditorTargetPath(name);
}

async function loadTemplateEditorBase() {
  const baseSelect = $("#template-editor-base");
  const body = $("#template-editor-body");
  const meta = $("#template-editor-meta");
  if (!baseSelect || !body) return;
  const name = baseSelect.value;
  if (!name) return;
  try {
    const detail = state.templateDetails[name]
      || (await fetchJSON(`/api/templates/${encodeURIComponent(name)}`));
    if (!detail?.path) {
      throw new Error("Template path not found.");
    }
    const file = await fetchJSON(`/api/files?path=${encodeURIComponent(detail.path)}`);
    body.value = file.content || "";
    if (meta) meta.textContent = `Loaded base template: ${detail.path}`;
    const builderMeta = detail?.meta || {};
    state.templateBuilder.meta = { ...builderMeta };
    state.templateBuilder.css = resolveStyleOption(builderMeta.css || "");
    const sections = (detail?.sections || []).map((section) => ({
      name: section,
      guide: (detail?.guides || {})[section] || "",
    }));
    renderTemplateSections(sections);
    const writerBox = $("#template-writer-guidance");
    if (writerBox) writerBox.value = (detail?.writer_guidance || []).join("\n");
    refreshTemplateStyleSelect();
    const cssSelect = $("#template-style-select");
    if (cssSelect && state.templateBuilder.css) {
      cssSelect.value = resolveStyleOption(state.templateBuilder.css);
    }
    const nameInput = $("#template-editor-name");
    if (nameInput && !nameInput.value) {
      const baseName = name.includes("/") ? name.split("/").pop()?.replace(/\\.md$/, "") : name;
      nameInput.value = normalizeTemplateName(baseName || name);
      updateTemplateEditorPath();
    }
    refreshTemplatePreview();
  } catch (err) {
    appendLog(`[template-editor] failed to load base: ${err}\n`);
  }
}

async function saveTemplateEditor() {
  const nameInput = $("#template-editor-name");
  const body = $("#template-editor-body");
  const meta = $("#template-editor-meta");
  if (!nameInput || !body) return;
  const name = normalizeTemplateName(nameInput.value);
  if (!name) {
    appendLog("[template-editor] template name is required.\n");
    return;
  }
  applyBuilderToEditor();
  const path = templateEditorTargetPath(name);
  try {
    await fetchJSON("/api/files", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ path, content: body.value || "" }),
    });
    if (meta) meta.textContent = `Saved template: ${path}`;
    nameInput.value = name;
    updateTemplateEditorPath();
    await loadTemplates();
    applyTemplateSelection(name);
  } catch (err) {
    appendLog(`[template-editor] save failed: ${err}\n`);
  }
}

function applyTemplateSelection(name, opts = {}) {
  const templateSelect = $("#template-select");
  const promptTemplateSelect = $("#prompt-template-select");
  if (templateSelect) templateSelect.value = name;
  if (promptTemplateSelect) promptTemplateSelect.value = name;
  if (opts.loadBase) {
    const baseSelect = $("#template-editor-base");
    if (baseSelect) baseSelect.value = name;
    loadTemplateEditorBase();
  }
  renderTemplatesPanel();
}

function applyRunFolderSelection(runRel) {
  const runName = runBaseName(runRel);
  const runInput = $("#feather-run-name");
  const output = $("#feather-output");
  const input = $("#feather-input");
  const updateRun = $("#feather-update-run");
  if (runInput) runInput.value = runName;
  featherOutputTouched = false;
  featherInputTouched = false;
  if (output) output.value = runRel;
  if (input) input.value = `${runRel}/instruction/${runName}.txt`;
  if (updateRun) updateRun.checked = true;
  updateHeroStats();
  maybeReloadAskHistory();
}

function openTemplateModal(name) {
  const modal = $("#template-modal");
  if (!modal) return;
  const detail = state.templateDetails[name];
  const meta = detail?.meta || {};
  const title = $("#template-modal-title");
  const metaLine = $("#template-modal-meta");
  const body = $("#template-modal-body");
  if (title) title.textContent = name;
  if (metaLine) {
    const description = meta.description || meta.tone || "Template details";
    metaLine.textContent = description;
  }
  if (body) {
    const metaRows = Object.entries(meta || {})
      .map(([k, v]) => `<li><strong>${escapeHtml(k)}</strong>: ${escapeHtml(v)}</li>`)
      .join("");
    const sections = (detail?.sections || [])
      .map((s) => `<span class="template-section">${escapeHtml(s)}</span>`)
      .join("");
    const guides = Object.entries(detail?.guides || {})
      .map(
        ([k, v]) =>
          `<li><strong>${escapeHtml(k)}</strong>: ${escapeHtml(v)}</li>`,
      )
      .join("");
    const guidance = (detail?.writer_guidance || [])
      .map((g) => `<li>${escapeHtml(g)}</li>`)
      .join("");
    body.innerHTML = `
      <div class="template-modal-layout">
        <div class="template-modal-info">
          <div class="template-modal-section">
            <h4>Metadata</h4>
            <ul>${metaRows || "<li>No metadata.</li>"}</ul>
          </div>
          <div class="template-modal-section">
            <h4>Sections</h4>
            <div class="template-sections">${sections || "<span class=\"template-section\">No sections</span>"}</div>
          </div>
          <div class="template-modal-section">
            <h4>Section Guidance</h4>
            <ul>${guides || "<li>No section guidance.</li>"}</ul>
          </div>
          <div class="template-modal-section">
            <h4>Writer Guidance</h4>
            <ul>${guidance || "<li>No writer guidance.</li>"}</ul>
          </div>
        </div>
        <div class="template-modal-preview">
          <iframe title="Template preview"></iframe>
        </div>
      </div>
    `;
    const frame = body.querySelector("iframe");
    fetchJSON(`/api/template-preview?name=${encodeURIComponent(name)}`)
      .then((payload) => {
        if (frame && payload?.html) frame.srcdoc = payload.html;
      })
      .catch((err) => {
        appendLog(`[templates] preview failed: ${err}\n`);
      });
  }
  openOverlayModal("template-modal");
}

function closeTemplateModal() {
  closeOverlayModal("template-modal");
}

async function loadTemplateDetails(names) {
  const entries = await Promise.all(
    names.map(async (name) => {
      try {
        const detail = await fetchJSON(`/api/templates/${encodeURIComponent(name)}`);
        return [name, detail];
      } catch (err) {
        appendLog(`[templates] failed to load details for ${name}: ${err}\n`);
        return [name, null];
      }
    }),
  );
  state.templateDetails = Object.fromEntries(entries.filter(([, v]) => v));
}

function refreshTemplateStyleSelect() {
  const select = $("#template-style-select");
  if (!select) return;
  const current = select.value || state.templateBuilder.css || "";
  select.innerHTML = state.templateStyles
    .map((name) => {
      const label = name.includes("/custom_templates/")
        ? `custom:${name.split("/").pop()?.replace(/\\.css$/, "")}`
        : name;
      return `<option value="${escapeHtml(name)}">${escapeHtml(label || name)}</option>`;
    })
    .join("");
  if (current && state.templateStyles.includes(current)) {
    select.value = current;
  } else if (state.templateStyles[0]) {
    select.value = state.templateStyles[0];
  }
}

async function loadTemplateStyles(runRel) {
  try {
    const query = runRel ? `?run=${encodeURIComponent(runRel)}` : "";
    state.templateStyles = await fetchJSON(`/api/template-styles${query}`);
  } catch (err) {
    appendLog(`[templates] failed to load styles: ${err}\n`);
    state.templateStyles = [];
  }
  refreshTemplateStyleSelect();
}

async function loadTemplates() {
  const runRel = $("#run-select")?.value;
  const query = runRel ? `?run=${encodeURIComponent(runRel)}` : "";
  state.templates = await fetchJSON(`/api/templates${query}`);
  await loadTemplateDetails(state.templates);
  await loadTemplateStyles(runRel);
  refreshTemplateSelectors();
  refreshTemplateEditorOptions();
  updateHeroStats();
  renderTemplatesPanel();
}

function parseStageCsv(csv) {
  return String(csv || "")
    .split(",")
    .map((s) => s.trim())
    .filter((s) => s && STAGE_INDEX[s] !== undefined);
}

function selectedStagesInOrder() {
  return state.pipeline.order.filter((id) => state.pipeline.selected.has(id));
}

function loadWorkflowPreferences() {
  const raw = localStorage.getItem(WORKFLOW_PREF_STORAGE_KEY);
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object") return null;
    const order = Array.isArray(parsed.order)
      ? parsed.order.filter((id) => STAGE_INDEX[id] !== undefined)
      : [];
    const selected = Array.isArray(parsed.selected)
      ? parsed.selected.filter((id) => STAGE_INDEX[id] !== undefined)
      : [];
    const qualityIterations = parseQualityIterations(parsed.quality_iterations);
    return {
      order,
      selected,
      quality_iterations: qualityIterations,
    };
  } catch (err) {
    return null;
  }
}

function saveWorkflowPreferences() {
  const payload = {
    order: currentPipelineStageOrder(),
    selected: selectedStagesInOrder(),
    quality_iterations: getQualityIterations(),
  };
  localStorage.setItem(WORKFLOW_PREF_STORAGE_KEY, JSON.stringify(payload));
}

function currentPipelineStageOrder() {
  const canonical = STAGE_DEFS.map((s) => s.id);
  const ordered = [];
  const seen = new Set();
  for (const id of state.pipeline.order || []) {
    if (!STAGE_INDEX[id] && STAGE_INDEX[id] !== 0) continue;
    if (seen.has(id)) continue;
    seen.add(id);
    ordered.push(id);
  }
  for (const id of canonical) {
    if (!seen.has(id)) ordered.push(id);
  }
  return ordered;
}

function updatePipelineOutputs() {
  const selected = selectedStagesInOrder();
  const skipped = STAGE_DEFS.map((s) => s.id).filter((id) => !state.pipeline.selected.has(id));
  const stagesCsv = selected.join(",");
  const skipCsv = skipped.join(",");
  const stagesInput = $("#federlicht-stages");
  const skipInput = $("#federlicht-skip-stages");
  if (stagesInput) stagesInput.value = stagesCsv;
  if (skipInput) skipInput.value = skipCsv;
  setText("#pipeline-stages-value", stagesCsv || "-");
  setText("#pipeline-skip-value", skipCsv || "-");
  syncWorkflowStageSelection(selected);
  syncWorkflowQualityControls();
  saveWorkflowPreferences();
}

function parseQualityIterations(value) {
  const parsed = Number.parseInt(String(value ?? "").trim(), 10);
  if (!Number.isFinite(parsed)) return 1;
  if (parsed < 1) return 1;
  return Math.min(parsed, 10);
}

function getQualityIterations() {
  const mainInput = $("#federlicht-quality-iterations");
  if (mainInput) return parseQualityIterations(mainInput.value);
  return 1;
}

function setQualityIterations(value) {
  const normalized = parseQualityIterations(value);
  const text = String(normalized);
  const mainInput = $("#federlicht-quality-iterations");
  if (mainInput && mainInput.value !== text) mainInput.value = text;
  saveWorkflowPreferences();
  return normalized;
}

function closeWorkflowQualityMenu(options = {}) {
  if (!state.workflow.qualityMenuOpen) return;
  state.workflow.qualityMenuOpen = false;
  if (!options.silent) {
    renderWorkflow();
  }
}

function bindWorkflowDismissHandlers() {
  if (workflowDismissBound) return;
  workflowDismissBound = true;
  document.addEventListener("click", (ev) => {
    if (!state.workflow.qualityMenuOpen) return;
    const target = ev.target;
    if (!(target instanceof Element)) return;
    if (target.closest("#workflow-track")) return;
    closeWorkflowQualityMenu();
  });
  window.addEventListener("resize", () => {
    if (state.workflow.qualityMenuOpen) {
      closeWorkflowQualityMenu();
    }
  });
}

function syncWorkflowQualityControls() {
  const qualitySelected = workflowIsStageSelected("quality");
  const current = getQualityIterations();
  setQualityIterations(current);
  if (!qualitySelected || state.workflow.running) {
    closeWorkflowQualityMenu({ silent: true });
  }
  const mainInput = $("#federlicht-quality-iterations");
  if (mainInput) {
    mainInput.title = qualitySelected
      ? "Quality stage is enabled: iterations control critic/reviser loops."
      : "Quality stage is disabled: this value is kept but not used.";
  }
}

function workflowLabel(stepId) {
  if (stepId === "federhav") {
    return currentAskAgentDisplayName();
  }
  return WORKFLOW_LABELS[stepId] || stepId || "-";
}

function workflowNodeHint(stepId) {
  if (stepId === "federhav") {
    return `${currentAskAgentDisplayName()}: 사용자 요청을 해석하고 run/agent/workflow 실행 제안을 조율하는 governing agent.`;
  }
  if (stepId === "feather") {
    return "Feather: 입력 소스를 수집·정리하여 분석 가능한 아카이브를 만듭니다.";
  }
  if (stepId === "result") {
    return "Result: 최종 보고서 산출물입니다. 클릭하면 현재 결과 파일을 미리보기로 엽니다.";
  }
  const stage = STAGE_DEFS.find((item) => item.id === stepId);
  if (stage) {
    return `${stage.label}: ${stage.desc} (단일 클릭: 단계 포커스, 더블 클릭: Workflow Studio 열기)`;
  }
  return workflowLabel(stepId);
}

function workflowSpotLabel(kind) {
  return WORKFLOW_SPOT_LABELS[kind] || WORKFLOW_SPOT_LABELS.job;
}

function clearWorkflowLoopbackTimer() {
  if (state.workflow.loopbackTimer) {
    window.clearTimeout(state.workflow.loopbackTimer);
    state.workflow.loopbackTimer = null;
  }
}

function clearWorkflowSpotTimer(spotId) {
  const timer = state.workflow.spotTimers?.[spotId];
  if (!timer) return;
  window.clearTimeout(timer);
  delete state.workflow.spotTimers[spotId];
}

function removeWorkflowSpot(spotId) {
  clearWorkflowSpotTimer(spotId);
  state.workflow.spots = (state.workflow.spots || []).filter((spot) => spot.id !== spotId);
  if (!state.workflow.running) {
    const anyRunningSpot = state.workflow.spots.some((spot) => spot.running);
    if (!anyRunningSpot) {
      state.workflow.statusText = state.workflow.mainStatusText || "Idle";
    }
  }
  renderWorkflow();
}

function scheduleWorkflowSpotRemoval(spotId, ttlMs = WORKFLOW_SPOT_TTL_MS) {
  clearWorkflowSpotTimer(spotId);
  const timer = window.setTimeout(() => {
    removeWorkflowSpot(spotId);
  }, ttlMs);
  state.workflow.spotTimers[spotId] = timer;
}

function findRunningWorkflowSpot(kind) {
  const spots = state.workflow.spots || [];
  for (let i = spots.length - 1; i >= 0; i -= 1) {
    const spot = spots[i];
    if (spot.kind === kind && spot.running) return spot;
  }
  return null;
}

function beginWorkflowSpot(kind, payload = {}) {
  const id = `spot-${kind}-${Date.now()}-${state.workflow.spotSeq++}`;
  const path = normalizePathString(payload._spot_path || payload.output || "");
  const spot = {
    id,
    kind,
    label: String(payload._spot_label || "").trim() || workflowSpotLabel(kind),
    running: true,
    status: "running",
    hasError: false,
    path,
    startedAt: Date.now(),
  };
  state.workflow.spots.push(spot);
  if (state.workflow.spots.length > 6) {
    const trimmed = state.workflow.spots.shift();
    if (trimmed?.id) clearWorkflowSpotTimer(trimmed.id);
  }
  if (!state.workflow.running) {
    state.workflow.activeStep = "";
    state.workflow.statusText = `Extra · ${spot.label}`;
  }
  renderWorkflow();
  return spot;
}

function completeWorkflowSpot(kind, returnCode, status = "") {
  const spot = findRunningWorkflowSpot(kind);
  if (!spot) return;
  const statusLower = String(status || "").toLowerCase();
  const failedByStatus = ["fail", "error", "killed", "cancel", "abort"].some((token) =>
    statusLower.includes(token),
  );
  let success = Number(returnCode) === 0;
  if (!Number.isFinite(Number(returnCode)) && statusLower) {
    success = !failedByStatus;
  }
  if (failedByStatus) success = false;
  spot.running = false;
  spot.status = success ? "done" : "error";
  spot.hasError = !success;
  if (!state.workflow.running) {
    state.workflow.statusText = success ? `Extra done · ${spot.label}` : `Extra failed · ${spot.label}`;
  }
  scheduleWorkflowSpotRemoval(spot.id);
  renderWorkflow();
}

function triggerWorkflowLoopback() {
  state.workflow.loopbackCount = Number(state.workflow.loopbackCount || 0) + 1;
  state.workflow.loopbackPulse = true;
  clearWorkflowLoopbackTimer();
  state.workflow.loopbackTimer = window.setTimeout(() => {
    state.workflow.loopbackPulse = false;
    state.workflow.loopbackTimer = null;
    renderWorkflow();
  }, WORKFLOW_LOOPBACK_PULSE_MS);
}

function resetWorkflowState() {
  state.workflow.kind = "";
  state.workflow.running = false;
  state.workflow.historyMode = false;
  state.workflow.historySourcePath = "";
  state.workflow.resumeStage = "";
  state.workflow.resumePromptPath = "";
  state.workflow.resumePromptStage = "";
  state.workflow.resumePromptAt = "";
  state.workflow.historyStageStatus = {};
  state.workflow.historyFailedStage = "";
  state.workflow.selectedStages = new Set(selectedStagesInOrder());
  state.workflow.stageOrder = currentPipelineStageOrder();
  state.workflow.autoStages = new Set();
  state.workflow.autoStageReasons = {};
  state.workflow.passMetrics = [];
  state.workflow.activeStep = "";
  state.workflow.completedSteps = new Set();
  state.workflow.hasError = false;
  state.workflow.statusText = "Idle";
  state.workflow.mainStatusText = "Idle";
  state.workflow.runRel = "";
  state.workflow.resultPath = "";
  clearWorkflowLoopbackTimer();
  state.workflow.lastMainStageIndex = -1;
  state.workflow.loopbackCount = 0;
  state.workflow.loopbackPulse = false;
  state.workflow.qualityMenuOpen = false;
  (state.workflow.spots || []).forEach((spot) => {
    if (spot?.id) clearWorkflowSpotTimer(spot.id);
  });
  state.workflow.spots = [];
  state.workflow.spotTimers = {};
  state.workflow.spotSeq = 0;
}

function syncWorkflowStageSelection(selected = selectedStagesInOrder()) {
  if (state.workflow.running && state.workflow.kind === "federlicht") return;
  if (state.workflow.historyMode && state.workflow.kind === "federlicht") {
    state.workflow.selectedStages = new Set(selected);
    state.workflow.stageOrder = currentPipelineStageOrder();
    if (!state.workflow.selectedStages.has(state.workflow.resumeStage || "")) {
      const ordered = workflowStageOrder().filter((id) => state.workflow.selectedStages.has(id));
      state.workflow.resumeStage = ordered[0] || "";
    }
    renderWorkflow();
    return;
  }
  state.workflow.selectedStages = new Set(selected);
  state.workflow.stageOrder = currentPipelineStageOrder();
  state.workflow.autoStages = new Set();
  state.workflow.autoStageReasons = {};
  state.workflow.passMetrics = [];
  renderWorkflow();
}

function workflowStageOrder() {
  const raw = Array.isArray(state.workflow.stageOrder) ? state.workflow.stageOrder : [];
  const ordered = [];
  const seen = new Set();
  for (const id of raw) {
    if (!WORKFLOW_STAGE_ORDER.includes(id)) continue;
    if (seen.has(id)) continue;
    seen.add(id);
    ordered.push(id);
  }
  for (const id of WORKFLOW_STAGE_ORDER) {
    if (!seen.has(id)) ordered.push(id);
  }
  return ordered;
}

function workflowNodeOrder() {
  return ["federhav", "feather", ...workflowStageOrder(), "result"];
}

function nextSelectedWorkflowStage(afterStageId) {
  const ordered = workflowStageOrder().filter((id) => state.workflow.selectedStages.has(id));
  const idx = ordered.indexOf(afterStageId);
  if (idx < 0) return afterStageId;
  for (let i = idx + 1; i < ordered.length; i += 1) {
    const candidate = ordered[i];
    if (!state.workflow.completedSteps.has(candidate)) {
      return candidate;
    }
  }
  return afterStageId;
}

function workflowIsStageSelected(stepId) {
  if (stepId === "federhav" || stepId === "feather" || stepId === "result") return true;
  if (state.workflow.kind !== "federlicht" && !state.workflow.running) {
    return state.workflow.selectedStages.has(stepId);
  }
  if (state.workflow.kind !== "federlicht") return false;
  return state.workflow.selectedStages.has(stepId);
}

function stageOrderIndex(stageId) {
  return workflowStageOrder().indexOf(stageId);
}

function markWorkflowCompletedThroughStage(stageId) {
  const selected = workflowStageOrder().filter((id) => state.workflow.selectedStages.has(id));
  const stopIdx = selected.indexOf(stageId);
  selected.forEach((id, idx) => {
    if (stopIdx >= 0 && idx < stopIdx) {
      state.workflow.completedSteps.add(id);
    }
  });
}

function beginWorkflow(kind, payload = {}) {
  const selected = selectedStagesInOrder();
  if (kind === "federlicht") {
    const workflowRun = normalizePathString(selectedRunRel() || inferRunRelFromPayload(payload) || "");
    state.workflow.kind = "federlicht";
    state.workflow.running = true;
    state.workflow.historyMode = false;
    state.workflow.historySourcePath = "";
    state.workflow.resumeStage = "";
    state.workflow.historyStageStatus = {};
    state.workflow.runRel = workflowRun;
    state.workflow.selectedStages = new Set(selected);
    state.workflow.stageOrder = currentPipelineStageOrder();
    state.workflow.autoStages = new Set();
    state.workflow.autoStageReasons = {};
    state.workflow.passMetrics = [];
    state.workflow.completedSteps = new Set(["feather"]);
    state.workflow.activeStep = selected[0] || "scout";
    state.workflow.hasError = false;
    state.workflow.statusText = `Streaming · ${workflowLabel(state.workflow.activeStep)}`;
    state.workflow.mainStatusText = state.workflow.statusText;
    state.workflow.resultPath = normalizeWorkflowResultPath(payload.output || "");
    state.workflow.lastMainStageIndex = stageOrderIndex(state.workflow.activeStep);
    state.workflow.loopbackCount = 0;
    state.workflow.loopbackPulse = false;
    clearWorkflowLoopbackTimer();
    renderWorkflow();
    return;
  }
  if (kind === "feather") {
    state.workflow.runRel = "";
    state.workflow.kind = "feather";
    state.workflow.running = true;
    state.workflow.historyMode = false;
    state.workflow.historySourcePath = "";
    state.workflow.resumeStage = "";
    state.workflow.historyStageStatus = {};
    state.workflow.selectedStages = new Set();
    state.workflow.stageOrder = currentPipelineStageOrder();
    state.workflow.autoStages = new Set();
    state.workflow.autoStageReasons = {};
    state.workflow.passMetrics = [];
    state.workflow.completedSteps = new Set();
    state.workflow.activeStep = "feather";
    state.workflow.hasError = false;
    state.workflow.statusText = "Streaming · Feather";
    state.workflow.mainStatusText = state.workflow.statusText;
    state.workflow.resultPath = "";
    state.workflow.lastMainStageIndex = -1;
    state.workflow.loopbackCount = 0;
    state.workflow.loopbackPulse = false;
    clearWorkflowLoopbackTimer();
    renderWorkflow();
    return;
  }
  beginWorkflowSpot(kind, payload);
}

function detectFederlichtStageFromLog(text) {
  const lowered = String(text || "").toLowerCase();
  if (!lowered.trim()) return "";
  if (lowered.includes("job end") || lowered.includes("[done] done") || lowered.includes("job failed")) {
    return "result";
  }
  if (
    lowered.includes("scout notes")
    || lowered.includes("alignment check (scout)")
    || lowered.includes("stage: scout")
  ) {
    return "scout";
  }
  if (
    lowered.includes("\nplan:")
    || lowered.startsWith("plan:")
    || /(^|[\s\]])plan:/.test(lowered)
    || lowered.includes("alignment plan")
    || lowered.includes("report plan")
  ) {
    return "plan";
  }
  if (
    lowered.includes("evidence notes")
    || lowered.includes("alignment check (evidence)")
    || lowered.includes("stage: evidence")
  ) {
    return "evidence";
  }
  if (
    lowered.includes("quality")
    || lowered.includes("critic")
    || lowered.includes("reviser")
    || lowered.includes("pairwise compare")
  ) {
    return "quality";
  }
  if (
    lowered.includes("report preview")
    || lowered.includes("stage: writer")
    || lowered.includes("writer")
  ) {
    return "writer";
  }
  return "";
}

function normalizeWorkflowEventStage(stageName) {
  const raw = String(stageName || "").trim().toLowerCase();
  if (!raw) return "";
  if (raw === "clarifier" || raw === "template_adjust") return "scout";
  if (raw === "plan_check") return "plan";
  if (raw === "web" || raw === "alignment" || raw === "reducer") return "evidence";
  if (
    raw === "critic"
    || raw === "reviser"
    || raw === "evaluator"
    || raw === "pairwise_compare"
    || raw === "synthesizer"
  ) {
    return "quality";
  }
  if (WORKFLOW_STAGE_ORDER.includes(raw) || raw === "result") return raw;
  return "";
}

function parseWorkflowEvent(text) {
  const match = String(text || "").match(WORKFLOW_EVENT_RE);
  if (!match) return null;
  const stageId = normalizeWorkflowEventStage(match[1]);
  if (!stageId) return null;
  return {
    stageId,
    status: String(match[2] || "").toLowerCase(),
    detail: String(match[3] || "").trim(),
  };
}

function parseWorkflowDetailMeta(detail) {
  const payload = {
    autoRequiredBy: [],
    autoRequired: false,
    passMetric: null,
  };
  const text = String(detail || "").trim();
  if (!text) return payload;
  if (/\bauto_required\b/i.test(text)) {
    payload.autoRequired = true;
  }
  const autoMatch = text.match(/auto_required_by=([a-z_,]+)/i);
  if (autoMatch && autoMatch[1]) {
    const seen = new Set();
    const requiredBy = [];
    autoMatch[1]
      .split(",")
      .map((token) => String(token || "").trim().toLowerCase())
      .forEach((token) => {
        if (!token || !WORKFLOW_STAGE_ORDER.includes(token) || seen.has(token)) return;
        seen.add(token);
        requiredBy.push(token);
      });
    payload.autoRequiredBy = requiredBy;
  }
  const passMatch = text.match(/(?:^|[,\s])pass=(\d+)(?:[,]|$)/i);
  const elapsedMatch = text.match(/(?:^|[,\s])elapsed_ms=(\d+)(?:[,]|$)/i);
  const tokenMatch = text.match(/(?:^|[,\s])est_tokens=(\d+)(?:[,]|$)/i);
  const cacheMatch = text.match(/(?:^|[,\s])cache_hits=(\d+)(?:[,]|$)/i);
  const runtimeMatch = text.match(/(?:^|[,\s])runtime=([a-z_|]+)(?:[,]|$)/i);
  if (passMatch || elapsedMatch || tokenMatch || cacheMatch) {
    payload.passMetric = {
      pass: passMatch ? Number(passMatch[1]) : 0,
      elapsedMs: elapsedMatch ? Number(elapsedMatch[1]) : 0,
      estTokens: tokenMatch ? Number(tokenMatch[1]) : 0,
      cacheHits: cacheMatch ? Number(cacheMatch[1]) : 0,
      runtime: runtimeMatch ? String(runtimeMatch[1] || "").trim() : "",
    };
  }
  return payload;
}

function normalizeWorkflowStatusToken(rawStatus) {
  const token = String(rawStatus || "").trim().toLowerCase().replace("-", "_");
  if (!token) return "";
  if (token === "ok" || token === "success") return "ran";
  if (token === "complete") return "done";
  if (token === "inprogress") return "in_progress";
  return token;
}

function workflowStatusPriority(status) {
  const token = normalizeWorkflowStatusToken(status);
  if (Object.prototype.hasOwnProperty.call(WORKFLOW_STATUS_PRIORITY, token)) {
    return Number(WORKFLOW_STATUS_PRIORITY[token]);
  }
  return 0;
}

function mergeWorkflowStageStatus(stageStore, stageId, status, detail = "") {
  if (!stageId || !WORKFLOW_STAGE_ORDER.includes(stageId)) return;
  const nextStatus = normalizeWorkflowStatusToken(status || "");
  if (!nextStatus) return;
  const nextDetail = String(detail || "").trim();
  const prev = stageStore[stageId];
  if (!prev) {
    stageStore[stageId] = { status: nextStatus, detail: nextDetail };
    return;
  }
  const prevScore = workflowStatusPriority(prev.status);
  const nextScore = workflowStatusPriority(nextStatus);
  if (nextScore > prevScore) {
    stageStore[stageId] = { status: nextStatus, detail: nextDetail };
    return;
  }
  if (nextScore === prevScore && nextDetail && !String(prev.detail || "").trim()) {
    stageStore[stageId] = { status: nextStatus, detail: nextDetail };
  }
}

function parseWorkflowDoneEvent(line) {
  const match = String(line || "").match(/\[done\]\s*([^\(\n]+?)?(?:\s*\(rc=(-?\d+)\))?\s*$/i);
  if (!match) return null;
  const status = normalizeWorkflowStatusToken(match[1] || "done");
  const rcRaw = match[2];
  const returnCode = rcRaw !== undefined && rcRaw !== null && rcRaw !== ""
    ? Number.parseInt(rcRaw, 10)
    : null;
  return {
    status,
    returnCode: Number.isFinite(returnCode) ? Number(returnCode) : null,
  };
}

function parseWorkflowHistoryFromLog(logText) {
  const stageStore = {};
  let hasEnd = false;
  let hasError = false;
  let resultPath = "";
  const lines = String(logText || "").split(/\r?\n/);
  lines.forEach((rawLine) => {
    const line = String(rawLine || "");
    const workflowEvent = parseWorkflowEvent(line);
    if (workflowEvent && workflowEvent.stageId !== "result") {
      mergeWorkflowStageStatus(
        stageStore,
        workflowEvent.stageId,
        workflowEvent.status,
        workflowEvent.detail,
      );
      if (["error", "failed"].includes(normalizeWorkflowStatusToken(workflowEvent.status))) {
        hasError = true;
      }
    }
    const stageHint = detectFederlichtStageFromLog(line);
    if (stageHint && stageHint !== "result") {
      mergeWorkflowStageStatus(stageStore, stageHint, "ran", "history_detected");
    } else if (stageHint === "result") {
      hasEnd = true;
    }
    const doneEvent = parseWorkflowDoneEvent(line);
    if (doneEvent) {
      hasEnd = true;
      if ((doneEvent.returnCode ?? 0) !== 0) {
        hasError = true;
      }
      if (["error", "failed"].includes(doneEvent.status)) {
        hasError = true;
      }
    }
    if (/\bjob failed\b/i.test(line) || /\btraceback \(most recent call last\):/i.test(line)) {
      hasError = true;
      hasEnd = true;
    }
    if (/\bjob end\b/i.test(line)) {
      hasEnd = true;
    }
    const path = parseWorkflowResultPathFromLog(line);
    if (path) resultPath = path;
  });
  return { stageStore, hasEnd, hasError, resultPath };
}

function parseWorkflowHistoryFromSummary(summaryData) {
  const stageStore = {};
  const stageOrder = [];
  if (!summaryData || typeof summaryData !== "object") {
    return { stageStore, stageOrder };
  }
  const stages = summaryData.stages && typeof summaryData.stages === "object"
    ? summaryData.stages
    : {};
  const runtimeOrder = Array.isArray(summaryData.order) ? summaryData.order : [];
  const seenTop = new Set();
  const ingest = (runtimeName) => {
    const runtime = String(runtimeName || "").trim();
    if (!runtime) return;
    const topStage = normalizeWorkflowEventStage(runtime);
    if (!WORKFLOW_STAGE_ORDER.includes(topStage)) return;
    const runtimePayload = stages[runtime] && typeof stages[runtime] === "object"
      ? stages[runtime]
      : {};
    mergeWorkflowStageStatus(
      stageStore,
      topStage,
      runtimePayload.status || "disabled",
      runtimePayload.detail || "",
    );
    if (!seenTop.has(topStage)) {
      seenTop.add(topStage);
      stageOrder.push(topStage);
    }
  };
  runtimeOrder.forEach(ingest);
  Object.keys(stages).forEach(ingest);
  return { stageStore, stageOrder };
}

async function loadRunWorkflowHistorySummary(runRel) {
  const normalizedRun = normalizePathString(runRel);
  if (!normalizedRun) return null;
  const workflowJsonPath = joinPath(normalizedRun, "report_notes/report_workflow.json");
  try {
    const payload = await fetchJSON(`/api/files?path=${encodeURIComponent(workflowJsonPath)}`);
    const content = String(payload?.content || "").trim();
    if (!content) return null;
    const parsed = JSON.parse(content);
    if (!parsed || typeof parsed !== "object") return null;
    return parsed;
  } catch (err) {
    const workflowMdPath = joinPath(normalizedRun, "report_notes/report_workflow.md");
    try {
      const payload = await fetchJSON(`/api/files?path=${encodeURIComponent(workflowMdPath)}`);
      const content = String(payload?.content || "");
      const lines = content.split(/\r?\n/);
      const stages = {};
      const order = [];
      lines.forEach((line) => {
        const match = line.match(/^\s*\d+\.\s*([a-z_]+)\s*:\s*([a-z_]+)(?:\s*\(([^)]*)\))?\s*$/i);
        if (!match) return;
        const stageName = String(match[1] || "").trim();
        const status = String(match[2] || "").trim();
        const detail = String(match[3] || "").trim();
        if (!stageName || !status) return;
        stages[stageName] = { status, detail };
        order.push(stageName);
      });
      if (!order.length) return null;
      return { stages, order };
    } catch (mdErr) {
      return null;
    }
  }
}

function findWorkflowResumeStage() {
  const ordered = workflowStageOrder().filter((id) => state.workflow.selectedStages.has(id));
  const nextPending = ordered.find((id) => !state.workflow.completedSteps.has(id));
  if (nextPending) return nextPending;
  if (ordered.includes("writer")) return "writer";
  return ordered[0] || "";
}

function syncWorkflowHistoryControls() {
  const controls = $("#workflow-history-controls");
  const hintEl = $("#workflow-history-hint");
  const resumeBtn = $("#workflow-resume-apply");
  const promptBtn = $("#workflow-resume-prompt");
  const guideEl = $("#workflow-resume-guide");
  if (!controls || !hintEl || !resumeBtn || !promptBtn || !guideEl) return;
  const active =
    state.workflow.historyMode
    && state.workflow.kind === "federlicht"
    && !state.workflow.running;
  controls.classList.toggle("is-active", active);
  if (!active) {
    hintEl.textContent = "History checkpoint: -";
    resumeBtn.disabled = true;
    resumeBtn.textContent = "Resume from stage";
    promptBtn.disabled = true;
    guideEl.innerHTML = "";
    guideEl.classList.add("is-empty");
    return;
  }
  const ordered = workflowStageOrder().filter((id) => WORKFLOW_STAGE_ORDER.includes(id));
  const completedTop = ordered.filter((id) => state.workflow.completedSteps.has(id));
  const lastCompleted = completedTop.length ? completedTop[completedTop.length - 1] : "";
  const resumeStage = state.workflow.resumeStage || "";
  const lastLabel = lastCompleted ? workflowLabel(lastCompleted) : "Start";
  const resumeLabel = resumeStage ? workflowLabel(resumeStage) : "-";
  const sourceName = state.workflow.historySourcePath
    ? state.workflow.historySourcePath.split("/").pop()
    : "";
  const failedStage = String(state.workflow.historyFailedStage || "").trim();
  const failedText = failedStage ? ` · stopped at ${workflowLabel(failedStage)}` : "";
  hintEl.textContent = sourceName
    ? `체크포인트: 마지막 완료 ${lastLabel} · 재시작 ${resumeLabel}${failedText} (${sourceName})`
    : `체크포인트: 마지막 완료 ${lastLabel} · 재시작 ${resumeLabel}${failedText}`;
  resumeBtn.disabled = !resumeStage;
  resumeBtn.textContent = resumeStage
    ? `Resume from ${workflowLabel(resumeStage)}`
    : "Resume from stage";
  promptBtn.disabled = !normalizePathString(state.workflow.runRel || "");
  const promptPath = normalizePathString(state.workflow.resumePromptPath || "");
  const promptStage = state.workflow.resumePromptStage || resumeStage || "";
  const promptRun = normalizePathString(state.workflow.runRel || "");
  if (!promptPath) {
    guideEl.innerHTML = "";
    guideEl.classList.add("is-empty");
    return;
  }
  const promptRel = stripRunPrefix(promptPath, promptRun) || stripSiteRunsPrefix(promptPath) || promptPath;
  const promptTime = state.workflow.resumePromptAt
    ? new Date(state.workflow.resumePromptAt).toLocaleString()
    : "";
  guideEl.classList.remove("is-empty");
  guideEl.innerHTML = `
    <div class="workflow-resume-guide-head">
      <strong>최근 update request</strong>
      <span>선택 단계: ${escapeHtml(promptStage ? workflowLabel(promptStage) : "선택 필요")}</span>
    </div>
    <div class="workflow-resume-guide-meta">
      <span>파일:</span>
      <code>${escapeHtml(promptRel)}</code>
      ${promptTime ? `<span>${escapeHtml(promptTime)}</span>` : ""}
    </div>
    <div class="workflow-resume-guide-actions">
      <button type="button" class="ghost" data-workflow-open-update="${escapeHtml(promptPath)}">Open update request</button>
      <button type="button" class="ghost" data-workflow-focus-inline="true">Focus Inline Prompt</button>
    </div>
  `;
  guideEl.querySelectorAll("[data-workflow-open-update]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const path = btn.getAttribute("data-workflow-open-update") || "";
      if (!path) return;
      await loadFilePreview(path);
    });
  });
  guideEl.querySelectorAll("[data-workflow-focus-inline]").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelector('.tab[data-tab="federlicht"]')?.dispatchEvent(
        new MouseEvent("click", { bubbles: true }),
      );
      const prompt = $("#federlicht-prompt");
      if (prompt) {
        prompt.focus();
        prompt.setSelectionRange(prompt.value.length, prompt.value.length);
      }
    });
  });
}

function applyResumeStagesFromStage(stageId) {
  const target = String(stageId || "").trim().toLowerCase();
  if (!WORKFLOW_STAGE_ORDER.includes(target)) return false;
  const ordered = workflowStageOrder();
  const activeSet = new Set(state.workflow.selectedStages);
  activeSet.add(target);
  const selectedOrdered = ordered.filter((id) => activeSet.has(id));
  const startIdx = selectedOrdered.indexOf(target);
  if (startIdx < 0) return false;
  const resumeStages = selectedOrdered.slice(startIdx);
  if (!resumeStages.length) return false;
  const stagesCsv = resumeStages.join(",");
  const stageInput = $("#federlicht-stages");
  const skipInput = $("#federlicht-skip-stages");
  if (stageInput) stageInput.value = stagesCsv;
  if (skipInput) skipInput.value = "";
  state.pipeline.selected = new Set(resumeStages);
  state.pipeline.activeStageId = target;
  state.workflow.kind = "federlicht";
  state.workflow.running = false;
  state.workflow.resumeStage = target;
  state.workflow.historyMode = false;
  state.workflow.historySourcePath = "";
  state.workflow.completedSteps = new Set(["feather"]);
  state.workflow.activeStep = target;
  state.workflow.hasError = false;
  state.workflow.statusText = `Resume preset · ${workflowLabel(target)}`;
  state.workflow.mainStatusText = state.workflow.statusText;
  state.workflow.autoStages = new Set();
  state.workflow.autoStageReasons = {};
  state.workflow.passMetrics = [];
  renderPipelineChips();
  renderPipelineSelected();
  updatePipelineOutputs();
  renderStageDetail(target);
  appendLog(`[workflow] resume preset staged=${stagesCsv}\n`);
  return true;
}

async function draftWorkflowResumePrompt() {
  const runRel = normalizePathString(state.workflow.runRel || selectedRunRel() || "");
  if (!runRel) {
    appendLog("[workflow] resume prompt failed: run folder not resolved.\n");
    return;
  }
  const resumeStage = state.workflow.resumeStage || findWorkflowResumeStage();
  const latestReport = normalizePathString(state.workflow.resultPath || state.runSummary?.latest_report_rel || "");
  const updatePath = await nextUpdateRequestPath(runRel);
  if (!updatePath) {
    appendLog("[workflow] resume prompt failed: update prompt path not available.\n");
    return;
  }
  const lines = [
    "Resume update request:",
    `- Resume stage: ${resumeStage || "writer"}`,
    "- Goal: improve and continue from the latest run artifacts without losing validated context.",
    latestReport ? `- Base report: ${stripRunPrefix(latestReport, runRel) || latestReport}` : "- Base report: (none)",
    "",
    "Change requests (edit before run):",
    "1) [필수] 이번 재실행에서 강화할 관점/요구사항을 구체적으로 작성하세요.",
    "2) [선택] 제외하거나 축소할 섹션/주장을 적으세요.",
    "3) [선택] 반드시 추가할 근거 소스 유형(공식문서/최신자료/사례)을 적으세요.",
    "",
    "Execution guardrails:",
    "- Keep useful prior evidence; replace only stale or weak claims.",
    "- Preserve citation traceability and explicitly mark newly added evidence.",
    "- If quality issues remain, iterate with concrete edits (not full rewrite).",
  ];
  await saveInstructionContent(updatePath, lines.join("\n"));
  const promptFileInput = $("#federlicht-prompt-file");
  if (promptFileInput) {
    promptFileInput.value = updatePath;
  }
  state.workflow.resumePromptPath = updatePath;
  state.workflow.resumePromptStage = resumeStage || "writer";
  state.workflow.resumePromptAt = new Date().toISOString();
  promptFileTouched = true;
  await syncPromptFromFile(true).catch((err) => {
    appendLog(`[workflow] resume prompt load warning: ${err}\n`);
  });
  await loadFilePreview(updatePath).catch((err) => {
    appendLog(`[workflow] resume prompt preview warning: ${err}\n`);
  });
  const updateRel = stripRunPrefix(updatePath, runRel) || updatePath;
  setJobStatus(`Update request ready · ${updateRel}`, false);
  appendLog(`[workflow] resume prompt ready: ${updatePath}\n`);
  syncWorkflowHistoryControls();
}

function inferHistoryJobKind(path, kindHint = "") {
  const hinted = String(kindHint || "").trim().toLowerCase();
  if (hinted) return hinted;
  const lowered = normalizePathString(path || "").toLowerCase();
  if (lowered.includes("federlicht")) return "federlicht";
  if (lowered.includes("feather") || lowered.endsWith("_log.txt")) return "feather";
  return "log";
}

async function hydrateWorkflowFromHistory({ logPath, runRel, kind, logText }) {
  const historyKind = inferHistoryJobKind(logPath, kind);
  const normalizedRun = normalizePathString(runRel || selectedRunRel() || "");
  const text = String(logText || "");
  resetWorkflowState();
  state.workflow.kind = historyKind;
  state.workflow.running = false;
  state.workflow.historyMode = true;
  state.workflow.historySourcePath = normalizePathString(logPath || "");
  state.workflow.runRel = normalizedRun;
  state.workflow.stageOrder = currentPipelineStageOrder();
  state.workflow.statusText = "History";
  state.workflow.mainStatusText = state.workflow.statusText;
  if (historyKind === "federlicht") {
    const parsedFromLog = parseWorkflowHistoryFromLog(text);
    const stageStore = { ...parsedFromLog.stageStore };
    const summary = await loadRunWorkflowHistorySummary(normalizedRun);
    const parsedFromSummary = parseWorkflowHistoryFromSummary(summary);
    Object.entries(parsedFromSummary.stageStore).forEach(([stageId, payload]) => {
      mergeWorkflowStageStatus(stageStore, stageId, payload.status, payload.detail);
    });
    const mergedOrder = [];
    const seenOrder = new Set();
    parsedFromSummary.stageOrder.forEach((stageId) => {
      if (WORKFLOW_STAGE_ORDER.includes(stageId) && !seenOrder.has(stageId)) {
        seenOrder.add(stageId);
        mergedOrder.push(stageId);
      }
    });
    currentPipelineStageOrder().forEach((stageId) => {
      if (WORKFLOW_STAGE_ORDER.includes(stageId) && !seenOrder.has(stageId)) {
        seenOrder.add(stageId);
        mergedOrder.push(stageId);
      }
    });
    state.workflow.stageOrder = mergedOrder.length ? mergedOrder : currentPipelineStageOrder();
    state.workflow.selectedStages = new Set();
    state.workflow.completedSteps = new Set(["feather"]);
    state.workflow.historyStageStatus = {};
    state.workflow.historyFailedStage = "";
    state.workflow.autoStages = new Set();
    state.workflow.autoStageReasons = {};
    WORKFLOW_STAGE_ORDER.forEach((stageId) => {
      const snapshot = stageStore[stageId];
      const status = normalizeWorkflowStatusToken(snapshot?.status || "");
      const detail = String(snapshot?.detail || "").trim();
      if (!status) return;
      state.workflow.historyStageStatus[stageId] = status;
      if (status !== "disabled") {
        state.workflow.selectedStages.add(stageId);
      }
      if (["ran", "cached", "skipped", "done", "complete"].includes(status)) {
        state.workflow.completedSteps.add(stageId);
      }
      if (["error", "failed"].includes(status)) {
        state.workflow.hasError = true;
        if (!state.workflow.historyFailedStage) {
          state.workflow.historyFailedStage = stageId;
        }
      }
      const detailMeta = parseWorkflowDetailMeta(detail);
      if (detailMeta.autoRequired || detailMeta.autoRequiredBy.length) {
        state.workflow.autoStages.add(stageId);
        state.workflow.autoStageReasons[stageId] = detailMeta.autoRequiredBy.join(", ");
      }
    });
    if (!state.workflow.selectedStages.size) {
      selectedStagesInOrder().forEach((stageId) => state.workflow.selectedStages.add(stageId));
    }
    const latest = normalizePathString(state.runSummary?.latest_report_rel || "");
    if (latest) {
      state.workflow.resultPath = latest;
    } else if (parsedFromLog.resultPath) {
      state.workflow.resultPath = normalizePathString(parsedFromLog.resultPath);
    }
    if (parsedFromLog.hasError) {
      state.workflow.hasError = true;
    }
    const orderedSelected = workflowStageOrder().filter((id) => state.workflow.selectedStages.has(id));
    const nextPending = orderedSelected.find((id) => !state.workflow.completedSteps.has(id));
    if (nextPending) {
      state.workflow.resumeStage = nextPending;
      state.workflow.activeStep = nextPending;
      if (!state.workflow.historyFailedStage && state.workflow.hasError) {
        state.workflow.historyFailedStage = nextPending;
      }
      state.workflow.statusText = state.workflow.hasError
        ? `History · Failed near ${workflowLabel(nextPending)}`
        : `History · Resume ${workflowLabel(nextPending)}`;
    } else {
      state.workflow.resumeStage = orderedSelected.includes("writer")
        ? "writer"
        : (orderedSelected[0] || "");
      state.workflow.activeStep = "result";
      state.workflow.completedSteps.add("result");
      state.workflow.statusText = state.workflow.hasError
        ? "History · Failed"
        : "History · Finished";
    }
    state.workflow.mainStatusText = state.workflow.statusText;
    state.workflow.lastMainStageIndex = stageOrderIndex(state.workflow.activeStep);
    renderWorkflow();
    return;
  }
  const endDetected = /\bjob end\b/i.test(text) || /\[done\]/i.test(text);
  const failedDetected = /\bjob failed\b/i.test(text);
  if (historyKind === "feather") {
    state.workflow.completedSteps = endDetected ? new Set(["feather", "result"]) : new Set(["feather"]);
    state.workflow.activeStep = endDetected ? "result" : "feather";
    state.workflow.hasError = failedDetected;
    state.workflow.statusText = failedDetected ? "History · Feather failed" : "History · Feather";
    state.workflow.mainStatusText = state.workflow.statusText;
    renderWorkflow();
    return;
  }
  state.workflow.statusText = "History";
  state.workflow.mainStatusText = state.workflow.statusText;
  renderWorkflow();
}

function normalizeWorkflowResultPath(rawPath) {
  const candidate = normalizeLogPathCandidate(rawPath) || normalizePathString(rawPath);
  const normalized = normalizePathString(candidate);
  if (!normalized) return "";
  const workflowRun = normalizePathString(state.workflow.runRel || "");
  if (!workflowRun) return normalized;
  if (normalized.startsWith(`${workflowRun}/`)) return normalized;
  if (isRunScopedPath(normalized)) return `${workflowRun}/${normalized}`;
  return normalized;
}

function parseWorkflowResultPathFromLog(text) {
  const line = String(text || "").trim();
  if (!line) return "";
  const wroteMatch = line.match(/\bWrote report:\s*(.+)$/i);
  if (wroteMatch && wroteMatch[1]) {
    return normalizeWorkflowResultPath(wroteMatch[1]);
  }
  if (/\[workflow\]\s+stage=result\s+/i.test(line)) {
    const detailMatch = line.match(/\boutput(?:_path)?=([^,]+)(?:,|$)/i);
    if (detailMatch && detailMatch[1]) {
      return normalizeWorkflowResultPath(detailMatch[1]);
    }
  }
  return "";
}

function syncWorkflowResultPathFromLog(text) {
  const nextPath = parseWorkflowResultPathFromLog(text);
  if (!nextPath) return false;
  const currentPath = normalizePathString(state.workflow.resultPath || "");
  if (currentPath === nextPath) return false;
  state.workflow.resultPath = nextPath;
  return true;
}

function upsertWorkflowPassMetric(stageId, metric) {
  if (!metric || !Number.isFinite(Number(metric.pass))) return;
  const pass = Number(metric.pass);
  const items = Array.isArray(state.workflow.passMetrics) ? [...state.workflow.passMetrics] : [];
  const next = {
    stageId: stageId || "",
    pass,
    elapsedMs: Math.max(0, Number(metric.elapsedMs || 0)),
    estTokens: Math.max(0, Number(metric.estTokens || 0)),
    cacheHits: Math.max(0, Number(metric.cacheHits || 0)),
    runtime: String(metric.runtime || "").trim(),
  };
  const idx = items.findIndex((entry) => Number(entry.pass) === pass);
  if (idx >= 0) {
    items[idx] = { ...items[idx], ...next };
  } else {
    items.push(next);
  }
  items.sort((a, b) => Number(a.pass) - Number(b.pass));
  state.workflow.passMetrics = items.slice(-8);
}

function updateWorkflowFromLog(text) {
  if (!state.workflow.running || state.workflow.kind !== "federlicht") return;
  const resultPathChanged = syncWorkflowResultPathFromLog(text);
  const workflowEvent = parseWorkflowEvent(text);
  if (workflowEvent) {
    const { stageId, status } = workflowEvent;
    const detailMeta = parseWorkflowDetailMeta(workflowEvent.detail);
    if (detailMeta.passMetric) {
      upsertWorkflowPassMetric(stageId, detailMeta.passMetric);
    }
    if (detailMeta.autoRequired || detailMeta.autoRequiredBy.length) {
      state.workflow.autoStages.add(stageId);
      state.workflow.selectedStages.add(stageId);
      state.workflow.autoStageReasons[stageId] = detailMeta.autoRequiredBy.join(", ");
    }
    if (stageId === "result") {
      state.workflow.completedSteps = new Set([
        "feather",
        ...workflowStageOrder().filter((id) => state.workflow.selectedStages.has(id)),
      ]);
      state.workflow.activeStep = "result";
      state.workflow.statusText = "Streaming · Result";
      state.workflow.mainStatusText = state.workflow.statusText;
      state.workflow.lastMainStageIndex = -1;
      renderWorkflow();
      return;
    }
    if (!state.workflow.selectedStages.has(stageId) && status === "disabled") {
      renderWorkflow();
      return;
    }
    const nextIdx = stageOrderIndex(stageId);
    if (nextIdx >= 0) {
      const prevIdx = Number(state.workflow.lastMainStageIndex);
      if (Number.isFinite(prevIdx) && prevIdx >= 0 && nextIdx < prevIdx) {
        triggerWorkflowLoopback();
      }
      markWorkflowCompletedThroughStage(stageId);
      if (["ran", "cached", "skipped", "disabled"].includes(status)) {
        state.workflow.completedSteps.add(stageId);
        state.workflow.activeStep = nextSelectedWorkflowStage(stageId);
      } else {
        state.workflow.activeStep = stageId;
      }
      const statusStage = state.workflow.activeStep || stageId;
      state.workflow.statusText = `Streaming · ${workflowLabel(statusStage)}`;
      state.workflow.mainStatusText = state.workflow.statusText;
      state.workflow.lastMainStageIndex = nextIdx;
      renderWorkflow();
      return;
    }
  }
  const stageId = detectFederlichtStageFromLog(text);
  if (!stageId) {
    if (resultPathChanged) renderWorkflow();
    return;
  }
  if (stageId === "result") {
    state.workflow.completedSteps = new Set([
      "feather",
      ...workflowStageOrder().filter((id) => state.workflow.selectedStages.has(id)),
    ]);
    state.workflow.activeStep = "result";
    state.workflow.statusText = "Streaming · Result";
    state.workflow.mainStatusText = state.workflow.statusText;
    state.workflow.lastMainStageIndex = -1;
    renderWorkflow();
    return;
  }
  const nextIdx = stageOrderIndex(stageId);
  if (nextIdx < 0) return;
  const prevIdx = Number(state.workflow.lastMainStageIndex);
  if (Number.isFinite(prevIdx) && prevIdx >= 0 && nextIdx < prevIdx) {
    triggerWorkflowLoopback();
  }
  markWorkflowCompletedThroughStage(stageId);
  state.workflow.activeStep = stageId;
  state.workflow.statusText = `Streaming · ${workflowLabel(stageId)}`;
  state.workflow.mainStatusText = state.workflow.statusText;
  state.workflow.lastMainStageIndex = nextIdx;
  renderWorkflow();
}

function completeWorkflow(kind, returnCode, status = "") {
  const statusLower = String(status || "").toLowerCase();
  const failedByStatus = ["fail", "error", "killed", "cancel", "abort"].some((token) =>
    statusLower.includes(token),
  );
  let success = Number(returnCode) === 0;
  if (!Number.isFinite(Number(returnCode)) && statusLower) {
    success = !failedByStatus;
  }
  if (failedByStatus) {
    success = false;
  }
  if (kind === "federlicht" && state.workflow.kind === "federlicht") {
    const selected = workflowStageOrder().filter((id) => state.workflow.selectedStages.has(id));
    state.workflow.running = false;
    state.workflow.activeStep = "result";
    state.workflow.completedSteps = new Set(["feather", ...selected, "result"]);
    state.workflow.hasError = !success;
    state.workflow.statusText = success ? "Finished" : `Failed (rc=${returnCode ?? "?"})`;
    state.workflow.mainStatusText = state.workflow.statusText;
    state.workflow.lastMainStageIndex = -1;
    renderWorkflow();
    return;
  }
  if (kind === "feather" && state.workflow.kind === "feather") {
    state.workflow.running = false;
    state.workflow.activeStep = success ? "result" : "feather";
    state.workflow.completedSteps = success ? new Set(["feather", "result"]) : new Set();
    state.workflow.hasError = !success;
    state.workflow.statusText = success ? "Finished" : `Failed (rc=${returnCode ?? "?"})`;
    state.workflow.mainStatusText = state.workflow.statusText;
    state.workflow.lastMainStageIndex = -1;
    renderWorkflow();
    return;
  }
  completeWorkflowSpot(kind, returnCode, status);
}

function clearWorkflowIfIdle() {
  if (state.activeJobId) return;
  if ((state.workflow.spots || []).some((spot) => spot.running)) return;
  resetWorkflowState();
  renderWorkflow();
}

function renderWorkflow() {
  const host = $("#workflow-track");
  const status = $("#workflow-status");
  const extrasHost = $("#workflow-extras");
  const strip = $("#workflow-strip");
  if (!host || !status || !extrasHost || !strip) return;
  if (state.workflow.running || !workflowIsStageSelected("quality")) {
    state.workflow.qualityMenuOpen = false;
  }
  status.textContent = state.workflow.statusText || "Idle";
  status.classList.toggle("is-running", !!state.workflow.running);
  host.classList.toggle("is-running", !!state.workflow.running);
  const nodeOrder = workflowNodeOrder();
  const federhavBusy = Boolean(state.ask.busy || state.liveAsk.busy || state.activeJobPending);
  const federhavTouched = federhavBusy || normalizeLiveAskStoredHistory(state.liveAsk.history, 6).length > 0;
  const opsWrapNode = $("#workflow-ops-wrap");
  const opsOpen = opsWrapNode instanceof HTMLDetailsElement && opsWrapNode.open;
  const shouldCompactStrip = (
    !state.workflow.historyMode
    && !state.workflow.hasError
    && !opsOpen
  );
  strip.classList.toggle("is-idle-compact", shouldCompactStrip);
  const activeToolHint = latestActiveToolHint();
  host.innerHTML = nodeOrder.map((stepId, idx) => {
    const classes = ["workflow-node"];
    const isFederhav = stepId === "federhav";
    const isResult = stepId === "result";
    const isMainStage = WORKFLOW_STAGE_ORDER.includes(stepId);
    if (isFederhav) classes.push("is-governor");
    if (stepId === "feather") classes.push("is-ingest");
    if (isResult) classes.push("is-result");
    if (isMainStage) classes.push("is-agent");
    const selected = workflowIsStageSelected(stepId);
    const isAuto = state.workflow.autoStages.has(stepId);
    const isActive = isFederhav ? federhavBusy : state.workflow.activeStep === stepId;
    const isRunningNode = isFederhav ? isActive : (isActive && state.workflow.running);
    const isComplete = isFederhav ? federhavTouched : state.workflow.completedSteps.has(stepId);
    const isResumeTarget =
      state.workflow.historyMode
      && !state.workflow.running
      && state.workflow.kind === "federlicht"
      && state.workflow.resumeStage === stepId;
    if (!selected) classes.push("is-skipped");
    if (selected) classes.push("is-enabled");
    if (isAuto) classes.push("is-auto");
    if (isActive) classes.push("is-active");
    if (isComplete) classes.push("is-complete");
    if (isResumeTarget) classes.push("is-resume-target");
    if (!isActive && !isComplete) classes.push("is-pending");
    if (stepId === "result" && state.workflow.hasError) classes.push("is-error");
    const canEdit = !state.workflow.running && isMainStage;
    const nodeHint = workflowNodeHint(stepId);
    const previewPath = isResult ? normalizePathString(state.workflow.resultPath || "") : "";
    const openAttr = previewPath ? `data-workflow-open="${escapeHtml(previewPath)}"` : "";
    const stageAttr = (isMainStage || stepId === "feather" || isFederhav)
      ? `data-workflow-stage="${stepId}"`
      : "";
    const dragAttr = canEdit ? 'draggable="true"' : "";
    const autoReason = String(state.workflow.autoStageReasons?.[stepId] || "").trim();
    const autoTitle = autoReason
      ? `Auto-enabled by dependency (${autoReason})`
      : "Auto-enabled by dependency";
    const autoBadge = isAuto
      ? `<span class="workflow-node-auto" title="${escapeHtml(autoTitle)}">auto</span>`
      : "";
    const pathLabel = previewPath
      ? `<span class="workflow-node-path">${escapeHtml(stripSiteRunsPrefix(previewPath) || previewPath)}</span>`
      : "";
    const toolLabel = (isFederhav && activeToolHint)
      ? `<span class="workflow-node-tool" title="${escapeHtml(activeToolHint.message || activeToolHint.id || "")}">tool:${escapeHtml(activeToolHint.label || activeToolHint.id || "")}</span>`
      : "";
    let stateToken = "ready";
    if (stepId === "result" && state.workflow.hasError) {
      stateToken = "error";
    } else if (isResumeTarget) {
      stateToken = "resume";
    } else if (isRunningNode) {
      stateToken = "running";
    } else if (isComplete) {
      stateToken = "done";
    } else if (!selected) {
      stateToken = "off";
    } else if (state.workflow.running) {
      stateToken = "queued";
    }
    const stateLabelMap = {
      ready: "ready",
      queued: "queued",
      running: "running",
      done: "done",
      off: "off",
      resume: "resume",
      error: "error",
    };
    const showStateBadge = (
      stateToken === "running"
      || stateToken === "resume"
      || stateToken === "error"
      || (stepId === "result" && (stateToken === "done" || state.workflow.hasError))
    );
    const stateBadge = showStateBadge
      ? `<span class="workflow-node-state is-${stateToken}" title="${escapeHtml(
        `state: ${stateLabelMap[stateToken] || stateToken}`,
      )}">${escapeHtml(stateLabelMap[stateToken] || stateToken)}</span>`
      : "";
    const isQualityNode = stepId === "quality";
    const qualityIterations = getQualityIterations();
    const showLoop =
      isQualityNode
      && (state.workflow.kind === "federlicht" || workflowIsStageSelected("quality"))
      && workflowIsStageSelected("writer");
    const loopTitle = showLoop
      ? `Quality feedback loop-back (${qualityIterations} iteration${qualityIterations === 1 ? "" : "s"})`
      : "";
    const loopClasses = [
      "workflow-loop-arrow",
      state.workflow.loopbackPulse ? "is-pulse" : "",
      state.workflow.loopbackCount > 0 ? "is-seen" : "",
    ]
      .filter(Boolean)
      .join(" ");
    const loopBadge =
      state.workflow.loopbackCount > 0
        ? `<span class="workflow-loop-count">${escapeHtml(String(state.workflow.loopbackCount))}</span>`
        : "";
    const loopHtml = showLoop
      ? `<span class="${loopClasses}" title="${escapeHtml(loopTitle)}">
          <span class="workflow-loop-symbol">↺</span>
          ${loopBadge}
        </span>`
      : "";
    const qualityStageOn = workflowIsStageSelected("quality");
    const iterSelectDisabled = state.workflow.running || !qualityStageOn;
    const iterTriggerClasses = ["workflow-iter-trigger"];
    if (state.workflow.running && state.workflow.activeStep === "quality") {
      iterTriggerClasses.push("is-running");
    }
    if (!qualityStageOn) {
      iterTriggerClasses.push("is-off");
    }
    if (state.workflow.qualityMenuOpen && !iterSelectDisabled) {
      iterTriggerClasses.push("is-open");
    }
    const iterValues = Array.from({ length: 10 }, (_, idx) => idx + 1);
    const iterOptions = iterValues
      .map((value) => {
        const selected = value === qualityIterations ? "is-selected" : "";
        const label = `x${value}`;
        return (
          `<button type="button" class="workflow-iter-option ${selected}" data-workflow-quality-value="${value}">`
          + `${escapeHtml(label)}</button>`
        );
      })
      .join("");
    const menuOpen = state.workflow.qualityMenuOpen && !iterSelectDisabled;
    const qualityControls = isQualityNode
      ? `<span class="workflow-iter-wrap">
          <button
            type="button"
            class="${iterTriggerClasses.join(" ")}"
            data-workflow-quality-toggle="true"
            aria-label="Quality iterations"
            title="Quality iterations"
            aria-haspopup="listbox"
            aria-expanded="${menuOpen ? "true" : "false"}"
            ${iterSelectDisabled ? "disabled" : ""}
          >
            <span class="workflow-iter-label">${escapeHtml(`x${qualityIterations}`)}</span>
            <span class="workflow-iter-caret">▾</span>
          </button>
          <span class="workflow-iter-menu ${menuOpen ? "is-open" : ""}" role="listbox">
            ${iterOptions}
          </span>
        </span>`
      : "";
    const arrow = idx < nodeOrder.length - 1 ? '<span class="workflow-arrow">→</span>' : "";
    return `
      <span class="workflow-node-wrap">
        <button
          type="button"
          class="${classes.join(" ")}"
          data-workflow-node="${stepId}"
          title="${escapeHtml(nodeHint)}"
          ${stageAttr}
          ${openAttr}
          ${dragAttr}
        >
          <span class="workflow-node-label">${escapeHtml(workflowLabel(stepId))}</span>
          ${stateBadge}
          ${autoBadge}
          ${toolLabel}
          ${isResult ? pathLabel : ""}
        </button>
        ${loopHtml}
        ${qualityControls}
        ${arrow}
      </span>
    `;
  }).join("");
  const spots = state.workflow.spots || [];
  const metrics = Array.isArray(state.workflow.passMetrics) ? state.workflow.passMetrics : [];
  const metricHtml = metrics
    .map((item) => {
      const pass = Number(item.pass || 0);
      const elapsedMs = Number(item.elapsedMs || 0);
      const estTokens = Number(item.estTokens || 0);
      const cacheHits = Number(item.cacheHits || 0);
      const stageText = workflowLabel(item.stageId || "");
      const runtimeText = String(item.runtime || "").replaceAll("|", " > ");
      const elapsedLabel = elapsedMs >= 1000
        ? `${(elapsedMs / 1000).toFixed(1)}s`
        : `${elapsedMs}ms`;
      const tokenLabel = estTokens >= 1000
        ? `${(estTokens / 1000).toFixed(1)}k`
        : `${estTokens}`;
      const title = runtimeText
        ? `Runtime bundle: ${runtimeText}`
        : "Runtime bundle";
      return `
        <span class="workflow-metric" title="${escapeHtml(title)}">
          <span class="workflow-metric-pass">P${escapeHtml(String(pass))}</span>
          <span class="workflow-metric-stage">${escapeHtml(stageText)}</span>
          <span class="workflow-metric-stat">${escapeHtml(elapsedLabel)}</span>
          <span class="workflow-metric-stat">${escapeHtml(tokenLabel)} tok</span>
          <span class="workflow-metric-stat">cache ${escapeHtml(String(cacheHits))}</span>
        </span>
      `;
    })
    .join("");
  const spotHtml = spots
    .map((spot) => {
      const classes = [
        "workflow-spot",
        spot.running ? "is-running" : "",
        !spot.running && !spot.hasError ? "is-done" : "",
        spot.hasError ? "is-error" : "",
      ]
        .filter(Boolean)
        .join(" ");
      const label = spot.label || workflowSpotLabel(spot.kind);
      const path = normalizePathString(spot.path || "");
      const openAttr = path ? `data-workflow-open="${escapeHtml(path)}"` : "";
      const statusText = spot.running ? "running" : spot.hasError ? "failed" : "done";
      const pathLabel = path
        ? `<span class="workflow-spot-path">${escapeHtml(stripSiteRunsPrefix(path) || path)}</span>`
        : "";
      return `
        <button type="button" class="${classes}" data-workflow-spot="${escapeHtml(spot.id)}" ${openAttr}>
          <span class="workflow-spot-label">${escapeHtml(label)}</span>
          <span class="workflow-spot-state">${escapeHtml(statusText)}</span>
          ${pathLabel}
        </button>
      `;
    })
    .join("");
  extrasHost.innerHTML = `${metricHtml}${spotHtml}`;
  extrasHost.classList.toggle("is-empty", spots.length === 0 && metrics.length === 0);
  const statusToken = String(state.workflow.statusText || "").trim().toLowerCase();
  const compactIdle =
    !state.workflow.running
    && !state.workflow.historyMode
    && !state.workflow.hasError
    && spots.length === 0
    && metrics.length === 0
    && (!statusToken || statusToken === "idle");
  strip.classList.toggle("is-idle", compactIdle);
  const hasHistorySignals = Boolean(
    state.workflow.historyMode
    || state.workflow.resumeStage
    || state.workflow.historySourcePath
    || spots.length
    || metrics.length,
  );
  strip.classList.toggle("is-running", Boolean(state.workflow.running));
  strip.classList.toggle("has-error", Boolean(state.workflow.hasError));
  strip.classList.toggle("has-history", hasHistorySignals);
  const opsWrap = $("#workflow-ops-wrap");
  const showOps =
    !compactIdle
    && (
      state.workflow.historyMode
      || state.workflow.running
      || state.workflow.hasError
      || spots.length > 0
      || metrics.length > 0
    );
  if (opsWrap) {
    opsWrap.classList.toggle("is-empty", !showOps);
    if (!showOps) {
      opsWrap.open = false;
    } else if ((state.workflow.historyMode || state.workflow.hasError) && !opsWrap.open) {
      opsWrap.open = true;
    }
  }
  host.querySelectorAll("[data-workflow-open]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const relPath = btn.getAttribute("data-workflow-open") || "";
      if (!relPath) return;
      await loadFilePreview(relPath);
    });
  });
  host.querySelectorAll("[data-workflow-stage]").forEach((btn) => {
    const stageId = btn.getAttribute("data-workflow-stage") || "";
    if (!stageId) return;
    btn.addEventListener("click", () => {
      if (state.workflow.running) return;
      const isMainStageNode = STAGE_INDEX[stageId] !== undefined;
      const isFeatherNode = stageId === "feather";
      const isFederhavNode = stageId === "federhav";
      if (!isMainStageNode && !isFeatherNode && !isFederhavNode) return;
      state.pipeline.activeStageId = stageId;
      state.workflow.focusHintStage = stageId;
      if (isFederhavNode) {
        state.workflow.qualityMenuOpen = false;
        if (state.workflow.studioOpen) {
          renderWorkflowStudioPanel("overview");
        }
        setAskStatus("FederHav 단계 포커스. 아래 대화 입력창에서 질문/실행 요청을 이어가세요.");
        $("#live-ask-input")?.focus();
        renderWorkflow();
        return;
      }
      if (state.workflow.historyMode && state.workflow.kind === "federlicht" && isMainStageNode) {
        state.workflow.resumeStage = stageId;
        state.workflow.selectedStages.add(stageId);
        state.workflow.statusText = `History · Resume ${workflowLabel(stageId)}`;
        state.workflow.mainStatusText = state.workflow.statusText;
        state.workflow.qualityMenuOpen = false;
        if (state.workflow.studioOpen) {
          setWorkflowStudioOpen(true, { stageId: "overview" });
        }
        renderWorkflow();
        return;
      }
      state.workflow.qualityMenuOpen = false;
      if (state.workflow.studioOpen) {
        renderWorkflowStudioPanel("overview");
      }
      setAskStatus(`${workflowLabel(stageId)} 단계 포커스. 단계 on/off는 Workflow Studio의 Pipeline 선택에서 조정하세요.`);
      renderWorkflow();
    });
    btn.addEventListener("dblclick", () => {
      if (state.workflow.running) return;
      state.pipeline.activeStageId = stageId;
      state.workflow.focusHintStage = stageId;
      setWorkflowStudioOpen(true, { stageId: "overview" });
      setAskStatus("Workflow Studio를 열었습니다. 단계 on/off는 Pipeline 선택에서 조정하세요.");
    });
    btn.addEventListener("dragstart", (ev) => {
      if (state.workflow.running) return;
      state.pipeline.draggingId = stageId;
      btn.classList.add("dragging");
      ev.dataTransfer?.setData("text/plain", stageId);
      ev.dataTransfer?.setDragImage(btn, 12, 12);
    });
    btn.addEventListener("dragend", () => {
      state.pipeline.draggingId = null;
      btn.classList.remove("dragging");
    });
    btn.addEventListener("dragover", (ev) => {
      if (state.workflow.running) return;
      ev.preventDefault();
      const draggingId = state.pipeline.draggingId;
      if (!draggingId || draggingId === stageId) return;
      if ((!STAGE_INDEX[draggingId] && STAGE_INDEX[draggingId] !== 0)) return;
      state.pipeline.order = moveStageBefore(state.pipeline.order, draggingId, stageId);
      renderPipelineSelected();
      updatePipelineOutputs();
      renderWorkflow();
    });
  });
  host.querySelectorAll("[data-workflow-quality-toggle]").forEach((el) => {
    el.addEventListener("click", (ev) => {
      ev.preventDefault();
      ev.stopPropagation();
      if (state.workflow.running) return;
      if (!workflowIsStageSelected("quality")) return;
      state.workflow.qualityMenuOpen = !state.workflow.qualityMenuOpen;
      renderWorkflow();
    });
  });
  host.querySelectorAll("[data-workflow-quality-value]").forEach((el) => {
    el.addEventListener("click", (ev) => {
      ev.preventDefault();
      ev.stopPropagation();
      if (state.workflow.running) return;
      const value = Number.parseInt(el.getAttribute("data-workflow-quality-value") || "", 10);
      if (!Number.isFinite(value)) return;
      setQualityIterations(value);
      state.workflow.qualityMenuOpen = false;
      syncWorkflowQualityControls();
      renderWorkflow();
    });
  });
  extrasHost.querySelectorAll("[data-workflow-open]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const relPath = btn.getAttribute("data-workflow-open") || "";
      if (!relPath) return;
      await loadFilePreview(relPath);
    });
  });
  renderWorkflowStudioPanel(state.workflow.studioFocusStage || "overview");
  syncWorkflowQualityControls();
  syncWorkflowHistoryControls();
  recoverIdleJobControls();
}

function renderStageDetail(stageId) {
  const stage = String(stageId || "").trim().toLowerCase() || "overview";
  state.workflow.focusHintStage = stage;
  state.workflow.studioFocusStage = stage;
  if (WORKFLOW_STAGE_ORDER.includes(stage)) {
    state.workflow.stageOverrideStage = stage;
  }
  renderWorkflowStudioPanel(stage);
}

function renderPipelineChips() {
  const host = $("#pipeline-chips");
  if (!host) return;
  host.innerHTML = STAGE_DEFS.map((def) => {
    const active = state.pipeline.selected.has(def.id) ? "active" : "";
    return `<button type="button" class="pipeline-chip ${active}" data-stage-chip="${def.id}" title="${escapeHtml(def.desc)}">${escapeHtml(def.label)}</button>`;
  }).join("");
  host.querySelectorAll("[data-stage-chip]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-stage-chip");
      if (id) toggleStage(id);
    });
  });
}

function moveStageBefore(order, movingId, beforeId) {
  const next = order.filter((id) => id !== movingId);
  const beforeIdx = next.indexOf(beforeId);
  if (beforeIdx === -1) {
    next.push(movingId);
    return next;
  }
  next.splice(beforeIdx, 0, movingId);
  return next;
}

function renderPipelineSelected() {
  const host = $("#pipeline-selected");
  if (!host) return;
  host.innerHTML = "";
  host.style.display = "none";
}

function insertStageInOrder(id) {
  if (state.pipeline.order.includes(id)) return;
  const idx = STAGE_INDEX[id];
  let insertAt = state.pipeline.order.findIndex((stageId) => STAGE_INDEX[stageId] > idx);
  if (insertAt < 0) insertAt = state.pipeline.order.length;
  state.pipeline.order.splice(insertAt, 0, id);
}

function toggleStage(id) {
  const isActive = state.pipeline.selected.has(id);
  if (isActive) {
    state.pipeline.selected.delete(id);
  } else {
    state.pipeline.selected.add(id);
    insertStageInOrder(id);
  }
  state.pipeline.activeStageId = id;
  renderStageDetail(id);
  renderPipelineChips();
  renderPipelineSelected();
  updatePipelineOutputs();
}

function initPipelineFromInputs() {
  const canonicalOrder = STAGE_DEFS.map((s) => s.id);
  const stagesCsv = $("#federlicht-stages")?.value;
  const skipCsv = $("#federlicht-skip-stages")?.value;
  const explicitStages = parseStageCsv(stagesCsv);
  const explicitSkip = new Set(parseStageCsv(skipCsv));
  const preferredDefault = ["scout", "evidence", "plan", "writer", "quality"].filter(
    (id) => STAGE_INDEX[id] !== undefined,
  );
  const stored = loadWorkflowPreferences();
  const storedOrder = stored?.order?.length ? stored.order : [];
  const storedSelected = stored?.selected?.length ? stored.selected : [];
  const defaultStages = storedSelected.length
    ? storedSelected
    : explicitStages.length
      ? explicitStages
    : explicitSkip.size
      ? canonicalOrder.filter((id) => !explicitSkip.has(id))
      : preferredDefault;
  if (storedOrder.length) {
    const seen = new Set(storedOrder);
    const remaining = canonicalOrder.filter((id) => !seen.has(id));
    state.pipeline.order = [...storedOrder, ...remaining];
  } else if (explicitStages.length) {
    const seen = new Set(explicitStages);
    const remaining = canonicalOrder.filter((id) => !seen.has(id));
    state.pipeline.order = [...explicitStages, ...remaining];
  } else {
    state.pipeline.order = [...canonicalOrder];
  }
  state.pipeline.selected = new Set(defaultStages);
  defaultStages.forEach((id) => insertStageInOrder(id));
  if (stored && Number.isFinite(stored.quality_iterations)) {
    setQualityIterations(stored.quality_iterations);
  }
  state.pipeline.activeStageId = defaultStages[0] || STAGE_DEFS[0]?.id || null;
  state.workflow.stageOverrideStage = state.pipeline.activeStageId || "scout";
  renderPipelineChips();
  renderPipelineSelected();
  renderStageDetail(state.pipeline.activeStageId);
  updatePipelineOutputs();
  renderWorkflowStudioPanel(state.pipeline.activeStageId);
}

function normalizeLogText(text, opts = {}) {
  const ensureTrailingNewline = Boolean(opts.ensureTrailingNewline);
  if (!text) return "";
  const raw = String(text).replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  if (!raw) return "";
  const trimmed = raw.trim();
  if (trimmed.toLowerCase() === "[reducer]") {
    return "";
  }
  const normalized = raw;
  if (ensureTrailingNewline && !normalized.endsWith("\n")) {
    return `${normalized}\n`;
  }
  return normalized;
}

function setLogBufferFromText(text) {
  const content = String(text || "");
  const lines = content.split(/\r?\n/);
  const buffer = lines.map((line, idx) => {
    if (idx === lines.length - 1 && line === "") return "";
    return normalizeLogText(line, { ensureTrailingNewline: true });
  });
  state.logBuffer = buffer.slice(-LOG_LINE_LIMIT);
  scheduleLogRender(true);
}

function isNearBottom(el, threshold = 40) {
  if (!el) return false;
  const delta = el.scrollHeight - el.scrollTop - el.clientHeight;
  return delta <= threshold;
}

function activeLogElement() {
  return $("#log-output-md");
}

function stripLogTokenWrapping(value) {
  let token = String(value || "").trim();
  if (!token) return "";
  token = token.replace(/^[`"'(<\[{]+/, "");
  token = token.replace(/[>"'`)\]}.,;!?]+$/, "");
  return token;
}

function isRunScopedPath(pathValue) {
  const lowered = String(pathValue || "").toLowerCase();
  return RUN_SCOPED_DIR_PREFIXES.some((prefix) => lowered.startsWith(prefix));
}

function normalizeLogPathCandidate(rawToken) {
  let token = stripLogTokenWrapping(rawToken);
  if (!token) return "";
  if (token.includes("://")) return "";
  token = token.replaceAll("\\", "/");
  token = token.replace(/^\.\/+/, "");
  if (token.startsWith("file:///")) {
    token = token.slice("file:///".length);
  }
  const rootAbs = normalizePathString(state.info?.root_abs || "");
  const normalizedToken = normalizePathString(token);
  if (/^[a-z]:\//i.test(normalizedToken)) {
    if (rootAbs && normalizedToken.startsWith(`${rootAbs}/`)) {
      return normalizedToken.slice(rootAbs.length + 1);
    }
    const loweredToken = normalizedToken.toLowerCase();
    const runRoots = Array.isArray(state.info?.run_roots) ? state.info.run_roots : [];
    for (const root of runRoots) {
      const normalizedRoot = normalizePathString(root).toLowerCase();
      if (!normalizedRoot) continue;
      const marker = `/${normalizedRoot}/`;
      const pos = loweredToken.indexOf(marker);
      if (pos >= 0) {
        return normalizedToken.slice(pos + 1);
      }
    }
    const runsPos = loweredToken.indexOf("/runs/");
    if (runsPos >= 0) {
      return normalizedToken.slice(runsPos + 1);
    }
    return normalizedToken;
  }
  const sanitized = normalizedToken
    .replace(/:(\d+)(?:-(\d+)|:(\d+))?$/, "")
    .replace(/#L\d+(?:C\d+)?$/i, "");
  if (token.startsWith("/")) {
    const trimmed = normalizePathString(sanitized.replace(/^\/+/, ""));
    if (!trimmed) return "";
    if (isRunScopedPath(trimmed)) {
      const workflowRunRel =
        state.workflow.running && state.workflow.kind === "federlicht"
          ? state.workflow.runRel
          : "";
      const runRel = normalizePathString(workflowRunRel || selectedRunRel() || state.runSummary?.run_rel || "");
      if (runRel) return `${normalizePathString(runRel)}/${trimmed}`;
    }
    return trimmed;
  }
  if (sanitized.startsWith("site/") || sanitized.startsWith("examples/")) {
    return sanitized;
  }
  if (isRunScopedPath(sanitized)) {
    const workflowRunRel =
      state.workflow.running && state.workflow.kind === "federlicht"
        ? state.workflow.runRel
        : "";
    const runRel = normalizePathString(workflowRunRel || selectedRunRel() || state.runSummary?.run_rel || "");
    if (runRel) {
      return `${normalizePathString(runRel)}/${sanitized}`;
    }
  }
  return sanitized;
}

function isLikelyPreviewFilePath(pathValue) {
  const normalized = normalizePathString(pathValue);
  if (!normalized || normalized.endsWith("/")) return false;
  const name = normalized.split("/").pop() || "";
  if (!name || !name.includes(".")) return false;
  if (normalized.includes("://")) return false;
  return true;
}

function renderRawLineSourceCitations(lineText) {
  const line = String(lineText || "");
  if (!/\[S\d+\]/i.test(line)) return null;
  const sourceTokenRegex = /\[S\d+\]\s+[\s\S]*?(?=(?:\s+\[S\d+\]\s+)|$)/gi;
  const matches = [...line.matchAll(sourceTokenRegex)];
  if (!matches.length) return null;
  let cursor = 0;
  let html = "";
  let linkedCount = 0;
  for (const match of matches) {
    const index = Number(match.index ?? -1);
    const token = String(match[0] || "").trim();
    if (index < 0 || !token) continue;
    html += escapeHtml(line.slice(cursor, index));
    const parsed = parseLogSourceToken(token);
    if (parsed) {
      linkedCount += 1;
      html += `<a href="#" class="log-link" data-log-path="${escapeHtml(
        parsed.normalizedPath,
      )}" data-log-start="${parsed.start > 0 ? parsed.start : ""}" data-log-end="${
        parsed.end > 0 ? parsed.end : ""
      }" title="Open in File Preview">${escapeHtml(parsed.label)}</a>`;
    } else {
      html += escapeHtml(token);
    }
    cursor = index + match[0].length;
  }
  html += escapeHtml(line.slice(cursor));
  return linkedCount > 0 ? html : null;
}

function renderRawLineWithLinks(lineText) {
  const line = String(lineText || "");
  const citationHtml = renderRawLineSourceCitations(line);
  if (citationHtml) return citationHtml;
  const tokenRe =
    /(?:[A-Za-z]:[\\/][^\s"'`<>()\[\]{}]+|(?:\.{0,2}\/)?[^\s"'`<>()\[\]{}]+\/[^\s"'`<>()\[\]{}]+(?:\/[^\s"'`<>()\[\]{}]+)*)/g;
  let cursor = 0;
  let html = "";
  const splitTrailingPunctuation = (token) => {
    const match = String(token || "").match(/^(.*?)([)\],.;!?]+)?$/);
    return {
      body: String(match?.[1] || token || ""),
      suffix: String(match?.[2] || ""),
    };
  };
  for (const match of line.matchAll(tokenRe)) {
    const index = match.index ?? -1;
    const rawToken = match[0] || "";
    if (index < 0 || !rawToken) continue;
    html += escapeHtml(line.slice(cursor, index));
    const { body, suffix } = splitTrailingPunctuation(rawToken);
    if (/^https?:\/\//i.test(body)) {
      html += `<a href="${escapeHtml(body)}" class="log-link" data-log-url="${escapeHtml(
        body,
      )}" target="_blank" rel="noopener noreferrer">${escapeHtml(body)}</a>${escapeHtml(suffix)}`;
    } else {
      const lineRangeMatch = String(body || "").match(/:(\d+)(?:-(\d+)|:(\d+))?$/);
      const lineStart = Number(lineRangeMatch?.[1] || 0);
      const lineEnd = Number(lineRangeMatch?.[2] || lineRangeMatch?.[3] || lineRangeMatch?.[1] || 0);
      const normalizedPath = normalizeLogPathCandidate(body);
      if (isLikelyPreviewFilePath(normalizedPath)) {
        html += `<a href="#" class="log-link" data-log-path="${escapeHtml(
          normalizedPath,
        )}" data-log-start="${lineStart > 0 ? lineStart : ""}" data-log-end="${
          lineEnd > 0 ? lineEnd : ""
        }" title="Open in File Preview">${escapeHtml(body)}</a>${escapeHtml(suffix)}`;
      } else {
        html += escapeHtml(rawToken);
      }
    }
    cursor = index + rawToken.length;
  }
  html += escapeHtml(line.slice(cursor));
  return html;
}

function renderRawLogWithLinks(rawText) {
  return String(rawText || "")
    .split("\n")
    .map((line) => renderRawLineWithLinks(line))
    .join("\n");
}

function escapeMarkdownLinkLabel(value) {
  return String(value || "")
    .replaceAll("\\", "\\\\")
    .replaceAll("[", "\\[")
    .replaceAll("]", "\\]");
}

function encodeMarkdownHref(value) {
  return encodeURI(String(value || ""))
    .replaceAll("(", "%28")
    .replaceAll(")", "%29");
}

function linkifyRawLogLineForMarkdown(lineText) {
  const line = String(lineText || "");
  if (!line.trim()) return line;
  const sourceTokenRegex = /\[S\d+\]\s+[\s\S]*?(?=(?:\s+\[S\d+\]\s+)|$)/gi;
  let processed = line.replace(sourceTokenRegex, (token) => {
    const parsed = parseLogSourceToken(token);
    if (!parsed) return token;
    let href = parsed.normalizedPath;
    if (parsed.start > 0) {
      const end = parsed.end > parsed.start ? parsed.end : parsed.start;
      href = `${href}:${parsed.start}${end > parsed.start ? `-${end}` : ""}`;
    }
    return `[${escapeMarkdownLinkLabel(parsed.markdownLabel || parsed.label)}](${encodeMarkdownHref(href)})`;
  });
  const tokenRe =
    /(?:[A-Za-z]:[\\/][^\s"'`<>()\[\]{}]+|(?:\.{0,2}\/)?[^\s"'`<>()\[\]{}]+\/[^\s"'`<>()\[\]{}]+(?:\/[^\s"'`<>()\[\]{}]+)*)/g;
  const existingLinkRanges = [];
  for (const match of processed.matchAll(/\[[^\]]+\]\([^)\s]+\)/g)) {
    const start = Number(match.index ?? -1);
    if (start < 0) continue;
    existingLinkRanges.push({ start, end: start + String(match[0] || "").length });
  }
  const isInsideExistingLink = (start, end) =>
    existingLinkRanges.some((range) => start >= range.start && end <= range.end);
  const splitTrailingPunctuation = (token) => {
    const match = String(token || "").match(/^(.*?)([)\],.;!?]+)?$/);
    return {
      body: String(match?.[1] || token || ""),
      suffix: String(match?.[2] || ""),
    };
  };
  let cursor = 0;
  let output = "";
  for (const match of processed.matchAll(tokenRe)) {
    const index = Number(match.index ?? -1);
    const rawToken = String(match[0] || "");
    if (index < 0 || !rawToken) continue;
    output += processed.slice(cursor, index);
    const end = index + rawToken.length;
    if (isInsideExistingLink(index, end)) {
      output += rawToken;
      cursor = end;
      continue;
    }
    const { body, suffix } = splitTrailingPunctuation(rawToken);
    if (/^https?:\/\//i.test(body)) {
      output += `[${escapeMarkdownLinkLabel(body)}](${encodeMarkdownHref(body)})${suffix}`;
      cursor = end;
      continue;
    }
    const lineRangeMatch = String(body || "").match(/:(\d+)(?:-(\d+)|:(\d+))?$/);
    const lineStart = Number(lineRangeMatch?.[1] || 0);
    const lineEnd = Number(lineRangeMatch?.[2] || lineRangeMatch?.[3] || lineRangeMatch?.[1] || 0);
    const normalizedPath = normalizeLogPathCandidate(body);
    if (!isLikelyPreviewFilePath(normalizedPath)) {
      output += rawToken;
      cursor = end;
      continue;
    }
    let href = normalizedPath;
    if (lineStart > 0) {
      const resolvedEnd = lineEnd > lineStart ? lineEnd : lineStart;
      href = `${href}:${lineStart}${resolvedEnd > lineStart ? `-${resolvedEnd}` : ""}`;
    }
    output += `[${escapeMarkdownLinkLabel(body)}](${encodeMarkdownHref(href)})${suffix}`;
    cursor = end;
  }
  output += processed.slice(cursor);
  return output;
}

function linkifyRawLogForMarkdown(rawText) {
  return String(rawText || "")
    .split("\n")
    .map((line) => linkifyRawLogLineForMarkdown(line))
    .join("\n");
}

function normalizeWorkflowStageToken(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9_]/g, "");
}

function workflowStageMeta(stageToken) {
  const stage = normalizeWorkflowStageToken(stageToken);
  const map = {
    feather: { label: "Feather", icon: "F" },
    scout: { label: "Scout", icon: "S" },
    plan: { label: "Plan", icon: "P" },
    evidence: { label: "Evidence", icon: "E" },
    writer: { label: "Writer", icon: "W" },
    quality: { label: "Quality", icon: "Q" },
    clarifier: { label: "Clarifier", icon: "C" },
    templateadjust: { label: "Template", icon: "T" },
  };
  return map[stage] || { label: stageToken || "Stage", icon: "•" };
}

function workflowStatusMeta(statusToken) {
  const status = String(statusToken || "").trim().toLowerCase();
  if (!status) return { label: "active", className: "active" };
  if (["ok", "done", "ran", "completed", "success", "finished"].includes(status)) {
    return { label: status, className: "success" };
  }
  if (["cached", "cache", "reuse"].includes(status)) {
    return { label: status, className: "cached" };
  }
  if (["pending", "queued", "waiting", "running", "active"].includes(status)) {
    return { label: status, className: "active" };
  }
  if (["skipped", "disabled"].includes(status)) {
    return { label: status, className: "skipped" };
  }
  if (["error", "failed", "failure"].includes(status)) {
    return { label: status, className: "error" };
  }
  if (["resume", "resumed", "preset", "plan"].includes(status)) {
    return { label: status, className: "resume" };
  }
  return { label: status, className: "active" };
}

function parseWorkflowStageEvents(lineText) {
  const text = String(lineText || "").trim();
  if (!text) return [];
  let rawStages = "";
  let status = "";
  const stageMatch = text.match(/\bstage=([a-z0-9_,-]+)/i);
  const stagedMatch = text.match(/\bstaged=([a-z0-9_,-]+)/i);
  const planMatch = text.match(/\bexecution_plan=([a-z0-9_,-]+)/i);
  const statusMatch = text.match(/\bstatus=([a-z0-9_/-]+)/i);
  if (stageMatch && stageMatch[1]) {
    rawStages = stageMatch[1];
    status = statusMatch?.[1] || "";
  } else if (stagedMatch && stagedMatch[1]) {
    rawStages = stagedMatch[1];
    status = statusMatch?.[1] || "resume";
  } else if (planMatch && planMatch[1]) {
    rawStages = planMatch[1];
    status = statusMatch?.[1] || "plan";
  } else {
    return [];
  }
  return rawStages
    .split(",")
    .map((token) => token.trim())
    .filter(Boolean)
    .map((token) => {
      const stage = normalizeWorkflowStageToken(token);
      const stageInfo = workflowStageMeta(stage);
      const statusInfo = workflowStatusMeta(status);
      return {
        stage,
        stageLabel: stageInfo.label,
        icon: stageInfo.icon,
        status: statusInfo.label,
        statusClass: statusInfo.className,
      };
    });
}

function renderWorkflowTimelineFromLines(lines) {
  const events = [];
  const seen = new Set();
  for (const line of lines || []) {
    for (const event of parseWorkflowStageEvents(line)) {
      const key = `${event.stage}:${event.status}`;
      if (seen.has(key)) continue;
      seen.add(key);
      events.push(event);
    }
  }
  if (!events.length) return "";
  return `<div class="log-workflow-timeline">${events
    .map((event, idx) => {
      const node = `
        <span class="log-workflow-node status-${escapeHtml(event.statusClass)}">
          <span class="log-workflow-icon">${escapeHtml(event.icon)}</span>
          <span class="log-workflow-stage">${escapeHtml(event.stageLabel)}</span>
          <span class="log-workflow-state">${escapeHtml(event.status)}</span>
        </span>
      `;
      if (idx >= events.length - 1) return node;
      return `${node}<span class="log-workflow-arrow" aria-hidden="true">→</span>`;
    })
    .join("")}</div>`;
}

function classifyLogEntryLine(rawLine) {
  const line = String(rawLine || "");
  const trimmed = line.trim();
  if (!trimmed) return { kind: "blank", text: "" };
  const runAgentMatch = trimmed.match(/^\[run-agent:(user|assistant|sources|done|action|activity)\]\s*(.*)$/i);
  if (runAgentMatch) {
    const role = String(runAgentMatch[1] || "").toLowerCase();
    const text = String(runAgentMatch[2] || "");
    if (role === "user") return { kind: "user", label: "User", text, merge: false, mergeKey: "user" };
    if (role === "assistant") {
      return { kind: "assistant", label: currentAskAgentDisplayName(), text, merge: true, mergeKey: "assistant" };
    }
    if (role === "sources") return { kind: "sources", label: "Sources", text, merge: false, mergeKey: "sources" };
    if (role === "action") return { kind: "action", label: "Action", text, merge: true, mergeKey: "action" };
    if (role === "activity") return { kind: "activity", label: "Activity", text, merge: true, mergeKey: "activity" };
    return { kind: "done", label: "Run Summary", text, merge: false, mergeKey: "done" };
  }
  const workflowMatch = trimmed.match(/^\[workflow\]\s*(.*)$/i);
  if (workflowMatch) {
    return {
      kind: "workflow",
      label: "Workflow",
      text: String(workflowMatch[1] || "").trim(),
      merge: true,
      mergeKey: "workflow",
    };
  }
  const taggedLine = trimmed.match(/^\[([^\]]+)\]\s*(.+)$/);
  if (taggedLine) {
    const actor = String(taggedLine[1] || "").trim();
    const text = String(taggedLine[2] || "");
    const actorToken = actor.toLowerCase();
    const mappedKind = actorToken === "feather"
      ? "feather"
      : actorToken === "federlicht"
        ? "federlicht"
        : actorToken === "federhav"
          ? "assistant"
          : (actorToken === "capability" || actorToken === "tool" || actorToken === "tools")
            ? "tool"
            : "tag";
    return {
      kind: mappedKind,
      label: actor || "Log",
      text,
      merge: true,
      mergeKey: `${mappedKind}:${actor.toLowerCase()}`,
    };
  }
  if (trimmed.startsWith("$ ")) {
    return { kind: "command", label: "Command", text: line, merge: false, mergeKey: "command" };
  }
  const sectionMatch = trimmed.match(/^\[([^\]]+)\]\s*$/);
  if (sectionMatch) {
    return {
      kind: "section",
      label: String(sectionMatch[1] || "Section").trim(),
      text: "",
      merge: false,
      mergeKey: `section:${String(sectionMatch[1] || "section").trim().toLowerCase()}`,
    };
  }
  return { kind: "text", label: "Log", text: line, merge: true, mergeKey: "text" };
}

function buildStructuredLogEntries(rawText) {
  const lines = String(rawText || "").split("\n");
  const entries = [];
  let current = null;
  const flush = () => {
    if (!current) return;
    entries.push(current);
    current = null;
  };
  for (const rawLine of lines) {
    const parsed = classifyLogEntryLine(rawLine);
    if (parsed.kind === "blank") {
      if (current) current.lines.push("");
      continue;
    }
    if (parsed.kind === "section") {
      flush();
      current = {
        kind: "section",
        label: parsed.label,
        lines: [],
      };
      continue;
    }
    if (
      current
      && current.kind === parsed.kind
      && current.label === parsed.label
      && current.mergeKey === parsed.mergeKey
      && parsed.merge
      && parsed.kind !== "user"
      && parsed.kind !== "done"
      && parsed.kind !== "command"
    ) {
      current.lines.push(parsed.text);
      continue;
    }
    if (current && current.kind === "section" && parsed.kind === "text") {
      current.lines.push(parsed.text);
      continue;
    }
    flush();
    current = {
      kind: parsed.kind,
      label: parsed.label,
      lines: [parsed.text],
      mergeKey: parsed.mergeKey || parsed.kind,
    };
  }
  flush();
  if (entries.length > 300) {
    return entries.slice(entries.length - 300);
  }
  return entries;
}

function foldRunAgentTurns(entries) {
  const out = [];
  let turn = null;
  const flushTurn = () => {
    if (!turn) return;
    out.push(turn);
    turn = null;
  };
  for (const entry of entries || []) {
    const kind = String(entry?.kind || "");
    const isRunAgent = ["user", "assistant", "sources", "done", "action", "activity"].includes(kind);
    if (!isRunAgent) {
      flushTurn();
      out.push(entry);
      continue;
    }
    if (kind === "user") {
      flushTurn();
      turn = {
        kind: "agent-turn",
        label: `${currentAskAgentDisplayName()} Turn`,
        userLines: [...(entry.lines || [])],
        assistantLines: [],
        sourceLines: [],
        actionLines: [],
        activityLines: [],
        doneLines: [],
      };
      continue;
    }
    if (!turn) {
      turn = {
        kind: "agent-turn",
        label: `${currentAskAgentDisplayName()} Turn`,
        userLines: [],
        assistantLines: [],
        sourceLines: [],
        actionLines: [],
        activityLines: [],
        doneLines: [],
      };
    }
    if (kind === "assistant") turn.assistantLines.push(...(entry.lines || []));
    if (kind === "sources") turn.sourceLines.push(...(entry.lines || []));
    if (kind === "action") turn.actionLines.push(...(entry.lines || []));
    if (kind === "activity") turn.activityLines.push(...(entry.lines || []));
    if (kind === "done") turn.doneLines.push(...(entry.lines || []));
  }
  flushTurn();
  return out;
}

function parseRunAgentDoneMeta(lines) {
  const merged = String((lines || []).join(" ")).trim();
  const backend = (merged.match(/\bbackend=([^\s]+)/i) || [])[1] || "";
  const model = (merged.match(/\bmodel=([^\s]+)/i) || [])[1] || "";
  const indexed = (merged.match(/\bindexed=([0-9]+)/i) || [])[1] || "";
  const traceId = (merged.match(/\btrace=([^\s]+)/i) || [])[1] || "";
  const tools = (merged.match(/\btools=([0-9]+)/i) || [])[1] || "";
  const error = (merged.match(/\berror=(.+)$/i) || [])[1] || "";
  return {
    backend: String(backend || "").trim(),
    model: String(model || "").trim(),
    indexed: String(indexed || "").trim(),
    trace_id: String(traceId || "").trim(),
    tools: String(tools || "").trim(),
    error: String(error || "").trim(),
  };
}

function renderRunAgentTurn(entry) {
  const agentLabel = currentAskAgentDisplayName();
  const userText = String((entry.userLines || []).join("\n")).trim();
  const assistantText = String((entry.assistantLines || []).join("\n")).trim();
  const actionText = String((entry.actionLines || []).join("\n")).trim();
  const activityText = String((entry.activityLines || []).join("\n")).trim();
  const sourcesHtml = (entry.sourceLines || []).length
    ? renderSourcesInlineChips((entry.sourceLines || []).join(" | "), { limit: 6 })
    : "";
  const done = parseRunAgentDoneMeta(entry.doneLines || []);
  const metaChips = [
    done.backend ? `<span class="log-agent-meta-chip">backend=${escapeHtml(done.backend)}</span>` : "",
    done.model ? `<span class="log-agent-meta-chip">model=${escapeHtml(done.model)}</span>` : "",
    done.indexed ? `<span class="log-agent-meta-chip">indexed=${escapeHtml(done.indexed)}</span>` : "",
    done.trace_id ? `<span class="log-agent-meta-chip">trace=${escapeHtml(done.trace_id)}</span>` : "",
    done.tools ? `<span class="log-agent-meta-chip">tools=${escapeHtml(done.tools)}</span>` : "",
    done.error ? `<span class="log-agent-meta-chip is-error">error=${escapeHtml(done.error)}</span>` : "",
  ]
    .filter(Boolean)
    .join("");
  const userBlock = userText
    ? `
      <div class="log-agent-msg user">
        <div class="log-agent-msg-head"><span>User</span></div>
        <div class="log-agent-msg-body">${userText.split("\n").map((line) => `<div class="log-line">${renderRawLineWithLinks(line)}</div>`).join("")}</div>
      </div>
    `
    : "";
  const assistantBlock = assistantText
    ? `
      <div class="log-agent-msg assistant">
        <div class="log-agent-msg-head"><span>${escapeHtml(agentLabel)}</span></div>
        <div class="log-agent-msg-body">${assistantText.split("\n").map((line) => `<div class="log-line">${renderRawLineWithLinks(line)}</div>`).join("")}</div>
      </div>
    `
    : "";
  const actionBlock = actionText
    ? `
      <div class="log-agent-action">
        <strong>Action</strong>
        ${actionText.split("\n").map((line) => `<div class="log-line">${renderRawLineWithLinks(line)}</div>`).join("")}
      </div>
    `
    : "";
  const activityBlock = activityText
    ? `
      <div class="log-agent-action">
        <strong>Tool Trace</strong>
        ${activityText.split("\n").map((line) => `<div class="log-line">${renderRawLineWithLinks(line)}</div>`).join("")}
      </div>
    `
    : "";
  const doneBlock = metaChips
    ? `<div class="log-agent-meta">${metaChips}</div>`
    : "";
  return `
    <article class="log-entry role-agent-turn is-inline">
      <div class="log-entry-body log-agent-turn">
        ${userBlock}
        ${assistantBlock}
        ${actionBlock}
        ${activityBlock}
        ${sourcesHtml ? `<div class="log-agent-sources">${sourcesHtml}</div>` : ""}
        ${doneBlock}
      </div>
    </article>
  `;
}

function parseLogSourceToken(token) {
  let raw = String(token || "").trim();
  if (!raw) return null;
  raw = raw.replace(/(?:\s*[|;])+$/g, "").trim();
  if (!raw) return null;
  let sourceId = "";
  let remainder = raw;
  const sourceIdMatch = raw.match(/^\[?(S\d+)\]?\s+(.+)$/i);
  if (sourceIdMatch) {
    sourceId = String(sourceIdMatch[1] || "").toUpperCase();
    remainder = String(sourceIdMatch[2] || "").trim();
  }
  let pathToken = remainder;
  let start = 0;
  let end = 0;
  const rangeMatch = remainder.match(/^(.*):(\d+)(?:-(\d+)|:(\d+))?$/);
  if (rangeMatch && String(rangeMatch[1] || "").trim()) {
    pathToken = String(rangeMatch[1] || "").trim();
    start = Number(rangeMatch[2] || 0);
    end = Number(rangeMatch[3] || rangeMatch[4] || rangeMatch[2] || 0);
  }
  const normalizedPath = normalizeLogPathCandidate(pathToken);
  if (!isLikelyPreviewFilePath(normalizedPath)) return null;
  const rangeText = start > 0 ? `${start}-${end > 0 ? end : start}` : "-";
  const label = sourceId ? `[${sourceId}] ${pathToken}:${rangeText}` : `${pathToken}:${rangeText}`;
  const markdownLabel = sourceId ? `${sourceId} ${pathToken}:${rangeText}` : `${pathToken}:${rangeText}`;
  return { normalizedPath, start, end, label, markdownLabel };
}

function renderSourcesInlineChips(text, options = {}) {
  const rawText = String(text || "");
  const limitRaw = Number(options?.limit);
  const visibleLimit = Number.isFinite(limitRaw) && limitRaw > 0 ? Math.floor(limitRaw) : 8;
  let tokens = [];
  const sourceTokenRegex = /\[S\d+\]\s+[\s\S]*?(?=(?:\s+\[S\d+\]\s+)|$)/gi;
  let sourceMatch = sourceTokenRegex.exec(rawText);
  while (sourceMatch) {
    const token = String(sourceMatch[0] || "").trim();
    if (token) tokens.push(token);
    sourceMatch = sourceTokenRegex.exec(rawText);
  }
  if (!tokens.length) {
    tokens = rawText
      .split(/\s+\|\s+/)
      .map((item) => item.trim())
      .filter(Boolean);
  }
  if (!tokens.length) {
    return '<div class="log-line">-</div>';
  }
  const renderToken = (token) => {
    const parsed = parseLogSourceToken(token);
    if (!parsed) {
      return `<span class="log-source-chip">${renderRawLineWithLinks(token)}</span>`;
    }
    return `<span class="log-source-chip"><a href="#" class="log-link" data-log-path="${escapeHtml(
      parsed.normalizedPath,
    )}" data-log-start="${parsed.start > 0 ? parsed.start : ""}" data-log-end="${
      parsed.end > 0 ? parsed.end : ""
    }" title="Open in File Preview">${escapeHtml(parsed.label)}</a></span>`;
  };
  if (tokens.length <= visibleLimit) {
    return `<div class="log-source-list">${tokens.map((token) => renderToken(token)).join("")}</div>`;
  }
  const visible = tokens.slice(0, visibleLimit);
  const hidden = tokens.slice(visibleLimit);
  const foldKey = `inline-src:${hashFoldToken(tokens.join("||"))}`;
  const opened = Boolean(state.liveAsk.inlineSourceFoldState?.[foldKey]);
  const toggleText = opened ? "접기" : `+${hidden.length}개 더보기`;
  return `
    <div
      class="log-source-list is-collapsible"
      data-source-expanded="${opened ? "true" : "false"}"
      data-source-fold-key="${escapeHtml(foldKey)}"
    >
      <span class="log-source-inline">${visible.map((token) => renderToken(token)).join("")}</span>
      <span class="log-source-hidden"${opened ? "" : " hidden"}>${hidden.map((token) => renderToken(token)).join("")}</span>
      <button
        type="button"
        class="ghost mini log-source-toggle"
        data-source-toggle
        data-more-count="${hidden.length}"
        aria-expanded="${opened ? "true" : "false"}"
      >${toggleText}</button>
    </div>
  `;
}

function renderStructuredLog(rawText) {
  const entries = foldRunAgentTurns(buildStructuredLogEntries(rawText));
  if (!entries.length) {
    return `<div class="log-stream"><div class="log-entry role-generic"><div class="log-entry-body"><div class="log-line">No logs yet.</div></div></div></div>`;
  }
  return `<div class="log-stream">${entries
    .map((entry) => {
      if (entry.kind === "agent-turn") {
        return renderRunAgentTurn(entry);
      }
      const kindToken = String(entry.kind || "generic");
      const roleClass = `role-${escapeHtml(kindToken)}`;
      const showHeader = kindToken !== "text";
      const showKindCode = kindToken !== "tag" && kindToken !== "text";
      const header = showHeader
        ? `
        <div class="log-entry-head">
          <span class="log-entry-badge">${escapeHtml(entry.label || "Log")}</span>
          ${showKindCode ? `<code>${escapeHtml(kindToken)}</code>` : ""}
        </div>
      `
        : "";
      let body = "";
      if (entry.kind === "sources") {
        body = renderSourcesInlineChips(entry.lines.join(" | "), { limit: 6 });
      } else {
        body = entry.lines
          .map((line) => {
            if (!String(line || "").trim()) return '<div class="log-line is-empty"></div>';
            return `<div class="log-line">${renderRawLineWithLinks(line)}</div>`;
          })
          .join("");
      }
      const timeline = entry.kind === "workflow" ? renderWorkflowTimelineFromLines(entry.lines) : "";
      return `<article class="log-entry ${roleClass}">${header}<div class="log-entry-body">${timeline}${body}</div></article>`;
    })
    .join("")}</div>`;
}

function isStructuredLogLine(line) {
  const text = String(line || "").trim();
  if (!text) return false;
  if (/^\[[^\]]+\]/.test(text)) return true;
  if (/^#{1,6}\s/.test(text)) return true;
  if (/^[-*]\s+/.test(text)) return true;
  if (/^\d+\.\s+/.test(text)) return true;
  return false;
}

function reflowLogTextForDisplay(rawText) {
  return String(rawText || "").replace(/\r\n/g, "\n").replace(/\r/g, "\n");
}

function renderLogs(autoScroll = false) {
  const mdOut = $("#log-output-md");
  const shell = $(".log-shell");
  const raw = reflowLogTextForDisplay(state.logBuffer.join(""));
  if (!mdOut || !shell) {
    renderLiveAskThread();
    return;
  }
  const mdScrollTop = mdOut.scrollTop;
  const shouldStickMd = Boolean(state.logAutoFollow) && (autoScroll || isNearBottom(mdOut, 120));
  let mdSource = raw;
  let notice = "";
  if (raw.length > LOG_MD_MAX_CHARS) {
    mdSource = raw.slice(-LOG_MD_TAIL_CHARS);
    notice =
      `> Log preview is truncated for markdown rendering (${LOG_MD_TAIL_CHARS.toLocaleString()} chars tail).\n\n`;
  }
  const markdownSource = linkifyRawLogForMarkdown(mdSource);
  setRenderedMarkdown(mdOut, `${notice}${markdownSource}`);
  shell.classList.add("mode-markdown");
  const active = activeLogElement();
  if (active) {
    const shouldStick = shouldStickMd;
    if (shouldStick) {
      active.scrollTop = active.scrollHeight;
    } else if (active === mdOut) {
      mdOut.scrollTop = mdScrollTop;
    }
    state.logAutoFollow = isNearBottom(active, 140);
  }
  renderLiveAskThread();
}

function scheduleLogRender(autoScroll = false) {
  if (autoScroll && state.logAutoFollow) state.logAutoScrollRequested = true;
  if (state.logRenderPending) return;
  state.logRenderPending = true;
  window.requestAnimationFrame(() => {
    state.logRenderPending = false;
    const shouldScroll = state.logAutoScrollRequested;
    state.logAutoScrollRequested = false;
    renderLogs(shouldScroll);
  });
}

function setLogMode(mode) {
  state.logMode = "markdown";
  localStorage.setItem("federnett-log-mode", "markdown");
  scheduleLogRender(false);
}

function appendLog(text) {
  if (!text) return;
  const normalized = normalizeLogText(text, { ensureTrailingNewline: true });
  if (!normalized) return;
  state.logBuffer.push(normalized);
  if (state.logBuffer.length > LOG_LINE_LIMIT) {
    state.logBuffer.splice(0, state.logBuffer.length - LOG_LINE_LIMIT);
  }
  scheduleLogRender(true);
}

function clearLogs() {
  state.logBuffer = [];
  state.liveAsk.jobLogStartIndex = -1;
  state.liveAsk.lastJobLogStartIndex = -1;
  scheduleLogRender(false);
}

function shortId(id) {
  return id ? id.slice(0, 8) : "";
}

async function loadHistoryLog(relPath, runRel, kind = "") {
  try {
    const resolvedRunRel = normalizePathString(runRel || inferRunRelFromPath(relPath) || "");
    closeActiveSource();
    setKillEnabled(false);
    setJobStatus(`History log: ${relPath.split("/").pop() || relPath}`, false);
    if (resolvedRunRel) {
      if ($("#run-select")) $("#run-select").value = resolvedRunRel;
      if ($("#prompt-run-select")) $("#prompt-run-select").value = resolvedRunRel;
      if ($("#instruction-run-select")) $("#instruction-run-select").value = resolvedRunRel;
      refreshRunDependentFields();
      await updateRunStudio(resolvedRunRel).catch((err) => {
        appendLog(`[studio] failed to refresh run studio: ${err}\n`);
      });
      applyRunFolderSelection(resolvedRunRel);
    }
    const payload = await fetchJSON(`/api/files?path=${encodeURIComponent(relPath)}`);
    const content = payload.content || "";
    setLogBufferFromText(content);
    await hydrateWorkflowFromHistory({
      logPath: relPath,
      runRel: resolvedRunRel,
      kind,
      logText: content,
    });
    focusPanel("#logs-wrap .logs-block");
  } catch (err) {
    appendLog(`[logs] failed to load history: ${err}\n`);
  }
}

function upsertJob(jobPatch) {
  const now = Date.now();
  const idx = state.jobs.findIndex((j) => j.job_id === jobPatch.job_id);
  const base = idx >= 0 ? state.jobs[idx] : {};
  const next = {
    started_at: base.started_at || now,
    ...base,
    ...jobPatch,
  };
  if (idx >= 0) {
    state.jobs[idx] = next;
  } else {
    state.jobs.unshift(next);
  }
  state.jobs = state.jobs.slice(0, 12);
  renderJobs();
}

function renderJobs() {
  const host = $("#jobs-modal-list");
  if (!host) return;
  const runRel = selectedRunRel();
  const limit = 6;
  const collapsed = !state.jobsExpanded;
  const allJobs = buildRecentJobs(runRel);
  const jobs = collapsed ? allJobs.slice(0, limit) : allJobs;
  host.classList.toggle("is-collapsed", collapsed);
  host.classList.toggle("is-expanded", !collapsed);
  if (!jobs.length) {
    host.innerHTML = `<div class="muted">No recent jobs yet.</div>`;
  } else {
    host.innerHTML = jobs
      .map((job) => {
        const status = job.status || "unknown";
        const code =
          typeof job.returncode === "number" ? `rc=${job.returncode}` : "";
        const title = job.label || job.kind || "job";
        const when = job.updated_at ? formatDate(job.updated_at) : "";
        const extraPill = when ? `<span class="job-pill">${escapeHtml(when)}</span>` : "";
        return `
          <div class="job-item">
            <div>
              <strong>${escapeHtml(title)}</strong>
              <div class="job-meta">
                <span class="job-pill">${status}</span>
                ${code ? `<span class="job-pill">${code}</span>` : ""}
                ${extraPill}
              </div>
            </div>
            <button class="ghost" data-job-open="${job.job_id}" data-job-source="${job.source}" data-job-path="${escapeHtml(
              job.log_path || "",
            )}" data-job-run="${escapeHtml(job.run_rel || "")}" data-job-kind="${escapeHtml(
              job.kind || "",
            )}">Open</button>
          </div>
        `;
      })
      .join("");
  }
  const toggle = $("#jobs-toggle");
  if (toggle) {
    toggle.style.display = allJobs.length > limit ? "inline-flex" : "none";
    toggle.textContent = state.jobsExpanded ? "Show less" : "Show more";
    toggle.onclick = () => {
      state.jobsExpanded = !state.jobsExpanded;
      renderJobs();
    };
  }
  host.querySelectorAll("[data-job-open]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const jobId = btn.getAttribute("data-job-open");
      if (!jobId) return;
      const source = btn.getAttribute("data-job-source");
      if (source === "history") {
        const path = btn.getAttribute("data-job-path");
        const runRel = btn.getAttribute("data-job-run");
        const kind = btn.getAttribute("data-job-kind") || "";
        if (path) {
          loadHistoryLog(path, runRel || "", kind);
        }
        return;
      }
      const kind = btn.getAttribute("data-job-kind") || "job";
      attachToJob(jobId, { kind });
    });
  });
  updateRecentJobsSummary();
}

function renderRunHistory() {
  const host = $("#jobs-history-list");
  if (!host) return;
  const runs = [...(state.runs || [])]
    .filter((run) => run.run_rel)
    .sort((a, b) => {
      const da = Date.parse(a.updated_at || "") || 0;
      const db = Date.parse(b.updated_at || "") || 0;
      return db - da;
    })
    .slice(0, 5);
  if (!runs.length) {
    host.innerHTML = `<div class="muted">No past runs.</div>`;
    return;
  }
  host.innerHTML = runs
    .map((run) => {
      const rel = run.run_rel || "";
      const name = run.run_name || rel || "run";
      const updated = run.updated_at ? formatDate(run.updated_at) : "";
      return `
        <div class="job-item secondary">
          <div>
            <strong>${escapeHtml(name)}</strong>
            <div class="job-meta">
              <span class="job-pill">${escapeHtml(rel)}</span>
              ${updated ? `<span class="job-pill">${escapeHtml(updated)}</span>` : ""}
            </div>
          </div>
          <button class="ghost" data-run-open="${escapeHtml(rel)}">Open</button>
        </div>
      `;
    })
    .join("");
  host.querySelectorAll("[data-run-open]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const runRel = btn.getAttribute("data-run-open");
      if (!runRel) return;
      if ($("#run-select")) $("#run-select").value = runRel;
      if ($("#prompt-run-select")) $("#prompt-run-select").value = runRel;
      if ($("#instruction-run-select")) $("#instruction-run-select").value = runRel;
      refreshRunDependentFields();
      updateRunStudio(runRel).catch(() => {});
    });
  });
}

function setJobStatus(text, running = false) {
  const el = $("#job-status");
  if (!el) return;
  const statusText = String(text || "").trim();
  const runningHint = running ? " · 로그: 타임라인 + 로그 브릿지" : "";
  el.textContent = `${statusText}${runningHint}`;
  el.title = running
    ? "실시간 실행 로그는 Live Logs 타임라인 카드와 답변 카드의 로그 브릿지에서 확인할 수 있습니다."
    : "";
  el.classList.toggle("is-running", !!running);
}

function recoverIdleJobControls() {
  const hasActiveJob =
    Boolean(state.activeJobId)
    || Boolean(state.activeSource)
    || Boolean(state.activeJobPending);
  if (hasActiveJob) return;
  state.activeJobKind = null;
  const quickFederlicht = $("#quick-run-federlicht");
  if (quickFederlicht && (quickFederlicht.disabled || /running/i.test(quickFederlicht.textContent || ""))) {
    setFederlichtRunEnabled(true);
  }
  const quickFeather = $("#quick-run-feather");
  if (quickFeather && (quickFeather.disabled || /running/i.test(quickFeather.textContent || ""))) {
    setFeatherRunEnabled(true);
  }
  setKillEnabled(false);
  const statusText = String($("#job-status")?.textContent || "").trim();
  if (/실행 중|running/i.test(statusText)) {
    setJobStatus("No active job.", false);
  }
}

function setLogsCollapsed(_collapsed) {
  // Hide Logs UI removed: keep logs expanded.
  state.logsCollapsed = false;
  document.body.dataset.logsCollapsed = "false";
  localStorage.removeItem("federnett-logs-collapsed");
}

function normalizeLanguage(value) {
  if (!value) return "";
  const lowered = String(value).trim().toLowerCase();
  if (lowered.startsWith("ko") || lowered.includes("korean")) return "ko";
  if (lowered.startsWith("en") || lowered.includes("english")) return "en";
  if (lowered.startsWith("de") || lowered.includes("german")) return "de";
  return lowered;
}

function applyFreeFormatMode() {
  const enabled = !!$("#federlicht-free-format")?.checked;
  const templateSelect = $("#template-select");
  if (templateSelect) {
    templateSelect.disabled = enabled;
    templateSelect.classList.toggle("is-disabled", enabled);
    templateSelect.setAttribute("aria-disabled", enabled ? "true" : "false");
  }
  const rigiditySelect = $("#federlicht-template-rigidity");
  if (rigiditySelect) {
    rigiditySelect.disabled = enabled;
    rigiditySelect.classList.toggle("is-disabled", enabled);
    rigiditySelect.setAttribute("aria-disabled", enabled ? "true" : "false");
  }
  const stylePackSelect = $("#federlicht-style-pack");
  if (stylePackSelect) {
    stylePackSelect.disabled = !enabled;
    stylePackSelect.classList.toggle("is-disabled", !enabled);
    stylePackSelect.setAttribute("aria-disabled", !enabled ? "true" : "false");
  }
}

function applyRunSettings(summary) {
  const meta = summary?.report_meta || {};
  const freeFormatToggle = $("#federlicht-free-format");
  if (
    freeFormatToggle
    && Object.prototype.hasOwnProperty.call(meta, "free_format")
  ) {
    freeFormatToggle.checked = !!meta.free_format;
  }
  const template = meta.template;
  if (template) {
    const templateSelect = $("#template-select");
    if (templateSelect && Array.from(templateSelect.options).some((o) => o.value === template)) {
      templateSelect.value = template;
    }
    const promptTemplateSelect = $("#prompt-template-select");
    if (
      promptTemplateSelect &&
      Array.from(promptTemplateSelect.options).some((o) => o.value === template)
    ) {
      promptTemplateSelect.value = template;
    }
  }
  if (meta.style_pack) {
    const stylePackSelect = $("#federlicht-style-pack");
    if (
      stylePackSelect
      && Array.from(stylePackSelect.options).some((o) => o.value === meta.style_pack)
    ) {
      stylePackSelect.value = meta.style_pack;
    }
  }
  const lang = normalizeLanguage(meta.language);
  if (lang) {
    const langSelect = $("#federlicht-lang");
    if (langSelect && Array.from(langSelect.options).some((o) => o.value === lang)) {
      langSelect.value = lang;
    }
  }
  if (meta.model) {
    const modelInput = $("#federlicht-model");
    if (modelInput) modelInput.value = meta.model;
  }
  if (meta.quality_model) {
    const checkModelInput = $("#federlicht-check-model");
    if (checkModelInput) checkModelInput.value = meta.quality_model;
  }
  if (meta.model_vision) {
    const visionInput = $("#federlicht-model-vision");
    if (visionInput) visionInput.value = meta.model_vision;
  }
  if (meta.template_rigidity) {
    const rigiditySelect = $("#federlicht-template-rigidity");
    if (
      rigiditySelect
      && Array.from(rigiditySelect.options).some((o) => o.value === meta.template_rigidity)
    ) {
      rigiditySelect.value = meta.template_rigidity;
    }
  }
  if (meta.temperature_level) {
    const levelSelect = $("#federlicht-temperature-level");
    if (levelSelect && Array.from(levelSelect.options).some((o) => o.value === meta.temperature_level)) {
      levelSelect.value = meta.temperature_level;
    }
  }
  if (meta.quality_iterations !== undefined && meta.quality_iterations !== null) {
    setQualityIterations(meta.quality_iterations);
  }
  if (meta.agent_profile) {
    const profileId =
      typeof meta.agent_profile === "string" ? meta.agent_profile : meta.agent_profile.id;
    if (profileId) {
      const match = (state.agentProfiles.list || []).find((item) => item.id === profileId);
      if (match) {
        openAgentProfile(match.id, match.source || "builtin").catch((err) => {
          appendLog(`[agents] failed to switch profile from run meta: ${err}\n`);
        });
      }
    }
  }
  syncFederlichtModelControls({ announce: false });
  renderActiveProfileSummary();
  applyFreeFormatMode();
  syncWorkflowQualityControls();
  renderWorkflowStudioPanel();
}

function setKillEnabled(enabled) {
  const kill = $("#job-kill");
  if (kill) kill.disabled = !enabled;
}

function setPrimaryRunButtonState(selectors, enabled, idleLabel, runningLabel) {
  const targets = Array.isArray(selectors) ? selectors : [selectors];
  targets.forEach((selector) => {
    const button = $(selector);
    if (!button) return;
    button.disabled = !enabled;
    button.classList.toggle("is-running", !enabled);
    button.textContent = enabled ? idleLabel : runningLabel;
  });
}

function setFederlichtRunEnabled(enabled) {
  setPrimaryRunButtonState(
    ["#federlicht-run", "#quick-run-federlicht"],
    enabled,
    "Run Federlicht",
    "Running...",
  );
}

function setFeatherRunEnabled(enabled) {
  setPrimaryRunButtonState(
    ["#feather-run", "#quick-run-feather"],
    enabled,
    "Run Feather",
    "Running...",
  );
}

function setPromptGenerateEnabled(enabled) {
  const button = $("#federlicht-prompt-generate");
  if (!button) return;
  button.disabled = !enabled;
  button.classList.toggle("is-running", !enabled);
  button.textContent = enabled ? "Generate Prompt" : "Generating Prompt...";
}

function describeJobKind(kind) {
  switch (kind) {
    case "federlicht":
      return "Federlicht 리포트";
    case "feather":
      return "Feather 수집";
    case "prompt":
    case "generate_prompt":
      return "프롬프트 생성";
    case "template":
      return "템플릿 생성";
    default:
      return "작업";
  }
}

function isSystemExecutionKind(kind) {
  const token = String(kind || "").trim().toLowerCase();
  return token === "feather" || token === "federlicht" || token === "prompt" || token === "generate_prompt";
}

function closeActiveSource() {
  if (state.activeSource) {
    state.activeSource.close();
    state.activeSource = null;
  }
}

function attachToJob(jobId, opts = {}) {
  closeActiveSource();
  state.activeJobPending = false;
  state.activeJobId = jobId;
  state.activeJobKind = opts.kind || "job";
  if (!Number.isFinite(Number(state.liveAsk.jobLogStartIndex)) || state.liveAsk.jobLogStartIndex < 0) {
    state.liveAsk.jobLogStartIndex = state.logBuffer.length;
  }
  if (state.activeJobKind === "federlicht") {
    setFederlichtRunEnabled(false);
  } else if (state.activeJobKind === "feather") {
    setFeatherRunEnabled(false);
  }
  setKillEnabled(true);
  const label = opts.jobLabel || describeJobKind(state.activeJobKind);
  setJobStatus(`${label} 실행 중 (${shortId(jobId)})`, true);
  state.liveAsk.autoFollowThread = true;
  scrollLiveAskThreadToLatest();
  const source = new EventSource(`/api/jobs/${jobId}/events`);
  state.activeSource = source;
  source.addEventListener("log", (ev) => {
    try {
      const payload = JSON.parse(ev.data);
      const text = payload.text || "";
      appendLog(text);
      updateWorkflowFromLog(text);
      if (state.activeJobKind === "template") {
        appendTemplateGenLog(text);
      }
    } catch (err) {
      appendLog(`[log] failed to parse event: ${err}\n`);
    }
  });
  source.addEventListener("done", (ev) => {
    const finishedKind = state.activeJobKind;
    let completionReported = false;
    try {
      const payload = JSON.parse(ev.data);
      const status = payload.status || "done";
      const code =
        typeof payload.returncode === "number" ? ` (rc=${payload.returncode})` : "";
      const doneProcessLog = extractLiveAskProcessLog(state.liveAsk.jobLogStartIndex);
      appendLog(`[done] ${status}${code}\n`);
      upsertJob({
        job_id: jobId,
        status,
        returncode: payload.returncode,
        kind: opts.kind || "job",
      });
      if (opts.onDone) opts.onDone(payload);
      if (payload.returncode === 0 && opts.onSuccess) opts.onSuccess(payload);
      completeWorkflow(finishedKind, payload.returncode, status);
      setJobStatus(`Job ${shortId(jobId)} ${status}${code}`, false);
      if (isSystemExecutionKind(finishedKind)) {
        const label = describeJobKind(finishedKind);
        const statusLabel = payload.returncode === 0 ? "완료" : `실패${code}`;
        const processSummary = summarizeLiveAskProcess(doneProcessLog);
        const summaryLine = processSummary.total > 0
          ? `요약: cmd ${processSummary.commands} · workflow ${processSummary.workflow} · error ${processSummary.errors}`
          : "요약: 실행 로그 없음";
        const nextLine = payload.returncode === 0
          ? (
            finishedKind === "feather"
              ? "다음 단계: Federlicht 실행 또는 instruction 보강 후 재수집"
              : finishedKind === "prompt" || finishedKind === "generate_prompt"
                ? "다음 단계: 생성된 prompt 확인 후 Federlicht 실행"
                : "다음 단계: run_overview/claim_map/gap_finder 확인"
          )
          : "다음 단계: 모델/권한/입력 경로와 로그 오류를 확인 후 재실행";
        appendLiveAskSystemEntry(
          `[시스템] ${label} ${statusLabel}.\n상태: ${status || "done"}${code || ""}\n${summaryLine}\n${nextLine}`,
          { processLog: doneProcessLog },
        );
        completionReported = true;
      }
    } catch (err) {
      appendLog(`[done] failed to parse event: ${err}\n`);
    } finally {
      state.activeJobPending = false;
      if (!completionReported && isSystemExecutionKind(finishedKind)) {
        const label = describeJobKind(finishedKind);
        appendLiveAskSystemEntry(`[시스템] ${label} 실행이 종료되었습니다. (상세 상태 파싱 실패)`);
      }
      setKillEnabled(false);
      if (finishedKind === "federlicht") {
        setFederlichtRunEnabled(true);
      } else if (finishedKind === "feather") {
        setFeatherRunEnabled(true);
      }
      if (opts.runRel) {
        loadRunLogs(opts.runRel).catch(() => {});
      }
      if (state.activeJobId === jobId) {
        state.activeJobId = null;
        state.activeJobKind = null;
      }
      if (Number.isFinite(Number(state.liveAsk.jobLogStartIndex)) && state.liveAsk.jobLogStartIndex >= 0) {
        state.liveAsk.lastJobLogStartIndex = state.liveAsk.jobLogStartIndex;
      }
      state.liveAsk.jobLogStartIndex = -1;
      closeActiveSource();
      recoverIdleJobControls();
    }
  });
  source.onerror = () => {
    if (state.activeJobId !== jobId) {
      state.activeJobPending = false;
      recoverIdleJobControls();
      return;
    }
    const failedKind = state.activeJobKind;
    const streamProcessLog = extractLiveAskProcessLog(state.liveAsk.jobLogStartIndex);
    appendLog("[error] event stream closed unexpectedly\n");
    setJobStatus("Stream closed unexpectedly.", false);
    setKillEnabled(false);
    if (failedKind === "federlicht") {
      setFederlichtRunEnabled(true);
    } else if (failedKind === "feather") {
      setFeatherRunEnabled(true);
    }
    if (failedKind) {
      completeWorkflow(failedKind, -1, "stream_error");
      if (isSystemExecutionKind(failedKind)) {
        const label = describeJobKind(failedKind);
        appendLiveAskSystemEntry(
          `[시스템] ${label} 실행 중 이벤트 스트림이 비정상 종료되었습니다.`,
          { processLog: streamProcessLog },
        );
      }
    }
    if (Number.isFinite(Number(state.liveAsk.jobLogStartIndex)) && state.liveAsk.jobLogStartIndex >= 0) {
      state.liveAsk.lastJobLogStartIndex = state.liveAsk.jobLogStartIndex;
    }
    state.liveAsk.jobLogStartIndex = -1;
    state.activeJobPending = false;
    state.activeJobId = null;
    state.activeJobKind = null;
    closeActiveSource();
    recoverIdleJobControls();
  };
}

async function startJob(endpoint, payload, meta = {}) {
  const kind = meta.kind || "job";
  state.activeJobPending = true;
  if (kind === "federlicht" || kind === "feather") {
    state.activeJobKind = kind;
  }
  state.liveAsk.jobLogStartIndex = state.logBuffer.length;
  if (kind === "federlicht") {
    setFederlichtRunEnabled(false);
  } else if (kind === "feather") {
    setFeatherRunEnabled(false);
  }
  const body = JSON.stringify(payload || {});
  appendLog(`\n[start] POST ${endpoint}\n`);
  if (isSystemExecutionKind(kind)) {
    const runHint = normalizePathString(
      payload?.run
      || payload?.output
      || meta?.runRel
      || "",
    );
    const label = describeJobKind(kind);
    appendLiveAskSystemEntry(
      `[시스템] ${label} 실행 요청을 접수했습니다.${runHint ? `\nrun: ${runHint}` : ""}`,
    );
  }
  if (kind === "federlicht") {
    const backend = String(payload?.llm_backend || "openai_api");
    const model = String(payload?.model || "-");
    const checkModel = String(payload?.check_model || payload?.model || "-");
    const reasoning = String(payload?.reasoning_effort || "off");
    const progressCharsRaw = Number.parseInt(String(payload?.progress_chars || "0"), 10);
    const progressChars = Number.isFinite(progressCharsRaw) && progressCharsRaw > 0
      ? String(progressCharsRaw)
      : "off";
    const runPath = String(payload?.run || "-");
    const outputPath = String(payload?.output || "-");
    appendLog(
      `[federlicht:start] backend=${backend} model=${model} check=${checkModel} reasoning=${reasoning} progress=${progressChars} run=${runPath} output=${outputPath}\n`,
    );
  }
  let res;
  try {
    res = await fetchJSON(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body,
    });
  } catch (err) {
    const errorPayload = err?.payload && typeof err.payload === "object" ? err.payload : null;
    const errorMessageRaw = String(
      errorPayload?.error
      || errorPayload?.message
      || err?.body
      || err?.message
      || err
      || "",
    ).trim();
    const compactError = errorMessageRaw.length > 180
      ? `${errorMessageRaw.slice(0, 179)}…`
      : errorMessageRaw;
    const conflictStatus = Number(err?.status || 0) === 409;
    const conflictPayload = err?.payload && typeof err.payload === "object" ? err.payload : null;
    const runningJobId = String(conflictPayload?.running_job_id || "").trim();
    const runningKind = String(conflictPayload?.running_kind || kind || "job").trim() || "job";
    if (conflictStatus && runningJobId) {
      state.activeJobPending = false;
      const inferredRunRel = inferRunRelFromPayload(payload);
      const resolvedRunRel = normalizePathString(meta.runRel || inferredRunRel || "");
      appendLog(
        `[${kind}:start-info] another job is already running (${runningKind}:${runningJobId}) → 기존 실행 로그에 자동 연결합니다.\n`,
      );
      if (isSystemExecutionKind(kind)) {
        const label = describeJobKind(kind);
        appendLiveAskSystemEntry(
          `[시스템] ${label}은 이미 실행 중인 작업에 연결되었습니다. (${shortId(runningJobId)})`,
        );
      }
      upsertJob({
        job_id: runningJobId,
        status: "running",
        kind: runningKind,
        run_rel: resolvedRunRel,
      });
      const runningLabel = meta.jobLabel || describeJobKind(runningKind);
      setJobStatus(`${runningLabel} 실행 중 (${shortId(runningJobId)})`, true);
      beginWorkflow(runningKind, {
        ...(payload || {}),
        _spot_label: meta.spotLabel || "",
        _spot_path: meta.spotPath || "",
      });
      if (state.logsCollapsed) setLogsCollapsed(false);
      focusPanel("#logs-wrap .logs-block");
      attachToJob(runningJobId, {
        ...meta,
        kind: runningKind,
        jobLabel: runningLabel,
        runRel: resolvedRunRel,
      });
      return runningJobId;
    }
    appendLog(`[${kind}:start-error] ${err}\n`);
    if (compactError && compactError !== String(err)) {
      appendLog(`[${kind}:start-error:detail] ${compactError}\n`);
    }
    if (/reasoning(?:[._\s-]?effort)?/i.test(errorMessageRaw)) {
      appendLog("[federlicht:model] 요청 파라미터의 reasoning_effort 호환성을 확인하세요. (지원되지 않으면 off)\n");
    }
    if (
      /(model|deployment|engine).*(not[\s_-]?found|unknown|unauthorized|forbidden|does not exist|do not have access|access denied|permission)/i.test(
        errorMessageRaw,
      )
    ) {
      appendLog("[federlicht:model] 모델 접근 권한/배포명을 확인하세요. 필요 시 OpenAI fallback 모델로 전환하세요.\n");
    }
    if (kind === "federlicht") {
      setFederlichtRunEnabled(true);
      state.workflow.hasError = true;
      state.workflow.running = false;
      state.workflow.statusText = compactError
        ? `Start failed · ${compactError}`
        : "Start failed";
      state.workflow.mainStatusText = state.workflow.statusText;
      renderWorkflow();
      setJobStatus(state.workflow.statusText, false);
    } else if (kind === "feather") {
      setFeatherRunEnabled(true);
      state.workflow.hasError = true;
      state.workflow.running = false;
      state.workflow.statusText = compactError
        ? `Start failed · ${compactError}`
        : "Start failed";
      state.workflow.mainStatusText = state.workflow.statusText;
      renderWorkflow();
      setJobStatus(state.workflow.statusText, false);
    } else {
      beginWorkflowSpot(kind, {
        ...(payload || {}),
        _spot_label: meta.spotLabel || "",
        _spot_path: meta.spotPath || "",
      });
      completeWorkflowSpot(kind, -1, "start_failed");
    }
    if (isSystemExecutionKind(kind)) {
      const label = describeJobKind(kind);
      appendLiveAskSystemEntry(`[시스템] ${label} 시작 실패: ${compactError || String(err)}`);
    }
    if (Number.isFinite(Number(state.liveAsk.jobLogStartIndex)) && state.liveAsk.jobLogStartIndex >= 0) {
      state.liveAsk.lastJobLogStartIndex = state.liveAsk.jobLogStartIndex;
    }
    state.activeJobPending = false;
    if (!state.activeJobId) {
      state.activeJobKind = null;
    }
    state.liveAsk.jobLogStartIndex = -1;
    throw err;
  }
  if (Array.isArray(res?.warnings) && res.warnings.length) {
    res.warnings.forEach((line) => {
      const text = String(line || "").trim();
      if (!text) return;
      appendLog(`[${kind}:config] ${text}\n`);
    });
  }
  if (kind === "federlicht" && res && typeof res.runtime === "object") {
    const runtime = res.runtime || {};
    const backend = String(runtime.llm_backend || payload?.llm_backend || "openai_api");
    const model = String(runtime.model || payload?.model || "-");
    const checkModel = String(runtime.check_model || runtime.model || payload?.check_model || payload?.model || "-");
    const reasoning = String(runtime.reasoning_effort || payload?.reasoning_effort || "off");
    const progressCharsRaw = Number.parseInt(String(runtime.progress_chars || payload?.progress_chars || "0"), 10);
    const progressChars = Number.isFinite(progressCharsRaw) && progressCharsRaw > 0
      ? String(progressCharsRaw)
      : "off";
    appendLog(
      `[federlicht:resolved] backend=${backend} model=${model} check=${checkModel} reasoning=${reasoning} progress=${progressChars}\n`,
    );
  }
  const jobId = res.job_id;
  if (!jobId) {
    const err = new Error("start response missing job_id");
    appendLog(`[${kind}:start-error] ${err}\n`);
    state.activeJobPending = false;
    if (!state.activeJobId) {
      state.activeJobKind = null;
    }
    if (kind === "federlicht") {
      setFederlichtRunEnabled(true);
    } else if (kind === "feather") {
      setFeatherRunEnabled(true);
    }
    throw err;
  }
  if (kind === "federlicht") {
    appendLog("[federlicht:run] job accepted and streaming started\n");
  }
  if (isSystemExecutionKind(kind)) {
    const label = describeJobKind(kind);
    appendLiveAskSystemEntry(`[시스템] ${label} 실행이 시작되었습니다. (job=${shortId(jobId)})`);
  }
  const inferredRunRel = inferRunRelFromPayload(payload);
  upsertJob({
    job_id: jobId,
    status: "running",
    kind,
    run_rel: meta.runRel || inferredRunRel || "",
  });
  const jobLabel = meta.jobLabel || describeJobKind(kind);
  if (state.logsCollapsed) setLogsCollapsed(false);
  setJobStatus(`${jobLabel} 실행 중 (${shortId(jobId)})`, true);
  beginWorkflow(kind, {
    ...(payload || {}),
    _spot_label: meta.spotLabel || "",
    _spot_path: meta.spotPath || "",
  });
  state.liveAsk.autoFollowThread = true;
  scrollLiveAskThreadToLatest();
  focusPanel("#logs-wrap .logs-block");
  state.activeJobPending = false;
  attachToJob(jobId, {
    ...meta,
    jobLabel,
    runRel: meta.runRel || inferredRunRel || "",
  });
  window.setTimeout(() => {
    recoverIdleJobControls();
  }, 3200);
  return jobId;
}

function pruneEmpty(obj) {
  const out = {};
  Object.entries(obj || {}).forEach(([k, v]) => {
    if (v === null || v === undefined) return;
    if (typeof v === "string" && v.trim() === "") return;
    out[k] = v;
  });
  return out;
}

function buildFeatherPayload(options = {}) {
  const fallbackQuery = String(options?.fallbackQuery || "").trim();
  const selectedRun = normalizePathString(selectedRunRel() || "");
  const inputValueRaw = $("#feather-input")?.value?.trim();
  const inputValue = inputValueRaw ? expandSiteRunsPath(inputValueRaw, { runRel: selectedRun }) : inputValueRaw;
  const queryValue = String($("#feather-query")?.value || "").trim();
  const resolvedQuery = queryValue || fallbackQuery;
  const outputRaw = String($("#feather-output")?.value || "").trim();
  const outputFallback = outputRaw || ensureAskRunRel() || selectedRunRel() || "";
  const globalPolicy = normalizeGlobalModelPolicy(state.modelPolicy, state.modelPolicy.backend);
  const backend = normalizeAskLlmBackend(globalPolicy.backend || "openai_api");
  const payload = {
    input: inputValue,
    query: inputValue ? undefined : resolvedQuery,
    output: expandSiteRunsPath(outputFallback, { runRel: selectedRun }),
    lang: $("#feather-lang")?.value,
    days: Number.parseInt($("#feather-days")?.value || "", 10),
    max_results: Number.parseInt($("#feather-max-results")?.value || "", 10),
    agentic_search: $("#feather-agentic-search")?.checked,
    max_iter: Number.parseInt($("#feather-max-iter")?.value || "", 10),
    download_pdf: $("#feather-download-pdf")?.checked,
    openalex: $("#feather-openalex")?.checked,
    youtube: $("#feather-youtube")?.checked,
    yt_transcript: $("#feather-yt-transcript")?.checked,
    update_run: $("#feather-update-run")?.checked,
    yt_order: $("#feather-yt-order")?.value,
    llm_backend: backend,
    model: globalPolicy.model || "",
    extra_args: $("#feather-extra-args")?.value,
  };
  if (!payload.input && !payload.query) {
    throw new Error("Provide either an instruction path or a query.");
  }
  if (!payload.output) {
    throw new Error("Output folder is required.");
  }
  if (!Number.isFinite(payload.days)) delete payload.days;
  if (!Number.isFinite(payload.max_results)) delete payload.max_results;
  if (!Number.isFinite(payload.max_iter)) delete payload.max_iter;
  if (payload.agentic_search) {
    const backendToken = normalizeAskLlmBackend(payload.llm_backend || "openai_api");
    const modelToken = normalizeModelToken(payload.model);
    if (
      !modelToken
      || (backendToken === "codex_cli" && (isOpenaiModelToken(modelToken) || isCommonOpenaiDefaultModel(modelToken)))
      || (backendToken === "openai_api" && (isCodexModelToken(modelToken) || isCodexModelPlaceholderToken(modelToken)))
    ) {
      payload.model = backendToken === "codex_cli" ? codexModelHint() : openaiModelHint();
    }
    if (backendToken === "codex_cli") {
      payload.model = normalizeCodexModelToken(payload.model || codexModelHint());
    }
  }
  if (!payload.agentic_search) {
    delete payload.model;
    delete payload.max_iter;
  }
  return pruneEmpty(payload);
}

function buildFederlichtPayload() {
  const figuresEnabled = $("#federlicht-figures")?.checked;
  const noTags = $("#federlicht-no-tags")?.checked;
  const freeFormat = $("#federlicht-free-format")?.checked;
  const stylePack = ($("#federlicht-style-pack")?.value || "none").trim().toLowerCase();
  const normalizedModelConfig = syncFederlichtModelControls({ announce: false });
  const backend = normalizedModelConfig.backend;
  const selectedStages = selectedStagesInOrder();
  const skippedStages = STAGE_DEFS
    .map((stage) => stage.id)
    .filter((stageId) => !state.pipeline.selected.has(stageId));
  const activeProfile = resolveActiveAgentProfileItem();
  const agentProfile = activeProfile?.id || "";
  const agentSource = activeProfile?.source || "builtin";
  const agentProfileDir =
    agentSource === "site" ? joinPath(state.info?.site_root || "site", "agent_profiles") : "";
  const runRel = normalizePathString($("#run-select")?.value || "");
  const rawPromptFile = String($("#federlicht-prompt-file")?.value || "").trim();
  const promptFileValue = rawPromptFile
    ? expandSiteRunsPath(rawPromptFile, { runRel })
    : "";
  const promptValue = $("#federlicht-prompt")?.value;
  const includeInlinePrompt = isPromptDirty() || !promptFileValue;
  const payload = {
    run: runRel,
    output: ensureOutputPathForRun($("#federlicht-output")?.value, runRel),
    template: freeFormat ? undefined : $("#template-select")?.value,
    free_format: freeFormat ? true : undefined,
    style_pack: freeFormat && stylePack && stylePack !== "none" ? stylePack : undefined,
    lang: $("#federlicht-lang")?.value,
    depth: $("#federlicht-depth")?.value,
    prompt: includeInlinePrompt ? promptValue : undefined,
    prompt_file: promptFileValue,
    model: normalizedModelConfig.model,
    reasoning_effort:
      normalizedModelConfig.reasoningEffort
      && normalizedModelConfig.reasoningEffort !== "off"
        ? normalizedModelConfig.reasoningEffort
        : undefined,
    check_model: normalizedModelConfig.checkModel,
    model_vision: normalizedModelConfig.visionModel,
    template_rigidity: freeFormat ? undefined : $("#federlicht-template-rigidity")?.value,
    temperature_level: $("#federlicht-temperature-level")?.value,
    stages: selectedStages.join(","),
    skip_stages: skippedStages.join(","),
    quality_iterations: Number.parseInt(
      $("#federlicht-quality-iterations")?.value || "",
      10,
    ),
    quality_strategy: $("#federlicht-quality-strategy")?.value,
    progress_chars: 240,
    tags: noTags ? undefined : $("#federlicht-tags")?.value,
    no_tags: noTags ? true : undefined,
    figures: figuresEnabled ? true : undefined,
    no_figures: figuresEnabled ? undefined : true,
    figures_mode: $("#federlicht-figures-mode")?.value,
    figures_select: $("#federlicht-figures-select")?.value,
    web_search: $("#federlicht-web-search")?.checked,
    site_output: $("#federlicht-site-output")?.value,
    agent_profile: agentProfile,
    agent_profile_dir: agentProfileDir,
    agent_config: $("#federlicht-agent-config")?.value,
    llm_backend: backend,
    extra_args: $("#federlicht-extra-args")?.value,
  };
  if (!payload.run) {
    throw new Error("Run folder is required.");
  }
  if (!payload.output) {
    throw new Error("Output report path is required.");
  }
  if (!Number.isFinite(payload.quality_iterations)) delete payload.quality_iterations;
  return pruneEmpty(payload);
}

function buildPromptPayload() {
  const run = $("#prompt-run-select")?.value;
  const normalizedModelConfig = syncFederlichtModelControls({ announce: false });
  const backend = normalizedModelConfig.backend;
  let output = $("#prompt-output")?.value;
  if (!output && run) {
    output = defaultPromptPath(run);
    const field = $("#prompt-output");
    if (field) field.value = output;
  }
  const payload = {
    run,
    output: run
      ? normalizePromptPath(output || defaultPromptPath(run), { runRel: run })
      : expandSiteRunsPath(output),
    template: $("#prompt-template-select")?.value,
    depth: $("#prompt-depth")?.value,
    model: normalizeModelToken($("#prompt-model")?.value) || normalizedModelConfig.model,
    reasoning_effort:
      normalizedModelConfig.reasoningEffort
      && normalizedModelConfig.reasoningEffort !== "off"
        ? normalizedModelConfig.reasoningEffort
        : undefined,
    llm_backend: backend,
    extra_args: $("#prompt-extra-args")?.value,
  };
  if (!payload.run) throw new Error("Run folder is required.");
  return pruneEmpty(payload);
}

function buildPromptPayloadFromFederlicht() {
  const run = $("#run-select")?.value;
  if (!run) throw new Error("Run folder is required.");
  const freeFormat = $("#federlicht-free-format")?.checked;
  const stylePack = ($("#federlicht-style-pack")?.value || "none").trim().toLowerCase();
  const normalizedModelConfig = syncFederlichtModelControls({ announce: false });
  const backend = normalizedModelConfig.backend;
  let output = $("#federlicht-prompt-file")?.value;
  if (!output) {
    output = defaultPromptPath(run);
    const field = $("#federlicht-prompt-file");
    if (field) field.value = output;
  }
  const payload = {
    run,
    output: normalizePromptPath(output || defaultPromptPath(run), { runRel: run }),
    template: freeFormat ? undefined : $("#template-select")?.value,
    free_format: freeFormat ? true : undefined,
    style_pack: freeFormat && stylePack && stylePack !== "none" ? stylePack : undefined,
    depth: $("#federlicht-depth")?.value,
    model: normalizedModelConfig.model,
    reasoning_effort:
      normalizedModelConfig.reasoningEffort
      && normalizedModelConfig.reasoningEffort !== "off"
        ? normalizedModelConfig.reasoningEffort
        : undefined,
    llm_backend: backend,
    template_rigidity: freeFormat ? undefined : $("#federlicht-template-rigidity")?.value,
    temperature_level: $("#federlicht-temperature-level")?.value,
  };
  return pruneEmpty(payload);
}

function handleTabs() {
  const tabs = Array.from(document.querySelectorAll(".tab"));
  const tabGuide = $("#tab-guide");
  const panels = {
    feather: $("#tab-feather"),
    federlicht: $("#tab-federlicht"),
    runstudio: $("#run-studio-wrap"),
  };
  const setActiveTab = (key) => {
    const resolved = key === "federlicht" || key === "runstudio" ? key : "feather";
    document.body.dataset.tab = resolved;
    tabs.forEach((tab) => {
      const active = String(tab.dataset.tab || "").trim() === resolved;
      tab.classList.toggle("active", active);
      tab.setAttribute("aria-selected", active ? "true" : "false");
    });
    if (tabGuide) {
      if (resolved === "federlicht") {
        tabGuide.innerHTML =
          "<strong>2단계 Federlicht</strong><span>수집 자료 기반 보고서 생성과 품질 점검</span>";
      } else if (resolved === "runstudio") {
        tabGuide.innerHTML =
          "<strong>Run Studio</strong><span>run 폴더/산출물/근거 파일 구조를 한 화면에서 관리</span>";
      } else {
        tabGuide.innerHTML =
          "<strong>1단계 Feather</strong><span>외부 자료 수집과 증거 아카이빙</span>";
      }
    }
    if (panels.feather) panels.feather.classList.toggle("active", resolved === "feather");
    if (panels.federlicht) panels.federlicht.classList.toggle("active", resolved === "federlicht");
    if (panels.runstudio) panels.runstudio.classList.toggle("active", resolved === "runstudio");
    if (resolved === "federlicht") {
      syncPromptFromFile(true).catch((err) => {
        if (!isMissingFileError(err)) {
          appendLog(`[prompt] failed to load: ${err}\n`);
        }
      });
    }
  };
  const initial = tabs.find((t) => t.classList.contains("active"))?.dataset.tab;
  setActiveTab(initial || "feather");
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const key = tab.dataset.tab;
      setActiveTab(key || "feather");
    });
  });
}

function handleQuickRunButtons() {
  const featherQuick = $("#quick-run-feather");
  const federlichtQuick = $("#quick-run-federlicht");
  featherQuick?.addEventListener("click", () => {
    $("#feather-form")?.requestSubmit();
  });
  federlichtQuick?.addEventListener("click", () => {
    $("#federlicht-form")?.requestSubmit();
  });
}

function handlePromptExpandControl() {
  const editor = $("#federlicht-prompt");
  const button = $("#federlicht-prompt-expand");
  if (!editor || !button) return;
  const applyState = () => {
    const expanded = editor.classList.contains("is-expanded");
    button.classList.toggle("is-active", expanded);
    button.textContent = expanded ? "Collapse Prompt" : "Expand Prompt";
  };
  button.addEventListener("click", () => {
    editor.classList.toggle("is-expanded");
    applyState();
  });
  applyState();
}

function syncFeatherOutputHint() {
  const output = $("#feather-output");
  const hint = $("#feather-output-hint");
  if (!output || !hint) return;
  const base = siteRunsPrefix();
  const current = normalizePathString(output.value || "");
  if (!current) {
    hint.innerHTML = `Run Folder에서 대상을 선택하세요. 현재 run root: <code>${escapeHtml(base)}</code>`;
    return;
  }
  const resolved = normalizePathString(expandSiteRunsPath(current));
  hint.innerHTML = `선택 run: <code>${escapeHtml(resolved || current)}</code>`;
}

function handleFeatherRunName() {
  const runName = $("#feather-run-name");
  const output = $("#feather-output");
  const input = $("#feather-input");
  if (!output) return;
  if (runName) runName.setAttribute("readonly", "readonly");
  output.setAttribute("readonly", "readonly");
  output.classList.add("readonly-field");
  input?.addEventListener("input", () => {
    featherInputTouched = true;
  });
  syncFeatherOutputHint();
}

function handleFeatherAgenticControls() {
  const toggle = $("#feather-agentic-search");
  const iterInput = $("#feather-max-iter");
  const policyNote = $("#feather-agentic-policy-note");
  if (!toggle) return;
  const updatePolicyNote = () => {
    if (!policyNote) return;
    const policy = normalizeGlobalModelPolicy(state.modelPolicy, state.modelPolicy.backend);
    const backend = normalizeAskLlmBackend(policy.backend || "openai_api");
    const backendLabel = backend === "codex_cli" ? "Codex CLI Auth" : "OpenAI API";
    const modelLabel = normalizeModelToken(policy.model || (backend === "codex_cli" ? codexModelHint() : openaiModelHint()));
    if (!toggle.checked) {
      policyNote.textContent = `Agentic Search OFF · 전역 LLM 설정 유지 (backend=${backendLabel}, model=${modelLabel || "-"})`;
      return;
    }
    policyNote.textContent = `Agentic Search ON · backend=${backendLabel} · model=${modelLabel || "-"}`;
  };
  const applyState = () => {
    if (iterInput) iterInput.disabled = false;
    updatePolicyNote();
  };
  toggle.addEventListener("change", applyState);
  document.addEventListener("federnett:model-policy-updated", updatePolicyNote);
  applyState();
}

function handlePipelineBackendControls() {
  const federBackend = $("#federlicht-llm-backend");
  const modelInput = $("#federlicht-model");
  const checkModelInput = $("#federlicht-check-model");
  const visionInput = $("#federlicht-model-vision");
  const reasoningSelect = $("#federlicht-reasoning-effort");
  const syncAndAnnounce = (source = "") => {
    const next = syncFederlichtModelControls({ announce: true });
    if (source === "backend") {
      appendLog(`[federlicht] backend: ${next.backend}\n`);
    }
    return next;
  };
  federBackend?.addEventListener("change", () => {
    syncFederlichtModelControls({ announce: true, forceBackendDefaults: true });
    appendLog(`[federlicht] backend: ${normalizeAskLlmBackend(federBackend.value)}\n`);
    maybeSyncGlobalModelPolicyFromSource("federlicht");
  });
  modelInput?.addEventListener("input", () => {
    syncFederlichtModelControls({ announce: false });
    maybeSyncGlobalModelPolicyFromSource("federlicht");
  });
  checkModelInput?.addEventListener("input", () => {
    syncFederlichtModelControls({ announce: false });
    maybeSyncGlobalModelPolicyFromSource("federlicht");
  });
  visionInput?.addEventListener("input", () => {
    syncFederlichtModelControls({ announce: false });
    maybeSyncGlobalModelPolicyFromSource("federlicht");
  });
  modelInput?.addEventListener("change", () => {
    syncAndAnnounce("model");
    maybeSyncGlobalModelPolicyFromSource("federlicht");
  });
  checkModelInput?.addEventListener("change", () => {
    syncAndAnnounce("check");
    maybeSyncGlobalModelPolicyFromSource("federlicht");
  });
  visionInput?.addEventListener("change", () => {
    syncAndAnnounce("vision");
    maybeSyncGlobalModelPolicyFromSource("federlicht");
  });
  reasoningSelect?.addEventListener("change", () => {
    syncAndAnnounce("reasoning");
    maybeSyncGlobalModelPolicyFromSource("federlicht");
  });
  syncFederlichtModelControls({ announce: false });
}

function syncModelInputCatalogBindings() {
  const globalBackend = normalizeAskLlmBackend(
    $("#global-llm-backend")?.value || state.modelPolicy.backend || "openai_api",
  );
  bindModelInputCatalog($("#ask-model"), globalBackend);
  bindModelInputCatalog($("#live-ask-model"), globalBackend);
  bindModelInputCatalog($("#global-model"), globalBackend);
  bindModelInputCatalog($("#global-check-model"), globalBackend);
  bindModelInputCatalog($("#global-vision-model"), globalBackend);
  bindModelInputCatalog($("#template-gen-model"), "openai_api");
}

function handleRunOutputTouch() {
  $("#federlicht-output")?.addEventListener("input", () => {
    reportOutputTouched = true;
    refreshFederlichtOutputHint().catch(() => {});
    syncFederlichtFieldTitles();
  });
  $("#federlicht-output")?.addEventListener("change", () => {
    reportOutputTouched = true;
    refreshFederlichtOutputHint().catch(() => {});
    syncFederlichtFieldTitles();
  });
  $("#federlicht-prompt-file")?.addEventListener("input", () => {
    promptFileTouched = true;
    syncFederlichtFieldTitles();
  });
  $("#federlicht-prompt-file")?.addEventListener("change", () => {
    promptFileTouched = true;
    syncFederlichtFieldTitles();
    syncPromptFromFile(true).catch((err) => {
      if (!isMissingFileError(err)) {
        appendLog(`[prompt] failed to load: ${err}\n`);
      }
    });
  });
  $("#prompt-output")?.addEventListener("input", () => {
    promptOutputTouched = true;
  });
  $("#federlicht-prompt")?.addEventListener("input", () => {
    promptInlineTouched = true;
  });
}

function handlePipelineInputs() {
  $("#federlicht-stages")?.addEventListener("change", () => {
    initPipelineFromInputs();
  });
  $("#federlicht-skip-stages")?.addEventListener("change", () => {
    initPipelineFromInputs();
  });
  $("#federlicht-quality-iterations")?.addEventListener("input", () => {
    setQualityIterations($("#federlicht-quality-iterations")?.value || 0);
    syncWorkflowQualityControls();
    renderWorkflow();
  });
}

function handleRunChanges() {
  $("#run-select")?.addEventListener("change", () => {
    const runRel = $("#run-select").value;
    if ($("#prompt-run-select")) $("#prompt-run-select").value = runRel;
    if ($("#instruction-run-select")) $("#instruction-run-select").value = runRel;
    const newPath = $("#instruction-new-path");
    if (newPath) newPath.value = defaultInstructionPath(runRel);
    promptFileTouched = false;
    promptInlineTouched = false;
    refreshRunDependentFields();
    updateTemplateEditorPath();
    loadTemplates().catch((err) => {
      appendLog(`[templates] failed to refresh: ${err}\n`);
    });
    updateHeroStats();
    updateRunStudio(runRel).catch((err) => {
      appendLog(`[studio] failed to refresh run studio: ${err}\n`);
    });
    syncWorkflowStageOverridesToRun().catch((err) => {
      appendLog(`[workflow] stage override sync failed: ${err}\n`);
    });
    maybeReloadAskHistory();
  });
  $("#instruction-run-select")?.addEventListener("change", () => {
    const runRel = $("#instruction-run-select").value;
    if ($("#run-select")) $("#run-select").value = runRel;
    if ($("#prompt-run-select")) $("#prompt-run-select").value = runRel;
    const newPath = $("#instruction-new-path");
    if (newPath) newPath.value = defaultInstructionPath(runRel);
    promptFileTouched = false;
    promptInlineTouched = false;
    refreshRunDependentFields();
    updateTemplateEditorPath();
    loadTemplates().catch((err) => {
      appendLog(`[templates] failed to refresh: ${err}\n`);
    });
    updateHeroStats();
    updateRunStudio(runRel).catch((err) => {
      appendLog(`[studio] failed to refresh run studio: ${err}\n`);
    });
    syncWorkflowStageOverridesToRun().catch((err) => {
      appendLog(`[workflow] stage override sync failed: ${err}\n`);
    });
    maybeReloadAskHistory();
  });
  $("#prompt-run-select")?.addEventListener("change", () => {
    const runRel = $("#prompt-run-select").value;
    if ($("#run-select")) $("#run-select").value = runRel;
    if ($("#instruction-run-select")) $("#instruction-run-select").value = runRel;
    const newPath = $("#instruction-new-path");
    if (newPath) newPath.value = defaultInstructionPath(runRel);
    promptFileTouched = false;
    promptInlineTouched = false;
    refreshRunDependentFields();
    updateTemplateEditorPath();
    loadTemplates().catch((err) => {
      appendLog(`[templates] failed to refresh: ${err}\n`);
    });
    updateHeroStats();
    updateRunStudio(runRel).catch((err) => {
      appendLog(`[studio] failed to refresh run studio: ${err}\n`);
    });
    syncWorkflowStageOverridesToRun().catch((err) => {
      appendLog(`[workflow] stage override sync failed: ${err}\n`);
    });
    maybeReloadAskHistory();
  });
}

function handleRunOpen() {
  const openRunPickerFromUi = () => {
    openRunPickerModal();
    loadWorkspaceSettings()
      .catch(() => null)
      .finally(() => {
        loadRunPickerItems();
      });
  };
  $("#workspace-run-folder")?.addEventListener("click", openRunPickerFromUi);
  $("#sidebar-open-run-folder")?.addEventListener("click", openRunPickerFromUi);
  $("#feather-open-run-folder")?.addEventListener("click", openRunPickerFromUi);
  $("#federlicht-open-run-folder")?.addEventListener("click", openRunPickerFromUi);
}

function handleInstructionEditor() {
  $("#instruction-file-select")?.addEventListener("change", () => {
    const pathRel = $("#instruction-file-select").value;
    loadInstructionContent(pathRel).catch((err) => {
      appendLog(`[instruction] failed to load file: ${err}\n`);
    });
  });
  $("#instruction-reload")?.addEventListener("click", () => {
    const runRel = $("#instruction-run-select")?.value;
    if (!runRel) return;
    loadInstructionFiles(runRel).catch((err) => {
      appendLog(`[instruction] reload failed: ${err}\n`);
    });
  });
  $("#instruction-save")?.addEventListener("click", () => {
    const runRel = $("#instruction-run-select")?.value;
    if (!runRel) return;
    saveInstruction(runRel).catch((err) => {
      appendLog(`[instruction] save failed: ${err}\n`);
    });
  });
  $("#instruction-new")?.addEventListener("click", () => {
    const runRel = $("#instruction-run-select")?.value;
    if (!runRel) return;
    const input = $("#instruction-new-path");
    if (!input) return;
    input.value = defaultInstructionPath(runRel);
    const editor = $("#instruction-editor");
    if (editor) {
      editor.value = "";
      editor.dataset.path = "";
    }
    input.focus();
    input.select();
  });
  $("#instruction-use-feather")?.addEventListener("click", () => {
    const runRel = $("#instruction-run-select")?.value;
    if (!runRel) return;
    const selected =
      $("#instruction-new-path")?.value ||
      $("#instruction-file-select")?.value ||
      defaultInstructionPath(runRel);
    if (!selected) return;
    const featherInput = $("#feather-input");
    if (featherInput) featherInput.value = selected;
    const featherOutput = $("#feather-output");
    if (featherOutput && !featherOutputTouched) {
      featherOutput.value = runRel;
    }
    appendLog(`[instruction] wired into Feather: ${selected}\n`);
  });
}

function handleFilePreviewControls() {
  mountPreviewPopupToLayer();
  const editor = $("#file-preview-editor");
  const saveAsInput = $("#file-preview-saveas-path");
  const previewSizeSelect = $("#file-preview-size");
  const previewBlock = mountPreviewPopupToLayer() || previewPopupElement();
  const previewHead = $("#preview-popup-head");
  const popupToggleBtn = $("#preview-popup-toggle");
  const popupCloseBtn = $("#preview-popup-close");
  const popupResetBtn = $("#preview-popup-reset");
  const popupMaxBtn = $("#preview-popup-maximize");
  try {
    const savedOpen = localStorage.getItem(PREVIEW_POPUP_OPEN_KEY);
    const initialOpen = savedOpen == null ? false : savedOpen === "true";
    setPreviewPopupOpen(initialOpen, { persist: false });
  } catch (err) {
    setPreviewPopupOpen(false, { persist: false });
  }
  restorePreviewPopupGeometry();
  try {
    const savedMax = localStorage.getItem(PREVIEW_POPUP_MAX_KEY);
    setPreviewPopupMaximized(savedMax === "true", { persist: false });
  } catch (err) {
    setPreviewPopupMaximized(false, { persist: false });
  }
  popupToggleBtn?.addEventListener("click", () => {
    const nextOpen = !state.previewPopup.open;
    setPreviewPopupOpen(nextOpen, { persist: true, focus: nextOpen });
  });
  popupCloseBtn?.addEventListener("click", () => {
    requestClosePreviewPopup({ persist: true, reason: "button" });
  });
  popupMaxBtn?.addEventListener("click", () => {
    setPreviewPopupMaximized(!state.previewPopup.maximized, { persist: true });
    if (!state.previewPopup.open) {
      setPreviewPopupOpen(true, { persist: true, focus: true });
    }
  });
  popupResetBtn?.addEventListener("click", () => {
    setPreviewPopupMaximized(false, { persist: true });
    resetPreviewPopupGeometry();
    setPreviewPopupOpen(true, { persist: true, focus: true });
  });
  document.addEventListener("pointerdown", (ev) => {
    if (!state.previewPopup.open) return;
    const popup = previewPopupElement();
    if (!popup) return;
    const target = ev.target;
    if (!(target instanceof Element)) return;
    if (popup.contains(target)) return;
    if (isPreviewPopupTriggerTarget(target)) return;
    const closed = requestClosePreviewPopup({ persist: true, reason: "outside" });
    if (closed) {
      // Prevent the outside click from immediately toggling underlying details/links.
      ev.preventDefault();
      ev.stopPropagation();
    }
  });
  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape") return;
    if (!state.previewPopup.open) return;
    const closed = requestClosePreviewPopup({ persist: true, reason: "escape" });
    if (closed) {
      ev.preventDefault();
      ev.stopPropagation();
    }
  });
  if (previewBlock && previewHead) {
    let dragging = false;
    let dragOffsetX = 0;
    let dragOffsetY = 0;
    const move = (ev) => {
      if (!dragging) return;
      const rect = previewBlock.getBoundingClientRect();
      const width = rect.width || previewBlock.offsetWidth;
      const height = rect.height || previewBlock.offsetHeight;
      const maxLeft = Math.max(8, window.innerWidth - width - 8);
      const maxTop = Math.max(8, window.innerHeight - height - 8);
      const nextLeft = Math.min(Math.max(ev.clientX - dragOffsetX, 8), maxLeft);
      const nextTop = Math.min(Math.max(ev.clientY - dragOffsetY, 8), maxTop);
      previewBlock.style.left = `${Math.round(nextLeft)}px`;
      previewBlock.style.top = `${Math.round(nextTop)}px`;
      previewBlock.style.right = "auto";
      previewBlock.style.bottom = "auto";
    };
    const stop = () => {
      if (!dragging) return;
      dragging = false;
      window.removeEventListener("pointermove", move);
      window.removeEventListener("pointerup", stop);
      savePreviewPopupGeometry();
    };
    previewHead.addEventListener("pointerdown", (ev) => {
      if (state.previewPopup.maximized) return;
      if (ev.button !== 0) return;
      const target = ev.target;
      if (target instanceof Element) {
        const interactive = target.closest("button,select,input,textarea,a,label,summary");
        if (interactive) return;
      }
      dragging = true;
      const rect = previewBlock.getBoundingClientRect();
      previewBlock.style.left = `${Math.round(rect.left)}px`;
      previewBlock.style.top = `${Math.round(rect.top)}px`;
      previewBlock.style.right = "auto";
      previewBlock.style.bottom = "auto";
      dragOffsetX = ev.clientX - rect.left;
      dragOffsetY = ev.clientY - rect.top;
      previewHead.setPointerCapture(ev.pointerId);
      window.addEventListener("pointermove", move);
      window.addEventListener("pointerup", stop);
    });
    previewBlock.addEventListener("mouseup", () => {
      if (!state.previewPopup.open) return;
      savePreviewPopupGeometry();
    });
    window.addEventListener("resize", () => {
      if (!state.previewPopup.open) return;
      if (state.previewPopup.maximized) return;
      clampPreviewPopupPosition();
      savePreviewPopupGeometry();
    });
  }
  const applyPreviewSize = (value) => {
    if (!previewBlock) return;
    const valid = value === "compact" || value === "expanded" ? value : "fit";
    previewBlock.dataset.previewSize = valid;
    if (previewSizeSelect && previewSizeSelect.value !== valid) {
      previewSizeSelect.value = valid;
    }
    localStorage.setItem("federnett-preview-size", valid);
  };
  if (previewSizeSelect) {
    const storedSize = localStorage.getItem("federnett-preview-size") || previewSizeSelect.value || "fit";
    applyPreviewSize(storedSize);
    previewSizeSelect.addEventListener("change", () => {
      applyPreviewSize(previewSizeSelect.value);
    });
  } else {
    applyPreviewSize("fit");
  }
  const pickDownloadFilename = ({ preferPdf = false } = {}) => {
    const rel = normalizePathString(state.filePreview.path || "");
    const mode = String(state.filePreview.mode || "text").toLowerCase();
    if (rel) {
      const leaf = rel.split("/").pop() || "download";
      if (!preferPdf) return leaf;
      if (/\.pdf$/i.test(leaf)) return leaf;
      const stem = leaf.replace(/\.[^.]+$/, "") || "preview";
      return `${stem}.pdf`;
    }
    if (preferPdf) return "preview.pdf";
    if (mode === "markdown") return "preview.md";
    if (mode === "html") return "preview.html";
    if (mode === "json") return "preview.json";
    return "preview.txt";
  };
  const triggerDownload = (href, filename) => {
    if (!href) return false;
    const link = document.createElement("a");
    link.href = href;
    if (filename) link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    return true;
  };
  const openPrintWindow = ({ title, html, fullDocument = false }) => {
    const printWin = window.open("", "_blank", "width=1220,height=860");
    if (!printWin) return false;
    if (fullDocument) {
      printWin.document.open();
      printWin.document.write(html);
      printWin.document.close();
    } else {
      const safeTitle = escapeHtml(title || "Preview");
      const wrapped = `<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>${safeTitle}</title>
  <style>
    :root { color-scheme: light; }
    body {
      margin: 24px;
      color: #101820;
      background: #ffffff;
      font-family: "Noto Sans KR", "Segoe UI", sans-serif;
      line-height: 1.65;
      font-size: 15px;
    }
    pre {
      white-space: pre-wrap;
      word-break: break-word;
      overflow-wrap: anywhere;
      margin: 0;
      font-family: "IBM Plex Mono", ui-monospace, monospace;
      font-size: 13px;
      line-height: 1.6;
    }
    img { max-width: 100%; height: auto; display: block; margin: 0 auto; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ccd4e2; padding: 8px 10px; text-align: left; }
    a { color: #0b63c6; }
    @page { size: auto; margin: 16mm; }
  </style>
</head>
<body>${html || ""}</body>
</html>`;
      printWin.document.open();
      printWin.document.write(wrapped);
      printWin.document.close();
    }
    const trigger = () => {
      try {
        printWin.focus();
        printWin.print();
      } catch (err) {
        // ignore
      }
    };
    window.setTimeout(trigger, 320);
    window.setTimeout(trigger, 920);
    return true;
  };
  const buildPdfExportMarkup = async () => {
    const rel = normalizePathString(state.filePreview.path || "");
    const mode = String(state.filePreview.mode || "text").toLowerCase();
    if (mode === "html") {
      const inlineDoc = String(state.filePreview.htmlDoc || "").trim();
      if (inlineDoc) {
        return { html: inlineDoc, fullDocument: /<html[\s>]/i.test(inlineDoc) };
      }
      if (rel) {
        try {
          const data = await fetchJSON(`/api/files?path=${encodeURIComponent(rel)}`);
          const content = String(data?.content || "").trim();
          if (content) {
            return { html: content, fullDocument: /<html[\s>]/i.test(content) };
          }
        } catch (err) {
          // fallback below
        }
      }
      const frameHtml = $("#file-preview-frame")?.contentDocument?.documentElement?.outerHTML || "";
      if (frameHtml) return { html: frameHtml, fullDocument: true };
      return { html: `<pre>${escapeHtml(state.filePreview.content || "(empty file)")}</pre>`, fullDocument: false };
    }
    if (mode === "markdown") {
      const rendered = $("#file-preview-markdown")?.innerHTML || renderMarkdown(state.filePreview.content || "");
      return { html: rendered, fullDocument: false };
    }
    if (mode === "image") {
      const src = state.filePreview.objectUrl
        || (rel ? rawFileUrl(rel) : $("#file-preview-image")?.src || "");
      if (!src) return { html: "", fullDocument: false };
      return { html: `<img src="${escapeHtml(src)}" alt="" />`, fullDocument: false };
    }
    const text = String(state.filePreview.content || "").trim();
    return {
      html: `<pre>${escapeHtml(text || "(empty file)")}</pre>`,
      fullDocument: false,
    };
  };
  editor?.addEventListener("input", () => {
    if (!state.filePreview.canEdit) return;
    state.filePreview.dirty = true;
    state.filePreview.content = editor.value || "";
    const statusEl = $("#file-preview-status");
    if (statusEl) statusEl.textContent = "modified";
  });
  $("#file-preview-open")?.addEventListener("click", () => {
    const rel = state.filePreview.path;
    if (!rel) return;
    const url = state.filePreview.objectUrl || rawFileUrl(rel);
    if (!url) return;
    const lower = String(rel).toLowerCase();
    if (lower.endsWith(".pptx")) {
      const name = rel.split("/").pop() || "download.pptx";
      const link = document.createElement("a");
      link.href = url;
      link.download = name;
      document.body.appendChild(link);
      link.click();
      link.remove();
      return;
    }
    window.open(url, "_blank", "noopener");
  });
  $("#file-preview-canvas")?.addEventListener("click", () => {
    const rel = state.filePreview.path;
    if (!rel) return;
    const url = `./canvas.html?report=${encodeURIComponent(rel)}`;
    window.open(url, "_blank", "noopener");
  });
  $("#file-preview-save")?.addEventListener("click", async () => {
    const rel = state.filePreview.path;
    const saveAsPath = saveAsInput?.value?.trim();
    const allowReadOnlySaveAs = canSaveReadOnlyPreviewAsCopy();
    if (!state.filePreview.canEdit && !allowReadOnlySaveAs) {
      setAskStatus("read-only 파일은 직접 저장할 수 없습니다.");
      return;
    }
    if (!state.filePreview.canEdit && allowReadOnlySaveAs) {
      openSaveAsModal(rel || "", "preview");
      const filenameInput = $("#saveas-filename");
      if (filenameInput && !filenameInput.value) {
        const base = String(rel || "preview.txt").split("/").pop() || "preview.txt";
        const suggested = base.replace(/(\.[^.]+)?$/, "_copy$1");
        filenameInput.value = suggested;
        filenameInput.focus();
        filenameInput.select();
      }
      setAskStatus("read-only 파일입니다. Save As로 저장 경로를 선택하세요.");
      return;
    }
    try {
      if (!rel && !saveAsPath) {
        openSaveAsModal(rel || "", "preview");
        return;
      }
      await saveFilePreview(rel || saveAsPath);
      appendLog(`[file] saved ${rel || saveAsPath}\n`);
    } catch (err) {
      appendLog(`[file] save failed: ${err}\n`);
    }
  });
  $("#file-preview-saveas")?.addEventListener("click", () => {
    const rel = normalizePathString(state.filePreview.path || "");
    const mode = String(state.filePreview.mode || "text").toLowerCase();
    const filename = pickDownloadFilename();
    if (rel) {
      triggerDownload(state.filePreview.objectUrl || rawFileUrl(rel), filename);
      appendLog(`[file] downloaded ${rel}\n`);
      return;
    }
    const inlineContent = mode === "html"
      ? String(state.filePreview.htmlDoc || state.filePreview.content || "")
      : String(state.filePreview.content || "");
    if (!inlineContent) {
      appendLog("[file] download skipped: no preview content\n");
      return;
    }
    const mime =
      mode === "html"
        ? "text/html;charset=utf-8"
        : mode === "markdown"
          ? "text/markdown;charset=utf-8"
          : "text/plain;charset=utf-8";
    const blob = new Blob([inlineContent], { type: mime });
    const blobUrl = URL.createObjectURL(blob);
    try {
      triggerDownload(blobUrl, filename);
      appendLog(`[file] downloaded ${filename}\n`);
    } finally {
      window.setTimeout(() => {
        URL.revokeObjectURL(blobUrl);
      }, 1500);
    }
  });
  $("#file-preview-export-pdf")?.addEventListener("click", async () => {
    const rel = normalizePathString(state.filePreview.path || "");
    const mode = String(state.filePreview.mode || "text").toLowerCase();
    try {
      if (mode === "pdf" && rel) {
        triggerDownload(state.filePreview.objectUrl || rawFileUrl(rel), pickDownloadFilename({ preferPdf: true }));
        appendLog(`[file] downloaded ${rel}\n`);
        return;
      }
      const payload = await buildPdfExportMarkup();
      if (!payload?.html) {
        appendLog("[file] pdf export skipped: no preview content\n");
        return;
      }
      const opened = openPrintWindow({
        title: pickDownloadFilename({ preferPdf: true }),
        html: payload.html,
        fullDocument: !!payload.fullDocument,
      });
      if (!opened) {
        appendLog("[file] pdf export failed: popup blocked\n");
        return;
      }
      appendLog(`[file] pdf export started (${rel || "inline content"})\n`);
    } catch (err) {
      appendLog(`[file] pdf export failed: ${err}\n`);
    }
  });
  $("#saveas-confirm")?.addEventListener("click", async () => {
    const filenameInput = $("#saveas-filename");
    const rel = state.saveAs.path;
    const filename = filenameInput?.value?.trim();
    if (!filename) return;
    const target = rel ? `${rel}/${filename}` : filename;
    try {
      const mode = state.saveAs.mode || "preview";
      if (mode === "prompt") {
        const content = $("#federlicht-prompt")?.value || "";
        await savePromptContent(target, content);
        const promptField = $("#federlicht-prompt-file");
        if (promptField) promptField.value = target;
        promptFileTouched = true;
        appendLog(`[prompt] saved as ${target}\n`);
      } else {
        await saveFilePreview(target);
        if (saveAsInput) saveAsInput.value = target;
        appendLog(`[file] saved as ${target}\n`);
      }
      closeSaveAsModal();
    } catch (err) {
      appendLog(`[file] save-as failed: ${err}\n`);
    }
  });
  $("#saveas-up")?.addEventListener("click", () => {
    const current = state.saveAs.path || "";
    const parent = current.replace(/\/[^/]*$/, "");
    loadSaveAsDir(parent);
  });
  document.querySelectorAll("[data-saveas-close]").forEach((btn) =>
    btn.addEventListener("click", closeSaveAsModal)
  );
}

function handleFeatherInstructionPicker() {
  const openBtn = $("#feather-pick-instruction");
  const saveBtn = $("#feather-save-instruction");
  const saveAsInlineBtn = $("#feather-saveas-instruction");
  const modal = $("#instruction-modal");
  const search = $("#instruction-search");
  const saveAsBtn = $("#instruction-saveas-btn");
  const useSelectedBtn = $("#instruction-use-selected");
  const importInput = $("#instruction-import");
  const saveAsInput = $("#instruction-saveas");

  const applySelection = async (pathRel) => {
    if (!pathRel) return;
    $("#feather-input").value = pathRel;
    featherInputTouched = true;
    await loadFeatherInstructionContent(pathRel).catch((err) => {
      appendLog(`[instruction] failed to load content: ${err}\n`);
    });
  };

  const refreshModal = async () => {
    await loadInstructionModalItems();
  };

  const filterModal = () => {
    const query = search?.value?.trim().toLowerCase() || "";
    if (!query) {
      state.instructionModal.filtered = [];
    } else {
      state.instructionModal.filtered = state.instructionModal.items.filter((item) => {
        return (
          item.name?.toLowerCase().includes(query) ||
          item.path?.toLowerCase().includes(query)
        );
      });
    }
    renderInstructionModalList();
  };

  openBtn?.addEventListener("click", async () => {
    openInstructionModal("feather");
    await refreshModal();
  });

  modal?.querySelectorAll("[data-modal-close]")?.forEach((el) => {
    el.addEventListener("click", () => {
      closeInstructionModal();
    });
  });

  search?.addEventListener("input", filterModal);

  useSelectedBtn?.addEventListener("click", async () => {
    const mode = state.instructionModal.mode || "feather";
    const pathRel =
      state.instructionModal.selectedPath || saveAsInput?.value?.trim() || "";
    if (!pathRel) return;
    if (mode === "prompt") {
      const promptField = $("#federlicht-prompt-file");
      if (promptField) promptField.value = pathRel;
      promptFileTouched = true;
      syncPromptFromFile(true).catch((err) => {
        if (!isMissingFileError(err)) {
          appendLog(`[prompt] failed to load: ${err}\n`);
        }
      });
      closeInstructionModal();
      return;
    }
    await applySelection(pathRel);
    closeInstructionModal();
  });

  saveAsBtn?.addEventListener("click", async () => {
    const mode = state.instructionModal.mode || "feather";
    const rawPath = saveAsInput?.value || $("#feather-input")?.value;
    const runRel = state.instructionModal.runRel;
    const normalized =
      mode === "prompt"
        ? normalizeInstructionPath(runRel, rawPath || "")
        : normalizeFeatherInstructionPath(rawPath);
    if (!normalized) return;
    if (mode === "prompt") {
      const promptField = $("#federlicht-prompt-file");
      if (promptField) promptField.value = normalized;
      promptFileTouched = true;
      syncPromptFromFile(true).catch((err) => {
        if (!isMissingFileError(err)) {
          appendLog(`[prompt] failed to load: ${err}\n`);
        }
      });
      closeInstructionModal();
      return;
    }
    const content = $("#feather-query")?.value || "";
    await saveInstructionContent(normalized, content).catch((err) => {
      appendLog(`[instruction] save-as failed: ${err}\n`);
    });
    $("#feather-input").value = normalized;
    featherInputTouched = true;
    await applySelection(normalized);
    closeInstructionModal();
    await loadRuns().catch(() => {});
  });

  saveBtn?.addEventListener("click", async () => {
    const rawPath = $("#feather-input")?.value;
    const normalized = normalizeFeatherInstructionPath(rawPath);
    const content = $("#feather-query")?.value || "";
    const editor = $("#feather-query");
    const loadedPath = editor?.dataset.path || "";
    const isDirty = isFeatherInstructionDirty();
    if (!rawPath || !rawPath.trim()) {
      openInstructionModal("feather");
      await refreshModal();
      if (saveAsInput) saveAsInput.focus();
      return;
    }
    if (normalized !== loadedPath && normalized.trim()) {
      await saveInstructionContent(normalized, content).catch((err) => {
        appendLog(`[instruction] save failed: ${err}\n`);
      });
      $("#feather-input").value = normalized;
      featherInputTouched = true;
      setFeatherInstructionSnapshot(normalized, content);
      await loadRuns().catch(() => {});
      return;
    }
    if (isDirty) {
      const ok = window.confirm(
        "This instruction was loaded from an existing file. Save a new copy to avoid overwriting?",
      );
      if (!ok) return;
      openInstructionModal("feather");
      await refreshModal();
      if (saveAsInput) {
        saveAsInput.value = normalizeFeatherInstructionPath(normalized);
        saveAsInput.focus();
        saveAsInput.select();
      }
      return;
    }
    await saveInstructionContent(normalized, content).catch((err) => {
      appendLog(`[instruction] save failed: ${err}\n`);
    });
    $("#feather-input").value = normalized;
    featherInputTouched = true;
    setFeatherInstructionSnapshot(normalized, content);
    await loadRuns().catch(() => {});
  });

  saveAsInlineBtn?.addEventListener("click", async () => {
    const rawPath = $("#feather-input")?.value;
    openInstructionModal("feather");
    await refreshModal();
    if (saveAsInput) {
      saveAsInput.value = normalizeFeatherInstructionPath(rawPath);
      saveAsInput.focus();
      saveAsInput.select();
    }
  });

  importInput?.addEventListener("change", async () => {
    const file = importInput.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = async () => {
      const content = reader.result ? String(reader.result) : "";
      const editor = $("#feather-query");
      if (editor) editor.value = content;
      openInstructionModal("feather");
      await refreshModal();
      if (saveAsInput && !saveAsInput.value.trim()) {
        saveAsInput.value = normalizeFeatherInstructionPath(
          $("#feather-input")?.value || "",
        );
      }
    };
    reader.readAsText(file);
    importInput.value = "";
  });
}

function handleCanvasModal() {
  const modal = $("#canvas-modal");
  if (!modal) return;
  modal.querySelectorAll("[data-canvas-close]").forEach((el) => {
    el.addEventListener("click", () => closeCanvasModal());
  });
  $("#canvas-use-selection")?.addEventListener("click", () => {
    syncCanvasSelection();
  });
  $("#canvas-clear-selection")?.addEventListener("click", () => {
    state.canvas.selection = "";
    updateCanvasFields();
  });
  $("#canvas-output-path")?.addEventListener("input", (event) => {
    const value = event.target?.value || "";
    state.canvas.outputPath = value;
  });
  $("#canvas-run")?.addEventListener("click", () => {
    runCanvasUpdate().catch((err) => {
      appendLog(`[canvas] update failed: ${err}\n`);
    });
  });
}

function handleUploadDrop() {
  const target = document.body;
  if (!target) return;
  const onDragOver = (ev) => {
    if (!isFeatherTab()) return;
    ev.preventDefault();
  };
  const onDrop = async (ev) => {
    if (!isFeatherTab()) return;
    ev.preventDefault();
    const file = ev.dataTransfer?.files?.[0];
    if (!file) return;
    try {
      const res = await fetch(`/api/upload?name=${encodeURIComponent(file.name)}`, {
        method: "POST",
        headers: { "Content-Type": file.type || "application/octet-stream" },
        body: file,
      });
      const payload = await res.json();
      if (!res.ok || payload?.error) {
        throw new Error(payload?.error || res.statusText);
      }
      const absPath = payload.abs_path || payload.path;
      const line = `file: "${absPath}" | title="${file.name}"`;
      const query = $("#feather-query");
      if (query) {
        const current = query.value || "";
        query.value = current ? `${current.trim()}\n${line}\n` : `${line}\n`;
      }
      const featherInput = $("#feather-input");
      if (featherInput) featherInput.value = "";
      appendLog(`[upload] added ${file.name} -> ${absPath}\n`);
    } catch (err) {
      appendLog(`[upload] failed: ${err}\n`);
    }
  };
  target.addEventListener("dragover", onDragOver);
  target.addEventListener("drop", onDrop);
}

function handleFederlichtPromptPicker() {
  const pickBtn = $("#federlicht-prompt-pick");
  const genBtn = $("#federlicht-prompt-generate");
  pickBtn?.addEventListener("click", async () => {
    openInstructionModal("prompt");
    await loadInstructionModalItems();
  });
  genBtn?.addEventListener("click", async () => {
    setPromptGenerateEnabled(false);
    try {
      const payload = buildPromptPayloadFromFederlicht();
      promptFileTouched = true;
      await startJob("/api/federlicht/generate_prompt", payload, {
        kind: "prompt",
        spotLabel: "Prompt Generate",
        spotPath: payload.output,
        onSuccess: async () => {
          if (payload.output) {
            await hydrateGeneratedPromptInline(payload.output).catch((err) => {
              if (!isMissingFileError(err)) {
                appendLog(`[prompt] failed to load: ${err}\n`);
              }
            });
            appendLog(`[prompt] ready: ${payload.output}\n`);
          }
        },
        onDone: () => {
          setPromptGenerateEnabled(true);
        },
      });
    } catch (err) {
      appendLog(`[prompt] ${err}\n`);
      setPromptGenerateEnabled(true);
    }
  });
}

function handleFederlichtPromptEditor() {
  const saveBtn = $("#federlicht-save-prompt");
  const saveAsBtn = $("#federlicht-saveas-prompt");
  saveBtn?.addEventListener("click", async () => {
    const editor = $("#federlicht-prompt");
    const promptField = $("#federlicht-prompt-file");
    const rawPath = promptField?.value?.trim();
    const normalized = normalizePromptPath(rawPath);
    const content = editor?.value || "";
    const loadedPath = editor?.dataset.path || "";
    const isDirty = isPromptDirty();
    if (!rawPath) {
      openSaveAsModal(normalized, "prompt");
      const filenameInput = $("#saveas-filename");
      if (filenameInput && normalized) {
        filenameInput.value = normalized.split("/").pop() || "";
      }
      return;
    }
    if (normalized && normalized !== loadedPath) {
      try {
        await savePromptContent(normalized, content);
        if (promptField) promptField.value = normalized;
        promptFileTouched = true;
      } catch (err) {
        appendLog(`[prompt] save failed: ${err}\n`);
      }
      return;
    }
    if (isDirty) {
      const ok = window.confirm(
        "This prompt was loaded from an existing file. Save a new copy to avoid overwriting?",
      );
      if (!ok) return;
      openSaveAsModal(normalized, "prompt");
      const filenameInput = $("#saveas-filename");
      if (filenameInput && normalized) {
        filenameInput.value = normalized.split("/").pop() || "";
        filenameInput.focus();
        filenameInput.select();
      }
      return;
    }
    try {
      await savePromptContent(normalized, content);
      if (promptField) promptField.value = normalized;
      promptFileTouched = true;
    } catch (err) {
      appendLog(`[prompt] save failed: ${err}\n`);
    }
  });

  saveAsBtn?.addEventListener("click", () => {
    const promptField = $("#federlicht-prompt-file");
    const rawPath = promptField?.value?.trim();
    const normalized = normalizePromptPath(rawPath);
    openSaveAsModal(normalized, "prompt");
    const filenameInput = $("#saveas-filename");
    if (filenameInput && normalized) {
      filenameInput.value = normalized.split("/").pop() || "";
      filenameInput.focus();
      filenameInput.select();
    }
  });
}

function handleRunPicker() {
  const modal = $("#run-picker-modal");
  const search = $("#run-picker-search");
  const rootSelect = $("#run-picker-root");
  const useBtn = $("#run-picker-use");
  const openBtn = $("#run-picker-open");
  const createBtn = $("#run-picker-create");
  const createNameInput = $("#run-picker-create-name");
  const reloadBtn = $("#run-picker-reload");
  const runRootAddInput = $("#workspace-run-root-add");
  const runRootAddBtn = $("#workspace-run-root-add-btn");
  const settingsReloadBtn = $("#workspace-settings-reload");
  const settingsSaveBtn = $("#workspace-settings-save");
  const applySelection = async (runRel) => {
    const resolved = normalizePathString(runRel || "");
    if (!resolved) return;
    const runSelect = $("#run-select");
    if (runSelect) runSelect.value = resolved;
    applyRunFolderSelection(resolved);
    refreshRunDependentFields();
    await updateRunStudio(resolved).catch((err) => {
      appendLog(`[studio] failed to refresh run studio: ${err}\n`);
    });
  };
  const filterRunPickerByQuery = () => {
    const query = String(search?.value || "").trim().toLowerCase();
    state.runPicker.query = query;
    if (!query) {
      state.runPicker.filtered = [];
    } else {
      state.runPicker.filtered = state.runPicker.items.filter((item) => {
        const rel = String(item.run_rel || "").toLowerCase();
        const name = String(item.run_name || "").toLowerCase();
        return rel.includes(query) || name.includes(query);
      });
    }
    renderRunPickerList();
  };
  const reloadRunPicker = () => {
    state.runPicker.items = runPickerItems();
    if (!state.runPicker.items.some((item) => item.run_rel === state.runPicker.selected)) {
      state.runPicker.selected = state.runPicker.items[0]?.run_rel || "";
    }
    filterRunPickerByQuery();
  };
  modal?.querySelectorAll("[data-runpicker-close]")?.forEach((el) => {
    el.addEventListener("click", () => closeRunPickerModal());
  });
  search?.addEventListener("input", filterRunPickerByQuery);
  rootSelect?.addEventListener("change", () => {
    state.runPicker.root = normalizePathString(rootSelect.value || "");
    reloadRunPicker();
  });
  createNameInput?.addEventListener("input", () => {
    const raw = String(createNameInput.value || "");
    const normalized = raw.replace(/\s+/g, "_").replace(/_+/g, "_");
    if (raw !== normalized) {
      createNameInput.value = normalized;
    }
  });
  const addRunRootFromInput = async () => {
    const raw = String(runRootAddInput?.value || "").trim();
    const sanitized = normalizePathString(raw.replace(/\s+/g, "_"));
    if (!sanitized) {
      setWorkspaceSettingsStatus("run root 입력값이 비어 있습니다.", true);
      return;
    }
    if (runRootAddInput && raw !== sanitized) {
      runRootAddInput.value = sanitized;
      appendLog(`[run-root] sanitized: ${raw} -> ${sanitized}\n`);
    }
    const appended = appendRunRootTokenToWorkspaceInput(sanitized);
    if (!appended) return;
    try {
      setWorkspaceSettingsStatus(`workspace settings saving... (add root: ${sanitized})`);
      await saveWorkspaceSettingsFromControls();
      await loadRunPickerItems();
      if (rootSelect) rootSelect.value = sanitized;
      state.runPicker.root = sanitized;
      if (runRootAddInput) runRootAddInput.value = "";
      setWorkspaceSettingsStatus(`run root added: ${sanitized}`);
      appendLog(`[run-root] added: ${sanitized}\n`);
    } catch (err) {
      const errText = String(err || "");
      const legacyHint = /unknown_endpoint|404/i.test(errText)
        ? " · 실행 중 Federnett가 구버전일 수 있습니다(서버 재시작 필요)"
        : "";
      setWorkspaceSettingsStatus(`run root add failed: ${err}${legacyHint}`, true);
      appendLog(`[run-root] add failed: ${err}${legacyHint}\n`);
    }
  };
  runRootAddBtn?.addEventListener("click", () => {
    addRunRootFromInput();
  });
  runRootAddInput?.addEventListener("keydown", (ev) => {
    if (ev.key !== "Enter") return;
    ev.preventDefault();
    addRunRootFromInput();
  });
  reloadBtn?.addEventListener("click", async () => {
    try {
      await loadRuns();
      await loadRunPickerItems();
      setWorkspaceSettingsStatus("run folders reloaded");
    } catch (err) {
      appendLog(`[runs] reload failed: ${err}\n`);
      setWorkspaceSettingsStatus(`run folders reload failed: ${err}`, true);
    }
  });
  useBtn?.addEventListener("click", async () => {
    const runRel = state.runPicker.selected;
    if (!runRel) return;
    await applySelection(runRel);
    appendLog(`[run-folder] loaded: ${runRel}\n`);
    closeRunPickerModal();
  });
  openBtn?.addEventListener("click", async () => {
    const runRel = state.runPicker.selected;
    if (!runRel) return;
    await applySelection(runRel);
    openPath(runRel);
    appendLog(`[run-folder] opened: ${runRel}\n`);
    closeRunPickerModal();
  });
  createBtn?.addEventListener("click", async () => {
    const runNameRaw = String(createNameInput?.value || "").trim();
    const runNameNoSpaces = runNameRaw.replace(/\s+/g, "_");
    const runName = sanitizeRunNameHint(runNameNoSpaces);
    const root = normalizePathString(rootSelect?.value || state.runPicker.root || "");
    if (runNameRaw && !runName) {
      appendLog("[run-folder] create failed: run name is empty after sanitization\n");
      return;
    }
    if (createNameInput && runNameRaw && runName && runNameRaw !== runNameNoSpaces) {
      createNameInput.value = runName;
      appendLog(`[run-folder] sanitized run name: ${runNameRaw} -> ${runName}\n`);
    } else if (createNameInput && runNameRaw && runName && runNameRaw !== runName) {
      createNameInput.value = runName;
      appendLog(`[run-folder] normalized run name: ${runNameRaw} -> ${runName}\n`);
    }
    const payload = {
      run_name: runName || undefined,
      run_root: root || undefined,
    };
    try {
      const created = await fetchJSON("/api/runs/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      await loadRuns();
      const runRel = normalizePathString(created?.run_rel || "");
      if (runRel) {
        await applySelection(runRel);
        appendLog(`[run-folder] created: ${runRel}\n`);
      }
      if (createNameInput) createNameInput.value = "";
      await loadRunPickerItems();
      closeRunPickerModal();
    } catch (err) {
      appendLog(`[run-folder] create failed: ${err}\n`);
    }
  });
  settingsReloadBtn?.addEventListener("click", () => {
    loadWorkspaceSettings()
      .then(() => setWorkspaceSettingsStatus("workspace settings reloaded"))
      .catch((err) => {
        const errText = String(err || "");
        const legacyHint = /unknown_endpoint|404/i.test(errText)
          ? " · 실행 중 Federnett가 구버전일 수 있습니다(서버 재시작 필요)"
          : "";
        setWorkspaceSettingsStatus(`workspace settings reload failed: ${err}${legacyHint}`, true);
        appendLog(`[workspace] settings reload failed: ${err}${legacyHint}\n`);
      });
  });
  settingsSaveBtn?.addEventListener("click", async () => {
    try {
      setWorkspaceSettingsStatus("workspace settings saving...");
      await saveWorkspaceSettingsFromControls();
      setWorkspaceSettingsStatus("workspace settings saved");
    } catch (err) {
      const errText = String(err || "");
      const legacyHint = /unknown_endpoint|404/i.test(errText)
        ? " · 실행 중 Federnett가 구버전일 수 있습니다(서버 재시작 필요)"
        : "";
      setWorkspaceSettingsStatus(`workspace settings save failed: ${err}${legacyHint}`, true);
      appendLog(`[workspace] settings save failed: ${err}${legacyHint}\n`);
    }
  });
}

function handleModelPolicyModal() {
  $("#workspace-model-settings")?.addEventListener("click", () => {
    openModelPolicyModal();
  });
  $("#global-llm-backend")?.addEventListener("change", () => {
    syncModelInputCatalogBindings();
  });
  $("#model-policy-apply")?.addEventListener("click", () => {
    const policy = readGlobalModelPolicyControls();
    applyGlobalModelPolicy(policy, { persist: true, announce: true });
    closeModelPolicyModal();
  });
  $("#global-model-lock")?.addEventListener("change", (ev) => {
    state.modelPolicy.lock = Boolean(ev?.target?.checked);
    persistGlobalModelPolicy();
  });
  document.querySelectorAll("[data-modelpolicy-close]").forEach((el) => {
    el.addEventListener("click", () => closeModelPolicyModal());
  });
}

function handleJobsModal() {
  const modal = $("#jobs-modal");
  const openBtn = $("#jobs-open");
  openBtn?.addEventListener("click", (ev) => {
    ev.stopPropagation();
    openJobsModal();
  });
  modal?.querySelectorAll("[data-jobs-close]")?.forEach((el) => {
    el.addEventListener("click", () => closeJobsModal());
  });
}

function handleReloadRuns() {
  $("#reload-runs")?.addEventListener("click", async () => {
    try {
      await loadRuns();
    } catch (err) {
      appendLog(`[runs] reload failed: ${err}\n`);
    }
  });
}

function bindTemplateModalClose() {
  const modal = $("#template-modal");
  if (!modal) return;
  modal.querySelectorAll("[data-modal-close]").forEach((el) => {
    el.addEventListener("click", () => closeTemplateModal());
  });
}

function bindHelpModal() {
  const modal = $("#help-modal");
  $("#help-button")?.addEventListener("click", () => openHelpModal());
  $("#pipeline-help")?.addEventListener("click", () => openHelpModal());
  modal?.querySelectorAll("[data-help-close]")?.forEach((el) => {
    el.addEventListener("click", () => closeHelpModal());
  });
}

function handleWorkflowHistoryControls() {
  $("#workflow-resume-apply")?.addEventListener("click", () => {
    const targetStage = state.workflow.resumeStage || findWorkflowResumeStage();
    if (!targetStage) {
      appendLog("[workflow] resume preset failed: choose a stage first.\n");
      return;
    }
    const ok = applyResumeStagesFromStage(targetStage);
    if (!ok) {
      appendLog(`[workflow] resume preset failed: invalid stage ${targetStage}.\n`);
      return;
    }
    setJobStatus(`Resume preset ready from ${workflowLabel(targetStage)}.`, false);
  });
  $("#workflow-resume-prompt")?.addEventListener("click", async () => {
    const btn = $("#workflow-resume-prompt");
    const original = btn?.textContent || "Draft update prompt";
    if (btn) {
      btn.disabled = true;
      btn.textContent = "Drafting...";
    }
    try {
      await draftWorkflowResumePrompt();
    } catch (err) {
      appendLog(`[workflow] resume prompt failed: ${err}\n`);
    } finally {
      if (btn) btn.textContent = original;
      syncWorkflowHistoryControls();
    }
  });
  syncWorkflowHistoryControls();
}

function handleWorkflowStudioPanel() {
  const panel = $("#workflow-studio-panel");
  if (!panel) return;
  if (panel.parentElement !== document.body) {
    document.body.appendChild(panel);
  }
  panel.querySelectorAll("#pipeline-selected, .pipeline-selected").forEach((legacy) => {
    legacy.remove();
  });
  const toggleButtons = [
    $("#workflow-studio-toggle"),
    $("#workflow-studio-toggle-global"),
  ].filter(Boolean);
  const closeBtn = $("#workflow-studio-close");
  const applyBoundValue = (control) => {
    const targetSel = control.getAttribute("data-bind-target") || "";
    if (!targetSel) return;
    const target = $(targetSel);
    if (!target) return;
    if (control instanceof HTMLInputElement && control.type === "checkbox") {
      if (target instanceof HTMLInputElement) {
        target.checked = control.checked;
      }
      target.dispatchEvent(new Event("change", { bubbles: true }));
      syncWorkflowStudioBindings();
      return;
    }
    if ("value" in control && "value" in target) {
      target.value = control.value;
      target.dispatchEvent(new Event("input", { bubbles: true }));
      target.dispatchEvent(new Event("change", { bubbles: true }));
      syncWorkflowStudioBindings();
    }
  };
  panel.querySelectorAll("[data-bind-target]").forEach((control) => {
    const eventName = control.getAttribute("data-bind-event") || "input";
    control.addEventListener(eventName, () => applyBoundValue(control));
  });
  ["#wf-stage-enabled", "#wf-stage-prompt", "#wf-stage-tools"].forEach((selector) => {
    const control = $(selector);
    if (!control) return;
    const eventName = selector === "#wf-stage-enabled" ? "change" : "input";
    control.addEventListener(eventName, () => queueWorkflowStageOverrideSync());
  });
  $("#wf-stage-select")?.addEventListener("change", (ev) => {
    const value = String(ev.target?.value || "").trim().toLowerCase();
    if (!WORKFLOW_STAGE_ORDER.includes(value)) return;
    state.workflow.stageOverrideStage = value;
    state.pipeline.activeStageId = value;
    renderStageDetail(value);
    applyWorkflowStageOverrideControls(value);
  });
  $("#wf-stage-focus-active")?.addEventListener("click", () => {
    const ok = focusWorkflowStageOverrideToActive();
    if (!ok) {
      appendLog("[workflow] 활성 pipeline stage를 찾지 못했습니다. stage를 직접 선택하세요.\n");
    }
  });
  $("#wf-stage-reset")?.addEventListener("click", () => {
    const stageId = activeWorkflowStageForOverrides();
    resetWorkflowStageOverrideControls(stageId);
    appendLog(`[workflow] stage override reset: ${stageId}\n`);
  });
  $("#wf-quality-iterations")?.addEventListener("change", (ev) => {
    const value = Number.parseInt(String(ev.target?.value || "").trim(), 10);
    if (!Number.isFinite(value)) return;
    setQualityIterations(value);
    syncWorkflowQualityControls();
    renderWorkflow();
  });
  toggleButtons.forEach((toggleBtn) => {
    toggleBtn.addEventListener("click", () => {
      const next = !state.workflow.studioOpen;
      setWorkflowStudioOpen(next, { stageId: "overview" });
    });
  });
  closeBtn?.addEventListener("click", () => {
    setWorkflowStudioOpen(false);
  });
  $("#workflow-run-feather")?.addEventListener("click", () => {
    if (state.activeJobId) {
      appendLog("[workflow] job is running. wait until current job ends.\n");
      return;
    }
    document.querySelector('[data-tab="feather"]')?.dispatchEvent(
      new MouseEvent("click", { bubbles: true }),
    );
    $("#feather-form")?.requestSubmit();
  });
  $("#workflow-run-federlicht")?.addEventListener("click", () => {
    if (state.activeJobId) {
      appendLog("[workflow] job is running. wait until current job ends.\n");
      return;
    }
    syncWorkflowStageOverridesToRun()
      .catch((err) => appendLog(`[workflow] stage override sync failed: ${err}\n`))
      .finally(() => {
        document.querySelector('[data-tab="federlicht"]')?.dispatchEvent(
          new MouseEvent("click", { bubbles: true }),
        );
        $("#federlicht-form")?.requestSubmit();
      });
  });
  $("#workflow-run-all")?.addEventListener("click", async () => {
    if (state.activeJobId) {
      appendLog("[workflow] job is running. wait until current job ends.\n");
      return;
    }
    await syncWorkflowStageOverridesToRun().catch((err) => {
      appendLog(`[workflow] stage override sync failed: ${err}\n`);
    });
    await executeAskSuggestedAction("run_feather_then_federlicht");
  });
  $("#workflow-run-resume")?.addEventListener("click", () => {
    const targetStage =
      String(state.pipeline.activeStageId || state.workflow.resumeStage || findWorkflowResumeStage() || "").trim();
    if (!targetStage || !WORKFLOW_STAGE_ORDER.includes(targetStage)) {
      appendLog("[workflow] resume preset failed: choose a valid stage first.\n");
      return;
    }
    const ok = applyResumeStagesFromStage(targetStage);
    if (!ok) {
      appendLog(`[workflow] resume preset failed: invalid stage ${targetStage}.\n`);
      return;
    }
    syncWorkflowStageOverridesToRun()
      .catch((err) => appendLog(`[workflow] stage override sync failed: ${err}\n`))
      .finally(() => {
        document.querySelector('[data-tab="federlicht"]')?.dispatchEvent(
          new MouseEvent("click", { bubbles: true }),
        );
        $("#federlicht-form")?.requestSubmit();
      });
  });
  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape") return;
    if (!state.workflow.studioOpen) return;
    setWorkflowStudioOpen(false);
  });
  try {
    const saved = localStorage.getItem(WORKFLOW_STUDIO_OPEN_KEY);
    const statusToken = String(state.workflow.statusText || "").trim().toLowerCase();
    const workflowBusy =
      state.workflow.running
      || state.workflow.historyMode
      || (statusToken && statusToken !== "idle");
    const allowSavedOpen = window.innerWidth >= 1880 && !workflowBusy;
    setWorkflowStudioOpen(saved === "true" && allowSavedOpen, { stageId: "overview" });
  } catch (err) {
    setWorkflowStudioOpen(false, { stageId: "overview" });
  }
}

function toggleLogSourceVisibility(toggle) {
  if (!(toggle instanceof Element)) return false;
  const list = toggle.closest(".log-source-list.is-collapsible");
  const hidden = list?.querySelector(".log-source-hidden");
  if (!list || !hidden) return false;
  const expanded = list.getAttribute("data-source-expanded") === "true";
  const next = !expanded;
  list.setAttribute("data-source-expanded", next ? "true" : "false");
  const foldKey = String(list.getAttribute("data-source-fold-key") || "").trim();
  if (foldKey) {
    if (!state.liveAsk.inlineSourceFoldState || typeof state.liveAsk.inlineSourceFoldState !== "object") {
      state.liveAsk.inlineSourceFoldState = {};
    }
    state.liveAsk.inlineSourceFoldState[foldKey] = next;
    saveLiveAskPrefs();
  }
  hidden.hidden = !next;
  toggle.setAttribute("aria-expanded", next ? "true" : "false");
  const moreCount = Number(toggle.getAttribute("data-more-count") || "0");
  toggle.textContent = next ? "접기" : `+${moreCount}개 더보기`;
  return true;
}

function openLogPathFromLink(link, fallbackHref = "") {
  if (!(link instanceof Element)) return false;
  const explicitPath = String(link.getAttribute("data-log-path") || "").trim();
  const fallback = String(fallbackHref || "").trim();
  const relPath = explicitPath || normalizeLogPathCandidate(fallback);
  if (!relPath || !isLikelyPreviewFilePath(relPath)) return false;
  const startLine = Number(link.getAttribute("data-log-start") || 0);
  const endLine = Number(link.getAttribute("data-log-end") || startLine || 0);
  loadFilePreview(relPath, {
    focusLine: startLine > 0 ? startLine : 0,
    endLine: endLine > 0 ? endLine : startLine,
    readOnly: true,
  }).catch((err) => {
    appendLog(`[preview] failed to open from log: ${err}\n`);
  });
  return true;
}

function handleLinkedContentClick(ev) {
  const target = ev.target;
  if (!(target instanceof Element)) return;
  const sourceToggle = target.closest("[data-source-toggle]");
  if (sourceToggle) {
    ev.preventDefault();
    toggleLogSourceVisibility(sourceToggle);
    return;
  }
  const urlLink = target.closest("[data-log-url]");
  if (urlLink) {
    ev.preventDefault();
    const href = String(urlLink.getAttribute("data-log-url") || "").trim();
    if (href) window.open(href, "_blank", "noopener,noreferrer");
    return;
  }
  const pathLink = target.closest("[data-log-path]");
  if (pathLink) {
    ev.preventDefault();
    openLogPathFromLink(pathLink);
    return;
  }
  const anchor = target.closest("a[href]");
  if (!(anchor instanceof HTMLAnchorElement)) return;
  const href = String(anchor.getAttribute("href") || "").trim();
  if (!href || href === "#") return;
  if (/^https?:\/\//i.test(href)) {
    ev.preventDefault();
    window.open(href, "_blank", "noopener,noreferrer");
    return;
  }
  if (openLogPathFromLink(anchor, href)) {
    ev.preventDefault();
  }
}

function handleLogControls() {
  // Hide Logs UI removed: keep logs panel expanded by default.
  setLogsCollapsed(false);
  localStorage.removeItem("federnett-logs-collapsed");
  setLogMode("markdown");
  $("#log-clear")?.addEventListener("click", () => {
    clearLogs();
  });
  try {
    const savedMax = localStorage.getItem(LOGS_MAXIMIZED_KEY);
    setLogsMaximized(savedMax === "true", { persist: false });
  } catch (err) {
    setLogsMaximized(false, { persist: false });
  }
  $("#log-maximize")?.addEventListener("click", () => {
    const wrap = $("#logs-wrap");
    const next = !(wrap?.classList.contains("is-maximized"));
    setLogsMaximized(next, { persist: true });
  });
  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Escape") return;
    const wrap = $("#logs-wrap");
    if (!wrap?.classList.contains("is-maximized")) return;
    setLogsMaximized(false, { persist: true });
  });
  const bindLogAutoFollow = (el) => {
    if (!el) return;
    el.addEventListener(
      "scroll",
      () => {
        state.logAutoFollow = isNearBottom(el, 120);
      },
      { passive: true },
    );
  };
  const bindLinkedContentClick = (el) => {
    if (!el) return;
    el.addEventListener("click", handleLinkedContentClick);
  };
  bindLogAutoFollow($("#log-output"));
  bindLogAutoFollow($("#log-output-md"));
  bindLinkedContentClick($("#log-output"));
  bindLinkedContentClick($("#log-output-md"));
  bindLinkedContentClick($("#ask-answer"));
  bindLinkedContentClick($("#live-ask-thread"));
  $("#job-kill")?.addEventListener("click", async () => {
    const jobId = state.activeJobId;
    if (!jobId) return;
    try {
      appendLog(`[kill] ${shortId(jobId)}\n`);
      await fetchJSON(`/api/jobs/${jobId}/kill`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: "{}",
      });
    } catch (err) {
      appendLog(`[kill] failed: ${err}\n`);
    }
  });
}

function handleTemplateSync() {
  $("#template-select")?.addEventListener("change", () => {
    if ($("#prompt-template-select")) {
      $("#prompt-template-select").value = $("#template-select").value;
    }
    renderTemplatesPanel();
  });
}

function handleFreeFormatToggle() {
  const checkbox = $("#federlicht-free-format");
  if (!checkbox) return;
  checkbox.addEventListener("change", () => {
    applyFreeFormatMode();
    if (checkbox.checked) {
      const stylePack = ($("#federlicht-style-pack")?.value || "none").trim();
      appendLog(`[federlicht] free format enabled: template guidance disabled (style-pack=${stylePack}).\n`);
    }
  });
  applyFreeFormatMode();
}

function handleTemplateEditor() {
  $("#template-editor-name")?.addEventListener("input", updateTemplateEditorPath);
  $("#template-store-site")?.addEventListener("change", () => {
    updateTemplateEditorPath();
  });
  $("#template-editor-base")?.addEventListener("change", () => {
    const nameInput = $("#template-editor-name");
    if (nameInput && !nameInput.value) {
      const raw = $("#template-editor-base").value;
      const baseName = raw.includes("/") ? raw.split("/").pop()?.replace(/\\.md$/, "") : raw;
      nameInput.value = normalizeTemplateName(baseName || raw);
    }
    updateTemplateEditorPath();
  });
  $("#template-style-select")?.addEventListener("change", () => {
    const select = $("#template-style-select");
    if (select) state.templateBuilder.css = select.value || "";
    refreshTemplatePreview();
  });
  $("#template-section-add")?.addEventListener("click", () => {
    const rows = [...document.querySelectorAll(".template-section-row")].map((el) => ({
      name: el.querySelector("[data-section-name]")?.value || "",
      guide: el.querySelector("[data-section-guide]")?.value || "",
    }));
    rows.push({ name: "", guide: "" });
    renderTemplateSections(rows);
  });
  $("#template-apply-frontmatter")?.addEventListener("click", () => {
    applyBuilderToEditor();
  });
  $("#template-preview-refresh")?.addEventListener("click", () => {
    refreshTemplatePreview();
  });
  $("#template-editor-load")?.addEventListener("click", () => {
    loadTemplateEditorBase();
  });
  $("#template-editor-save")?.addEventListener("click", () => {
    saveTemplateEditor();
  });
}

function handleTemplateGenerator() {
  $("#template-generate")?.addEventListener("click", async () => {
    const button = $("#template-generate");
    const prompt = $("#template-gen-prompt")?.value?.trim();
    if (!prompt) {
      appendLog("[template-generator] prompt is required.\n");
      return;
    }
    const nameInput = $("#template-editor-name");
    let normalized = normalizeTemplateName(nameInput?.value || "");
    if (!normalized) {
      const fallback = slugifyLabel(prompt).slice(0, 24) || "custom_template";
      normalized = normalizeTemplateName(fallback);
      if (nameInput) nameInput.value = normalized;
    }
    if (nameInput) nameInput.value = normalized;
    updateTemplateEditorPath();
    const runRel = $("#run-select")?.value;
    const store = templateStoreChoice();
    if (store === "run" && !runRel) {
      appendLog("[template-generator] run folder is required for run storage.\n");
      return;
    }
    state.templateGen.log = "";
    appendTemplateGenLog("Generating template...\n");
    if (button) {
      button.disabled = true;
      button.textContent = "Generating...";
    }
    const payload = {
      prompt,
      name: normalized,
      run: runRel,
      store,
      model: $("#template-gen-model")?.value,
      lang: $("#federlicht-lang")?.value || "ko",
      site_output: reportHubBase(),
    };
    const targetPath = templateEditorTargetPath(normalized);
    await startJob("/api/templates/generate", payload, {
      kind: "template",
      spotLabel: "Template Generate",
      spotPath: targetPath,
      onSuccess: async () => {
        await loadTemplates();
        const baseSelect = $("#template-editor-base");
        if (baseSelect) baseSelect.value = targetPath;
        await loadTemplateEditorBase();
        appendTemplateGenLog("\nDone.\n");
        if (button) {
          button.disabled = false;
          button.textContent = "Generate Base";
        }
      },
      onDone: () => {
        if (button) {
          button.disabled = false;
          button.textContent = "Generate Base";
        }
      },
    });
  });
}

function setAgentStatus(message) {
  const el = $("#agent-status");
  if (el) {
    el.textContent = message || "";
  }
}

function saveActiveAgentProfileSelection(id, source) {
  const payload = {
    id: String(id || "").trim(),
    source: String(source || "").trim() || "builtin",
  };
  localStorage.setItem(AGENT_PROFILE_STORAGE_KEY, JSON.stringify(payload));
}

function loadActiveAgentProfileSelection() {
  const raw = localStorage.getItem(AGENT_PROFILE_STORAGE_KEY);
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw);
    const id = String(parsed?.id || "").trim();
    const source = String(parsed?.source || "builtin").trim() || "builtin";
    if (!id) return null;
    return { id, source };
  } catch (err) {
    return null;
  }
}

function normalizeApplyTo(value) {
  const values = Array.isArray(value) ? value : [value];
  const tokens = [];
  values.forEach((entry) => {
    String(entry || "")
      .split(/[,\n]/)
      .map((v) => v.trim())
      .filter(Boolean)
      .forEach((token) => tokens.push(token));
  });
  const aliasMap = {
    plan: "planner",
    plans: "planner",
    align: "alignment",
    aligned: "alignment",
    aligner: "alignment",
  };
  const normalizedTokens = tokens.map((token) => {
    const lowered = String(token || "").trim().toLowerCase();
    if (!lowered) return "";
    return aliasMap[lowered] || lowered;
  }).filter(Boolean);
  const repaired = [];
  for (let idx = 0; idx < normalizedTokens.length; idx += 1) {
    const token = normalizedTokens[idx];
    const pair = normalizedTokens.slice(idx, idx + 2);
    const triplet = normalizedTokens.slice(idx, idx + 3);
    if (pair.length === 2 && pair[0] === "pla" && pair[1] === "er") {
      repaired.push("planner");
      idx += 1;
      continue;
    }
    if (triplet.length === 3 && triplet[0] === "alig" && triplet[1] === "me" && triplet[2] === "t") {
      repaired.push("alignment");
      idx += 2;
      continue;
    }
    repaired.push(token);
  }
  const deduped = [];
  const seen = new Set();
  repaired.forEach((token) => {
    const normalized = String(token).trim();
    if (!normalized) return;
    if (seen.has(normalized)) return;
    seen.add(normalized);
    deduped.push(normalized);
  });
  let cleaned = deduped;
  if (seen.has("planner")) {
    cleaned = cleaned.filter((token) => token !== "pla" && token !== "er");
  }
  if (seen.has("alignment")) {
    cleaned = cleaned.filter((token) => token !== "alig" && token !== "me" && token !== "t");
  }
  return cleaned;
}

function renderAgentApplyTargetChecks() {
  const host = $("#agent-apply-to-checks");
  if (!host) return;
  if (host.childElementCount > 0) return;
  host.innerHTML = AGENT_APPLY_TARGETS.map((item) => {
    const id = escapeHtml(item.id);
    const label = escapeHtml(item.label);
    const hint = escapeHtml(item.hint || "");
    return `
      <label class="agent-apply-chip" title="${hint}">
        <input type="checkbox" value="${id}" data-apply-target="${id}" />
        <span>${label}</span>
      </label>
    `;
  }).join("");
  host.querySelectorAll("[data-apply-target]").forEach((input) => {
    input.addEventListener("change", () => {
      const label = input.closest(".agent-apply-chip");
      if (label) {
        label.classList.toggle("is-on", input.checked);
      }
    });
  });
}

function setAgentApplySelection(values) {
  renderAgentApplyTargetChecks();
  const tokens = normalizeApplyTo(values);
  const known = new Set(AGENT_APPLY_TARGETS.map((item) => item.id));
  const host = $("#agent-apply-to-checks");
  if (host) {
    host.querySelectorAll("[data-apply-target]").forEach((input) => {
      const token = input.getAttribute("data-apply-target") || "";
      const checked = tokens.includes(token);
      input.checked = checked;
      const label = input.closest(".agent-apply-chip");
      if (label) label.classList.toggle("is-on", checked);
    });
  }
  const custom = tokens.filter((token) => !known.has(token));
  const customInput = $("#agent-apply-to-custom");
  if (customInput) customInput.value = custom.join(", ");
}

function readAgentApplySelection() {
  renderAgentApplyTargetChecks();
  const selected = [];
  const host = $("#agent-apply-to-checks");
  if (host) {
    host.querySelectorAll("[data-apply-target]").forEach((input) => {
      if (input.checked) {
        const token = input.getAttribute("data-apply-target");
        if (token) selected.push(token);
      }
    });
  }
  const customTokens = normalizeApplyTo($("#agent-apply-to-custom")?.value || "");
  return normalizeApplyTo([...selected, ...customTokens]);
}

function isSixDigitProfileId(value) {
  return /^\d{6}$/.test(String(value || "").trim());
}

function generateSiteProfileId() {
  const used = new Set((state.agentProfiles.list || []).map((item) => String(item.id || "").trim()));
  for (let i = 0; i < 512; i += 1) {
    const candidate = String(Math.floor(Math.random() * 1000000)).padStart(6, "0");
    if (!used.has(candidate)) {
      return candidate;
    }
  }
  return String(Date.now() % 1000000).padStart(6, "0");
}

function renderAgentList() {
  const listEl = $("#agent-list");
  if (!listEl) return;
  const items = state.agentProfiles.list || [];
  listEl.innerHTML = items
    .map((profile) => {
      const id = escapeHtml(profile.id);
      const name = escapeHtml(profile.name || profile.id);
      const tagline = escapeHtml(profile.tagline || "");
      const applyItems = Array.isArray(profile.apply_to) ? profile.apply_to : [];
      const applyTo = escapeHtml(applyItems.join(", "));
      const applyPreview = applyItems
        .slice(0, 5)
        .map((token) => `<span class="agent-apply-pill">${escapeHtml(token)}</span>`)
        .join("");
      const applyOverflow = applyItems.length > 5 ? `<span class="agent-apply-pill">+${applyItems.length - 5}</span>` : "";
      const sourceLabel = profile.source === "site" ? "SITE" : "BUILTIN";
      const org = escapeHtml(profile.organization || "");
      const active =
        state.agentProfiles.activeId === profile.id &&
        state.agentProfiles.activeSource === profile.source;
      return `
        <button class="agent-item ${active ? "active" : ""}" data-id="${id}" data-source="${profile.source}">
          <div class="agent-title-row">
            <strong>${name}</strong>
            <span class="agent-source">${escapeHtml(sourceLabel)}</span>
          </div>
          <div>
            <div class="agent-meta-line">${id}${org ? ` · ${org}` : ""}</div>
            ${tagline ? `<div class="agent-meta-line">${tagline}</div>` : ""}
            ${applyTo ? `<div class="agent-meta">${applyTo}</div>` : ""}
            <div class="agent-apply-row">${applyPreview}${applyOverflow}</div>
          </div>
        </button>
      `;
    })
    .join("");
  [...listEl.querySelectorAll(".agent-item")].forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.dataset.id;
      const source = btn.dataset.source;
      if (id && source) {
        openAgentProfile(id, source);
      }
    });
  });
}

function resolveActiveAgentProfileItem() {
  const items = state.agentProfiles.list || [];
  if (!items.length) return null;
  const exact = items.find(
    (profile) =>
      profile.id === state.agentProfiles.activeId
      && profile.source === state.agentProfiles.activeSource,
  );
  if (exact) return exact;
  const byId = items.find((profile) => profile.id === state.agentProfiles.activeId);
  if (byId) return byId;
  return items[0] || null;
}

function renderActiveProfileSummary() {
  const el = $("#federlicht-profile-summary");
  if (!el) return;
  const active = resolveActiveAgentProfileItem();
  if (!active) {
    el.textContent = "활성 프로필 없음 (기본값 사용)";
    refreshLiveAskAgentLabel();
    renderWorkflowStudioPanel();
    return;
  }
  const source = active.source === "site" ? "site" : "builtin";
  const name = active.name || active.id;
  const applyTo = Array.isArray(active.apply_to) ? active.apply_to.join(", ") : "";
  const applyLabel = applyTo ? ` · apply: ${applyTo}` : "";
  el.textContent = `${name} (${active.id}/${source})${applyLabel}`;
  refreshLiveAskAgentLabel();
  renderWorkflowStudioPanel();
}

function rootAuthBadgeText() {
  const auth = state.agentProfiles?.rootAuth || {};
  const sessionRoot = Boolean(auth.session_root) || sessionHasRootRole();
  if (!auth.enabled && sessionRoot) return "Root auth: session-root";
  if (!auth.enabled) return "Root auth: disabled";
  if (!auth.unlocked && sessionRoot) return "Root auth: session-root";
  if (!auth.unlocked) return "Root auth: locked";
  const until = String(auth.expires_at || "").trim();
  if (sessionRoot) {
    return until
      ? `Root auth: unlocked(session-root) · expires ${formatDate(until)}`
      : "Root auth: unlocked(session-root)";
  }
  return until ? `Root auth: unlocked · expires ${formatDate(until)}` : "Root auth: unlocked";
}

function sessionAuthBadgeText() {
  const auth = state.agentProfiles?.sessionAuth || {};
  if (!auth.enabled) return "Session auth: disabled";
  if (!auth.authenticated) return "Session auth: signed out";
  const display = String(auth.display_name || auth.username || "user").trim();
  const role = String(auth.role || "user").trim();
  const until = String(auth.expires_at || "").trim();
  const suffix = until ? ` · expires ${formatDate(until)}` : "";
  return `Session auth: ${display} (${role})${suffix}`;
}

function sessionHasRootRole() {
  const role = String(state.agentProfiles?.sessionAuth?.role || "").trim().toLowerCase();
  return role === "root" || role === "admin" || role === "owner" || role === "superuser";
}

function refreshAgentRootAuthButton() {
  const button = $("#agent-root-auth");
  if (!button) return;
  const auth = state.agentProfiles?.rootAuth || {};
  if (sessionHasRootRole()) {
    button.textContent = "Session Root";
    button.disabled = true;
    button.title = "현재 세션 계정이 root 권한을 보유해 built-in profile 편집이 가능합니다.";
    return;
  }
  if (!auth.enabled) {
    button.textContent = "Root Auth Off";
    button.disabled = true;
    button.title = "FEDERNETT_ROOT_PASSWORD가 설정되지 않았습니다.";
    return;
  }
  button.disabled = false;
  button.textContent = auth.unlocked ? "Root Lock" : "Root Unlock";
  button.title = auth.unlocked
    ? "현재 root unlock 상태입니다. 클릭하면 잠금합니다."
    : "built-in 프로파일 편집 권한을 위해 root unlock 합니다.";
}

function refreshAgentSessionAuthButton() {
  const button = $("#agent-session-auth");
  const statusEl = $("#agent-session-status");
  const auth = state.agentProfiles?.sessionAuth || {};
  if (button) {
    if (!auth.enabled) {
      button.textContent = "Sign In Off";
      button.disabled = true;
      button.title = "FEDERNETT_AUTH_ACCOUNTS_JSON가 설정되지 않았습니다.";
    } else {
      button.disabled = false;
      button.textContent = auth.authenticated ? "Sign Out" : "Sign In";
      button.title = auth.authenticated
        ? "현재 세션에서 로그아웃합니다."
        : "Federnett session 로그인";
    }
  }
  if (statusEl) {
    statusEl.textContent = sessionAuthBadgeText();
  }
}

function builtinEditableByRoot(source) {
  return String(source || "") === "builtin"
    && (
      Boolean(state.agentProfiles?.rootAuth?.unlocked)
      || sessionHasRootRole()
    );
}

function setAgentEditorReadOnly(readOnly, source = "") {
  const effectiveReadOnly = Boolean(readOnly) && !builtinEditableByRoot(source);
  const saveBtn = $("#agent-save");
  const deleteBtn = $("#agent-delete");
  const hint = $("#agent-readonly-hint");
  if (saveBtn) saveBtn.disabled = effectiveReadOnly;
  if (deleteBtn) deleteBtn.disabled = effectiveReadOnly;
  if (hint) {
    hint.classList.toggle("is-readonly", effectiveReadOnly);
    if (String(source || "") === "builtin") {
      if (effectiveReadOnly) {
        hint.textContent = `Built-in profile is read-only. ${rootAuthBadgeText()} · Clone 후 site profile로 저장하세요.`;
      } else {
        hint.textContent = `Built-in profile editable (${rootAuthBadgeText()}). 저장 시 builtin 파일이 직접 갱신됩니다.`;
      }
    } else {
      hint.textContent = rootAuthBadgeText();
    }
  }
  refreshAgentRootAuthButton();
}

function fillAgentForm(profile, memoryText, source, readOnly) {
  const memoryHook = profile?.memory_hook || {};
  const configOverrides =
    profile?.config_overrides && typeof profile.config_overrides === "object"
      ? profile.config_overrides
      : {};
  const agentOverrides =
    profile?.agent_overrides && typeof profile.agent_overrides === "object"
      ? profile.agent_overrides
      : {};
  $("#agent-id").value = profile?.id || "";
  $("#agent-name").value = profile?.name || "";
  $("#agent-author-name").value = profile?.author_name || profile?.name || "";
  $("#agent-organization").value = profile?.organization || "";
  $("#agent-tagline").value = profile?.tagline || "";
  setAgentApplySelection(profile?.apply_to || []);
  $("#agent-system-prompt").value = profile?.system_prompt || "";
  $("#agent-config-overrides").value = Object.keys(configOverrides).length
    ? JSON.stringify(configOverrides, null, 2)
    : "";
  $("#agent-agent-overrides").value = Object.keys(agentOverrides).length
    ? JSON.stringify(agentOverrides, null, 2)
    : "";
  $("#agent-memory-desc").value = memoryHook?.description || "";
  $("#agent-memory-path").value = memoryHook?.path || "";
  $("#agent-memory-text").value = memoryText || "";
  const storeCheck = $("#agent-store-site");
  if (storeCheck) {
    storeCheck.checked = true;
    storeCheck.disabled = true;
  }
  const meta = $("#agent-editor-meta");
  if (meta) {
    meta.textContent = readOnly
      ? `Read-only built-in profile · ${source}`
      : `Editable profile · ${source}`;
  }
  setAgentEditorReadOnly(readOnly, source);
}

function parseOptionalJsonObject(rawText, fieldLabel) {
  const text = String(rawText || "").trim();
  if (!text) return null;
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch (err) {
    throw new Error(`${fieldLabel} must be valid JSON.`);
  }
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
    throw new Error(`${fieldLabel} must be a JSON object.`);
  }
  return parsed;
}

function applyRootAuthPayload(payload) {
  const token = activeRootAuthToken();
  const enabled = Boolean(payload?.enabled);
  const unlocked = Boolean(payload?.unlocked);
  const sessionRoot = Boolean(payload?.session_root);
  const expiresAt = String(payload?.expires_at || "").trim();
  state.agentProfiles.rootAuth = {
    enabled,
    unlocked,
    session_root: sessionRoot,
    token: unlocked ? token : "",
    expires_at: expiresAt,
  };
  if (!unlocked) {
    persistRootAuthToken("");
  }
  refreshAgentRootAuthButton();
}

function applySessionAuthPayload(payload) {
  const token = activeSessionAuthToken();
  const enabled = Boolean(payload?.enabled);
  const authenticated = Boolean(payload?.authenticated);
  const nextToken = authenticated ? token : "";
  state.agentProfiles.sessionAuth = {
    enabled,
    authenticated,
    username: String(payload?.username || "").trim(),
    display_name: String(payload?.display_name || "").trim(),
    role: String(payload?.role || "").trim(),
    token: nextToken,
    expires_at: String(payload?.expires_at || "").trim(),
  };
  if (!authenticated) {
    persistSessionAuthToken("");
  }
  refreshAgentSessionAuthButton();
  refreshAgentRootAuthButton();
  const activeSource = String(state.agentProfiles?.activeSource || "").trim();
  if (activeSource) {
    setAgentEditorReadOnly(Boolean(state.agentProfiles?.readOnly), activeSource);
  }
}

async function refreshRootAuthStatus() {
  try {
    const payload = await fetchJSON("/api/auth/root/status");
    applyRootAuthPayload(payload || {});
  } catch (err) {
    applyRootAuthPayload({ enabled: false, unlocked: false });
  }
}

async function refreshSessionAuthStatus() {
  try {
    const payload = await fetchJSON("/api/auth/session/status");
    applySessionAuthPayload(payload || {});
  } catch (err) {
    applySessionAuthPayload({ enabled: false, authenticated: false });
  }
}

async function toggleRootAuth() {
  const auth = state.agentProfiles?.rootAuth || {};
  if (!auth.enabled) {
    setAgentStatus("Root auth is disabled. FEDERNETT_ROOT_PASSWORD를 설정하세요.");
    return;
  }
  if (auth.unlocked) {
    await fetchJSON("/api/auth/root/lock", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    applyRootAuthPayload({ enabled: true, unlocked: false, expires_at: "" });
    setAgentStatus("Root auth locked.");
    await loadAgentProfiles(state.agentProfiles.activeId, state.agentProfiles.activeSource || "builtin");
    return;
  }
  const password = window.prompt("Root password");
  if (!password) {
    setAgentStatus("Root unlock cancelled.");
    return;
  }
  try {
    const payload = await fetchJSON("/api/auth/root/unlock", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    });
    const token = String(payload?.token || "").trim();
    if (token) {
      persistRootAuthToken(token);
    }
    applyRootAuthPayload({ ...payload, unlocked: true });
    setAgentStatus("Root auth unlocked.");
    await loadAgentProfiles(state.agentProfiles.activeId, state.agentProfiles.activeSource || "builtin");
  } catch (err) {
    setAgentStatus(`Root unlock failed: ${err}`);
    await refreshRootAuthStatus();
  }
}

async function toggleSessionAuth() {
  const auth = state.agentProfiles?.sessionAuth || {};
  if (!auth.enabled) {
    setAgentStatus("Session auth is disabled. FEDERNETT_AUTH_ACCOUNTS_JSON를 설정하세요.");
    return;
  }
  if (auth.authenticated) {
    await fetchJSON("/api/auth/session/logout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    applySessionAuthPayload({
      enabled: true,
      authenticated: false,
      username: "",
      display_name: "",
      role: "",
      expires_at: "",
    });
    setAgentStatus("Session signed out.");
    return;
  }
  const username = String(window.prompt("Username") || "").trim();
  if (!username) {
    setAgentStatus("Session sign-in cancelled.");
    return;
  }
  const password = String(window.prompt("Password") || "");
  if (!password) {
    setAgentStatus("Session sign-in cancelled.");
    return;
  }
  try {
    const payload = await fetchJSON("/api/auth/session/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const token = String(payload?.token || "").trim();
    if (token) {
      persistSessionAuthToken(token);
    }
    applySessionAuthPayload({ ...payload, authenticated: true });
    setAgentStatus("Session signed in.");
  } catch (err) {
    setAgentStatus(`Session sign-in failed: ${err}`);
    await refreshSessionAuthStatus();
  }
}

async function openAgentProfile(id, source) {
  try {
    const detail = await fetchJSON(`/api/agent-profiles/${encodeURIComponent(id)}?source=${encodeURIComponent(source)}`);
    if (detail?.root_auth && typeof detail.root_auth === "object") {
      applyRootAuthPayload(detail.root_auth);
    }
    state.agentProfiles.activeId = id;
    state.agentProfiles.activeSource = source;
    state.agentProfiles.activeProfile = detail.profile;
    state.agentProfiles.memoryText = detail.memory_text || "";
    state.agentProfiles.readOnly = Boolean(detail.read_only);
    saveActiveAgentProfileSelection(id, source);
    fillAgentForm(detail.profile, detail.memory_text, source, detail.read_only);
    renderAgentList();
    renderActiveProfileSummary();
    setAgentStatus("Profile loaded.");
    maybeReloadAskHistory();
  } catch (err) {
    setAgentStatus(`Failed to load profile: ${err}`);
  }
}

function newAgentProfile() {
  const generatedId = generateSiteProfileId();
  state.agentProfiles.activeId = "";
  state.agentProfiles.activeSource = "site";
  state.agentProfiles.activeProfile = {
    id: generatedId,
    name: "",
    author_name: "",
    organization: "",
    tagline: "",
    apply_to: [],
    system_prompt: "",
    config_overrides: {},
    agent_overrides: {},
    memory_hook: {},
  };
  state.agentProfiles.memoryText = "";
  state.agentProfiles.readOnly = false;
  fillAgentForm(state.agentProfiles.activeProfile, "", "site", false);
  renderAgentList();
  renderActiveProfileSummary();
  setAgentStatus(`New profile (site) ready. Assigned ID ${generatedId}.`);
}

function readAgentForm() {
  let id = $("#agent-id").value.trim();
  if (!isSixDigitProfileId(id)) {
    id = generateSiteProfileId();
  }
  const name = $("#agent-name").value.trim();
  const authorName = $("#agent-author-name").value.trim();
  const organization = $("#agent-organization").value.trim();
  const tagline = $("#agent-tagline").value.trim();
  const applyTo = readAgentApplySelection();
  const systemPrompt = $("#agent-system-prompt").value;
  const configOverrides = parseOptionalJsonObject(
    $("#agent-config-overrides").value,
    "Config overrides",
  );
  const agentOverrides = parseOptionalJsonObject(
    $("#agent-agent-overrides").value,
    "Agent overrides",
  );
  const memoryDesc = $("#agent-memory-desc").value.trim();
  const memoryPath = $("#agent-memory-path").value.trim();
  const memoryText = $("#agent-memory-text").value;
  const profile = {
    id,
    name,
    author_name: authorName || name,
    organization: organization || "",
    tagline,
    apply_to: applyTo,
    system_prompt: systemPrompt,
  };
  if (configOverrides) {
    profile.config_overrides = configOverrides;
  }
  if (agentOverrides) {
    profile.agent_overrides = agentOverrides;
  }
  if (memoryDesc || memoryPath) {
    profile.memory_hook = {
      description: memoryDesc,
      path: memoryPath || undefined,
    };
  }
  return { profile, memoryText };
}

async function saveAgentProfile() {
  try {
    const activeSource = String(state.agentProfiles.activeSource || "site");
    const builtinEdit = builtinEditableByRoot(activeSource);
    const isReadOnly = Boolean(state.agentProfiles.readOnly) && !builtinEdit;
    if (isReadOnly) {
      setAgentStatus("Built-in profiles are read-only. Clone and save with a new ID.");
      return;
    }
    const { profile, memoryText } = readAgentForm();
    $("#agent-id").value = profile.id;
    const store = activeSource === "builtin" && builtinEdit ? "builtin" : "site";
    setAgentStatus("Saving profile...");
    await fetchJSON("/api/agent-profiles/save", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        profile,
        memory_text: memoryText,
        store,
      }),
    });
    await loadAgentProfiles(profile.id, store);
    setAgentStatus(store === "builtin" ? "Built-in profile updated." : "Profile saved.");
  } catch (err) {
    setAgentStatus(`Save failed: ${err}`);
  }
}

async function deleteAgentProfile() {
  try {
    if (state.agentProfiles.readOnly) {
      setAgentStatus("Built-in profiles cannot be deleted.");
      return;
    }
    const id = $("#agent-id").value.trim();
    if (!id) {
      setAgentStatus("Profile ID is required.");
      return;
    }
    setAgentStatus("Deleting profile...");
    await fetchJSON("/api/agent-profiles/delete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id }),
    });
    await loadAgentProfiles();
    newAgentProfile();
    setAgentStatus("Profile deleted.");
  } catch (err) {
    setAgentStatus(`Delete failed: ${err}`);
  }
}

function cloneAgentProfile() {
  const { profile, memoryText } = readAgentForm();
  profile.id = generateSiteProfileId();
  $("#agent-id").value = profile.id;
  $("#agent-memory-text").value = memoryText || "";
  state.agentProfiles.readOnly = false;
  const meta = $("#agent-editor-meta");
  if (meta) meta.textContent = "Editable profile · site";
  setAgentEditorReadOnly(false);
  renderActiveProfileSummary();
  setAgentStatus(`Cloned. New profile ID ${profile.id}.`);
}

async function loadAgentProfiles(selectId, selectSource) {
  try {
    const payload = await fetchJSON("/api/agent-profiles");
    state.agentProfiles.list = payload.profiles || [];
    if (payload?.root_auth && typeof payload.root_auth === "object") {
      applyRootAuthPayload(payload.root_auth);
    }
    renderAgentList();
    renderActiveProfileSummary();
    const persisted = loadActiveAgentProfileSelection();
    if (selectId && selectSource) {
      await openAgentProfile(selectId, selectSource);
      return;
    }
    if (!state.agentProfiles.activeId && persisted) {
      const matched = state.agentProfiles.list.find(
        (item) => item.id === persisted.id && item.source === persisted.source,
      );
      if (matched) {
        await openAgentProfile(matched.id, matched.source);
        return;
      }
    }
    if (!state.agentProfiles.activeId && state.agentProfiles.list.length) {
      const first = state.agentProfiles.list[0];
      await openAgentProfile(first.id, first.source);
      return;
    }
    renderActiveProfileSummary();
  } catch (err) {
    setAgentStatus(`Failed to load profiles: ${err}`);
  }
}

function handleAgentPanelToggle() {
  const panel = $("#agent-panel");
  const button = $("#agent-panel-toggle");
  if (!panel || !button) return;
  const stored = localStorage.getItem("federnett-agent-panel-collapsed");
  if (stored === "true") {
    panel.classList.add("collapsed");
    button.textContent = "Show panel";
  }
  button.addEventListener("click", () => {
    const collapsed = panel.classList.toggle("collapsed");
    button.textContent = collapsed ? "Show panel" : "Hide panel";
    localStorage.setItem("federnett-agent-panel-collapsed", collapsed ? "true" : "false");
  });
}

function handleAgentProfiles() {
  renderAgentApplyTargetChecks();
  $("#agent-new")?.addEventListener("click", () => newAgentProfile());
  $("#agent-save")?.addEventListener("click", () => saveAgentProfile());
  $("#agent-delete")?.addEventListener("click", () => deleteAgentProfile());
  $("#agent-clone")?.addEventListener("click", () => cloneAgentProfile());
  $("#agent-root-auth")?.addEventListener("click", () => {
    toggleRootAuth().catch((err) => setAgentStatus(`Root auth error: ${err}`));
  });
  $("#agent-session-auth")?.addEventListener("click", () => {
    toggleSessionAuth().catch((err) => setAgentStatus(`Session auth error: ${err}`));
  });
  refreshAgentSessionAuthButton();
}

function handleControlPanelToggle() {
  const panel = $("#control-panel");
  const layout = $(".layout");
  const toggle = $("#control-panel-toggle");
  const collapsedActions = panel?.querySelector(".control-collapsed-actions");
  const openFeather = $("#control-collapsed-open-feather");
  const openFederlicht = $("#control-collapsed-open-federlicht");
  const openRunStudio = $("#control-collapsed-open-runstudio");
  if (!panel || !layout || !toggle) return;
  const apply = (collapsed) => {
    panel.classList.toggle("is-collapsed", collapsed);
    layout.classList.toggle("control-collapsed", collapsed);
    toggle.textContent = collapsed ? "사이드바 열기" : "사이드바 닫기";
    toggle.title = collapsed ? "사이드바 열기" : "사이드바 닫기";
    toggle.setAttribute("aria-label", collapsed ? "사이드바 열기" : "사이드바 닫기");
    collapsedActions?.setAttribute("aria-hidden", collapsed ? "false" : "true");
  };
  const stored = localStorage.getItem(CONTROL_PANEL_COLLAPSE_KEY);
  apply(stored === "true");
  toggle.addEventListener("click", () => {
    const next = !panel.classList.contains("is-collapsed");
    apply(next);
    localStorage.setItem(CONTROL_PANEL_COLLAPSE_KEY, next ? "true" : "false");
  });
  const openPanel = () => {
    apply(false);
    localStorage.setItem(CONTROL_PANEL_COLLAPSE_KEY, "false");
  };
  openFeather?.addEventListener("click", () => {
    openPanel();
    document.querySelector('[data-tab="feather"]')?.dispatchEvent(new MouseEvent("click", { bubbles: true }));
    focusPanel("#tab-feather");
  });
  openFederlicht?.addEventListener("click", () => {
    openPanel();
    document.querySelector('[data-tab="federlicht"]')?.dispatchEvent(new MouseEvent("click", { bubbles: true }));
    focusPanel("#tab-federlicht");
  });
  openRunStudio?.addEventListener("click", () => {
    openPanel();
    document.querySelector('.tab[data-tab="runstudio"]')?.dispatchEvent(new MouseEvent("click", { bubbles: true }));
  });
}

function handleLayoutSplitter() {
  const splitter = $("#layout-splitter");
  const layout = $(".layout");
  if (!splitter || !layout) return;
  const rootStyle = document.documentElement.style;
  const minWidth = 460;
  const saved = localStorage.getItem(CONTROL_PANEL_WIDTH_KEY);
  if (saved) {
    const parsed = Number.parseFloat(String(saved).replace(/[^\d.]+/g, ""));
    if (Number.isFinite(parsed)) {
      rootStyle.setProperty("--control-width-open", `${Math.max(minWidth, Math.round(parsed))}px`);
    } else {
      rootStyle.setProperty("--control-width-open", saved);
    }
  }
  let dragging = false;
  const onMove = (event) => {
    if (!dragging) return;
    if (layout.classList.contains("control-collapsed")) return;
    const rect = layout.getBoundingClientRect();
    const maxWidth = Math.max(minWidth, rect.width - 560);
    const next = Math.min(Math.max(event.clientX - rect.left, minWidth), maxWidth);
    rootStyle.setProperty("--control-width-open", `${Math.round(next)}px`);
  };
  const stopDrag = () => {
    if (!dragging) return;
    dragging = false;
    layout.classList.remove("resizing");
    localStorage.setItem(
      CONTROL_PANEL_WIDTH_KEY,
      rootStyle.getPropertyValue("--control-width-open"),
    );
    window.removeEventListener("pointermove", onMove);
    window.removeEventListener("pointerup", stopDrag);
  };
  splitter.addEventListener("pointerdown", (event) => {
    dragging = true;
    layout.classList.add("resizing");
    splitter.setPointerCapture(event.pointerId);
    window.addEventListener("pointermove", onMove);
    window.addEventListener("pointerup", stopDrag);
  });
}

function handleTelemetrySplitter() {
  const splitter = $("#telemetry-splitter");
  const wrap = $("#logs-wrap");
  if (!splitter || !wrap) return;
  const rootStyle = document.documentElement.style;
  const saved = localStorage.getItem("federnett-log-height");
  if (saved) {
    const parsed = Number.parseFloat(saved);
    if (Number.isFinite(parsed)) {
      const viewportLimit = Math.max(260, window.innerHeight - 220);
      const clamped = Math.min(Math.max(220, parsed), viewportLimit);
      rootStyle.setProperty("--telemetry-log-height", `${Math.round(clamped)}px`);
    }
  }
  let dragging = false;
  const onMove = (event) => {
    if (!dragging) return;
    const rect = wrap.getBoundingClientRect();
    const minHeight = 220;
    const viewportLimit = Math.max(minHeight, window.innerHeight - rect.top - 110);
    const maxHeight = Math.max(minHeight, Math.min(rect.height - 120, viewportLimit));
    const next = Math.min(Math.max(event.clientY - rect.top, minHeight), maxHeight);
    rootStyle.setProperty("--telemetry-log-height", `${Math.round(next)}px`);
  };
  const stopDrag = () => {
    if (!dragging) return;
    dragging = false;
    localStorage.setItem(
      "federnett-log-height",
      rootStyle.getPropertyValue("--telemetry-log-height"),
    );
    window.removeEventListener("pointermove", onMove);
    window.removeEventListener("pointerup", stopDrag);
  };
  splitter.addEventListener("pointerdown", (event) => {
    dragging = true;
    splitter.setPointerCapture(event.pointerId);
    window.addEventListener("pointermove", onMove);
    window.addEventListener("pointerup", stopDrag);
  });
  splitter.addEventListener("dblclick", () => {
    rootStyle.removeProperty("--telemetry-log-height");
    localStorage.removeItem("federnett-log-height");
  });
}

function bindForms() {
  $("#feather-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      appendLog("[policy] sidebar Run Feather is direct execution. Plan/Act affects FederHav suggested actions only.\n");
      const runHint = normalizePathString($("#feather-output")?.value || selectedRunRel() || "");
      const inputReady = await ensureFeatherActionHasMeaningfulInput(runHint, {
        forceAutoDraft: false,
      });
      if (!inputReady) {
        appendLog("[feather] 실행이 보류되었습니다. instruction 품질 확인 후 다시 실행하세요.\n");
        return;
      }
      const payload = buildFeatherPayload();
      const runRel = normalizePathString(payload.output || "");
      if (runRel) {
        payload.output = runRel;
      }
      if (payload.input) {
        const normalized = normalizeFeatherInstructionPath(payload.input);
        payload.input = normalized;
        const content = $("#feather-query")?.value || "";
        if (content.trim()) {
          await saveInstructionContent(normalized, content);
          setFeatherInstructionSnapshot(normalized, content);
        }
      }
      await startJob("/api/feather/start", payload, {
        kind: "feather",
        onSuccess: async () => {
          await loadRuns().catch(() => {});
          if (runRel && $("#run-select")) {
            $("#run-select").value = runRel;
            if ($("#prompt-run-select")) $("#prompt-run-select").value = runRel;
            if ($("#instruction-run-select")) $("#instruction-run-select").value = runRel;
            refreshRunDependentFields();
            await updateRunStudio(runRel).catch(() => {});
          }
        },
      });
    } catch (err) {
      appendLog(`[feather] ${err}\n`);
    }
  });

  $("#federlicht-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      appendLog("[policy] sidebar Run Federlicht is direct execution. Plan/Act affects FederHav suggested actions only.\n");
      const runtime = syncFederlichtModelControls({ announce: true });
      await syncWorkflowStageOverridesToRun().catch((err) => {
        appendLog(`[workflow] stage override sync failed: ${err}\n`);
      });
      const payload = buildFederlichtPayload();
      appendLog(
        `[federlicht] runtime backend=${runtime.backend} model=${runtime.model || "$OPENAI_MODEL"} check=${runtime.checkModel || runtime.model || "-"} reasoning=${runtime.reasoningEffort || "off"}\n`,
      );
      await applyFederlichtOutputSuggestionToPayload(payload, { syncInput: true });
      const runRel = payload.run;
      await startJob("/api/federlicht/start", payload, {
        kind: "federlicht",
        onSuccess: async () => {
          await loadRuns().catch(() => {});
          if (runRel && $("#run-select")) {
            $("#run-select").value = runRel;
            if ($("#instruction-run-select")) $("#instruction-run-select").value = runRel;
            refreshRunDependentFields();
            await updateRunStudio(runRel).catch(() => {});
          }
        },
      });
    } catch (err) {
      appendLog(`[federlicht] ${err}\n`);
    }
  });

  $("#prompt-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    setPromptGenerateEnabled(false);
    try {
      const payload = buildPromptPayload();
      const outputPath = payload.output;
      await startJob("/api/federlicht/generate_prompt", payload, {
        kind: "prompt",
        spotLabel: "Prompt Generate",
        spotPath: outputPath,
        onSuccess: async () => {
          if (outputPath) {
            await hydrateGeneratedPromptInline(outputPath).catch((err) => {
              if (!isMissingFileError(err)) {
                appendLog(`[prompt] failed to load: ${err}\n`);
              }
            });
            appendLog(`[prompt] ready: ${outputPath}\n`);
          }
        },
        onDone: () => {
          setPromptGenerateEnabled(true);
        },
      });
    } catch (err) {
      appendLog(`[prompt] ${err}\n`);
      setPromptGenerateEnabled(true);
    }
  });
}

function handleTemplatesPanelToggle() {
  const panel = $("#templates-panel");
  const cardsButton = $("#templates-toggle");
  const panelButton = $("#templates-panel-toggle");
  if (!panel || !cardsButton) return;
  panel.classList.remove("collapsed");
  const applyCardsState = (collapsed) => {
    panel.classList.toggle("cards-collapsed", collapsed);
    cardsButton.textContent = collapsed ? "Show cards" : "Hide cards";
  };
  const applyPanelState = (collapsed) => {
    panel.classList.toggle("panel-collapsed", collapsed);
    if (panelButton) {
      panelButton.textContent = collapsed ? "Show panel" : "Hide panel";
    }
  };
  const cardsStored =
    localStorage.getItem("federnett-templates-cards-collapsed")
    ?? localStorage.getItem("federnett-templates-collapsed");
  const panelStored = localStorage.getItem("federnett-templates-panel-collapsed");
  applyCardsState(cardsStored === "true");
  applyPanelState(panelStored === "true");
  cardsButton.addEventListener("click", () => {
    const collapsed = !panel.classList.contains("cards-collapsed");
    applyCardsState(collapsed);
    localStorage.setItem("federnett-templates-cards-collapsed", collapsed ? "true" : "false");
  });
  panelButton?.addEventListener("click", () => {
    const collapsed = !panel.classList.contains("panel-collapsed");
    applyPanelState(collapsed);
    localStorage.setItem("federnett-templates-panel-collapsed", collapsed ? "true" : "false");
  });
}

async function loadModelOptions() {
  const allList = $("#model-options");
  const openaiList = $("#openai-model-options");
  const codexList = $("#codex-model-options");
  if (!allList && !openaiList && !codexList) return;
  const codexOptions = codexModelPresetOptions();
  const openaiPresets = openaiModelPresetOptions();
  try {
    const models = await fetchJSON("/api/models");
    const openaiRemote = Array.isArray(models)
      ? models.filter((token) => !isCodexModelToken(token))
      : [];
    const openaiMerged = uniqueTokens([...openaiPresets, ...openaiRemote]);
    const codexMerged = uniqueTokens(codexOptions);
    const merged = uniqueTokens([...MODEL_PRESET_OPTIONS, ...openaiMerged, ...codexMerged]);
    state.modelCatalog = {
      all: merged,
      openai: openaiMerged,
      codex: codexMerged,
    };
    if (allList) allList.innerHTML = merged.map((m) => `<option value="${escapeHtml(m)}"></option>`).join("");
    if (openaiList) {
      openaiList.innerHTML = openaiMerged.map((m) => `<option value="${escapeHtml(m)}"></option>`).join("");
    }
    if (codexList) codexList.innerHTML = codexMerged.map((m) => `<option value="${escapeHtml(m)}"></option>`).join("");
  } catch (err) {
    const openaiMerged = uniqueTokens(openaiPresets);
    const codexMerged = uniqueTokens(codexOptions);
    const merged = uniqueTokens([...MODEL_PRESET_OPTIONS, ...openaiMerged, ...codexMerged]);
    state.modelCatalog = {
      all: merged,
      openai: openaiMerged,
      codex: codexMerged,
    };
    if (allList) {
      allList.innerHTML = merged.map((m) => `<option value="${escapeHtml(m)}"></option>`).join("");
    }
    if (openaiList) {
      openaiList.innerHTML = openaiMerged.map((m) => `<option value="${escapeHtml(m)}"></option>`).join("");
    }
    if (codexList) {
      codexList.innerHTML = codexMerged.map((m) => `<option value="${escapeHtml(m)}"></option>`).join("");
    }
    appendLog(`[models] ${err}\n`);
  }
  syncModelInputCatalogBindings();
}

async function bootstrap() {
  initTheme();
  applyFieldTooltips();
  bindGlobalOverlayEscape();
  initPopupDragBindings();
  bindWheelScrollAssist("#logs-wrap", "#live-ask-thread");
  bindWheelScrollAssist("#control-panel", "#control-panel");
  bindWheelScrollAssist("#workflow-studio-panel", ".workflow-studio-scroll");
  bindWheelScrollAssist("#workspace-panel", "#workspace-panel");
  bindWheelScrollAssist("#run-picker-modal", "#run-picker-list");
  loadWorkflowStageOverrides();
  handleAskPanel();
  handleWorkspacePanel();
  handleTabs();
  handleQuickRunButtons();
  handleFeatherRunName();
  handleFeatherAgenticControls();
  handlePipelineBackendControls();
  handleRunOutputTouch();
  handlePipelineInputs();
  handleRunChanges();
  handleRunOpen();
  handleInstructionEditor();
  handleFilePreviewControls();
  handleFeatherInstructionPicker();
  handleUploadDrop();
  handleFederlichtPromptPicker();
  handleFederlichtPromptEditor();
  handlePromptExpandControl();
  handleRunPicker();
  handleModelPolicyModal();
  handleJobsModal();
  handleReloadRuns();
  handleLogControls();
  handleWorkflowHistoryControls();
  handleWorkflowStudioPanel();
  bindWorkflowDismissHandlers();
  handleTemplateSync();
  handleFreeFormatToggle();
  handleTemplateEditor();
  handleTemplateGenerator();
  handleTemplatesPanelToggle();
  handleAgentProfiles();
  handleAgentPanelToggle();
  handleControlPanelToggle();
  bindTemplateModalClose();
  bindHelpModal();
  handleLayoutSplitter();
  handleTelemetrySplitter();
  bindForms();
  window.setInterval(() => {
    recoverIdleJobControls();
  }, 2200);
  setFederlichtRunEnabled(true);
  setFeatherRunEnabled(true);
  setPromptGenerateEnabled(true);
  renderJobs();
  resetWorkflowState();
  renderWorkflow();
  renderWorkflowRuntimeConfig();
  syncWorkflowQualityControls();
  renderActiveProfileSummary();

  try {
    await loadInfo();
    bindHeroCards();
    initPipelineFromInputs();
    const rootAuthSupported = Boolean(state.info?.root_auth && typeof state.info.root_auth === "object");
    const sessionAuthSupported = Boolean(state.info?.session_auth && typeof state.info.session_auth === "object");
    await Promise.all([
      loadTemplates(),
      loadRuns(),
      loadModelOptions(),
      rootAuthSupported ? refreshRootAuthStatus() : Promise.resolve(),
      sessionAuthSupported ? refreshSessionAuthStatus() : Promise.resolve(),
      loadAgentProfiles(),
      loadAskCapabilityRegistry({ silent: true }),
    ]);
    await syncWorkflowStageOverridesToRun().catch((err) => {
      appendLog(`[workflow] stage override sync failed: ${err}\n`);
    });
    syncFederlichtModelControls({ announce: false });
    loadGlobalModelPolicy();
    const hasStoredModelSignal = Boolean(
      state.modelPolicy.model
      || state.modelPolicy.checkModel
      || state.modelPolicy.visionModel,
    );
    const startupPolicy = hasStoredModelSignal ? state.modelPolicy : policySnapshotFromSource("federlicht");
    applyGlobalModelPolicy(startupPolicy, { persist: false, announce: false });
  } catch (err) {
    appendLog(`[init] ${err}\n`);
  }
}

bootstrap();
