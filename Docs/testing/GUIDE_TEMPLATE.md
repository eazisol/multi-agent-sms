# Guide template (heading contract)

Every [`Docs/modules/MOD-NNN/E2E_GUIDE.md`](../modules/) uses these headings in this order. Depth may vary by module, but the headings stay stable so first-time users, QA, developers, and owners can scan the same document.

```markdown
# MOD-NNN — Title

## 1. Who this guide is for
## 2. What this module is
## 3. Status honesty
## 4. Requirements and dependencies
## 5. How to start
## 6. Screens, buttons, and files
## 7. API, data, and automated tests
## 8. Test flows
## 9. Security, privacy, and approvals
## 10. Planned versus implemented
## 11. Related journeys
## 12. Pass / fail checklist
```

Section rules:

- **What this module is** starts with a plain-language paragraph, then a short “in this company it means…” example.
- **Status honesty** must list Implemented / Stubbed / Planned / Blocked items. Never call a stub “live”.
- **Screens, buttons, and files** is a table: control, what it does, status, source file.
- **Test flows** use F-SETUP, F-HAPPY, F-VALIDATE, F-AUTHZ, F-TENANT, F-CONCUR, F-TRANS, F-GATE, F-TERM, F-RECOVER, F-CLEAN from [`TESTING_CONVENTIONS.md`](TESTING_CONVENTIONS.md).
- Each step has: action, expected UI, expected data/audit, evidence to capture.
- **Pass / fail checklist** is copy-pasteable for a test session.
