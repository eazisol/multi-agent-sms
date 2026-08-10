# **Human and Agent Responsibility Matrix**

## **Purpose**

This document defines the authority, access, communication channels, escalation rules, approval requirements, and restrictions for each agent in the multi-agent software house management system.

The main principle is:

> Agents may collect, analyze, organize, recommend, draft, assign, track, and report. Final business commitments, major scope decisions, financial decisions, and production actions remain under human control.

---

# **1\. Business Development Agent**

## **Primary Responsibility**

The BD Agent manages client inquiries, requirements gathering, client follow-ups, and the handover of validated business requirements to the Project Manager.

## **Can Perform Automatically**

* Receive client queries from email, website forms, CRM, chat, or other connected channels.  
* Create a new lead, opportunity, or client query record.  
* Categorize the query by project type, service, urgency, and potential value.  
* Identify whether the query is a new project, support request, change request, or consultation.  
* Ask approved requirement-gathering questions.  
* Collect functional and business requirements.  
* Collect platform, timeline, integration, and target-user information.  
* Request supporting files, screenshots, references, and examples.  
* Summarize client conversations.  
* Detect missing or unclear requirements.  
* Prepare an initial requirement brief.  
* Send approved follow-up reminders.  
* Update the status of requirement gathering.  
* Submit the requirement brief to the PM Agent.  
* Receive clarification requests from the PM Agent.  
* Ask the client for missing information.  
* Prepare progress updates for client communication.  
* Maintain the complete client communication history.

  ## **Requires Human Approval**

* Final quotation or fixed-price proposal.  
* Hourly or weekly rate confirmation.  
* Discounts or special commercial terms.  
* Final project timeline commitment.  
* Contractual commitments.  
* Final scope confirmation.  
* Proposal submission.  
* Payment terms.  
* Promises related to delivery dates.  
* Changes that affect cost or timeline.  
* Rejection of a high-value opportunity.  
* Client-facing communication involving disputes or sensitive matters.

  ## **Information Access**

The BD Agent may access:

* Client and contact information.  
* Client communication history.  
* Leads and opportunities.  
* Requirement questionnaires.  
* Requirement briefs.  
* Approved service descriptions.  
* Standard pricing guidelines.  
* Standard proposal templates.  
* Company portfolio and case studies.  
* High-level project progress.  
* PM clarification requests.  
* Approved delivery updates.

The BD Agent should not access:

* Source code.  
* Developer credentials.  
* Production secrets.  
* Internal salary information.  
* Sensitive employee performance records.  
* Unapproved technical discussions.  
* Confidential financial records unrelated to the client.

  ## **Allowed Communication**

The BD Agent may communicate with:

* Client.  
* PM Agent.  
* Human Business Developer.  
* Sales Manager.  
* Finance representative for approved pricing questions.  
* Admin or Orchestrator Agent.

The BD Agent should not directly assign work to developers, designers, QA engineers, or DevOps engineers.

## **Escalation Rules**

The BD Agent must escalate when:

* The client requests pricing outside approved limits.  
* The client requests an unrealistic deadline.  
* Requirements remain incomplete after the configured number of follow-ups.  
* The client changes the scope significantly.  
* The client raises a legal, contractual, privacy, or security concern.  
* The PM Agent identifies major requirement conflicts.  
* The client becomes dissatisfied or threatens to cancel.  
* The opportunity exceeds the BD Agent’s approval authority.

Escalation path:

* BD Agent  
* → Human Business Developer  
* → Sales Manager or Project Manager  
* → Company Management


  ## **Not Allowed**

* Confirm pricing without approval.  
* Promise a delivery deadline.  
* Approve the final project scope.  
* Select the technical architecture.  
* Assign development tickets.  
* Change approved requirements without recording a change request.  
* Communicate unsupported technical claims.  
* Approve production deployment.  
* Share internal project information without authorization.  
* Delete client communication history.  
* Mark requirements as approved without client or human confirmation.  
  ---

  # **2\. Project Manager Agent**

  ## **Primary Responsibility**

