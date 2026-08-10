# **Existing System Integration Plan**

## **1\. Integration Strategy**

The agentic platform should **connect with existing company systems rather than replace them during the MVP**.

Based on the current company toolset:

| Business Function | Existing System |
| ----- | ----- |
| Client email | Gmail |
| Internal communication | Slack |
| Project management | Jira |
| Source control | GitHub |
| Document storage | Google Drive |
| CRM | HubSpot |
| Accounting | QuickBooks |
| Time tracking | Toggl |
| Credential management | 1Password |

The agentic platform will become the central source for:

* Agent and human workflows  
* Requirement management  
* Follow-ups and escalations  
* Human approvals  
* Project handoffs  
* Requirement traceability  
* Agent execution history  
* SLA tracking  
* Audit logs  
* Cross-system reporting

Existing systems will continue to perform their specialized functions.

---

# **2\. Recommended MVP Integrations**

For the first version, integrate only:

Communication Platform: Gmail

Project-Management Platform: Jira

Do not integrate Slack, GitHub, Drive, HubSpot, QuickBooks, and Toggl in the first release unless they are required for the initial pilot.

## **Why Gmail First**

The complete workflow begins with:

Client Query  
→ BD Agent  
→ Requirement Gathering  
→ Client Follow-Up

Gmail integration enables the system to:

* Receive client inquiries.  
* Create client-query records.  
* connect email threads with clients, queries, and projects.  
* Detect client replies.  
* Generate BD response drafts.  
* Send approved client messages.  
* Save attachments and conversation history.  
* Create follow-ups when clients do not respond.

