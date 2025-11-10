# Response to ANZ Review Team
## Case Reference: C25101056246

**Date:** 10 November 2025
**Entity:** A2 Square Pty Ltd (trading as Tapease)
**Business Model:** Independent Selling Organization (ISO) for payment terminals

---

## Executive Summary

**A2 Square Pty Ltd** operates as an **Independent Selling Organization (ISO)** in partnership with **Fiserv**, providing payment terminal services to taxi operators in Sydney, Australia.

**Critical Point:** We do NOT process card transactions, handle cardholder data, or participate in the payment authorization/settlement process. Our role is strictly:
- Terminal deployment and merchant onboarding
- Receiving bulk settlements from Fiserv
- Calculating and distributing merchant payouts

**Our ANZ account is used for:**
1. **Receiving Payins:** Daily bulk settlement from Fiserv (all merchant transactions combined)
2. **Making Payouts:** Distributing funds to individual merchants via EFT, PayID, or cash

---

## 1. Visual Diagram of End-to-End Payment Flow

Please refer to the attached comprehensive payment flow diagram (`comprehensive_payment_flow.puml` and `comprehensive_payment_flow.png`) which illustrates:

### Transaction Flow Overview

#### Phase 1: Card Transaction Processing (Fiserv Ecosystem)
1. **Customer** pays taxi fare using credit/debit card at **Clover Terminal**
2. **Clover Terminal** (managed by Fiserv) encrypts and transmits card data to **Fiserv**
3. **Fiserv** (as the payment processor/acquirer) routes transaction through:
   - Card Networks (Visa/Mastercard)
   - Customer's issuing bank
4. **Authorization** is returned to terminal
5. **Receipt** is issued to customer

**IMPORTANT:** Tapease has **ZERO access** to card data during this process. All cardholder data remains within Fiserv's PCI-compliant environment.

#### Phase 2: Daily Settlement (Payin to Tapease)
1. **Fiserv** calculates end-of-day settlement for all merchants under our ISO account
2. **Fiserv** transfers **bulk settlement** to our **ANZ account** (single daily transfer)
3. **Fiserv** provides transaction reports via API containing:
   - Transaction amounts
   - Merchant identifiers
   - Terminal IDs
   - Transaction timestamps and status
   - **NO CARD DATA** (no PAN, cardholder names, etc.)

#### Phase 3: Payout Calculation (Internal Process)
1. **Tapease system** retrieves transaction data from Fiserv API
2. **Calculates merchant payouts:**
   - Gross transaction amount
   - Less: Tapease service fees (terminal rental, support)
   - Less: Processing fees (if applicable)
   - **= Net payout to merchant**
3. **Creates payout instructions** in our database with merchant payment preferences

#### Phase 4: Merchant Payouts (Three Methods)

**Method 1: Electronic Funds Transfer (EFT) - Preferred**
- Direct credit to merchant's bank account (BSB + Account Number)
- Processed via ANZ
- Confirmation received and recorded

**Method 2: PayID Transfer - Growing Adoption**
- Payment to merchant's PayID (mobile number or email)
- Processed via ANZ
- Confirmation received and recorded

**Method 3: Cash Payment - Legacy Method**
- Used by merchants who prefer/require cash
- Tapease withdraws cash from ANZ account (ATM or branch)
- Physical cash handed to merchant
- Merchant signs receipt as proof of payment
- Receipt scanned and stored in our system

---

## 2. List of Entities Receiving Cash Payments

**Note:** We are actively transitioning away from cash payments. Below is the current list of merchants who still receive cash payouts:

### Current Cash Payment Recipients (as of November 2025)

| Merchant Name | ABN | Monthly Average Cash Payout | Reason for Cash Preference |
|---------------|-----|---------------------------|----------------------------|
| **[TO BE COMPLETED]** | [ABN] | $[Amount] AUD | [Reason: e.g., No bank account, Preference, etc.] |
| **[TO BE COMPLETED]** | [ABN] | $[Amount] AUD | [Reason] |
| **[TO BE COMPLETED]** | [ABN] | $[Amount] AUD | [Reason] |

**Total Merchants Receiving Cash:** [TO BE COUNTED]
**Total Monthly Cash Disbursement:** $[TO BE CALCULATED] AUD

### Cash Payment Procedure

1. **Authorization:** Cash payout request approved by authorized Tapease personnel
2. **Withdrawal:** Cash withdrawn from ANZ account (recorded with merchant reference)
3. **Disbursement:** Cash physically handed to merchant
4. **Receipt:** Merchant signs receipt acknowledging payment amount and date
5. **Record Keeping:** Signed receipt scanned and stored with transaction reference
6. **Reconciliation:** Daily reconciliation of cash withdrawals vs cash receipts

