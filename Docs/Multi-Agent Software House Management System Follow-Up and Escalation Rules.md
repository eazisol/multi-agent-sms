# **Follow-Up and Escalation Rules**

## **1\. Purpose**

The follow-up engine ensures that every request, clarification, approval, blocker, assignment, and client response has:

* A responsible owner  
* A response deadline  
* Automated reminders  
* A defined escalation path  
* A maximum escalation level  
* Clear closure conditions  
* A complete audit history

These rules must be stored as configurable workflow settings rather than embedded directly in application code.

---

# **2\. Standard Escalation Levels**

| Level | Escalation Target | Purpose |
| ----- | ----- | ----- |
| Level 0 | Assigned agent or human | Initial owner responsible for responding |
| Level 1 | Parent role or direct supervisor | First operational escalation |
| Level 2 | Human department lead | Department-level intervention |
| Level 3 | PM, Operations Manager, or Management | Project or organizational intervention |
| Level 4 | Senior Management, Security Lead, or Executive | Critical business, production, security, or contractual risk |

Routine follow-ups should normally stop at Level 2 or Level 3\. Level 4 should be reserved for critical issues.

---

# **3\. Follow-Up Types and Default Rules**

## **3.1 New Client Inquiry Response**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | BD Agent or Orchestrator Agent |
| Received by | Human BD |
| Expected response time | 2 business hours |
| First reminder | After 1 business hour |
| Second reminder | At 2 business hours |
| First escalation | BD Manager |
| Second escalation | Operations Manager |
| Maximum escalation level | Level 3 |
| Closure condition | Human BD responds, assigns the inquiry, rejects it with reason, or closes it as invalid |

### **Flow**

Inquiry Created  
→ Assigned to Human BD  
→ Reminder After 1 Hour  
→ Overdue After 2 Hours  
→ Escalated to BD Manager  
→ Escalated to Operations Manager  
→ Responded / Reassigned / Rejected  
→ Closed

---

## **3.2 Client Requirement Information**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | BD Agent |
| Received by | Client |
| Expected response time | 2 business days |
| First reminder | After 1 business day |
| Second reminder | After 2 business days |
| First escalation | Human BD |
| Second escalation | BD Manager or PM |
| Maximum escalation level | Level 3 |
| Closure condition | Client provides the required information, confirms the requirement summary, withdraws the request, or the inquiry is marked dormant |

### **Closure outcomes**

Information Received  
→ Requirement Record Updated  
→ Follow-Up Resolved  
→ Closed

or:

No Response After Final Follow-Up  
→ Escalated  
→ Opportunity Marked Dormant / On Hold  
→ Closed

---

## **3.3 BD-to-PM Handover Review**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | BD Agent |
| Received by | PM Agent or Human PM |
| Expected response time | 4 working hours |
| First reminder | After 2 working hours |
| Second reminder | At 4 working hours |
| First escalation | Human PM |
| Second escalation | PM Department Lead |
| Maximum escalation level | Level 2 |
| Closure condition | Handover accepted, returned with clarification questions, or rejected with reason |

---

## **3.4 PM Clarification to BD**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | PM Agent |
| Received by | BD Agent or Human BD |
| Expected response time | 4 working hours |
| First reminder | After 2 working hours |
| Second reminder | At 4 working hours |
| First escalation | Human BD and Human PM |
| Second escalation | BD Manager or PM Lead |
| Maximum escalation level | Level 3 |
| Closure condition | Required clarification is provided and accepted by PM, or the project is placed on hold |

When client input is required, the follow-up may create a linked child follow-up:

PM Clarification  
→ BD Follow-Up  
→ Client Follow-Up  
→ Client Response  
→ BD Response  
→ PM Confirmation

The parent follow-up should remain open until the complete response chain is resolved.

---

## **3.5 PM-to-TL Technical Handover**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | PM Agent |
| Received by | TL Agent or Human TL |
| Expected response time | 1 business day |
| First reminder | After 4 working hours |
| Second reminder | At 1 business day |
| First escalation | Human TL |
| Second escalation | Engineering Manager |
| Maximum escalation level | Level 3 |
| Closure condition | TL accepts the handover, requests clarification, or rejects it with a documented technical reason |

