# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Python-based Monoova Payments API integration** for automating customer payouts in Australian dollars. The system follows an event-driven architecture designed for AWS serverless deployment (Lambda, API Gateway, DynamoDB, SQS, Secrets Manager).

**Core Business Flow:**
1. Fiserv settles funds → ANZ accounts
2. Manual/automated transfer → Monoova mAccount
3. Admin-triggered payouts → End users via NPP (PayId/Bank Account)

**Current Status:** Documentation and design phase. Implementation not yet started.

## Key Commands

### Diagram Generation
```bash
python render_diagrams.py
```
Renders all `.plantuml` files in `docs/` to PNG images using the PlantUML web service. This is the primary build command currently available.

### Future Commands (Not Yet Implemented)
```bash
# Application execution (when implemented)
python payout_service.py

# Testing (when implemented)
python -m unittest discover
# OR
pytest

# Dependencies (when requirements.txt exists)
pip install -r requirements.txt
```

## Critical API Information

### ⚠️ IMPORTANT: Monoova API Payload Structure

The correct structure for NPP payouts to `/financial/v2/transaction/execute`:

```json
{
  "uniqueReference": "unique-id-here",
  "totalAmount": 100.00,
  "paymentSource": "mAccount",
  "mAccount": {
    "token": "6279059726039800"
  },
  "disbursements": [
    {
      "disbursementMethod": "NppCreditPayId",
      "toNppCreditPayIdDetails": {
        "payId": "customer@example.com",
        "payIdType": "Email",
        "accountName": "Customer Name",
        "remitterName": "Your Business Name"
      },
      "sourceBSB": "802-985",
      "sourceAccountNumber": "654378888",
      "amount": 100.00,
      "lodgementReference": "Payment reference"
    }
  ]
}
```

**Critical field names:**
- `uniqueReference` (NOT `callerUniqueReference`)
- `paymentSource: "mAccount"` (required)
- `mAccount.token` (16-digit account number)
- `disbursementMethod: "NppCreditPayId"` or `"NppCreditBankAccount"`

**See `validation_report.md` for detailed corrections to the initial documentation.**

### Monoova API Endpoints
- Base URL (Sandbox): `https://api.m-pay.com.au`
- Base URL (Production): `https://api.mpay.com.au`
- Authentication: HTTP Basic Auth with API key as username (password blank)
- Main payout endpoint: `POST /financial/v2/transaction/execute`
- Validation endpoint: `POST /financial/v2/transaction/validate`

### Webhook Events
- `NppPaymentStatus` - Final status of NPP payouts (Payment Successful/Rejected)
- `NPPReceivePayment` - Incoming NPP payments to mAccount
- `InboundDirectCredit` - Incoming Direct Entry payments
- `DirectEntryDishonour` - Payment failures

## Architecture & Design Patterns

### Event-Driven Asynchronous Model
- NPP payouts return `"Pending"` status immediately
- Final status delivered via `NppPaymentStatus` webhook
- Must implement webhook handlers to update transaction status
- Failed webhook processing → Dead Letter Queue (AWS SQS)

### Security Requirements
- **API Keys:** NEVER hardcode. Store in AWS Secrets Manager
- **Customer Data:** Encrypt bank accounts/PayIDs at rest (DynamoDB/RDS encryption)
- **Transport:** All communication via HTTPS/TLS
- **Idempotency:** Use unique `uniqueReference` per transaction to prevent duplicates on retry

### Planned AWS Infrastructure
- **Lambda:** Backend API handlers and webhook processors
- **API Gateway:** REST API exposure
- **DynamoDB:** Customer payout details storage (encrypted at rest)
- **Secrets Manager:** Monoova API key storage
- **SQS:** Dead Letter Queue for failed webhook processing
- **CloudWatch:** Logging and monitoring

## Documentation Structure

### Primary Documentation Files
- **`requirements.md`** - Functional requirements, business flows, compliance (PCI DSS, Privacy Act)
- **`analysis.md`** - Technical/non-functional requirements (security, scalability, reliability)
- **`validation_report.md`** - ⚠️ **READ THIS FIRST** - API corrections and validation results
- **`GEMINI.md`** - Original project overview (contains outdated API structure)

### Diagram Files (`docs/`)
All PlantUML source files with corresponding PNG renders:
- `funding_flow.plantuml` - ANZ → Monoova funding sequence
- `payout_flow.plantuml` - Admin-initiated payout to customer (⚠️ contains outdated API structure)
- `user_management_flow.plantuml` - Customer onboarding and payout destination setup
- `account_verification_flow.plantuml` - Optional bank account ownership verification
- `payout_activity_diagram.plantuml` - Activity diagram for payout process

**Note:** Some diagrams contain outdated API payload structures. Refer to `validation_report.md` for corrections.

### API Specifications
- `openapi.7b8bc5fd4cb41853ebd3.yaml` - Main Monoova Payments API (v5.29)
- `openapiPayTo.0f647d2bab917d5c40d6.yaml` - PayTo API (not currently used)
- `openapiCC.96fb2a03066b976b4b02.yaml` - Credit Card API (not currently used)

## Known Issues & Corrections

### Documentation Inconsistencies
1. **`requirements.md` lines 49-52:** API payload structure is incorrect (uses `callerUniqueReference` and wrong nesting)
2. **`docs/payout_flow.plantuml` lines 38-56:** Payload example needs updating
3. **`GEMINI.md` line 72:** References `callerUniqueReference` (should be `uniqueReference`)
4. **Transaction Limit:** $1,000 limit mentioned in docs is likely a business rule, not Monoova API limit (NPP max is $99,999,999,999)

**Action:** Update these files using the correct structure documented in `validation_report.md` before implementation.

## Development Conventions (Planned)

### Code Style
- Follow PEP 8 style guide
- Use type hints for all function signatures
- Python's `unittest` or `pytest` for testing

### Idempotency Pattern
Every API call to Monoova must include a unique `uniqueReference` (max 200 chars). On network failures, retry with the **same** reference to prevent duplicate transactions. Monoova deduplicates based on this field.

### Error Handling Pattern
- Transient errors: Retry with exponential backoff + jitter
- Failed webhooks: Send to DLQ for manual review
- Log all Monoova API errors to CloudWatch with full request/response context

## Important Context for Code Generation

When implementing Monoova API calls:
1. Always validate the payload structure against `validation_report.md`, NOT against the older `requirements.md` or diagram examples
2. Include the `mAccount.token` field (your 16-digit mAccount number)
3. Use `disbursementMethod: "NppCreditPayId"` or `"NppCreditBankAccount"` in disbursements
4. Minimum amount: $0.01 (enforce in validation)
5. All financial amounts are decimal/float, not integers
6. PayIdType values are case-sensitive: `"Email"`, `"PhoneNumber"`, `"ABN"`, `"ACN"`, `"OrganisationId"`

## Git Workflow Notes

- Main branch: `master`
- Initial commits include documentation setup and validation report
- `.gitignore` configured for Python projects (see `../.gitignore`)