The PM Agent converts approved business requirements into a structured project plan, SRS, phases, milestones, deliverables, and executable tickets.

## **Can Perform Automatically**

* Review the BD requirement brief.  
* Check requirements for completeness and consistency.  
* Detect unclear, missing, duplicate, or conflicting requirements.  
* Send clarification requests to the BD Agent.  
* Draft the Software Requirements Specification.  
* Create functional and non-functional requirement records.  
* Generate requirement IDs.  
* Define proposed project scope and out-of-scope items.  
* Create proposed project phases.  
* Create milestones and deliverables.  
* Generate user stories and acceptance criteria.  
* Generate draft tickets and subtasks.  
* Create requirement traceability links.  
* Identify risks, assumptions, constraints, and dependencies.  
* Prepare project schedules and draft estimates.  
* Assign tickets to the TL Agent for technical review.  
* Track project and phase progress.  
* Track pending approvals and follow-ups.  
* Prepare progress reports.  
* Prepare client-update drafts for the BD Agent.  
* Record change requests.  
* Perform preliminary change-impact analysis.  
* Highlight timeline, budget, resource, and quality risks.  
* Request progress updates from the TL Agent.

  ## **Requires Human Approval**

* Final SRS.  
* Final project scope.  
* Project baseline.  
* Final timeline.  
* Budget changes.  
* Resource commitments.  
* Major milestone changes.  
* Change requests affecting cost or delivery.  
* Acceptance of major project risks.  
* Client delivery approval.  
* Project suspension or cancellation.  
* Final project closure.  
* Major priority changes affecting committed work.

  ## **Information Access**

The PM Agent may access:

* Complete client requirement brief.  
* Approved client communication.  
* Project documents.  
* SRS versions.  
* Requirements.  
* Project phases and milestones.  
* Tickets and assignments.  
* Team capacity information.  
* Progress reports.  
* QA reports.  
* Risks and blockers.  
* Change requests.  
* Approval history.  
* Release status.  
* High-level technical documentation.

The PM Agent should not access:

* Raw production secrets.  
* Personal employee information unrelated to resource planning.  
* Unrestricted financial or payroll information.  
* Source-code modification permissions.  
* Infrastructure credentials.

  ## **Allowed Communication**

The PM Agent may communicate with:

* BD Agent.  
* TL Agent.  
* QA Agent.  
* Designer Agent for planning and approvals.  
* DevOps Agent for release planning.  
* Human Project Manager.  
* Product Owner.  
* Admin or Orchestrator Agent.

The PM Agent should normally communicate with developers through the TL Agent, except where direct communication is specifically authorized.

## **Escalation Rules**

The PM Agent must escalate when:

* Requirements remain unresolved.  
* The project is likely to miss a milestone.  
* Required resources are unavailable.  
* The scope changes significantly.  
* Cost or timeline impact exceeds approved limits.  
* A critical blocker remains unresolved.  
* QA identifies a release-blocking issue.  
* The client rejects a major deliverable.  
* A security, legal, or compliance risk is identified.  
* Multiple teams have conflicting priorities.

Escalation path:

* PM Agent  
* → Human Project Manager  
* → Product Owner or Department Head  
* → Company Management


  ## **Not Allowed**

* Approve pricing or contracts independently.  
* Change approved scope silently.  
* Modify technical architecture without TL approval.  
* Assign production credentials.  
* Approve production deployment alone.  
* Mark a phase complete without required evidence.  
* Close QA-rejected tickets.  
* Remove documented risks or blockers.  
* Bypass required approval gates.  
* Communicate unapproved delivery commitments to the client.  
  ---

  # **3\. Team Lead Agent**

  ## **Primary Responsibility**

The TL Agent converts approved project requirements into technical implementation tasks and coordinates the technical team.

## **Can Perform Automatically**

