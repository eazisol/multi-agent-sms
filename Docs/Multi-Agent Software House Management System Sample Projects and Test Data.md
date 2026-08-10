# Sample Projects and Test Data

## Purpose

This document provides three realistic but fully synthetic historical projects for validating the multi-agent software house management system.

The projects test whether BD, PM, TL, Developer, Designer, QA, DevOps, and Orchestrator Agents can correctly:

- Understand client queries  
- Gather missing requirements  
- Create requirement briefs and SRS documents  
- Divide projects into phases  
- Create and assign tickets  
- Track progress and blockers  
- Process bugs and client feedback  
- Manage change requests  
- Prepare delivery documentation  
- Maintain approvals, traceability, and audit history

>   
> All names, contacts, dates, budgets, and project details are fictional and intended only for controlled testing.

---

# Project 1: Small Website Project

## Project Summary

| Field | Value |
| :---- | :---- |
| Project ID | PRJ-SAMPLE-001 |
| Client | Northfield Home Services |
| Project Type | Small Business Website |
| Industry | Home Maintenance Services |
| Delivery Model | Fixed Price |
| Duration | 4 Weeks |
| Team Size | 4 |
| Complexity | Low |
| Final Status | Completed |

## 1\. Original Client Query

**Source:** Website inquiry form  
**Query ID:** QRY-001  
**Initial Status:** New  
**Priority:** Normal

> We are a local home maintenance company and need a professional website. Our current website is old and does not work properly on mobile devices. We need pages for our services, an inquiry form, customer reviews, and contact information. We would like the site completed within one month.

## 2\. Requirement Conversations

### Conversation 1

**BD Agent:** How many services should be displayed?

**Client:** Plumbing, electrical repair, painting, HVAC maintenance, and general handyman services.

### Conversation 2

**BD Agent:** Do you need online booking or only an inquiry form?

**Client:** Only an inquiry form for now. Online booking may be added later.

### Conversation 3

**BD Agent:** Do you already have a logo, brand colors, images, and reviews?

**Client:** We have a logo, some images, and eight Google reviews.

### Conversation 4

**BD Agent:** Who should receive inquiries, and which fields should be collected?

**Client:** Send them to our service mailbox. Collect name, phone, email, service type, address, preferred contact time, and message.

### Conversation 5

**BD Agent:** Should privacy and terms pages be included?

**Client:** Yes.

## 3\. Final Requirements

### Functional Requirements

| Requirement ID | Requirement | Priority |
| :---- | :---- | :---- |
| REQ-001 | Responsive home page | Must Have |
| REQ-002 | Five service pages | Must Have |
| REQ-003 | About-us page | Must Have |
| REQ-004 | Approved customer reviews | Must Have |
| REQ-005 | Contact and inquiry form | Must Have |
| REQ-006 | Email inquiry notifications | Must Have |
| REQ-007 | Store inquiries in admin panel | Should Have |
| REQ-008 | Privacy and terms pages | Must Have |
| REQ-009 | Google Maps location | Should Have |
| REQ-010 | Admin content editing | Must Have |

### Non-Functional Requirements

- Responsive on desktop, tablet, and mobile  
- Main pages should load within three seconds under normal conditions  
- Server-side form validation  
- HTTPS required  
- Current Chrome, Edge, Safari, and Firefox support  
- Basic accessibility compliance

### Out of Scope

- Online payments  
- Online booking  
- Customer portal  
- Multilingual support  
- CRM integration  
- Mobile application

## 4\. SRS Summary

### User Roles

| Role | Permissions |
| :---- | :---- |
| Visitor | View pages and submit inquiries |
| Administrator | Manage content, reviews, and inquiries |

### Inquiry Form

| Field | Type | Required | Validation |
| :---- | :---- | ----: | :---- |
| Full Name | Text | Yes | 2–100 characters |
| Email | Email | Yes | Valid email format |
| Phone | Text | Yes | 7–20 valid phone characters |
| Service Type | Dropdown | Yes | Configured service only |
| Address | Text | No | Maximum 250 characters |
| Preferred Contact Time | Dropdown | No | Morning, Afternoon, Evening |
| Message | Text Area | Yes | 10–1,000 characters |
| Consent | Checkbox | Yes | Must be selected |

### Workflow

Visitor Opens Contact Page

\-\> Completes Form

\-\> Form Is Validated

\-\> Inquiry Is Stored

\-\> Email Notification Is Sent

\-\> Success Message Is Displayed

## 5\. Project Phases

