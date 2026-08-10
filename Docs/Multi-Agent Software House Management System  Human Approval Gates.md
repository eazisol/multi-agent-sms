# **Human Approval Gates**

## **1\. Purpose**

Approval gates ensure that AI agents may prepare, analyze, recommend, and coordinate work, but cannot independently make critical commercial, contractual, technical, quality, or production decisions.

Every approval must identify:

* What is being approved  
* Current document or record version  
* Requesting agent or human  
* Authorized approver  
* Required supporting evidence  
* Approval deadline  
* Decision and comments  
* Approval date  
* Any conditions attached to the approval  
* Complete audit history

---

# **2\. Standard Approval Lifecycle**

Draft Created  
→ Submitted for Review  
→ Assigned to Approver  
→ Acknowledged  
→ Under Review  
→ More Information Required  
→ Resubmitted  
→ Approved / Rejected  
→ Applied to Workflow  
→ Closed

Possible approval statuses:

Draft  
Pending Submission  
Pending Approval  
Under Review  
More Information Required  
Approved  
Approved with Conditions  
Rejected  
Withdrawn  
Expired  
Superseded  
Closed

An approval should be applied only to the exact version reviewed by the approver.

---

# **3\. Approval Authority Levels**

| Level | Authority |
| ----- | ----- |
| Level 1 | Routine operational approval within an assigned project |
| Level 2 | Department-level approval |
| Level 3 | Cross-department, commercial, or client-impacting approval |
| Level 4 | Production, security, major financial, or company-level approval |
| Level 5 | Executive, contractual, legal, or exceptional-risk approval |

Agents may submit and track approval requests but cannot act as final human approvers.

---

# **4\. Approval Gate Matrix**

| Approval Gate | Prepared By | Required Internal Approver | External Approval | Minimum Level |
| ----- | ----- | ----- | ----- | ----- |
| Final project scope | PM Agent / Human PM | Human PM and Human TL | Client/Product Owner | Level 3 |
| Quotation | BD Agent / Human BD | Sales Manager or Management | Client acceptance | Level 4 |
| Timeline commitment | PM Agent and TL Agent | Human PM and Human TL | Client where committed | Level 3 |
| SRS approval | PM Agent | Human PM, TL, and QA Lead | Client/Product Owner | Level 3 |
| Resource allocation | TL Agent / PM Agent | Human TL and Human PM | None normally | Level 2 |
| Major architecture decision | TL Agent | Technical Architect, Engineering Manager, or CTO | Client when it affects scope/cost | Level 4 |
| Change request | PM Agent | Human PM and TL; Management if commercial impact | Client/Product Owner | Level 3–4 |
| Production deployment | DevOps Agent / TL Agent | QA Lead, TL, PM or Release Manager | Client where required | Level 4 |
| Client delivery | PM Agent | Human PM, TL, and QA Lead | Client acknowledgment | Level 3 |
| Project closure | PM Agent | Human PM, TL, QA, BD, and Finance where applicable | Client acceptance | Level 4 |

---

# **5\. Final Project Scope Approval**

## **Trigger**

The requirements have been reviewed and the proposed in-scope and out-of-scope items are ready for baseline approval.

## **Prepared By**

* PM Agent  
* Human Project Manager

## **Required Reviewers**

* Human Business Developer  
* Human Team Lead  
* QA Lead  
* Designer or DevOps Lead where applicable

## **Authorized Approvers**

### **Internal**

* Human Project Manager  
* Human Team Lead

### **External**

* Client Product Owner  
* Client Sponsor  
* Authorized Client Approver

## **Required Evidence**

* Requirement brief  
* In-scope list  
* Out-of-scope list  
* Assumptions  
* Constraints  
* Dependencies  
* High-level timeline  
* Identified risks  
* Client confirmation  
* Related proposal version

## **Approval Conditions**

The scope may be approved only when:

* Required features are clearly documented.  
* Exclusions are clearly stated.  
* Open questions are either resolved or accepted as assumptions.  
* Technical feasibility has been reviewed.  
* Client approval authority is verified.

