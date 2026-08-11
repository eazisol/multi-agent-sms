export type NavItem = {
  href: string;
  label: string;
  badge?: string;
  ready?: boolean;
};

export type NavSection = {
  id: string;
  label: string;
  items: NavItem[];
};

/** Sidebar IA from New UI.md — ready=true for implemented desks. */
export const NAV_SECTIONS: NavSection[] = [
  {
    id: "workspace",
    label: "Workspace",
    items: [
      { href: "/", label: "Dashboard", ready: true },
      { href: "/my-work", label: "My Work", ready: false },
      { href: "/inbox", label: "Inbox", ready: false },
    ],
  },
  {
    id: "bd",
    label: "Business Development",
    items: [
      { href: "/clients", label: "Clients", ready: true },
      { href: "/queries", label: "Queries", ready: true },
      { href: "/opportunities", label: "Opportunities", ready: false },
      { href: "/comms", label: "Messages", ready: true },
    ],
  },
  {
    id: "delivery",
    label: "Project Delivery",
    items: [
      { href: "/projects", label: "Projects", ready: true },
      { href: "/requirements", label: "Requirements", ready: true },
      { href: "/roadmap", label: "Roadmaps", ready: true },
      { href: "/tickets", label: "Tickets", ready: true },
      { href: "/documents", label: "Documents", ready: true },
    ],
  },
  {
    id: "coord",
    label: "Coordination",
    items: [
      { href: "/follow-ups", label: "Follow-ups", ready: true },
      { href: "/approvals", label: "Approvals", ready: true },
    ],
  },
  {
    id: "quality",
    label: "Quality",
    items: [
      { href: "/test-cases", label: "Test Cases", ready: false },
      { href: "/bugs", label: "Bugs", ready: false },
    ],
  },
  {
    id: "ai",
    label: "AI Operations",
    items: [
      { href: "/agents", label: "Agents", ready: false },
      { href: "/agent-runs", label: "Agent Runs", ready: false },
      { href: "/knowledge", label: "Knowledge Base", ready: false },
    ],
  },
  {
    id: "release",
    label: "Delivery",
    items: [
      { href: "/releases", label: "Releases", ready: false },
      { href: "/deployments", label: "Deployments", ready: false },
    ],
  },
  {
    id: "gov",
    label: "Governance",
    items: [
      { href: "/governance/baselines", label: "Source Baselines", ready: true },
      { href: "/architecture-decisions", label: "Architecture Decisions", ready: false },
      { href: "/change-requests", label: "Change Requests", ready: false },
      { href: "/audit-logs", label: "Audit Logs", ready: false },
    ],
  },
  {
    id: "admin",
    label: "Administration",
    items: [
      { href: "/users", label: "Users & Teams", ready: false },
      { href: "/roles", label: "Roles & Permissions", ready: false },
      { href: "/capacity", label: "Skills & Capacity", ready: false },
      { href: "/workflows", label: "Workflows", ready: false },
      { href: "/integrations", label: "Integrations", ready: false },
      { href: "/notifications", label: "Notifications", ready: false },
      { href: "/security", label: "Security", ready: false },
    ],
  },
];

export function findNavLabel(pathname: string): string {
  for (const section of NAV_SECTIONS) {
    for (const item of section.items) {
      if (pathname === item.href || pathname.startsWith(`${item.href}/`)) {
        return item.label;
      }
    }
  }
  return "MASMS";
}
