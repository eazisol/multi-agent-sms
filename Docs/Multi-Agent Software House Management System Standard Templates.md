# Agentic Software House Standard Templates

## Purpose

These templates provide a consistent structure for all documents created by BD, PM, TL, Developer, Designer, QA, DevOps, and Orchestrator Agents.

Each template should be:

- Version-controlled  
- Linked to the relevant client, project, phase, requirement, or ticket  
- Reviewed by the responsible human role  
- Stored in the shared project knowledge base  
- Traceable through audit logs  
- Reusable across different project types

---

# Standard Document Metadata

The following metadata should appear at the beginning of every document:

| Field | Description |
| :---- | :---- |
| Document ID | Unique document identifier |
| Document Type | Questionnaire, SRS, Roadmap, Bug Report, etc. |
| Client | Client or organization name |
| Project | Project name |
| Project ID | Unique project identifier |
| Related Phase | Project phase, if applicable |
| Related Requirement IDs | Linked requirement identifiers |
| Related Ticket IDs | Linked ticket identifiers |
| Version | Document version |
| Status | Draft, Under Review, Approved, Rejected, Superseded, Archived |
| Prepared By | Agent or human who created the document |
| Reviewed By | Assigned reviewer |
| Approved By | Authorized approver |
| Created Date | Initial creation date |
| Last Updated | Latest modification date |
| Approval Date | Date approved |
| Confidentiality | Public, Internal, Confidential, Restricted |

## Standard Approval Section

Prepared By:

Reviewed By:

Approved By:

Approval Status:

Approval Date:

Comments:

## Standard Version History

| Version | Date | Updated By | Changes | Approval Status |
| :---- | :---- | :---- | :---- | :---- |

---

# 1\. Client Requirement Questionnaire

## Document Purpose

Used by the BD Agent and Human BD to collect complete business, functional, technical, commercial, and delivery information from the client.

## Template

### A. Client Information

- Client name:  
- Company name:  
- Industry:  
- Email:  
- Phone:  
- Country and time zone:  
- Preferred communication channel:  
- Primary decision-maker:  
- Other stakeholders:

### B. Project Overview

- Project name:  
- Briefly describe the project:  
- What problem should this project solve?  
- What is the main business objective?  
- Is this a new system, redesign, integration, or enhancement?  
- What is the expected business outcome?  
- Why is the project required now?

### C. Target Users

- Who will use the system?  
- What user roles are required?  
- Approximate number of users:  
- Are users internal, external, or both?  
- Are there user-location or language requirements?  
- Are accessibility requirements required?

### D. Functional Requirements

For every requested feature:

| Feature | Description | User Role | Priority | Expected Outcome |
| :---- | :---- | :---- | :---- | :---- |

Questions:

- What actions should users perform?  
- What data must users enter?  
- What information should the system display?  
- What reports are needed?  
- What notifications are required?  
- What approval workflows are required?  
- What search, filtering, sorting, import, or export functions are needed?

### E. User Journey

- How does a user start the process?  
- What are the main steps?  
- What decisions occur during the process?  
- What happens when the process succeeds?  
- What happens when the process fails?  
- What exceptions should be handled?

### F. Platforms

- Web application:  
- Mobile application:  
- Android:  
- iOS:  
- Desktop:  
- Tablet:  
- Admin portal:  
- Client portal:  
- Public website:

### G. Integrations

| Integration | Purpose | Existing Account | API Available | Sandbox Available |
| :---- | :---- | :---- | :---- | :---- |

Examples:

- Payment gateway  
- CRM  
- Accounting platform  
- Email service  
- SMS service  
- Calendar  
- Maps  
- Analytics  
- Social login  
- Third-party APIs

### H. Existing System

- Is there an existing application?  
- Current technology stack:  
- Source code available:  
- Documentation available:  
- Database available:  
- Hosting provider:  
- Current limitations:  
- Migration required:  
- Existing user/data volume:

