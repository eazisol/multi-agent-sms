Use this complete prompt in Cursor:

````md
# TASK: Replace All Inline Success/Error/Warning/Info Messages With a Global Premium Toast Notification System

## Goal

Replace all current inline feedback messages across the MASMS frontend with one reusable, modern, premium toast notification system.

The current UI sometimes shows messages as full-width bars inside page content, for example a green success bar after creating a client. These should be removed from normal page flow and replaced with bottom-right floating toast notifications.

The result must match the current premium dark MASMS UI and feel polished, modern, compact, accessible, and consistent across the entire application.

---

# 1. First Inspect the Existing Project

Before changing code:

1. Inspect the frontend structure.
2. Identify:
   - Next.js version
   - App Router or Pages Router
   - Existing shadcn/ui setup
   - Existing toast library, if any
   - Existing notification/message utility
   - Existing success/error state handling
   - Current form submission patterns
   - Current API error handling
   - Current dark/light theme implementation
3. Search the entire frontend for:
   - inline success banners
   - inline error banners
   - warning banners
   - info banners
   - `alert(...)`
   - custom message state
   - `setSuccess`
   - `setError`
   - `setMessage`
   - `successMessage`
   - `errorMessage`
   - `toast`
   - any temporary full-width notification components
4. Reuse the existing design system and dependencies where appropriate.
5. Do not create duplicate notification systems.

Do not start implementation until the existing pattern is understood.

---

# 2. Preferred Implementation

Use **Sonner** with shadcn/ui if it is already available or can be added cleanly.

Preferred architecture:

```text
Root App Layout
    ↓
Global Toaster
    ↓
Reusable Toast Helper / Utility
    ↓
All Modules
````

The toast system must be globally available from any client-side page/component.

Do not add one `<Toaster />` per page.

There must be only one global toaster instance.

---

# 3. Global Toast Position

All toast notifications must appear:

* fixed at the **bottom-right corner**
* above the viewport edge with safe spacing
* above any bottom navigation or floating UI
* consistently positioned on all desktop pages

Recommended desktop spacing:

```text
right: 20–24px
bottom: 20–24px
```

For smaller/mobile screens:

* keep safe screen margins
* allow the toast container to use most of the available width
* do not let the toast overflow horizontally

---

# 4. Required Toast Variants

Implement reusable support for:

## Success

Use for:

* record created
* record updated
* saved successfully
* approval completed
* upload completed
* status changed successfully
* configuration saved
* item deleted/archived successfully where appropriate

Example:

Title:
`Client created successfully`

Optional description:
`Ahmad Akram has been added to your clients.`

---

## Error

Use for:

* API request failure
* validation failure not tied to one field
* failed create/update/delete
* network error
* permission failure where toast is appropriate
* unexpected application error

Example:

Title:
`Failed to create client`

Description:
`Please try again. If the issue continues, contact your administrator.`

Never show raw stack traces or technical backend details to normal users.

---

## Warning

Use for:

* incomplete data
* potentially risky action
* partial success
* dependency missing
* business warning that does not block the entire screen

Example:

Title:
`Some information is missing`

Description:
`Add the primary client contact before starting requirement gathering.`

---

## Info

Use for:

* background state
* general updates
* non-critical system feedback
* saved draft notification

Example:

Title:
`Draft saved`

Description:
`Your changes are saved but have not been submitted for approval.`

---

## Loading / Processing

Support loading toast where useful for asynchronous actions.

Example:

`Creating client...`

Then update the same toast to:

`Client created successfully`

or:

`Failed to create client`

Do not generate multiple separate loading/success toasts for one action if a single toast can be updated.

---

# 5. Toast Visual Design

The design must match the existing dark MASMS design.

## General appearance

Toast should feel like a premium floating card.

Use:

* compact width
* rounded corners
* subtle border
* soft shadow
* layered dark surface
* clear icon
* title
* optional description
* close button
* subtle accent based on type

Recommended values:

```text
border-radius: 12px–14px
padding: 14px–16px
gap: 10px–12px
```

Recommended width:

```text
min-width: 320px
max-width: 420px
```

Responsive mobile width:

```text
calc(100vw - 32px)
```

---

# 6. Toast Color Direction

Do not use large flat bright backgrounds.

Keep the main toast surface dark/neutral and use accents.

## Success

* emerald/green icon
* subtle green border/accent
* dark neutral background

## Error

* red icon
* subtle red border/accent
* dark neutral background

## Warning

* amber/orange icon
* subtle amber border/accent

## Info

* blue icon
* subtle blue border/accent

## Loading

* neutral/blue animated spinner
* no aggressive animation

The toast must remain readable in both dark and light themes if both themes are supported.

---

# 7. Icons

Use the project’s existing icon library.

If Lucide is already used, prefer:

```text
Success     CircleCheck
Error       CircleX
Warning     TriangleAlert
Info        Info
Loading     Loader2
Close       X
```

Do not introduce a second icon library only for toast notifications.

---

# 8. Typography

Use the existing MASMS typography system.

Recommended hierarchy:

```text
Title:
14px
font-weight: 600