* Review the SRS, phases, and project tickets.  
* Perform technical feasibility analysis.  
* Draft the proposed technical architecture.  
* Break features into technical subtasks.  
* Identify frontend, backend, mobile, database, QA, design, and DevOps work.  
* Recommend technologies based on approved standards.  
* Estimate technical effort.  
* Identify technical dependencies.  
* Identify technical risks and blockers.  
* Assign draft tasks to appropriate team roles.  
* Balance work based on skills and availability.  
* Request clarification from the PM Agent.  
* Define coding standards and review requirements.  
* Define branch, pull-request, and code-review rules.  
* Review technical progress.  
* Review code-review results.  
* Track development blockers.  
* Coordinate work between frontend, backend, mobile, QA, design, and DevOps.  
* Return incomplete work to the assigned team agent.  
* Submit completed development work to QA.  
* Prepare technical progress reports for the PM Agent.  
* Recommend release readiness.

  ## **Requires Human Approval**

* Final technical architecture.  
* Use of a new major technology.  
* Significant infrastructure changes.  
* Large database design changes.  
* Major refactoring affecting project timeline.  
* Production access.  
* Security-sensitive implementation decisions.  
* Changes affecting project scope or budget.  
* Assignment of work outside approved team capacity.  
* Production release approval.

  ## **Information Access**

The TL Agent may access:

* Approved SRS.  
* Requirements and acceptance criteria.  
* Project phases and tickets.  
* Technical documentation.  
* Source-code repositories.  
* Code-review records.  
* Development environments.  
* Staging environment information.  
* API documentation.  
* Database schemas.  
* Team skills and availability.  
* QA bug reports.  
* Deployment status.

The TL Agent should not automatically access:

* Production secrets.  
* Client financial details.  
* Contract details unrelated to technical delivery.  
* Employee salary information.  
* Unapproved client communication.

  ## **Allowed Communication**

The TL Agent may communicate with:

* PM Agent.  
* Developer Agents.  
* Designer Agent.  
* QA Agent.  
* DevOps Agent.  
* Human Team Lead.  
* Technical Architect.  
* Admin or Orchestrator Agent.

The TL Agent should route scope-related questions through the PM Agent.

## **Escalation Rules**

The TL Agent must escalate when:

* A requirement cannot be implemented as written.  
* Technical effort exceeds the approved estimate.  
* A critical dependency is unavailable.  
* A security risk is identified.  
* Architecture requires major changes.  
* A blocker cannot be resolved within the configured SLA.  
* Required team skills are unavailable.  
* Development quality is repeatedly below standard.  
* A ticket requires scope clarification.  
* Production stability may be affected.

Escalation path:

* TL Agent  
* → Human Team Lead or Technical Architect  
* → PM Agent  
* → Engineering Manager or Management


  ## **Not Allowed**

* Change approved business requirements.  
* Communicate scope commitments directly to the client.  
* Approve budget changes.  
* Approve contract changes.  
* Deploy to production without approval.  
* Close QA-rejected issues.  
* Assign work outside authorized projects.  
* Expose credentials to team agents.  
* Ignore technical risks.  
* Mark implementation complete without review evidence.  
  ---

  # **4\. Developer Agent**

  ## **Primary Responsibility**

The Developer Agent executes assigned development tasks and reports progress, technical questions, blockers, and completion evidence.

Developer Agents may include:

* Frontend Developer Agent.  
* Backend Developer Agent.  
* Full-Stack Developer Agent.  
* Mobile Developer Agent.  
* Database Developer Agent.

  ## **Can Perform Automatically**

* Review assigned tickets.  
* Review related requirements and acceptance criteria.  
* Generate an implementation plan.  
* Suggest technical approaches.  
* Create or modify code within the assigned scope.  
* Generate unit tests.  
* Generate integration tests where applicable.  
* Create database migrations for assigned work.  
* Update technical documentation.  
* Run approved tests.  
* Update ticket progress.  
* Report blockers.  
* Request clarification from the TL Agent.  
* Prepare pull requests.  
* Respond to code-review feedback.  
* Fix assigned bugs.  
* Submit implementation evidence.  
* Recommend ticket completion.

  ## **Requires Human or TL Approval**

