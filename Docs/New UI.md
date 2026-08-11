Bilkul. Is project ki UI ko **sirf colors/cards change karke improve nahi karna**. Humein complete MASMS ko **design-system-first redesign** karna chahiye so that it feels like a premium 2026 enterprise AI operations platform.

Current live build abhi developer-oriented feel deta hai—for example current Clients screen directly `MOD-200` aur server-authorization text show karti hai, aur basic create form primary experience hai. ([MASMS][1]) Final product mein aisi technical implementation information normal business users ko visible nahi honi chahiye.

## Final UI direction

Main visual direction recommend karunga:

**“Modern Enterprise AI Command Center”**

Feel should be similar to the quality level of modern Linear / Notion / Vercel-style SaaS products, but copied nahi—MASMS ki apni identity honi chahiye.

Visual characteristics:

* Clean, spacious but not wasteful
* Premium neutral background
* Strong information hierarchy
* Compact enterprise navigation
* Subtle gradients only where useful
* Very light shadows and borders
* Rounded components, but overly bubbly UI nahi
* Consistent status colors
* Excellent tables
* Beautiful empty states
* Contextual drawers instead of unnecessary pages
* Command palette
* Global search
* AI assistant integrated into workflow
* Light + Dark mode
* Smooth micro-interactions
* Mobile/tablet responsive
* Accessibility built in

For the component layer, continuing with **shadcn/ui is a strong fit** because its current component system is designed around composable accessible primitives; the 2026 docs also provide explicit component-composition guidance. Current shadcn supports Base UI, React Aria and Radix; if the project already uses Radix successfully, there is no reason to migrate simply for visual reasons. ([Shadcn UI][2])

---

# 1. Completely replace the current application shell

Current horizontal:

`Clients | Queries | Projects | Documents | Roadmap | Governance`

should be replaced with a professional collapsible sidebar.

### Proposed sidebar

```text
MASMS

WORKSPACE
  Dashboard
  My Work
  Inbox

BUSINESS DEVELOPMENT
  Clients
  Queries
  Opportunities

PROJECT DELIVERY
  Projects
  Requirements
  Roadmaps
  Tickets

COORDINATION
  Follow-ups
  Approvals

QUALITY
  Test Cases
  Bugs

AI OPERATIONS
  Agents
  Agent Runs
  Knowledge Base

DELIVERY
  Releases
  Deployments

GOVERNANCE
  Source Baselines
  Architecture Decisions
  Change Requests
  Audit Logs

ADMINISTRATION
  Users & Teams
  Roles & Permissions
  Skills & Capacity
  Workflows
  Integrations
  Notifications
  Security
```

Sidebar should support:

* Expanded mode
* Collapsed icon mode
* Active module indicator
* Badge counts
* Section grouping
* Keyboard navigation
* Responsive mobile drawer

---

# 2. Global top header

Every screen should get a professional context header.

```text
[☰]  Acme Project / Client Portal

Search anything...                     + Create
                                       Notifications
                                       AI Assistant
                                       User Avatar
```

Also add contextual breadcrumbs:

```text
Projects / EarthCo / Requirements / REQ-104
```

Do **not** show raw UUIDs unless user intentionally opens developer/system information.

---

# 3. Remove developer-centric UI completely

Normal users should never see things like:

* `MOD-200`
* `Server authorization remains authoritative`
* `Active Project ID`
* `Query ID`
* `Storage Key`
* Raw UUID inputs
* Internal API terminology
* Database-oriented actions

These are useful in development/testing, but should live under:

**Developer Tools / Debug Mode**

or not be rendered at all in production.

The user experience should always be:

```text
Search
→ Select
→ View context
→ Take allowed action
```

not:

```text
Copy UUID
→ Paste UUID
→ Execute API action
```

---

# 4. New visual design system

## Colors

Avoid excessively colorful SaaS UI.

Recommended foundation:

```text
Primary Accent
Deep Indigo / Electric Blue

Background
Very light cool gray

Surface
White

Dark Mode
Near-black graphite

Text Primary
Deep charcoal

Text Secondary
Muted slate

Borders
Soft neutral

Success
Emerald

Warning
Amber

Danger
Red

Information
Blue

AI-specific
Indigo → Violet subtle gradient
```

