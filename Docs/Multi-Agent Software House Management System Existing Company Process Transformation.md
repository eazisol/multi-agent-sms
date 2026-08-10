# **Existing Company Process Transformation**

## **Human-Based to Agentic Software Delivery System**

## **1\. Purpose**

The company currently operates through a primarily human-managed delivery process involving Business Development, Project Management, Team Leads, Developers, Designers, QA Engineers, and DevOps resources.

The target operating model is a **hybrid agentic system with human involvement**, where:

* Agents perform repetitive, administrative, analytical, documentation, tracking, and follow-up activities.  
* Human team members review, approve, correct, and take responsibility for critical decisions.  
* Every process has a defined owner, input, output, deadline, approval gate, and escalation path.  
* Information moves in both directions between BD, PM, TL, delivery teams, QA, and the client.  
* No requirement, commitment, blocker, approval, or change request is lost.

---

# **2\. Current Human-Based Process**

The company currently follows this general structure:

| Process | Current Responsible Role |
| ----- | ----- |
| New client inquiries | Human BD |
| Requirement gathering | Human BD |
| Proposal preparation | Human BD and PM |
| Project handover | PM and TL |
| SRS preparation | TL and QA |
| Project planning | TL and QA |
| Ticket creation | TL |
| Team assignment | TL |
| Development | Development team |
| QA testing | QA team |
| Client updates | TL, PM, and Human BD |
| Change requests | TL and Development team |
| Deployment | TL |
| Project completion | PM, TL, QA, and BD |

This process depends heavily on manual communication, individual follow-ups, and personal knowledge. The agentic system should standardize these activities while keeping humans responsible for important approvals.

---

# **3\. Target Hybrid Agentic Operating Model**

The recommended process structure is:

Client  
  ↕  
Human BD \+ BD Agent  
  ↕  
Human PM \+ PM Agent  
  ↕  
Human TL \+ TL Agent  
  ↕  
Developer, Designer, QA and DevOps Agents  
  ↕  
Human Delivery Team

Each process should follow this standard lifecycle:

Trigger  
→ Agent Review  
→ Information Validation  
→ Agent Action  
→ Human Approval, when required  
→ Handover  
→ Tracking  
→ Follow-Up  
→ Escalation  
→ Completion

---

# **4\. Process 1: New Client Inquiry Management**

## **Starting Condition**

A new inquiry is received through:

* Website form  
* Email  
* Phone call  
* LinkedIn  
* Upwork  
* Referral  
* CRM  
* WhatsApp  
* Slack  
* Any connected lead source

## **Responsible Roles**

* Primary agent: BD Agent  
* Human owner: Human Business Developer  
* Supporting agent: Orchestrator Agent

## **Required Information**

* Client name  
* Company name  
* Email  
* Phone number  
* Inquiry source  
* Client message  
* Requested service  
* Estimated urgency  
* Attachments  
* Referral details  
* Preferred communication method

## **Agent Actions**

The BD Agent should:

1. Create a lead or inquiry record.  
2. Check whether the client already exists.  
3. Categorize the inquiry.  
4. Identify the requested service.  
5. Determine whether the inquiry is relevant to company services.  
6. Assign an initial priority.  
7. Generate an acknowledgment message.  
8. Assign the inquiry to the appropriate Human BD.  
9. Create the first follow-up task.  
10. Track whether the client receives a response.

## **Human Approval Requirements**

Human BD approval is required before:

* Rejecting a potentially valid inquiry.  
* Making any commercial commitment.  
* Discussing pricing.  
* Confirming availability.  
* Confirming a delivery deadline.  
* Sending a customized proposal.

Standard acknowledgment messages may be sent automatically if approved templates are used.

## **Expected Output**

* New inquiry record  
* Initial inquiry classification  
* Assigned Human BD  
* Client acknowledgment  
* Requirement-gathering task  
* Follow-up deadline

## **Next Destination**

New Inquiry  
→ Requirement Gathering

## **Recommended SLA**

* Automatic acknowledgment: within 5 minutes  
* Human BD review: within 2 business hours  
* Initial meaningful response: within 4 business hours  
* Urgent inquiry: within 1 business hour

## **Escalation Rule**

* After 2 hours without review: remind Human BD.  
* After 4 hours without action: escalate to BD Manager.  
* After 1 business day without response: escalate to management.  
* High-value or urgent leads should be escalated immediately.

