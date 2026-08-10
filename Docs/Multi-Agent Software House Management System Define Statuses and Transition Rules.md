# **Statuses and Transition Rules**

## **General Transition Rules**

All status changes must follow these rules:

* Every change must record the previous status, new status, user or agent, date, reason, and supporting evidence.  
* Agents may perform routine transitions automatically within their approved permissions.  
* Commercial, scope, production, cancellation, and final-completion transitions require human approval.  
* A status cannot be skipped unless an authorized human provides an override reason.  
* Reopening a completed or closed record requires approval and a documented reason.  
* `On Hold`, `Blocked`, `Waiting for Client`, and `Waiting for Response` must include an owner, reason, and follow-up date.  
* SLA timers should pause only when the item is formally waiting on an external party.  
* Terminal statuses cannot move forward without an approved reopening process.

---

# **1\. Client Query Statuses**

## **Standard Flow**

New  
→ Assigned to BD  
→ Requirement Gathering  
→ Waiting for Client  
→ Requirement Gathering  
→ Qualified  
→ Converted to Project  
→ Closed

Alternative outcome:

Requirement Gathering  
→ Not Qualified  
→ Closed

## **Transition Matrix**

| Current Status | Allowed Next Status | Transition Condition |
| ----- | ----- | ----- |
| New | Assigned to BD | A BD Agent or Human BD is selected as the owner. |
| New | Closed | Inquiry is spam, duplicate, invalid, or withdrawn. |
| Assigned to BD | Requirement Gathering | BD acknowledges the inquiry and begins discovery. |
| Assigned to BD | Waiting for Client | Initial response is sent and client input is required. |
| Assigned to BD | Closed | Inquiry is duplicate, invalid, or cancelled. |
| Requirement Gathering | Waiting for Client | Additional answers, files, access, or confirmation are required. |
| Requirement Gathering | Qualified | Requirements, budget fit, service fit, and opportunity criteria are satisfied. |
| Requirement Gathering | Not Qualified | The inquiry does not meet company qualification criteria. |
| Requirement Gathering | Closed | Client withdraws the inquiry or requests closure. |
| Waiting for Client | Requirement Gathering | Client provides the requested information. |
| Waiting for Client | Qualified | Client response completes the required qualification information. |
| Waiting for Client | Not Qualified | Client response confirms the opportunity is not suitable. |
| Waiting for Client | Closed | Client remains unresponsive after the defined follow-up cycle. |
| Qualified | Converted to Project | Proposal, agreement, internal approval, and required payment conditions are complete. |
| Qualified | Requirement Gathering | New information creates additional questions. |
| Qualified | Not Qualified | A later review identifies a disqualifying condition. |
| Qualified | Closed | Client declines or withdraws before project conversion. |
| Not Qualified | Closed | Disqualification is confirmed and documented. |
| Not Qualified | Requirement Gathering | New information justifies reopening the inquiry. |
| Converted to Project | Closed | The inquiry lifecycle is complete and linked to the project. |
| Closed | Assigned to BD | An authorized human reopens the inquiry. |

## **Approval Rules**

* `Qualified`: BD Agent may recommend; Human BD approves when pricing, risk, or strategic review is needed.  
* `Not Qualified`: Human BD approval is recommended for genuine business inquiries.  
* `Converted to Project`: Requires Human BD or PM approval and completion of commercial prerequisites.  
* `Closed → Assigned to BD`: Requires a reopening reason.

## **Required Data by Status**

| Status | Required Information |
| ----- | ----- |
| Assigned to BD | Owner and response SLA |
| Waiting for Client | Required information, follow-up date, and client contact method |
| Qualified | Qualification reason and completeness confirmation |
| Not Qualified | Disqualification reason |
| Converted to Project | Project ID, approved scope or proposal reference |
| Closed | Closure reason |

---

# **2\. Project Statuses**

## **Standard Flow**

Draft  
→ Requirement Review  
→ SRS Preparation  
→ Planning  
→ Design  
→ Development  
→ QA  
→ Client Review  
→ Deployment  
→ Completed

When design is not required:

Planning  
→ Development

Exception flow:

Any Active Status  
→ On Hold  
→ Previous Active Status

Cancellation flow:

Draft / Requirement Review / SRS Preparation / Planning / Design /  
Development / QA / Client Review / Deployment / On Hold  
→ Cancelled

## **Transition Matrix**

| Current Status | Allowed Next Status | Transition Condition |
| ----- | ----- | ----- |
| Draft | Requirement Review | Initial project record and handover information are available. |
| Draft | On Hold | The project cannot proceed temporarily. |
| Draft | Cancelled | The project is withdrawn or rejected. |
| Requirement Review | SRS Preparation | Requirements are sufficiently complete. |
| Requirement Review | Draft | Major information is missing or the project must be restructured. |
| Requirement Review | On Hold | Client, contract, access, or commercial dependency is pending. |
| Requirement Review | Cancelled | The project will not proceed. |
| SRS Preparation | Planning | SRS is approved or baselined for planning. |
| SRS Preparation | Requirement Review | Missing or conflicting requirements are identified. |
| SRS Preparation | On Hold | Required information or approval is unavailable. |
| SRS Preparation | Cancelled | Project cancellation is approved. |
| Planning | Design | UI/UX or design work is required. |
| Planning | Development | Design is not required or already approved. |
| Planning | SRS Preparation | Planning reveals requirement gaps. |
| Planning | On Hold | Resource, timeline, client, or dependency issue blocks progress. |
| Planning | Cancelled | Project cancellation is approved. |
| Design | Development | Required designs are approved and developer-ready. |
| Design | Planning | Design changes affect phase, resources, or delivery planning. |
| Design | SRS Preparation | Design review identifies requirement changes. |
| Design | On Hold | Design feedback or approval is pending. |
| Design | Cancelled | Project cancellation is approved. |
| Development | QA | Development is complete, reviewed, and deployed to a test environment. |
| Development | Design | Implementation requires approved design revision. |
| Development | Planning | A major technical, resource, or scope issue requires replanning. |
| Development | On Hold | Work is blocked at project level. |
| Development | Cancelled | Project cancellation is approved. |
| QA | Client Review | QA has passed and the release candidate is ready. |
| QA | Development | Bugs or failed acceptance criteria require fixes. |
| QA | Design | UI or UX defects require design changes. |
| QA | On Hold | Testing cannot continue. |
| QA | Cancelled | Project cancellation is approved. |
| Client Review | Deployment | Client or Product Owner approves the release. |
| Client Review | Development | Client feedback requires development changes. |
| Client Review | QA | Additional validation or regression testing is required. |
| Client Review | Design | Client requests an approved design correction. |
| Client Review | On Hold | Client decision or feedback is pending. |
| Client Review | Cancelled | Project cancellation is approved. |
| Deployment | Completed | Deployment and post-deployment verification are successful. |
| Deployment | QA | Deployment build requires additional validation. |
| Deployment | Development | Deployment fails because of an application defect. |
| Deployment | On Hold | Release is paused or rolled back pending a decision. |
| Deployment | Cancelled | Release and project cancellation are approved. |
| Completed | Development | Project is formally reopened through an approved change, warranty issue, or critical defect. |
| Completed | QA | Post-release validation is required without new development. |
| On Hold | Previous Active Status | The blocking condition is resolved. |
| On Hold | Cancelled | The project will not resume. |
| Cancelled | Draft | Management authorizes restoration of the cancelled project. |

## **Human Approval Requirements**

Human approval is required for:

* SRS completion and movement to `Planning`.  
* Project baseline and movement from `Planning`.  
* Production movement from `Client Review` to `Deployment`.  
* Movement from `Deployment` to `Completed`.  
* Any transition to `Cancelled`.  
* Reopening `Completed`.  
* Restoring a `Cancelled` project.  
* Moving from `On Hold` back to active work when commercial or contractual issues were involved.

## **On-Hold Rule**

When a project moves to `On Hold`, the system must save:

Previous Status  
Hold Reason  
Responsible Party  
Expected Resume Date  
Follow-Up Owner  
Escalation Date

The project should return to its saved previous status after the hold is resolved.

---

# **3\. Ticket Statuses**

## **Standard Development Flow**

Backlog  
→ Ready  
→ Assigned  
→ In Progress  
→ Code Review  
→ Ready for QA  
→ QA In Progress  
→ Passed QA  
→ Done

Bug-fix loop:

QA In Progress  
→ Failed QA  
→ In Progress  
→ Code Review  
→ Ready for QA  
→ QA In Progress

Blocked flow:

Assigned / In Progress / Code Review / Ready for QA / QA In Progress  
→ Blocked  
→ In Progress / Assigned / Ready for QA

## **Transition Matrix**

| Current Status | Allowed Next Status | Transition Condition |
| ----- | ----- | ----- |
| Backlog | Ready | Ticket meets the Definition of Ready. |
| Ready | Assigned | An appropriate team member is selected. |
| Ready | Backlog | Ticket is deprioritized or no longer ready. |
| Assigned | In Progress | Assignee acknowledges and starts work. |
| Assigned | Ready | Assignment is removed before work starts. |
| Assigned | Blocked | Work cannot start due to a dependency. |
| In Progress | Code Review | Code implementation and developer testing are complete. |
| In Progress | Ready for QA | Non-code work does not require code review. |
| In Progress | Blocked | Progress cannot continue. |
| In Progress | Assigned | Work is reassigned to another team member. |
| Code Review | Ready for QA | Review is approved and required checks pass. |
| Code Review | In Progress | Reviewer requests changes. |
| Code Review | Blocked | Review is blocked by technical or access issues. |
| Ready for QA | QA In Progress | QA accepts and begins testing. |
| Ready for QA | In Progress | Build, evidence, or implementation is incomplete. |
| Ready for QA | Blocked | QA environment or required dependency is unavailable. |
| QA In Progress | Passed QA | Acceptance criteria and required tests pass. |
| QA In Progress | Failed QA | One or more acceptance criteria fail. |
| QA In Progress | Blocked | Testing cannot continue. |
| Failed QA | In Progress | Developer begins corrective work. |
| Failed QA | Assigned | Bug fix is assigned or reassigned. |
| Passed QA | Done | Required QA and TL approvals are complete. |
| Passed QA | QA In Progress | Retesting or regression testing is required. |
| Passed QA | In Progress | A defect is identified before ticket closure. |
| Blocked | In Progress | Existing assignee can resume work. |
| Blocked | Assigned | Ticket must be reassigned. |
| Blocked | Ready | Ticket is unassigned and returned to the ready queue. |
| Blocked | Ready for QA | QA-specific blocker is resolved without development changes. |
| Blocked | Backlog | Ticket is deferred. |
| Done | In Progress | Ticket is formally reopened due to a confirmed defect or incomplete acceptance criterion. |
| Done | QA In Progress | Retesting is required without development changes. |

## **Status Control Rules**

### **Backlog → Ready**

The ticket must have:

* Clear description  
* Requirement reference  
* Acceptance criteria  
* Priority  
* Dependencies  
* Required design or technical information  
* Definition of Done  
* Estimate or sizing

### **Assigned → In Progress**

The assignee must acknowledge:

* Ownership  
* Expected start date  
* Due date  
* Required dependencies

### **In Progress → Code Review**

The ticket must include:

* Pull request  
* Completed implementation  
* Unit-test result  
* Implementation notes  
* No unresolved critical blocker

### **Code Review → Ready for QA**

The ticket must include:

* Approved code review  
* Successful build  
* Required automated tests  
* Test environment or build reference

### **Passed QA → Done**

The ticket must include:

* QA evidence  
* Acceptance criteria results  
* No unresolved blocking defects  
* Required TL or PM approval

## **Human Approval Requirements**

* `Ready`: TL or authorized project owner.  
* `Assigned`: TL or approved assignment automation.  
* `Code Review → Ready for QA`: Human developer or TL reviewer.  
* `Passed QA`: Human QA confirmation for critical or release-facing tickets.  
* `Done`: TL, QA, or PM depending on ticket type.  
* `Done → In Progress`: Requires a reopening reason and authorized approval.

---

# **4\. Follow-Up Statuses**

## **Standard Flow**

Created  
→ Sent  
→ Acknowledged  
→ Waiting for Response  
→ Responded  
→ Resolved  
→ Closed

Escalation flow:

Sent / Acknowledged / Waiting for Response  
→ Overdue  
→ Escalated  
→ Responded  
→ Resolved  
→ Closed

## **Transition Matrix**

