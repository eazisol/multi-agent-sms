# MOD-230 — Requirement Gathering, Completeness, Clarifications, Brief

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

Analysts and PMs turning a qualified inquiry into a scored questionnaire and an approved brief. QA checks the 95% completeness threshold and the combined approve shortcut.

## 2. What this module is

Before a project SRS exists, the company asks structured questions. This desk publishes a questionnaire, stores answers, scores completeness, opens clarifications for gaps, and can create-and-approve a brief.

In daily language: fill the intake form, see what is missing, then lock a brief. **Create & approve brief** is a human clicking a combined button — not an agent auto-approving.

## 3. Status honesty

| Item | Status |
|---|---|
| `/requirements` desk | Implemented |
| Publish questionnaire, answer, score, clarifications, briefs list | Implemented |
| Create & approve brief (one button) | Implemented shortcut; target design wants separate human approval |
| Suggest questions (AI empty-state button) | Planned — no handler |
| Questionnaire designer / version history UI | Planned |
| Header identity | Stubbed |
| Human M1 acceptance (AC-901) | Blocked — not obtained in VERIFICATION.md |

Current-source limits testers must preserve:

- **Publish questionnaire** combines questionnaire creation, version creation, and publish.
- The desk renders the published version’s questions; its bootstrap path uses three mandatory defaults.
- **Save answers & score** writes nonblank answers sequentially before computing the score.
- **Create clarifications** assigns each reported gap to the current actor.
- **Create & approve brief** makes two API calls and can leave a draft if approval fails.
- Brief approval is human-only even though the current UI combines creation and approval.
- Briefs are paginated; selecting an inquiry or project scopes the list.
- The browser remembers query and questionnaire ids through the shared workspace helper.

## 4. Requirements and dependencies

- MVP-FR-003
- Needs a query (or project) id from [MOD-210](../MOD-210/E2E_GUIDE.md) / [MOD-240](../MOD-240/E2E_GUIDE.md)
- Workspace key: `masms.workspace.queryId` / `questionnaireId`

## 5. How to start

Complete J-QUERY. Open **Project Delivery → Requirements**. Role: Contributor to publish; Baseline Approver/Admin if the brief button is hidden.

## 6. Screens, buttons, and files

Route: `/requirements`  
Files: [`apps/web/src/app/requirements/page.tsx`](../../../apps/web/src/app/requirements/page.tsx), [`requirements-desk-page.tsx`](../../../apps/web/src/components/requirements-desk-page.tsx)

| Control | What happens | Status |
|---|---|---|
| New / toggle bootstrap | Publish intake questionnaire form | Implemented |
| Short name, Title | Questionnaire identity | Implemented |
| Publish questionnaire | Create + version + publish | Implemented |
| Search questionnaires | Filters list | Implemented |
| Start questionnaire | Empty-state open form | Implemented |
| Suggest questions | Decorative AI button | Planned |
| Select questionnaire | Loads questions / answers | Implemented |
| Linked inquiry | Entity id for scoring | Implemented |
| Save answers & score | Upsert answers + completeness | Implemented |
| Create clarifications | Gap questions become follow-up-like records | Implemented |
| Create & approve brief | Combined create + approve | Implemented (human gate) |
| Briefs table + pagination | List | Implemented |

## 7. API, data, and automated tests

Prefix: `/api/v1/requirements`  
Router: [`modules/requirements/router.py`](../../../apps/api/src/masms_api/modules/requirements/router.py)  
Migration: `20260811_0012`  
Client helpers: `createQuestionnaire`, `publishQuestionnaireVersion`, `upsertRequirementAnswer`, `computeCompleteness`, `createClarification`, `createRequirementsBrief`, `approveRequirementsBrief`.

Tests: `tests/unit/requirements/`, `tests/integration/requirements/`

```bash
uv run pytest tests/unit/requirements tests/integration/requirements -q --tb=short
```

## 8. Test flows

### F-SETUP

A query id from [MOD-210](../MOD-210/E2E_GUIDE.md).

### F-HAPPY

1. Publish questionnaire.
2. Select it; link the inquiry.
3. Answer questions; **Save answers & score**.
4. If below threshold, **Create clarifications**.
5. When threshold met, **Create & approve brief**.
6. **Expected:** brief appears with approved status; published questionnaire version is immutable.

### F-VALIDATE

Publish with empty title — browser required.

### F-AUTHZ

Viewer: no publish. Agent role: must not be treated as brief approver on the API.

### F-TENANT

Other org cannot see questionnaires.

### F-CONCUR

Approve brief with stale version via API — conflict.

### F-TRANS

Approve a brief that is already approved — invalid / immutable.

### F-GATE

Brief approval is human-only even though the UI combines create+approve.

### F-TERM

Approved brief is immutable; changes need a new version (API).

### F-RECOVER

N/A.

### F-CLEAN

Keep the questionnaire as sample intake.

## 9. Security, privacy, and approvals

Answers may contain client PII. Do not paste them into agent prompts.

## 10. Planned versus implemented

Question designer, separate submit vs approve screens, and AI suggestions are later.

## 11. Related journeys

- [J-BRIEF](../../testing/CROSS_MODULE_JOURNEYS.md#j-brief-questionnaire-to-project-srs)

## 12. Pass / fail checklist

| Step | Result |
|---|---|
| Publish questionnaire | |
| Score answers | |
| Clarifications on gaps | |
| Human brief approve (combined button) | |
| Suggest questions not claimed live | |
| Requirements tests run | |