### I. Non-Functional Requirements

- Expected number of users:  
- Expected traffic:  
- Required performance:  
- Security requirements:  
- Backup requirements:  
- Data retention:  
- Compliance requirements:  
- Availability target:  
- Browser support:  
- Device support:  
- Localization:  
- Scalability expectations:

### J. Design Requirements

- Existing brand guidelines:  
- Logo available:  
- Preferred color palette:  
- Design references:  
- Competitor references:  
- Required design style:  
- Existing wireframes:  
- Accessibility expectations:

### K. Timeline and Budget

- Target start date:  
- Target completion date:  
- Important deadline:  
- Budget range:  
- Preferred pricing model:  
- Payment expectations:  
- Phased delivery acceptable:  
- MVP required:

### L. Delivery and Support

- Hosting responsibility:  
- Deployment responsibility:  
- Training required:  
- Documentation required:  
- Maintenance required:  
- Warranty expectations:  
- Support channels:  
- Source-code handover required:

### M. Constraints and Risks

- Known technical constraints:  
- Legal constraints:  
- Business constraints:  
- Third-party dependencies:  
- Internal approval dependencies:  
- Known risks:

### N. Final Confirmation

- Client-confirmed project objective:  
- Client-confirmed priority:  
- Client-confirmed deadline:  
- Client-confirmed budget:  
- Open questions:  
- Next action:

---

# 2\. Requirement Brief

## Document Purpose

Summarizes the client’s business need and validated high-level requirements before proposal or SRS preparation.

## Template

### 1\. Executive Summary

- Client:  
- Project:  
- Business objective:  
- Problem statement:  
- Proposed solution summary:

### 2\. Project Background

- Current process:  
- Current problems:  
- Business impact:  
- Reason for change:

### 3\. Project Objectives

| Objective ID | Objective | Success Indicator | Priority |
| :---- | :---- | :---- | :---- |

### 4\. Scope Summary

#### In Scope

#### Out of Scope

### 5\. Target Users

| User Role | Description | Key Needs |
| :---- | :---- | :---- |

### 6\. High-Level Features

| Feature ID | Feature | Description | Priority |
| :---- | :---- | :---- | :---- |

### 7\. Platforms

- Web:  
- Mobile:  
- Admin:  
- Client portal:  
- Other:

### 8\. Integrations

| Integration | Purpose | Dependency | Current Status |
| :---- | :---- | :---- | :---- |

### 9\. Non-Functional Requirements

- Security:  
- Performance:  
- Scalability:  
- Availability:  
- Compliance:  
- Accessibility:  
- Backup:  
- Data retention:

### 10\. Assumptions

### 11\. Constraints

### 12\. Risks

| Risk | Impact | Likelihood | Proposed Mitigation |
| :---- | :---- | :---- | :---- |

### 13\. Open Questions

| Question | Responsible Party | Due Date | Status |
| :---- | :---- | :---- | :---- |

### 14\. Client Priorities

- Must have:  
- Should have:  
- Could have:  
- Future phase:

### 15\. Approval

- Prepared by:  
- Reviewed by:  
- Client confirmation:  
- Approval status:

---

# 3\. Project Handover Document

## Document Purpose

Transfers the project from BD to PM and TL after commercial acceptance.

## Template

### 1\. Project Identification

- Client:  
- Project name:  
- Project ID:  
- Proposal reference:  
- Contract reference:  
- Handover date:

### 2\. Commercial Summary

- Approved budget:  
- Pricing model:  
- Payment terms:  
- Deposit status:  
- Delivery commitment:  
- Support terms:  
- Special commitments:

### 3\. Scope Summary

#### In Scope

#### Out of Scope

### 4\. Key Requirements

| Requirement ID | Requirement | Priority | Status |
| :---- | :---- | :---- | :---- |

### 5\. Client Contacts

| Name | Role | Email | Phone | Decision Authority |
| :---- | :---- | :---- | :---- | :---- |