---

## **3.6 Ticket Assignment Acknowledgment**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | TL Agent |
| Received by | Developer, Designer, QA, or DevOps team member |
| Expected response time | 2 working hours |
| First reminder | After 1 working hour |
| Second reminder | At 2 working hours |
| First escalation | Human TL |
| Second escalation | PM |
| Maximum escalation level | Level 2 |
| Closure condition | Assignee acknowledges the ticket, rejects it with a valid reason, or the ticket is reassigned |

---

## **3.7 Developer Blocker**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | Developer Agent or Human Developer |
| Received by | TL Agent or Human TL |
| Expected response time | 4 working hours |
| First reminder | After 2 working hours |
| Second reminder | At 4 working hours |
| First escalation | Human PM |
| Second escalation | Engineering Manager or Department Manager |
| Maximum escalation level | Level 3 |
| Closure condition | Blocker resolved, workaround approved, dependency provided, ticket reassigned, or project-level decision recorded |

### **Critical blocker rule**

A blocker should be treated as critical when it:

* Stops an entire development phase  
* Affects production  
* Risks data loss  
* Creates a security concern  
* Blocks multiple team members  
* Threatens a committed delivery

Critical blocker timing:

Created  
→ Immediate Notification to TL  
→ Reminder After 30 Minutes  
→ Escalation After 1 Hour  
→ Management Escalation After 2 Hours

---

## **3.8 Requirement Clarification from Developer**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | Developer Agent |
| Received by | TL Agent |
| Expected response time | 4 working hours |
| First reminder | After 2 working hours |
| First escalation | Human TL |
| Second escalation | PM |
| Maximum escalation level | Level 3 |
| Closure condition | Requirement is clarified, ticket acceptance criteria are updated, or work is paused with a documented reason |

The developer should not contact the client directly unless explicitly authorized.

---

## **3.9 Design Clarification**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | Developer Agent, QA Agent, or TL Agent |
| Received by | Designer Agent or Human Designer |
| Expected response time | 4 working hours |
| First reminder | After 2 working hours |
| First escalation | Human Designer or TL |
| Second escalation | PM |
| Maximum escalation level | Level 2 |
| Closure condition | Design clarification is provided, design is revised, or PM approves an alternative |

---

## **3.10 Design Approval**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | Designer Agent |
| Received by | PM, Product Owner, or Client |
| Expected response time | 2 business days |
| First reminder | After 1 business day |
| Second reminder | At 2 business days |
| First escalation | Human PM |
| Second escalation | Human BD or Product Owner |
| Maximum escalation level | Level 3 |
| Closure condition | Design is approved, rejected with feedback, or project is placed on hold |

---

## **3.11 Code Review Request**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | Developer Agent |
| Received by | Human TL or assigned code reviewer |
| Expected response time | 4 working hours |
| First reminder | After 2 working hours |
| Second reminder | At 4 working hours |
| First escalation | Human TL |
| Second escalation | Engineering Manager or PM |
| Maximum escalation level | Level 2 |
| Closure condition | Code is approved, changes are requested, or another reviewer is assigned |

---

## **3.12 Development Submission to QA**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | TL Agent or Developer Agent |
| Received by | QA Agent or Human QA |
| Expected response time | 4 working hours |
| First reminder | After 2 working hours |
| First escalation | QA Lead |
| Second escalation | TL and PM |
| Maximum escalation level | Level 3 |
| Closure condition | QA starts testing, rejects the submission as incomplete, or the ticket is reassigned to development |

---

## **3.13 QA Bug Assignment**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | QA Agent |
| Received by | Developer through TL |
| Expected response time | Based on bug severity |
| First reminder | Based on severity |
| First escalation | Human TL |
| Second escalation | PM or Engineering Manager |
| Maximum escalation level | Level 3 |
| Closure condition | Bug is fixed and submitted for retesting, rejected with evidence, or accepted as a known issue by an authorized human |

### **Severity-based SLA**