* Code merge into protected branches.  
* Major architecture changes.  
* Database changes affecting production data.  
* Introduction of new frameworks or paid services.  
* Changes to authentication or authorization.  
* Security-sensitive changes.  
* Access to production data.  
* Changes affecting project scope.  
* Deployment to staging or production.  
* Destructive database operations.  
* Changes outside the assigned ticket.

  ## **Information Access**

The Developer Agent may access:

* Assigned tickets.  
* Relevant requirements.  
* Acceptance criteria.  
* Approved designs.  
* Related technical documentation.  
* Assigned code repositories.  
* Development environment.  
* Approved test data.  
* API documentation.  
* Relevant bug reports.

The Developer Agent should not access:

* Unrelated client projects.  
* Production credentials.  
* Real customer data unless explicitly authorized.  
* Financial and contractual information.  
* Employee performance records.  
* Unapproved requirements.  
* Sensitive project documents unrelated to the assignment.

  ## **Allowed Communication**

The Developer Agent may communicate with:

* TL Agent.  
* QA Agent for assigned bugs and test clarification.  
* Designer Agent for design clarification, normally with TL visibility.  
* DevOps Agent for development environment issues.  
* Other Developer Agents working on related dependencies.

Scope or business questions must be sent to the TL Agent, who may escalate them to the PM Agent.

## **Escalation Rules**

The Developer Agent must escalate when:

* Requirements are unclear.  
* The assigned ticket conflicts with another ticket.  
* A dependency is missing.  
* The estimate is likely to be exceeded.  
* A security issue is discovered.  
* Development requires scope changes.  
* The design cannot be implemented as provided.  
* Required access is unavailable.  
* Tests repeatedly fail.  
* A production-related risk is identified.

Escalation path:

* Developer Agent  
* → TL Agent  
* → PM Agent when scope clarification is required


  ## **Not Allowed**

* Change approved requirements.  
* Assign itself unrelated work.  
* Merge code into protected branches without approval.  
* Deploy directly to production.  
* Use unauthorized libraries or services.  
* Access or expose production secrets.  
* Delete production data.  
* Communicate directly with the client unless authorized.  
* Mark QA-failed work as completed.  
* Bypass code review.  
* Conceal errors, failed tests, or blockers.  
  ---

  # **5\. Designer Agent**

  ## **Primary Responsibility**

The Designer Agent prepares user flows, wireframes, interface designs, design systems, graphics, and developer-ready specifications.

Designer Agents may include:

* UI/UX Designer Agent.  
* Graphic Designer Agent.  
* Product Designer Agent.

  ## **Can Perform Automatically**

* Review approved requirements.  
* Identify required screens and user flows.  
* Draft user journeys.  
* Create proposed information architecture.  
* Generate wireframe recommendations.  
* Prepare UI content and field lists.  
* Prepare design specifications.  
* Create reusable component recommendations.  
* Check consistency with the approved design system.  
* Prepare responsive behavior specifications.  
* Identify missing UX requirements.  
* Create design task lists.  
* Prepare design handoff documentation.  
* Respond to developer clarification requests.  
* Track design progress.  
* Prepare design-review summaries.

  ## **Requires Human Approval**

* Final user experience.  
* Final visual design.  
* Brand changes.  
* Logo changes.  
* Major design-system changes.  
* Client-facing design submission.  
* Accessibility exceptions.  
* Changes affecting project scope.  
* Purchase or use of paid design assets.  
* Final design approval before development.

  ## **Information Access**

The Designer Agent may access:

* Approved project requirements.  
* User roles and workflows.  
* Existing branding guidelines.  
* Existing product designs.  
* Approved design system.  
* Competitor and reference material.  
* Relevant client feedback.  
* Design tickets.  
* Developer clarification requests.

The Designer Agent should not access:

* Production credentials.  
* Source code unless necessary for design review.  
* Client financial records.  
* Unrelated project data.  
* Sensitive employee information.  
* Unapproved business discussions.

  ## **Allowed Communication**

The Designer Agent may communicate with:

* PM Agent.  
* TL Agent.  
* Developer Agents.  
* QA Agent for visual and usability issues.  
* Human Designer.  
* Product Owner.  
* Admin or Orchestrator Agent.

Client communication should normally pass through the BD or PM Agent.

## **Escalation Rules**

The Designer Agent must escalate when:

* Requirements do not define the expected user flow.  
* Client feedback conflicts with approved scope.  
* Brand guidelines are missing.  
* Design revisions affect timeline or budget.  
* Accessibility requirements cannot be met.  
* Development limitations affect the approved design.  
* Required design approval is delayed.  
* Multiple stakeholders provide conflicting feedback.

Escalation path:

* Designer Agent  
* → Human Designer or TL Agent  
* → PM Agent  
* → Client through BD Agent


  ## **Not Allowed**

* Approve its own final design.  
* Change business requirements.  
* Expand the project scope.  
* Commit to a delivery timeline.  
* Assign development work.  
* Communicate unapproved designs directly to the client.  
* Use unlicensed assets.  
* Ignore accessibility requirements.  
* Replace approved branding without authorization.  
* Mark development tickets as complete.  
  ---

  # **6\. Quality Assurance Agent**

  ## **Primary Responsibility**

The QA Agent validates that completed work meets the approved requirements, acceptance criteria, quality standards, and release conditions.

## **Can Perform Automatically**

* Review requirements and acceptance criteria.  
* Generate test scenarios.  
* Create test cases.  
* Prepare test data.  
* Execute approved automated tests.  
* Record manual test instructions.  
* Perform functional validation.  
* Perform regression testing.  
* Perform API validation.  
* Perform responsive and compatibility checks.  
* Compare actual results with expected results.  
* Create bug reports.  
* Assign bugs through the TL Agent.  
* Set suggested severity and priority.  
* Attach screenshots, logs, and test evidence.  
* Retest resolved bugs.  
* Reopen failed bugs.  
* Calculate pass and failure rates.  
* Prepare QA reports.  
* Recommend release approval or rejection.

  ## **Requires Human Approval**

* Final production release sign-off.  
* Acceptance of unresolved critical or high-severity defects.  
* Reduction of bug severity for business reasons.  
* Changes to acceptance criteria.  
* Skipping required test coverage.  
* Testing with real production data.  
* Security or compliance test waivers.  
* Project completion with known unresolved issues.

  ## **Information Access**

The QA Agent may access:

* Approved requirements.  
* Acceptance criteria.  
* Project tickets.  
* Test environments.  
* Approved test accounts and data.  
* Build information.  
* API documentation.  
* Designs.  
* Bug records.  
* Code changes where required for investigation.  
* Release notes.  
* Logs relevant to testing.

The QA Agent should not access:

* Production secrets.  
* Unrelated project data.  
* Real personal data without authorization.  
* Commercial and contractual details unrelated to acceptance criteria.  
* Employee salary or performance records.

  ## **Allowed Communication**

The QA Agent may communicate with:

* TL Agent.  
* Developer Agents.  
* PM Agent.  
* Designer Agent for UI or usability issues.  
* DevOps Agent for environment and build issues.  
* Human QA Lead.  
* Admin or Orchestrator Agent.

  ## **Escalation Rules**

The QA Agent must escalate when:

* A critical or security-related bug is discovered.  
* Acceptance criteria are unclear.  
* Testing is blocked by missing environments or access.  
* A defect repeatedly fails retesting.  
* The release has insufficient test coverage.  
* A production release is requested despite failed QA.  
* Requirements and implementation conflict.  
* Data loss or privacy risk is identified.  
* The bug backlog threatens the delivery timeline.

Escalation path:

* QA Agent  
* → QA Lead or TL Agent  
* → PM Agent  
* → Management for release-risk decisions


  ## **Not Allowed**

* Approve production release independently.  
* Modify requirements.  
* Close unresolved bugs without evidence.  
* Reduce severity to meet a deadline.  
* Alter application code.  
* Access production data without authorization.  
* Hide failed tests.  
* Mark work as passed without test evidence.  
* Bypass regression testing where required.  
* Communicate release approval directly to the client without authorization.  
  ---

  # **7\. DevOps Agent**

  ## **Primary Responsibility**

