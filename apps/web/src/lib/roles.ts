/** Governance UI role variants — mirrors docs/governance/UI_ROLE_VARIANTS.md (client UX only). */

export type GovVariant =
  | "gov.viewer"
  | "gov.contributor"
  | "gov.adr_approver"
  | "gov.baseline_approver"
  | "gov.cr_approver"
  | "gov.admin"
  | "gov.agent_drafter";

export type ActorKind = "human" | "agent" | "system" | "integration";

export type BaselineAction =
  | "view_list"
  | "view_detail"
  | "create"
  | "edit_draft"
  | "submit"
  | "approve"
  | "reject"
  | "supersede";

const MATRIX: Record<GovVariant, Record<BaselineAction, "A" | "D" | "H">> = {
  "gov.viewer": {
    view_list: "A",
    view_detail: "A",
    create: "H",
    edit_draft: "H",
    submit: "H",
    approve: "H",
    reject: "H",
    supersede: "H",
  },
  "gov.contributor": {
    view_list: "A",
    view_detail: "A",
    create: "A",
    edit_draft: "A",
    submit: "A",
    approve: "H",
    reject: "H",
    supersede: "H",
  },
  "gov.adr_approver": {
    view_list: "A",
    view_detail: "A",
    create: "A",
    edit_draft: "A",
    submit: "A",
    approve: "H",
    reject: "H",
    supersede: "H",
  },
  "gov.baseline_approver": {
    view_list: "A",
    view_detail: "A",
    create: "A",
    edit_draft: "A",
    submit: "A",
    approve: "A",
    reject: "A",
    supersede: "A",
  },
  "gov.cr_approver": {
    view_list: "A",
    view_detail: "A",
    create: "A",
    edit_draft: "A",
    submit: "A",
    approve: "D",
    reject: "D",
    supersede: "D",
  },
  "gov.admin": {
    view_list: "A",
    view_detail: "A",
    create: "A",
    edit_draft: "A",
    submit: "A",
    approve: "A",
    reject: "A",
    supersede: "A",
  },
  "gov.agent_drafter": {
    view_list: "A",
    view_detail: "A",
    create: "A",
    edit_draft: "A",
    submit: "A",
    approve: "H",
    reject: "H",
    supersede: "H",
  },
};

export const VARIANT_OPTIONS: { id: GovVariant; label: string }[] = [
  { id: "gov.viewer", label: "Viewer" },
  { id: "gov.contributor", label: "Contributor" },
  { id: "gov.baseline_approver", label: "Baseline Approver" },
  { id: "gov.admin", label: "Admin" },
  { id: "gov.agent_drafter", label: "Agent (draft only)" },
];

export function actorKindForVariant(variant: GovVariant): ActorKind {
  return variant === "gov.agent_drafter" ? "agent" : "human";
}

export function can(variant: GovVariant, action: BaselineAction): boolean {
  return MATRIX[variant][action] === "A";
}

export function isDisabled(variant: GovVariant, action: BaselineAction): boolean {
  return MATRIX[variant][action] === "D";
}

export function isHidden(variant: GovVariant, action: BaselineAction): boolean {
  return MATRIX[variant][action] === "H";
}