| Severity | Acknowledgment | Resolution Target | Reminder |
| ----- | ----- | ----- | ----- |
| Critical | 30 minutes | 4 working hours | Every hour |
| High | 2 working hours | 1 business day | Every 4 hours |
| Medium | 4 working hours | 3 business days | Daily |
| Low | 1 business day | According to sprint plan | Every 2 business days |

---

## **3.14 QA Retesting**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | Developer Agent after bug fix |
| Received by | QA Agent |
| Expected response time | 1 business day |
| First reminder | After 4 working hours |
| First escalation | QA Lead |
| Second escalation | PM |
| Maximum escalation level | Level 2 |
| Closure condition | Bug passes and is closed, fails and is reopened, or is accepted as a known issue |

---

## **3.15 Progress Update from Team to TL**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | Orchestrator Agent |
| Received by | Developer, Designer, QA, or DevOps team member |
| Expected response time | Before the configured daily reporting time |
| First reminder | 1 hour before deadline |
| Second reminder | At deadline |
| First escalation | Human TL |
| Second escalation | PM |
| Maximum escalation level | Level 2 |
| Closure condition | Progress, remaining effort, blocker status, and next action are submitted |

---

## **3.16 TL Progress Report to PM**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | PM Agent or Orchestrator |
| Received by | TL Agent |
| Expected response time | Same business day |
| First reminder | After 4 working hours |
| First escalation | Human TL |
| Second escalation | Engineering Manager |
| Maximum escalation level | Level 2 |
| Closure condition | Complete project progress report is provided and accepted by PM |

---

## **3.17 PM Progress Report to BD**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | PM Agent |
| Received by | BD Agent or Human BD |
| Expected response time | 4 working hours |
| First reminder | After 2 working hours |
| First escalation | Human PM and Human BD |
| Second escalation | Department managers |
| Maximum escalation level | Level 2 |
| Closure condition | BD confirms receipt and prepares or sends the approved client update |

---

## **3.18 Client Progress Update Response**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | BD Agent |
| Received by | Client |
| Expected response time | 2 business days when a response is required |
| First reminder | After 1 business day |
| Second reminder | At 2 business days |
| First escalation | Human BD |
| Second escalation | Human PM |
| Maximum escalation level | Level 3 |
| Closure condition | Client responds, confirms receipt, approves the deliverable, or the project is placed on hold |

---

## **3.19 Client Approval Request**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | BD Agent or PM Agent |
| Received by | Client or Product Owner |
| Expected response time | 3 business days |
| First reminder | After 1 business day |
| Second reminder | After 2 business days |
| Final reminder | At 3 business days |
| First escalation | Human BD |
| Second escalation | Human PM |
| Maximum escalation level | Level 3 |
| Closure condition | Approved, rejected with comments, withdrawn, or project placed on hold |

Examples include:

* SRS approval  
* Design approval  
* Milestone approval  
* UAT approval  
* Change request approval  
* Production release approval

---

## **3.20 Change Request Impact Analysis**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | PM Agent |
| Received by | TL Agent, QA Agent, Designer Agent, and relevant Developers |
| Expected response time | Small: 1 day; Medium: 3 days; Complex: 5 days |
| First reminder | At 50% of SLA |
| Second reminder | At SLA deadline |
| First escalation | Human TL |
| Second escalation | PM or Engineering Manager |
| Maximum escalation level | Level 3 |
| Closure condition | Technical, timeline, quality, design, and cost impacts are documented |

---

## **3.21 Change Request Approval**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | PM Agent |
| Received by | Client, PM, BD, TL, or Management depending on impact |
| Expected response time | 2 business days |
| First reminder | After 1 business day |
| First escalation | Human PM |
| Second escalation | Human BD or Management |
| Maximum escalation level | Level 3 |
| Closure condition | Change is approved, rejected, deferred, or withdrawn |

No development should start until the approval follow-up is resolved, except for authorized emergency work.

---

## **3.22 Missing Access or Credentials**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | Developer, TL, QA, or DevOps Agent |
| Received by | PM, Client, Admin, or DevOps owner |
| Expected response time | 4 working hours |
| First reminder | After 2 working hours |
| First escalation | Human PM |
| Second escalation | Client owner or Management |
| Maximum escalation level | Level 3 |
| Closure condition | Access is provided and verified, an alternative is approved, or affected work is formally placed on hold |