**Security Measures:**
- Maximum cash limit per transaction: $[TO BE DEFINED] AUD
- Cash stored in secure safe when not immediately disbursed
- Only authorized personnel handle cash
- CCTV coverage of cash handling areas

---

## 3. Approximate Total Monthly Cash Withdrawals

### Historical Cash Withdrawal Data (Last 6 Months)

| Month | Total Cash Withdrawals (AUD) | Number of Cash Payouts | Average per Payout |
|-------|------------------------------|------------------------|-------------------|
| May 2025 | $[AMOUNT] | [COUNT] | $[AVG] |
| June 2025 | $[AMOUNT] | [COUNT] | $[AVG] |
| July 2025 | $[AMOUNT] | [COUNT] | $[AVG] |
| August 2025 | $[AMOUNT] | [COUNT] | $[AVG] |
| September 2025 | $[AMOUNT] | [COUNT] | $[AVG] |
| October 2025 | $[AMOUNT] | [COUNT] | $[AVG] |

**Average Monthly Cash Withdrawal:** $[TO BE CALCULATED] AUD

### Projected Future Cash Withdrawals

Based on our transition plan to electronic payments:

- **Next 3 months (Nov 2025 - Jan 2026):** Estimated $[AMOUNT] AUD/month
- **Next 6 months (Nov 2025 - Apr 2026):** Estimated $[AMOUNT] AUD/month
  *(Target: 50% reduction)*
- **Next 12 months (Nov 2025 - Oct 2026):** Estimated $[AMOUNT] AUD/month
  *(Target: 80% reduction)*

---

## 4. Transition to Fully Electronic Disbursement Method

**YES, we are actively transitioning to fully electronic disbursement (EFT and PayID only).**

### Transition Plan

#### Current State (November 2025)
- **Electronic Payments (EFT + PayID):** [X]% of merchants
- **Cash Payments:** [Y]% of merchants

#### Target State (December 2026)
- **Electronic Payments (EFT + PayID):** 95%+ of merchants
- **Cash Payments:** <5% of merchants (exceptional cases only)

### Implementation Strategy

**Phase 1: Education & Incentives (Nov 2025 - Feb 2026)**
- Educate merchants on benefits of electronic payments:
  - Faster payments (same-day or next-day)
  - Improved security (no physical cash handling)
  - Better record-keeping for tax purposes
  - PayID convenience (no need to remember BSB/Account)
- Offer incentives:
  - Reduced service fees for electronic payment adoption
  - Priority support for electronic payment users

**Phase 2: Mandatory Requirements for New Merchants (March 2026)**
- All new merchant onboarding requires valid bank account or PayID
- Cash payment option not offered to new merchants

**Phase 3: Migration of Existing Cash Users (April 2026 - August 2026)**
- Work with remaining cash-preferring merchants individually
- Assist with bank account setup if needed
- Provide PayID registration support

**Phase 4: Cash Payment Sunset (September 2026 onwards)**
- Cash payments available only for documented exceptional circumstances
- Requires special approval from management
- Subject to enhanced AML/CTF scrutiny

### Benefits of Electronic-Only Disbursement

**For Tapease:**
- Reduced operational costs (no cash handling)
- Improved security (no physical cash risks)
- Complete digital audit trail
- Simplified reconciliation
- Reduced AML/CTF compliance burden

**For ANZ:**
- Reduced cash withdrawal activity from our account
- More predictable transaction patterns
- Enhanced transparency and traceability
- Lower risk profile

**For Merchants:**
- Faster access to funds
- Better financial records for tax reporting
- Improved security
- Modern payment experience

---

## 5. AML/CTF Compliance Program

Please see the attached comprehensive AML/CTF Compliance Framework document (`AML_CTF_Compliance_Framework.md`).

### Overview of Our AML/CTF Program

As an ISO providing payment terminal services to merchants, we have implemented a comprehensive AML/CTF compliance program covering:

#### 1. Customer Due Diligence (CDD)

**All merchants undergo verification before terminal deployment:**

- **Identity Verification:**
  - Driver's license (front and back)
  - License number, expiry date, state of issue
  - Photo verification

- **Business Verification:**
  - Australian Business Number (ABN) verification via ABR lookup
  - Business name and trading name
  - Business address verification

- **Financial Verification:**
  - Bank account details (for EFT payments)
  - PayID verification (if using PayID)
  - Beneficial ownership information

