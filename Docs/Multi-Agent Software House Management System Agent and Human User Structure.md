# **Agent and Human User Structure**

## **1\. Recommended Organization Hierarchy**

Admin / Company Management  
│  
├── Business Development Department  
│   ├── BD Manager  
│   ├── Human Business Developer  
│   └── BD Agent  
│  
├── Project Management Department  
│   ├── PMO Lead / Operations Manager  
│   ├── Human Project Manager  
│   └── PM Agent  
│  
├── Engineering Department  
│   ├── Engineering Manager  
│   ├── Human Team Lead  
│   ├── TL Agent  
│   ├── Frontend Developer  
│   ├── Backend Developer  
│   ├── Full-Stack Developer  
│   ├── Mobile Developer  
│   └── Developer Agents  
│  
├── Design Department  
│   ├── Design Lead  
│   ├── UI/UX Designer  
│   ├── Graphic Designer  
│   └── Designer Agent  
│  
├── Quality Assurance Department  
│   ├── QA Lead  
│   ├── QA Engineer  
│   └── QA Agent  
│  
├── DevOps / Infrastructure Department  
│   ├── DevOps Lead  
│   ├── DevOps Engineer  
│   └── DevOps Agent  
│  
├── Cross-Functional System Agents  
│   ├── Orchestrator Agent  
│   ├── Documentation Agent  
│   └── Notification Agent  
│  
└── External Users  
    ├── Client Administrator  
    ├── Client Approver / Product Owner  
    └── Client Viewer

The human role remains accountable. The related agent performs drafting, analysis, tracking, reminders, recommendations, and approved automation.

---

# **2\. Common User Profile Structure**

Every human user and agent record should contain:

| Field | Purpose |
| ----- | ----- |
| User/Agent ID | Unique identifier |
| User type | Human, Agent, Client, System, Integration |
| Name | Display name |
| Role | Business Developer, PM, TL, Developer, etc. |
| Department | Organizational department |
| Reporting manager | Direct supervisor or responsible human |
| Human supervisor | Required for every operational agent |
| Skills | Technical and operational capabilities |
| Skill level | Beginner, Intermediate, Advanced, Expert |
| Availability | Available, Partially Available, Busy, On Leave, Offline |
| Capacity | Percentage or hours available |
| Working hours | User-specific work calendar |
| Time zone | Used for SLA and notification calculations |
| Project access | Projects the user can view or modify |
| Approval authority | Actions the user may approve |
| Notification preferences | Channels, frequency, and event types |
| Escalation level | Maximum level the user may receive or initiate |
| Status | Active, Inactive, Suspended, Archived |
| Effective dates | Start and end of role assignment |

---

# **3\. Admin / System Administrator**

## **Role**

Controls organization configuration, security, users, agents, permissions, workflows, integrations, and system settings.

## **Department**

Administration / Operations / IT.

## **Reporting Manager**

Company owner, operations director, or senior management.

## **Required Skills**

* System administration  
* Role-based access control  
* Workflow configuration  
* Security management  
* Integration configuration  
* Audit and compliance  
* Incident coordination

## **Availability**

Full organizational availability during business hours, with emergency access for critical system incidents.

## **Working Hours**

Organization business calendar, with optional emergency on-call schedule.

## **Project Access**

* Access to all projects for administration  
* Access to configuration and audit information  
* Restricted access to confidential content unless specifically authorized

## **Approval Authority**

May approve:

* User activation and deactivation  
* Role and permission changes  
* Agent activation and suspension  
* Workflow configuration changes  
* Integration configuration  
* Emergency system access  
* Audit and security actions

Should not independently approve:

* Client pricing  
* Project scope  
* Technical architecture  
* QA sign-off  
* Production deployment unless also assigned as an authorized release manager

## **Notification Preferences**

Recommended notifications:

* In-app and email for administrative actions  
* Immediate alerts for permission violations  
* Immediate alerts for agent failures  
* Immediate alerts for security incidents  
* Daily summary of system health and failed automations

---

# **4\. Human Business Developer**

## **Role**

Manages client inquiries, qualification, requirements, proposals, commercial discussions, and client relationships.