| Phase | Duration | Deliverables |
| :---- | ----: | :---- |
| Discovery and Content | 3 Days | Requirements, sitemap, content checklist |
| UI/UX Design | 5 Days | Desktop and mobile designs |
| Development | 8 Days | Website and admin content management |
| QA and Client Review | 4 Days | Functional testing and feedback |
| Deployment | 2 Days | Production release and verification |

## 6\. Tickets

| Ticket ID | Type | Title | Estimate | Status |
| :---- | :---- | :---- | ----: | :---- |
| TKT-001 | Design | Create sitemap | 4 Hours | Done |
| TKT-002 | Design | Design responsive home page | 8 Hours | Done |
| TKT-003 | Design | Design service-page template | 5 Hours | Done |
| TKT-004 | Frontend | Develop home page | 10 Hours | Done |
| TKT-005 | Frontend | Develop service pages | 8 Hours | Done |
| TKT-006 | Backend | Develop inquiry API | 6 Hours | Done |
| TKT-007 | Backend | Configure email notifications | 4 Hours | Done |
| TKT-008 | Backend | Create admin inquiry list | 6 Hours | Done |
| TKT-009 | QA | Test responsive layout | 5 Hours | Done |
| TKT-010 | QA | Test form and notifications | 4 Hours | Done |
| TKT-011 | DevOps | Configure domain, SSL, and deployment | 4 Hours | Done |

## 7\. Team Assignments

| Team Member | Role | Assignment |
| :---- | :---- | :---- |
| Sarah Khan | PM | Planning and client coordination |
| Hamza Ali | UI/UX Designer | Website designs |
| Ahmed Raza | Full-Stack Developer | Frontend, backend, and admin panel |
| Maha Noor | QA Engineer | Functional and responsive testing |
| DevOps Agent | DevOps Support | Deployment checks |

## 8\. Progress Reports

### Week 1

- Requirements confirmed  
- Sitemap completed  
- Client provided logo and initial content  
- Home-page design completed  
- Service descriptions pending  
- Overall status: On Track

### Week 2

- Designs approved  
- Frontend 65% complete  
- Inquiry API completed  
- Remaining content received  
- Overall status: On Track

### Week 3

- Development completed  
- Admin content editing completed  
- QA started  
- Three minor responsive issues identified  
- Overall status: On Track

### Week 4

- QA completed  
- Client feedback applied  
- Production deployed  
- SSL and email delivery verified  
- Overall status: Completed

## 9\. Bugs

### BUG-001: Mobile Navigation Overlap

| Field | Value |
| :---- | :---- |
| Severity | Medium |
| Environment | Staging |
| Related Ticket | TKT-004 |
| Status | Closed |

**Expected:** Mobile menu displays above page content.  
**Actual:** Contact button overlaps the open menu.  
**Resolution:** Updated mobile stacking and navigation layout.

### BUG-002: Duplicate Inquiry Email

| Field | Value |
| :---- | :---- |
| Severity | High |
| Environment | Staging |
| Related Ticket | TKT-007 |
| Status | Closed |

**Root Cause:** Email triggered in both API handler and background worker.  
**Resolution:** Removed duplicate trigger and added idempotency.

## 10\. Client Feedback

- “Make the phone number more visible on mobile.”  
  **Outcome:** Accepted as an in-scope usability improvement.  
    
- “Can we add online booking before launch?”  
  **Outcome:** Recorded as a future change request.

## 11\. Final Delivery Details

| Field | Value |
| :---- | :---- |
| Release | v1.0.0 |
| Deployment Date | 2026-02-02 |
| Client Acceptance | Approved |
| Open Critical Bugs | 0 |
| Open High Bugs | 0 |
| Deferred Item | Online booking |
| Documentation | Admin guide and release notes |
| Warranty | 30 Days |
| Final Status | Completed |

## 12\. Expected Agent Decisions

- BD asks about booking rather than assuming it.  
- PM records booking as out of scope.  
- PM creates a design phase.  
- TL assigns the compact scope to a full-stack developer.  
- QA marks duplicate notifications as High.  
- Project cannot close without client acceptance.

---

# Project 2: Medium Web and Mobile Application

## Project Summary

| Field | Value |
| :---- | :---- |
| Project ID | PRJ-SAMPLE-002 |
| Client | WellTrack Clinics |
| Project Type | Web and Mobile Appointment Platform |
| Industry | Wellness Clinic Administration |
| Delivery Model | Milestone Based |
| Duration | 14 Weeks |
| Team Size | 8 |
| Complexity | Medium |
| Final Status | Completed with Deferred Enhancement |