---

# **5\. Process 2: Requirement Gathering**

## **Starting Condition**

The inquiry has been reviewed and confirmed as a valid potential project.

## **Responsible Roles**

* Primary agent: BD Agent  
* Human owner: Human BD  
* Supporting agent: PM Agent  
* Consultation support: TL Agent, when technical clarification is needed

## **Required Information**

* Business problem  
* Project objective  
* Target users  
* Required features  
* User workflows  
* Platforms  
* Integrations  
* Technical constraints  
* Existing system details  
* Design references  
* Timeline expectations  
* Budget expectations  
* Security requirements  
* Compliance requirements  
* Hosting expectations  
* Required deliverables  
* Acceptance expectations

## **Agent Actions**

The BD Agent should:

1. Review all previous client communication.  
2. Use an approved requirement questionnaire.  
3. Ask one clear question at a time.  
4. Record each answer in structured fields.  
5. Summarize uploaded files and reference systems.  
6. Detect missing information.  
7. Detect conflicting requirements.  
8. Create follow-up questions.  
9. Prepare a requirement completeness score.  
10. Generate the initial Project Requirement Brief.  
11. Request PM or TL input for complex requirements.  
12. Obtain client confirmation of the summarized requirements.

## **Human Approval Requirements**

Human BD must approve:

* Final Requirement Brief  
* Interpretation of unclear client requirements  
* Commercially sensitive questions  
* Any assumptions that may affect cost or timeline

PM or TL approval is required when:

* Technical feasibility is uncertain.  
* The requested integration is unclear.  
* Security or infrastructure requirements are complex.  
* The project appears larger than originally described.

## **Expected Output**

* Completed Requirement Brief  
* List of functional requirements  
* List of non-functional requirements  
* Business objectives  
* User roles  
* Project assumptions  
* Constraints  
* Risks  
* Open questions  
* Client confirmation record  
* Requirement completeness score

## **Next Destination**

Requirement Gathering  
→ Initial Feasibility Review  
→ Proposal Preparation

## **Recommended SLA**

* Small inquiry: 1–2 business days  
* Medium project: 3–5 business days  
* Complex project: 5–10 business days  
* Client follow-up reminder: every 2 business days

## **Escalation Rule**

* Missing client response after two reminders: notify Human BD.  
* No client response after three reminders: mark as dormant and escalate to BD Manager.  
* Technical uncertainty: escalate to TL.  
* Scope uncertainty: escalate to PM.  
* Security or legal concern: escalate to management.

---

# **6\. Process 3: Proposal Preparation**

## **Starting Condition**

The Requirement Brief is sufficiently complete and initial feasibility has been confirmed.

## **Responsible Roles**

* Primary agents: BD Agent and PM Agent  
* Human owners: Human BD and Human PM  
* Technical support: Human TL and TL Agent  
* Financial approval: Authorized management or finance representative

## **Required Information**

* Approved Requirement Brief  
* Proposed scope  
* Out-of-scope items  
* Project phases  
* Estimated effort  
* Required team structure  
* Timeline estimate  
* Risks  
* Assumptions  
* Pricing rules  
* Payment terms  
* Support terms  
* Validity period

## **Agent Actions**

The BD and PM Agents should:

1. Convert requirements into a proposal structure.  
2. Create a draft scope.  
3. Separate in-scope and out-of-scope items.  
4. Generate recommended project phases.  
5. Request estimates from the TL Agent.  
6. Calculate a proposed timeline range.  
7. Identify delivery risks and dependencies.  
8. Generate a draft commercial proposal.  
9. Prepare optional packages where relevant.  
10. Validate that all client requirements are covered.  
11. Create a proposal approval request.  
12. Track client follow-ups after submission.

## **Human Approval Requirements**

Approval is required from:

* Human TL for technical feasibility and estimates.  
* Human PM for scope, phases, and delivery plan.  
* Human BD for client-facing language.  
* Management or finance for final pricing and payment terms.

The agent must not send the final proposal without approval.

## **Expected Output**

* Approved proposal  
* Scope statement  
* Out-of-scope statement  
* Timeline  
* Effort estimate  
* Team recommendation  
* Commercial pricing  
* Payment schedule  
* Assumptions  
* Risks  
* Proposal version  
* Approval history

## **Next Destination**

Proposal Approved  
→ Proposal Sent to Client  
→ Negotiation  
→ Client Acceptance  
→ Project Handover

