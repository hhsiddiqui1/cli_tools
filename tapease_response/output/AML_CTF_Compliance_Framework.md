# AML/CTF Compliance Framework
## A2 Square Pty Ltd (trading as Tapease)

**Document Version:** 1.0
**Last Updated:** November 2025
**Review Frequency:** Annual (or as required by regulation)
**Next Review Due:** November 2026

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Regulatory Framework](#regulatory-framework)
3. [Business Risk Assessment](#business-risk-assessment)
4. [Customer Due Diligence (CDD)](#customer-due-diligence-cdd)
5. [Ongoing Monitoring](#ongoing-monitoring)
6. [Suspicious Matter Reporting](#suspicious-matter-reporting)
7. [Record Keeping](#record-keeping)
8. [Employee Training](#employee-training)
9. [Governance & Oversight](#governance--oversight)
10. [Appendices](#appendices)

---

## Executive Summary

**A2 Square Pty Ltd (Tapease)** operates as an Independent Selling Organization (ISO) providing payment terminal services to taxi operators in Sydney, Australia. As part of our commitment to preventing money laundering and terrorism financing, we have implemented this comprehensive AML/CTF compliance framework.

### Our AML/CTF Obligations

As a business that:
- Provides designated services (facilitating payment transactions)
- Handles cash disbursements
- Maintains customer relationships with merchants

We are subject to the obligations under the **Anti-Money Laundering and Counter-Terrorism Financing Act 2006** (AML/CTF Act) and associated rules.

### Key Elements of Our Program

✓ Customer identification and verification (KYC)
✓ Ongoing customer due diligence
✓ Transaction monitoring and reporting
✓ Risk-based approach to compliance
✓ Employee training and awareness
✓ Regular program review and updates

---

## Regulatory Framework

### Applicable Legislation

1. **Anti-Money Laundering and Counter-Terrorism Financing Act 2006** (AML/CTF Act)
2. **Anti-Money Laundering and Counter-Terrorism Financing Rules Instrument 2007 (No. 1)**
3. **Privacy Act 1988**
4. **Australian Business Number Act 1999**

### Regulator

**AUSTRAC (Australian Transaction Reports and Analysis Centre)**
- Website: www.austrac.gov.au
- Reporting Portal: online.austrac.gov.au

### Our Reporting Entity Details

**Entity Name:** A2 Square Pty Ltd
**Trading Name:** Tapease
**ABN:** [TO BE COMPLETED]
**AUSTRAC Registration:** [TO BE COMPLETED - if applicable]
**Business Type:** Independent Selling Organization (ISO) for payment terminals

---

## Business Risk Assessment

### Our Business Model

**What We Do:**
- Deploy payment terminals (Clover devices) to taxi drivers
- Facilitate merchant onboarding and identity verification
- Receive bulk settlements from Fiserv (payment processor)
- Calculate and disburse merchant payouts via EFT, PayID, or cash

**What We DON'T Do:**
- Process card transactions (handled by Fiserv)
- Store or access cardholder data
- Provide banking services

### ML/TF Risk Assessment

#### Inherent Risks

**HIGH RISK FACTORS:**
1. **Cash Handling:** Some merchants prefer cash payouts (legacy practice being phased out)
2. **Customer Base:** Independent taxi drivers (sole traders) with varying levels of financial sophistication
3. **Cash Business:** Taxi industry has historically been cash-intensive

**MEDIUM RISK FACTORS:**
1. **Transaction Monitoring:** Reliance on Fiserv for initial transaction processing
2. **Geographic Concentration:** Sydney-based operations

**LOW RISK FACTORS:**
1. **Customer Type:** Legitimate taxi drivers with verified licenses and ABNs
2. **Transaction Type:** Small-value retail payments (taxi fares)
3. **Regulatory Environment:** Highly regulated taxi industry in NSW
4. **Card Transactions:** Primary payment method is card (not cash)

#### Mitigating Controls

**Controls Implemented:**
1. **Robust KYC:** Driver license verification, ABN verification, bank account verification
2. **Transaction Monitoring:** Automated alerts for unusual patterns
3. **Cash Reduction:** Active program to transition to electronic payments only
4. **Audit Trail:** Complete digital record of all transactions and payouts
5. **Regulatory Compliance:** Licensed taxi operators subject to NSW transport regulations

#### Overall Risk Rating

**MEDIUM RISK** (after considering controls)

**Rationale:**
- While cash handling and customer type present risks, our strong KYC procedures, transaction monitoring, and transition away from cash significantly mitigate these risks
- Merchant base consists of licensed, regulated taxi operators (not anonymous)
- Transaction patterns are predictable and consistent with legitimate taxi operations

---

## Customer Due Diligence (CDD)

### Identification and Verification Requirements

All merchants (taxi drivers) must complete our KYC process before terminal deployment.

#### 1. Individual Identification

**Required Documents:**

**A. Driver's License (Primary ID)**
- Front and back images uploaded to system
- Verified information:
  - Full legal name
  - License number
  - Date of birth
  - License state
  - License expiry date
  - Photo verification

**System Implementation:** `/auth/upload-documents` API endpoint captures and stores documents securely

#### 2. Business Verification

**Australian Business Number (ABN)**
- ABN provided during signup
- Verified via ABR (Australian Business Register) lookup
- Confirmed details:
  - Business name
  - Entity type (Sole Trader, Company, Partnership)
  - ABN status (Active)
  - Registration date

**System Implementation:** ABN stored in `auth_users` table, verified during onboarding

#### 3. Financial Details Verification

**Bank Account Details (for EFT payouts):**
- Account name
- BSB number
- Account number
- Bank name

**Verification:** Initial test payment of $0.01 sent to verify account is active and correctly specified

**PayID Details (for PayID payouts):**
- PayID (email address or mobile number)
- PayID holder name

**Verification:** PayID lookup performed before first payment

**System Implementation:** Payment details stored securely in `auth_users` table (columns: `account_name`, `account_bsb`, `account_no`, `pay_id`, `pay_id_holder_name`)

#### 4. Contact Information

**Required:**
- Email address (verified via email verification link)
- Mobile phone number
- Residential address

**System Implementation:** Email verification via `/auth/verify-email` endpoint

#### 5. Beneficial Ownership

For sole traders (majority of our merchants):
- The driver is the beneficial owner
- License verification establishes identity

For companies:
- Company ABN and structure verified via ABR
- Directors and beneficial owners (>25% ownership) identified
- Company documents requested if needed

### Enhanced Due Diligence (EDD)

**Triggers for Enhanced Due Diligence:**

1. **High-Risk Merchants:**
   - Prefer cash payments
   - Irregular transaction patterns
   - Multiple declined transactions
   - Expired or expiring licenses
   - ABN issues (suspended, cancelled)

2. **EDD Measures:**
   - Additional identity verification (secondary ID)
   - Verification of source of wealth
   - More frequent transaction monitoring
   - Senior management approval required
   - Mandatory electronic payment (no cash option)

3. **Politically Exposed Persons (PEPs):**
   - Screening against PEP databases
   - Enhanced ongoing monitoring
   - Senior management approval

### Simplified Due Diligence

**Not Applicable** - Given our risk profile and the nature of our merchant relationships, we do not apply simplified due diligence.

### Timing of Verification

**Standard Approach:** Verification BEFORE terminal deployment

- All documents uploaded and verified during signup
- Account reviewed and approved by operations team
- Terminal deployed only after full verification

**Exception:** No terminals are deployed without complete identity verification.

---

## Ongoing Monitoring

### Transaction Monitoring

#### Automated Monitoring Systems

**Daily Transaction Analysis:**

1. **Volume Anomalies:**
   - Sudden increase in transaction volume (>200% of average)
   - Unusual spike in transaction values
   - Alert threshold: 3x standard deviation from merchant's norm

2. **Pattern Changes:**
   - Significant change in transaction times (e.g., normally daytime, suddenly nighttime)
   - Geographic pattern changes (if GPS data available)
   - Change in average transaction size

3. **Declined Transactions:**
   - High rate of declined transactions (>10% of attempts)
   - Multiple high-value declined transactions
   - Could indicate card testing or fraudulent activity

4. **Structuring Indicators:**
   - Multiple transactions just below reporting thresholds
   - Unusual transaction splitting patterns

**System Implementation:**
- Transaction data retrieved via `/transactions/search_transactions_by_user` API
- Automated daily analysis via scheduled jobs
- Alerts generated and logged in `audit_logs` table

#### Manual Review Procedures

**Weekly Reviews:**
- Review all automated alerts from past week
- Categorize alerts: False positive, Requires investigation, Report to AUSTRAC
- Document review outcomes in compliance log

**Monthly Reviews:**
- Top 10 highest-volume merchants reviewed
- Any merchants with cash payment preference reviewed
- Merchant status verification (licenses, ABNs)

#### Red Flags for Suspicious Activity

1. **Transaction Red Flags:**
   - Transactions inconsistent with merchant's expected profile
   - Sudden unexplained changes in transaction patterns
   - Attempts to process large numbers of small transactions
   - Transactions at unusual times or locations

2. **Merchant Behavior Red Flags:**
   - Reluctance to provide identification documents
   - Providing false or misleading information
   - Unusual interest in AML/CTF policies
   - Requesting frequent changes to payout methods
   - Multiple accounts or terminals under different names

3. **Cash-Related Red Flags:**
   - Insistence on cash payments despite electronic options
   - Large cash payout requests
   - Structuring cash withdrawals to avoid reporting thresholds
   - Inconsistency between transaction volume and cash requests

### Periodic Reviews

**Quarterly Merchant Review:**
- Verify merchant is still actively trading
- Check license expiry dates (alert if <90 days to expiry)
- Review transaction patterns for anomalies
- Update risk rating if needed

**Annual Merchant Re-verification:**
- Request updated identity documents if license renewed
- Re-verify ABN status
- Re-verify bank account/PayID details
- Update merchant profile information
- Re-assess merchant risk rating

**System Implementation:**
- Automated reminders for quarterly and annual reviews
- Review status tracked in database
- Compliance dashboard showing overdue reviews

---

## Suspicious Matter Reporting

### When to Report

**Suspicious Matter Reports (SMRs)** must be submitted to AUSTRAC when we have reasonable grounds to suspect that a transaction or activity:

1. Involves proceeds of crime
2. Is related to terrorism financing
3. Is related to money laundering
4. Breaches financial sanctions laws

**Key Principle:** "Reasonable grounds to suspect" means more than speculation but less than proof. If in doubt, report.

### SMR Process

#### Step 1: Initial Detection
- Automated alert triggered, OR
- Staff member identifies suspicious activity

#### Step 2: Preliminary Assessment
- Compliance Officer reviews alert/report
- Gathers additional information from internal systems
- Documents initial assessment

#### Step 3: Investigation
- Review merchant transaction history
- Review merchant onboarding documents
- Check for related accounts or patterns
- Interview staff if necessary
- Document all findings

#### Step 4: Decision
- Compliance Officer determines if SMR required
- If yes: Proceed to Step 5
- If no: Document rationale and close investigation

#### Step 5: SMR Submission
- Complete SMR form via AUSTRAC Online portal
- Include all relevant details:
  - Merchant details
  - Transaction details
  - Reasons for suspicion
  - Supporting evidence
- Submit within required timeframe (depends on urgency)

#### Step 6: Follow-up
- Do NOT disclose to merchant that SMR filed (tipping off offence)
- Continue monitoring merchant
- Provide additional information to AUSTRAC if requested
- Consider account restriction or termination if risk too high

### Threshold Transaction Reports (TTRs)

**Reporting Requirement:** Report physical currency transactions ≥ $10,000 AUD to AUSTRAC within 10 business days

**Our Context:**
- Rare given our typical payout amounts
- Most payouts are electronic
- Cash payouts being phased out

**Process:**
1. Cash payout ≥ $10,000 requires senior management pre-approval
2. Transaction logged with all details:
   - Merchant details
   - Amount
   - Date and time
   - Purpose
   - Receiving person details
3. TTR submitted to AUSTRAC within 10 business days
4. Record retained for 7 years

### Terrorism Financing Reporting

**Immediate Reporting Required** if we become aware that:
- A transaction involves funds owned or controlled by a designated terrorist entity
- Funds are being transferred to/from a designated terrorist entity

**Process:**
- Immediate suspension of transaction
- Immediate report to AUSTRAC (within 24 hours)
- Immediate report to AFP (Australian Federal Police)
- Do not complete transaction
- Do not notify merchant (tipping off)

### Record Keeping

**All Suspicious Matter Investigations:**
- Document created for each alert/investigation
- Includes: Alert details, investigation steps, evidence reviewed, decision, outcome
- Retained for 7 years
- Stored securely with restricted access

---

## Record Keeping

### Retention Requirements

As per AML/CTF Act requirements, we retain all records for **7 years** from the date of transaction or account closure.

### Records Maintained

#### 1. Customer Identification Records

**Stored for each merchant:**
- Driver's license (front and back images)
- ABN verification documents
- Bank account/PayID details
- Contact information
- Email and phone verification records
- Beneficial ownership information

**Location:** Secure server storage with encrypted backups
**Access:** Restricted to authorized compliance and operations personnel
**System:** File paths stored in database (`auth_users` table: `license_front_file_location`, `license_back_file_location`, `abn_file_location`)

#### 2. Transaction Records

**Stored for each transaction:**
- Transaction ID
- Merchant ID and terminal ID
- Date, time, and location
- Transaction amount (gross, net, fees)
- Payment method
- Transaction status (approved/declined)
- Authorization codes

**Location:** Database (`trans_transactions` table)
**Access:** Restricted with audit logging
**Retention:** 7 years from transaction date
**System API:** `/transactions/search_transactions_by_user`

#### 3. Payout Records

**Stored for each payout:**
- Payout ID
- Merchant ID
- Payout amount
- Payment method (EFT, PayID, Cash)
- Bank details or PayID used
- Payout date and time
- Status (pending, completed, failed)
- Receipt/confirmation number
- For cash: Signed receipt from merchant

**Location:** Database (`trans_payout` table)
**Access:** Restricted with audit logging
**Retention:** 7 years from payout date
**System API:** `/payout/search_user_payouts`

#### 4. Audit Logs

**Comprehensive audit trail of all system activities:**
- User logins and logouts (session logs)
- Database record changes (create, update, delete)
- API access logs
- Document uploads and access
- System configuration changes
- Compliance review activities

**Location:** Database (`audit_logs`, `session_logs` tables)
**Access:** Compliance Officer and senior management only
**Retention:** 7 years
**System APIs:**
- `/admin/get_all_auditlogs` - Retrieve audit logs
- `/admin/get_session_logs` - Session tracking
- `/admin/get_auditlog_details` - Detailed audit information

#### 5. AML/CTF Compliance Records

**Maintained records:**
- SMR investigation files
- SMR submission records
- TTR submission records (if any)
- Risk assessment documentation
- Compliance review reports
- Training records
- Policy and procedure updates
- Independent review reports (when conducted)

**Location:** Secure compliance folder with restricted access
**Retention:** 7 years from creation

#### 6. Correspondence Records

**Retained communications:**
- Merchant onboarding communications
- Compliance inquiries and responses
- AUSTRAC correspondence
- Regulator communications
- Bank (ANZ) correspondence re: compliance

**Location:** Secure email archives and document management system
**Retention:** 7 years

### Data Security

**Security Measures:**
- Encrypted storage (at rest and in transit)
- Role-based access control
- Multi-factor authentication for admin access
- Regular security audits
- Secure backup and disaster recovery
- Incident response procedures

**Privacy Compliance:**
- Personal information handled in accordance with Privacy Act 1988
- Privacy policy published on website
- Data subject access requests handled appropriately
- Data breach notification procedures in place

---

## Employee Training

### AML/CTF Training Program

#### Initial Training

**All new employees** receive AML/CTF training within **first week** of employment:

**Training Modules:**
1. **Introduction to AML/CTF**
   - What is money laundering?
   - What is terrorism financing?
   - Why it matters
   - Legal consequences of non-compliance

2. **Regulatory Framework**
   - AML/CTF Act overview
   - AUSTRAC role and responsibilities
   - Our obligations as a reporting entity

3. **Our AML/CTF Program**
   - Our business model and risks
   - Customer due diligence procedures
   - Transaction monitoring
   - Reporting obligations

4. **Red Flags and Suspicious Activity**
   - How to identify suspicious activity
   - Examples relevant to our business
   - What to do if you suspect something

5. **Policies and Procedures**
   - KYC procedures
   - Document verification
   - Escalation procedures
   - Record keeping requirements

6. **Legal Obligations**
   - Tipping off offence (do not alert customers)
   - Protection for reporting
   - Confidentiality requirements

**Training Method:**
- In-person or video training session
- Written materials provided
- Comprehension quiz (must pass with 80%+)
- Training completion recorded

#### Annual Refresher Training

**All employees** complete refresher training **annually**:

**Content:**
- Review of key AML/CTF concepts
- Updates to legislation or regulations
- Case studies of money laundering/terrorism financing
- Review of internal procedures and any changes
- Red flag scenarios and discussion
- Q&A session

**Duration:** Minimum 2 hours
**Method:** In-person or online module
**Assessment:** Quiz or scenario-based assessment
**Record:** Training completion logged

#### Role-Specific Training

**Operations Staff** (who interact with merchants):
- Advanced red flag identification
- Customer interview techniques
- Document verification best practices
- Escalation procedures

**Compliance Officer:**
- Advanced AML/CTF training
- AUSTRAC reporting procedures
- Investigation techniques
- Regulatory update monitoring

**Senior Management:**
- AML/CTF risk governance
- Regulatory obligations and penalties
- Strategic compliance planning

#### Training Records

**Maintained for each employee:**
- Date of initial training
- Training modules completed
- Assessment results
- Date of annual refresher training
- Training materials received
- Acknowledgment of understanding

**Retention:** Duration of employment + 7 years

### Training Materials

**Sources:**
- AUSTRAC resources and guidance
- Industry best practices
- Internal policies and procedures
- Case studies from public sources
- Legal updates from compliance consultants

---

## Governance & Oversight

### Compliance Officer

**Designated AML/CTF Compliance Officer:**
- **Name:** [TO BE SPECIFIED]
- **Title:** [TO BE SPECIFIED]
- **Email:** [TO BE SPECIFIED]
- **Phone:** [TO BE SPECIFIED]

**Responsibilities:**
1. Oversee implementation and maintenance of AML/CTF program
2. Ensure compliance with AML/CTF obligations
3. Conduct/oversee transaction monitoring and investigations
4. Prepare and submit reports to AUSTRAC (SMRs, TTRs)
5. Coordinate employee training
6. Liaise with AUSTRAC and other regulators
7. Conduct annual AML/CTF program review
8. Report to senior management and board on compliance status
9. Maintain up-to-date knowledge of regulatory changes
10. Manage record keeping and documentation

**Authority:**
- Direct access to senior management and board
- Authority to suspend merchants or transactions if risk identified
- Authority to engage external experts if needed
- Budget for compliance tools and resources

**Qualifications:**
- Understanding of AML/CTF legislation
- Compliance or risk management experience
- Attention to detail and analytical skills
- Understanding of payment systems

### Senior Management Oversight

**Board/Senior Management Responsibilities:**
1. Approve AML/CTF program and any material changes
2. Allocate adequate resources for compliance
3. Receive regular compliance reports (at least quarterly)
4. Ensure compliance culture throughout organization
5. Approve high-risk merchant relationships
6. Review and approve annual compliance report

**Reporting Frequency:**
- **Monthly:** Brief status update (metrics, alerts, any issues)
- **Quarterly:** Detailed compliance report
- **Annually:** Comprehensive program review and approval

### Internal Audit

**Annual Internal Audit:**
- Review sample of merchant onboarding files for completeness
- Test transaction monitoring system effectiveness
- Review SMR investigation files
- Verify training records are current
- Test record keeping and retention
- Review compliance officer's activities and documentation

**Audit Report:**
- Findings and recommendations
- Management response
- Action plan with timelines
- Follow-up on prior recommendations

### Independent Review

**Every 2 Years (or as required by regulation):**
- Engage external AML/CTF specialist
- Comprehensive review of:
  - Program design and effectiveness
  - Compliance with regulations
  - Adequacy of resources and systems
  - Training effectiveness
  - Record keeping practices
  - Remediation of any identified issues

**Next Independent Review Due:** [TO BE SPECIFIED]

### Program Review and Updates

**Annual Program Review:**
- Review business risk assessment
- Review policies and procedures for accuracy
- Update for regulatory changes
- Incorporate lessons learned
- Update training materials
- Board approval of updated program

**Ad-Hoc Updates:**
- When regulations change
- When business model changes
- After significant incidents
- Based on audit findings
- Based on AUSTRAC guidance updates

### Performance Metrics

**Key Compliance Metrics Tracked:**

1. **Onboarding Metrics:**
   - % of merchants with complete KYC documentation
   - Average time to complete verification
   - % of merchant applications rejected

2. **Monitoring Metrics:**
   - Number of transaction alerts generated
   - % of alerts reviewed within 48 hours
   - Number of SMRs filed
   - Number of TTRs filed (if any)

3. **Training Metrics:**
   - % of employees with current AML/CTF training
   - Average training assessment scores
   - Time to complete training for new hires

4. **System Metrics:**
   - System uptime and availability
   - Audit log completeness
   - Record retention compliance

**Reporting:** Dashboard reviewed monthly by Compliance Officer, quarterly by management

---

## Appendices

### Appendix A: Glossary of Terms

**AML/CTF:** Anti-Money Laundering and Counter-Terrorism Financing

**AUSTRAC:** Australian Transaction Reports and Analysis Centre (Australian FIU and AML/CTF regulator)

**CDD:** Customer Due Diligence

**EDD:** Enhanced Due Diligence

**ISO:** Independent Selling Organization (merchant acquirer agent)

**KYC:** Know Your Customer

**ML/TF:** Money Laundering / Terrorism Financing

**PEP:** Politically Exposed Person

**SMR:** Suspicious Matter Report

**TTR:** Threshold Transaction Report

### Appendix B: Reporting Thresholds

**Suspicious Matter Reports (SMRs):**
- Threshold: Reasonable grounds to suspect ML/TF
- Timing: As soon as practicable (no specific deadline, but urgency-dependent)

**Threshold Transaction Reports (TTRs):**
- Threshold: Physical currency transactions ≥ AUD $10,000
- Timing: Within 10 business days

**International Funds Transfer Instructions (IFTIs):**
- Not applicable to our business (we don't transfer funds internationally)

### Appendix C: Red Flag Examples

**Examples of Suspicious Activity in Our Business Context:**

1. Merchant insists on cash payouts despite having bank account
2. Merchant processes unusually high transaction volumes compared to typical taxi operations
3. Merchant requests frequent changes to payout bank account details
4. Multiple merchants using same bank account for payouts
5. Merchant processes transactions at unusual times (e.g., 3am) inconsistent with taxi operations
6. High rate of declined transactions suggesting card testing
7. Merchant provides false or inconsistent information
8. Merchant's license expired or suspended, but still requesting terminal
9. Unusual geographic patterns (transactions far from merchant's usual area)
10. Structuring behavior (multiple payouts just under $10,000)

### Appendix D: Contact Information

**Internal Contacts:**

**AML/CTF Compliance Officer:**
- Name: [TO BE COMPLETED]
- Email: [TO BE COMPLETED]
- Phone: [TO BE COMPLETED]

**Senior Management:**
- Name: [TO BE COMPLETED]
- Title: [TO BE COMPLETED]
- Email: [TO BE COMPLETED]
- Phone: [TO BE COMPLETED]

**External Contacts:**

**AUSTRAC:**
- Website: www.austrac.gov.au
- Online Reporting: online.austrac.gov.au
- Phone: 1300 021 037
- Email: contact@austrac.gov.au

**Australian Federal Police (for terrorism financing):**
- National Hotline: 131 AFP (131 237)
- Website: www.afp.gov.au

**Privacy Commissioner (for privacy matters):**
- Website: www.oaic.gov.au
- Phone: 1300 363 992

### Appendix E: Document Control

**Document History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | November 2025 | [Compliance Officer Name] | Initial version |

**Approval:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Compliance Officer | [Name] | | |
| Senior Management | [Name] | | |
| Board Representative | [Name] | | |

**Distribution:**

This document is distributed to:
- All employees (relevant sections)
- Board members (full document)
- External auditors (as required)
- Stored securely in compliance folder

**Confidentiality:**

This document contains confidential business information and should be handled accordingly.

---

**END OF AML/CTF COMPLIANCE FRAMEWORK**

**Document Reference:** AML-CTF-001
**Next Review Date:** November 2026
**Compliance Officer:** [Name]
