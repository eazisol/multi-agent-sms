Yes. For MASMS, the cleanest approach is to implement **one global multi-level scrolling architecture** rather than fixing scrolling separately on every page.

The important point is: **do not make every container scrollable.** Define specific scroll levels and reuse them everywhere.

## Recommended MASMS scrolling model

```text
Browser Viewport
│
├── Sidebar
│     └── Independent vertical scroll
│
└── Application Area
      │
      ├── Top Header             ← fixed/sticky
      │
      └── Main Page              ← primary vertical scroll
            │
            ├── Page Header      ← optionally sticky
            │
            ├── Tabs             ← optionally sticky
            │
            └── Page Content
                  │
                  ├── Table      ← internal scroll when required
                  ├── Drawer     ← independent vertical scroll
                  ├── Modal      ← independent vertical scroll
                  ├── Timeline   ← horizontal scroll
                  └── Logs/code  ← horizontal + vertical scroll
```

This gives you controlled **multi-level scrolling** without the UI becoming confusing.

---

# 1. Level 0 — Lock the application to the viewport

For the main application shell, don't let the entire browser body continuously grow.

Use:

```tsx
<div className="h-dvh overflow-hidden">
  <AppShell />
</div>
```

Prefer:

```css
100dvh
```

instead of only:

```css
100vh
```

because `dvh` behaves better with modern mobile browser viewport changes.

---

# 2. Global App Shell

Create one reusable shell for the complete MASMS application.

```tsx
<div className="grid h-dvh grid-cols-[auto_1fr] overflow-hidden">
  <Sidebar />

  <div className="flex min-w-0 flex-col overflow-hidden">
    <TopHeader />

    <main className="min-h-0 flex-1 overflow-y-auto">
      {children}
    </main>
  </div>
</div>
```

The critical classes are:

```text
h-dvh
overflow-hidden
min-h-0
min-w-0
flex-1
overflow-y-auto
```

Especially **`min-h-0`**.

Without it, nested flex containers frequently refuse to shrink and scrolling starts happening on the wrong element.

---

# 3. Sidebar should scroll independently

Your sidebar will eventually contain many sections:

```text
Dashboard

Workspace
CRM
Delivery
Coordination
Quality
AI Operations
Governance
Administration
```

Therefore the sidebar should stay fixed while only its navigation area scrolls.

```tsx
<aside className="flex h-dvh w-64 flex-col border-r">
  <SidebarHeader />

  <nav className="min-h-0 flex-1 overflow-y-auto">
    <SidebarNavigation />
  </nav>

  <SidebarFooter />
</aside>
```

Result:

```text
Logo                  Fixed
──────────────────────────
Navigation             Scroll
Navigation
Navigation
Navigation
──────────────────────────
User Profile           Fixed
```

This is ideal.

---

# 4. Header remains fixed

The global header should not scroll away.

```tsx
<header className="h-16 shrink-0 border-b">
  ...
</header>
```

Because the actual scrolling happens inside:

```tsx
<main className="min-h-0 flex-1 overflow-y-auto">
```

the header automatically stays visible.

You don't even necessarily need `position: sticky`.

---

# 5. Main page should have primary scrolling

Create one standard `PageShell`.

```tsx
export function PageShell({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-full px-6 py-6 lg:px-8">
      {children}
    </div>
  )
}
```

Then pages like:

```text
Clients
Queries
Projects
Tickets
Follow-ups
Approvals
QA
Agents
Governance
```

all behave consistently.

---

# 6. Sticky page headers

For long screens, page actions should stay accessible.

Example:

```tsx
<div className="sticky top-0 z-20 border-b bg-background/95 backdrop-blur">
  <PageHeader />
</div>
```

Example:

```text
Clients                              + New Client
Accounts your team delivers...

------------------------------------------------

                  page content
                     ↓
                   scroll
```

The header remains available.

---

# 7. Sticky tabs

Project detail will have many tabs:

```text
Overview
Requirements
SRS
Roadmap
Tickets
Team
Follow-ups
Approvals
QA
Risks
Changes
Documents
Releases
Activity
```

Keep the tabs visible while content scrolls.

```tsx
<div className="sticky top-0 z-10 bg-background">
  <ProjectTabs />
</div>
```

Or if the page header is also sticky:

```tsx
top-[72px]
```

depending on your shell.

---

# 8. Table scrolling

Tables are where multi-level scrolling becomes especially useful.

For large MASMS tables:

```tsx
<div className="min-h-0 overflow-hidden rounded-xl border">
  <div className="max-h-[calc(100dvh-260px)] overflow-auto">
    <table className="min-w-[900px]">
      ...
    </table>
  </div>
</div>
```

