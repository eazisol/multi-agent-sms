# **Required Data Structure**

## **1\. Core Design Principles**

The database should use the following standards:

* Use `UUID` primary keys.  
* Store timestamps in UTC using `timestamptz`.  
* Use soft deletion for business records.  
* Maintain immutable audit logs.  
* Maintain separate status-history records.  
* Maintain document and requirement versions.  
* Use configurable status and transition tables instead of hard-coded database enums.  
* Link all user and agent actions through a common `Actor` entity.  
* Apply organization- and project-level access control.  
* Use junction tables for many-to-many relationships.  
* Store structured business information in relational columns.  
* Use `JSONB` only for flexible metadata, AI output, or integration payloads.

Not every record should require a project. For example, a client inquiry may exist before a project is created. Therefore, `project_id` should be nullable where appropriate.

---

# **2\. Common Fields**

Most business entities should contain the following fields:

id  
organization\_id  
project\_id  
status\_id  
owner\_actor\_id  
created\_by\_actor\_id  
updated\_by\_actor\_id  
created\_at  
updated\_at  
deleted\_at  
is\_deleted  
version\_number  
metadata

## **Common Field Definitions**

| Field | Purpose |
| ----- | ----- |
| `id` | Unique UUID for the record |
| `organization_id` | Separates company or tenant data |
| `project_id` | Links the record to a project when applicable |
| `status_id` | Links to configurable status definitions |
| `owner_actor_id` | Current responsible human or agent |
| `created_by_actor_id` | Human, agent, or system that created it |
| `updated_by_actor_id` | Last actor that modified it |
| `created_at` | Creation timestamp |
| `updated_at` | Last update timestamp |
| `deleted_at` | Soft-deletion timestamp |
| `is_deleted` | Indicates whether the record is archived or deleted |
| `version_number` | Optimistic concurrency and version reference |
| `metadata` | Flexible JSON information |

---

# **3\. Actor Model**

A shared `actors` table should represent humans, agents, and system services.

## **Actors**

actors  
\- id  
\- organization\_id  
\- actor\_type  
\- display\_name  
\- email  
\- status  
\- human\_user\_id  
\- agent\_id  
\- created\_at  
\- updated\_at

### **Actor Types**

human  
agent  
system  
integration

This prevents the database from needing fields such as:

created\_by\_user\_id  
created\_by\_agent\_id  
assigned\_to\_user\_id  
assigned\_to\_agent\_id

Instead, every action uses:

created\_by\_actor\_id  
assigned\_to\_actor\_id  
owner\_actor\_id

---

# **4\. CRM and Client Entities**

## **4.1 Clients**

Represents a client company, individual customer, or organization.

clients  
\- id  
\- organization\_id  
\- client\_type  
\- legal\_name  
\- display\_name  
\- industry  
\- website  
\- country  
\- timezone  
\- preferred\_language  
\- preferred\_communication\_channel  
\- account\_manager\_actor\_id  
\- status\_id  
\- source  
\- notes  
\- created\_at  
\- updated\_at  
\- deleted\_at

### **Relationships**

Client  
├── Contacts  
├── Queries  
├── Opportunities  
├── Projects  
├── Documents  
└── Messages

---

## **4.2 Contacts**

Represents individuals associated with a client.

contacts  
\- id  
\- organization\_id  
\- client\_id  
\- first\_name  
\- last\_name  
\- job\_title  
\- email  
\- phone  
\- alternate\_phone  
\- timezone  
\- preferred\_language  
\- preferred\_channel  
\- is\_primary  
\- is\_decision\_maker  
\- approval\_authority  
\- status\_id  
\- created\_at  
\- updated\_at  
\- deleted\_at

### **Relationships**

* One client can have many contacts.  
* A contact may be linked to several projects through `project_contacts`.  
* A contact may send queries, messages, approvals, and change requests.

---

## **4.3 Queries**

Represents an incoming client inquiry before it becomes an opportunity or project.

queries  
\- id  
\- organization\_id  
\- client\_id  
\- contact\_id  
\- query\_number  
\- title  
\- description  
\- source  
\- service\_category  
\- urgency  
\- priority  
\- assigned\_bd\_actor\_id  
\- qualification\_score  
\- status\_id  
\- received\_at  
\- first\_response\_at  
\- qualified\_at  
\- closed\_at  
\- closure\_reason  
\- created\_at  
\- updated\_at