## **After Approval**

Scope Approved  
→ Scope Baseline Created  
→ SRS Preparation or Finalization  
→ Requirement Changes Require Change Request

## **Rejection Outcome**

Scope Rejected  
→ Rejection Reason Recorded  
→ Returned to Requirement Gathering  
→ Revised Scope Resubmitted

---

# **6\. Quotation Approval**

## **Trigger**

The project scope, effort estimate, pricing model, and commercial terms are ready.

## **Prepared By**

* BD Agent  
* Human Business Developer  
* PM Agent for delivery inputs  
* TL Agent for effort inputs

## **Authorized Approvers**

| Quotation Type | Required Approver |
| ----- | ----- |
| Within standard approved pricing | Sales Manager or authorized Human BD |
| Discounted quotation | Sales Manager and Management |
| Large fixed-price project | Management or Company Owner |
| Non-standard payment terms | Finance and Management |
| High-risk or urgent delivery | PM, TL, and Management |
| Contractually sensitive quotation | Management and Legal representative |

## **Required Evidence**

* Approved scope  
* Effort estimate  
* Role allocation  
* Risk contingency  
* Timeline estimate  
* Pricing calculation  
* Payment schedule  
* Assumptions  
* Proposal validity period  
* Third-party costs  
* Discount reason, when applicable

## **Approval Rules**

Agents cannot:

* Confirm rates  
* Apply discounts  
* Send final pricing  
* Change payment terms  
* Promise commercial concessions

## **After Approval**

Quotation Approved  
→ Proposal Version Locked  
→ Sent to Client by Authorized BD  
→ Client Acceptance Tracked

---

# **7\. Timeline Commitment Approval**

## **Trigger**

The project schedule is ready to be communicated as an official client commitment.

## **Prepared By**

* PM Agent  
* TL Agent

## **Required Approvers**

* Human Team Lead for technical estimates  
* Human Project Manager for delivery planning  
* Department Manager when resource conflicts exist  
* Management when the deadline creates exceptional risk

## **Required Evidence**

* Phase estimates  
* Team availability  
* Dependencies  
* Design allocation  
* Development allocation  
* QA allocation  
* Deployment allocation  
* Risk contingency  
* Client dependencies  
* Holiday and working-calendar impact  
* Critical path

## **Approval Conditions**

A timeline should not be approved when:

* Requirements remain materially incomplete.  
* Required resources are unavailable.  
* Important third-party access is missing.  
* The estimate excludes QA or deployment.  
* Major technical risks remain unassessed.

## **After Approval**

Timeline Approved  
→ Baseline Schedule Created  
→ Milestones Published  
→ Client Commitment Sent

Any later change to the approved timeline must be recorded through a project-impact or change-request process.

---

# **8\. SRS Approval**

## **Trigger**

The SRS has been prepared, reviewed, and is ready to become the authoritative project specification.

## **Prepared By**

* PM Agent  
* Human PM or Business Analyst

## **Required Internal Approvers**

* Human PM: business scope and completeness  
* Human TL: technical feasibility  
* QA Lead: testability and acceptance criteria  
* Design Lead: UI/UX requirements, when applicable  
* Security Lead: security requirements, when required

## **Required External Approver**

* Client Product Owner  
* Client Sponsor  
* Authorized Client Approver

## **Required Evidence**

* Functional requirements  
* Non-functional requirements  
* User roles  
* User flows  
* Validation rules  
* Business rules  
* Integrations  
* Acceptance criteria  
* Traceability matrix  
* Open assumptions  
* Version history

## **Approval Sequence**

PM Review  
→ TL Technical Review  
→ QA Testability Review  
→ Internal Approval  
→ Client Review  
→ Client Approval  
→ SRS Baseline

## **After Approval**

* The approved version becomes read-only.  
* New changes require a new version.  
* Material changes require an approved change request.  
* Tickets must reference the approved requirement IDs.

---

# **9\. Resource Allocation Approval**

## **Trigger**