## **Recommended SLA**

* Small proposal: 1 business day  
* Medium proposal: 2–3 business days  
* Complex proposal: 3–5 business days  
* Proposal follow-up: after 2 business days  
* Second follow-up: after 5 business days

## **Escalation Rule**

* Missing technical estimate: escalate to Human TL.  
* Missing commercial approval: escalate to management.  
* Proposal delayed beyond SLA: notify BD Manager and PM.  
* Client requests major changes: return to Requirement Gathering.

---

# **7\. Process 4: Project Handover**

## **Starting Condition**

The client has accepted the proposal, and required contract or payment conditions have been completed.

## **Responsible Roles**

* Primary agents: PM Agent and TL Agent  
* Human owners: Human PM and Human TL  
* Supporting role: Human BD

## **Required Information**

* Signed proposal or approved agreement  
* Final Requirement Brief  
* Commercial commitments  
* Client contacts  
* Delivery timeline  
* Approved scope  
* Out-of-scope items  
* Assumptions  
* Risks  
* Attachments  
* Access requirements  
* Communication expectations  
* Payment status  
* Client priorities

## **Agent Actions**

The PM Agent should:

1. Create the project record.  
2. Link the client, proposal, and requirements.  
3. Generate the project handover checklist.  
4. Verify all mandatory documentation.  
5. Create the project communication channel.  
6. Define project owners.  
7. Identify missing access or credentials.  
8. Schedule the internal kickoff.  
9. Prepare a handover summary for the TL.  
10. Record all commitments made during sales.  
11. Create initial risks and dependencies.  
12. Request formal acknowledgment from PM and TL.

## **Human Approval Requirements**

* Human BD confirms commercial commitments.  
* Human PM accepts project ownership.  
* Human TL confirms technical readiness.  
* Management approves any unresolved commercial exception.

## **Expected Output**

* Active project record  
* Approved handover document  
* Project owner assignment  
* Technical owner assignment  
* Client communication plan  
* Initial risk register  
* Missing-access checklist  
* Kickoff meeting record

## **Next Destination**

Project Handover  
→ SRS Preparation

## **Recommended SLA**

* Handover initiated: within 1 business day of client acceptance  
* Internal kickoff: within 2 business days  
* Handover acceptance: within 1 business day after kickoff

## **Escalation Rule**

* Missing commercial information: return to Human BD.  
* Missing requirements: return to BD Agent.  
* Missing technical information: escalate to TL.  
* Incomplete payment or contract conditions: pause project and escalate to management.

---

# **8\. Process 5: SRS Preparation**

## **Starting Condition**

The project handover has been accepted, and sufficient requirements are available.

## **Responsible Roles**

* Primary agents: PM Agent, TL Agent, and QA Agent  
* Human owners: Human PM, Human TL, and Human QA Lead

Although the existing process assigns SRS mainly to TL and QA, the market-standard model should place primary ownership with the PM or Business Analyst, with TL and QA providing technical and testability reviews.

## **Required Information**

* Requirement Brief  
* Approved proposal  
* Project scope  
* User roles  
* User workflows  
* Business rules  
* Integrations  
* Security requirements  
* Performance expectations  
* Design references  
* Acceptance expectations  
* Technical constraints

## **Agent Actions**

The agents should:

1. Create uniquely numbered requirements.  
2. Separate functional and non-functional requirements.  
3. Define user roles and permissions.  
4. Create user flows.  
5. Define field-level requirements.  
6. Define validation rules.  
7. Define error scenarios.  
8. Define integration requirements.  
9. Define security and performance requirements.  
10. Create acceptance criteria.  
11. Create requirement traceability records.  
12. Detect contradictions and missing details.  
13. Generate clarification requests.  
14. Maintain SRS version history.  
15. Prepare the document for approval.

## **Human Approval Requirements**

* Human PM approves business scope.  
* Human TL approves technical feasibility.  
* Human QA approves testability.  
* Client or Product Owner approves the final SRS.  
* Any change after approval requires a change request or formal revision.

## **Expected Output**

* Approved SRS  
* Functional requirements  
* Non-functional requirements  
* User roles  
* User flows  
* Acceptance criteria  
* Validation rules  
* Integration specifications  
* Requirement traceability matrix  
* Open issues list  
* Approval record

## **Next Destination**

Approved SRS  
→ Project Planning