## 1\. Original Client Query

**Source:** Referral email

> We operate three wellness clinics and need a web and mobile system where customers can browse services, book appointments, receive reminders, and manage upcoming bookings. Clinic staff should manage schedules and appointments through an admin portal. We need Android and iOS applications and would prefer to launch within three months.

## 2\. Requirement Conversations

### Conversation 1

**BD Agent:** Should customers pay online or at the clinic?

**Client:** At the clinic initially. Deposits may be added later.

### Conversation 2

**BD Agent:** Can each clinic have different services, prices, staff, and working hours?

**Client:** Yes.

### Conversation 3

**BD Agent:** Can customers reschedule or cancel their own appointments?

**Client:** Yes, but cancellation is blocked within six hours.

### Conversation 4

**BD Agent:** Which reminders are required?

**Client:** Email confirmation immediately and push reminders 24 hours and 2 hours before.

### Conversation 5

**PM Agent:** Should staff see only their own schedules?

**Client:** Staff see their own schedule. Clinic managers see all appointments in their clinic.

### Conversation 6

**TL Agent:** Is an external patient system integration required?

**Client:** No. CSV export is enough for the first release.

### Conversation 7

**QA Agent:** What should happen if two customers confirm the same slot?

**Client:** Only the first confirmed booking should succeed.

## 3\. Final Requirements

### User Roles

| Role | Description |
| :---- | :---- |
| Customer | Browse services and manage own bookings |
| Staff Member | View assigned schedule |
| Clinic Manager | Manage clinic services, staff, and appointments |
| System Administrator | Manage all clinics and reporting |

### Functional Requirements

| Requirement ID | Requirement | Priority |
| :---- | :---- | :---- |
| REQ-101 | Customer registration and login | Must Have |
| REQ-102 | Browse clinics and services | Must Have |
| REQ-103 | Real-time appointment availability | Must Have |
| REQ-104 | Book appointment | Must Have |
| REQ-105 | Reschedule appointment | Must Have |
| REQ-106 | Cancel subject to policy | Must Have |
| REQ-107 | Email confirmation | Must Have |
| REQ-108 | Push reminders | Must Have |
| REQ-109 | Staff schedule management | Must Have |
| REQ-110 | Clinic-specific services and pricing | Must Have |
| REQ-111 | CSV export | Should Have |
| REQ-112 | Appointment history | Should Have |
| REQ-113 | Admin dashboard | Must Have |
| REQ-114 | Appointment audit history | Must Have |
| REQ-115 | Android application | Must Have |
| REQ-116 | iOS application | Must Have |

### Non-Functional Requirements

- Prevent duplicate slot confirmation  
- Support at least 10,000 customers  
- Encrypt sensitive personal information  
- Enforce role and clinic access  
- Support current Android and iOS versions  
- Normal booking API response below two seconds  
- Retry and log notification failures

### Out of Scope

- Online payments  
- Insurance processing  
- Electronic health records  
- Video consultations  
- Medical diagnosis data  
- External patient-system integration

## 4\. SRS Summary

### Booking Workflow

Select Clinic

\-\> Select Service

\-\> Select Staff or Any Available Staff

\-\> View Slots

\-\> Select Slot

\-\> Confirm Booking

\-\> Revalidate Availability

\-\> Create Appointment

\-\> Send Confirmation

\-\> Schedule Reminders

### Cancellation Rule

Appointment Start \- Current Time \>= 6 Hours

\-\> Cancellation Allowed

Appointment Start \- Current Time \< 6 Hours

\-\> Cancellation Rejected

\-\> Contact Clinic Message Displayed

### Double-Booking Acceptance Criteria

Given two customers select the same slot

When both confirm

Then only one appointment is created

And the second request receives a slot-unavailable response

## 5\. Project Phases

| Phase | Duration | Deliverables |
| :---- | ----: | :---- |
| Discovery and SRS | 2 Weeks | Requirements and architecture |
| UI/UX Design | 2 Weeks | Web, admin, Android, and iOS designs |
| Backend and Admin | 4 Weeks | APIs, schedules, bookings, admin |
| Mobile Applications | 4 Weeks | Android and iOS apps |
| QA and UAT | 2 Weeks | Testing and client validation |
| Deployment and Store Submission | 1 Week | Web release and app submissions |

## 6\. Tickets