### **Statuses**

New  
Assigned to BD  
Requirement Gathering  
Waiting for Client  
Qualified  
Not Qualified  
Converted to Project  
Closed

### **Relationships**

* Query belongs to a client and contact.  
* Query may create one opportunity.  
* Query may contain messages, documents, attachments, and follow-ups.

---

## **4.4 Opportunities**

Represents a qualified commercial opportunity.

opportunities  
\- id  
\- organization\_id  
\- client\_id  
\- query\_id  
\- opportunity\_number  
\- title  
\- description  
\- estimated\_value  
\- currency  
\- probability\_percentage  
\- expected\_start\_date  
\- expected\_close\_date  
\- budget\_range\_min  
\- budget\_range\_max  
\- pricing\_model  
\- bd\_owner\_actor\_id  
\- pm\_reviewer\_actor\_id  
\- status\_id  
\- lost\_reason  
\- won\_at  
\- lost\_at  
\- converted\_project\_id  
\- created\_at  
\- updated\_at

### **Suggested Statuses**

Draft  
Discovery  
Qualified  
Estimation  
Proposal Preparation  
Proposal Sent  
Negotiation  
Won  
Lost  
On Hold  
Converted

### **Relationships**

* Opportunity belongs to a client.  
* Opportunity may originate from a query.  
* A won opportunity may create one project.  
* Opportunity may contain proposals, approvals, follow-ups, and documents.

---

# **5\. Project Management Entities**

## **5.1 Projects**

Represents the complete delivery engagement.

projects  
\- id  
\- organization\_id  
\- client\_id  
\- opportunity\_id  
\- project\_code  
\- name  
\- description  
\- project\_type  
\- delivery\_model  
\- priority  
\- pm\_actor\_id  
\- tl\_actor\_id  
\- bd\_actor\_id  
\- qa\_lead\_actor\_id  
\- start\_date  
\- target\_end\_date  
\- actual\_end\_date  
\- budget  
\- currency  
\- completion\_percentage  
\- health\_status  
\- current\_phase\_id  
\- status\_id  
\- hold\_reason  
\- previous\_status\_id  
\- cancellation\_reason  
\- created\_at  
\- updated\_at  
\- completed\_at

### **Statuses**

Draft  
Requirement Review  
SRS Preparation  
Planning  
Design  
Development  
QA  
Client Review  
Deployment  
Completed  
On Hold  
Cancelled

### **Relationships**

Project  
├── Requirements  
├── Requirement Versions  
├── Phases  
├── Milestones  
├── Tickets  
├── Subtasks  
├── Assignments  
├── Follow-Ups  
├── Messages  
├── Approvals  
├── Documents  
├── Test Cases  
├── Bugs  
├── Change Requests  
├── Risks  
├── Releases  
└── Audit Logs

---

## **5.2 Project Members**

Links humans and agents to projects.

project\_members  
\- id  
\- project\_id  
\- actor\_id  
\- role\_id  
\- team\_id  
\- access\_level  
\- allocation\_percentage  
\- start\_date  
\- end\_date  
\- is\_active  
\- added\_by\_actor\_id  
\- created\_at

This table controls project visibility and responsibility.

---

## **5.3 Requirements**

Stores the current approved or working version of a requirement.

requirements  
\- id  
\- project\_id  
\- requirement\_code  
\- parent\_requirement\_id  
\- requirement\_type  
\- module  
\- title  
\- current\_description  
\- business\_purpose  
\- priority  
\- source  
\- owner\_actor\_id  
\- current\_version\_id  
\- approval\_status  
\- status\_id  
\- created\_at  
\- updated\_at

### **Requirement Types**

Business  
Functional  
Non-Functional  
Technical  
Security  
Compliance  
Integration  
Reporting  
UI/UX  
Data

### **Relationships**

* A requirement belongs to a project.  
* A requirement can have many versions.  
* A requirement may link to many tickets, test cases, bugs, and releases.  
* Requirements may have parent-child structures.

---

## **5.4 Requirement Versions**

Stores immutable snapshots of requirement changes.

requirement\_versions  
\- id  
\- requirement\_id  
\- version\_number  
\- title  
\- description  
\- business\_rules  
\- acceptance\_criteria  
\- validations  
\- assumptions  
\- dependencies  
\- change\_reason  
\- change\_request\_id  
\- created\_by\_actor\_id  
\- approval\_status  
\- approved\_by\_actor\_id  
\- approved\_at  
\- effective\_from  
\- superseded\_at  
\- created\_at