## **Department**

Business Development / Sales.

## **Reporting Manager**

BD Manager or Company Management.

## **Required Skills**

* Client communication  
* Requirement gathering  
* Sales qualification  
* Proposal preparation  
* Negotiation  
* Scope understanding  
* Follow-up management  
* Software service knowledge

## **Availability**

Normally available during client-facing business hours.

## **Working Hours**

Based on the assigned client market and time zone. The system should support separate calendars for local and international clients.

## **Project Access**

May access:

* Assigned clients  
* Contacts  
* Queries  
* Opportunities  
* Requirement briefs  
* Proposals  
* High-level project progress  
* Client-facing documents  
* Approved scope and timeline

Should not normally access:

* Production credentials  
* Source-code details  
* Internal technical secrets  
* Unrelated client projects

## **Approval Authority**

May approve:

* Inquiry qualification  
* Requirement brief  
* Standard client communications  
* Proposal wording  
* Lead closure  
* Client update drafts

Requires higher approval for:

* Final pricing  
* Discounts  
* Contracts  
* Delivery commitments  
* Major commercial changes

## **Notification Preferences**

* Immediate new-inquiry notification  
* Reminder before client follow-up deadline  
* PM clarification notifications  
* Proposal approval alerts  
* Client-response notifications  
* Weekly opportunity summary

---

# **5\. BD Agent**

## **Role**

Supports the Human BD by processing inquiries, gathering requirements, preparing summaries, drafting responses, and tracking client follow-ups.

## **Department**

Business Development.

## **Reporting Manager**

Human Business Developer or BD Manager.

## **Required Skills**

* Inquiry classification  
* Structured requirement gathering  
* Conversation summarization  
* Missing-information detection  
* Requirement brief generation  
* Follow-up scheduling  
* Client-friendly drafting

## **Availability**

Continuous system availability, subject to platform uptime and configured operating rules.

## **Working Hours**

May operate continuously, but client-facing messages should follow the client’s permitted communication hours.

## **Project Access**

Access limited to:

* Assigned clients  
* Assigned queries  
* Opportunities  
* Requirement records  
* Approved sales templates  
* High-level project reports

## **Approval Authority**

May automatically:

* Categorize inquiries  
* Create follow-ups  
* Prepare requirement drafts  
* Send approved acknowledgment templates  
* Route requirements to PM

Cannot approve:

* Pricing  
* Final scope  
* Contracts  
* Delivery dates  
* Technical architecture

## **Notification Preferences**

Primarily system events rather than personal notifications:

* New query triggers  
* Missing client information  
* PM clarification requests  
* Follow-up deadline events  
* Human review decisions

---

# **6\. Human Project Manager**

## **Role**

Owns project planning, scope, timeline, coordination, reporting, risks, approvals, and delivery governance.

## **Department**

Project Management Office / Operations.

## **Reporting Manager**

PMO Lead, Operations Manager, or Company Management.

## **Required Skills**

* Project planning  
* SRS and scope management  
* Stakeholder communication  
* Risk management  
* Resource planning  
* Change management  
* Progress reporting  
* Delivery governance

## **Availability**

Available throughout the project’s primary business hours.

## **Working Hours**

Organization business calendar, adjusted for client meetings when necessary.

## **Project Access**

Full access to assigned projects, including:

* Requirements  
* SRS  
* Phases  
* Milestones  
* Tickets  
* Risks  
* Follow-ups  
* QA reports  
* Change requests  
* Releases  
* Client communication

Should not have direct access to production secrets unless separately authorized.

## **Approval Authority**

May approve:

* Project plans  
* Phase plans  
* Internal priorities  
* Progress reports  
* Project-level risks  
* Change-impact submissions  
* Client update drafts  
* Project holds

Joint approval required for:

* Final scope  
* Timeline commitments  
* Production releases  
* Project completion  
* Major change requests  
* Cancellation

## **Notification Preferences**

* Immediate critical blocker notifications  
* Approval requests  
* Milestone-risk alerts  
* Overdue follow-up alerts  
* Daily project-health digest  
* Weekly portfolio report

---

# **7\. PM Agent**