## **Recommended SLA**

* Small project: 2–4 business days  
* Medium project: 5–10 business days  
* Complex project: 10–20 business days  
* Internal review: 2 business days  
* Client review: 3–5 business days

## **Escalation Rule**

* Missing requirement: PM Agent to BD Agent.  
* Technical conflict: escalate to Human TL.  
* Untestable requirement: escalate to PM and client.  
* Approval delay: remind approver, then escalate to Human PM.

---

# **9\. Process 6: Project Planning**

## **Starting Condition**

The SRS has been approved or sufficiently baselined for planning.

## **Responsible Roles**

* Primary agents: PM Agent and TL Agent  
* Supporting agent: QA Agent  
* Human owners: Human PM and Human TL

## **Required Information**

* Approved SRS  
* Project scope  
* Available team members  
* Skills matrix  
* Capacity  
* Timeline commitment  
* Risks  
* Dependencies  
* Technical architecture  
* QA requirements  
* Deployment requirements

## **Agent Actions**

The PM and TL Agents should:

1. Divide the project into phases.  
2. Create milestones.  
3. Define deliverables.  
4. Map requirements to phases.  
5. Identify dependencies.  
6. Estimate effort.  
7. Define resource requirements.  
8. Create the delivery sequence.  
9. Define QA activities.  
10. Define deployment activities.  
11. Identify the critical path.  
12. Create a risk-adjusted timeline.  
13. Define reporting frequency.  
14. Create phase-level acceptance gates.  
15. Prepare the project baseline.

## **Human Approval Requirements**

* Human TL approves estimates and technical sequencing.  
* Human PM approves timeline and milestone structure.  
* QA Lead approves testing allocation.  
* Management approves additional resources or major timeline changes.

## **Expected Output**

* Project roadmap  
* Phase plan  
* Milestones  
* Delivery schedule  
* Resource plan  
* Dependency map  
* Risk register  
* Communication schedule  
* QA plan  
* Deployment plan

## **Next Destination**

Project Planning  
→ Ticket Creation

## **Recommended SLA**

* Initial project plan: within 2–5 business days after SRS approval  
* Planning review: within 1–2 business days  
* Baseline approval: within 1 business day after review

## **Escalation Rule**

* Missing resources: escalate to management.  
* Timeline conflict: escalate to PM and BD.  
* Technical dependency conflict: escalate to TL.  
* Testing capacity issue: escalate to QA Lead.

---

# **10\. Process 7: Ticket Creation**

## **Starting Condition**

The project phases, requirements, and delivery plan have been approved.

## **Responsible Roles**

* Primary agent: TL Agent  
* Supporting agents: PM Agent and QA Agent  
* Human owner: Human TL

## **Required Information**

* Approved requirements  
* Project phases  
* Technical architecture  
* Acceptance criteria  
* Designs  
* Dependencies  
* Team roles  
* Definition of Ready  
* Definition of Done

## **Agent Actions**

The TL Agent should:

1. Create epics for major modules.  
2. Create user stories.  
3. Create development tasks.  
4. Create design tasks.  
5. Create QA tasks.  
6. Create DevOps tasks.  
7. Add acceptance criteria.  
8. Add technical notes.  
9. Add requirement references.  
10. Add dependencies.  
11. Add estimates.  
12. Add priority.  
13. Add required evidence.  
14. Identify tickets requiring design.  
15. Validate ticket completeness.

## **Human Approval Requirements**

Human TL must approve:

* Technical breakdown  
* Estimates  
* Dependencies  
* Priority  
* Definition of Done  
* Tickets affecting architecture or infrastructure

PM approval is required when ticket scope affects committed project deliverables.

## **Expected Output**

* Approved epics  
* User stories  
* Development tickets  
* Design tickets  
* QA tickets  
* DevOps tickets  
* Requirement traceability links  
* Estimates  
* Dependencies  
* Acceptance criteria

## **Next Destination**

Approved Tickets  
→ Team Assignment

## **Recommended SLA**

* Ticket creation: within 1–3 business days per phase  
* Ticket review: within 1 business day  
* Clarification before assignment: within 4 working hours

## **Escalation Rule**

* Incomplete requirements: return to PM.  
* Missing design: escalate to Designer.  
* Unclear technical solution: escalate to Human TL.  
* Missing acceptance criteria: return to PM or QA Agent.

---