The Gmail API supports authorized mailbox access and message sending. Gmail mailbox changes can be tracked through Gmail push notifications using Google Cloud Pub/Sub. ([Google for Developers](https://developers.google.com/workspace/gmail/api/guides?utm_source=chatgpt.com))

## **Why Jira First**

Jira integration enables the PM and TL workflow:

Approved Requirement  
→ Phase  
→ User Story  
→ Technical Ticket  
→ Assignment  
→ Development  
→ QA  
→ Done

The integration can create and synchronize:

* Epics  
* User stories  
* Development tickets  
* Design tickets  
* QA tickets  
* Bug tickets  
* Assignees  
* Priorities  
* Estimates  
* Statuses  
* Comments  
* Sprint information  
* Ticket dependencies

Jira Cloud provides REST APIs and webhooks that can send issue and project events to the agentic platform. Dynamic webhook management is available for supported OAuth 2.0 and app-based integrations. ([Atlassian Developer](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/?utm_source=chatgpt.com))

---

# **3\. MVP Source-of-Truth Rules**

Clear ownership must be defined to avoid conflicting records.

## **Agentic Platform Owns**

* Clients and project relationships  
* Requirements  
* Requirement versions  
* SRS documents  
* Project phases  
* Human approvals  
* Follow-ups  
* Escalations  
* SLAs  
* Risks  
* Change requests  
* Agent actions  
* Audit logs  
* Client-visible project status

## **Gmail Owns**

* Actual email delivery  
* Gmail thread ID  
* Gmail message ID  
* Mailbox labels  
* Delivery timestamps  
* Original email content

## **Jira Owns**

* Sprint assignment  
* Development assignee  
* Story points  
* Developer execution status  
* Jira comments  
* Jira issue links  
* Jira board placement

## **Synchronization Rule**

Agentic Platform  
→ Creates approved execution ticket  
→ Jira issue created  
→ Jira issue key returned  
→ Jira updates received through webhook  
→ Agentic ticket record synchronized

Requirement descriptions, commercial information, client approvals, and confidential internal information should not be editable from Jira.

---

# **4\. Gmail Integration**

## **Integration Decision**

Connect to Gmail  
Do not replace Gmail

## **Initial Use Cases**

* Receive new client inquiries.  
* Match the sender with an existing contact.  
* Create a new client and contact when approved.  
* Create a query record.  
* Import the email subject, content, attachments, and thread.  
* Classify the inquiry using the BD Agent.  
* Draft replies.  
* Request Human BD approval before sensitive messages.  
* Send approved emails.  
* detect client replies.  
* Create client-response follow-ups.  
* Link the conversation with an opportunity or project.

## **Required Access**

* Google Cloud project  
* Gmail API enabled  
* OAuth consent configuration  
* Authorized company mailbox  
* Test mailbox  
* Approved OAuth scopes  
* Google Workspace administrator approval where required  
* Cloud Pub/Sub configuration for mailbox-change notifications  
* Secure token storage

Gmail push notification watches must be created and renewed by the application, and notifications are delivered through Google Cloud Pub/Sub rather than an ordinary direct mailbox webhook. ([Google for Developers](https://developers.google.com/workspace/gmail/api/guides/push?utm_source=chatgpt.com))

## **Recommended Initial Permissions**

Use the minimum permissions required to:

* Read approved mailbox messages  
* Read message metadata  
* Create drafts  
* Send approved messages  
* Read attachments  
* Apply integration-specific labels

Do not request full mailbox permissions unless the approved workflows require them. Google documents separate Gmail OAuth scopes with different access levels. ([Google for Developers](https://developers.google.com/workspace/gmail/api/auth/scopes?utm_source=chatgpt.com))

## **Test Data Required**

* New-client inquiry  
* Existing-client inquiry  
* Email with attachment  
* Multi-message thread  
* Client reply  
* Forwarded email  
* CC recipients  
* Duplicate inquiry  
* Spam or irrelevant inquiry  
* Failed outgoing email  
* Email requiring human approval

## **Gmail Workflow**

Email Received  
→ Gmail Notification Received  
→ Message Retrieved  
→ Sender Matched to Contact  
→ Query Created or Existing Record Updated  
→ BD Agent Classifies Inquiry  
→ Human BD Reviews When Required  
→ Response Drafted  
→ Response Approved  
→ Gmail Sends Email  
→ Thread and Message IDs Stored

---

# **5\. Jira Integration**

## **Integration Decision**

Connect to Jira  
Do not replace Jira during the MVP

## **Initial Use Cases**

* Create Jira projects or map existing projects.  
* Create epics.  
* Create user stories.  
* Create technical tickets.  
* Create QA tickets.  
* Create bugs.  
* Assign issues.  
* Synchronize priority.  
* Synchronize estimates.  
* Synchronize status.  
* Import Jira comments.  
* Link pull requests later through GitHub integration.  
* Create follow-ups for blocked or overdue tickets.

## **Required Access**

* Jira Cloud test or sandbox site  
* Test project  
* Atlassian developer application  
* OAuth 2.0 credentials  
* Authorized Jira administrator  
* Required project permissions  
* Issue-type configuration  
* Workflow and status mapping  
* Webhook callback URL  
* Test users  
* Test epics and issues  
* Current API and rate-limit documentation

## **Initial Jira Permissions**

The integration should initially receive permissions to:

* Read projects  
* Read users  
* Read issue types  
* Create issues  
* Update approved fields  
* Read comments  
* Add integration comments  
* Read status changes  
* Read sprint information  
* Receive webhook events

Avoid administrative permissions unrelated to the approved project scope.

## **Jira Field Mapping**

| Agentic Platform | Jira |
| ----- | ----- |
| Ticket ID | External reference/custom field |
| Project | Jira project |
| Phase | Epic or custom field |
| User story | Story |
| Technical ticket | Task |
| Subtask | Sub-task |
| Bug | Bug |
| Priority | Priority |
| Assignee | Assignee |
| Estimate | Story points/original estimate |
| Status | Jira workflow status |
| Requirement ID | Custom field or issue link |
| Acceptance criteria | Description or custom field |

## **Jira Status Mapping Example**

| Agentic Status | Jira Status |
| ----- | ----- |
| Backlog | Backlog |
| Ready | Selected for Development |
| Assigned | To Do |
| In Progress | In Progress |
| Blocked | Blocked |
| Code Review | In Review |
| Ready for QA | Ready for QA |
| QA In Progress | Testing |
| Failed QA | Reopened |
| Passed QA | QA Passed |
| Done | Done |

The mapping must be configurable because Jira workflows can differ between projects.

## **Jira Workflow**

PM Agent Creates Draft Ticket  
→ Human PM/TL Approves Ticket  
→ Ticket Sent to Jira  
→ Jira Issue Created  
→ Developer Updates Jira  
→ Jira Webhook Sent  
→ Agentic Platform Updates Ticket  
→ Follow-Up Rules Evaluated  
→ PM and TL Dashboards Updated

## **Test Data Required**

* Epic  
* User story  
* Task  
* Subtask  
* Bug  
* Assigned ticket  
* Reassigned ticket  
* Blocked ticket  
* Status transition  
* Comment  
* Attachment  
* Sprint assignment  
* Closed ticket  
* Reopened ticket

---

# **6\. Phase 2 Integrations**

After Gmail and Jira are stable, add the following integrations.

## **6.1 Slack**

### **Integration Decision**

Connect for internal notifications and operational interactions  
Do not use Slack as the official system of record

### **Use Cases**

* New assignment notification  
* Approval request notification  
* Overdue follow-up alert  
* Developer blocker escalation  
* QA critical-bug alert  
* Deployment notification  
* Daily project summary  
* Weekly management summary  
* Deep link to the agentic platform

Slack supports OAuth-based app installation, event subscriptions, API calls, and incoming webhooks. Incoming requests from Slack should be verified by the receiving application. ([Slack API](https://api.slack.com/authentication/oauth-v2?utm_source=chatgpt.com))

### **Important Rule**

Slack messages should contain summaries and secure links. Sensitive credentials, private client data, and full approval evidence should remain in the platform.

Formal approvals should initially be completed in the platform rather than only through a Slack reaction or message.

---

## **6.2 GitHub**

### **Integration Decision**

Connect repositories and development activity  
Do not replace GitHub

### **Initial Use Cases**

* Link repositories to projects.  
* Link branches to tickets.  
* Link commits to tickets.  
* Link pull requests to tickets.  
* Read pull-request status.  
* Read review status.  
* Read automated-check results.  
* Detect merges.  
* Update ticket evidence.  
* Notify TL about failed checks.

A GitHub App can receive webhook events for activity such as commits, pushes, and pull requests in repositories where the app is installed. ([GitHub Docs](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/using-webhooks-with-github-apps?utm_source=chatgpt.com))

### **Initial Security Rule**

The first GitHub integration should be primarily read-only.

The agent may:

* Read repository metadata.  
* Read commits.  
* Read pull requests.  
* Read checks.  
* Link evidence with tickets.

The agent must not:

* Merge pull requests.  
* Delete branches.  
* Modify protected branches.  
* Change repository security settings.  
* Publish a release without human approval.

---

## **6.3 Google Drive**

### **Integration Decision**

Connect for project documents and knowledge-base content  
Do not replace Google Drive

### **Initial Use Cases**

* Create a project folder.  
* Store SRS documents.  
* Store meeting records.  
* Store designs and reports.  
* Store release notes.  
* Link files to project records.  
* Import approved documents into the AI knowledge base.  
* Detect file changes.  
* Maintain document references.

Google Drive provides OAuth scopes for controlled access and push notifications for supported file and change resources. Push callbacks require a valid HTTPS endpoint. ([Google for Developers](https://developers.google.com/workspace/drive/api/guides/api-specific-auth?utm_source=chatgpt.com))

### **Recommended Folder Structure**

Client Name  
└── Project Name  
    ├── 01 Requirements  
    ├── 02 SRS  
    ├── 03 Planning  
    ├── 04 Design  
    ├── 05 Development  
    ├── 06 QA  
    ├── 07 Releases  
    ├── 08 Client Updates  
    └── 09 Completion

---

# **7\. Phase 3 Integrations**

## **7.1 HubSpot CRM**

### **Integration Decision**

Connect HubSpot as the commercial CRM  
Do not duplicate CRM ownership

### **HubSpot Should Own**

* Companies  
* Contacts  
* Leads  
* Deals  
* Sales pipeline  
* Opportunity commercial stage  
* Sales activities

### **Agentic Platform Should Own**

* Requirement collection  
* Project handover  
* Delivery workflow  
* Agent activity  
* Project execution  
* Follow-ups after handover  
* Requirements, tickets, QA, and releases

### **Use Cases**

* Import companies and contacts.  
* Import new deals.  
* Create a query from a qualified lead.  
* Synchronize opportunity status.  
* Return project-conversion status to HubSpot.  
* Add high-level project updates to the deal timeline.

HubSpot provides CRM APIs, OAuth authorization, and webhook subscriptions for CRM object changes. App permissions must include the required scopes for each subscribed CRM object. ([HubSpot Developers](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/authentication/overview?utm_source=chatgpt.com))

---

## **7.2 QuickBooks**

### **Integration Decision**

Connect for accounting visibility  
QuickBooks remains the accounting source of truth

### **Initial Use Cases**

* Read client/customer records.  
* Read invoice status.  
* Read payment status.  
* Associate invoices with projects.  
* Show commercial status to authorized PM or BD users.  
* Trigger an internal notification when payment status changes.

QuickBooks Online integrations use OAuth authorization and support webhook-based change notifications. Intuit provides sandbox companies for integration testing and requires webhook functionality to be tested when an application relies on it. ([Intuit Developer](https://developer.intuit.com/app/developer/qbo/docs/develop/sdks-and-samples-collections/net/configuration?utm_source=chatgpt.com))

### **Important Rule**

Agents must not automatically:

* Create financial commitments.  
* Issue refunds.  
* Delete invoices.  
* Modify accounting transactions.  
* Change tax information.  
* Mark invoices paid without accounting confirmation.

Start with read-only financial visibility.

---

## **7.3 Toggl Track**

### **Integration Decision**

Connect for time and capacity reporting  
Toggl remains the time-entry source of truth

### **Initial Use Cases**

* Import time entries.  
* Map Toggl projects to agentic projects.  
* Map Toggl tasks to tickets.  
* Compare estimated and actual effort.  
* Calculate team capacity.  
* Identify estimate overruns.  
* Generate phase and project time reports.

Toggl Track provides API and webhook functionality for workspace entities. Its request quotas depend on the account or subscription context, and clients should monitor quota headers and handle throttling rather than assuming unlimited access. ([Toggl Engineering](https://engineering.toggl.com/docs/track/?utm_source=chatgpt.com))

---

# **8\. Systems Not Recommended for Initial Integration**

Because the company currently uses Gmail, Slack, Jira, GitHub, Google Drive, HubSpot, QuickBooks, and Toggl, the following alternatives should not be integrated initially:

* Outlook  
* Microsoft Teams  
* ClickUp  
* Trello  
* Asana  
* GitLab  
* AWS CodePipeline  
* OneDrive  
* Additional CRM systems  
* Additional accounting platforms  
* Additional time-tracking platforms

Supporting several systems that perform the same function would increase:

* Development effort  
* Testing effort  
* Synchronization conflicts  
* Permission complexity  
* Support cost  
* Data duplication  
* Rate-limit management  
* Failure scenarios

The integration architecture should remain provider-based so additional systems can be added later.

EmailProvider  
├── GmailProvider  
└── OutlookProvider – Future

WorkManagementProvider  
├── JiraProvider  
├── ClickUpProvider – Future  
└── AwsWorkManagementProvider – Future

SourceControlProvider  
├── GitHubProvider  
├── GitLabProvider – Future  
└── CodeCommitProvider – Future

---

# **9\. Required Information for Every Integration**

Before development begins, prepare an **Integration Readiness Record** for every system.

## **Standard Integration Checklist**

| Requirement | Description |
| ----- | ----- |
| Integration owner | Human responsible for the connected system |
| Business purpose | Why the system is being connected |
| Use cases | Actions the integration must support |
| Source of truth | Which system owns each data type |
| API documentation | Current official API documentation |
| API version | Approved API version |
| Test account | Dedicated non-production account |
| Sandbox | Sandbox or isolated test environment |
| Credentials | OAuth client, app key, or approved token |
| Permissions | Minimum required scopes and roles |
| Webhook access | Ability to register and test callbacks |
| Callback URL | Public HTTPS integration endpoint |
| Rate limits | Current quotas and throttling rules |
| Test data | Representative records and scenarios |
| Field mapping | Internal-to-external field mapping |
| Status mapping | Internal-to-external status mapping |
| Retry policy | Retry and backoff behaviour |
| Idempotency | Duplicate-event prevention |
| Error handling | Failure and recovery process |
| Audit rules | Required integration logs |
| Data retention | How long imported data is stored |
| Security classification | Sensitivity of synchronized data |
| Disconnect process | Behaviour when access is revoked |
| Acceptance criteria | Conditions for production readiness |

---

# **10\. API Credential Requirements**

Credentials must:

* Be stored in 1Password or the deployment secret manager.  
* Never be stored in tickets, prompts, logs, or chat messages.  
* Be encrypted at rest.  
* Be accessible only to the integration worker.  
* Have the minimum permissions required.  
* Support expiration and rotation.  
* Be separated by environment.  
* Have ownership and expiry records.

Recommended separation:

Development Credentials  
Staging Credentials  
Production Credentials

Production credentials should never be used for ordinary development testing.

---

# **11\. Webhook Requirements**

Every webhook integration should include:

* Public HTTPS endpoint  
* Request-signature validation where supported  
* Event ID storage  
* Duplicate-event protection  
* Event timestamp validation  
* Retry handling  
* Dead-letter queue  
* Failed-event replay  
* Event audit log  
* Integration health monitoring  
* Secret rotation procedure

## **Event Processing Flow**

External Event  
→ Webhook Received  
→ Signature Validated  
→ Event ID Checked  
→ Raw Event Logged  
→ Normalized Event Created  
→ Business Rules Evaluated  
→ Internal Record Updated  
→ Follow-Up or Notification Triggered  
→ Processing Result Recorded

---

# **12\. Rate-Limit Handling**

Rate limits should not be hard-coded into workflow logic.

Create configurable integration settings:

Provider  
API Version  
Request Limit  
Time Window  
Current Usage  
Retry-After Handling  
Maximum Retry Count  
Backoff Strategy  
Batch Size  
Concurrency Limit  
Last Limit Error

The integration service should:

* Prefer webhooks over frequent polling.  
* Use incremental synchronization.  
* Cache stable reference data.  
* Batch requests where supported.  
* Respect provider retry instructions.  
* Use exponential backoff.  
* Queue non-urgent operations.  
* Alert administrators when repeated throttling occurs.

---

# **13\. Integration Environment Structure**

Each integration should support:

Disconnected  
Development  
Testing  
Staging  
Production  
Suspended  
Error

Each environment must have separate:

* Credentials  
* Webhooks  
* Callback URLs  
* Test data  
* Logs  
* Configuration  
* Synchronization state

---

# **14\. MVP Integration Acceptance Criteria**

## **Gmail Is Ready When**

* OAuth connection succeeds.  
* Approved mailbox can be connected.  
* New emails create or update queries.  
* Email threads remain linked correctly.  
* Attachments are captured.  
* BD Agent can draft a response.  
* Human BD can approve the response.  
* Approved email is sent.  
* Client replies are detected.  
* Duplicate notifications do not create duplicate messages.  
* Failed processing can be retried.  
* All activity is audited.

## **Jira Is Ready When**

* OAuth connection succeeds.  
* Test project can be mapped.  
* Approved tickets create Jira issues.  
* Jira issue keys return to the platform.  
* Assignees synchronize.  
* Statuses synchronize.  
* Comments synchronize according to permissions.  
* Jira webhooks are validated and processed.  
* Duplicate webhook events are ignored safely.  
* Blocked and overdue states trigger follow-ups.  
* Jira failure does not corrupt internal project data.  
* All synchronization activity is audited.

---

# **15\. Final Integration Roadmap**

## **MVP**

Gmail  
\+  
Jira  
\+  
Internal In-App Notifications

## **Phase 2**

Slack  
\+  
GitHub  
\+  
Google Drive

## **Phase 3**

HubSpot  
\+  
QuickBooks  
\+  
Toggl

## **Future Provider Expansion**

Outlook  
Microsoft Teams  
ClickUp  
Trello  
Asana  
GitLab  
AWS CodePipeline  
OneDrive  
Other CRM Platforms  
Other Accounting Platforms  
Other Time-Tracking Platforms

The most appropriate MVP decision is to integrate **Gmail for client communication and Jira for work execution**, while the agentic platform controls requirements, approvals, follow-ups, escalations, and audit history. This keeps the first release focused while still supporting the complete client-to-delivery workflow.