### **Rules**

* Approved versions must never be overwritten.  
* New changes create a new version.  
* Only one version should be marked current.  
* Superseded versions remain available for audit.

---

## **5.5 Phases**

Represents major delivery stages.

phases  
\- id  
\- project\_id  
\- phase\_code  
\- name  
\- description  
\- sequence\_number  
\- owner\_actor\_id  
\- planned\_start\_date  
\- planned\_end\_date  
\- actual\_start\_date  
\- actual\_end\_date  
\- completion\_percentage  
\- status\_id  
\- approval\_status  
\- created\_at  
\- updated\_at

### **Relationships**

* A project has many phases.  
* A phase has many milestones, tickets, risks, and releases.

---

## **5.6 Milestones**

Represents important delivery or approval points.

milestones  
\- id  
\- project\_id  
\- phase\_id  
\- milestone\_code  
\- title  
\- description  
\- milestone\_type  
\- owner\_actor\_id  
\- planned\_date  
\- forecast\_date  
\- actual\_date  
\- approval\_required  
\- approver\_actor\_id  
\- status\_id  
\- created\_at  
\- updated\_at

### **Milestone Types**

Internal  
Client  
Technical  
Commercial  
QA  
Release  
Payment

---

# **6\. Work Management Entities**

## **6.1 Tickets**

Represents user stories, technical work, design work, QA work, DevOps work, or bugs.

tickets  
\- id  
\- project\_id  
\- phase\_id  
\- milestone\_id  
\- parent\_ticket\_id  
\- ticket\_number  
\- ticket\_type  
\- title  
\- description  
\- priority  
\- severity  
\- estimate\_value  
\- estimate\_unit  
\- story\_points  
\- owner\_actor\_id  
\- reporter\_actor\_id  
\- reviewer\_actor\_id  
\- status\_id  
\- due\_date  
\- started\_at  
\- completed\_at  
\- definition\_of\_ready  
\- definition\_of\_done  
\- acceptance\_criteria  
\- technical\_notes  
\- created\_at  
\- updated\_at

### **Ticket Types**

Epic  
User Story  
Development  
Design  
QA  
DevOps  
Research  
Documentation  
Bug  
Change  
Support

### **Statuses**

Backlog  
Ready  
Assigned  
In Progress  
Blocked  
Code Review  
Ready for QA  
QA In Progress  
Failed QA  
Passed QA  
Done

---

## **6.2 Subtasks**

Represents smaller execution steps inside a ticket.

subtasks  
\- id  
\- project\_id  
\- ticket\_id  
\- subtask\_number  
\- title  
\- description  
\- sequence\_number  
\- owner\_actor\_id  
\- estimate\_value  
\- estimate\_unit  
\- status\_id  
\- due\_date  
\- started\_at  
\- completed\_at  
\- created\_at  
\- updated\_at

---

## **6.3 Assignments**

Maintains current and historical ownership.

assignments  
\- id  
\- organization\_id  
\- project\_id  
\- entity\_type  
\- entity\_id  
\- assigned\_actor\_id  
\- assigned\_team\_id  
\- assignment\_role  
\- allocation\_percentage  
\- assigned\_by\_actor\_id  
\- assigned\_at  
\- acknowledged\_at  
\- effective\_from  
\- effective\_to  
\- assignment\_status  
\- reassignment\_reason  
\- created\_at

### **Entity Types**

Query  
Opportunity  
Project  
Requirement  
Phase  
Milestone  
Ticket  
Subtask  
Bug  
Risk  
Follow-Up  
Change Request  
Release

Assignments should not be overwritten. When ownership changes, close the previous assignment using `effective_to` and create a new assignment record.

---

## **6.4 Ticket Dependencies**

ticket\_dependencies  
\- id  
\- project\_id  
\- predecessor\_ticket\_id  
\- successor\_ticket\_id  
\- dependency\_type  
\- status  
\- created\_by\_actor\_id  
\- created\_at

### **Dependency Types**

Finish-to-Start  
Start-to-Start  
Finish-to-Finish  
Blocks  
Related  
Duplicates

---

# **7\. Agents, Human Users, and Teams**