This provides:

* vertical scrolling
* horizontal scrolling
* page remains stable

---

# 9. Sticky table headers

Use:

```tsx
<thead className="sticky top-0 z-10 bg-card">
```

Then:

```text
CLIENT    INDUSTRY    STATUS    CREATED
---------------------------------------
Client 1
Client 2
Client 3
      ↓
scroll
```

Column headings remain visible.

This is especially important for:

* Clients
* Queries
* Tickets
* Follow-ups
* Approvals
* Bugs
* Agent Runs
* Audit Logs

---

# 10. Horizontal scrolling for wide tables

Don't squeeze 12 columns into a small screen.

Use:

```tsx
<div className="overflow-x-auto">
  <table className="min-w-[1100px]">
```

Example:

```text
Ticket | Owner | Phase | Priority | Status | Due | Estimate | QA | ...
←──────────────────────────────────────────────────────────→
```

Much better than destroying readability.

---

# 11. Project detail should have nested scrolling

Project pages will be complex.

Recommended:

```text
┌──────────────────────────────────────────────────┐
│ EarthCo CRM                     Healthy •        │
│ 67% Complete                                     │
├──────────────────────────────────────────────────┤
│ Overview Requirements SRS Roadmap Tickets ...   │ ← sticky
├──────────────────────────────────────────────────┤
│                                                  │
│              Current Tab Content                 │
│                    ↓ scroll                      │
│                                                  │
└──────────────────────────────────────────────────┘
```

Only the tab body needs to scroll.

Example:

```tsx
<div className="flex h-full min-h-0 flex-col">
  <ProjectHeader />

  <ProjectTabs />

  <div className="min-h-0 flex-1 overflow-y-auto">
    {children}
  </div>
</div>
```

---

# 12. Split-panel pages

Requirement Gathering should probably use this.

Example:

```text
┌───────────────────────────────┬────────────────────┐
│ Requirement Content           │ BD Agent           │
│                               │                    │
│ ↓ independent scroll          │ ↓ independent      │
│                               │    scroll          │
│                               │                    │
└───────────────────────────────┴────────────────────┘
```

Implementation:

```tsx
<div className="grid h-full min-h-0 grid-cols-[minmax(0,1fr)_380px] overflow-hidden">
  <section className="min-w-0 overflow-y-auto">
    ...
  </section>

  <aside className="min-w-0 overflow-y-auto border-l">
    ...
  </aside>
</div>
```

This would work extremely well for:

* Requirement Gathering
* SRS Review
* Approval Review
* Agent Run Review
* QA
* Change Request analysis

---

# 13. Drawers should have independent scrolling

Ticket details should open inside a right drawer.

Structure:

```text
Drawer Header         Fixed
────────────────────────────
Drawer Content        Scroll
                      ↓
────────────────────────────
Drawer Footer         Fixed
```

Implementation:

```tsx
<div className="flex h-full flex-col overflow-hidden">
  <DrawerHeader className="shrink-0" />

  <div className="min-h-0 flex-1 overflow-y-auto">
    <DrawerContent />
  </div>

  <DrawerFooter className="shrink-0" />
</div>
```

Very important for long ticket, bug and approval details.

---

# 14. Modal scrolling

For large modal content:

```tsx
<DialogContent className="flex max-h-[90dvh] flex-col overflow-hidden">
  <DialogHeader className="shrink-0" />

  <div className="min-h-0 flex-1 overflow-y-auto">
    ...
  </div>

  <DialogFooter className="shrink-0" />
</DialogContent>
```

Don't allow the full modal to go outside the viewport.

---

# 15. Horizontal roadmap scrolling

Roadmaps need different behavior.

```text
Phase 1 ─────
       Phase 2 ─────────
               Phase 3 ─────────────
                         Phase 4 ───────
←────────────────────────────────────────→
```

Use:

```tsx
<div className="overflow-x-auto overflow-y-hidden">
```

Keep phase labels optionally sticky on the left.

---

# 16. Kanban scrolling

Tickets may eventually use:

```text
BACKLOG | READY | IN PROGRESS | REVIEW | QA | DONE
```

The board itself should support horizontal scroll:

```tsx
<div className="flex min-h-0 flex-1 gap-4 overflow-x-auto">
```

Each column:

```tsx
<div className="flex h-full w-80 shrink-0 flex-col">
  <ColumnHeader />

  <div className="min-h-0 flex-1 overflow-y-auto">
    <TicketCards />
  </div>
</div>
```

This gives **two-dimensional nested scrolling**:

* Entire board → horizontal
* Individual column → vertical