Team members or agents need to be allocated to a project, phase, or set of tickets.

## **Prepared By**

* TL Agent  
* PM Agent

## **Authorized Approvers**

| Allocation Type | Approver |
| ----- | ----- |
| Normal assignment within available capacity | Human TL |
| Project-level allocation | Human TL and PM |
| Cross-project movement | PMs and Department Manager |
| Overtime or weekend work | Department Manager and Management |
| New external contractor | Management or HR/Operations |
| Critical production support | TL, PM, and DevOps Lead |
| Agent execution budget increase | System Admin and Management |

## **Required Evidence**

* Required skill  
* Suggested person or agent  
* Availability  
* Current workload  
* Allocation percentage  
* Duration  
* Expected deliverables  
* Cost impact  
* Replacement or backup resource  
* Conflict analysis

## **Approval Conditions**

The system should prevent allocation when:

* Capacity is unavailable.  
* Required skills do not match.  
* The user lacks project access.  
* Working hours conflict with the deadline.  
* The allocation exceeds authorized limits.

---

# **10\. Major Architecture Decision Approval**

## **Trigger**

A decision materially affects technology, infrastructure, security, scalability, cost, or maintainability.

## **Examples**

* Changing the main backend framework  
* Introducing microservices  
* Selecting a new cloud provider  
* Changing the primary database  
* Adding a major third-party platform  
* Changing authentication architecture  
* Introducing sensitive AI processing  
* Changing data residency  
* Major database redesign  
* High-cost infrastructure changes

## **Prepared By**

* TL Agent  
* Human Team Lead  
* Technical Architect

## **Required Approvers**

* Technical Architect or Engineering Manager  
* CTO for major or organization-wide decisions  
* Security Lead for security-sensitive changes  
* DevOps Lead for infrastructure changes  
* PM for timeline and scope impact  
* Management for material cost impact  
* Client when contract, scope, cost, or data handling changes

## **Required Evidence**

* Architecture decision record  
* Problem statement  
* Options considered  
* Recommended option  
* Benefits and disadvantages  
* Security impact  
* Performance impact  
* Cost impact  
* Migration impact  
* Timeline impact  
* Risks  
* Rollback or reversal approach

## **After Approval**

The system should create an immutable Architecture Decision Record linked to affected projects, requirements, and tickets.

---

# **11\. Change Request Approval**

## **Trigger**

A requested change affects approved requirements, scope, cost, design, delivery, or technical architecture.

## **Prepared By**

* PM Agent  
* Human PM

## **Required Reviewers**

* Human TL  
* Relevant developers  
* QA Lead  
* Designer  
* DevOps  
* Human BD  
* Finance where cost is affected

## **Authorized Approvers**

| Impact | Required Approval |
| ----- | ----- |
| No scope, cost, or timeline impact | PM and TL |
| Minor timeline impact | PM, TL, and Client Product Owner |
| Cost impact | PM, BD/Finance, Management, and Client |
| Major architecture impact | Technical Architect/CTO and PM |
| Security impact | Security Lead/CTO |
| Production emergency | Authorized incident manager with retrospective approval |

## **Required Evidence**

* Current approved requirement  
* Requested change  
* Business reason  
* Technical impact  
* Design impact  
* QA impact  
* Timeline impact  
* Cost impact  
* Resource impact  
* Risk impact  
* Recommended action

## **Approval Outcomes**

Approved  
Rejected  
Deferred  
More Information Required  
Withdrawn

No normal development work should begin until the request is approved.

---

# **12\. Production Deployment Approval**

## **Trigger**

The release candidate is technically ready for production.

## **Prepared By**

* DevOps Agent  
* TL Agent  
* Human DevOps Engineer

## **Mandatory Approval Sequence**

Development Complete  
→ Code Review Approved  
→ QA Passed  
→ Known Issues Reviewed  
→ TL Technical Approval  
→ PM/Release Manager Approval  
→ Client Approval When Required  
→ Production Deployment Authorized

## **Authorized Approvers**