## **7.1 Human Users**

human\_users  
\- id  
\- organization\_id  
\- employee\_code  
\- first\_name  
\- last\_name  
\- email  
\- phone  
\- job\_title  
\- department  
\- manager\_user\_id  
\- timezone  
\- working\_calendar\_id  
\- employment\_status  
\- authentication\_provider  
\- external\_auth\_id  
\- last\_login\_at  
\- status\_id  
\- created\_at  
\- updated\_at

---

## **7.2 Agents**

agents  
\- id  
\- organization\_id  
\- agent\_code  
\- name  
\- agent\_type  
\- role\_id  
\- description  
\- model\_provider  
\- model\_name  
\- prompt\_version\_id  
\- tool\_configuration  
\- memory\_configuration  
\- maximum\_authority\_level  
\- human\_supervisor\_actor\_id  
\- status\_id  
\- last\_run\_at  
\- created\_at  
\- updated\_at

### **Agent Types**

BD Agent  
PM Agent  
TL Agent  
Developer Agent  
Designer Agent  
QA Agent  
DevOps Agent  
Orchestrator Agent  
Document Agent  
Notification Agent

---

## **7.3 Agent Runs**

Strongly recommended for AI traceability.

agent\_runs  
\- id  
\- agent\_id  
\- project\_id  
\- workflow\_instance\_id  
\- trigger\_type  
\- trigger\_entity\_type  
\- trigger\_entity\_id  
\- input\_reference  
\- output\_reference  
\- model\_name  
\- prompt\_version  
\- tokens\_input  
\- tokens\_output  
\- estimated\_cost  
\- started\_at  
\- completed\_at  
\- run\_status  
\- error\_message  
\- human\_review\_required  
\- reviewed\_by\_actor\_id

---

## **7.4 Teams**

teams  
\- id  
\- organization\_id  
\- name  
\- team\_type  
\- department  
\- lead\_actor\_id  
\- description  
\- status\_id  
\- created\_at  
\- updated\_at

### **Team Types**

BD  
PM  
Frontend  
Backend  
Full Stack  
Mobile  
UI/UX  
Graphic Design  
QA  
DevOps  
Support  
Cross-Functional

---

## **7.5 Team Members**

team\_members  
\- id  
\- team\_id  
\- actor\_id  
\- team\_role  
\- allocation\_percentage  
\- joined\_at  
\- left\_at  
\- is\_active

---

# **8\. Communication and Follow-Up Entities**

## **8.1 Follow-Ups**

follow\_ups  
\- id  
\- organization\_id  
\- project\_id  
\- parent\_follow\_up\_id  
\- follow\_up\_type\_id  
\- source\_actor\_id  
\- recipient\_actor\_id  
\- responsible\_actor\_id  
\- related\_entity\_type  
\- related\_entity\_id  
\- title  
\- description  
\- priority  
\- status\_id  
\- response\_due\_at  
\- reminder\_rule\_id  
\- escalation\_rule\_id  
\- current\_escalation\_level  
\- waiting\_reason  
\- acknowledged\_at  
\- responded\_at  
\- resolved\_at  
\- closed\_at  
\- closure\_reason  
\- created\_at  
\- updated\_at

### **Relationships**

* A follow-up may have child follow-ups.  
* It may link to any project entity.  
* It may generate reminders, escalations, messages, and notifications.

---

## **8.2 Follow-Up Reminders**

follow\_up\_reminders  
\- id  
\- follow\_up\_id  
\- reminder\_number  
\- scheduled\_at  
\- sent\_at  
\- recipient\_actor\_id  
\- channel  
\- status  
\- failure\_reason

---

## **8.3 Follow-Up Escalations**

follow\_up\_escalations  
\- id  
\- follow\_up\_id  
\- escalation\_level  
\- escalated\_from\_actor\_id  
\- escalated\_to\_actor\_id  
\- reason  
\- escalated\_at  
\- acknowledged\_at  
\- resolved\_at  
\- status

---

## **8.4 Messages**

Stores internal, client, agent, email, chat, and system communication.

messages  
\- id  
\- organization\_id  
\- project\_id  
\- conversation\_id  
\- parent\_message\_id  
\- sender\_actor\_id  
\- recipient\_actor\_id  
\- direction  
\- message\_type  
\- channel  
\- subject  
\- content  
\- content\_format  
\- external\_message\_id  
\- related\_entity\_type  
\- related\_entity\_id  
\- delivery\_status  
\- sent\_at  
\- delivered\_at  
\- read\_at  
\- created\_at