Description:
13px
muted foreground
line-height: 1.4
```

Avoid oversized titles or long paragraphs.

---

# 9. Auto Dismiss Behavior

Default duration:

```text
4500ms
```

Acceptable range:

```text
4000–5000ms
```

Configure globally unless a specific toast requires another duration.

---

# 10. Hover Pause Behavior

This is mandatory.

When a user hovers over a toast:

* pause the auto-dismiss timer
* keep the toast visible
* do not close while the pointer remains over the toast

When the pointer leaves:

* resume the remaining dismiss duration

Use Sonner’s built-in supported behavior where available rather than implementing fragile custom timers.

Verify this behavior manually.

---

# 11. Manual Close

Every normal toast should provide a close button.

Requirements:

* small
* visually subtle
* clearly visible on hover/focus
* keyboard accessible
* correct accessible label

Example accessible label:

`Dismiss notification`

Do not rely only on auto-dismiss.

---

# 12. Multiple Toast Behavior

Configure the system so:

* maximum visible toasts: **4**
* toasts stack vertically
* spacing between toasts is consistent
* newest toast appears in the natural new-toast position supported by the library
* overflow should be handled gracefully

Do not fill the screen with unlimited notifications.

---

# 13. Animations

Use subtle modern animations.

## Enter

* fade in
* slight translate from bottom/right

## Exit

* fade out
* slight translate down/right

Recommended duration:

```text
150–250ms
```

Do not use:

* bouncing
* large scale effects
* excessive spring animation
* flashing colors

Respect reduced-motion preferences.

---

# 14. Accessibility

Toast implementation must include:

* proper ARIA behavior from the toast library
* keyboard-accessible close action
* visible focus states
* sufficient text contrast
* icons must not be the only indication of status
* success/error/warning/info should also be communicated through text
* respect `prefers-reduced-motion`

Do not use color alone to communicate status.

---

# 15. Build a Reusable Toast API

Create or standardize a reusable helper so feature modules do not directly duplicate visual configuration.

Recommended usage pattern:

```ts
notify.success({
  title: "Client created successfully",
  description: "The client is now available in your workspace.",
})
```

```ts
notify.error({
  title: "Failed to create client",
  description: "Please try again.",
})
```

```ts
notify.warning({
  title: "Missing information",
  description: "Add the required fields before continuing.",
})
```

```ts
notify.info({
  title: "Draft saved",
})
```

Also support simple shorthand if appropriate:

```ts
notify.success("Client created successfully")
```

Keep the API strongly typed.

---

# 16. Recommended File Structure

Adapt to the actual repository, but prefer a structure similar to:

```text
components/
  ui/
    sonner.tsx

lib/
  notifications/
    notify.ts
    notification-types.ts

app/
  layout.tsx
```

or the equivalent structure already used in the repository.

Do not create unnecessary wrappers if the project already has an established pattern.

---

# 17. Global Toaster Configuration

Add the global toaster to the root layout/provider level.

Example behavior requirements:

```text
position: bottom-right
duration: 4500
visibleToasts: 4
closeButton: true
richColors: false or custom styled
expand: false unless UX testing proves expanded is better
```

Match the existing design tokens.

Do not use Sonner's default styling blindly if it visually conflicts with MASMS.

Apply custom class names / CSS variables / Tailwind classes as necessary.

---

# 18. Remove Existing Inline Feedback Bars

Search the entire application and replace non-persistent feedback such as:

```text
Client created successfully
Project created successfully
Document created
Requirement approved
SRS created
Settings saved
Failed to create...
Failed to update...
```

that currently renders inside the normal page layout.

Remove success/error bars that exist only to confirm an action.

The example full-width green message shown on the Clients page must be removed.

After successful creation, only the bottom-right toast should appear.

---

# 19. Do Not Remove Persistent Business Alerts

Important distinction:

Not every alert should become a toast.

Keep persistent inline/card/banner alerts when the information remains relevant after the toast disappears.

Examples that should remain persistent:

* Project is On Hold
* Production incident is active
* Requirement approval is blocking work
* User lacks required access
* Client response is overdue
* Critical security issue
* Release is blocked
* Failed integration connection
* Unsaved destructive conflict
* Permanent validation summary requiring user action

Use toast for temporary action feedback.

Use persistent UI for ongoing business state.

Do not blindly convert all `<Alert>` components.

---

# 20. Form Validation Rules

Field-level validation should remain next to the field.

Example:

```text
Email
[ invalid-email ]