| Ticket ID | Type | Title | Estimate | Status |
| :---- | :---- | :---- | ----: | :---- |
| TKT-101 | Backend | Authentication and roles | 24 Hours | Done |
| TKT-102 | Backend | Clinic and service management | 32 Hours | Done |
| TKT-103 | Backend | Staff schedule engine | 40 Hours | Done |
| TKT-104 | Backend | Atomic appointment booking | 32 Hours | Done |
| TKT-105 | Backend | Cancellation policy | 12 Hours | Done |
| TKT-106 | Backend | Email notifications | 16 Hours | Done |
| TKT-107 | Backend | Push reminder scheduler | 24 Hours | Done |
| TKT-108 | Frontend | Customer booking flow | 40 Hours | Done |
| TKT-109 | Frontend | Clinic admin portal | 56 Hours | Done |
| TKT-110 | Mobile | Authentication screens | 24 Hours | Done |
| TKT-111 | Mobile | Clinic and service browsing | 32 Hours | Done |
| TKT-112 | Mobile | Appointment booking flow | 48 Hours | Done |
| TKT-113 | Mobile | Booking management | 28 Hours | Done |
| TKT-114 | QA | Booking test suite | 24 Hours | Done |
| TKT-115 | QA | Regression testing | 32 Hours | Done |
| TKT-116 | DevOps | Staging and production | 20 Hours | Done |
| TKT-117 | DevOps | Mobile build pipelines | 24 Hours | Done |

## 7\. Team Assignments

| Team Member | Role | Assignment |
| :---- | :---- | :---- |
| Nadia Abbas | PM | Delivery and client coordination |
| Usman Tariq | TL | Architecture and oversight |
| Alina Shah | UI/UX Designer | Web and mobile design |
| Bilal Ahmed | Backend Developer | APIs and booking engine |
| Saad Hussain | Frontend Developer | Web and admin portal |
| Hira Malik | Mobile Developer | Android and iOS |
| Ayesha Farooq | QA Engineer | Functional, API, and mobile testing |
| Omar Siddiqui | DevOps Engineer | CI/CD and releases |

## 8\. Progress Reports

### Week 2

- SRS internally approved  
- Client cancellation-policy approval pending  
- Architecture completed  
- Design started  
- Apple Developer account missing  
- Status: At Risk

### Week 5

- Authentication and clinic management complete  
- Booking engine 70%  
- Admin portal 45%  
- Mobile designs approved  
- Apple account still pending  
- Escalated to client sponsor  
- Status: At Risk

### Week 8

- Backend complete  
- Web booking complete  
- Mobile 60%  
- Duplicate booking found under concurrency  
- Critical fix assigned  
- Status: At Risk but Recoverable

### Week 11

- Mobile development complete  
- Regression started  
- Android notifications passed  
- iOS notifications intermittent  
- Store credentials received  
- Status: On Track for adjusted release

### Week 14

- Web deployed  
- Android released  
- iOS submitted for review  
- UAT completed  
- Status: Delivered with External Dependency

## 9\. Bugs

### BUG-101: Duplicate Booking Under Concurrency

| Field | Value |
| :---- | :---- |
| Severity | Critical |
| Related Ticket | TKT-104 |
| Status | Closed |

**Root Cause:** Availability checked before insertion without uniqueness protection.  
**Fix:** Added unique constraint and transactional conflict handling.

### BUG-102: iOS Push Reminder Not Delivered

| Field | Value |
| :---- | :---- |
| Severity | High |
| Related Ticket | TKT-107 |
| Status | Closed |

**Root Cause:** Expired APNs token was not refreshed.  
**Fix:** Added token-refresh handling.

### BUG-103: Clinic Manager Could View Another Clinic

| Field | Value |
| :---- | :---- |
| Severity | Critical |
| Status | Closed |

**Root Cause:** Role checked, but assigned clinic was not.  
**Fix:** Added clinic-level authorization and regression tests.

### BUG-104: CSV Export Time Zone Incorrect

| Field | Value |
| :---- | :---- |
| Severity | Medium |
| Status | Closed |

**Fix:** Export now uses the clinic’s configured time zone.

## 10\. Client Feedback and Change Request

- “Allow multiple services in one appointment.”  
  **Outcome:** CR-101 created and deferred to Phase 2\.  
    
- “Display cancellation policy before confirmation.”  
  **Outcome:** Accepted as an in-scope clarification.  
    
- “Allow managers to export phone numbers.”  
  **Outcome:** Approved with permission controls and audit logging.

### CR-101

| Field | Value |
| :---- | :---- |
| Change | Multiple services in one appointment |
| Technical Impact | Booking model and pricing |
| Mobile Impact | Booking flow redesign |
| QA Impact | Combination and duration tests |
| Timeline Impact | 3 Weeks |
| Decision | Deferred |