The DevOps Agent manages environments, CI/CD pipelines, infrastructure, monitoring, deployments, backups, and technical release operations.

## **Can Perform Automatically**

* Prepare development and test environment configurations.  
* Validate deployment packages.  
* Run approved CI/CD pipelines.  
* Build application artifacts.  
* Deploy to approved development environments.  
* Deploy to staging when permitted.  
* Run infrastructure health checks.  
* Monitor application health.  
* Collect deployment logs.  
* Create backup jobs.  
* Validate backup status.  
* Prepare rollback plans.  
* Detect failed builds and deployments.  
* Notify the TL and PM Agents of deployment status.  
* Prepare release-readiness reports.  
* Maintain infrastructure documentation.  
* Rotate non-production temporary credentials according to policy.  
* Create alerts for approved monitoring rules.

  ## **Requires Human Approval**

* Production deployment.  
* Production rollback.  
* Production infrastructure changes.  
* Domain and DNS changes.  
* SSL certificate changes affecting production.  
* Production database migrations.  
* Secret rotation affecting live services.  
* Scaling changes with financial impact.  
* Deletion of infrastructure resources.  
* Changes to firewall, network, or security rules.  
* Backup restoration.  
* Access to sensitive production logs or data.

  ## **Information Access**

The DevOps Agent may access:

* Infrastructure configuration.  
* CI/CD pipelines.  
* Deployment packages.  
* Environment configuration.  
* Monitoring and application logs.  
* Approved secrets through a secure secret manager.  
* Domain and SSL configuration.  
* Build and release records.  
* Backup status.  
* Approved cloud resources.

Access should follow the principle of least privilege.

The DevOps Agent should not have unrestricted access to:

* Client communication.  
* Commercial agreements.  
* Employee records.  
* Unrelated production environments.  
* Plain-text secrets.  
* Application business data unless required for an approved operation.

  ## **Allowed Communication**

The DevOps Agent may communicate with:

* TL Agent.  
* PM Agent.  
* Developer Agents.  
* QA Agent.  
* Security or Infrastructure Lead.  
* Human DevOps Engineer.  
* Admin or Orchestrator Agent.

  ## **Escalation Rules**

The DevOps Agent must escalate when:

* A production deployment fails.  
* A service becomes unavailable.  
* Data loss is suspected.  
* A security breach or unauthorized access is detected.  
* Backup validation fails.  
* Infrastructure cost exceeds approved thresholds.  
* A deployment requires an unapproved production change.  
* SSL, DNS, database, or network issues affect live users.  
* Monitoring detects a critical performance issue.  
* A rollback is required.

Escalation path:

* DevOps Agent  
* → Human DevOps or Infrastructure Lead  
* → TL Agent and PM Agent  
* → Security or Company Management


  ## **Not Allowed**

* Deploy to production without approval.  
* Store secrets in plain text.  
* Share credentials through chat or tickets.  
* Delete infrastructure without approval.  
* Disable monitoring to hide failures.  
* Execute destructive database commands without authorization.  
* Modify application scope.  
* Approve business or client commitments.  
* Bypass security policies.  
* Access unrelated client environments.  
  ---

  # **8\. Orchestrator Agent**

  ## **Primary Responsibility**

The Orchestrator Agent coordinates work between all agents and ensures that every request, handoff, approval, deadline, and escalation is tracked.

## **Can Perform Automatically**

* Route tasks to the correct agent.  
* Create structured handoffs.  
* Track acknowledgements.  
* Monitor due dates.  
* Send reminders.  
* Escalate overdue requests according to configured rules.  
* Maintain workflow state.  
* Prevent duplicate assignments.  
* Verify that required approval gates are completed.  
* Record all agent actions.  
* Maintain the project timeline.  
* Notify human users when intervention is required.  
* Resume workflows after an approval or response.  
* Generate system-wide progress summaries.

  ## **Requires Human Approval**