**Documentation:** All verification documents stored securely in our system (see API: `/auth/upload-documents`)

#### 2. Ongoing Monitoring

- **Transaction Monitoring:**
  - Daily review of transaction patterns via Fiserv reports
  - Automated alerts for unusual activity:
    - Sudden spikes in transaction volumes
    - Unusual transaction times or patterns
    - Multiple declined transactions
  - Monthly merchant transaction analysis

- **Merchant Status Reviews:**
  - Quarterly review of merchant account status
  - Annual re-verification of merchant details
  - License expiry monitoring

#### 3. Risk Assessment

**Merchant Risk Classification:**
- **Low Risk:** Established taxi drivers with verified credentials, consistent transaction patterns
- **Medium Risk:** New merchants, temporary licenses, irregular patterns
- **High Risk:** Cash payment preference, high transaction variability (subject to enhanced scrutiny)

**Risk Factors Considered:**
- Transaction volumes and patterns
- Payment method preferences (cash vs electronic)
- License verification status
- ABN verification status
- Length of relationship
- Compliance history

#### 4. Reporting Obligations

- **Suspicious Matter Reports (SMRs):** Procedures in place to identify and report suspicious activities to AUSTRAC
- **Threshold Transaction Reports (TTRs):** Physical currency transactions ≥ $10,000 AUD reported to AUSTRAC
- **Record Keeping:** All transaction records retained for 7 years as required

#### 5. Training & Awareness

- All staff trained on AML/CTF obligations
- Annual refresher training
- Updates provided when regulations change
- Clear escalation procedures for suspicious activities

#### 6. AML/CTF Officer

**Designated AML/CTF Compliance Officer:**
- Name: [TO BE SPECIFIED]
- Role: [TO BE SPECIFIED]
- Responsibilities:
  - Oversee AML/CTF program implementation
  - Review and investigate alerts
  - Liaise with AUSTRAC as needed
  - Maintain compliance documentation
  - Conduct annual program review

---

## 6. Independent Review of AML/CTF Compliance Program

### Current Status

**[TO BE COMPLETED]**

We acknowledge that an independent review of our AML/CTF compliance program is a best practice and may be required depending on our regulatory classification.

### Action Plan

If we are required to have an independent review, we commit to:

1. **Engage Qualified Reviewer:** Retain an independent AML/CTF compliance specialist or audit firm with expertise in payment services
2. **Scope of Review:**
   - Assessment of our AML/CTF policies and procedures
   - Testing of control effectiveness
   - Review of transaction monitoring systems
   - Evaluation of staff training
   - Review of record-keeping practices
   - Assessment of reporting procedures
3. **Timeline:** Complete independent review by [DATE TO BE DETERMINED]
4. **Remediation:** Implement all recommendations from the review within 90 days

**Alternative:** If independent review is not yet completed, we can provide:
- Internal audit reports
- Compliance self-assessment documentation
- Evidence of ongoing compliance monitoring

---

## 7. Key Compliance Highlights

### PCI DSS Compliance

**Tapease PCI DSS Scope: MINIMAL (likely SAQ A-EP or exempt)**

**Rationale:**
- We do NOT process, store, or transmit cardholder data
- We do NOT have access to Fiserv's payment terminals (managed remotely by Fiserv)
- We receive only non-sensitive transaction data (amounts, timestamps, merchant IDs)
- All card data encryption and processing handled by Fiserv

**Fiserv Responsibility:**
- Fiserv (as the payment processor) maintains full PCI DSS Level 1 compliance
- Clover terminals are P2PE (Point-to-Point Encryption) certified
- All card data encrypted from point of entry
- Fiserv responsible for terminal security and updates

**Our Responsibility:**
- Protect Fiserv API credentials
- Secure transaction reporting data (non-cardholder data)
- Ensure merchant onboarding data security

### Data Security

**Our System Security Measures:**
- Secure API authentication (JWT tokens)
- Database encryption at rest
- TLS encryption in transit
- Role-based access control
- Audit logging of all system access
- Regular security updates
- Incident response procedures

**Data Retention:**
- Transaction data: 7 years (regulatory requirement)
- Merchant onboarding documents: 7 years
- Payout records: 7 years
- Audit logs: 7 years

---

## 8. Banking Arrangement with ANZ

### Our ANZ Account Usage

**Account Purpose:** Business transaction account for ISO operations

**Inflows (Credits):**
- Daily bulk settlements from Fiserv (single transfer per day)
- Occasional transfers from company operating account (if needed for cash flow)