# **11\. Process 8: Team Assignment**

## **Starting Condition**

Tickets meet the Definition of Ready.

## **Responsible Roles**

* Primary agent: TL Agent  
* Human owner: Human TL  
* Supporting agent: PM Agent

## **Required Information**

* Ticket type  
* Required skills  
* Team member skills  
* Availability  
* Current workload  
* Estimated effort  
* Dependencies  
* Ticket priority  
* Delivery deadline

## **Agent Actions**

The TL Agent should:

1. Match tickets with appropriate skills.  
2. Review team workload.  
3. Check developer availability.  
4. Recommend assignees.  
5. Prevent workload conflicts.  
6. Assign related tasks consistently.  
7. Create assignment notifications.  
8. Request task acknowledgment.  
9. Track unacknowledged assignments.  
10. Reassign tasks when approved.

## **Human Approval Requirements**

Human TL approval is required for:

* Final task assignment  
* Workload exceptions  
* Reassignment of critical work  
* Cross-project resource movement  
* Overtime or special resource allocation

## **Expected Output**

* Assigned tickets  
* Task owner  
* Planned start date  
* Due date  
* Workload update  
* Assignment acknowledgment  
* Escalation owner

## **Next Destination**

Assigned Ticket  
→ Development or Design

## **Recommended SLA**

* Normal ticket assignment: within 4 working hours  
* Ticket acknowledgment: within 2 working hours  
* Urgent ticket assignment: within 1 working hour

## **Escalation Rule**

* No acknowledgment: remind assignee.  
* No response after SLA: escalate to Human TL.  
* No suitable resource: escalate to PM.  
* Workload overload: escalate to PM and management.

---

# **12\. Process 9: Development and Design Execution**

## **Starting Condition**

A ticket has been assigned and acknowledged.

## **Responsible Roles**

* Primary agents: Developer Agent or Designer Agent  
* Human owners: Assigned Developer or Designer  
* Supervising role: Human TL

## **Required Information**

* Ticket description  
* Requirement reference  
* Acceptance criteria  
* Technical notes  
* Approved design  
* Dependencies  
* Environment access  
* Due date  
* Definition of Done

## **Agent Actions**

The relevant agent should:

1. Review the ticket.  
2. Check whether all required information is present.  
3. Generate an implementation plan.  
4. Identify risks and dependencies.  
5. Track task progress.  
6. Maintain implementation notes.  
7. Generate or update tests.  
8. Create code-review or design-review requests.  
9. Report blockers.  
10. Record evidence of completion.  
11. Submit work for TL review.  
12. Update the ticket status automatically based on evidence.

## **Human Approval Requirements**

Human developer, designer, or TL approval is required for:

* Final code or design  
* Code merge  
* Architecture changes  
* Database migrations  
* Security-related changes  
* New paid services  
* Major design changes  
* Completion confirmation

## **Expected Output**

* Implemented code or completed design  
* Tests  
* Pull request or design handoff  
* Technical documentation  
* Completion evidence  
* Updated ticket  
* Blocker history  
* Review record

## **Next Destination**

Development Complete  
→ TL Review  
→ QA Testing

## **Recommended SLA**

SLA should be based on the approved estimate.

Recommended control rules:

* Daily progress update for active tickets.  
* Blocker reporting within 1 working hour.  
* Estimate-overrun warning at 70–80% of planned effort.  
* Review request immediately after completion.

## **Escalation Rule**

* Requirement unclear: escalate to TL.  
* Scope issue: TL escalates to PM.  
* Missing access: escalate to DevOps and TL.  
* Estimate overrun: escalate to TL.  
* Security concern: immediate escalation to TL and Security Lead.

---

# **13\. Process 10: QA Testing**

## **Starting Condition**

Development work has passed TL review and is deployed to an approved test environment.

## **Responsible Roles**

* Primary agent: QA Agent  
* Human owner: Human QA Engineer or QA Lead  
* Supporting roles: Developer Agent and TL Agent

## **Required Information**

* Approved build  
* Related ticket  
* Requirements  
* Acceptance criteria  
* Test cases  
* Test environment  
* Test data  
* Designs  
* Known limitations  
* Release notes

## **Agent Actions**

The QA Agent should:

1. Generate or retrieve test cases.  
2. Validate the test environment.  
3. Execute automated tests.  
4. Support manual testing.  
5. Compare results against acceptance criteria.  
6. Record test evidence.  
7. Create bug tickets.  
8. Recommend severity and priority.  
9. Link bugs to requirements and tickets.  
10. Route defects to the TL.  
11. Retest completed fixes.  
12. Run regression testing.  
13. Prepare a QA summary.  
14. Recommend pass or fail status.

## **Human Approval Requirements**

Human QA approval is required for:

* Final test result  
* Severity confirmation  
* QA sign-off  
* Acceptance of known issues  
* Release-readiness recommendation

PM or management approval is required to release with unresolved high-risk defects.

## **Expected Output**

* Test execution results  
* Bug reports  
* Evidence  
* Retest results  
* Regression results  
* QA completion report  
* Release recommendation

## **Next Destination**

QA Failed  
→ TL  
→ Developer  
→ Fix  
→ QA Retest

QA Passed  
→ PM and TL  
→ Client Review or Deployment

## **Recommended SLA**

* QA start: within 4 working hours after test-ready status  
* Bug reporting: same working day  
* Critical bug notification: immediately  
* Retesting: within 1 business day after fix  
* QA summary: at the end of each testing cycle

## **Escalation Rule**

* Critical defect: immediate escalation to TL and PM.  
* Test environment unavailable: escalate to DevOps.  
* Requirement conflict: escalate to PM.  
* Repeated failed fix: escalate to Human TL.  
* Release requested without QA approval: escalate to management.

---

# **14\. Process 11: Client Progress Updates**

## **Starting Condition**

A scheduled reporting date is reached, a milestone is completed, or a significant issue requires client communication.

## **Responsible Roles**

* Primary agent: PM Agent  
* Supporting agents: TL Agent and BD Agent  
* Human owners: Human PM and Human BD

## **Required Information**

* Completed work  
* Work in progress  
* Upcoming work  
* Blockers  
* Risks  
* Milestone status  
* Budget or timeline impact  
* Decisions required  
* QA status  
* Deployment status

## **Agent Actions**

The PM Agent should:

1. Collect progress from all active tickets.  
2. Summarize completed work.  
3. Identify delays and blockers.  
4. Compare progress against the baseline.  
5. Generate a client-friendly update.  
6. Remove unnecessary internal technical details.  
7. Highlight decisions required from the client.  
8. Include planned next steps.  
9. Send the draft to the Human PM or BD.  
10. Track client acknowledgment and questions.

## **Human Approval Requirements**

Human PM or Human BD must approve:

* Client-facing progress updates  
* Delay communication  
* Timeline changes  
* Scope concerns  
* Budget-related information  
* Sensitive issues

## **Expected Output**

* Approved client update  
* Internal progress report  
* Client decision request  
* Updated risks  
* Follow-up tasks  
* Communication record

## **Next Destination**

Approved Update  
→ Client  
→ Client Response  
→ PM, TL or BD Follow-Up

## **Recommended SLA**

* Standard update: weekly  
* Active high-priority project: twice weekly  
* Critical blocker: same business day  
* Client response acknowledgment: within 4 business hours

## **Escalation Rule**

* Missing team progress: escalate to TL.  
* Serious delay: escalate to Human PM.  
* Client dissatisfaction: escalate to Human BD and management.  
* Client decision overdue: reminders followed by project-risk escalation.

---

# **15\. Process 12: Change Request Management**

## **Starting Condition**

A client, stakeholder, PM, TL, or team member requests a modification to approved requirements, scope, design, timeline, or functionality.

## **Responsible Roles**

* Primary agent: PM Agent  
* Supporting agents: TL Agent, Developer Agent, QA Agent, and BD Agent  
* Human owners: Human PM and Human TL

The current model involving only TL and developers should be expanded. A professional process requires PM ownership because change requests affect scope, cost, schedule, and client commitments.

## **Required Information**

* Requested change  
* Requester  
* Business reason  
* Related requirement  
* Related ticket  
* Priority  
* Expected outcome  
* Supporting evidence  
* Requested deadline

## **Agent Actions**

The PM Agent should:

1. Create a formal change request.  
2. Record the original requirement.  
3. Describe the requested change.  
4. Request technical impact analysis from the TL Agent.  
5. Request effort estimates.  
6. Identify affected tickets and phases.  
7. Identify QA and design impact.  
8. Calculate timeline impact.  
9. Prepare commercial-impact information.  
10. Generate approval options.  
11. Track client approval.  
12. Update the SRS and project baseline after approval.