### **Channels**

Internal  
Email  
SMS  
Slack  
Teams  
WhatsApp  
CRM  
Client Portal  
System

Messages should normally be immutable. Corrections should create a revision or new message.

---

## **8.5 Conversations**

conversations  
\- id  
\- organization\_id  
\- project\_id  
\- client\_id  
\- conversation\_type  
\- subject  
\- owner\_actor\_id  
\- status\_id  
\- created\_at  
\- closed\_at

---

# **9\. Approval Entities**

## **9.1 Approvals**

Supports approval of SRS, scope, change requests, releases, designs, budgets, and project closure.

approvals  
\- id  
\- organization\_id  
\- project\_id  
\- approval\_type  
\- target\_entity\_type  
\- target\_entity\_id  
\- approval\_step  
\- requested\_by\_actor\_id  
\- assigned\_approver\_actor\_id  
\- decision  
\- decision\_reason  
\- due\_at  
\- requested\_at  
\- acknowledged\_at  
\- decided\_at  
\- status\_id  
\- created\_at

### **Approval Decisions**

Pending  
Approved  
Rejected  
More Information Required  
Withdrawn  
Expired

---

## **9.2 Approval Workflows**

approval\_workflows  
\- id  
\- organization\_id  
\- name  
\- entity\_type  
\- approval\_type  
\- is\_sequential  
\- minimum\_approvals  
\- rejection\_behavior  
\- status

## **9.3 Approval Steps**

approval\_steps  
\- id  
\- approval\_workflow\_id  
\- sequence\_number  
\- approver\_role\_id  
\- approver\_actor\_id  
\- is\_mandatory  
\- response\_sla  
\- escalation\_rule\_id

---

# **10\. Documents and Attachments**

## **10.1 Documents**

documents  
\- id  
\- organization\_id  
\- client\_id  
\- project\_id  
\- document\_type  
\- document\_code  
\- title  
\- description  
\- current\_version\_id  
\- owner\_actor\_id  
\- status\_id  
\- confidentiality\_level  
\- source\_type  
\- created\_at  
\- updated\_at  
\- archived\_at

### **Document Types**

Requirement Questionnaire  
Requirement Brief  
Proposal  
Handover  
SRS  
Roadmap  
Phase Plan  
Technical Specification  
Test Report  
Risk Register  
Change Request  
Progress Report  
Meeting Summary  
Release Notes  
Completion Report

---

## **10.2 Document Versions**

Required for complete document history.

document\_versions  
\- id  
\- document\_id  
\- version\_number  
\- file\_reference  
\- text\_content  
\- change\_summary  
\- generated\_by\_agent\_id  
\- created\_by\_actor\_id  
\- approval\_status  
\- approved\_by\_actor\_id  
\- approved\_at  
\- created\_at

Approved versions should never be overwritten.

---

## **10.3 Attachments**

attachments  
\- id  
\- organization\_id  
\- project\_id  
\- file\_name  
\- original\_file\_name  
\- storage\_provider  
\- storage\_key  
\- content\_type  
\- file\_size  
\- checksum  
\- uploaded\_by\_actor\_id  
\- related\_entity\_type  
\- related\_entity\_id  
\- confidentiality\_level  
\- virus\_scan\_status  
\- uploaded\_at  
\- deleted\_at

The database should store file metadata and storage references, not large file content.

---

# **11\. QA Entities**

## **11.1 Test Cases**

test\_cases  
\- id  
\- project\_id  
\- test\_case\_code  
\- module  
\- title  
\- objective  
\- preconditions  
\- test\_type  
\- priority  
\- owner\_actor\_id  
\- requirement\_id  
\- user\_story\_ticket\_id  
\- status\_id  
\- created\_at  
\- updated\_at

---

## **11.2 Test Steps**

test\_steps  
\- id  
\- test\_case\_id  
\- sequence\_number  
\- action  
\- expected\_result  
\- test\_data

---

## **11.3 Test Runs**

Strongly recommended.

test\_runs  
\- id  
\- project\_id  
\- release\_id  
\- test\_case\_id  
\- environment  
\- build\_version  
\- executed\_by\_actor\_id  
\- result  
\- actual\_result  
\- evidence\_reference  
\- started\_at  
\- completed\_at  
\- bug\_id