Accent should mostly appear on:

* Primary buttons
* Active navigation
* Important metrics
* AI features
* Selected states
* Links

Not on every card.

---

# 5. Typography

Use a modern UI typeface such as:

**Geist** as first preference.

Hierarchy:

```text
Page Title        28–32px / semibold
Section Heading   20–24px / semibold
Card Heading      15–16px / semibold
Body              14px
Metadata          12–13px
```

Use weight and spacing more than huge font sizes.

Enterprise software needs information density.

---

# 6. Spacing system

Use consistent spacing:

```text
4
8
12
16
20
24
32
40
48
```

No random padding such as:

```text
17px
22px
29px
```

Use predictable rhythm throughout the application.

---

# 7. Border radius

Recommended:

```text
Inputs          8px
Buttons         8px
Small cards    10px
Main cards     12px
Drawers        16px
Large modals   16px
```

Avoid huge 24–32px rounded boxes everywhere.

That usually makes enterprise applications look less professional.

---

# 8. Shadows

Keep shadows very subtle.

Default surfaces should primarily use:

```text
border + background
```

Elevation should be reserved for:

* Dropdowns
* Command palette
* Floating menus
* Dialogs
* Drawers
* Dragged cards

This will make MASMS feel cleaner and more premium.

---

# 9. Buttons

Standardize buttons.

### Variants

```text
Primary
Secondary
Outline
Ghost
Destructive
Link
AI Action
```

Examples:

**Primary**

`Create Project`

**Secondary**

`Generate Report`

**Ghost**

`View Details`

**Destructive**

`Archive`

**AI**

`✦ Generate SRS`

AI-related actions can use a subtle indigo treatment so users immediately understand when AI is involved.

---

# 10. Forms

Current plain stacked forms should become structured form experiences.

Instead of:

```text
Code
[       ]

Name
[       ]

Industry
[       ]
```

use:

```text
┌─────────────────────────────────────────────┐
│ Create Client                               │
│ Add the basic business information.         │
│                                             │
│ Client Name          Industry               │
│ [____________]       [____________]         │
│                                             │
│ Website              Country                │
│ [____________]       [____________]         │
│                                             │
│ Account Manager                             │
│ [ Search team member ▼ ]                    │
│                                             │
│                     Cancel   Create Client  │
└─────────────────────────────────────────────┘
```

Use:

* Inline descriptions
* Proper labels
* Required indicators
* Helpful error text
* Validation while typing where appropriate
* Comboboxes
* Date pickers
* Searchable selects

Current shadcn form patterns provide structured `Field`, label, description and error composition rather than loose labels and inputs. ([Shadcn UI][3])

---

# 11. Tables must become a core component

MASMS is an operations platform, so tables need to be excellent.

Every important list should support:

* Search
* Filters
* Sort
* Pagination
* Column visibility
* Saved views
* Bulk actions where safe
* Status badges
* Row selection
* Context actions
* Sticky header
* Loading skeleton
* Empty state

For example Clients:

```text
┌──────────────────────────────────────────────────────────────┐
│ Clients                                    + New Client      │
│                                                              │
│ Search clients...     Status ▼   Industry ▼   Owner ▼       │
├──────────────────────────────────────────────────────────────┤
│ Client        Industry      Manager     Projects    Status   │
│ Acme Inc      Technology    Sarah        3          Active   │
│ EarthCo       Landscaping   Asad         2          Active   │
│ GreenCore     Services      Nadia        1          Active   │
└──────────────────────────────────────────────────────────────┘
```

Clicking the row opens the client—not a raw ID field.

---

# 12. Client UI redesign

### `/clients`

Client list.

### `/clients/[clientId]`

Client workspace:

```text
Acme Corporation
Technology • United States

[Overview] [Contacts] [Queries] [Opportunities]
[Projects] [Documents] [Messages] [Activity]
```

Overview:

```text
Active Projects      Open Queries      Contacts
      4                   2                8

Account Manager
Sarah Khan

Primary Contact
John Peterson

Latest Activity
────────────────────
Requirement updated
Client replied
Project milestone approved
```