## **Human Approval Requirements**

Required approvals may include:

* Human TL for technical impact.  
* Human PM for project impact.  
* Human BD or management for commercial impact.  
* Client or Product Owner for scope approval.  
* QA Lead for testing impact.

Development must not start before approval unless the change is classified as an emergency fix.

## **Expected Output**

* Change request record  
* Impact analysis  
* Effort estimate  
* Timeline impact  
* Cost impact  
* Risk analysis  
* Approval or rejection  
* Revised SRS version  
* Updated tickets and roadmap

## **Next Destination**

Approved Change  
→ Updated Requirements  
→ Updated Planning  
→ Ticket Creation  
→ Assignment  
→ Development

Rejected Change  
→ Closed with Reason

## **Recommended SLA**

* Change acknowledgment: within 4 business hours  
* Small change analysis: within 1 business day  
* Medium change analysis: within 2–3 business days  
* Complex change analysis: within 5 business days

## **Escalation Rule**

* Work started without approval: immediate escalation to PM and TL.  
* Commercial impact unclear: escalate to management.  
* Client demands immediate unapproved work: escalate to Human BD and PM.  
* Change threatens committed release: escalate to management.

---

# **16\. Process 13: Deployment**

## **Starting Condition**

The release candidate has passed required QA checks and has received the required release approvals.

## **Responsible Roles**

* Primary agent: DevOps Agent  
* Supervising agent: TL Agent  
* Human owners: Human DevOps Engineer and Human TL  
* Approval owner: PM or authorized release manager

The current process assigns deployment to TL. In the target market-standard system, TL should supervise release readiness, while DevOps should execute deployment.

## **Required Information**

* Approved release candidate  
* QA approval  
* Release notes  
* Deployment checklist  
* Database migration plan  
* Backup confirmation  
* Rollback plan  
* Environment details  
* Deployment window  
* Approval record

## **Agent Actions**

The DevOps Agent should:

1. Validate the release package.  
2. Confirm QA approval.  
3. Confirm backup status.  
4. Validate required environment variables.  
5. Check migration scripts.  
6. Execute pre-deployment checks.  
7. Run the approved deployment pipeline.  
8. Monitor deployment logs.  
9. Execute smoke tests.  
10. Record deployment results.  
11. Notify stakeholders.  
12. Trigger rollback when approved conditions are met.  
13. Generate a deployment report.

## **Human Approval Requirements**

Human approval is mandatory for:

* Production deployment  
* Production database migration  
* Rollback  
* Infrastructure changes  
* DNS changes  
* Secret changes  
* Release with known defects

## **Expected Output**

* Deployment record  
* Release version  
* Deployment logs  
* Smoke-test results  
* Environment status  
* Rollback status  
* Deployment approval history  
* Stakeholder notification

## **Next Destination**

Successful Deployment  
→ Post-Deployment Monitoring  
→ Client Confirmation  
→ Project Completion Review

## **Recommended SLA**

* Staging deployment: within 1 business day after readiness  
* Production deployment: according to approved release window  
* Smoke testing: immediately after deployment  
* Critical deployment failure escalation: immediate

## **Escalation Rule**

* Deployment failure: notify DevOps Lead, TL, and PM.  
* Data issue: initiate incident process.  
* Rollback required: obtain authorized approval immediately.  
* Production outage: critical escalation to management.

---

# **17\. Process 14: Project Completion**

## **Starting Condition**

All approved requirements have been delivered, tested, deployed, and accepted.

## **Responsible Roles**

* Primary agent: PM Agent  
* Supporting agents: TL Agent, QA Agent, BD Agent, and DevOps Agent  
* Human owners: Human PM and Human TL

## **Required Information**

* Completed requirements  
* Closed tickets  
* QA approval  
* Deployment confirmation  
* Client acceptance  
* Open issues  
* Documentation  
* Access handover  
* Training records  
* Support terms  
* Final commercial status

## **Agent Actions**

The PM Agent should:

1. Verify requirement traceability.  
2. Confirm all approved scope items are completed.  
3. Identify unresolved issues.  
4. Confirm QA and deployment status.  
5. Prepare a completion checklist.  
6. Prepare final release notes.  
7. Prepare client handover documentation.  
8. Prepare support and warranty information.  
9. Request formal client acceptance.  
10. Archive project documentation.  
11. Record lessons learned.  
12. Generate a project completion report.  
13. Create post-project follow-up tasks.