### 6\. Internal Ownership

| Role | Assigned Person | Responsibility |
| :---- | :---- | :---- |
| Human BD |  |  |
| PM |  |  |
| TL |  |  |
| QA Lead |  |  |
| DevOps |  |  |

### 7\. Timeline and Milestones

| Milestone | Target Date | Dependency |
| :---- | :---- | :---- |

### 8\. Required Access

| Access | Owner | Status | Due Date |
| :---- | :---- | :---- | :---- |

### 9\. Client Communication Rules

- Primary client contact:  
- Update frequency:  
- Communication channel:  
- Approval method:  
- Escalation contact:

### 10\. Risks and Dependencies

| Item | Type | Owner | Status | Mitigation |
| :---- | :---- | :---- | :---- | :---- |

### 11\. Pending Items

| Item | Responsible Party | Deadline | Status |
| :---- | :---- | :---- | :---- |

### 12\. Handover Acceptance

- BD confirmation:  
- PM acceptance:  
- TL acceptance:  
- Missing information:  
- Handover status:

---

# 4\. Software Requirements Specification

## Document Purpose

Defines the complete functional, non-functional, interface, validation, security, and acceptance requirements.

## Template

### 1\. Introduction

#### 1.1 Purpose

#### 1.2 Project Scope

#### 1.3 Definitions and Abbreviations

#### 1.4 Reference Documents

#### 1.5 Intended Audience

### 2\. Product Overview

#### 2.1 Business Context

#### 2.2 Product Perspective

#### 2.3 Product Objectives

#### 2.4 User Types

| Role | Description | Permissions |
| :---- | :---- | :---- |

### 3\. System Scope

#### 3.1 In Scope

#### 3.2 Out of Scope

#### 3.3 Assumptions

#### 3.4 Constraints

### 4\. Functional Requirements

For every requirement:

#### Requirement Template

- Requirement ID:  
- Requirement title:  
- Module:  
- Description:  
- Business purpose:  
- Actor:  
- Preconditions:  
- Trigger:  
- Main flow:  
- Alternative flow:  
- Exception flow:  
- Inputs:  
- Outputs:  
- Validation:  
- Permissions:  
- Dependencies:  
- Priority:  
- Acceptance criteria:  
- Related design:  
- Related ticket:  
- Status:

### 5\. Business Rules

| Rule ID | Rule | Applies To | Exception |
| :---- | :---- | :---- | :---- |

### 6\. Data Requirements

| Entity | Field | Data Type | Required | Validation | Description |
| :---- | :---- | :---- | :---- | :---- | :---- |

### 7\. User Interface Requirements

- Screen list:  
- Navigation:  
- Responsive behavior:  
- Accessibility:  
- Error messages:  
- Empty states:  
- Loading states:  
- Confirmation dialogs:

### 8\. Integration Requirements

| Integration ID | System | Direction | Data | Authentication | Error Handling |
| :---- | :---- | :---- | :---- | :---- | :---- |

### 9\. Non-Functional Requirements

#### 9.1 Performance

#### 9.2 Security

#### 9.3 Availability

#### 9.4 Scalability

#### 9.5 Reliability

#### 9.6 Accessibility

#### 9.7 Compliance

#### 9.8 Backup and Recovery

#### 9.9 Logging and Monitoring

### 10\. Reporting Requirements

| Report | Users | Filters | Output | Frequency |
| :---- | :---- | :---- | :---- | :---- |

### 11\. Notification Requirements

| Event | Recipient | Channel | Trigger | Template |
| :---- | :---- | :---- | :---- | :---- |

### 12\. Acceptance Criteria

### 13\. Requirement Traceability Matrix

| Requirement ID | Phase | User Story | Ticket | Test Case | Release |
| :---- | :---- | :---- | :---- | :---- | :---- |

### 14\. Open Questions

### 15\. Approval

---

# 5\. Project Roadmap

## Document Purpose