---

# 13. Query Inbox redesign

This should look like an actual business-development inbox.

```text
Queries

[ All 18 ] [ New 5 ] [ Waiting Client 4 ]
[ Qualified 6 ] [ Overdue 3 ]

Search...      Owner ▼      Priority ▼

─────────────────────────────────────────────
Acme Corporation
Mobile application development
High priority                     12 min ago

EarthCo
CRM enhancement
Waiting for client                 2h ago
```

Selecting a query opens a complete workspace.

---

# 14. Query detail should become a split workspace

```text
┌─────────────────────────────┬─────────────────────────────┐
│ Query / Requirements        │ BD Agent                   │
│                             │                             │
│ Client                      │ ✦ Requirement completeness │
│ Project objective           │ 76%                         │
│ Required features           │                             │
│ Platform                    │ Missing                    │
│ Integrations                │ • Expected users           │
│ Timeline                    │ • Hosting preference       │
│ Budget                      │ • Approval workflow        │
│                             │                             │
│ Conversation                │ Ask client                 │
│ -----------------------     │ [Generate questions]       │
└─────────────────────────────┴─────────────────────────────┘
```

This is where the product begins to feel truly **agentic**.

---

# 15. AI should be visible but not dominate everything

Don't turn MASMS into one giant chatbot.

AI needs to appear contextually.

Examples:

```text
✦ Generate Requirement Brief
✦ Analyze Missing Requirements
✦ Draft SRS
✦ Suggest Project Phases
✦ Break into Tickets
✦ Recommend Assignee
✦ Generate Test Cases
✦ Summarize Project Status
```

Each AI result should clearly show:

```text
AI Recommendation
Confidence: High

Based on:
• SRS v1.4
• Requirement Brief v2
• Client Meeting – Aug 10

[Review]
[Edit]
[Approve]
[Reject]
```

shadcn also introduced dedicated chat-interface components in 2026, so a contextual assistant panel can be built without making the entire product a chat UI. ([Shadcn UI][4])

---

# 16. Project workspace must be the strongest screen

Instead of a project creation/testing form:

```text
EarthCo CRM Platform               Healthy ●
Client: EarthCo                   67% Complete

Overview   Requirements   SRS   Roadmap
Tickets    Team           Follow-ups
Approvals  QA             Risks
Changes    Documents      Releases    Activity
```

Top summary:

```text
Overall        Current Phase    Target
67%            Development      Sep 15

Open Tickets   Blocked          Critical Bugs
23             3                0
```

Then:

```text
Current Phase
Development
████████████████░░ 78%

Upcoming Milestone
CRM Beta Release
Aug 23

Attention Needed
3 overdue follow-ups
2 pending approvals
1 blocked ticket
```

---

# 17. Requirements screen

Use a professional structured table:

```text
ID        Requirement                   Module      Priority  Status
REQ-001   User authentication           Auth        Must      Approved
REQ-002   Role based permissions        Security    Must      Review
REQ-003   Project dashboard             Dashboard   High      Draft
```

Clicking opens:

```text
REQ-002
Role Based Permissions

Current Version: 1.3
Approved Version: 1.2

[Overview] [Acceptance Criteria]
[Versions] [Tickets] [Tests]
[Approvals] [Activity]
```

---

# 18. SRS experience

This requires a proper document experience.

```text
Software Requirements Specification

Version 1.4
Under Review

─────────────────────────────

Table of Contents
1. Introduction
2. Product Overview
3. User Roles
4. Functional Requirements
5. Non-Functional Requirements
...

─────────────────────────────

Human Review
PM       Approved
TL       Approved
QA       Pending
Client   Pending
```

Actions:

`Compare Versions`

`Request Changes`

`Submit for Approval`

Never:

**Create & Approve SRS**

as one button.

---

# 19. Roadmap redesign

Roadmap needs actual visual planning.

Modes:

```text
Timeline
Phases
Milestones
Dependencies
Baseline
```

Timeline example:

```text
Discovery      █████
Design             ███████
Development             █████████████
QA                               ██████
Deployment                             ███
```