## **Role**

Assists the Human PM by analyzing requirements, preparing SRS drafts, creating phases and tickets, tracking progress, and generating reports.

## **Department**

Project Management Office.

## **Reporting Manager**

Human Project Manager.

## **Required Skills**

* Requirement completeness analysis  
* SRS generation  
* Roadmap generation  
* Phase planning  
* Risk identification  
* Ticket drafting  
* Progress summarization  
* Change-impact coordination

## **Availability**

Continuous system availability.

## **Working Hours**

Can process internally at any time. Notifications and communications follow configured business calendars.

## **Project Access**

Access to all records within assigned projects, excluding secrets and restricted commercial data.

## **Approval Authority**

May automatically:

* Draft documents  
* Create proposed phases  
* Generate draft tickets  
* Create risks  
* Request clarification  
* Generate progress reports  
* Create follow-ups

Cannot approve:

* Final scope  
* Final timeline  
* Pricing  
* Production deployment  
* Project closure

## **Notification Preferences**

* Requirement updates  
* TL responses  
* Phase-status changes  
* Ticket delays  
* Risk-threshold events  
* Client approval responses

---

# **8\. Human Team Lead**

## **Role**

Owns technical planning, task breakdown, technical assignments, code quality, technical risk, and development coordination.

## **Department**

Engineering.

## **Reporting Manager**

Engineering Manager, CTO, or Human Project Manager depending on organization structure.

## **Required Skills**

* Software architecture  
* Technical estimation  
* Code review  
* Team leadership  
* Database and API design  
* Security awareness  
* Troubleshooting  
* Technical risk management

## **Availability**

Available during team working hours and critical release windows.

## **Working Hours**

Engineering business calendar, with optional on-call coverage.

## **Project Access**

Full technical access to assigned projects:

* SRS  
* Technical documents  
* Tickets  
* Repositories  
* Test environments  
* QA bugs  
* Release plans  
* Deployment records

Production access must be separately assigned.

## **Approval Authority**

May approve:

* Technical breakdown  
* Ticket readiness  
* Team assignments  
* Code reviews  
* Technical estimates  
* Staging readiness  
* Development completion  
* Technical architecture within authority

Joint approval required for:

* Major architecture changes  
* Production deployment  
* Major infrastructure changes  
* Scope-impacting technical decisions

## **Notification Preferences**

* Developer blockers  
* Code review requests  
* Failed builds  
* QA failures  
* Security warnings  
* Assignment acknowledgments  
* Deployment events

---

# **9\. TL Agent**

## **Role**

Supports the Human TL with technical analysis, task breakdown, assignment recommendations, progress tracking, and blocker coordination.

## **Department**

Engineering.

## **Reporting Manager**

Human Team Lead.

## **Required Skills**

* Technical requirement analysis  
* Architecture recommendation  
* Effort estimation  
* Ticket decomposition  
* Skill-based assignment  
* Dependency identification  
* Code-review assistance  
* Blocker analysis

## **Availability**

Continuous system availability.

## **Project Access**

Access to assigned project requirements, tickets, team workload, technical documents, QA defects, and approved repository metadata.

## **Approval Authority**

May automatically:

* Generate technical subtasks  
* Recommend assignees  
* Request clarification  
* Track blockers  
* Route work to QA  
* Prepare technical summaries

Cannot independently:

* Approve major architecture  
* Merge protected code  
* Change project scope  
* Deploy to production

## **Notification Preferences**

* New PM handovers  
* Developer blockers  
* Assignment rejections  
* QA failures  
* Architecture review requests  
* Overdue technical tasks

---

# **10\. Frontend Developer**

## **Role**

Implements user interfaces, frontend logic, API integrations, validation, and responsive behavior.

## **Department**

Engineering / Frontend.

## **Reporting Manager**

Human Team Lead or Frontend Lead.

## **Required Skills**

* React or Next.js  
* TypeScript  
* HTML and CSS  
* UI frameworks  
* API integration  
* State management  
* Responsive design  
* Accessibility  
* Frontend testing

## **Availability**

Based on assigned project capacity.

Example:

Available: 60%  
Current allocation: 40%  
Daily capacity: 8 hours