Provides the high-level delivery sequence, phases, milestones, dependencies, and expected outcomes.

## Template

### 1\. Roadmap Overview

- Project:  
- Start date:  
- Target completion:  
- Delivery model:  
- Roadmap owner:

### 2\. Strategic Goals

| Goal | Description | Target Outcome |
| :---- | :---- | :---- |

### 3\. Phase Summary

| Phase | Objective | Main Deliverables | Start | End | Status |
| :---- | :---- | :---- | :---- | :---- | :---- |

### 4\. Milestones

| Milestone | Description | Target Date | Approval Owner |
| :---- | :---- | :---- | :---- |

### 5\. Dependencies

| Dependency | Related Phase | Owner | Impact |
| :---- | :---- | :---- | :---- |

### 6\. Resource Summary

| Role | Required Capacity | Phase |
| :---- | :---- | :---- |

### 7\. Risk Summary

| Risk | Impacted Phase | Mitigation |
| :---- | :---- | :---- |

### 8\. Release Plan

| Release | Features | Target Date | Environment |
| :---- | :---- | :---- | :---- |

### 9\. Roadmap Approval

---

# 6\. Phase Plan

## Document Purpose

Defines the detailed execution plan for one project phase.

## Template

### 1\. Phase Information

- Phase ID:  
- Phase name:  
- Objective:  
- Start date:  
- End date:  
- Phase owner:  
- Status:

### 2\. Scope

#### Included

#### Excluded

### 3\. Deliverables

| Deliverable | Description | Owner | Due Date |
| :---- | :---- | :---- | :---- |

### 4\. Requirements

| Requirement ID | Description | Priority |
| :---- | :---- | :---- |

### 5\. Tickets

| Ticket ID | Title | Type | Owner | Estimate | Status |
| :---- | :---- | :---- | :---- | :---- | :---- |

### 6\. Resources

| Role | Assigned Person | Capacity |
| :---- | :---- | :---- |

### 7\. Dependencies

| Dependency | Owner | Required By | Status |
| :---- | :---- | :---- | :---- |

### 8\. QA Plan

- Test scope:  
- Test environment:  
- Test data:  
- Regression requirements:  
- Acceptance gate:

### 9\. Risks

| Risk | Probability | Impact | Mitigation | Owner |
| :---- | :---- | :---- | :---- | :---- |

### 10\. Phase Completion Criteria

### 11\. Approval

---

# 7\. User Story

## Document Purpose

Defines a user-centered requirement that can be implemented and tested.

## Template

- User Story ID:  
- Epic:  
- Module:  
- Priority:  
- Estimate:  
- Requirement reference:

### User Story Statement

As a \[user role\],

I want \[capability\],

so that \[business benefit\].

### Description

### Preconditions

### Main Flow

1\. 2\. 3\.

### Alternative Flow

### Exception Flow

### Acceptance Criteria

Given \[context\]

When \[action\]

Then \[expected result\]

### Validation Rules

| Field or Action | Validation | Error Message |
| :---- | :---- | :---- |

### Dependencies

### Design Reference

### API Reference

### Definition of Ready

- Requirement approved  
- Acceptance criteria available  
- Design available  
- Dependencies identified  
- Estimate provided

### Definition of Done

- Implementation complete  
- Code reviewed  
- Tests passed  
- QA passed  
- Documentation updated  
- Acceptance criteria satisfied

---

# 8\. Technical Ticket

## Document Purpose

Defines implementation-level work for developers, designers, QA, or DevOps.

## Template

- Ticket ID:  
- Ticket type:  
- Project:  
- Phase:  
- Module:  
- Priority:  
- Assignee:  
- Reviewer:  
- Estimate:  
- Due date:  
- Related user story:  
- Related requirement:

### Title

### Objective

### Technical Description

### Implementation Requirements

### Technical Approach

### Files or Components Affected

### API Changes

### Database Changes

### Validation Rules

