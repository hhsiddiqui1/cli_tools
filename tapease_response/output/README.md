# Tapease ANZ Response Package

**Case Reference:** C25101056246
**Due Date:** 12 November 2025
**Prepared for:** ANZ Review Team

---

## Package Contents

This folder contains comprehensive documentation prepared in response to ANZ's review request regarding A2 Square Pty Ltd (trading as Tapease) banking arrangements.

### 1. Primary Documents

#### a) **ANZ_Response_Complete.md**
Comprehensive response document addressing all six requirements from ANZ:
1. ✅ Visual diagram of end-to-end payment flow
2. ✅ List of entities receiving cash payments (template provided - requires completion)
3. ✅ Monthly cash withdrawal estimates (template provided - requires completion)
4. ✅ Transition plan to fully electronic disbursement
5. ✅ AML/CTF compliance program (see separate document)
6. ✅ Independent review status and plan

**Action Required:** Complete the bracketed placeholders [TO BE COMPLETED] with your specific data.

#### b) **AML_CTF_Compliance_Framework.md**
Detailed AML/CTF compliance program covering:
- Regulatory framework
- Business risk assessment
- Customer due diligence procedures
- Ongoing monitoring systems
- Suspicious matter reporting procedures
- Record keeping requirements
- Employee training program
- Governance and oversight structure

**Action Required:** Complete placeholders with Compliance Officer details and specific dates.

### 2. Payment Flow Diagrams

#### a) **comprehensive_payment_flow.puml**
PlantUML source file showing complete end-to-end payment flow including:
- Card present transaction processing (Fiserv ecosystem)
- PCI DSS scope boundaries
- Daily settlement (Payin from Fiserv)
- Payout calculation
- Three payout methods (EFT, PayID, Cash)
- Audit and compliance checkpoints

#### b) **payment_flow.puml**
Original simplified payment flow diagram

#### c) **Highlevel_Flow.png**
Existing high-level flow visualization

### 3. Supporting Files

#### **tapease-openapi.json**
Complete backend API specification demonstrating:
- Transaction management endpoints
- Payout management system
- Comprehensive audit logging
- KYC/merchant onboarding workflows
- Device/terminal management
- Session tracking and monitoring

This demonstrates the technical infrastructure supporting compliance obligations.

---

## Generating Visual Diagrams

The PlantUML (.puml) files need to be converted to PNG images for submission to ANZ.

### Option 1: Online PlantUML Editor (Easiest)
1. Visit: http://www.plantuml.com/plantuml/uml/
2. Open `comprehensive_payment_flow.puml` in a text editor
3. Copy the entire contents
4. Paste into the online editor
5. Click "Submit" to generate the diagram
6. Right-click the generated image and "Save Image As..."
7. Save as `comprehensive_payment_flow.png`

### Option 2: PlantUML Desktop Application
1. Download PlantUML from: https://plantuml.com/download
2. Install Java if not already installed
3. Run: `java -jar plantuml.jar comprehensive_payment_flow.puml`
4. Output: `comprehensive_payment_flow.png`

### Option 3: VS Code Extension (if using VS Code)
1. Install "PlantUML" extension by jebbs
2. Open `comprehensive_payment_flow.puml`
3. Press `Alt+D` to preview
4. Right-click preview and export to PNG

### Option 4: Command Line (Linux/WSL)
```bash
# Install PlantUML
sudo apt-get update
sudo apt-get install -y plantuml

# Generate diagrams
cd /mnt/c/Users/hhsid/cli_root/tapease_response/output
plantuml comprehensive_payment_flow.puml
plantuml payment_flow.puml
```

---

## Documents to Submit to ANZ

### Must Submit:
1. ✅ **ANZ_Response_Complete.md** (or convert to PDF)
2. ✅ **comprehensive_payment_flow.png** (generated from .puml)
3. ✅ **AML_CTF_Compliance_Framework.md** (or convert to PDF)

### Should Submit (if available):
4. **Merchant_Cash_Payment_Log.xlsx** - List of merchants receiving cash with amounts
5. **Cash_Withdrawal_History.xlsx** - Historical cash withdrawal data (last 6 months)
6. **Merchant_KYC_Sample.pdf** - Redacted sample of merchant onboarding documentation

### Optional Supporting Documents:
7. **tapease-openapi.json** - Technical API documentation (if ANZ requests technical details)
8. Sample audit log reports
9. Sample transaction reports from Fiserv

---

## Before Submitting to ANZ - Checklist

### ANZ_Response_Complete.md - Data to Complete:

- [ ] **Section 2: List of Entities Receiving Cash Payments**
  - [ ] Merchant names, ABNs, monthly amounts
  - [ ] Total merchants receiving cash
  - [ ] Total monthly cash disbursement

- [ ] **Section 3: Approximate Total Monthly Cash Withdrawals**
  - [ ] Historical data for last 6 months (table)
  - [ ] Average monthly cash withdrawal amount
  - [ ] Projected future amounts

- [ ] **Section 4: Current State Percentages**
  - [ ] % of merchants using electronic payments
  - [ ] % of merchants using cash payments

- [ ] **Section 5: AML/CTF Compliance Officer Details**
  - [ ] Officer name, title, contact details

- [ ] **Section 6: Independent Review Status**
  - [ ] Has independent review been completed?
  - [ ] If not, proposed timeline