Credentials must never be sent through the follow-up message itself. The follow-up should reference a secure credential-sharing method.

---

## **3.23 Staging Deployment Request**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | TL Agent |
| Received by | DevOps Agent |
| Expected response time | 4 working hours |
| First reminder | After 2 working hours |
| First escalation | Human DevOps |
| Second escalation | TL and PM |
| Maximum escalation level | Level 2 |
| Closure condition | Deployment completes successfully, fails with a documented result, or is rescheduled |

---

## **3.24 Production Deployment Approval**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | TL Agent or PM Agent |
| Received by | Authorized Human PM, Release Manager, Client, or Product Owner |
| Expected response time | Before the approved release window |
| First reminder | 4 hours before release |
| Second reminder | 1 hour before release |
| First escalation | Human PM |
| Second escalation | Operations Manager or Management |
| Maximum escalation level | Level 4 |
| Closure condition | Deployment approved, rejected, postponed, or cancelled |

Production deployment must not proceed without explicit approval.

---

## **3.25 Deployment Failure or Rollback**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | DevOps Agent |
| Received by | Human DevOps Lead, TL, and PM |
| Expected response time | Immediate |
| First reminder | After 15 minutes |
| First escalation | After 30 minutes |
| Second escalation | After 1 hour |
| Maximum escalation level | Level 4 |
| Closure condition | Deployment fixed, rollback completed, service restored, and incident report created |

---

## **3.26 Production Incident**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | Monitoring system, DevOps Agent, QA, or Support |
| Received by | DevOps Lead, TL, PM, and Security Lead where applicable |
| Expected response time | Critical: 15 minutes; High: 30 minutes |
| Reminder frequency | Every 15–30 minutes until acknowledged |
| First escalation | Engineering or DevOps Manager |
| Second escalation | Senior Management |
| Maximum escalation level | Level 4 |
| Closure condition | Service restored, impact assessed, stakeholders informed, and incident report completed |

---

## **3.27 Project Completion Approval**

| Configuration | Default Rule |
| ----- | ----- |
| Created by | PM Agent |
| Received by | Human PM, TL, QA Lead, BD, and Client |
| Expected response time | 3 business days |
| First reminder | After 1 business day |
| Second reminder | After 2 business days |
| First escalation | Human PM |
| Second escalation | Management or Client Sponsor |
| Maximum escalation level | Level 3 |
| Closure condition | Completion accepted, rejected with outstanding items, or transferred to support with approved exceptions |

---

# **4\. Priority-Based SLA Overrides**

Each follow-up type should have a default SLA, but priority may override it.

| Priority | Response-Time Multiplier | Reminder Rule |
| ----- | ----- | ----- |
| Critical | 25% of standard SLA | Frequent reminders and immediate escalation |
| High | 50% of standard SLA | Reminder at 50% and 100% |
| Normal | 100% of standard SLA | Standard configured reminders |
| Low | 150–200% of standard SLA | Less frequent reminders |

Example:

Normal Developer Blocker SLA: 4 working hours  
High Priority: 2 working hours  
Critical Priority: 1 working hour or immediate handling

---

# **5\. Configurable Follow-Up Rule Structure**

Each follow-up rule should be stored with fields such as:

Rule ID  
Rule Name  
Follow-Up Type  
Project Type  
Priority  
Source Role  
Recipient Role  
Response SLA Value  
Response SLA Unit  
Business Calendar  
First Reminder Offset  
Second Reminder Offset  
Reminder Frequency  
Maximum Reminder Count  
First Escalation Role  
Second Escalation Role  
Final Escalation Role  
Maximum Escalation Level  
Pause SLA While Waiting Externally  
Auto-Close Allowed  
Closure Conditions  
Reopen Allowed  
Notification Channels  
Active / Inactive  
Effective Date  
Created By  
Approved By  
Version

---

# **6\. Example Configuration Record**

