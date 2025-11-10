# PCI DSS Scope Statement
## A2 Square Pty Ltd (trading as Tapease)

**Document Version:** 1.0
**Date:** November 2025
**Review Date:** Annual

---

## Executive Summary

**A2 Square Pty Ltd (Tapease)** operates as an Independent Selling Organization (ISO) in partnership with Fiserv, providing payment terminal deployment services to merchants (taxi drivers) in Sydney, Australia.

**KEY FINDING:** Tapease has **MINIMAL TO NO PCI DSS SCOPE** because we do NOT process, store, or transmit cardholder data.

---

## What is PCI DSS?

The Payment Card Industry Data Security Standard (PCI DSS) is a set of security standards designed to ensure that all companies that accept, process, store, or transmit credit card information maintain a secure environment.

**PCI DSS applies to:** Any organization that stores, processes, or transmits cardholder data (CHD) or sensitive authentication data (SAD).

**Cardholder Data (CHD) includes:**
- Primary Account Number (PAN) - the credit/debit card number
- Cardholder name
- Expiration date
- Service code

**Sensitive Authentication Data (SAD) includes:**
- CVV/CVC (card verification value)
- PIN data
- Magnetic stripe data
- Chip data

---

## Tapease Business Model

### What We Do:
1. **Merchant Onboarding:** Sign up taxi drivers as merchants
2. **Terminal Deployment:** Deploy Fiserv-managed Clover terminals to merchants
3. **Settlement Receipt:** Receive daily bulk settlements from Fiserv (transaction amounts only)
4. **Payout Distribution:** Calculate and distribute merchant payouts via bank transfer, PayID, or cash

### What We Do NOT Do:
❌ Process card transactions
❌ Store cardholder data (card numbers, CVV, etc.)
❌ Transmit cardholder data
❌ Have access to payment terminals' card data
❌ Participate in payment authorization process
❌ Handle magnetic stripe, chip, or PIN data

---

## Payment Flow and Data Access

### Transaction Processing Flow

```
Customer → Clover Terminal (Fiserv) → Fiserv Gateway → Card Networks → Issuing Bank
                                            ↓
                                    Authorization Response
                                            ↓
                                    Fiserv Settlement
                                            ↓
                                    Transaction Reports (NO CHD)
                                            ↓
                                    Tapease (Amounts Only)
```

### Data Tapease Receives from Fiserv

**We ONLY receive:**
- Transaction ID
- Merchant ID
- Terminal ID
- Transaction amount (total, net, fees)
- Transaction timestamp
- Transaction status (approved/declined)
- Payment method TYPE (e.g., "Visa", "Mastercard", "EFTPOS")
- Last 4 digits of card (in some reports, but NOT full PAN)

**We NEVER receive:**
- Full card numbers (PAN)
- Cardholder names
- CVV/CVC
- Expiration dates
- Magnetic stripe data
- Chip data
- PIN data

### Sample Transaction Data We Receive

**Example from Fiserv API:**
```json
{
  "transaction_id": "TXN123456789",
  "merchant_id": "MERCH001",
  "terminal_id": "TERM12345",
  "amount": 2500,
  "timestamp": "2025-11-10T14:32:00Z",
  "status": "APPROVED",
  "payment_method": "Visa",
  "card_last4": "1234",
  "auth_code": "ABC123"
}
```

**Notice:** NO full card number, NO cardholder name, NO CVV, NO expiration date.

---

## Fiserv's Role and Responsibilities

### Fiserv as the Payment Processor

**Fiserv** is the payment processor (acquirer) and is responsible for:
- PCI DSS Level 1 compliance (highest level)
- All cardholder data security
- Payment terminal management (Clover devices)
- Point-to-Point Encryption (P2PE)
- Payment gateway security
- Authorization and settlement processing
- Card data storage and transmission
- Terminal software updates and security patches

### Clover Terminals (Fiserv-Managed)

**Clover devices** used by our merchants are:
- Owned and managed by Fiserv
- PCI PTS (PIN Transaction Security) certified
- P2PE (Point-to-Point Encryption) enabled
- Remotely managed and updated by Fiserv
- Card data encrypted from point of card entry
- Encrypted card data transmitted directly to Fiserv
- **Tapease has NO access to terminal internals or card data**

**Terminal Management:**
- Software updates: Fiserv
- Security patches: Fiserv
- Terminal configuration: Fiserv
- Encryption key management: Fiserv
- Monitoring and logging: Fiserv

**Tapease Involvement:**
- Physical deployment of terminal to merchant location
- Basic troubleshooting (power, connectivity issues)
- Escalation to Fiserv for payment-related issues
- **NO access to card data or payment processing functions**

---

## Tapease PCI DSS Scope Assessment

### PCI DSS Compliance Levels

PCI DSS categorizes merchants into levels based on transaction volume:

- **Level 1:** > 6 million card transactions/year
- **Level 2:** 1-6 million transactions/year
- **Level 3:** 20,000 - 1 million e-commerce transactions/year
- **Level 4:** < 20,000 e-commerce OR < 1 million other transactions/year

### Tapease's PCI Level

**Tapease Transaction Volume:** 0 (zero) transactions

**Rationale:** We do NOT process any card transactions. All transactions are processed by Fiserv.

**Result:** Tapease is NOT a merchant or payment processor in PCI DSS terms.

### Tapease's PCI DSS Obligations

Given our business model, our PCI DSS scope is determined by our relationship with Fiserv.

**Applicable SAQ (Self-Assessment Questionnaire):**

**Most Likely: SAQ A-EP** (E-commerce merchants who outsource all payment processing to validated third parties)

**Alternative: No SAQ Required** (if considered purely a merchant recruiting/management entity)

### Why SAQ A-EP May Apply:

- We do not store, process, or transmit cardholder data
- All payment processing outsourced to PCI DSS compliant third party (Fiserv)
- We only receive non-sensitive transaction data from Fiserv
- We do not have access to payment systems or cardholder data

### SAQ A-EP Requirements (if applicable):

**Key requirements under SAQ A-EP:**

1. **Maintain secure network:**
   - Firewall configuration for our systems
   - Change default passwords
   - ✅ **Status:** Implemented

2. **Protect cardholder data:**
   - We don't have cardholder data, so this is N/A
   - ✅ **Status:** N/A (no CHD)

3. **Maintain vulnerability management:**
   - Use and maintain antivirus software
   - Develop secure systems and applications
   - ✅ **Status:** Implemented (regular updates, security patches)

4. **Implement strong access control:**
   - Restrict access to transaction data by business need-to-know
   - Unique ID for each person with system access
   - Restrict physical access to systems
   - ✅ **Status:** Implemented (role-based access control, MFA)

5. **Monitor and test networks:**
   - Track and monitor all access to network resources and cardholder data
   - ✅ **Status:** Implemented (audit logs, session tracking)

6. **Maintain information security policy:**
   - Information security policy in place
   - ✅ **Status:** Implemented (see AML/CTF and security policies)

---

## Tapease Systems and Data Security

### What We Do Store and Protect

**Merchant Data (Non-Cardholder Data):**
- Merchant identity documents (driver license, ABN)
- Merchant bank account details (for payouts)
- Transaction reports (amounts, timestamps - NO card data)
- Payout records
- Audit logs

**Security Measures in Place:**

✅ **Encryption:**
- Data encrypted at rest (database encryption)
- Data encrypted in transit (TLS 1.2+)
- HTTPS for all web communications

✅ **Access Control:**
- Role-based access control (RBAC)
- Multi-factor authentication (MFA) for admin access
- Unique user IDs for all system access
- Principle of least privilege

✅ **Network Security:**
- Firewall protection
- Regular security updates and patches
- No direct database access from internet

✅ **Monitoring and Logging:**
- Comprehensive audit logging
- Session tracking
- Exception logging
- Regular log review

✅ **Physical Security:**
- Secure data center (cloud hosting with security certifications)
- Restricted physical access
- Backup and disaster recovery

✅ **Secure Development:**
- Input validation
- SQL injection prevention
- XSS prevention
- Authentication and authorization on all endpoints
- Regular security code reviews

✅ **Incident Response:**
- Incident response plan in place
- Breach notification procedures
- Regular backups

### Fiserv API Security

**Tapease's connection to Fiserv:**
- API authentication (API keys, OAuth tokens)
- TLS encryption for all API calls
- API credentials stored securely (encrypted)
- Rate limiting and monitoring
- No cardholder data transmitted via API

---

## Third-Party Service Providers

### Fiserv
- **Service:** Payment processing, terminal management
- **PCI Status:** PCI DSS Level 1 Service Provider (validated)
- **Attestation:** Annual ROC (Report on Compliance) completed
- **Cardholder Data Access:** YES (they are the processor)