### **Results**

Passed  
Failed  
Blocked  
Not Run  
Skipped

---

## **11.4 Bugs**

bugs  
\- id  
\- project\_id  
\- phase\_id  
\- related\_ticket\_id  
\- requirement\_id  
\- test\_case\_id  
\- bug\_number  
\- title  
\- description  
\- severity  
\- priority  
\- environment  
\- build\_version  
\- steps\_to\_reproduce  
\- expected\_result  
\- actual\_result  
\- reproduction\_frequency  
\- reporter\_actor\_id  
\- assigned\_actor\_id  
\- status\_id  
\- root\_cause  
\- resolution  
\- reported\_at  
\- fixed\_at  
\- verified\_at  
\- closed\_at

### **Suggested Bug Statuses**

New  
Triaged  
Assigned  
In Progress  
Ready for Retest  
Retesting  
Reopened  
Passed  
Closed  
Rejected  
Deferred  
Known Issue

---

# **12\. Change and Risk Entities**

## **12.1 Change Requests**

change\_requests  
\- id  
\- project\_id  
\- change\_request\_number  
\- requester\_actor\_id  
\- request\_source  
\- title  
\- description  
\- business\_reason  
\- current\_requirement  
\- requested\_change  
\- priority  
\- status\_id  
\- technical\_impact  
\- design\_impact  
\- qa\_impact  
\- security\_impact  
\- data\_impact  
\- timeline\_impact\_days  
\- resource\_impact  
\- estimated\_cost  
\- currency  
\- recommendation  
\- decision  
\- approved\_by\_actor\_id  
\- approved\_at  
\- implementation\_release\_id  
\- created\_at  
\- updated\_at  
\- closed\_at

### **Relationships**

* Change request may create new requirement versions.  
* Change request may create or update tickets.  
* Change request may affect phases, milestones, risks, and releases.

---

## **12.2 Risks**

risks  
\- id  
\- project\_id  
\- phase\_id  
\- risk\_number  
\- category  
\- title  
\- description  
\- cause  
\- probability\_score  
\- impact\_score  
\- overall\_score  
\- severity  
\- owner\_actor\_id  
\- mitigation\_plan  
\- contingency\_plan  
\- trigger\_condition  
\- target\_resolution\_date  
\- status\_id  
\- identified\_at  
\- reviewed\_at  
\- closed\_at

### **Risk Statuses**

Identified  
Under Review  
Mitigation Planned  
Mitigation in Progress  
Monitoring  
Occurred  
Closed  
Accepted

---

# **13\. Release and Deployment Entities**

## **13.1 Releases**

releases  
\- id  
\- project\_id  
\- phase\_id  
\- release\_number  
\- version  
\- name  
\- release\_type  
\- environment  
\- description  
\- planned\_release\_at  
\- actual\_release\_at  
\- owner\_actor\_id  
\- qa\_approval\_id  
\- deployment\_approval\_id  
\- status\_id  
\- rollback\_required  
\- rollback\_reason  
\- created\_at  
\- updated\_at

### **Release Statuses**

Draft  
Planning  
In Development  
Ready for QA  
QA Failed  
QA Passed  
Awaiting Approval  
Approved  
Deploying  
Deployed  
Failed  
Rolled Back  
Completed  
Cancelled

---

## **13.2 Release Items**

release\_items  
\- id  
\- release\_id  
\- entity\_type  
\- entity\_id  
\- inclusion\_reason  
\- status

Release items may include:

* Requirements  
* Tickets  
* Bugs  
* Change requests  
* Documents

---

## **13.3 Deployments**

Strongly recommended.

deployments  
\- id  
\- project\_id  
\- release\_id  
\- environment  
\- deployment\_number  
\- initiated\_by\_actor\_id  
\- approved\_by\_actor\_id  
\- deployment\_status  
\- pipeline\_reference  
\- build\_reference  
\- started\_at  
\- completed\_at  
\- rollback\_deployment\_id  
\- logs\_reference  
\- failure\_reason

---

# **14\. Notifications**

## **Notifications**

