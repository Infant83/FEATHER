# Report Workflow

## Stages
1. scout: ran
2. clarifier: skipped (no_questions)
3. template_adjust: skipped (depth=brief)
4. plan: ran
5. web: skipped (policy)
6. evidence: skipped (depth=brief)
7. plan_check: skipped (missing_evidence)
8. writer: ran
9. quality: disabled

## Timeline

1. [2026-02-25T00:58:49] template_adjust: skipped (depth=brief)
2. [2026-02-25T01:02:09] scout: ran
3. [2026-02-25T01:02:09] clarifier: skipped (no_questions)
4. [2026-02-25T01:02:30] plan: ran
5. [2026-02-25T01:02:30] web: skipped (policy)
6. [2026-02-25T01:02:30] plan_check: skipped (missing_evidence)
7. [2026-02-25T01:02:30] evidence: skipped (depth=brief)
8. [2026-02-25T01:06:27] writer: ran

## Artifacts
### scout
- Scout notes: ./report_notes/scout_notes.md

### plan
- Plan update: ./report_notes/report_plan.md

### evidence
- Evidence notes: ./report_notes/evidence_notes.md
- Source triage: ./report_notes/source_triage.md
- Source index: ./report_notes/source_index.jsonl
- Claim map: ./report_notes/claim_map.md
- Gap report: ./report_notes/gap_finder.md

## Diagram

```mermaid
flowchart LR
    scout["scout\nran"]
    clarifier["clarifier\nskipped"]
    template_adjust["template_adjust\nskipped"]
    plan["plan\nran"]
    web["web\nskipped"]
    evidence["evidence\nskipped"]
    plan_check["plan_check\nskipped"]
    writer["writer\nran"]
    quality["quality\ndisabled"]
    scout --> clarifier
    clarifier --> template_adjust
    template_adjust --> plan
    plan --> web
    web --> evidence
    evidence --> plan_check
    plan_check --> writer
    writer --> quality
```
## Outputs
- Report overview: ./report/run_overview_report_full_iter003_codex_classroom.md
- Report meta: ./report_notes/report_meta.json
- Report prompt copy: ./instruction/report_prompt_report_full_iter003_codex_classroom.txt
- Template summary: ./report_notes/report_template.txt