## 11\. Final Delivery Details

| Field | Value |
| :---- | :---- |
| Web Release | v1.0.0 |
| Android Release | v1.0.0 |
| iOS Release | Submitted and later approved |
| Client UAT | Passed |
| Critical Open Bugs | 0 |
| High Open Bugs | 0 |
| Deferred Changes | 1 |
| Documentation | Admin guide, API guide, release notes |
| Warranty | 60 Days |
| Final Status | Completed |

## 12\. Expected Agent Decisions

- BD asks about payment behavior.  
- PM identifies store accounts as client dependencies.  
- TL identifies double booking as a concurrency risk.  
- QA marks cross-clinic access as Critical.  
- Orchestrator escalates missing Apple credentials.  
- PM creates a formal change request for multiple services.  
- Security prevents cross-clinic access.

---

# Project 3: Complex Multi-Team Enterprise Platform

## Project Summary

| Field | Value |
| :---- | :---- |
| Project ID | PRJ-SAMPLE-003 |
| Client | GreenCore Field Operations |
| Project Type | Enterprise CRM and Field Operations Platform |
| Industry | Commercial Maintenance and Field Services |
| Delivery Model | Multi-Phase Time and Materials |
| Duration | 11 Months |
| Team Size | 17 |
| Complexity | High |
| Final Status | Phases 1 and 2 Completed; Phase 3 Active |

## 1\. Original Client Query

**Source:** Enterprise referral

> We currently use spreadsheets, email, and disconnected applications to manage sales opportunities, maintenance estimates, field teams, work orders, customer communication, invoices, and management reporting. We need one web and mobile platform for sales, operations, field staff, management, and customers. We also require accounting integration and automated reporting.

## 2\. Requirement Conversations

### Business Objective

**BD Agent:** What problem must the first release solve?

**Client:** Sales and operations use different information. We need one customer, project, and opportunity record.

### CRM Pipeline

**PM Agent:** Which sales stages are required?

**Client:** Prospect, Lead, RFP, Proposal, Verbal Approval, Closed Won, and Client.

### Maintenance Estimator

**TL Agent:** Can estimators override product prices?

**Client:** Authorized estimators can override with a required reason.

### Mobile Operations

**PM Agent:** Which modules are required on mobile?

**Client:** Maintenance estimates, site reports, time tracking, work orders, photos, and BD Scoreboard.

### Accounting

**TL Agent:** Which accounting platform is required?

**Client:** QuickBooks Online for customers, estimates, invoices, purchase orders, bills, vendors, and products.

### Time Tracking

**QA Agent:** How should field time be captured?

**Client:** Foreman selects the crew. Employees use geolocation, including yard time and drive time.

### Access

**Security Reviewer:** Can all managers see all branches?

**Client:** Regional managers see their region, branch managers see their branch, and field teams see assigned work only.

### Scope Change

**Client:** We need a button to move eligible opportunities from Proposal back to RFP for the new annual cycle.

**PM:** This is not in the approved phase and requires impact analysis.

## 3\. Final Requirements

### Main Modules

| Module | Description |
| :---- | :---- |
| CRM | Companies, contacts, opportunities, activities, notes, emails, pipeline |
| Customer Management | Prospect-to-customer conversion |
| Maintenance Estimator | Product estimates and authorized overrides |
| BD Scoreboard | Weekly entry, monthly grid, targets, spend, dashboard |
| Field Operations | Work orders, site reports, photos, punch lists |
| Time Tracking | Crew, geolocation, yard and drive time |
| Accounting Integration | QuickBooks synchronization |
| Mobile Applications | Android and iOS modules |
| Reporting | Revenue, lead volume, health, productivity |
| Settings | Custom fields, roles, permissions, pipeline stages |

### User Roles

| Role | Access |
| :---- | :---- |
| System Administrator | Full configuration |
| Executive | Company-wide reporting |
| Regional Manager | Assigned region |
| Branch Manager | Assigned branch |
| Business Developer | CRM and scoreboard |
| Estimator | Maintenance estimator |
| Project Manager | Projects and field operations |
| Foreman | Crew and work execution |
| Field Employee | Assigned work and time |
| Accounting User | Financial synchronization |
| Client Portal User | Approved client-facing information |

### Major Functional Requirements