### [Cloud Hosting Provider - if applicable]
- **Service:** Application hosting, database hosting
- **PCI Status:** PCI DSS compliant infrastructure
- **Cardholder Data Access:** NO (we don't store CHD)

### ANZ Bank
- **Service:** Banking services for settlements and payouts
- **PCI Status:** PCI compliant financial institution
- **Cardholder Data Access:** NO (only receive funds, not card data)

---

## Attestation of Compliance

### Annual Compliance Validation

**If SAQ A-EP is required:**

**Annual Requirements:**
1. Complete SAQ A-EP questionnaire
2. Quarterly network vulnerability scans by Approved Scanning Vendor (ASV) - if applicable
3. Attestation of Compliance (AOC) signed by authorized representative

**Timeline:**
- SAQ completion: [Month/Year]
- Next SAQ due: [Month/Year]

**Responsible Party:** [Name, Title]

### Compliance Evidence

**Evidence we can provide:**
- SAQ A-EP completion (if required)
- Network diagram showing data flow
- Policy and procedure documents
- Security controls documentation
- Fiserv PCI compliance certificate
- Third-party security assessments (if available)

---

## Clarification for Banking Partners (ANZ)

### Why ANZ Should Be Comfortable with Our PCI Scope

1. **No Card Data Exposure:**
   - We never touch, see, or store card data
   - All card data handled by Fiserv (PCI Level 1 compliant)

2. **Minimal Risk to Financial System:**
   - Even if our systems were compromised, no cardholder data would be exposed
   - Transaction amounts and merchant data are protected but not card data

3. **Segregation of Duties:**
   - We handle merchant relationships and payouts
   - Fiserv handles all payment processing
   - Clear separation of responsibilities

4. **Regulated Partners:**
   - Fiserv is PCI Level 1 compliant (highest level)
   - ANZ is PCI compliant (as a card-issuing bank)
   - We operate between two highly regulated entities

5. **Strong Security Posture:**
   - Despite minimal PCI scope, we maintain strong security
   - Encryption, access controls, monitoring, audit logging
   - Regular security updates and reviews

---

## Comparison: Payment Processor vs ISO

### Payment Processor (e.g., Fiserv)
- ✓ Processes card transactions
- ✓ Stores cardholder data
- ✓ Transmits cardholder data
- ✓ Manages payment terminals
- ✓ Connects to card networks
- ✓ **Full PCI DSS scope (Level 1)**

### Independent Selling Organization (Tapease)
- ✗ Does NOT process card transactions
- ✗ Does NOT store cardholder data
- ✗ Does NOT transmit cardholder data
- ○ Deploys terminals (but no access to card data)
- ✗ Does NOT connect to card networks
- ✓ **Minimal to no PCI DSS scope**

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    PCI DSS SCOPE BOUNDARY                   │
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│  │ Customer │ -> │  Clover  │ -> │  Fiserv  │            │
│  │   Card   │    │ Terminal │    │ Payment  │            │
│  └──────────┘    └──────────┘    │ Gateway  │            │
│                        │          └──────────┘            │
│                        │                 │                 │
│                   Card Data         Card Data             │
│                   (Encrypted)       (Processed)           │
│                                          │                 │
└──────────────────────────────────────────┼─────────────────┘
                                           │
                                           ▼
                              ┌────────────────────┐
                              │  Card Networks     │
                              │  (Visa/Mastercard) │
                              └────────────────────┘
                                           │
                                           ▼
                              ┌────────────────────┐
                              │   Issuing Bank     │
                              └────────────────────┘

────────────────────── OUTSIDE PCI SCOPE ──────────────────────

                              ┌────────────────────┐
                              │     Fiserv         │
                              │ Settlement System  │
                              └────────────────────┘
                                           │
                                           ▼
                              ┌────────────────────┐
                              │   Fiserv API       │
                              │ (Transaction Data) │
                              │  NO CARD DATA      │
                              └────────────────────┘
                                           │
                                           ▼
                              ┌────────────────────┐
                              │     Tapease        │
                              │  (ISO - Payout     │
                              │   Management)      │
                              └────────────────────┘
                                           │
                                           ▼
                              ┌────────────────────┐
                              │    ANZ Bank        │
                              │ (Payout Transfers) │
                              └────────────────────┘
                                           │
                                           ▼
                              ┌────────────────────┐
                              │    Merchants       │
                              │  (Taxi Drivers)    │
                              └────────────────────┘
```

---

## Conclusion

**Tapease operates with MINIMAL TO NO PCI DSS SCOPE** due to our business model as an ISO that does not process, store, or transmit cardholder data.

**Key Takeaways:**

1. ✅ All cardholder data security is Fiserv's responsibility (PCI Level 1 compliant)
2. ✅ Tapease only receives non-sensitive transaction data (amounts, IDs, timestamps)
3. ✅ Clover terminals are P2PE certified and managed by Fiserv
4. ✅ Card data never enters Tapease systems
5. ✅ We maintain strong security practices despite minimal PCI scope
6. ✅ Our role is merchant management and payout distribution, not payment processing

**For ANZ:** This means minimal risk from a payment card security perspective. Even in the unlikely event of a Tapease system breach, no cardholder data would be compromised because we don't have any.

---

## Contact for PCI DSS Questions

**Internal Contact:**
- Name: [TO BE COMPLETED]
- Title: IT/Security Manager or Compliance Officer
- Email: [TO BE COMPLETED]
- Phone: [TO BE COMPLETED]

**Fiserv PCI Compliance Contact:**
- Available upon request from Fiserv account manager

---

**Document Prepared by:** [Name, Title]
**Date:** [Date]
**Next Review:** [Date + 1 year]
**Approved by:** [Senior Management Name, Title]

---

**References:**
- PCI Security Standards Council: www.pcisecuritystandards.org
- PCI DSS v4.0 (current version)
- SAQ A-EP Instructions and Guidelines
- Fiserv PCI Compliance Documentation