Cards should show:

* Owner
* Dates
* Health
* Completion
* Dependencies
* Open risks
* Approval state

---

# 20. Ticket management

Three views:

```text
Board
List
Timeline
```

Kanban:

```text
BACKLOG      READY      IN PROGRESS      QA          DONE

DEV-102      DEV-114    DEV-121          DEV-116     DEV-098
DEV-103                 DEV-122          DEV-119
```

Ticket detail should open in a right-side drawer, allowing users to stay in context.

---

# 21. Follow-ups should become a first-class workspace

This is one of MASMS's biggest differentiators.

```text
Follow-ups

Due Today     8
Overdue       3
Escalated     2
Waiting       12
```

Each row:

```text
Developer blocker
DEV-102

From       Ali
To         Team Lead
Due        2:30 PM
Remaining  1h 24m
Priority   High
Status     Waiting
```

A visual SLA timeline would make this very strong.

---

# 22. Approvals should feel premium

Approval Inbox:

```text
Approval Center

Pending     12
Urgent       3
Approved    48
Rejected     4
```

Approval card:

```text
SRS Approval

EarthCo CRM
Version 1.4

Requested by PM Agent
2 hours ago

Changes since v1.3
+ 4 requirements
~ 2 requirements updated

[View Difference]

Reject          Request Changes       Approve
```

---

# 23. QA screen

Use:

```text
Test Cases
Test Runs
Bugs
Regression
Coverage
```

Beautiful QA summary:

```text
Pass Rate
94%

Passed      Failed       Blocked
382         18           5

Critical Bugs    0
High Bugs        3
```

---

# 24. Agent Operations screen

This needs a special modern treatment.

```text
AI Agents

BD Agent
● Running
42 tasks today
96% accepted

PM Agent
● Available
18 tasks today
92% accepted

TL Agent
● Running
12 tasks today
89% accepted
```

Agent detail:

```text
PM Agent

Status          Active
Supervisor      Sarah Khan
Model           GPT-...
Authority       Level 2
Current Runs    3

Recent Runs
──────────────────────────
Generated SRS Draft       Completed
Requirement Analysis      Review Required
Progress Summary          Completed
```

Do not expose raw prompt internals to normal users.

---

# 25. Dashboard

This should become the default `/`.

Something like:

```text
Good morning, Asad

Here is what needs attention today.

Projects
12 Active      2 At Risk       1 Delayed

Approvals
8 Pending      3 Urgent

Follow-ups
14 Due Today   4 Overdue

Quality
94% Pass Rate  2 Critical Issues

────────────────────────────────────────

Project Health

EarthCo CRM             Healthy     72%
Glaura Platform         At Risk     54%
Project Alpha           Healthy     87%

────────────────────────────────────────

Needs Attention

⚠ Development blocker overdue
  EarthCo / DEV-134
  1h 24m overdue

⚠ Client approval pending
  Glaura / SRS 1.3
  2 days

────────────────────────────────────────

Recent Agent Activity

PM Agent generated Phase Plan
QA Agent created 4 bug reports
BD Agent analyzed new inquiry
```

That makes MASMS immediately understandable.

---

# 26. Beautiful empty states

Never show:

`No requirements.`

alone.

Instead:

```text
        ◇

No requirements yet

Requirements define exactly what the project
needs to deliver.

[ + Add Requirement ]   [ ✦ Generate with PM Agent ]
```

Every empty state should explain:

1. What this module is.
2. Why it matters.
3. What user should do next.

---

# 27. Loading states

Replace plain:

`Loading clients…`

with skeleton rows/cards.

Example:

```text
████████████      ████████      █████
██████████        █████████     █████
████████████      ██████        █████
```

This immediately increases perceived quality.

---

# 28. Status system

Create one centralized status component.

Examples:

```text
● Draft
● In Progress
● Waiting
● Approved
● Blocked
● At Risk
● Rejected
● Completed
```

Same status must look identical everywhere.

No page-specific random colors.

---

# 29. Command palette

Add:

`Ctrl / Cmd + K`

Search:

```text
Search MASMS...

> Open EarthCo CRM
> Create Client
> Create Query
> View Overdue Follow-ups
> Pending Approvals
> Run PM Agent
```

This will give the app a genuinely modern professional feel.

---

# 30. Contextual global create button

Top right:

`+ Create`

opens:

```text
Client
Query
Project
Requirement
Ticket
Follow-up
Document
Risk
Change Request
```

Instead of placing giant create forms on every list page.

---

# 31. Notifications

Professional notification popover:

```text
Notifications

Approval Required
EarthCo SRS v1.4
5 min ago

Overdue Follow-up
Developer blocker
32 min ago

QA Failed
DEV-134
1 hour ago
```

---

# 32. Dark mode

We should definitely include a proper dark theme, not an inverted afterthought. Tailwind currently provides responsive variants and explicit dark/color-scheme support, so the design tokens should define both themes from the beginning. ([Tailwind CSS][5])

---

# 33. Accessibility

Beautiful design must still be usable.

We should target WCAG 2.2 AA for the product UI. In particular, interactive targets need sufficient size/spacing and keyboard focus must remain clearly visible. WCAG 2.2's AA minimum target-size criterion is 24×24 CSS pixels, while larger targets are advisable for primary actions. ([W3C][6])

So every redesign must consider:

* Keyboard navigation
* Proper focus states
* Screen-reader labels
* Contrast
* Error messages
* Accessible tables
* Accessible dialogs
* Accessible dropdowns
* Non-color-only status communication
* Reduced-motion support

---

# 34. Responsive behavior

Do not simply shrink desktop.

### Desktop

Full sidebar + content + optional contextual panel.

### Tablet

Collapsed sidebar + main content.

### Mobile

Bottom/sheet navigation for main operations, stacked content, drawers and responsive tables/cards.

---

# 35. Micro-interactions

Add subtle:

* 150–250ms transitions
* Hover states
* Button press feedback
* Row hover
* Skeletons
* Toast confirmations
* Drawer slide
* Status update animation
* Progress changes

Avoid unnecessary animated gradients and bouncing elements.

Enterprise UI should feel **fast**, not playful.

---

# 36. Complete redesign sequence

We should **not redesign random pages independently**.

Use this order:

| Phase     | UI Work                                   |
| --------- | ----------------------------------------- |
| **UI-01** | Design tokens + typography + color system |
| **UI-02** | App shell + sidebar + header              |
| **UI-03** | Shared components                         |
| **UI-04** | Dashboard                                 |
| **UI-05** | Clients                                   |
| **UI-06** | Queries                                   |
| **UI-07** | Requirement Gathering                     |
| **UI-08** | Projects                                  |
| **UI-09** | Requirements                              |
| **UI-10** | SRS                                       |
| **UI-11** | Roadmap                                   |
| **UI-12** | Tickets                                   |
| **UI-13** | Assignments / Team                        |
| **UI-14** | Follow-ups                                |
| **UI-15** | Approvals                                 |
| **UI-16** | Documents                                 |
| **UI-17** | QA / Test Cases                           |
| **UI-18** | Bugs                                      |
| **UI-19** | Risks                                     |
| **UI-20** | Change Requests                           |
| **UI-21** | Agents / Agent Runs                       |
| **UI-22** | Knowledge Base                            |
| **UI-23** | Releases / Deployments                    |
| **UI-24** | Governance / Audit                        |
| **UI-25** | Users / Teams / Permissions               |
| **UI-26** | Workflow Configuration                    |
| **UI-27** | Integrations                              |
| **UI-28** | Notifications / Settings                  |
| **UI-29** | Dark Mode                                 |
| **UI-30** | Responsive + Accessibility                |
| **UI-31** | Final visual consistency audit            |

### Most important rule

**Do not allow Cursor to invent a new style for every page.**

First we build one strong shared design system:

```text
Design Tokens
        ↓
Shared Components
        ↓
Page Templates
        ↓
Module Screens
```

Then every MASMS page automatically feels like the **same premium product**.

The target should be: **less like an admin/API testing dashboard and more like a polished enterprise AI operating system—clean, intelligent, fast, contextual, role-aware and visually premium.**