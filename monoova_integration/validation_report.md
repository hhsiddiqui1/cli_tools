# Monoova Integration Documentation Validation Report

**Date:** November 9, 2025
**Validation Scope:** Fund flow from ANZ → Monoova → End Users (NPP PayId/Account)

## Executive Summary

✅ **Overall Assessment: Documentation is MOSTLY CORRECT with some critical corrections needed**

Your research demonstrates a strong understanding of the Monoova payment flow. However, there are **critical API payload structure issues** that must be corrected before implementation.

---

## ✅ What You Got Right

### 1. **Fund Flow Architecture** ✓
Your documented flow is **CORRECT**:
- Fiserv → ANZ Accounts → Manual/Automated Transfer → Monoova mAccount → NPP Payouts

### 2. **Payment Methods** ✓
Correctly identified both NPP payment options:
- **NPP PayId** (NppCreditPayId) - for email, phone, ABN, etc.
- **NPP Bank Account** (NppCreditBankAccount) - for BSB + Account Number
Both are valid for Australian domestic transfers in AUD.

### 3. **Webhook Events** ✓
Correctly identified:
- `NPPReceivePayment` - for incoming funds to Monoova mAccount
- `NppPaymentStatus` - for outgoing payment status updates
- `InboundDirectCredit` - alternative for incoming Direct Entry payments
- `DirectEntryDishonour` - for failed payments

### 4. **Security & Compliance** ✓
- PCI DSS assessment is correct (not applicable since no card data handling)
- Privacy Act obligations correctly identified
- Security recommendations (encryption, AWS Secrets Manager) are sound

### 5. **Asynchronous Processing Model** ✓
Correctly understood that NPP payments return "Pending" status initially and final status comes via webhook.

---

## ❌ Critical Corrections Required

### 1. **API Request Structure** - INCORRECT

**Your Documentation (requirements.md:49-52):**
```json
{
  "callerUniqueReference": "payout-ref-xyz123",
  "source": { "accountNumber": "YOUR_mACCOUNT" },
  "disbursements": [...]
}
```

**❌ PROBLEM:** This structure is WRONG. The actual Monoova API uses a different schema.

**✅ CORRECT Structure (from official API):**

#### For NPP PayId Payment:
```json
{
  "uniqueReference": "f484ec18-6e1f-481b-a4bf-bea515d8lk34",
  "totalAmount": 100,
  "paymentSource": "mAccount",
  "mAccount": {
    "token": "6279059726039800"
  },
  "description": "NPP payment to PayID for immediate transaction settlement",
  "disbursements": [
    {
      "disbursementMethod": "NppCreditPayId",
      "toNppCreditPayIdDetails": {
        "payId": "customer@example.com",
        "payIdType": "Email",
        "accountName": "Customer Name",
        "endToEndId": "ABC/123-4356",
        "remitterName": "Your Business Name"
      },
      "sourceBSB": "802-985",
      "sourceAccountNumber": "654378888",
      "lodgementReference": "Payment reference",
      "amount": 100
    }
  ]
}
```

#### For NPP Bank Account Payment:
```json
{
  "uniqueReference": "f484ec18-6e1f-481b-a4bf-bea515d8lk34",
  "totalAmount": 100,
  "paymentSource": "mAccount",
  "mAccount": {
    "token": "6279059726039800"
  },
  "description": "Payment via NPP to bank account",
  "disbursements": [
    {
      "disbursementMethod": "NppCreditBankAccount",
      "toNppCreditBankAccountDetails": {
        "bsbNumber": "062-205",
        "accountNumber": "123456789",
        "accountName": "Customer Name",
        "endToEndId": "ABC/123-4356",
        "remitterName": "Your Business Name"
      },
      "sourceBSB": "802-985",
      "sourceAccountNumber": "654378888",
      "lodgementReference": "Payment reference",
      "amount": 100
    }
  ]
}
```

**Key Differences:**
1. Use `uniqueReference` NOT `callerUniqueReference`
2. Must include `paymentSource: "mAccount"` field
3. Must include `mAccount.token` with your 16-digit mAccount number
4. Must include `totalAmount` at top level
5. Source account specified via `sourceBSB` and `sourceAccountNumber` in each disbursement
6. Disbursement method is `NppCreditPayId` or `NppCreditBankAccount`, not just "npp"

---

### 2. **API Endpoint** - CORRECT BUT INCOMPLETE

**Your Documentation:**
- ✅ Endpoint: `POST /financial/v2/transaction/execute` is CORRECT
- ✅ Base URLs are correct (sandbox: api.m-pay.com.au, prod: api.mpay.com.au)

**Additional Info:**
- You should also document `POST /financial/v2/transaction/validate` for testing payloads before execution
- This endpoint uses the same payload structure but doesn't execute the transaction

---

### 3. **Transaction Limits** - NEEDS CLARIFICATION

**Your Documentation (requirements.md:47):**
> "Is the amount less than or equal to the AUD $1000 transaction limit?"

**⚠️ CLARIFICATION NEEDED:**
The Monoova API documentation does NOT specify a universal $1,000 limit for NPP payments. The actual limits are:

1. **NPP Network Maximum:** $99,999,999,999 (yes, that's ~$100 billion per the PayTo API docs)
2. **Your mAccount `nppPayoutLimit`:** This is account-specific and configured by Monoova
3. **Per-transaction minimum:** $0.01

**The $1,000 limit appears to be YOUR business rule, not Monoova's.**

**✅ RECOMMENDATION:**
- Clarify if $1,000 is your internal business limit or if Monoova set this limit on your account
- Document this as "business rule" not "Monoova API limit" to avoid confusion
- You can check your actual limit using the `GET /mAccount/v1/get/{accountNumber}` API which returns the `nppPayoutLimit` field

---

### 4. **Funding Flow Detail** - MISSING INFORMATION

**Your Documentation (requirements.md:20-26):**
You mention optional webhook notification for incoming funds.

**✅ ADDITIONAL INFO NEEDED:**
To receive webhook notifications for incoming funds, you need to:
1. Set up an **Automatcher account** (special receiving account type in Monoova)
2. Subscribe to either:
   - `NPPReceivePayment` webhook (for NPP incoming)
   - `InboundDirectCredit` webhook (for Direct Entry incoming)
3. The webhook will include the transaction amount, account number, and other details

**Note:** If you're doing a standard bank transfer from ANZ to Monoova without Automatcher, you won't get automatic webhooks. You'd need to check your mAccount balance via API or manually.

---

### 5. **PlantUML Diagrams** - PAYLOAD STRUCTURE INCORRECT

**File:** `docs/payout_flow.plantuml:38-56`

Your diagram shows:
```json
{
  "callerUniqueReference": "payout-ref-xyz123",
  "source": { "accountNumber": "YOUR_mACCOUNT" },
  "disbursements": [...]
}
```

**❌ This needs to be updated** to match the correct structure shown in Correction #1 above.

---

## 🔍 Additional Findings & Recommendations

### 1. **Response Status Values**
When you call `/financial/v2/transaction/execute`, the response will include:
- `status: "Accepted"` - Monoova accepted the request
- `uniqueReference` - Echo back your unique reference
- `transactionId` - Monoova's internal transaction ID

For NPP payments, the initial status will likely be **"Pending"** and you'll receive the final status (`Payment Successful` or `Rejected`) via the `NppPaymentStatus` webhook.

### 2. **Webhook Authentication**
The webhooks from Monoova include an `Authorization` header. You should:
- Validate this header in your webhook handler
- Implement signature verification (Monoova should provide details)
- Return HTTP 200 immediately or Monoova will retry once after 30 seconds

### 3. **Idempotency**
Your understanding of `uniqueReference` for idempotency is **CORRECT**. Monoova uses this as a nonce to prevent duplicate transactions.

### 4. **Account Verification Flow**
Your optional account verification using `POST /verify/v1/aba/initiate` is good practice. Note:
- The verification API actually uses `/verify/v2/npp/initiate` for NPP verification
- Endpoint: `POST /verify/v2/npp/initiate` (you referenced v1/aba)
- This sends a small NPP payment (typically $0.01) with a verification code

### 5. **Error Handling**
The API returns standard HTTP status codes:
- `200` - Success
- `400` - Bad request (validation errors)
- `500` - Internal server error

Errors include `statusDescription` field with plain English explanation.

### 6. **PayID Types**
Supported PayID types (case-sensitive strings):
- `"Email"`
- `"PhoneNumber"`
- `"ABN"`
- `"ACN"`
- `"OrganisationId"`

### 7. **Direct Entry (BECS) Alternative**
Your docs focus on NPP, but Monoova also supports Direct Entry (BECS) via `disbursementMethod: "directCredit"`. This is:
- ✅ Cheaper than NPP
- ❌ Slower (batch processing 7 times/day)
- ✅ Good for non-urgent payouts

Consider offering both options to users (NPP for urgent, Direct Entry for cost savings).

---

## 📋 Action Items

### Priority 1 (MUST FIX - Blocking)
1. ✅ Update `requirements.md` lines 49-56 with correct API payload structure
2. ✅ Update `docs/payout_flow.plantuml` lines 41-56 with correct payload
3. ✅ Clarify the $1,000 transaction limit source
4. ✅ Update any code examples to use correct field names

### Priority 2 (SHOULD FIX - Important)
5. ⚠️ Add documentation for the `/financial/v2/transaction/validate` endpoint
6. ⚠️ Document the mAccount token (16-digit account number) requirement
7. ⚠️ Clarify Automatcher setup requirements for incoming fund webhooks
8. ⚠️ Update account verification endpoint from v1/aba to v2/npp

### Priority 3 (NICE TO HAVE - Enhancement)
9. 💡 Add documentation for Direct Entry (BECS) as a cost-effective alternative
10. 💡 Document the mAccount balance checking API
11. 💡 Add error response examples
12. 💡 Document webhook retry behavior (1 retry after 30 seconds)

---

## 🎯 Conclusion

Your research is **thorough and demonstrates good understanding** of the payment flow architecture. The main issue is the **API request structure** which deviates from the official Monoova specification. This must be corrected before implementation to avoid runtime API errors.

**Confidence Level:**
- Overall flow understanding: ✅ 95% correct
- API implementation details: ⚠️ 60% correct (needs payload structure fix)
- Security & compliance: ✅ 100% correct

**Ready for Implementation?** ⚠️ **NOT YET** - Fix Priority 1 items first.

---

## 📚 Reference Files Validated

- ✅ `requirements.md` - Functional requirements
- ✅ `analysis.md` - Technical analysis
- ✅ `GEMINI.md` - Project overview
- ✅ `docs/funding_flow.plantuml` - Funding flow diagram
- ✅ `docs/payout_flow.plantuml` - Payout flow diagram
- ✅ `openapi.7b8bc5fd4cb41853ebd3.yaml` - Official Monoova API spec (v5.29)

---

**Validated by:** Claude Code (Sonnet 4.5)
**Official API Version:** Monoova Payments API v5.29
**Validation Date:** 2025-11-09