| Requirement ID | Requirement |
| :---- | :---- |
| REQ-201 | Manage companies, contacts, and opportunities |
| REQ-202 | Configurable pipeline stages |
| REQ-203 | Opportunity stage history |
| REQ-204 | Product-based maintenance estimates |
| REQ-205 | Authorized price override with reason |
| REQ-206 | Annual, monthly, and weekly sales targets |
| REQ-207 | Lead volume and proposed revenue |
| REQ-208 | Up to six client follow-ups |
| REQ-209 | Field work orders |
| REQ-210 | Site reports and photos |
| REQ-211 | Crew time with geolocation |
| REQ-212 | Yard and drive time |
| REQ-213 | QuickBooks customer sync |
| REQ-214 | Estimate and invoice sync |
| REQ-215 | Purchase order and bill sync |
| REQ-216 | Android and iOS applications |
| REQ-217 | Region, branch, project, and role access |
| REQ-218 | Complete audit logging |
| REQ-219 | Configurable custom fields |
| REQ-220 | Client-facing reports |

### Non-Functional Requirements

- Tenant, region, and branch isolation  
- Project- and role-level access  
- Complete audit trail  
- Offline-tolerant mobile capture  
- Secure photo uploads  
- Retry and idempotency for integrations  
- At least 500 internal users  
- 99.9% availability target  
- Critical APIs below three seconds under expected load  
- Point-in-time recovery  
- Data export and retention controls

## 4\. SRS Summary

### Pipeline

Prospect

\-\> Lead

\-\> RFP

\-\> Proposal

\-\> Verbal Approval

\-\> Closed Won

\-\> Client

### Price Override Rule

User Has Override Permission

AND Override Reason Is Provided

\-\> Override Allowed

\-\> Original and New Price Stored

\-\> User and Timestamp Audited

Otherwise

\-\> Override Rejected

### Geolocation Time Tracking

Foreman Selects Crew

\-\> Validate Assigned Project

\-\> Employees Enter Geofence

\-\> Create Clock-In

\-\> Store Location and Timestamp

\-\> Record Work, Yard, or Drive Category

\-\> Create Clock-Out

\-\> Update Variance Report

### QuickBooks Sync

Internal Record Changed

\-\> Queue Sync Event

\-\> Check Mapping

\-\> Send API Request

\-\> Log Response

\-\> Store External ID

\-\> Retry Temporary Failure

\-\> Escalate Permanent Failure

### Access Acceptance Criterion

Given a Branch Manager belongs to Branch A

When requesting Branch B records

Then access is denied

And the attempt is audited

## 5\. Project Phases

| Phase | Duration | Deliverables |
| :---- | ----: | :---- |
| Discovery and Architecture | 5 Weeks | SRS, architecture, migration plan |
| CRM and Core Settings | 12 Weeks | Companies, contacts, pipeline, roles |
| Estimator and BD Scoreboard | 14 Weeks | Estimator, entries, goals, dashboard |
| Field Operations and Time Tracking | 16 Weeks | Work orders, reports, geolocation |
| Mobile Applications | 18 Weeks, overlapping | Android and iOS modules |
| Accounting Integration | 10 Weeks, overlapping | QuickBooks sync |
| Reporting, UAT, and Rollout | 8 Weeks | Reports and phased rollout |

## 6\. Sample Tickets

| Ticket ID | Team | Title | Estimate | Status |
| :---- | :---- | :---- | ----: | :---- |
| TKT-201 | Backend | Organization and branch access model | 40 Hours | Done |
| TKT-202 | Backend | Company and contact APIs | 48 Hours | Done |
| TKT-203 | Frontend | CRM pipeline board | 56 Hours | Done |
| TKT-204 | Backend | Pipeline-stage history | 32 Hours | Done |
| TKT-205 | Frontend | Opportunity timeline | 40 Hours | Done |
| TKT-206 | Backend | Product and price management | 40 Hours | Done |
| TKT-207 | Frontend | Maintenance estimator | 64 Hours | Done |
| TKT-208 | Backend | Price override auditing | 20 Hours | Done |
| TKT-209 | Backend | Goal engine | 48 Hours | Done |
| TKT-210 | Frontend | BD Scoreboard dashboard | 56 Hours | Done |
| TKT-211 | Mobile | Mobile maintenance estimator | 72 Hours | In Progress |
| TKT-212 | Mobile | Mobile BD Scoreboard | 72 Hours | In Progress |
| TKT-213 | Backend | QuickBooks customer sync | 40 Hours | Done |
| TKT-214 | Backend | Invoice synchronization | 56 Hours | In Progress |
| TKT-215 | QA | CRM regression suite | 40 Hours | Done |
| TKT-216 | QA | Estimator pricing test suite | 32 Hours | Done |
| TKT-217 | DevOps | Production deployment pipeline | 32 Hours | Done |
| TKT-218 | DevOps | Monitoring and alerts | 24 Hours | Done |
| TKT-219 | Security | Audit-event service | 40 Hours | Done |
| TKT-220 | Data | Legacy migration scripts | 64 Hours | In Progress |