## **Working Hours**

Configured employee calendar and time zone.

## **Project Access**

* Assigned project  
* Assigned modules  
* Approved designs  
* Relevant APIs  
* Development and test environments  
* Related bugs and test cases

## **Approval Authority**

May approve:

* Own implementation plan  
* Routine technical decisions within assigned ticket  
* Developer-level completion submission

Cannot approve:

* Final UI design  
* Architecture changes  
* Production deployment  
* Scope changes  
* Own final code review where independent review is required

## **Notification Preferences**

* Ticket assignments  
* Clarifications  
* Design updates  
* API dependency updates  
* Code-review feedback  
* QA bugs  
* Due-date reminders

---

# **11\. Backend Developer**

## **Role**

Implements APIs, business logic, databases, integrations, authentication, validation, and server-side functionality.

## **Department**

Engineering / Backend.

## **Reporting Manager**

Human Team Lead or Backend Lead.

## **Required Skills**

* Python, .NET, Node.js, or approved backend stack  
* API development  
* Database design  
* Authentication and authorization  
* Security  
* Integration development  
* Unit and integration testing  
* Performance optimization

## **Availability**

Recorded as hours or allocation percentage per project.

## **Working Hours**

Configured employee calendar.

## **Project Access**

* Assigned repositories  
* Development database  
* API documentation  
* Integration documentation  
* Assigned tickets  
* Test environment logs

Production access should remain restricted.

## **Approval Authority**

May approve routine implementation decisions inside assigned scope.

Requires TL approval for:

* Schema changes  
* Authentication changes  
* New third-party services  
* Major API changes  
* Architecture changes  
* Destructive operations

## **Notification Preferences**

* Ticket assignments  
* Technical clarifications  
* Integration changes  
* Failed builds  
* Code-review requests  
* QA defects  
* Database migration alerts

---

# **12\. Full-Stack Developer**

## **Role**

Handles combined frontend and backend functionality for assigned modules.

## **Department**

Engineering / Full Stack.

## **Reporting Manager**

Human Team Lead.

## **Required Skills**

* Frontend framework  
* Backend framework  
* Database  
* API design  
* Authentication  
* Testing  
* Deployment awareness

## **Availability**

Assigned based on cross-functional project capacity.

## **Working Hours**

Configured employee calendar.

## **Project Access**

Frontend and backend resources for assigned project modules.

## **Approval Authority**

Same limitations as Frontend and Backend Developers.

## **Notification Preferences**

Combined frontend, backend, QA, and integration notifications relevant to assigned tickets.

---

# **13\. Mobile Developer**

## **Role**

Builds and maintains Android and iOS application functionality.

## **Department**

Engineering / Mobile.

## **Reporting Manager**

Human Team Lead or Mobile Lead.

## **Required Skills**

* React Native, Flutter, Swift, or Kotlin  
* Mobile API integration  
* Push notifications  
* Device permissions  
* Mobile build processes  
* App Store and Play Store requirements  
* Mobile testing

## **Availability**

Configured by project allocation.

## **Working Hours**

Employee calendar, with special availability for release submissions where required.

## **Project Access**

* Mobile source code  
* Mobile designs  
* API documentation  
* Test builds  
* App-store testing environments  
* Assigned bugs and test cases

## **Approval Authority**

May prepare builds and implementation.

Requires approval for:

* Production store submission  
* Signing certificates  
* Production secrets  
* Permission changes  
* Major architecture changes

## **Notification Preferences**

* Mobile ticket assignments  
* API changes  
* Build failures  
* Device-specific QA bugs  
* Store review updates  
* Release approvals

---

# **14\. Developer Agent**

## **Role**

Supports developers by analyzing tickets, generating implementation plans, drafting code or tests, documenting work, and identifying blockers.

## **Department**

Engineering.

## **Reporting Manager**

Assigned Human Developer or Human TL.

## **Required Skills**

Configured by specialization:

* Frontend Agent  
* Backend Agent  
* Full-Stack Agent  
* Mobile Agent  
* Database Agent

## **Availability**

Continuous system availability, subject to workload and cost limits.

