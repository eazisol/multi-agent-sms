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
      { href: "/insights", label: "Insights", ready: true },
      { href: "/my-work", label: "My Work", ready: true },
      { href: "/inbox", label: "Inbox", ready: true },
    ],
  },
  {
    id: "bd",
    label: "Business Development",
    items: [
      { href: "/clients", label: "Clients", ready: true },
      { href: "/queries", label: "Queries", ready: true },
      { href: "/opportunities", label: "Opportunities", ready: true },
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
      { href: "/test-cases", label: "Test Cases", ready: true },
      { href: "/bugs", label: "Bugs", ready: true },
    ],
  },
  {
    id: "ai",
    label: "AI Operations",
    items: [
      { href: "/agents", label: "Agents", ready: true },
      { href: "/agent-runs", label: "Agent Runs", ready: true },
      { href: "/knowledge", label: "Knowledge Base", ready: true },
    ],
  },
  {
    id: "release",
    label: "Delivery",
    items: [
      { href: "/releases", label: "Releases", ready: true },
      { href: "/deployments", label: "Deployments", ready: true },
    ],
  },
  {
    id: "gov",
    label: "Governance",
    items: [
      { href: "/governance/baselines", label: "Source Baselines", ready: true },
      { href: "/architecture-decisions", label: "Architecture Decisions", ready: true },
      { href: "/change-requests", label: "Change Requests", ready: true },
      { href: "/traceability", label: "Traceability", ready: true },
      { href: "/audit-logs", label: "Audit Logs", ready: true },
    ],
  },
  {
    id: "admin",
    label: "Administration",
    items: [
      { href: "/users", label: "Users & Teams", ready: true },
      { href: "/roles", label: "Roles & Permissions", ready: true },
      { href: "/capacity", label: "Skills & Capacity", ready: true },
      { href: "/workflows", label: "Workflows", ready: true },
      { href: "/integrations", label: "Integrations", ready: true },
      { href: "/gmail", label: "Gmail", ready: true },
      { href: "/jira", label: "Jira", ready: true },
      { href: "/notifications", label: "Notifications", ready: true },
      { href: "/security", label: "Security", ready: true },
      { href: "/reliability", label: "Reliability", ready: true },
      { href: "/uat", label: "UAT", ready: true },
      { href: "/pilot", label: "Pilot", ready: true },
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