## 7\. Team Assignments

| Team | Members | Responsibilities |
| :---- | :---- | :---- |
| PMO | 2 PMs and PM Agent | Planning, risk, reporting |
| Architecture | Architect and TL Agent | Architecture and standards |
| Backend | 4 Developers and Backend Agents | APIs and integrations |
| Frontend | 3 Developers and Frontend Agents | Web modules |
| Mobile | 2 Developers and Mobile Agent | Android and iOS |
| Design | 2 Designers and Designer Agent | UX and UI |
| QA | 3 QA Engineers and QA Agent | Functional and regression |
| DevOps | 1 Engineer and DevOps Agent | Cloud and releases |
| Data | 1 Data Engineer | Migration |
| Security | Shared Security Lead | Access and audit review |

## 8\. Progress Reports

### Month 1

- Discovery workshops completed  
- SRS 70%  
- Data quality identified as a major risk  
- Branch and region permissions not finalized  
- Status: At Risk

### Month 3

- CRM backend 80%  
- Company and contact UI complete  
- Pipeline approved after two revisions  
- Migration scripts started  
- Pipeline-stage approval delayed  
- Escalated to client sponsor  
- Status: At Risk

### Month 5

- Phase 1 on staging  
- Cross-branch visibility defect found  
- Audit service added to release gate  
- Phase 2 started  
- Status: Recovering

### Month 7

- Estimator complete  
- Scoreboard backend complete  
- Mobile started  
- QuickBooks customer sync passed sandbox  
- Annual pipeline reset change submitted  
- Status: On Track with Pending Change

### Month 9

- Phase 2 deployed  
- Mobile estimator 65%  
- Invoice sync delayed by tax configuration  
- Time-tracking design approved  
- Status: At Risk for Accounting Integration

### Month 11

- CRM and estimator stable  
- Scoreboard accepted  
- Mobile in UAT  
- Time tracking in development  
- Three QuickBooks exceptions open  
- Status: Multi-Phase Active

## 9\. Bugs

### BUG-201: Cross-Branch Contact Visibility

| Field | Value |
| :---- | :---- |
| Severity | Critical |
| Status | Closed |
| Related Ticket | TKT-202 |

**Root Cause:** Organization filtering existed, branch filtering did not.  
**Resolution:** Added branch authorization and row-level security tests.

### BUG-202: Estimator Total Not Updated After Override

| Field | Value |
| :---- | :---- |
| Severity | High |
| Status | Closed |

**Resolution:** Updated reactive calculation and server-side validation.

### BUG-203: Duplicate QuickBooks Customer

| Field | Value |
| :---- | :---- |
| Severity | High |
| Status | Closed |

**Root Cause:** Retry lost the idempotency key.  
**Resolution:** Stored outbound event IDs and checked mappings before retry.

### BUG-204: Mobile Photo Upload Fails on Weak Network

| Field | Value |
| :---- | :---- |
| Severity | High |
| Status | In Progress |

**Plan:** Add resumable upload and local retry queue.

### BUG-205: Dashboard Used Calendar Year

| Field | Value |
| :---- | :---- |
| Severity | Medium |
| Status | Closed |

**Resolution:** Added configurable fiscal-year start month.

## 10\. Client Feedback and Change Requests

### CR-201: Annual Pipeline Reset

| Field | Value |
| :---- | :---- |
| Status | Approved |
| Technical Impact | Bulk workflow and eligibility rules |
| Security Impact | Sales-manager permission required |
| Audit Requirement | Record each opportunity changed |
| Timeline Impact | 2 Weeks |
| Cost Impact | Additional budget approved |
| Release | v2.2 |

### CR-202: Percentage-Based Price Overrides

| Field | Value |
| :---- | :---- |
| Status | Approved |
| Rule | Branch managers 10%; regional managers 25% |
| Technical Impact | Role thresholds and validation |
| QA Impact | Boundary and permission testing |
| Timeline Impact | 1 Week |
| Release | v2.1 |

### CR-203: Client Portal Invoice PDFs

| Field | Value |
| :---- | :---- |
| Status | Deferred |
| Reason | Outside current phase |
| Future Phase | Client Portal Enhancement |

## 11\. Deployment and Delivery Details

### Phase 1