## **Working Hours**

Can operate continuously, but assignments and notifications follow project calendars.

## **Project Access**

Only assigned tickets and relevant project context.

## **Approval Authority**

May:

* Generate code drafts  
* Generate tests  
* Suggest fixes  
* Update draft technical notes  
* Report blockers

Cannot:

* Merge protected code  
* deploy to production  
* access unapproved secrets  
* change requirements  
* close QA failures

## **Notification Preferences**

System-triggered tasks, code-review feedback, test failures, and clarification responses.

---

# **15\. UI/UX Designer**

## **Role**

Creates user flows, wireframes, visual interfaces, design systems, and developer-ready specifications.

## **Department**

Design.

## **Reporting Manager**

Design Lead, Human TL, or Human PM depending on project structure.

## **Required Skills**

* User research  
* User flows  
* Wireframing  
* UI design  
* Prototyping  
* Design systems  
* Responsive design  
* Accessibility  
* Developer handoff

## **Availability**

Recorded by project allocation and active design workload.

## **Working Hours**

Configured design department calendar.

## **Project Access**

* Requirements  
* User roles and workflows  
* Branding  
* Design tickets  
* Client feedback  
* Relevant developer questions

## **Approval Authority**

May approve internal design completeness.

Final approval belongs to:

* Design Lead  
* PM or Product Owner  
* Client where required

## **Notification Preferences**

* Design assignments  
* Requirement changes  
* Client feedback  
* Developer clarification  
* QA visual defects  
* Approval reminders

---

# **16\. Graphic Designer**

## **Role**

Creates logos, illustrations, icons, marketing assets, presentation materials, and branded graphics.

## **Department**

Design / Creative.

## **Reporting Manager**

Design Lead or PM.

## **Required Skills**

* Graphic design  
* Branding  
* Illustration  
* Iconography  
* Image editing  
* Marketing design  
* File preparation  
* Licensing awareness

## **Availability**

Tracked through project and creative workload.

## **Working Hours**

Configured department calendar.

## **Project Access**

Only relevant project branding, content, references, and design tasks.

## **Approval Authority**

May approve internal asset readiness.

Client-facing or brand-changing work requires human and client approval.

## **Notification Preferences**

* Asset requests  
* Content changes  
* Branding feedback  
* Approval decisions  
* Delivery deadlines

---

# **17\. Designer Agent**

## **Role**

Supports designers by analyzing user flows, preparing wireframe concepts, checking consistency, and generating design specifications.

## **Department**

Design.

## **Reporting Manager**

Human UI/UX Designer or Design Lead.

## **Required Skills**

* UX analysis  
* Screen inventory  
* Design-system consistency  
* Responsive specifications  
* Accessibility checking  
* Design documentation

## **Availability**

Continuous system availability.

## **Project Access**

Approved project requirements, design references, branding, and assigned design tickets.

## **Approval Authority**

May draft and recommend only.

Cannot approve final designs, brand changes, or client submissions.

## **Notification Preferences**

* New design tickets  
* Requirement revisions  
* Developer questions  
* QA design defects  
* Human review feedback

---

# **18\. QA Engineer**

## **Role**

Validates functionality, requirements, integrations, usability, regressions, and release readiness.

## **Department**

Quality Assurance.

## **Reporting Manager**

QA Lead or Human Team Lead.

## **Required Skills**

* Test planning  
* Functional testing  
* API testing  
* Regression testing  
* Browser and device testing  
* Bug reporting  
* Test automation  
* Requirement traceability

## **Availability**

Capacity should consider active testing cycles and release schedules.

## **Working Hours**

QA calendar with additional release-window availability where required.

## **Project Access**

* Requirements  
* Acceptance criteria  
* Test environments  
* Builds  
* Test data  
* Designs  
* Tickets  
* Bug records  
* Release notes

## **Approval Authority**

May approve:

* Test-case completeness  
* Bug validation  
* Retest results  
* QA pass for normal tickets

QA Lead approval may be required for:

* Production release  
* Acceptance of known critical issues  
* Test waivers  
* Final project quality sign-off

## **Notification Preferences**