Enter a valid email address.
```

Do not replace field-level validation with only a toast.

Use an error toast only for:

* submission-level failure
* unexpected error
* several errors requiring attention
* server rejection not mapped to one field

---

# 21. API Error Handling

Create a consistent method for converting backend failures into user-friendly toast messages.

Handle at minimum:

```text
400 validation/business error
401 authentication expired
403 forbidden
404 not found
409 conflict/stale version
422 validation
429 rate limited
500 unexpected server error
network/offline failure
timeout
```

Examples:

### 403

Title:
`You don't have permission`

Description:
`Your current role cannot perform this action.`

### 409

Title:
`This record has changed`

Description:
`Refresh the latest version before trying again.`

### 429

Title:
`Too many requests`

Description:
`Please wait a moment and try again.`

### Network

Title:
`Connection problem`

Description:
`Check your internet connection and try again.`

Do not expose raw server exception messages unless the backend explicitly marks them safe for users.

---

# 22. Prevent Duplicate Toasts

Avoid duplicate feedback from:

```text
mutation callback
+
page effect
+
global API interceptor
```

For one user action, normally show one result toast.

Use toast IDs where helpful.

Example:

```ts
const toastId = toast.loading("Creating client...")

toast.success("Client created successfully", {
  id: toastId,
})
```

This must replace the existing loading toast instead of creating another one.

---

# 23. Update All Current Modules

Audit all currently implemented screens and use the new system consistently.

At minimum check:

```text
Clients
Queries
Projects
Requirements
SRS
Documents
Roadmap
Governance
Source Baselines
Architecture Decisions
Change Requests
Users
Teams
Permissions
Workflows
Integrations
```

And any additional currently implemented pages.

For each mutation:

```text
Create
Update
Delete
Archive
Restore
Assign
Reassign
Approve
Reject
Submit
Generate
Upload
Download failure
Status change
Integration connect/disconnect
```

provide appropriate feedback.

---

# 24. Client Page Specific Requirement

For the current Clients page:

Remove the inline green bar similar to:

`dsdcs added`

After client creation show:

```text
Success icon

Client created successfully
“dsdcs” has been added to your clients.
```

at the bottom-right.

After successful creation:

* reset the form if appropriate
* refresh/update the list
* keep user on the Clients page
* show the toast once

If creation fails:

```text
Failed to create client
Please review the details and try again.
```

Do not show both an inline error banner and an error toast for the same submission.

---

# 25. Query Example

After a query is created:

```text
Query created
The inquiry has been added and is ready for BD review.
```

After qualification:

```text
Query qualified
The inquiry can now move to the next workflow stage.
```

---

# 26. Project Example

After project creation:

```text
Project created
The project workspace is ready.
```

After SRS draft generation:

```text
SRS draft generated
Review the document before submitting it for approval.
```

Do NOT say:

`SRS approved`

unless the human approval action actually succeeded.

---

# 27. Approval Example

Approve:

```text
Approval recorded
SRS version 1.4 has been approved.
```

Reject:

```text
Approval rejected
Your reason has been recorded and the requester will be notified.
```

Request changes:

```text
Changes requested
The item has been returned to the owner for revision.
```

---

# 28. Document Example

Upload:

Loading:

```text
Uploading document...
```

Success:

```text
Document uploaded
The file has been uploaded and is being processed.
```

If malware/file validation happens asynchronously, do NOT say the document is "available" until that process actually succeeds.

---

# 29. Destructive Actions

For delete/archive actions:

* confirmation dialog remains separate
* toast happens after confirmed result

Success:

```text
Client archived
The client has been moved out of the active list.
```

Failure:

```text
Unable to archive client
The client may still be referenced by active records.
```

Do not use toast as the confirmation dialog.

---

# 30. Async Background Actions

For long-running tasks such as:

* Generate SRS
* Generate roadmap
* Agent analysis
* Large upload
* Sync integration

Use loading/progress feedback.

Example:

```text
Analyzing requirements...
```

Then:

```text
Requirement analysis completed
3 missing items were identified.
```

If the operation continues after the HTTP request:

do not falsely show completion.

Instead:

```text
Analysis started
You will be notified when the result is ready.
```

---