| Field | Value |
| :---- | :---- |
| Version | v1.0 |
| Modules | CRM, companies, contacts, pipeline, activities |
| QA Approval | Approved |
| Client Approval | Approved |
| Rollback | Not Required |

### Phase 2

| Field | Value |
| :---- | :---- |
| Version | v2.0 |
| Modules | Maintenance Estimator and BD Scoreboard |
| QA Approval | Approved |
| Client Approval | Approved |
| Post-Release Fix | v2.0.1 estimator correction |

### Phase Status

| Phase | Status | Acceptance |
| :---- | :---- | :---- |
| CRM | Completed | Client Accepted |
| Estimator and Scoreboard | Completed | Client Accepted |
| Field Operations | Active | Pending |
| Mobile | UAT | Pending |
| QuickBooks | In Progress | Pending |
| Reporting and Rollout | Planned | Pending |

## 12\. Expected Agent Decisions

- BD identifies the request as multi-phase.  
- PM separates CRM, estimator, mobile, field operations, and accounting.  
- TL assigns QuickBooks work to integration-capable developers.  
- QA marks cross-branch access as Critical.  
- Orchestrator escalates delayed client approvals.  
- CR-201 cannot start without approval.  
- PM distinguishes defects from new scope.  
- System maintains requirement-to-ticket-to-test-to-release traceability.  
- Completed phases remain closed while later phases continue.  
- QuickBooks retries remain idempotent.  
- Deferred portal work is not silently added.

---

# Cross-Project Test Matrix

| Test Area | Small | Medium | Complex |
| :---- | ----: | ----: | ----: |
| Requirement gathering | Yes | Yes | Yes |
| Multiple roles | Limited | Yes | Extensive |
| Mobile | No | Yes | Yes |
| External integration | Email | Push services | QuickBooks |
| Complex permissions | No | Clinic-level | Region and branch |
| Change requests | Future booking | Multiple services | Multiple changes |
| Concurrency defect | No | Yes | Yes |
| Multi-team delivery | Limited | Moderate | Extensive |
| Multi-phase delivery | Basic | Yes | Extensive |
| Client approval dependency | Yes | Yes | Yes |

# Recommended Evaluation Criteria

## BD Agent

- Asks missing questions  
- Avoids pricing and timeline commitments  
- Identifies scope boundaries  
- Produces a complete requirement brief  
- Detects new change requests

## PM Agent

- Creates realistic phases  
- Identifies dependencies and risks  
- Generates approval requests  
- Maintains baseline requirements  
- Distinguishes project and phase completion

## TL Agent

- Selects correct technical roles  
- Identifies concurrency, authorization, and integration risks  
- Creates technical tickets  
- Escalates scope questions

## QA Agent

- Generates positive, negative, boundary, security, and concurrency tests  
- Assigns correct severity  
- Links bugs to requirements and tickets  
- Prevents release with critical defects

## DevOps Agent

- Requires QA and release approval  
- Validates backup and rollback  
- Maintains environment separation  
- Records deployment evidence  
- Escalates failures

## Orchestrator Agent

- Tracks every handoff  
- Creates reminders  
- Escalates overdue responses  
- Prevents duplicate ownership  
- Preserves linked follow-ups  
- Stops workflows at approval gates

# Data Validation Rules

Every imported sample project must have:

- Unique IDs  
- Valid status transitions  
- Assigned human and agent owners  
- Complete timestamps  
- Linked approvals  
- Requirement traceability  
- Project-level access rules  
- Document versions  
- Audit history  
- No real credentials or personal data

# Suggested Import Order

Organizations

\-\> Human Users

\-\> Agents

\-\> Teams

\-\> Clients

\-\> Contacts

\-\> Queries

\-\> Opportunities

\-\> Projects

\-\> Requirements

\-\> Requirement Versions

\-\> Phases

\-\> Milestones

\-\> Tickets

\-\> Assignments

\-\> Follow-Ups

\-\> Messages

\-\> Approvals

\-\> Test Cases

\-\> Bugs

\-\> Change Requests

\-\> Risks

\-\> Releases

\-\> Deployments

\-\> Audit Logs

# Sample Data Acceptance Criteria

- All three projects import without validation errors.  
- Every requirement has a current version.  
- Every ticket belongs to a valid project and phase.  
- Every bug links to a valid project and relevant ticket where applicable.  
- Change requests contain impact and approval status.  
- Completed projects cannot close without approval.  
- Complex project phases can have independent statuses.  
- Cross-client and cross-branch access tests fail safely.  
- Agent output can be compared against the expected decisions in this document.