* Ready-for-QA tickets  
* Build availability  
* Bug-fix submissions  
* Requirement changes  
* Deployment schedules  
* Critical defect alerts

---

# **19\. QA Agent**

## **Role**

Generates test cases, analyzes requirements, records test evidence, prepares bug reports, and supports regression tracking.

## **Department**

Quality Assurance.

## **Reporting Manager**

Human QA Engineer or QA Lead.

## **Required Skills**

* Test-case generation  
* Acceptance-criteria validation  
* Automated test execution  
* Defect classification  
* Regression analysis  
* Requirement coverage analysis

## **Availability**

Continuous system availability.

## **Project Access**

Assigned requirements, test cases, builds, QA tickets, bugs, and approved test data.

## **Approval Authority**

May record automated test results and recommend pass or fail.

Cannot independently approve:

* Production release  
* Known critical defects  
* Test waivers  
* Final quality closure

## **Notification Preferences**

* QA submissions  
* New builds  
* Fix-ready bugs  
* Test-data availability  
* Requirement updates  
* Release deadlines

---

# **20\. DevOps Engineer**

## **Role**

Manages infrastructure, CI/CD, environments, monitoring, backups, deployments, and rollback operations.

## **Department**

DevOps / Infrastructure.

## **Reporting Manager**

DevOps Lead, Engineering Manager, or CTO.

## **Required Skills**

* Cloud infrastructure  
* Docker  
* CI/CD  
* Networking  
* Security  
* Monitoring  
* Backup and recovery  
* Database deployment  
* Incident management

## **Availability**

Normal business hours plus configurable on-call schedule.

## **Working Hours**

Infrastructure calendar and emergency on-call rotation.

## **Project Access**

* Approved infrastructure  
* CI/CD pipelines  
* Development and staging environments  
* Production environments where authorized  
* Secret manager references  
* Monitoring and deployment logs

## **Approval Authority**

May approve:

* Routine development-environment actions  
* Approved staging deployments  
* Infrastructure checks

Human approval required for:

* Production deployment  
* Rollback  
* Production migration  
* DNS or firewall changes  
* Destructive infrastructure operations  
* Cost-impacting scaling

## **Notification Preferences**

* Build failures  
* Deployment requests  
* Infrastructure health alerts  
* Backup failures  
* Security incidents  
* Production errors  
* Release-window reminders

---

# **21\. DevOps Agent**

## **Role**

Automates environment validation, build monitoring, deployment preparation, health checks, and operational reporting.

## **Department**

DevOps / Infrastructure.

## **Reporting Manager**

Human DevOps Engineer or DevOps Lead.

## **Required Skills**

* Pipeline execution  
* Environment validation  
* Monitoring analysis  
* Backup verification  
* Deployment checklist validation  
* Incident detection

## **Availability**

Continuous system availability.

## **Project Access**

Approved pipeline, environment, log, and deployment metadata.

Secrets should be accessed only through authorized secret-management tools.

## **Approval Authority**

May:

* Run approved checks  
* Build artifacts  
* Deploy to approved development environments  
* Prepare staging or production deployment  
* Generate rollback recommendations

Cannot independently:

* Deploy to production  
* rotate production secrets  
* change DNS or firewall rules  
* delete infrastructure  
* execute destructive migrations

## **Notification Preferences**

System events, failed builds, release approvals, infrastructure alerts, and rollback instructions.

---

# **22\. Client Administrator**

## **Role**

Manages the client organization’s users and project visibility within the client portal.

## **Department**

External Client Organization.

## **Reporting Manager**

Client Sponsor or Product Owner.

## **Required Skills**

* Basic project portal usage  
* Stakeholder coordination  
* Document review  
* User management

## **Availability**

Defined by client business hours.

## **Working Hours**

Client time zone and business calendar.

## **Project Access**

* Assigned client projects  
* Approved project documents  
* Progress updates  
* Approval requests  
* Deliverables  
* Client-visible risks and issues

No access to internal-only discussions, code, secrets, employee records, or internal estimates.

## **Approval Authority**

May approve client-side:

* SRS  
* Designs  
* Deliverables  
* Change requests  
* UAT results  
* Release timing  
* Project completion