- [ ] **Section 8: Banking Statistics**
  - [ ] Monthly account volumes (credits, debits)
  - [ ] Number of transactions
  - [ ] Typical settlement time from Fiserv

- [ ] **Section 11: Contact Information**
  - [ ] Company contact person details
  - [ ] AML/CTF officer details

- [ ] **Section 12: Submission Details**
  - [ ] Submission date
  - [ ] Name and title of person submitting

### AML_CTF_Compliance_Framework.md - Data to Complete:

- [ ] **Section 2: Regulatory Framework**
  - [ ] Company ABN
  - [ ] AUSTRAC registration number (if applicable)

- [ ] **Section 9: Compliance Officer**
  - [ ] Officer name, title, email, phone
  - [ ] Officer qualifications

- [ ] **Section 9: Independent Review**
  - [ ] Next independent review due date

- [ ] **Appendix D: Contact Information**
  - [ ] All internal contact details

- [ ] **Appendix E: Document Control**
  - [ ] Author name
  - [ ] Approval signatures and dates

---

## Key Messages for ANZ

### 1. We Are an ISO, Not a Payment Processor
- We do NOT handle, store, or process card data
- All card transactions processed by Fiserv (PCI Level 1 compliant)
- Our PCI DSS scope is minimal

### 2. We Have Robust AML/CTF Controls
- Comprehensive KYC verification for all merchants
- Transaction monitoring with automated alerts
- Complete audit trail of all transactions and payouts
- Structured reporting procedures

### 3. We Are Transitioning Away from Cash
- Active 12-month plan to move to 95%+ electronic payments
- Cash payments declining
- New merchants required to use electronic payments
- Benefits for all parties (security, transparency, efficiency)

### 4. Complete Transparency
- Full cooperation with ANZ review
- Willing to provide additional information
- Open to implementing additional controls if recommended
- Strong commitment to compliance

---

## Timeline

**ANZ Due Date:** 12 November 2025
**Days Remaining:** Calculate based on today's date (10 November 2025) = **2 days**

### Recommended Action Plan:

**Day 1 (Today):**
- ✅ Review all documents
- ✅ Complete all [TO BE COMPLETED] placeholders
- ✅ Generate PNG diagrams from PlantUML files
- ✅ Create Excel files for cash payment data
- ✅ Prepare sample KYC documentation (redacted)

**Day 2 (Tomorrow):**
- Convert markdown files to professional PDFs
- Final review of all documents
- Get senior management sign-off
- Prepare submission email
- Submit to ANZ before EOD

---

## Contact for Questions

**Internal:**
- Compliance Officer: [Name, Email, Phone]
- Senior Management: [Name, Email, Phone]

**ANZ Review Team:**
- Email: ANZresponse@anz.com
- Case Reference: C25101056246
- Hotline: 1800 717 686
- Extension: 23981 (Option 1)

---

## Document Quality Checklist

Before submitting, ensure:

- [ ] All documents professionally formatted
- [ ] No spelling or grammar errors
- [ ] All placeholders completed
- [ ] All data accurate and verifiable
- [ ] Diagrams clear and legible
- [ ] Consistent terminology throughout
- [ ] Senior management reviewed and approved
- [ ] All supporting documents attached
- [ ] Case reference included on all documents
- [ ] Contact information accurate

---

## Technical Notes

### Backend System Capabilities (for reference)

Our system demonstrates strong technical infrastructure for compliance:

**Transaction Management:**
- Complete transaction history with search/filter capabilities
- Real-time transaction status tracking
- Gross transaction calculations

**Payout Management:**
- Automated payout instruction creation
- Multi-method support (EFT, PayID, Cash)
- Status tracking (Pending, Completed, Rejected)
- Full payout history

**Audit & Compliance:**
- Comprehensive audit logging (all database changes)
- Session tracking (all user logins/activities)
- System health monitoring
- Exception logging (frontend and backend)

**Merchant Management:**
- KYC document upload and storage
- Identity verification workflows
- Account status management (Active, Inactive, Disabled)
- Profile update tracking

**Device/Terminal Management:**
- Terminal inventory tracking
- Assignment history (which terminal to which merchant)
- Status tracking
- Complete audit trail of assignments

All endpoints include authentication, authorization, and audit logging.

---

## Additional Resources

If ANZ requests additional information, we can provide:

1. **Sample Reports:**
   - Daily settlement report from Fiserv (redacted)
   - Sample transaction export
   - Sample payout report
   - Audit log sample

2. **System Documentation:**
   - Full API documentation (tapease-openapi.json)
   - Database schema (if requested)
   - Security measures documentation

3. **Compliance Documentation:**
   - Privacy policy
   - Data security policy
   - Incident response plan
   - Business continuity plan

4. **Financial Information:**
   - Transaction volume trends
   - Merchant growth statistics
   - Payout method breakdown over time

---

**Prepared by:** Claude Code AI Assistant
**Date:** 10 November 2025
**Purpose:** ANZ Review Response Package (Case C25101056246)

---

## Quick Start

1. Generate diagram: Visit http://www.plantuml.com/plantuml/uml/ and paste `comprehensive_payment_flow.puml` contents
2. Complete data: Open `ANZ_Response_Complete.md` and fill in all [TO BE COMPLETED] sections
3. Review: Check both main documents for accuracy
4. Submit: Email all documents to ANZresponse@anz.com with Case Reference: C25101056246

**Time is of the essence - due in 2 days!**