**Outflows (Debits):**
- EFT payments to merchants (multiple daily)
- PayID payments to merchants (multiple daily)
- Cash withdrawals for merchant cash payouts (decreasing frequency)
- Business operating expenses (if applicable)

**Typical Daily Pattern:**
1. Morning: Receive bulk settlement from Fiserv (~[TIME])
2. Throughout day: Process merchant payouts via EFT/PayID
3. As needed: Cash withdrawals for scheduled cash payouts

**Monthly Volume Estimates:**
- **Total Credits:** $[AMOUNT] AUD/month (Fiserv settlements)
- **Total Debits:** $[AMOUNT] AUD/month (merchant payouts + expenses)
- **Number of Transactions:** [COUNT] credits, [COUNT] debits

### Reconciliation Process

**Daily:**
- Reconcile Fiserv settlement amount vs transaction reports
- Reconcile payout obligations vs available balance
- Verify all payout transactions completed

**Monthly:**
- Full account reconciliation
- Variance analysis
- Financial reporting

---

## 9. Supporting Documentation

Please find attached:

1. **comprehensive_payment_flow.png** - Visual diagram of end-to-end payment flow
2. **AML_CTF_Compliance_Framework.md** - Detailed AML/CTF compliance program documentation
3. **Merchant_Cash_Payment_Log.xlsx** - [TO BE CREATED] List of merchants receiving cash with amounts
4. **Cash_Withdrawal_History.xlsx** - [TO BE CREATED] Historical cash withdrawal data
5. **Merchant_KYC_Sample.pdf** - [TO BE CREATED] Sample merchant onboarding documentation (redacted)

---

## 10. Commitment to Compliance

A2 Square Pty Ltd is committed to:

✓ Maintaining full compliance with all AML/CTF obligations
✓ Transitioning to electronic-only disbursements within 12 months
✓ Providing complete transparency to ANZ regarding our operations
✓ Cooperating fully with ANZ's ongoing review and monitoring
✓ Promptly reporting any suspicious activities
✓ Maintaining robust record-keeping and audit trails
✓ Completing independent AML/CTF review (if required)

We value our banking relationship with ANZ and understand the importance of these compliance requirements in maintaining a safe and transparent financial system.

---

## 11. Contact Information

**For questions regarding this response:**

**Company:** A2 Square Pty Ltd (trading as Tapease)
**Contact Person:** [Name]
**Title:** [Title]
**Email:** [Email]
**Phone:** [Phone]

**AML/CTF Compliance Officer:**
**Name:** [Name]
**Email:** [Email]
**Phone:** [Phone]

---

## 12. Next Steps

We are prepared to:

1. Provide any additional information or clarification needed
2. Meet with ANZ Review Team to discuss our operations in detail
3. Provide access to our systems for verification (with appropriate safeguards)
4. Complete independent AML/CTF review if required
5. Implement any additional measures recommended by ANZ

**Please contact us at your earliest convenience to discuss any questions or concerns.**

---

**Submitted:** [DATE]
**Case Reference:** C25101056246
**Submitted by:** [Name, Title]

---

## Appendix A: API Endpoints for Compliance

Our backend system (`tapease-openapi.json`) includes comprehensive audit and compliance features:

**Transaction Management:**
- `/transactions/search_transactions_by_user` - Search transaction history
- `/transactions/get_gross_total` - Calculate transaction totals

**Payout Management:**
- `/payout/create_payout_instructions` - Create payout records
- `/payout/search_user_payouts` - Search payout history
- `/payout/available_payout` - Check available payout amounts

**Audit & Compliance:**
- `/admin/get_all_auditlogs` - Retrieve complete audit logs
- `/admin/get_auditlog_details` - Detailed audit log information
- `/admin/get_session_logs` - User session tracking
- `/admin/system_status` - System health monitoring

**Merchant Management:**
- `/auth/signup` - Merchant onboarding with KYC data collection
- `/auth/upload-documents` - License and ABN document upload
- `/admin/search_users` - Merchant search and filtering
- `/admin/activate_deactivate` - Merchant account status management

**Device Management:**
- `/admin/get_all_devices` - Terminal inventory
- `/admin/assign_device_to_user` - Terminal assignment tracking
- `/admin/trans_device_users_history` - Terminal assignment history

All API endpoints include authentication, authorization, audit logging, and data validation.

---

**[TO BE COMPLETED BY USER]:** Please review and fill in the bracketed placeholders [TO BE COMPLETED], [AMOUNT], [COUNT], [NAME], etc. with your specific data before submitting to ANZ.