Authority must be configured per project.

## **Notification Preferences**

* Email and portal notifications  
* Approval requests  
* Progress reports  
* Client decisions required  
* Milestone updates  
* Release notifications

---

# **23\. Client Approver / Product Owner**

## **Role**

Provides business decisions, requirements confirmation, priority decisions, and formal acceptance.

## **Department**

External Client Organization.

## **Reporting Manager**

Client Sponsor or Executive Stakeholder.

## **Required Skills**

* Business-domain knowledge  
* Decision authority  
* Product understanding  
* Requirement prioritization  
* Acceptance review

## **Availability**

Configured based on agreed response SLAs.

## **Working Hours**

Client calendar and time zone.

## **Project Access**

* Requirements  
* SRS  
* Designs  
* Roadmap  
* Client updates  
* UAT  
* Change requests  
* Release and completion approvals

## **Approval Authority**

May approve:

* Business requirements  
* Scope  
* User experience  
* Change requests  
* UAT  
* Release  
* Completion

Commercial approval may require a separate client sponsor.

## **Notification Preferences**

* Approval requests  
* Reminder notifications  
* Change-impact summaries  
* Milestone reviews  
* Client decisions required

---

# **24\. Client Viewer**

## **Role**

Views approved project information without editing or approval authority.

## **Department**

External Client Organization.

## **Reporting Manager**

Client Administrator.

## **Required Skills**

Basic portal usage.

## **Availability and Working Hours**

Controlled by client organization settings.

## **Project Access**

Read-only access to selected:

* Progress updates  
* Documents  
* Milestones  
* Release notes  
* Deliverables

## **Approval Authority**

None.

## **Notification Preferences**

Optional progress and release notifications.

---

# **25\. Orchestrator Agent**

## **Role**

Coordinates communication, assignments, workflow transitions, reminders, escalations, and agent execution.

## **Department**

Cross-Functional System Operations.

## **Reporting Manager**

System Admin or Operations Manager.

## **Required Skills**

* Workflow routing  
* SLA management  
* Agent coordination  
* Escalation handling  
* Dependency tracking  
* Approval validation  
* Audit logging

## **Availability**

Continuous system availability.

## **Working Hours**

Continuous execution, while respecting role and client business calendars.

## **Project Access**

Workflow metadata for all authorized projects. It should disclose only the minimum required context to each operational agent.

## **Approval Authority**

May enforce approved rules but cannot approve:

* Pricing  
* Scope  
* Architecture  
* QA sign-off  
* Production deployment  
* Cancellation  
* Project closure

## **Notification Preferences**

* Workflow failures  
* Missing owners  
* SLA breaches  
* Approval delays  
* Agent errors  
* Conflicting assignments  
* Security violations

---

# **26\. Initial Reporting Structure**

| Role | Default Reporting Manager |
| ----- | ----- |
| Human Business Developer | BD Manager |
| BD Agent | Human Business Developer |
| Human Project Manager | PMO Lead / Operations Manager |
| PM Agent | Human Project Manager |
| Human Team Lead | Engineering Manager / CTO |
| TL Agent | Human Team Lead |
| Frontend Developer | Human Team Lead |
| Backend Developer | Human Team Lead |
| Full-Stack Developer | Human Team Lead |
| Mobile Developer | Human Team Lead |
| Developer Agent | Assigned Developer or Human TL |
| UI/UX Designer | Design Lead |
| Graphic Designer | Design Lead |
| Designer Agent | Human Designer |
| QA Engineer | QA Lead |
| QA Agent | Human QA Engineer / QA Lead |
| DevOps Engineer | DevOps Lead |
| DevOps Agent | Human DevOps Engineer |
| Orchestrator Agent | System Admin / Operations Manager |
| Client Administrator | Client Sponsor |
| Client Approver | Client Sponsor |
| Client Viewer | Client Administrator |

---

# **27\. Availability Structure**

Availability should not be a single text field. Store structured information:

Employment Status  
Current Availability Status  
Weekly Capacity Hours  
Allocated Hours  
Remaining Capacity  
Allocation Percentage  
Working Calendar  
Time Zone  
Leave Dates  
On-Call Status  
Temporary Unavailability Reason  
Expected Return Date