### Security Considerations

### Logging Requirements

### Error Handling

### Dependencies

### Acceptance Criteria

### Test Requirements

### Required Evidence

- Pull request  
- Screenshots  
- API response  
- Test results  
- Migration result  
- Deployment log

### Definition of Done

### Review Notes

---

# 9\. Bug Report

## Document Purpose

Records a defect with sufficient evidence for investigation, prioritization, correction, and retesting.

## Template

- Bug ID:  
- Project:  
- Environment:  
- Build or version:  
- Module:  
- Related ticket:  
- Related requirement:  
- Reporter:  
- Assigned developer:  
- Severity:  
- Priority:  
- Status:  
- Reported date:

### Bug Title

### Summary

### Preconditions

### Steps to Reproduce

1\. 2\. 3\.

### Expected Result

### Actual Result

### Reproduction Frequency

- Always  
- Frequently  
- Intermittently  
- Once

### Evidence

- Screenshot:  
- Video:  
- Logs:  
- API response:  
- Browser console:  
- Network trace:

### Environment Details

- Browser:  
- Device:  
- Operating system:  
- User role:  
- Test account:

### Business Impact

### Technical Notes

### Workaround

### Root Cause

### Fix Description

### Retest Result

### Closure Evidence

---

# 10\. Test Case

## Document Purpose

Defines repeatable steps to verify one requirement, feature, validation rule, or business process.

## Template

- Test Case ID:  
- Project:  
- Module:  
- Requirement ID:  
- User story:  
- Test type:  
- Priority:  
- Prepared by:  
- Execution status:

### Test Objective

### Preconditions

### Test Data

| Field | Value |
| :---- | :---- |

### Test Steps

| Step | Action | Expected Result | Actual Result | Status |
| :---- | :---- | :---- | :---- | :---- |

### Postconditions

### Negative Scenarios

### Edge Cases

### Evidence

### Defect Reference

### Final Result

- Passed  
- Failed  
- Blocked  
- Not Run

### Reviewer Comments

---

# 11\. Risk Register

## Document Purpose

Tracks project, technical, operational, commercial, security, and delivery risks.

## Template

| Risk ID | Category | Description | Cause | Probability | Impact | Score | Owner | Mitigation | Contingency | Status |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |

## Risk Categories

- Scope  
- Requirement  
- Technical  
- Resource  
- Timeline  
- Budget  
- Security  
- Compliance  
- Third-party  
- Infrastructure  
- Quality  
- Client dependency  
- Communication

## Risk Scoring

Risk Score \= Probability × Impact

Suggested levels:

- Low  
- Medium  
- High  
- Critical

## Risk Review Section

- Review date:  
- Reviewed by:  
- New risks:  
- Closed risks:  
- Escalated risks:  
- Required decisions:

---

# 12\. Change Request

## Document Purpose

Formally controls changes to approved scope, requirements, design, timeline, cost, or delivery.

## Template

- Change Request ID:  
- Project:  
- Requester:  
- Request date:  
- Priority:  
- Related requirement:  
- Related phase:  
- Related ticket:  
- Status:

### Current Approved Requirement

### Requested Change

### Business Reason

### Expected Outcome

### Technical Impact

### Design Impact

### QA Impact

### Security Impact

### Data Impact

### Integration Impact

### Timeline Impact

### Resource Impact

### Cost Impact

### Risks

### Alternatives Considered

### Recommendation

### Approval Decision

- Approved  
- Rejected  
- Deferred  
- More information required

### Approvers

| Role | Name | Decision | Date | Comments |
| :---- | :---- | :---- | :---- | :---- |

### Implementation Plan

### Updated Documents

- SRS version:  
- Roadmap version:  
- Tickets:  
- Release:

---

# 13\. Progress Report

## Document Purpose

Provides an internal project health and delivery summary for PM, TL, BD, and management.

## Template

### 1\. Report Information