* Human QA Lead for quality sign-off  
* Human TL for technical readiness  
* Human PM or Release Manager for release authorization  
* Client Product Owner when contractually required  
* DevOps Lead for operational execution  
* Security Lead for security-sensitive releases

## **Required Evidence**

* Release notes  
* QA report  
* Open-bug list  
* Accepted known issues  
* Deployment checklist  
* Backup confirmation  
* Migration plan  
* Rollback plan  
* Monitoring plan  
* Approved release window  
* Environment verification

## **Critical Rule**

The DevOps Agent may prepare or execute approved automation but cannot authorize the production deployment itself.

## **Rejection Outcome**

Deployment Rejected  
→ Reason Recorded  
→ Returned to Development / QA / DevOps  
→ Corrective Action Completed  
→ Resubmitted for Approval

---

# **13\. Client Delivery Approval**

## **Trigger**

A milestone, release, phase, or project deliverable is ready to be presented to the client.

## **Prepared By**

* PM Agent  
* Human PM  
* BD Agent for client-facing communication

## **Internal Approvers**

* Human TL confirms technical completion.  
* QA Lead confirms quality status.  
* Human PM confirms scope completion.  
* Human BD approves client-facing communication.

## **External Approver**

* Client Product Owner  
* Client Sponsor  
* Authorized Client Reviewer

## **Required Evidence**

* Delivered items  
* Acceptance criteria results  
* QA report  
* Release notes  
* User documentation  
* Known issues  
* Demonstration or test link  
* Client review instructions  
* Response deadline

## **Approval Outcomes**

Accepted  
Accepted with Minor Conditions  
Rejected with Feedback  
More Information Required  
Deferred

Client rejection must create linked corrective tickets or a formal change request, depending on whether the feedback is inside the approved scope.

---

# **14\. Project Closure Approval**

## **Trigger**

All approved work is delivered, accepted, deployed, and ready for administrative closure.

## **Prepared By**

* PM Agent  
* Human Project Manager

## **Required Internal Approvers**

* Human PM  
* Human TL  
* QA Lead  
* Human BD  
* DevOps Lead when production deployment is included  
* Finance when commercial closure is required  
* Support or Maintenance Owner

## **Required External Approver**

* Client Product Owner or Sponsor

## **Required Evidence**

* Completed requirement traceability  
* Closed or accepted tickets  
* QA sign-off  
* Production deployment confirmation  
* Client acceptance  
* Documentation delivery  
* Source-code handover where applicable  
* Access and credential handover reference  
* Open known issues  
* Support and warranty plan  
* Final commercial status  
* Lessons learned  
* Project completion report

## **Closure Conditions**

A project may close only when:

* No unresolved critical issue exists.  
* Required client acceptance is recorded.  
* Support ownership is assigned.  
* Final documents are stored.  
* Open issues have approved disposition.  
* Commercial exceptions are documented.  
* Project records and audit history are complete.

## **After Approval**

Project Closure Approved  
→ Project Status Changed to Completed  
→ Active Workflows Closed  
→ Support or Maintenance Activated  
→ Project Archived According to Policy

---

# **15\. Additional Recommended Approval Gates**

The following approvals are also recommended.

| Activity | Authorized Approver |
| ----- | ----- |
| Requirement brief | Human BD and PM |
| Proposal submission | Human BD or Sales Manager |
| Project handover acceptance | Human PM and TL |
| Project baseline | Human PM |
| Design approval | Design Lead, PM, and Client |
| Ticket readiness | Human TL |
| Code merge | Assigned reviewer or Human TL |
| QA waiver | QA Lead, PM, and Management |
| Acceptance of critical known issue | QA Lead, TL, PM, and Client |
| Project hold | Human PM |
| Project cancellation | Management and Client where required |
| Production rollback | DevOps Lead, TL, and PM |
| Security exception | Security Lead or CTO |
| Pricing discount | Sales Manager or Management |
| Agent permission expansion | System Admin and Department Owner |
| Knowledge-base publication | Knowledge Owner and Authorized Approver |

---

# **16\. Approval Authority Configuration**