## **Availability Statuses**

Available  
Partially Available  
Fully Allocated  
Busy  
On Leave  
Unavailable  
On Call  
Inactive

## **Assignment Rule**

An agent or human should only receive work when:

Required Skill Matches  
AND Project Access Exists  
AND Remaining Capacity Is Sufficient  
AND Working Calendar Supports Deadline  
AND No Permission Restriction Exists

---

# **28\. Skills Structure**

Skills should use a separate configurable catalog.

Skill ID  
Skill Name  
Skill Category  
Proficiency Level  
Years of Experience  
Last Used Date  
Certification  
Verified By  
Active / Inactive

## **Skill Categories**

* Business development  
* Project management  
* Requirement analysis  
* Frontend  
* Backend  
* Mobile  
* Database  
* UI/UX  
* Graphic design  
* QA  
* Test automation  
* DevOps  
* Cloud  
* Security  
* Integration  
* Client communication  
* Industry knowledge

## **Proficiency Levels**

Level 1 – Beginner  
Level 2 – Intermediate  
Level 3 – Advanced  
Level 4 – Expert  
Level 5 – Lead / Architect

---

# **29\. Project Access Levels**

| Access Level | Permissions |
| ----- | ----- |
| No Access | Cannot view the project |
| Summary View | View high-level progress only |
| Read Only | View authorized project records |
| Contributor | Create and update assigned records |
| Manager | Manage project records and assignments |
| Approver | Approve configured project actions |
| Technical Admin | Manage technical configuration |
| Project Admin | Full project-level control |
| Organization Admin | Organization-wide administration |

Access should also be limited by module:

Requirements  
Documents  
Tickets  
Source Code  
QA  
Risks  
Commercial Information  
Client Communication  
Deployments  
Audit Logs

---

# **30\. Approval Authority Structure**

Approval authority should be stored as configurable permissions.

Examples:

queries.qualify  
requirements.approve  
srs.approve  
projects.baseline  
tickets.assign  
architecture.approve  
designs.approve  
code\_review.approve  
qa.approve  
change\_request.approve  
pricing.approve  
deployment.approve  
project.complete  
project.cancel

Each approval permission should contain:

* Role  
* Project  
* Maximum financial value  
* Maximum change impact  
* Environment  
* Effective date  
* Expiry date  
* Delegation rules

---

# **31\. Notification Preferences Structure**

Each user should configure:

Notification Type  
Channel  
Priority Threshold  
Immediate or Digest  
Working-Hours Only  
Quiet Hours  
Escalation Notifications  
Project Filters  
Daily Summary  
Weekly Summary

## **Supported Channels**

In-App  
Email  
Slack  
Microsoft Teams  
SMS  
WhatsApp  
Push Notification

## **Recommended Defaults**

| Event | Default Channel |
| ----- | ----- |
| New assignment | In-app and email |
| Routine status update | In-app |
| Reminder | In-app and email |
| Overdue task | In-app, email, and manager notification |
| Critical blocker | Immediate email, in-app, and team channel |
| Production incident | All authorized emergency channels |
| Approval request | In-app and email |
| Client response | In-app and email |
| Daily summary | Email or team channel |
| Weekly report | Email |

---

# **32\. Human-Agent Pairing Rule**

Every operational agent must have a human supervisor.

BD Agent → Human Business Developer  
PM Agent → Human Project Manager  
TL Agent → Human Team Lead  
Developer Agent → Human Developer or TL  
Designer Agent → Human Designer  
QA Agent → Human QA Engineer  
DevOps Agent → Human DevOps Engineer  
Orchestrator Agent → System Admin or Operations Manager

When an agent:

* Exceeds its authority  
* Lacks confidence  
* Detects conflicting instructions  
* Identifies a high-risk issue  
* Encounters missing information  
* Cannot complete a task  
* Reaches the maximum retry limit

it must create a structured follow-up for its human supervisor.

This structure provides the data required for skill-based assignments, capacity planning, project authorization, notification routing, approval gates, and multi-level escalation.

