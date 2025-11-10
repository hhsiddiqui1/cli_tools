# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

This is the **tapease_response** subdirectory within the larger `cli_tools` repository. This directory contains comprehensive documentation prepared for ANZ Bank's review of A2 Square Pty Ltd's (trading as Tapease) banking arrangements.

**Purpose:** Response to ANZ Case Reference C25101056246 - Banking Arrangements Review

**Parent Repository:** CLI Tools - A command-line interface tool that leverages Google Gemini AI and integrated tools to streamline development workflows.

## Business Context

**A2 Square Pty Ltd (Tapease)** operates as an Independent Selling Organization (ISO) in partnership with Fiserv, providing payment terminal services to licensed taxi drivers in Sydney, Australia.

**Business Model:**
- Deploy Fiserv Clover terminals to taxi drivers (merchants)
- Receive daily bulk settlements from Fiserv (all merchant transactions combined)
- Calculate merchant payouts (gross transactions minus service fees)
- Distribute payouts via EFT, PayID, or cash

**Key Point:** Tapease does NOT process card transactions or handle cardholder data. All payment processing is performed by Fiserv in their PCI DSS Level 1 compliant environment.

**Compliance Context:**
- Subject to AML/CTF Act 2006 obligations
- Minimal PCI DSS scope (no cardholder data access)
- Transitioning to electronic-only merchant payouts

## Repository Structure