notifications  
\- id  
\- organization\_id  
\- project\_id  
\- recipient\_actor\_id  
\- notification\_type  
\- channel  
\- title  
\- body  
\- related\_entity\_type  
\- related\_entity\_id  
\- priority  
\- scheduled\_at  
\- sent\_at  
\- delivered\_at  
\- read\_at  
\- delivery\_status  
\- retry\_count  
\- failure\_reason  
\- created\_at

### **Notification Types**

Assignment  
Reminder  
Escalation  
Approval Request  
Status Change  
Deadline  
Blocker  
Bug  
Release  
Deployment  
Client Response  
System Alert

---

# **15\. Audit and Complete History**

## **15.1 Audit Logs**

Audit logs should be append-only.

audit\_logs  
\- id  
\- organization\_id  
\- project\_id  
\- actor\_id  
\- action  
\- entity\_type  
\- entity\_id  
\- before\_data  
\- after\_data  
\- changed\_fields  
\- reason  
\- source  
\- correlation\_id  
\- ip\_address  
\- user\_agent  
\- created\_at

### **Audit Actions**

Created  
Viewed  
Updated  
Deleted  
Restored  
Assigned  
Reassigned  
Status Changed  
Approved  
Rejected  
Escalated  
Closed  
Downloaded  
Agent Executed  
Deployment Started  
Deployment Completed

Audit logs must not be editable by normal users or agents.

---

## **15.2 Status History**

status\_history  
\- id  
\- organization\_id  
\- project\_id  
\- entity\_type  
\- entity\_id  
\- previous\_status\_id  
\- new\_status\_id  
\- changed\_by\_actor\_id  
\- transition\_rule\_id  
\- reason  
\- evidence\_reference  
\- changed\_at

Every status transition must create one status-history record.

---

## **15.3 Entity Activity Timeline**

Recommended for project timelines and dashboards.

activity\_events  
\- id  
\- organization\_id  
\- project\_id  
\- actor\_id  
\- event\_type  
\- entity\_type  
\- entity\_id  
\- title  
\- description  
\- event\_data  
\- visibility  
\- occurred\_at

This table can power a unified project timeline.

---

# **16\. Configurable Workflow Entities**

Because statuses, transitions, SLAs, reminders, and escalation rules must not be hard-coded, add the following configuration tables.

## **16.1 Workflow Definitions**

workflow\_definitions  
\- id  
\- organization\_id  
\- name  
\- module  
\- entity\_type  
\- version  
\- is\_active  
\- created\_by\_actor\_id  
\- approved\_by\_actor\_id  
\- effective\_from  
\- created\_at

---

## **16.2 Status Definitions**

status\_definitions  
\- id  
\- workflow\_definition\_id  
\- code  
\- name  
\- description  
\- sequence\_number  
\- category  
\- is\_initial  
\- is\_terminal  
\- pauses\_sla  
\- color\_reference  
\- is\_active

### **Status Categories**

Open  
Active  
Waiting  
Blocked  
Completed  
Cancelled  
Rejected

---

## **16.3 Transition Rules**

transition\_rules  
\- id  
\- workflow\_definition\_id  
\- from\_status\_id  
\- to\_status\_id  
\- transition\_name  
\- allowed\_role\_id  
\- allowed\_actor\_type  
\- approval\_required  
\- required\_approval\_type  
\- required\_fields  
\- required\_evidence  
\- condition\_expression  
\- action\_configuration  
\- is\_active

---

## **16.4 Follow-Up Rule Definitions**

follow\_up\_rule\_definitions  
\- id  
\- organization\_id  
\- follow\_up\_type  
\- source\_role\_id  
\- recipient\_role\_id  
\- priority  
\- response\_sla\_value  
\- response\_sla\_unit  
\- business\_calendar\_id  
\- maximum\_reminders  
\- maximum\_escalation\_level  
\- pause\_conditions  
\- closure\_conditions  
\- effective\_from  
\- is\_active

---

## **16.5 Reminder Rules**

reminder\_rules  
\- id  
\- follow\_up\_rule\_id  
\- reminder\_number  
\- trigger\_type  
\- trigger\_offset\_value  
\- trigger\_offset\_unit  
\- recipient\_role\_id  
\- notification\_channels

---

## **16.6 Escalation Rules**

escalation\_rules  
\- id  
\- follow\_up\_rule\_id  
\- escalation\_level  
\- trigger\_after\_value  
\- trigger\_after\_unit  
\- recipient\_role\_id  
\- notification\_channels  
\- action\_type

