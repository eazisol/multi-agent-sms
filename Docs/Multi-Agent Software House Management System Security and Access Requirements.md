# **Security and Access Requirements**

## **1\. Security Objective**

The platform should follow a **zero-trust and least-privilege model**:

Never trust access automatically  
→ Verify the actor  
→ Verify the tenant and project  
→ Verify the requested action  
→ Verify current authority  
→ Provide only the minimum required data  
→ Record the complete action

NIST zero-trust guidance emphasizes per-request, context-based, least-privilege access rather than relying only on network location. OWASP also identifies broken access control as a major application-security risk. ([NIST Publications](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf?utm_source=chatgpt.com))

---

# **2\. Authentication Requirements**

## **Human Users**

The system should support:

* Single sign-on through Microsoft Entra ID, Google Workspace, Auth0, or another approved identity provider.  
* Multi-factor authentication.  
* Secure account recovery.  
* Session expiration.  
* Device and login-history visibility.  
* Account-locking and rate-limiting controls.  
* Immediate user suspension.  
* Forced logout from all active sessions.  
* Time-limited guest and client accounts.

NIST’s current digital-identity guidance provides requirements covering identity proofing, authentication, federation, and authenticator assurance levels. ([NIST Computer Security Resource Center](https://csrc.nist.gov/pubs/sp/800/63/b/4/final?utm_source=chatgpt.com))

## **Mandatory MFA**

MFA should be required for:

* Administrators  
* Human approvers  
* PMs and TLs  
* Production-access users  
* DevOps users  
* Security users  
* Users accessing restricted documents  
* Users exporting large amounts of data  
* Users modifying permissions  
* Users accessing secret-management systems

## **Step-Up Authentication**

The system should request fresh authentication or MFA before:

* Production deployment approval  
* Production rollback  
* Permission changes  
* Secret access  
* Client data export  
* User impersonation  
* Project cancellation  
* Permanent deletion  
* Security-policy changes  
* Agent-authority expansion

## **Recommended Session Defaults**

| Configuration | Recommended Default |
| ----- | ----- |
| Access token lifetime | 15–30 minutes |
| Normal user session | 8–12 hours |
| Administrative session | 2–4 hours |
| Inactivity timeout | 30 minutes |
| Step-up authentication validity | 10–15 minutes |
| Client invitation expiry | 72 hours |
| Password-reset link expiry | 30 minutes |

These values should be configurable according to project sensitivity.

---

# **3\. Authorization Model**

Use a combination of:

RBAC  
\+ Project Membership  
\+ Data Classification  
\+ Ownership  
\+ Environment  
\+ Approval Authority  
\+ Contextual Conditions

## **RBAC**

Role-Based Access Control defines the user’s general authority.

Examples:

clients.read  
clients.update  
requirements.create  
requirements.approve  
tickets.assign  
tickets.update  
documents.download  
bugs.verify  
releases.approve  
deployments.execute  
deployments.approve  
users.manage  
agents.configure  
secrets.reference  
audit.read

## **Attribute-Based Rules**

Permissions should also consider:

* `organization_id`  
* `client_id`  
* `project_id`  
* Assigned role  
* Current project membership  
* Department  
* Document classification  
* Record ownership  
* Deployment environment  
* Financial threshold  
* Approval delegation  
* Effective and expiry dates  
* Working location where required  
* Whether the actor is human or AI

## **Default Authorization Behaviour**

No Explicit Permission  
→ Access Denied

The frontend must not be the only enforcement point. Permissions must be validated by the FastAPI backend and, for sensitive tenant-owned tables, reinforced through PostgreSQL Row-Level Security. PostgreSQL RLS can restrict which rows normal users may select or modify based on configured policies. ([PostgreSQL](https://www.postgresql.org/docs/17/ddl-rowsecurity.html?utm_source=chatgpt.com))

---

# **4\. Initial Role Permission Matrix**

| Role | Default Access |
| ----- | ----- |
| Organization Admin | Organization configuration, users, agents, integrations and audit metadata |
| Human BD | Assigned clients, contacts, queries, opportunities, requirements and client communication |
| BD Agent | Assigned queries and approved BD knowledge only |
| Human PM | Full business and operational access to assigned projects |
| PM Agent | Assigned project requirements, plans, risks, tickets and approved documents |
| Human TL | Assigned project technical information, tickets, repositories and QA records |
| TL Agent | Approved technical project context and assignment data |
| Developer | Assigned projects, modules and tickets |
| Developer Agent | Assigned ticket context and approved technical tools only |
| Designer | Assigned requirements, workflows, branding and design tickets |
| Designer Agent | Assigned design context only |
| QA Engineer | Requirements, acceptance criteria, builds, test data and bugs |
| QA Agent | Assigned test context and approved test tools only |
| DevOps Engineer | Approved infrastructure, pipelines, logs and deployments |
| DevOps Agent | Deployment metadata and approved automation only |
| Client Administrator | Client-owned projects and approved client-visible records |
| Client Approver | Assigned approvals and approved project information |
| Client Viewer | Read-only client-visible project information |
| Orchestrator Agent | Workflow metadata required for routing; no independent business authority |

---

# **5\. Client Data Isolation**

Every client’s data must be isolated from every other client.

## **Database Isolation**

All client-owned records should contain:

organization\_id  
client\_id  
project\_id

The backend must apply the authenticated tenant context to every query.

PostgreSQL Row-Level Security should be enabled on sensitive multi-tenant tables such as:

* Clients  
* Contacts  
* Projects  
* Requirements  
* Tickets  
* Messages  
* Documents  
* Attachments  
* Follow-ups  
* Approvals  
* Bugs  
* Releases  
* Audit logs

## **Storage Isolation**

Files should be separated by organization and project:

/{organization\_id}/{client\_id}/{project\_id}/{document\_type}/{file\_id}

Requirements:

* No public storage containers.  
* Short-lived signed download links.  
* Separate encryption and access policies where necessary.  
* Client-specific retention and deletion.  
* No predictable public file URLs.  
* No cross-client file search.

## **Vector Database Isolation**

Embeddings must include:

organization\_id  
client\_id  
project\_id  
knowledge\_id  
classification  
approved\_version

An agent must never retrieve another client’s document based only on semantic similarity.

## **Cache Isolation**

Cache keys must include tenant and project identifiers.

Example:

tenant:{organization\_id}:project:{project\_id}:ticket:{ticket\_id}

## **Integration Isolation**

OAuth tokens, API credentials, webhook configurations, and synchronization records must remain client- or organization-specific.

## **Required Isolation Tests**

QA must verify:

* User from Client A cannot view Client B records.  
* IDs cannot be changed in URLs to retrieve another project.  
* Search does not return unauthorized results.  
* Exports contain only the selected client.  
* Attachments cannot be accessed across projects.  
* Agent retrieval remains tenant-scoped.  
* Cache entries cannot leak across clients.  
* Webhooks update only the correct tenant.

---

# **6\. Project-Level Access**

Access to a project should require an active `project_membership` record.

## **Project Membership Data**

Project  
Actor  
Assigned Role  
Access Level  
Allowed Modules  
Start Date  
Expiry Date  
Assigned By  
Approval Authority  
Status

## **Project Access Levels**

| Level | Rights |
| ----- | ----- |
| Summary | View high-level status only |
| Read Only | View authorized project records |
| Contributor | Update assigned records |
| Manager | Manage project execution and assignments |
| Approver | Approve configured actions |
| Technical Administrator | Manage technical configuration |
| Project Administrator | Full project administration |

## **Project Access Rules**

* Access should not be granted automatically because a user belongs to the company.  
* Membership should expire when the project or assignment ends.  
* Reassigned users should lose access no longer required.  
* Users on leave may be temporarily suspended from approvals.  
* Contractors should receive time-limited access.  
* Client users should see only client-visible records.  
* Production access must be separate from project membership.  
* Cross-project access requires explicit authorization.

---

# **7\. Document Access**

## **Document Classification**

Every document must have a classification:

| Classification | Examples | Access |
| ----- | ----- | ----- |
| Public | Marketing material and public service descriptions | Approved public users |
| Internal | Standard processes and internal templates | Company users and approved agents |
| Confidential | Client requirements, SRS and technical specifications | Assigned project members |
| Restricted | Pricing, contracts, security reports and production information | Named authorized actors only |

## **Document Access Requirements**

Each document must store:

Owner  
Project  
Classification  
Allowed Roles  
Allowed Users  
Version  
Approval Status  
Effective Date  
Expiry Date  
Download Permission  
Share Permission  
AI Retrieval Permission

## **Document Controls**

* Draft documents cannot be presented as approved knowledge.  
* Superseded versions should not be used by agents.  
* Restricted files require explicit permission.  
* All downloads of restricted files must be logged.  
* External sharing links must expire.  
* Client downloads should use watermarks when required.  
* Files should be encrypted in transit and at rest.  
* Deleted documents should follow retention and legal-hold policies.  
* Document permissions must also apply to extracted text and embeddings.

---

# **8\. Agent Access Limitations**

Agents should operate with narrower permissions than the humans they support.

OWASP’s guidance for LLM applications highlights prompt injection, sensitive-information disclosure, improper output handling, and excessive agency as important risks. Critical authorization controls should be enforced outside the model through deterministic application logic. ([OWASP Gen AI Security Project](https://genai.owasp.org/llm-top-10/?utm_source=chatgpt.com))

## **Agent Identity**

Every agent must have:

* A unique system identity.  
* A named human supervisor.  
* A defined role.  
* An approved tool allowlist.  
* An approved project scope.  
* A maximum authority level.  
* Execution and cost limits.  
* Separate development, staging, and production identities.

## **Minimum Agent Context**

An agent should receive only:

The assigned task  
Relevant approved requirements  
Necessary project metadata  
Relevant communication  
Permitted knowledge sources  
Permitted tool definitions

It should not automatically receive the entire:

* Client account  
* Email mailbox  
* Project repository  
* Document library  
* Production environment  
* Employee directory  
* Accounting system  
* Secret store

## **Agent Tool Restrictions**

Agents should not have general-purpose unrestricted tools.

Example:

Bad:  
send\_any\_email(recipient, subject, content)

Preferred:  
create\_client\_email\_draft(  
    approved\_contact\_id,  
    approved\_template\_id,  
    project\_id  
)

## **Agent Write Restrictions**

Agents should normally write through controlled business APIs rather than direct database access.

Example:

Agent Recommendation  
→ Policy Validation  
→ Permission Validation  
→ Human Approval When Required  
→ Business API Executes Action  
→ Audit Record Created

## **Prohibited Agent Actions**

Agents must not independently:

* Approve pricing.  
* Confirm contractual commitments.  
* Approve project scope.  
* Approve production deployments.  
* Expand their own permissions.  
* Access raw secrets.  
* Delete audit records.  
* Query unrelated projects.  
* Send restricted data to external services.  
* Merge protected branches.  
* Execute destructive database operations.  
* Permanently delete client information.  
* Train models using client data.  
* Modify security policies.

## **Prompt-Injection Controls**

Untrusted content must be treated as data, not instructions.

Examples include:

* Client emails  
* Uploaded documents  
* Jira comments  
* Slack messages  
* GitHub issues  
* Website content  
* Third-party API responses

Controls should include:

* Clear separation between system instructions and retrieved content.  
* Removal or marking of embedded instructions.  
* Tool allowlists.  
* Server-side authorization.  
* Output validation.  
* Human confirmation for external actions.  
* Limits on repeated tool calls.  
* No secret access through model prompts.  
* No automatic execution of code found in documents.

## **Agent Output Validation**

Agent-generated outputs should be validated before use:

| Output | Required Validation |
| ----- | ----- |
| SRS | Template, requirement completeness and human approval |
| Ticket | Required fields, project scope and TL approval |
| Email | Recipient authorization, data classification and human approval where required |
| Status change | Valid transition and actor permission |
| Assignment | Skill, capacity and TL authority |
| Code | Testing, scanning and human code review |
| Deployment instruction | Approved release and DevOps validation |
| SQL or migration | Review and restricted execution |

---

# **9\. API Key Management**

## **Key Management Principles**

Each API key must have:

Key ID  
Provider  
Purpose  
Environment  
Owner  
Allowed Service  
Allowed Scopes  
Creation Date  
Expiry Date  
Rotation Date  
Last Used Date  
Status

## **Requirements**

* Prefer workload identity or managed identity instead of static API keys.  
* Store runtime secrets in a dedicated secrets manager.  
* Store separate credentials for development, staging, and production.  
* Use minimum API scopes.  
* Set expiration where supported.  
* Rotate keys automatically where possible.  
* Revoke credentials immediately after compromise.  
* Do not share keys between applications.  
* Do not use an employee’s personal token for production services.  
* Monitor unused and unusually used keys.

Azure Key Vault provides centralized storage for API keys, passwords, connection strings, keys, and certificates. Current Microsoft guidance recommends least-privilege RBAC, monitoring, network restrictions, and separate vaults by application and environment. ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/key-vault/secrets/secure-secrets?utm_source=chatgpt.com))

## **Recommended Responsibility**

1Password  
→ Human-controlled recovery details and controlled credential sharing

Azure Key Vault  
→ Runtime API credentials, database connections, certificates and service secrets

---

# **10\. Secret Storage**

## **Secrets Include**

* API keys  
* OAuth client secrets  
* Database connection strings  
* Signing keys  
* Encryption keys  
* Webhook secrets  
* Deployment tokens  
* Private certificates  
* SMTP credentials  
* Cloud credentials  
* Model-provider credentials

## **Secrets Must Never Be Stored In**

* Source code  
* Git repositories  
* `.env` files committed to Git  
* Jira tickets  
* Slack messages  
* Email  
* Agent prompts  
* Model memory  
* Application logs  
* Audit `before_data` or `after_data`  
* Database business tables  
* Client-facing documents

## **Runtime Access**

Applications should retrieve secrets using:

* Managed identity  
* Workload identity  
* Service principal with minimum access  
* Short-lived credentials

The application should normally receive a secret value at runtime without exposing it to users or AI agents.

## **Rotation Defaults**

| Secret Type | Recommended Rotation |
| ----- | ----- |
| Temporary tokens | Hours or days |
| OAuth access tokens | Provider-controlled |
| Webhook secrets | 90–180 days |
| Service API keys | 90 days where supported |
| Database application credentials | 60–90 days |
| Signing or encryption keys | Based on cryptographic policy |
| Emergency credentials | Immediately after use |

Rotation periods must also follow provider capabilities and client requirements.

---

# **11\. Audit Logging**

An audit log is a chronological record of system access and operations. NIST and OWASP guidance recommends logging security-relevant events and protecting and retaining logs according to organizational policy. ([NIST Publications](https://nvlpubs.nist.gov/nistpubs/legacy/SP/nistspecialpublication800-92.Pdf?utm_source=chatgpt.com))

## **Events That Must Be Logged**

### **Authentication**

* Login success and failure  
* MFA result  
* Password reset  
* Session creation and revocation  
* Suspicious authentication attempt

### **Authorization**

* Access denied  
* Restricted-document access  
* Permission change  
* Role assignment  
* Project membership change  
* Impersonation

### **Business Actions**

* Requirement changes  
* Status transitions  
* Assignments  
* Approval requests and decisions  
* Follow-up escalation  
* Change requests  
* Project holds and cancellation  
* Project completion

### **Agent Actions**

* Agent invoked  
* Trigger  
* Model and prompt version  
* Knowledge sources used  
* Tools requested  
* Tools executed  
* Result  
* Human reviewer  
* Approval outcome  
* Failure  
* Cost and token usage

### **Technical and Security Actions**

* Integration connection  
* API credential creation or revocation  
* Secret access metadata  
* File upload and malware result  
* Data export  
* Deployment  
* Rollback  
* Backup and restore  
* Configuration change  
* Security alert

## **Required Audit Fields**

Audit ID  
Organization ID  
Project ID  
Actor ID  
Actor Type  
Action  
Entity Type  
Entity ID  
Previous State  
New State  
Reason  
Source  
Correlation ID  
IP Address  
Device or User Agent  
Timestamp  
Risk Level

## **Audit Protection**

* Append-only for normal users and agents.  
* No direct updates or deletion.  
* Centralized log collection.  
* Restricted administrator access.  
* Encryption in transit and at rest.  
* Integrity monitoring.  
* Alerts for logging failures.  
* Redaction of passwords, tokens, secrets and unnecessary PII.

Full prompts and outputs should not automatically be copied into logs. Store a redacted record or secure reference where detailed traceability is required.

---

# **12\. Data Retention**

There should not be one universal retention period. Retention must be configurable by:

* Client contract  
* Jurisdiction  
* Data type  
* Project type  
* Legal requirement  
* Security classification  
* Business requirement  
* Legal hold

## **Provisional MVP Defaults**

These are proposed operational defaults and should be approved by legal, management, and client stakeholders.

| Data Category | Proposed Default |
| ----- | ----- |
| Active client and project data | While contract/project is active |
| Closed project operational data | 3 years after closure |
| Approved SRS and delivery records | 3–7 years according to contract |
| Approval and change-request history | 3–7 years |
| Security and authentication logs | 12 months searchable |
| Archived audit logs | Additional 12–24 months |
| Agent execution records | 12 months |
| Full redacted model inputs/outputs | 90–180 days where required |
| Temporary uploaded files | 7–30 days |
| Rejected or quarantined files | 7 days |
| Soft-deleted business records | 30 days |
| Client portal sessions | According to authentication policy |
| Backups | According to the backup schedule below |

## **Retention Requirements**

* Support legal holds.  
* Stop deletion when a legal hold exists.  
* Record deletion requests and outcomes.  
* Purge embeddings when their source document is deleted.  
* Remove files, extracted text, caches, search indexes and replicas.  
* Preserve only the minimum audit evidence required.  
* Notify the client when deletion cannot occur because of contractual or legal requirements.

---

# **13\. Backup and Recovery Policy**

NIST contingency-planning guidance recommends identifying recovery priorities, recovery strategies, testing, maintenance, and the business impact of system disruption. ([NIST Computer Security Resource Center](https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final?utm_source=chatgpt.com))

## **Recommended MVP Recovery Targets**

| Metric | Target |
| ----- | ----- |
| Database RPO | 15 minutes or less |
| Application RTO | 4 hours or less |
| Critical production incident RTO | 1–2 hours where feasible |
| File-storage recovery | 4 hours |
| Configuration recovery | 4 hours |

## **Backup Schedule**

| Backup | Frequency | Retention |
| ----- | ----- | ----- |
| PostgreSQL point-in-time recovery | Continuous | 7–14 days |
| Daily database backup | Daily | 35 days |
| Monthly database backup | Monthly | 12 months |
| File-storage versioning | Continuous | 30–90 days |
| Configuration and infrastructure backup | On every approved change | Minimum 12 months |
| Secret-store recovery configuration | According to provider policy | Configurable |

## **Backup Requirements**

* Encrypt all backups.  
* Store backups separately from production.  
* Restrict backup access.  
* Use a separate account or security boundary.  
* Protect backups from ordinary deletion.  
* Monitor backup success.  
* Alert on backup failure.  
* Test database restoration at least quarterly.  
* Test full disaster recovery at least annually.  
* Document the last successful restore.  
* Include knowledge-base metadata, workflow configuration and audit data.

A backup should not be considered valid until a restoration test succeeds.

---

# **14\. File Upload Restrictions**

OWASP recommends allowlisting permitted file types, validating filenames and sizes, storing files safely, and protecting against malicious or deceptive uploads. ([OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html?utm_source=chatgpt.com))

## **Recommended Allowed Types**

Initially allow only business-required formats:

.pdf  
.docx  
.xlsx  
.pptx  
.csv  
.txt  
.png  
.jpg  
.jpeg  
.webp

ZIP files should be disabled by default and enabled only for approved workflows.

## **Blocked Types**

Block executable and script formats, including:

.exe  
.dll  
.bat  
.cmd  
.ps1  
.sh  
.js  
.jar  
.msi  
.scr  
.com  
.php  
.py

This blocklist is additional protection; the primary rule should remain an allowlist.

## **File Upload Validation**

The platform must:

* Validate extension.  
* Validate MIME type.  
* Validate file signature or magic bytes.  
* Enforce maximum file size.  
* Rename files using generated identifiers.  
* Remove dangerous path characters.  
* Scan for malware.  
* Scan archive contents when archives are enabled.  
* Reject password-protected files unless approved.  
* Detect excessive decompression size.  
* Store files outside the application execution path.  
* Prevent file execution.  
* Record checksum.  
* Record uploader and project.  
* Apply document permissions.  
* Reject duplicate malicious files.

## **Recommended Size Limits**

| File Type | Default Limit |
| ----- | ----- |
| Image | 10 MB |
| PDF | 25 MB |
| Office document | 25 MB |
| CSV or text | 10 MB |
| Approved archive | 100 MB |
| Total files per request | Configurable |

## **File Processing Lifecycle**

Uploaded  
→ Quarantined  
→ Type Validated  
→ Malware Scanned  
→ Content Processed  
→ Access Classification Applied  
→ Available

Rejected lifecycle:

Uploaded  
→ Quarantined  
→ Validation or Scan Failed  
→ Rejected  
→ Security Event Recorded  
→ Deleted According to Policy

A file must not be sent to an AI model or indexed into the knowledge base before scanning and permission validation are complete.

---

# **15\. Personally Identifiable Information Handling**

PII includes information that identifies or can be linked to a specific individual. NIST recommends context-based identification and protection of PII against inappropriate access, use, and disclosure. ([NIST Computer Security Resource Center](https://csrc.nist.gov/pubs/sp/800/122/final?utm_source=chatgpt.com))

## **PII Examples**

* Name  
* Personal email  
* Phone number  
* Address  
* Government identifier  
* Date of birth  
* Financial information  
* Employment details  
* Authentication information  
* IP address and device information  
* Client communication associated with an individual

## **PII Classification**

| Level | Example | Protection |
| ----- | ----- | ----- |
| Low | Business name and public job title | Standard controlled access |
| Moderate | Email, phone and private communication | Project-restricted access |
| High | Financial, identity, health or authentication data | Restricted access and enhanced controls |

## **PII Requirements**

* Collect only information required for the workflow.  
* Document the purpose for collection.  
* Restrict access by role and project.  
* Mask information where full values are unnecessary.  
* Encrypt sensitive values.  
* Never store passwords in reversible form.  
* Exclude unnecessary PII from logs.  
* Use synthetic data for development and testing.  
* Support access, correction, export and deletion requests.  
* Record consent when required.  
* Define breach-notification procedures.  
* Do not copy client PII into another client’s knowledge base.  
* Do not send high-risk PII to external models without approval and contractual coverage.

## **Example Redaction**

Original:  
John Smith, john.smith@example.com, \+1 305 555 1234

Agent Context:  
Client Contact ID: CNT-1024  
Name: John  
Email: \[REDACTED\]  
Phone: \[REDACTED\]

The full information should be provided only when the task genuinely requires it.

---

# **16\. Model Training and Data-Sharing Restrictions**

## **Default Policy**

Client and Company Data  
→ Must Not Be Used for Model Training  
→ Unless Explicit Written Approval Exists

## **Provider Contract Requirements**

Before connecting an AI provider, confirm:

* Submitted data is not used for provider model training by default.  
* Data-retention controls are available.  
* Deletion procedures are documented.  
* Encryption is provided.  
* Data regions are documented.  
* Subprocessors are disclosed.  
* Breach-notification obligations are documented.  
* Access by provider personnel is controlled.  
* Enterprise or API terms are approved.  
* A data-processing agreement is available where required.

## **Internal Training Restrictions**

The company must not use:

* Client requirements  
* Source code  
* Emails  
* Documents  
* Tickets  
* Production data  
* Financial information  
* Personal information

to fine-tune or train models without written client authorization.

## **Model Input Rules**

Before data is sent to a model:

Verify Project Permission  
→ Verify Knowledge Approval  
→ Classify Information  
→ Remove Secrets  
→ Redact Unnecessary PII  
→ Apply Provider Policy  
→ Send Minimum Context  
→ Record Usage

## **Model Output Rules**

* Outputs are recommendations until validated.  
* Sensitive outputs must be reviewed.  
* Agent output cannot create permissions.  
* Generated code must undergo security review.  
* Generated communication must pass recipient and classification checks.  
* Generated decisions must not replace required human approvals.

NIST’s AI Risk Management Framework and its Generative AI profile recommend formal governance, documented responsibilities, privacy and information-security controls, and risk management throughout the AI lifecycle. ([NIST](https://www.nist.gov/itl/ai-risk-management-framework?utm_source=chatgpt.com))

---

# **17\. Data-Sharing Matrix**

| Data Type | Internal Agents | External AI Model | Client Users | External Integrations |
| ----- | ----- | ----- | ----- | ----- |
| Public service information | Allowed | Allowed | Allowed | Allowed |
| Internal process template | Authorized agents | Approved provider only | Normally no | Limited |
| Client requirements | Assigned agents | Minimum required context | Own client only | Approved systems only |
| Source code | Assigned technical agents | Only under approved policy | No | Git platform only |
| Pricing rules | BD/PM agents with restrictions | Normally no | Final quotation only | Accounting/CRM if approved |
| Production secrets | Never | Never | Never | Direct secret-manager integration only |
| Audit logs | Orchestrator/security only | Normally no | Limited client-visible events | Security platform only |
| PII | Minimum necessary | Redacted where possible | Own authorized records | Approved integrations only |
| Security incidents | Security-authorized agents | Normally no | Approved summary only | Security tools only |

---

# **18\. Security Administration Requirements**

Administrators must be able to configure:

* Roles  
* Permissions  
* Project access  
* Document classifications  
* Agent tool access  
* Agent authority  
* Secret references  
* Data retention  
* File upload rules  
* Model-provider policies  
* Approval requirements  
* Security notification rules  
* Session policies  
* MFA requirements  
* Access expiry  
* IP or network restrictions where required

Every security-policy change must:

* Require appropriate approval.  
* Be versioned.  
* Record the previous and new configuration.  
* Record the responsible human.  
* Generate an audit event.  
* Notify affected administrators.

---

# **19\. Security Incident Flow**

Security Event Detected  
→ Incident Created  
→ Security Owner Assigned  
→ Access Contained  
→ Credentials Revoked or Rotated  
→ Impact Assessed  
→ Evidence Preserved  
→ Client and Management Notification Evaluated  
→ Recovery Completed  
→ Root Cause Documented  
→ Security Rules Updated  
→ Incident Closed

Agents may detect and summarize incidents but should not independently make legal, client-notification, or destructive containment decisions.

---

# **20\. Security Acceptance Criteria**

Security prerequisites will be complete when:

* All human and agent roles have approved permissions.  
* Deny-by-default access is implemented.  
* MFA is enabled for privileged users.  
* Client data isolation passes automated tests.  
* Project access requires active membership.  
* PostgreSQL RLS is enabled on sensitive tenant tables.  
* Documents have classifications and access controls.  
* Agents use scoped identities and allowlisted tools.  
* Agents cannot access raw production secrets.  
* Runtime secrets are stored in an approved secret manager.  
* Development, staging and production credentials are separated.  
* Audit logs are append-only and protected.  
* Retention periods are configured by data category.  
* Backup and restore tests pass.  
* File uploads are quarantined and scanned.  
* PII is classified, minimized and protected.  
* AI-provider terms and data-processing requirements are approved.  
* Client data is excluded from model training by default.  
* Prompt-injection and excessive-agency controls are tested.  
* Human approval gates prevent unauthorized agent actions.  
* Security and access tests are included in the Definition of Done.

The central enforcement principle should be:

Minimum Data  
\+ Minimum Permission  
\+ Minimum Duration  
\+ Human Approval for High-Risk Actions  
\+ Complete Audit History