The parent `cli_tools` repository contains:
- **monoova_integration/** - Python-based Monoova Payments API integration for Australian dollar payouts
- **tapease_response/** (this directory) - ANZ banking review response documentation
- **README.md** - Comprehensive documentation for the CLI tools
- **requirements.txt** - Python dependencies (requests, plantuml, six, Pillow)
- **.venv/** - Python virtual environment

## Directory Contents

### Core Files
- **ANZ_Requests.txt** - Original communication from ANZ outlining review requirements
- **tapease-openapi.json** - Complete backend API specification (FastAPI)
- **GEMINI.md** - Instructions for Google Gemini AI
- **CLAUDE.md** - This file

### Output Folder (`/output`)

#### Primary Response Documents
1. **ANZ_Response_Complete.md** (18KB)
   - Comprehensive response to all 6 ANZ requirements
   - Payment flow explanation
   - Cash payment recipients list (template)
   - Monthly cash withdrawal estimates (template)
   - Electronic payment transition plan
   - AML/CTF program overview
   - Independent review status

2. **AML_CTF_Compliance_Framework.md** (27KB)
   - Complete AML/CTF compliance program
   - Regulatory framework
   - Risk assessment
   - Customer due diligence procedures
   - Transaction monitoring
   - Record keeping (7-year retention)
   - Employee training program
   - Governance structure

3. **PCI_DSS_Scope_Statement.md** (17KB)
   - Explains minimal PCI DSS scope
   - ISO vs Payment Processor comparison
   - Why Tapease doesn't handle cardholder data
   - Fiserv's responsibilities

4. **ANZ_Cover_Letter.md** (8.6KB)
   - Professional cover letter for submission
   - Executive summary
   - Key highlights
   - Contact information

#### Flow Diagrams
5. **comprehensive_payment_flow.puml** (4.7KB)
   - Detailed PlantUML sequence diagram
   - Shows card transaction → settlement → payout flow
   - Includes PCI DSS scope boundaries
   - Three payout methods (EFT, PayID, Cash)

6. **payment_flow.puml** (1.6KB)
   - Original simplified flow diagram

7. **Highlevel_Flow.png** (43KB)
   - Existing high-level flow visualization

#### Supporting Documents
8. **EXECUTIVE_SUMMARY.md** (12KB)
   - Quick reference guide
   - Key messages for ANZ
   - Risk assessment summary
   - Action checklist

9. **DATA_COLLECTION_TEMPLATE.md** (13KB)
   - Template to gather required data
   - Lists all data points needed
   - Identifies data sources

10. **README.md** (11KB)
    - Package overview
    - Diagram generation instructions
    - Submission checklist

11. **DIAGRAM_GENERATION_INSTRUCTIONS.txt** (6.7KB)
    - Step-by-step instructions for converting PlantUML to PNG

12. **ANZ_response.md** (2KB)
    - Original draft response

## Key Concepts

### Independent Selling Organization (ISO)
- Merchant acquirer agent that recruits and manages merchants
- Does NOT process transactions or handle cardholder data
- Facilitates relationship between merchants and payment processor (Fiserv)

### Payment Flow
1. **Transaction:** Customer → Clover Terminal → Fiserv → Card Networks → Issuing Bank
2. **Settlement (Payin):** Fiserv → ANZ (Tapease account) - Daily bulk transfer
3. **Payout:** Tapease → Merchants (EFT/PayID/Cash) - After fee calculation

### PCI DSS Scope
- **Tapease:** Minimal to NO scope (no cardholder data access)
- **Fiserv:** Full scope (PCI Level 1 compliant)
- **Card data flow:** Never enters Tapease systems

### AML/CTF Obligations
- Customer due diligence (KYC) on all merchants
- Transaction monitoring with automated alerts
- Suspicious matter reporting (SMRs to AUSTRAC)
- 7-year record retention
- Employee training program

## How to Use These Documents

### For ANZ Submission:

1. **Review all documents** in `/output` folder
2. **Complete data templates:**
   - Use `DATA_COLLECTION_TEMPLATE.md` to gather data
   - Fill in all [TO BE COMPLETED] placeholders in main documents
3. **Generate diagram:**
   - Convert `comprehensive_payment_flow.puml` to PNG
   - Use online tool: http://www.plantuml.com/plantuml/uml/
   - See `DIAGRAM_GENERATION_INSTRUCTIONS.txt`
4. **Convert to PDF:**
   - ANZ_Response_Complete.md → PDF
   - AML_CTF_Compliance_Framework.md → PDF
   - ANZ_Cover_Letter.md → PDF
5. **Submit to ANZ:**
   - Email: ANZresponse@anz.com
   - Subject: "Response to Case C25101056246"
   - Deadline: 12 November 2025

### Data Sources:

**From Database (tapease-openapi.json endpoints):**
- `/admin/search_users` - Merchant list
- `/transactions/search_transactions_by_user` - Transaction data
- `/payout/search_user_payouts` - Payout data
- `/admin/get_all_auditlogs` - Audit information

**From ANZ Statements:**
- Cash withdrawal amounts (last 6 months)
- Daily settlement receipts from Fiserv

**From Fiserv Reports:**
- Transaction volumes and amounts
- Settlement schedules
- Processing fees

## Key Commands

### Generate PlantUML Diagrams

```bash
# Install PlantUML (if needed)
sudo apt-get update
sudo apt-get install -y plantuml

# Navigate to output folder
cd /mnt/c/Users/hhsid/cli_root/tapease_response/output

# Generate PNG diagrams
plantuml comprehensive_payment_flow.puml
plantuml payment_flow.puml
```

### Or Use Online Tool (No Installation)
```
1. Visit: http://www.plantuml.com/plantuml/uml/
2. Copy contents of .puml file
3. Paste into editor
4. Download generated PNG
```

## Document Validation Checklist

Before submitting to ANZ:

- [ ] All [TO BE COMPLETED] placeholders filled with actual data
- [ ] Compliance Officer details added
- [ ] Cash payment merchant list complete with amounts
- [ ] Historical cash withdrawal data (6 months) added
- [ ] Banking statistics added (monthly volumes)
- [ ] Contact information verified
- [ ] PlantUML diagram converted to PNG
- [ ] Documents converted to PDF
- [ ] Senior management reviewed and approved
- [ ] Case reference (C25101056246) on all documents
- [ ] All attachments prepared
- [ ] Spelling and grammar checked

## ANZ Review Requirements

ANZ requested the following (all addressed in documentation):

1. ✅ **Visual payment flow diagram** - `comprehensive_payment_flow.puml/.png`
2. ✅ **List of cash payment recipients** - Template in `ANZ_Response_Complete.md` Section 2
3. ✅ **Monthly cash withdrawal amounts** - Template in `ANZ_Response_Complete.md` Section 3
4. ✅ **Electronic payment transition plan** - Detailed in `ANZ_Response_Complete.md` Section 4
5. ✅ **AML/CTF compliance program** - Complete in `AML_CTF_Compliance_Framework.md`
6. ✅ **Independent AML/CTF review** - Status and plan in `ANZ_Response_Complete.md` Section 6

## Important Dates

- **ANZ Letter Date:** 13 October 2025
- **Phone Call with ANZ:** 10 October 2025
- **Response Due Date:** 12 November 2025
- **Days to Complete:** 2 days from 10 November 2025

## Related Projects

### Monoova Integration
The sibling `monoova_integration/` directory contains a comprehensive payment API integration for Australian dollar payouts. Similar payment flow concepts apply:
- `/mnt/c/Users/hhsid/cli_root/monoova_integration/CLAUDE.md` - Detailed implementation guidance
- `/mnt/c/Users/hhsid/cli_root/monoova_integration/requirements.md` - Functional requirements
- Both projects involve merchant payouts and AML/CTF compliance

### Tapease Backend API
The `tapease-openapi.json` file in this directory documents the complete backend API including:
- Authentication and user management
- Transaction tracking and reporting
- Payout management
- Admin functions (user management, device assignment)
- Audit logging and compliance features
- Session tracking

## Critical Success Factors

1. **Emphasize LOW RISK:** No cardholder data access (Fiserv handles this)
2. **Demonstrate STRONG CONTROLS:** Comprehensive AML/CTF program
3. **Show CLEAR DIRECTION:** 12-month plan to eliminate cash
4. **Provide TRANSPARENCY:** Complete disclosure of operations
5. **Prove COMPLIANCE:** Operating in regulated taxi industry with licensed merchants

## Next Steps

1. **Complete data collection** using `DATA_COLLECTION_TEMPLATE.md`
2. **Fill in all placeholders** in main documents
3. **Generate diagram image** from PlantUML file
4. **Get management approval**
5. **Convert to professional PDFs**
6. **Submit to ANZ** before 12 November 2025
7. **Follow up** with ANZ after submission
8. **Implement** electronic payment transition plan
9. **Schedule** independent AML/CTF review (if required)
10. **Provide quarterly updates** to ANZ on progress