- Project:  
- Reporting period:  
- Prepared by:  
- Overall status:  
- Project completion:  
- Phase completion:

### 2\. Executive Summary

### 3\. Completed Work

| Item | Owner | Completion Date | Evidence |
| :---- | :---- | :---- | :---- |

### 4\. Work in Progress

| Item | Owner | Progress | Due Date | Status |
| :---- | :---- | :---- | :---- | :---- |

### 5\. Upcoming Work

| Item | Owner | Planned Start | Due Date |
| :---- | :---- | :---- | :---- |

### 6\. Milestone Status

| Milestone | Planned Date | Current Forecast | Status |
| :---- | :---- | :---- | :---- |

### 7\. Risks

| Risk | Impact | Owner | Mitigation |
| :---- | :---- | :---- | :---- |

### 8\. Blockers

| Blocker | Owner | Age | Escalation Level | Next Action |
| :---- | :---- | :---- | :---- | :---- |

### 9\. QA Status

- Tickets passed:  
- Tickets failed:  
- Open bugs:  
- Critical bugs:  
- Regression status:

### 10\. Timeline Status

- On track:  
- At risk:  
- Delayed:  
- Recovery plan:

### 11\. Decisions Required

| Decision | Required From | Due Date | Impact |
| :---- | :---- | :---- | :---- |

### 12\. Overall Health

- Scope:  
- Schedule:  
- Budget:  
- Quality:  
- Resources:  
- Client dependency:

---

# 14\. Client Update

## Document Purpose

Provides a clear, non-technical client-facing project update.

## Template

### Subject

Project Update – \[Project Name\] – \[Date\]

### Opening

Hello \[Client Name\],

Here is the latest update on the \[Project Name\] project.

### Completed This Period

### Currently in Progress

### Next Steps

### Decisions or Information Required

### Risks or Delays

- None

or:

- Issue:  
- Impact:  
- Proposed action:  
- Required decision:

### Upcoming Milestone

- Milestone:  
- Expected date:  
- Current status:

### Closing

Please review the items above and share any required feedback or approval by \[date\].

Regards,  
\[Name / Team\]

---

# 15\. Meeting Summary

## Document Purpose

Records discussions, decisions, action items, open questions, and follow-ups from internal or client meetings.

## Template

### Meeting Information

- Meeting title:  
- Project:  
- Date:  
- Start time:  
- End time:  
- Location or platform:  
- Meeting type:  
- Prepared by:

### Participants

| Name | Role | Organization |
| :---- | :---- | :---- |

### Agenda

1\. 2\. 3\.

### Discussion Summary

#### Topic 1

#### Topic 2

### Decisions

| Decision ID | Decision | Approved By | Date |
| :---- | :---- | :---- | :---- |

### Action Items

| Action | Owner | Due Date | Priority | Status |
| :---- | :---- | :---- | :---- | :---- |

### Open Questions

| Question | Responsible Party | Due Date |
| :---- | :---- | :---- |

### Risks or Concerns

### Follow-Up Meeting

- Required:  
- Proposed date:  
- Purpose:

---

# 16\. Release Notes

## Document Purpose

Documents the content, changes, fixes, known issues, deployment requirements, and validation result of a software release.

## Template

### Release Information

- Project:  
- Release version:  
- Release date:  
- Environment:  
- Release type:  
- Prepared by:  
- Approved by:

### Release Summary

### New Features

| Feature | Description | Requirement or Ticket |
| :---- | :---- | :---- |

### Enhancements

| Enhancement | Description | Ticket |
| :---- | :---- | :---- |

### Bug Fixes

| Bug ID | Description | Severity |
| :---- | :---- | :---- |

### Technical Changes

### Database Changes

### API Changes

### Configuration Changes

### Security Changes

### Deployment Instructions

1\. 2\. 3\.

### Migration Instructions

### Rollback Plan

### Known Issues

| Issue | Impact | Workaround |
| :---- | :---- | :---- |

### QA Summary