{  
  "rule\_name": "Developer Blocker",  
  "follow\_up\_type": "developer\_blocker",  
  "source\_roles": \["developer\_agent", "developer"\],  
  "recipient\_roles": \["tl\_agent", "team\_lead"\],  
  "priority": "normal",  
  "response\_sla": {  
    "value": 4,  
    "unit": "working\_hours"  
  },  
  "reminders": \[  
    {  
      "after": 2,  
      "unit": "working\_hours",  
      "recipient": "assigned\_owner"  
    },  
    {  
      "after": 4,  
      "unit": "working\_hours",  
      "recipient": "human\_team\_lead"  
    }  
  \],  
  "escalations": \[  
    {  
      "level": 1,  
      "recipient\_role": "project\_manager"  
    },  
    {  
      "level": 2,  
      "recipient\_role": "engineering\_manager"  
    }  
  \],  
  "maximum\_escalation\_level": 3,  
  "closure\_conditions": \[  
    "blocker\_resolved",  
    "workaround\_approved",  
    "dependency\_provided",  
    "ticket\_reassigned"  
  \],  
  "sla\_pause\_conditions": \[  
    "waiting\_for\_client",  
    "waiting\_for\_external\_vendor"  
  \]  
}

---

# **7\. Business-Time Configuration**

The follow-up engine must support:

* Working days  
* Working hours  
* User and department time zones  
* Public holidays  
* Company holidays  
* Weekends  
* Emergency after-hours rules  
* Client-specific working calendars

Example:

Business Hours:  
Monday–Friday  
9:00 AM–6:00 PM  
Asia/Karachi

A four-working-hour SLA created Friday at 4:00 PM:  
2 hours counted Friday  
2 hours counted Monday  
Deadline: Monday at 11:00 AM

Critical production and security incidents should use calendar time rather than working time.

---

# **8\. SLA Pause Rules**

The SLA may pause only when the follow-up is formally moved to a permitted waiting status.

Examples:

* Waiting for Client  
* Waiting for External Vendor  
* Waiting for Approved Access  
* Waiting for Required Legal Decision

The SLA should not pause for:

* Internal workload  
* Forgotten tasks  
* Unacknowledged assignments  
* Missing internal coordination  
* Delayed internal reviews

Every pause must record:

Pause Reason  
Paused By  
Pause Start Time  
Expected Resume Date  
Responsible External Party  
Total Paused Duration

---

# **9\. Closure Rules**

A follow-up should be closed only when:

1. The required response has been received.  
2. The requester confirms the response is sufficient.  
3. The requested action has been completed.  
4. Supporting evidence is attached where required.  
5. No child follow-up remains open.  
6. The resolution reason is recorded.  
7. The audit history is complete.

## **Automatic closure**

Automatic closure may be allowed for low-risk follow-ups such as:

* Assignment acknowledgment  
* Routine progress update  
* Delivery confirmation  
* Automated environment-health confirmation

## **Human closure required**

Human confirmation should be required for:

* Client approvals  
* Change requests  
* Critical blockers  
* Security incidents  
* Production deployments  
* Contractual matters  
* Project completion

---

# **10\. Rejection and Reopening Rules**

A rejected follow-up must include:

* Rejection reason  
* Person who rejected it  
* Required correction  
* Resubmission owner  
* New response deadline

Flow:

Responded  
→ Rejected  
→ Reassigned  
→ In Progress  
→ Responded  
→ Resolved  
→ Closed

A closed follow-up may be reopened only when:

* The original resolution was incomplete  
* New evidence changes the decision  
* The same dependency becomes active again  
* An authorized human approves reopening

---

# **11\. Required System Behaviour**

The system should automatically:

* Calculate deadlines using the configured business calendar.  
* Send reminders through selected channels.  
* Mark follow-ups as overdue.  
* Trigger the correct escalation level.  
* Create linked child follow-ups when another department or the client must respond.  
* Pause and resume SLA timers according to approved rules.  
* Prevent closure while linked dependencies remain unresolved.  
* Record every status change.  
* Maintain rule version history.  
* Allow authorized administrators to modify rules without code deployment.  
* Apply different rules by client, project, department, priority, or issue severity.

This configurable follow-up engine will become the central control layer for bidirectional communication between the client, BD, PM, TL, development, design, QA, and DevOps teams.