| Current Status | Allowed Next Status | Transition Condition |
| ----- | ----- | ----- |
| Created | Sent | Follow-up message or request is delivered. |
| Created | Closed | Follow-up is cancelled before sending. |
| Sent | Acknowledged | Recipient confirms receipt. |
| Sent | Waiting for Response | Delivery is confirmed and a response is required. |
| Sent | Responded | Recipient replies before acknowledgment is separately recorded. |
| Sent | Overdue | Response SLA expires. |
| Acknowledged | Waiting for Response | Recipient has received the request but has not answered. |
| Acknowledged | Responded | Recipient provides the required response. |
| Acknowledged | Overdue | Response SLA expires. |
| Waiting for Response | Responded | Requested information or decision is provided. |
| Waiting for Response | Overdue | Due date passes without sufficient response. |
| Waiting for Response | Escalated | Immediate escalation is required before the SLA expires. |
| Responded | Resolved | The requester confirms that the response satisfies the request. |
| Responded | Waiting for Response | The answer is incomplete and additional information is requested. |
| Responded | Escalated | The response creates a serious issue requiring higher authority. |
| Resolved | Closed | Final verification and records are complete. |
| Resolved | Waiting for Response | The issue is reopened because the resolution is incomplete. |
| Overdue | Escalated | The configured escalation rule is triggered. |
| Overdue | Responded | The recipient responds after the deadline. |
| Overdue | Resolved | The issue is completed without further escalation. |
| Overdue | Closed | The request is cancelled or no longer required. |
| Escalated | Responded | Escalated owner provides a decision or information. |
| Escalated | Resolved | Escalated owner resolves the matter. |
| Escalated | Waiting for Response | Another party must respond after escalation. |
| Escalated | Closed | Management closes or cancels the follow-up. |
| Closed | Waiting for Response | An authorized user reopens the follow-up. |
| Closed | Sent | The same follow-up is reissued with approval. |

## **Required Information by Status**

| Status | Required Information |
| ----- | ----- |
| Created | Sender, recipient, purpose, priority, and due date |
| Sent | Delivery channel and sent timestamp |
| Acknowledged | Acknowledgment timestamp |
| Waiting for Response | Required response and responsible person |
| Responded | Response content and timestamp |
| Resolved | Resolution and verification evidence |
| Overdue | SLA breach duration and missed deadline |
| Escalated | Escalation level, recipient, and reason |
| Closed | Closure reason and closed-by user |

## **Escalation Timing Example**

Created  
→ Sent

After 50% of SLA:  
Reminder Sent

At SLA Deadline:  
Overdue

After Configured Grace Period:  
Escalated to Parent Agent

Still Unresolved:  
Escalated to Corresponding Human Role

Critical or Repeated Delay:  
Escalated to Management

---

# **Transition Permission Summary**

| Transition Type | Agent Authority | Human Authority |
| ----- | ----- | ----- |
| Routine progress movement | May perform automatically | May override |
| Waiting or blocked status | May perform with reason | May resolve or reassign |
| Qualification decision | May recommend | BD approves where required |
| Project stage completion | May recommend | PM, TL, QA, or client approves |
| Ticket assignment | May recommend or assign within policy | TL confirms exceptions |
| QA pass or failure | May record automated results | Human QA confirms release-critical results |
| Production deployment | Cannot approve independently | Authorized human approval required |
| Project cancellation | Cannot approve | PM or management approval required |
| Closing completed records | May close routine items | Human approval required for major records |
| Reopening terminal records | Cannot perform without policy | Authorized human approval required |

# **Terminal and Reopening Rules**

## **Client Query**

* `Closed` is terminal.  
* `Converted to Project` should normally move only to `Closed`.  
* Reopening requires Human BD approval.

## **Project**

* `Completed` and `Cancelled` are terminal.  
* Reopening `Completed` requires an approved change request, warranty issue, or confirmed defect.  
* Restoring `Cancelled` requires management approval.

## **Ticket**

* `Done` is terminal.  
* Reopening requires evidence of a defect, missed acceptance criterion, or approved change.

## **Follow-Up**

* `Closed` is terminal.  
* It may be reopened only when the original request remains relevant and a new response is required.

This structure ensures that every client query, project, ticket, and follow-up follows a controlled and auditable lifecycle without allowing agents to skip approvals or silently change important business states.