- Test cycle:  
- Passed:  
- Failed:  
- Known accepted issues:  
- QA approval:

### Post-Deployment Checks

- Application health  
- API health  
- Database  
- Authentication  
- Notifications  
- Critical user flows

---

# 17\. Project Completion Report

## Document Purpose

Confirms that the project has been delivered, tested, deployed, accepted, documented, and transferred to support or maintenance.

## Template

### 1\. Project Information

- Client:  
- Project:  
- Project ID:  
- Start date:  
- Completion date:  
- PM:  
- TL:  
- Final release:

### 2\. Executive Summary

### 3\. Original Objectives

| Objective | Result | Status |
| :---- | :---- | :---- |

### 4\. Delivered Scope

| Deliverable | Status | Evidence |
| :---- | :---- | :---- |

### 5\. Out-of-Scope or Deferred Items

| Item | Reason | Future Recommendation |
| :---- | :---- | :---- |

### 6\. Requirement Completion

- Total requirements:  
- Completed:  
- Deferred:  
- Rejected:  
- Traceability status:

### 7\. Quality Summary

- QA result:  
- Open critical bugs:  
- Open high bugs:  
- Accepted known issues:  
- Test evidence location:

### 8\. Deployment Summary

- Production date:  
- Deployment status:  
- Rollback required:  
- Monitoring status:  
- Post-release issues:

### 9\. Documentation Delivered

- User guide  
- Admin guide  
- API documentation  
- Technical documentation  
- Deployment documentation  
- Source-code handover  
- Credentials handover reference

### 10\. Training and Handover

- Training completed:  
- Participants:  
- Support owner:  
- Maintenance plan:  
- Warranty period:

### 11\. Commercial Closure

- Final invoice:  
- Payment status:  
- Approved variations:  
- Outstanding commercial items:

### 12\. Lessons Learned

#### What went well

#### What could be improved

#### Recommended process changes

### 13\. Client Acceptance

- Client representative:  
- Acceptance date:  
- Acceptance status:  
- Comments:

### 14\. Internal Closure Approval

| Role | Name | Approval | Date |
| :---- | :---- | :---- | :---- |
| PM |  |  |  |
| TL |  |  |  |
| QA |  |  |  |
| BD |  |  |  |

---

# Template Governance Rules

## 1\. Template Ownership

Each template must have a responsible owner:

| Template | Primary Owner |
| :---- | :---- |
| Client requirement questionnaire | BD |
| Requirement brief | BD / PM |
| Project handover | PM |
| SRS | PM / Business Analyst |
| Project roadmap | PM |
| Phase plan | PM / TL |
| User story | PM / Business Analyst |
| Technical ticket | TL |
| Bug report | QA |
| Test case | QA |
| Risk register | PM |
| Change request | PM |
| Progress report | PM / TL |
| Client update | BD / PM |
| Meeting summary | Meeting organizer |
| Release notes | TL / DevOps |
| Project completion report | PM |

## 2\. Approval Rules

- Agents may prepare drafts.  
- Authorized humans must approve final client-facing or project-baseline documents.  
- Approved templates cannot be modified silently.  
- Updated templates require version history.  
- Superseded versions must remain available for audit.

## 3\. Knowledge Base Use

Existing company documents should be:

1. Collected and categorized.  
2. Reviewed for quality and completeness.  
3. Compared with the new standard templates.  
4. Approved or rejected as reference examples.  
5. Tagged by project type, industry, module, and document type.  
6. Added to the shared knowledge base.  
7. Used by agents only when marked as approved.

## 4\. Agent Output Rules

Before generating a document, the agent must:

- Identify the correct template.  
- Load the latest approved version.  
- Populate all mandatory fields.  
- Mark unknown information clearly.  
- Never invent missing approvals, estimates, prices, or client decisions.  
- Link the document to relevant records.  
- Submit the document for required human review.  
- Store the final approved version in the knowledge base.