Approval authority must be configurable by:

Organization  
Department  
Role  
Named User  
Project  
Client  
Approval Type  
Financial Threshold  
Risk Level  
Environment  
Change Impact  
Effective Date  
Expiry Date  
Delegation Status

Example:

{  
  "approval\_type": "production\_deployment",  
  "project\_id": "PRJ-001",  
  "authorized\_roles": \[  
    "qa\_lead",  
    "team\_lead",  
    "release\_manager"  
  \],  
  "minimum\_approvals": 3,  
  "sequential": true,  
  "environment": "production",  
  "delegation\_allowed": false,  
  "effective\_from": "2026-08-01",  
  "expires\_at": null  
}

---

# **17\. Sequential and Parallel Approvals**

## **Sequential Approval**

Used when one decision depends on a previous decision.

TL Approval  
→ QA Approval  
→ PM Approval  
→ Client Approval  
→ Deployment Authorization

## **Parallel Approval**

Used when several departments can review independently.

PM Review  
\+  
TL Review  
\+  
QA Review  
→ All Mandatory Reviews Completed  
→ Final Approval

The workflow configuration should define whether:

* All approvers are required.  
* A minimum number of approvals is sufficient.  
* One rejection stops the process.  
* The approval returns for correction.  
* Approvers must act in sequence.

---

# **18\. Delegation Rules**

Human approvers may delegate authority only when allowed by policy.

Every delegation must record:

* Original approver  
* Delegate  
* Approval type  
* Project or department  
* Effective date  
* Expiry date  
* Maximum authority  
* Delegation reason  
* Management approval where required

Delegation should not normally be allowed for:

* Major financial approval  
* Security exceptions  
* Production incidents of the highest severity  
* Contractual commitments  
* Executive-level approvals

---

# **19\. Approval SLA and Escalation**

| Approval Type | Default Response Time |
| ----- | ----- |
| Routine internal approval | 4 working hours |
| Project scope | 1 business day |
| SRS internal approval | 2 business days |
| Client approval | 3 business days |
| Change request | 2 business days |
| Production deployment | Before release window |
| Critical rollback | Immediate |
| Project closure | 3 business days |

Default escalation flow:

Approval Requested  
→ Reminder at 50% of SLA  
→ Overdue at SLA Deadline  
→ Escalated to Approver’s Manager  
→ Escalated to Department Head  
→ Escalated to Management

---

# **20\. Approval Data Structure**

Each approval record should contain:

Approval ID  
Approval Type  
Project ID  
Target Entity Type  
Target Entity ID  
Target Version  
Requested By  
Requested At  
Approver Role  
Assigned Approver  
Approval Sequence  
Mandatory / Optional  
Due Date  
Acknowledged At  
Decision  
Decision Comments  
Conditions  
Evidence  
Decided At  
Applied At  
Escalation Level  
Delegated From  
Status  
Created At  
Updated At

Supporting tables should include:

approval\_workflows  
approval\_steps  
approval\_requests  
approval\_decisions  
approval\_evidence  
approval\_delegations  
approval\_escalations  
approval\_history

---

# **21\. System Enforcement Rules**

The system must:

1. Prevent agents from approving human-controlled actions.  
2. Verify the approver’s active authority.  
3. Verify project and department access.  
4. Lock the exact version submitted for approval.  
5. Prevent changes while approval is in progress, or create a new version.  
6. Record every decision and comment.  
7. Reject expired approval authority.  
8. Trigger reminders and escalations.  
9. Prevent deployment, delivery, or closure when mandatory approvals are missing.  
10. Clearly distinguish agent recommendations from human decisions.  
11. Require a rejection reason.  
12. Require new approval when an approved document materially changes.  
13. Retain all previous approval records.  
14. Support emergency approval procedures with retrospective review.  
15. Display approval status on all relevant project records.

The central rule should be:

Agents Prepare and Recommend  
→ Authorized Humans Review and Decide  
→ System Verifies Authority  
→ Approved Decision Is Applied  
→ Complete History Is Retained