---

## **16.7 Business Calendars**

business\_calendars  
\- id  
\- organization\_id  
\- name  
\- timezone  
\- working\_days  
\- working\_start\_time  
\- working\_end\_time  
\- emergency\_calendar  
\- is\_default

## **Business Calendar Holidays**

business\_calendar\_holidays  
\- id  
\- business\_calendar\_id  
\- holiday\_date  
\- holiday\_name  
\- is\_working\_day\_override

---

# **17\. Requirement Traceability Tables**

## **Requirement-to-Ticket**

requirement\_ticket\_links  
\- requirement\_id  
\- ticket\_id  
\- relationship\_type

## **Requirement-to-Test Case**

requirement\_test\_case\_links  
\- requirement\_id  
\- test\_case\_id  
\- coverage\_type

## **Requirement-to-Release**

requirement\_release\_links  
\- requirement\_id  
\- release\_id  
\- delivery\_status

## **Requirement-to-Document**

requirement\_document\_links  
\- requirement\_id  
\- document\_id  
\- relationship\_type

## **Ticket-to-Test Case**

ticket\_test\_case\_links  
\- ticket\_id  
\- test\_case\_id

Traceability should support:

Requirement  
→ Requirement Version  
→ Phase  
→ User Story  
→ Technical Ticket  
→ Test Case  
→ Bug  
→ Release

---

# **18\. High-Level Relationship Diagram**

Organization  
├── Human Users  
├── Agents  
├── Teams  
├── Workflow Definitions  
└── Clients  
    ├── Contacts  
    ├── Queries  
    │   └── Opportunities  
    │       └── Projects  
    └── Projects  
        ├── Project Members  
        ├── Requirements  
        │   └── Requirement Versions  
        ├── Phases  
        │   ├── Milestones  
        │   └── Tickets  
        │       ├── Subtasks  
        │       ├── Assignments  
        │       ├── Test Cases  
        │       └── Bugs  
        ├── Follow-Ups  
        │   ├── Reminders  
        │   └── Escalations  
        ├── Messages  
        ├── Approvals  
        ├── Documents  
        │   └── Document Versions  
        ├── Attachments  
        ├── Change Requests  
        ├── Risks  
        ├── Releases  
        │   ├── Release Items  
        │   └── Deployments  
        ├── Notifications  
        ├── Status History  
        ├── Activity Events  
        └── Audit Logs

---

# **19\. Complete History Requirements**

Every major entity should maintain four types of history.

## **Status History**

Records every lifecycle transition.

Backlog  
→ Ready  
→ Assigned  
→ In Progress  
→ Blocked  
→ In Progress  
→ Done

## **Ownership History**

Records every assignment and reassignment.

## **Version History**

Used for:

* Requirements  
* SRS documents  
* Proposals  
* Roadmaps  
* Change requests  
* Release notes  
* Agent prompts

## **Audit History**

Records:

* Who performed the action  
* Whether it was a human or agent  
* What changed  
* Previous values  
* New values  
* When it happened  
* Why it happened  
* Which workflow or API triggered it

---

# **20\. Recommended MVP Entity Priority**

## **MVP Phase 1**

Implement first:

Organizations  
Actors  
Human Users  
Agents  
Teams  
Clients  
Contacts  
Queries  
Projects  
Requirements  
Requirement Versions  
Phases  
Tickets  
Subtasks  
Assignments  
Follow-Ups  
Messages  
Approvals  
Documents  
Attachments  
Notifications  
Status Definitions  
Transition Rules  
Status History  
Audit Logs

## **MVP Phase 2**

Add:

Opportunities  
Milestones  
Test Cases  
Test Runs  
Bugs  
Risks  
Change Requests  
Release Management  
Deployments  
Follow-Up Reminders  
Escalation Rules  
Business Calendars

## **MVP Phase 3**

Add:

Agent Runs  
Agent Prompt Versions  
Semantic Document Index  
Cost Tracking  
Performance Analytics  
Resource Capacity  
Timesheets  
Forecasting  
AI Evaluation Results

The most important architectural additions beyond the original entity list are `Actors`, `Status History`, `Document Versions`, `Workflow Definitions`, `Transition Rules`, `Agent Runs`, and `Activity Events`. These are necessary to provide consistent ownership, configurable workflows, complete traceability, and reliable human-agent accountability.