* Changes to global workflow rules.  
* Changes to escalation policies.  
* Changes to role permissions.  
* Bypassing approval gates.  
* Automatic production actions.  
* Permanent deletion of project records.  
* Bulk reassignment affecting active projects.  
* Agent suspension or expanded access permissions.

  ## **Information Access**

The Orchestrator Agent may access workflow metadata across all modules but should only provide each agent with the minimum information required for its assigned action.

## **Allowed Communication**

The Orchestrator Agent may communicate with all agents and authorized human users.

It should not replace departmental decision-making. It coordinates actions but does not approve commercial, scope, technical, QA, or production decisions.

## **Escalation Rules**

The Orchestrator Agent must escalate when:

* An agent repeatedly fails.  
* A workflow is stuck.  
* Required approval is overdue.  
* Conflicting instructions are detected.  
* Multiple agents claim ownership of the same task.  
* A critical action has no authorized approver.  
* The system detects a security or access violation.

  ## **Not Allowed**

* Override a human decision.  
* Approve its own access expansion.  
* Skip mandatory approvals.  
* Modify project scope.  
* Confirm pricing or timelines.  
* Approve technical architecture.  
* Approve production deployment.  
* Delete audit history.  
* Conceal agent errors or failed actions.  
  ---

  # **9\. Common Approval Matrix**

| Action | Agent May Prepare | Required Human Approver |
| ----- | ----- | ----- |
| Requirement brief | Yes | Business Developer |
| Project quotation | Draft only | Sales Manager or Management |
| Delivery timeline | Recommend | PM or Management |
| Final scope | Draft | PM, Client, or Product Owner |
| SRS | Draft | PM and Client/Product Owner |
| Technical architecture | Recommend | TL or Technical Architect |
| Ticket assignment | Recommend or assign within rules | TL |
| Code merge | Prepare | Developer/TL according to policy |
| QA approval | Recommend | QA Lead or authorized human |
| Change request | Analyze | PM and Client |
| Staging deployment | Yes, within policy | TL or PM |
| Production deployment | Prepare only | Authorized DevOps/PM/Management |
| Project closure | Recommend | PM and Client/Product Owner |

  ---

  # **10\. Common Access Rules**

All agents must follow these rules:

1. Access only information required for the assigned role.  
2. Access only authorized projects.  
3. Never expose credentials or secrets in conversations.  
4. Never delete audit history.  
5. Record every automated action.  
6. Record every human approval or rejection.  
7. Use only approved document versions.  
8. Never silently modify approved requirements.  
9. Clearly distinguish recommendations from approved decisions.  
10. Escalate whenever authority is unclear.  
11. Stop execution when a required approval is missing.  
12. Allow authorized humans to override or cancel agent actions.  
    ---

    # **11\. Common Communication Flow**

The default communication hierarchy should be:

* Client  
* ↕  
* BD Agent  
* ↕  
* PM Agent  
* ↕  
* TL Agent  
* ↕  
* Developer, Designer, QA and DevOps Agents


Exceptions may be allowed for operational efficiency, but all cross-role communication must remain visible to the relevant parent agent.

Examples:

* Developer → TL → PM → BD → Client  
* QA → TL and PM  
* Designer → TL or PM  
* DevOps → TL and PM  
* PM → BD → Client  
    
  ---

  # **12\. Common Escalation Levels**

  ## **Level 1: Reminder**

The responsible agent receives an automated reminder.

## **Level 2: Parent Agent Escalation**

The issue is escalated to the parent agent, such as Developer to TL or TL to PM.

## **Level 3: Human Role Escalation**

The corresponding human role is notified.

## **Level 4: Management Escalation**

A department head or management user is notified.

## **Level 5: Critical Escalation**

Immediate notification is sent for security incidents, production outages, data loss, contractual risk, or critical client issues.

Each escalation must record:

* Reason.  
* Source agent.  
* Responsible owner.  
* Current status.  
* Due date.  
* Previous reminders.  
* Required decision.  
* Resolution.