# 31. Toast Text Quality

All toast content must be professional.

Avoid:

```text
Success!
Done!
Added
Something went wrong
Oops
Error 500
```

Prefer:

```text
Client created successfully
Project updated
Requirement submitted for approval
Unable to save changes
Connection lost
```

Descriptions should explain the useful next context only.

---

# 32. No Raw Technical Information

Do not show in user-facing toast content:

* UUIDs
* database table names
* stack traces
* SQL errors
* raw API payloads
* raw exception classes
* storage keys
* internal module IDs
* environment secrets
* tokens

Technical details should go to logs/audit/diagnostics, not toast messages.

---

# 33. Toast and Audit Are Different

Toast is presentation feedback.

Audit logging must still happen independently.

Do not replace:

```text
audit record
activity event
notification record
status history
```

with a toast.

The toast does not count as business evidence.

---

# 34. Testing Requirements

Add tests for the toast system.

Test:

## Component / utility

* success toast renders
* error toast renders
* warning toast renders
* info toast renders
* close button dismisses
* duration is configured
* global toaster renders once

## Integration

Test at least:

* client create success
* client create failure
* project create success
* approval success
* API conflict
* permission failure

## Manual UX verification

Verify:

1. toast appears bottom-right
2. it does not move normal page content
3. auto closes after configured duration
4. hovering pauses dismissal
5. leaving resumes dismissal
6. manual close works
7. four toasts stack properly
8. fifth toast is handled gracefully
9. dark mode looks correct
10. mobile layout does not overflow
11. keyboard focus works
12. reduced motion works
13. no duplicate toast occurs
14. inline action-result bars have been removed

---

# 35. Design Acceptance Criteria

The task is complete only when:

* no temporary full-width success bar is shown after client creation
* reusable global toast system is implemented
* toast is bottom-right
* success, error, warning, info, loading are supported
* auto-dismiss is 4–5 seconds
* hover pauses auto-dismiss
* manual close is available
* maximum visible toasts is 4
* animations are subtle and premium
* dark theme matches MASMS
* mobile layout works
* accessibility is maintained
* field validation remains inline
* persistent business alerts remain persistent
* current mutation actions use toast consistently
* raw technical errors are not exposed
* duplicate notifications are prevented
* tests pass
* lint passes
* type checks pass
* production build passes

---

# 36. Cursor Work Rules

While implementing:

* do not modify backend behavior unnecessarily
* do not redesign unrelated pages
* do not weaken authorization
* do not change approved business workflows
* do not remove audit or notification logic
* do not hide actual application errors
* do not use `any` to avoid TypeScript errors
* do not add duplicate dependencies
* reuse existing tokens and utilities
* keep the implementation modular
* preserve responsive behavior
* preserve accessibility
* remove dead legacy message code after migration
* do not leave two toast systems active

---

# 37. Final Verification Commands

Run the project's actual equivalents of:

```bash
npm run lint
npm run typecheck
npm test
npm run build
```

Also run any existing frontend unit/integration tests.

Do not claim completion if any required check fails.

---

# 38. Required Final Cursor Response

When finished, report:

```text
Toast system:
Implemented / Partial / Blocked

Library used:
...

Global toaster location:
...

Files created:
...

Files modified:
...

Legacy inline message components removed:
...

Pages/mutations migrated:
...

Success variant:
Verified / Not verified

Error variant:
Verified / Not verified

Warning variant:
Verified / Not verified

Info variant:
Verified / Not verified

Loading variant:
Verified / Not verified

Bottom-right position:
Verified / Not verified

Auto-dismiss:
Verified / Not verified

Hover pause:
Verified / Not verified

Manual close:
Verified / Not verified

Maximum visible toasts:
Verified / Not verified

Dark mode:
Verified / Not verified

Mobile:
Verified / Not verified

Accessibility:
Verified / Not verified

Tests:
...

Lint:
...

Type check:
...

Build:
...

Remaining inline temporary alerts:
...

Remaining issues:
...
```

Do not mark anything as verified unless it was actually tested.

---

# FINAL EXPECTED RESULT

The current large inline green success message must disappear.

After a successful action, users should see a polished floating notification similar to:

```text
┌────────────────────────────────────────┐
│  ✓   Client created successfully   ×   │
│      Ahmad Akram has been added.       │
└────────────────────────────────────────┘
```

in the **bottom-right corner**, with:

* premium MASMS dark styling
* smooth entrance and exit
* automatic dismissal
* pause on hover
* manual close
* consistent behavior across the complete application

Implement this as the single global standard for temporary user feedback across MASMS.

```
```