## **Human Approval Requirements**

* Human QA confirms quality completion.  
* Human TL confirms technical completion.  
* Human PM confirms project completion.  
* Human BD confirms client communication and commercial closure.  
* Client or Product Owner provides acceptance.  
* Management approves closure where commercial issues remain.

## **Expected Output**

* Client acceptance  
* Project completion report  
* acceptance.  
* Management approves closure where commercial Final release notes  
* Technical handover  
* User documentation  
* Open-issue register  
* Support handover  
* Lessons learned  
* Archived project record

## **Next Destination**

Project Completion  
→ Warranty or Support  
→ Maintenance  
→ Client Relationship Follow-Up

## **Recommended SLA**

* Completion review: within 2 business days after final deployment  
* Client acceptance request: within 1 business day  
* Project closure: within 5 business days after acceptance  
* Lessons-learned session: within 10 business days

## **Escalation Rule**

* Client does not approve: escalate to Human PM and BD.  
* Open critical issue: project cannot close.  
* Missing documentation: return to TL or relevant owner.  
* Commercial dispute: escalate to management.  
* Unresolved support obligation: transfer formally before closure.

---

# **18\. Standard Human Approval Gates**

Human approval should be mandatory at the following points:

| Approval Gate | Required Human Role |
| ----- | ----- |
| Lead rejection | Human BD |
| Final requirement brief | Human BD |
| Final project scope | Human PM |
| Final pricing | Management or authorized BD |
| Delivery timeline | Human PM and TL |
| Technical feasibility | Human TL |
| SRS approval | PM, TL, QA, and Client/Product Owner |
| Project baseline | Human PM |
| Technical architecture | Human TL or Architect |
| Ticket assignment | Human TL |
| Code merge | Authorized Developer or TL |
| QA sign-off | Human QA |
| Change request | PM, TL, BD, and Client as applicable |
| Production deployment | Authorized Human TL, PM, or Release Manager |
| Project closure | Human PM and Client |

---

# **19\. Standard Agentic Follow-Up Rules**

Every process should generate structured follow-up records.

Each follow-up must include:

* Project  
* Process  
* Sender  
* Recipient  
* Required action  
* Due date  
* Priority  
* Status  
* Reminder schedule  
* Escalation owner  
* Response  
* Resolution date

Standard statuses:

Created  
Assigned  
Acknowledged  
In Progress  
Waiting for Information  
Responded  
Resolved  
Overdue  
Escalated  
Closed

---

# **20\. Professional Responsibility Model**

The recommended ownership structure is:

| Area | Agent Responsibility | Human Responsibility |
| ----- | ----- | ----- |
| Data collection | Collect and organize | Validate sensitive information |
| Documentation | Draft and update | Approve final version |
| Planning | Recommend phases and estimates | Confirm commitments |
| Assignment | Recommend suitable resources | Approve final assignment |
| Progress tracking | Track automatically | Resolve exceptions |
| Follow-ups | Send reminders | Handle escalated issues |
| QA | Generate and execute supported tests | Approve final quality result |
| Deployment | Prepare and execute approved pipeline | Approve production release |
| Client communication | Draft and track | Approve sensitive communication |
| Scope change | Analyze impact | Approve commercial and delivery impact |
| Project closure | Verify completion | Accept final closure |

---

# **21\. Final Target Workflow**

Client Inquiry  
→ BD Agent Qualification  
→ Human BD Review  
→ Agentic Requirement Gathering  
→ Human Requirement Approval  
→ PM Agent Scope and Proposal Draft  
→ TL Agent Feasibility and Estimate  
→ Human Commercial Approval  
→ Project Handover  
→ PM/TL/QA Agent SRS Preparation  
→ Human SRS Approval  
→ Agentic Project Planning  
→ Human Baseline Approval  
→ Agentic Ticket Creation  
→ Human TL Assignment Approval  
→ Development and Design Execution  
→ TL Review  
→ QA Testing  
→ Change or Bug Loop  
→ Human Release Approval  
→ DevOps Deployment  
→ Client Acceptance  
→ Project Completion

This model transforms the company from a person-dependent delivery process into a controlled, traceable, and scalable agentic operating system while ensuring that humans remain accountable for business, technical, quality, commercial, and production decisions.