Very useful.

---

# 17. Follow-up workspace

Example:

```text
Follow-up List            Follow-up Details
↓ scroll                  ↓ scroll
↓                         ↓
↓                         ↓
```

You could use:

```tsx
<div className="grid h-full min-h-0 grid-cols-[380px_minmax(0,1fr)] overflow-hidden">
```

Both panes independently scroll.

---

# 18. Approval Center

Same pattern:

```text
Approval Inbox | Approval Detail | Supporting Evidence
    ↓                 ↓                    ↓
```

Desktop could even use three panes:

```tsx
grid-cols-[340px_minmax(0,1fr)_360px]
```

All with:

```text
min-h-0
overflow-y-auto
```

---

# 19. Audit log scrolling

Audit tables can become enormous.

Don't load thousands of records into page scroll.

Use:

```text
Page
 └── Filter bar
 └── Table viewport
       ├── sticky headers
       └── virtualized rows
```

For very large lists, use virtualization.

Examples:

* TanStack Virtual
* existing virtualization library if project already has one

Do not render 20,000 DOM rows.

---

# 20. Custom scrollbar styling

For MASMS dark theme, native scrollbars can be subtly styled globally.

Example:

```css
* {
  scrollbar-width: thin;
  scrollbar-color:
    color-mix(in srgb, var(--muted-foreground) 35%, transparent)
    transparent;
}

*::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

*::-webkit-scrollbar-track {
  background: transparent;
}

*::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.28);
  border-radius: 999px;
}

*::-webkit-scrollbar-thumb:hover {
  background: rgba(148, 163, 184, 0.45);
}
```

Keep scrollbars subtle.

Don't make them bright blue or green.

---

# 21. When to use shadcn ScrollArea

Use native:

```css
overflow-auto
```

for most page-level scrolling.

Use shadcn `ScrollArea` when:

* custom scrollbar visuals matter
* drawer/list panel needs consistent scrollbar styling
* compact sidebar
* notification list
* agent activity panel

Don't wrap every page in multiple `ScrollArea` components.

Native scrolling is simpler and more reliable.

---

# 22. Important Tailwind rule

Most nested scrolling problems happen because developers forget:

```text
min-h-0
```

For horizontal layout:

```text
min-w-0
```

Remember:

```tsx
<div className="flex h-full flex-col">
  <div>Header</div>

  <div className="min-h-0 flex-1 overflow-y-auto">
    Scroll content
  </div>
</div>
```

Without `min-h-0`, the child may expand beyond the parent rather than scroll.

---

# 23. Global reusable components

Create these once:

```text
AppShell
PageShell
PageHeader
PageBody
StickyToolbar
ScrollableContent
ScrollablePanel
DataTableViewport
HorizontalScroller
SplitPane
DetailDrawer
ScrollableDialog
KanbanViewport
TimelineViewport
```

Then do not write arbitrary overflow logic page-by-page.

For example:

```tsx
<PageShell>
  <PageHeader />

  <PageBody>
    <DataTableViewport>
      <ClientsTable />
    </DataTableViewport>
  </PageBody>
</PageShell>
```

---

# 24. Define scroll levels formally

I recommend adding this to your Cursor UI rules:

| Level | Container           | Scroll            |
| ----- | ------------------- | ----------------- |
| L0    | Browser/Application | Locked            |
| L1    | Sidebar             | Vertical          |
| L1    | Main App Area       | Vertical          |
| L2    | Page Tabs/Workspace | Vertical          |
| L2    | Data Table          | X/Y when required |
| L2    | Drawer              | Vertical          |
| L2    | Modal body          | Vertical          |
| L3    | Kanban              | Horizontal        |
| L3    | Kanban column       | Vertical          |
| L3    | Timeline/Roadmap    | Horizontal        |
| L3    | Logs/code/data      | X/Y               |

---

# 25. Avoid excessive nested scrolls

Very important.

Don't build:

```text
Page scroll
  → Card scroll
      → Table scroll
          → Cell scroll
```

That becomes horrible UX.

Recommended maximum under normal circumstances:

```text
Viewport
→ Main page
→ One contextual component
```

Three levels only for things such as:

* Kanban
* split workspace
* logs
* code
* large tables

---

# 26. Mouse wheel behavior

Vertical wheel movement should normally control the element under the cursor.

Avoid custom JavaScript wheel interception.

Do **not** implement:

```js
onWheel()
preventDefault()
```

unless absolutely required for a special visualization.

Use native browser scrolling.

---

# 27. Scroll position persistence

This will make MASMS feel much more polished.

When user:

```text
Clients
→ opens Client
→ goes Back
```

restore previous list scroll position.

Similarly:

```text
Tickets Board
→ Ticket Drawer
→ Close
```

should preserve exact board scroll.

Don't reset every screen to top unnecessarily.

---

# 28. Route change behavior

Rules:

### New unrelated page

Scroll to top.

Example:

```text
Clients → Projects
```

### Open drawer/modal

Preserve page position.

### Change tab

Usually reset tab content to top.

### Close drawer

Restore exact page position.

### Pagination/filter

Usually maintain filter-toolbar position.

---

# 29. Mobile behavior

On mobile, reduce nested scrolling.

Desktop:

```text
Sidebar scroll
+
Main content scroll
+
Detail panel scroll
```

Mobile:

```text
Page scroll
+
Sheet/Drawer scroll
```

For tables, allow horizontal scroll.

Do not create multiple tiny vertically scrolling panes on a phone.

---

# 30. Recommended global structure for MASMS

```tsx
<AppRoot className="h-dvh overflow-hidden">

  <AppSidebar className="h-full overflow-hidden">
    <SidebarHeader />
    <SidebarNav className="min-h-0 flex-1 overflow-y-auto" />
    <SidebarFooter />
  </AppSidebar>

  <AppContent className="flex min-w-0 flex-col overflow-hidden">

    <GlobalHeader className="shrink-0" />

    <MainViewport className="min-h-0 flex-1 overflow-y-auto">

      <PageShell>

        <PageHeader />

        <PageContent>
          ...
        </PageContent>

      </PageShell>

    </MainViewport>

  </AppContent>

</AppRoot>
```

This should become the **global standard**.

---

# Cursor prompt

Give Cursor this:

```md
# TASK: Implement a Global Multi-Level Scrolling Architecture Across MASMS

Refactor the MASMS frontend so all pages use one professional and consistent scrolling system.

## Core objective

Implement controlled multi-level scrolling instead of allowing the browser body, random cards, tables, and panels to independently create uncontrolled scroll behavior.

The required hierarchy is:

L0 Application viewport
- height: 100dvh
- overflow: hidden

L1 Sidebar
- fixed within viewport
- header fixed
- navigation vertically scrollable
- footer fixed

L1 Main application
- global header fixed
- main content takes remaining height
- main viewport vertically scrollable

L2 Contextual page components
- tables may scroll internally
- drawers scroll internally
- dialogs scroll internally
- split panes may independently scroll
- project workspace tab body may scroll

L3 Specialized components
- Kanban board horizontal scroll
- Kanban columns vertical scroll
- roadmap/timeline horizontal scroll
- logs/code large-data components may use X/Y scrolling

## Important technical rules

Use:
- `h-dvh`
- `h-full`
- `min-h-0`
- `min-w-0`
- `flex-1`
- `overflow-hidden`
- `overflow-y-auto`
- `overflow-x-auto`

Use `min-h-0` for every flex/grid child that must shrink and scroll.

Use `min-w-0` for horizontal flex/grid children containing tables, text, or wide content.

Do not allow the `<body>` to become the primary application scroll container after authentication.

Do not use JavaScript wheel interception or `preventDefault` for normal scrolling.

Prefer native CSS overflow.

Use shadcn ScrollArea only where custom scrollbar presentation materially improves the UI.

## Create reusable components

Create or refactor:

- AppShell
- AppSidebar
- MainViewport
- PageShell
- PageHeader
- PageBody
- StickyToolbar
- ScrollableContent
- ScrollablePanel
- DataTableViewport
- HorizontalScroller
- SplitPane
- DetailDrawer
- ScrollableDialog
- KanbanViewport
- TimelineViewport

Reuse these instead of adding arbitrary overflow rules to individual pages.

## Sidebar

Structure:

SidebarHeader — fixed
SidebarNavigation — vertical scroll
SidebarFooter — fixed

The complete sidebar itself must not move with the main page.

## Global header

The top application header must remain visible while page content scrolls.

## Page behavior

Normal pages:
- page header at top
- optional sticky filters/tabs
- primary page body vertical scroll

Large data pages:
- filter toolbar remains accessible
- table viewport supports vertical and horizontal scrolling
- table headers sticky where appropriate

## Tables

Implement:
- horizontal overflow for wide tables
- internal vertical scrolling only when needed
- sticky table headers
- responsive minimum width
- do not compress large tables until unreadable

Apply this to:
- Clients
- Queries
- Projects
- Requirements
- Tickets
- Follow-ups
- Approvals
- Test Cases
- Bugs
- Agent Runs
- Audit Logs
- Users
- Integrations

## Project workspace

Implement:

Project Header
→ Tabs
→ Scrollable active tab content

Tabs should remain accessible during long page content.

## Drawers

Drawer structure:

Header — fixed
Body — scrollable
Footer/actions — fixed

Use for:
- ticket details
- requirement details
- bug details
- follow-up details
- approval details
- agent run details

## Dialogs

Dialogs must use a maximum viewport height.

Header fixed.
Body scrollable.
Footer fixed.

No dialog may extend beyond the visible viewport.

## Split workspaces

Support independent panes where appropriate.

Especially:
- Requirement Gathering
- SRS Review
- Approval Review
- Follow-up workspace
- QA workspace
- Agent Run review

Use CSS Grid/Flex with `min-h-0` and independent `overflow-y-auto`.

## Kanban

Board:
- horizontal scroll

Columns:
- fixed practical width
- shrink-0
- independent vertical scroll

Do not make the complete browser page horizontally scroll.

## Roadmap

Roadmap/timeline:
- horizontal scroll
- vertical page controls remain stable
- support wide phase timelines without compressing data

## Scrollbar styling

Create one global subtle scrollbar style matching the MASMS dark/light theme.

Requirements:
- approximately 8px
- rounded thumb
- transparent track
- muted neutral thumb
- slightly stronger hover state
- no bright colored scrollbar
- preserve browser accessibility

## Sticky behavior

Use sticky elements only where useful:
- page header
- tabs
- filter bar
- table headers
- left labels in very wide roadmaps where appropriate

Avoid excessive sticky layers.

Maintain correct z-index tokens.

## Scroll restoration

Implement logical scroll restoration:

- new unrelated route → top
- drawer/modal open → preserve underlying position
- drawer/modal close → restore position
- detail → back to list → restore list position where practical
- filter changes should not unnecessarily jump the user
- tab changes may reset the new tab body to top

Do not interfere with Next.js/browser behavior unnecessarily.

## Responsive behavior

Desktop:
- sidebar and main viewport independent
- split panes allowed
- table horizontal scrolling
- contextual panels allowed

Tablet:
- collapsed/sidebar drawer
- fewer independent panes

Mobile:
- prioritize one main vertical page scroll
- drawers/sheets independently scroll
- tables horizontally scroll
- avoid several small nested vertical scroll regions

## Accessibility

Ensure:
- keyboard scrolling works
- focus is not trapped unexpectedly
- focus remains visible
- sticky content does not obscure focused controls
- reduced motion is respected
- scrollbar styling remains usable
- touch scrolling works correctly
- use `overscroll-behavior` only where it materially improves UX

## Do not

- add `overflow-auto` randomly everywhere
- create nested scrolling inside every card
- use fixed heights without responsive reasoning
- intercept normal wheel events
- hide scrollbars completely
- create horizontal browser-page scrolling
- break existing responsive layout
- redesign unrelated business functionality
- weaken authorization or workflow behavior

## Migration

Audit the complete frontend for:
- `overflow-*`
- `h-screen`
- `min-h-screen`
- fixed heights
- sticky elements
- tables
- dialogs
- drawers
- sheets
- sidebars
- Kanban layouts
- timeline layouts

Refactor them to use the shared scroll architecture.

## Acceptance criteria

The work is complete when:

1. The application fits within `100dvh`.
2. Browser body does not produce an unnecessary second application scrollbar.
3. Sidebar scrolls independently.
4. Header remains visible.
5. Normal pages scroll smoothly.
6. Large tables support controlled X/Y scrolling.
7. Table headers remain visible where appropriate.
8. Drawers have fixed header/footer and scrollable body.
9. Dialogs never overflow the viewport.
10. Project tabs remain accessible on long screens.
11. Kanban supports horizontal board and vertical columns.
12. Roadmap supports horizontal timeline scrolling.
13. No unwanted horizontal page scroll exists.
14. Mobile behavior remains usable.
15. Keyboard scrolling works.
16. Existing functionality is preserved.
17. Dark/light theme scrollbar appearance is consistent.
18. Lint passes.
19. Type checking passes.
20. Tests pass.
21. Production build passes.

After implementation, provide a report listing:
- shared scroll components created
- pages migrated
- remaining exceptional scroll areas
- sticky components
- mobile behavior verified
- desktop behavior verified
- nested scroll areas
- test results
- lint result
- type-check result
- build result
```

This scrolling system should be implemented **before the project grows much further**, because Clients, Projects, Tickets, Follow-ups, Approvals, QA and Agent Operations will all become data-heavy screens. A common layout foundation now will prevent a lot of UI inconsistencies later.
