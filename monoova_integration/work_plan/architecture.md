# AWS Serverless Architecture for Monoova Payments Integration

## Executive Summary

This document describes a cost-optimized, serverless AWS architecture for processing 100-200 daily payouts through the Monoova Payments API. The solution leverages AWS Lambda, API Gateway, DynamoDB, and SQS to achieve a pay-per-use model with estimated monthly costs of **$15-25** including AWS Free Tier benefits.

**Key Architecture Principles:**
- Event-driven, asynchronous processing model
- Zero idle infrastructure costs (pure serverless)
- Automatic scaling from 0 to thousands of requests
- Built-in resilience with dead letter queues and retries
- Security-first design with encryption and secrets management

---

## High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          AWS Cloud (ap-southeast-2)                      │
│                                                                          │
│  ┌──────────────┐         ┌─────────────────┐                          │
│  │  Admin Web   │────────>│   API Gateway   │                          │
│  │  Application │  HTTPS  │  REST API       │                          │
│  └──────────────┘         │  /payouts       │                          │
│                           └────────┬─────────┘                          │
│                                    │                                     │
│                                    │ invoke                              │
│                           ┌────────▼─────────┐                          │
│                           │  Payout Handler  │                          │
│                           │  Lambda Function │                          │
│                           │  (Python 3.12)   │                          │
│                           └────────┬─────────┘                          │
│                                    │                                     │
│                    ┌───────────────┼───────────────┐                    │
│                    │               │               │                     │
│             ┌──────▼─────┐  ┌─────▼──────┐  ┌────▼────────┐           │
│             │   Secrets  │  │  DynamoDB  │  │  Monoova    │           │
│             │  Manager   │  │   Table    │  │  API        │           │
│             │ (API Key)  │  │ Payouts    │  │ (External)  │           │
│             └────────────┘  └────────────┘  └─────────────┘           │
│                                                     │                    │
│                                                     │ webhook            │
│                           ┌─────────────────────────▼──┐                │
│                           │   Webhook Handler Lambda   │                │
│                           │   (NppPaymentStatus)       │                │
│                           └─────────────┬──────────────┘                │
│                                         │                                │
│                                ┌────────┼────────┐                      │
│                                │                 │                       │
│                         ┌──────▼─────┐   ┌──────▼────────┐             │
│                         │  DynamoDB  │   │  SQS DLQ      │             │
│                         │  (Update)  │   │  (Failed)     │             │
│                         └────────────┘   └───────────────┘             │
│                                                                          │
│                           ┌─────────────────┐                           │
│                           │  CloudWatch     │                           │
│                           │  Logs & Alarms  │                           │
│                           └─────────────────┘                           │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. API Gateway

**Configuration:**
- Type: REST API (not HTTP API - for better feature support)
- Authentication: AWS IAM or Cognito User Pool
- Throttling: 100 requests/second (burst 200)
- Endpoint: Regional (ap-southeast-2)

**Routes:**
- `POST /payouts` → Payout Handler Lambda
- `POST /webhooks/monoova` → Webhook Handler Lambda

**Features:**
- Request validation at gateway level
- API keys for webhook authentication
- CloudWatch logging enabled
- CORS configuration for web app

**Cost:** $3.50/million requests (first 333M requests)
- Expected: ~6,000 requests/month (200 payouts × 30 days)
- Estimated cost: **$0.02/month** (effectively free with API Gateway free tier)

---

### 2. Lambda Functions

#### 2.1 Payout Handler Lambda

**Purpose:** Process payout requests from admin web application

**Specifications:**
- Runtime: Python 3.12 (ARM64 Graviton2 for 20% cost savings)
- Memory: 512 MB
- Timeout: 30 seconds
- Concurrency: Reserved 5 (to prevent cold starts during peak usage)

**Execution Flow:**
1. Receive payout request (customer_id, amount, payout_method)
2. Validate input parameters (amount > 0.01, amount <= 1000, customer exists)
3. Retrieve customer payout details from DynamoDB
4. Retrieve Monoova API key from Secrets Manager (cached)
5. Generate unique reference (UUID v4)
6. Construct Monoova API payload (correct structure from validation_report.md)
7. Call Monoova `/financial/v2/transaction/execute` with retry logic
8. Store transaction record in DynamoDB (status: Pending)
9. Return 202 Accepted with transaction_id

**Environment Variables:**
- `MONOOVA_API_SECRET_ARN`: ARN of Secrets Manager secret
- `DYNAMODB_TABLE_NAME`: Name of transactions table
- `MONOOVA_BASE_URL`: API endpoint (sandbox vs production)
- `MONOOVA_MACCOUNT_TOKEN`: 16-digit mAccount number
- `MONOOVA_SOURCE_BSB`: Source BSB for disbursements
- `MONOOVA_SOURCE_ACCOUNT`: Source account number

**IAM Permissions:**
- `secretsmanager:GetSecretValue` on Monoova API key secret
- `dynamodb:GetItem` on customers table
- `dynamodb:PutItem` on transactions table
- `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`

**Cost per invocation:**
- Compute: 512 MB × 2 seconds average × $0.0000133334/GB-second = $0.0000136
- Requests: $0.0000002 per request
- **Total: $0.0000138 per payout**
- **Monthly (200 payouts/day × 30): $8.28**

---

#### 2.2 Webhook Handler Lambda

**Purpose:** Process webhook notifications from Monoova (NppPaymentStatus events)

**Specifications:**
- Runtime: Python 3.12 (ARM64 Graviton2)
- Memory: 256 MB (webhooks are lightweight)
- Timeout: 10 seconds
- Concurrency: Unreserved (low volume)

**Execution Flow:**
1. Receive webhook POST from Monoova
2. Validate webhook authenticity (Authorization header check)
3. Parse webhook payload (event type, uniqueReference, status)
4. Query DynamoDB for matching transaction
5. Update transaction status (Completed, Rejected, Failed)
6. Return 200 OK immediately (within 3 seconds to avoid retry)
7. On processing error → Send to SQS DLQ

**Environment Variables:**
- `DYNAMODB_TABLE_NAME`: Name of transactions table
- `DLQ_URL`: SQS Dead Letter Queue URL
- `MONOOVA_WEBHOOK_SECRET`: Shared secret for webhook validation

**IAM Permissions:**
- `dynamodb:Query` on transactions table (by uniqueReference)
- `dynamodb:UpdateItem` on transactions table
- `sqs:SendMessage` on DLQ
- `logs:*`

**Cost per invocation:**
- Compute: 256 MB × 0.5 seconds × $0.0000133334/GB-second = $0.0000017
- **Monthly (200 webhooks/day × 30): $0.10**

---

### 3. DynamoDB

#### 3.1 Transactions Table

**Purpose:** Store payout transaction records with status tracking

**Schema:**
- **Primary Key:** `transaction_id` (String, UUID)
- **GSI:** `uniqueReference` (String) - for webhook lookups
- **GSI:** `customer_id-created_at` (Composite) - for customer history queries

**Attributes:**
```json
{
  "transaction_id": "uuid",
  "uniqueReference": "uuid-for-monoova",
  "customer_id": "customer-uuid",
  "amount": 100.00,
  "currency": "AUD",
  "status": "Pending|Completed|Rejected|Failed",
  "payout_method": "NppCreditPayId|NppCreditBankAccount",
  "monoova_transaction_id": "monoova-txn-id",
  "created_at": "2025-11-09T10:30:00Z",
  "updated_at": "2025-11-09T10:31:00Z",
  "error_message": "optional-error-details"
}
```

**Configuration:**
- Billing mode: On-Demand (pay-per-request)
- Encryption: AWS managed keys (SSE-KMS)
- Point-in-time recovery: Enabled
- TTL: 90 days (compliance requirement)

**Cost:**
- Write requests: 200/day × 2 writes (insert + update) = 400 × 30 = 12,000/month
- Read requests: 200/day × 1 read (webhook lookup) = 6,000/month
- Storage: Negligible (<1 GB)
- **Estimated: $2.00/month**

---

#### 3.2 Customers Table

**Purpose:** Store customer information and encrypted payout destinations

**Schema:**
- **Primary Key:** `customer_id` (String, UUID)

**Attributes:**
```json
{
  "customer_id": "uuid",
  "customer_name": "Full Name",
  "email": "customer@example.com",
  "payout_destinations": [
    {
      "type": "PayId",
      "payId": "encrypted-payid",
      "payIdType": "Email",
      "accountName": "encrypted-name"
    },
    {
      "type": "BankAccount",
      "bsbNumber": "encrypted-bsb",
      "accountNumber": "encrypted-account",
      "accountName": "encrypted-name"
    }
  ],
  "available_balance": 1500.00,
  "created_at": "2025-11-09T10:00:00Z"
}
```

**Configuration:**
- Billing mode: On-Demand
- Encryption: Customer managed CMK (for payout destination fields)
- Attribute-level encryption using AWS Encryption SDK

**Cost:**
- Minimal reads/writes (customer management operations)
- **Estimated: $0.50/month**

---

### 4. AWS Secrets Manager

**Purpose:** Secure storage of Monoova API key

**Configuration:**
- Secret name: `monoova/api-key`
- Secret type: String (API key only, no password needed)
- Rotation: Manual (when API key compromised)
- Encryption: AWS managed KMS key

**Cost:**
- Storage: $0.40/month per secret
- API calls: $0.05 per 10,000 calls
- Lambda caching reduces API calls (1 call per cold start)
- **Estimated: $0.45/month**

---

### 5. SQS Dead Letter Queue

**Purpose:** Capture failed webhook processing events for manual review

**Configuration:**
- Queue type: Standard
- Message retention: 14 days
- Visibility timeout: 30 seconds
- Encryption: SSE-SQS (AWS managed)

**Monitoring:**
- CloudWatch alarm when queue depth > 0
- SNS notification to operations team

**Cost:**
- Negligible (expect <1% failure rate = ~2 messages/day)
- **Estimated: $0.01/month**

---

### 6. CloudWatch

**Purpose:** Centralized logging, monitoring, and alerting

**Configuration:**

**Log Groups:**
- `/aws/lambda/payout-handler` - Retention: 7 days
- `/aws/lambda/webhook-handler` - Retention: 7 days
- `/aws/apigateway/monoova-api` - Retention: 3 days

**Alarms:**
1. **Payout Handler Errors** - Threshold: >5% error rate in 5 minutes
2. **Webhook Handler Errors** - Threshold: >3 errors in 10 minutes
3. **DLQ Depth** - Threshold: >0 messages
4. **API Gateway 5xx Errors** - Threshold: >10 in 5 minutes
5. **Lambda Throttles** - Threshold: >5 throttles

**Metrics:**
- Custom metric: Successful payout rate
- Custom metric: Average payout processing time
- Custom metric: Monoova API response time

**Cost:**
- Logs ingestion: ~1 GB/month = $0.50
- Alarms: 5 alarms × $0.10 = $0.50
- Metrics: Standard metrics (free)
- **Estimated: $1.00/month**

---

## Data Flow

### Payout Initiation Flow

```
1. Admin Web App
   └─> POST /payouts
       {
         "customer_id": "cust-123",
         "amount": 100.00,
         "payout_method": "PayId"
       }

2. API Gateway
   └─> Validates request schema
   └─> Routes to Payout Handler Lambda

3. Payout Handler Lambda
   ├─> Get customer from DynamoDB
   ├─> Get Monoova API key from Secrets Manager
   ├─> Generate uniqueReference (UUID)
   ├─> POST /financial/v2/transaction/execute to Monoova
   │   {
   │     "uniqueReference": "f484ec18-6e1f-481b-a4bf-bea515d8lk34",
   │     "totalAmount": 100,
   │     "paymentSource": "mAccount",
   │     "mAccount": { "token": "6279059726039800" },
   │     "disbursements": [
   │       {
   │         "disbursementMethod": "NppCreditPayId",
   │         "toNppCreditPayIdDetails": {
   │           "payId": "customer@example.com",
   │           "payIdType": "Email",
   │           "accountName": "Customer Name",
   │           "remitterName": "Your Business Name"
   │         },
   │         "sourceBSB": "802-985",
   │         "sourceAccountNumber": "654378888",
   │         "amount": 100
   │       }
   │     ]
   │   }
   ├─> Store transaction in DynamoDB
   │   {
   │     "transaction_id": "txn-456",
   │     "uniqueReference": "f484ec18-...",
   │     "status": "Pending",
   │     "monoova_transaction_id": "monoova-789"
   │   }
   └─> Return 202 Accepted
       {
         "transaction_id": "txn-456",
         "status": "Pending",
         "message": "Payout initiated successfully"
       }

4. Monoova API
   └─> Processes NPP payment asynchronously
   └─> Sends webhook when status changes
```

### Webhook Processing Flow

```
1. Monoova API
   └─> POST /webhooks/monoova
       Headers: { Authorization: "Bearer secret-token" }
       {
         "eventName": "NppPaymentStatus",
         "uniqueReference": "f484ec18-6e1f-481b-a4bf-bea515d8lk34",
         "status": "Payment Successful",
         "transactionId": "monoova-789",
         "timestamp": "2025-11-09T10:31:00Z"
       }

2. API Gateway
   └─> Routes to Webhook Handler Lambda

3. Webhook Handler Lambda
   ├─> Validate Authorization header
   ├─> Parse webhook payload
   ├─> Query DynamoDB by uniqueReference (GSI)
   ├─> Update transaction status
   │   {
   │     "transaction_id": "txn-456",
   │     "status": "Completed",
   │     "updated_at": "2025-11-09T10:31:00Z"
   │   }
   └─> Return 200 OK
       (If error → Send to SQS DLQ)

4. Admin Web App
   └─> Polls GET /payouts/{transaction_id} to check status
   └─> Displays "Completed" to admin
```

---

## Security Architecture

### 1. Authentication & Authorization

**API Gateway:**
- IAM authentication for internal services
- Cognito User Pool for admin web app
- API keys for Monoova webhooks (validated in Lambda)

**Monoova API:**
- HTTP Basic Auth with API key as username
- No password required
- Credentials stored in Secrets Manager

### 2. Data Encryption

**In Transit:**
- All communication via TLS 1.2+ (enforced by API Gateway)
- Monoova API requires TLS 1.2+ (no TLS 1.0/1.1)

**At Rest:**
- DynamoDB: AWS managed KMS keys (SSE-KMS)
- Customer payout destinations: Attribute-level encryption using AWS Encryption SDK
- Secrets Manager: AWS managed KMS keys
- CloudWatch Logs: Encrypted by default

**Encryption Strategy for Sensitive Data:**
```python
# Customer payout destinations are encrypted at the attribute level
from aws_encryption_sdk import EncryptionSDKClient
from aws_encryption_sdk.keyrings.aws_kms import AwsKmsKeyring

# Encrypt before storing in DynamoDB
encrypted_payid = encrypt_attribute("customer@example.com")
encrypted_bsb = encrypt_attribute("062-205")
encrypted_account = encrypt_attribute("123456789")

# Decrypt when needed for payout
decrypted_payid = decrypt_attribute(encrypted_payid)
```

### 3. IAM Least Privilege

**Payout Handler Lambda Role:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["secretsmanager:GetSecretValue"],
      "Resource": "arn:aws:secretsmanager:ap-southeast-2:*:secret:monoova/api-key-*"
    },
    {
      "Effect": "Allow",
      "Action": ["dynamodb:GetItem"],
      "Resource": "arn:aws:dynamodb:ap-southeast-2:*:table/customers"
    },
    {
      "Effect": "Allow",
      "Action": ["dynamodb:PutItem"],
      "Resource": "arn:aws:dynamodb:ap-southeast-2:*:table/transactions"
    },
    {
      "Effect": "Allow",
      "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
      "Resource": "arn:aws:logs:ap-southeast-2:*:log-group:/aws/lambda/payout-handler:*"
    }
  ]
}
```

### 4. Network Security

**VPC Configuration:**
- Lambda functions run in AWS managed VPC (no custom VPC required)
- No inbound internet access needed
- Outbound HTTPS to Monoova API via NAT Gateway (if private subnets used)

**Alternative (Recommended for Cost):**
- Lambda functions run outside VPC
- Direct internet access to Monoova API (over TLS)
- No NAT Gateway costs

---

## Resilience & Error Handling

### 1. Retry Strategy

**Monoova API Calls:**
- Transient errors (500, 502, 503, 504): Retry with exponential backoff
- Max retries: 3 attempts
- Backoff: 1s, 2s, 4s
- Jitter: ±20% to prevent thundering herd
- Use same `uniqueReference` for idempotency

**Implementation:**
```python
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry_strategy = Retry(
    total=3,
    status_forcelist=[500, 502, 503, 504],
    backoff_factor=1,
    raise_on_status=False
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)
```

### 2. Idempotency

**Unique Reference Pattern:**
- Generate UUID v4 for each payout request
- Store in DynamoDB before calling Monoova
- Use same reference on retry to prevent duplicate payouts
- Monoova deduplicates based on `uniqueReference`

### 3. Dead Letter Queue

**Failed Webhook Processing:**
- Lambda failure → Automatic retry (2 attempts)
- If still failing → Send to SQS DLQ
- CloudWatch alarm triggers SNS notification
- Operations team reviews and manually reprocesses

**DLQ Message Format:**
```json
{
  "webhook_payload": { "eventName": "NppPaymentStatus", ... },
  "error_message": "DynamoDB UpdateItem failed",
  "timestamp": "2025-11-09T10:31:00Z",
  "lambda_request_id": "abc-123"
}
```

### 4. Circuit Breaker

**Monoova API Protection:**
- If Monoova API returns >50% errors for 5 minutes
- Lambda stops processing new requests (returns 503)
- CloudWatch alarm notifies operations
- Manual reset or automatic after 10 minutes

---

## Scalability

### Current Volume: 100-200 payouts/day

**Lambda Concurrency:**
- Payout Handler: Reserved 5 concurrent executions
- Webhook Handler: Unreserved (on-demand)
- Average execution time: 2 seconds
- Peak throughput: 5 payouts/second = 18,000/hour (far exceeds current need)

### Future Scaling (10x growth to 2,000 payouts/day)

**Impact:**
- Lambda: Auto-scales to 50 concurrent executions
- DynamoDB: On-demand mode scales automatically
- API Gateway: No changes needed (1M requests/second limit)
- **Cost increase: ~10x linear scaling to $150-200/month**

**Breaking Points:**
- Monoova API rate limits (unknown - clarify with Monoova)
- DynamoDB: 40,000 RCU/WCU per table (way above need)
- Lambda: 1,000 concurrent executions (AWS account limit)

### Optimization at Scale

**Batch Processing:**
- If volume reaches >1,000 payouts/day, consider batching
- Monoova API supports multiple disbursements per request
- Reduce Lambda invocations by 80%
- Example: 10 disbursements per batch = 100 invocations vs 1,000

---

## Disaster Recovery

### Backup Strategy

**DynamoDB:**
- Point-in-time recovery: Enabled (35-day window)
- On-demand backups: Weekly full backup
- Cross-region replication: Not required (low RTO/RPO needs)

**Recovery Objectives:**
- RTO (Recovery Time Objective): 1 hour
- RPO (Recovery Point Objective): 5 minutes

### Incident Response

**Scenarios:**

1. **Monoova API Down:**
   - Lambda returns 503 to API Gateway
   - Requests queued in API Gateway (30 seconds)
   - Admin web app displays retry message
   - CloudWatch alarm notifies operations

2. **DynamoDB Unavailable:**
   - Lambda fails after 3 retries
   - Transaction not recorded
   - Return 500 to client
   - Manual reconciliation with Monoova after recovery

3. **Lambda Function Error:**
   - API Gateway retries (automatic)
   - If still failing → Return 500
   - CloudWatch alarm triggers
   - Deploy rollback version

4. **Webhook Processing Failure:**
   - Message sent to DLQ
   - Operations reviews manually
   - Update DynamoDB with correct status
   - Reconcile with Monoova transaction status API

---

## Monitoring & Observability

### Key Metrics

**Business Metrics:**
- Total payouts processed (daily, weekly, monthly)
- Success rate (Completed / Total)
- Average payout processing time (request to webhook)
- Failed payout rate by error type

**Technical Metrics:**
- Lambda invocation count, duration, errors
- API Gateway 4xx, 5xx error rates
- DynamoDB read/write throttles
- Monoova API response time (p50, p95, p99)

### Dashboards

**Operations Dashboard:**
- Real-time payout success rate (last 1 hour)
- Lambda error count (last 24 hours)
- DLQ depth (current)
- API Gateway latency (p95)

**Business Dashboard:**
- Daily payout volume
- Total payout value (AUD)
- Top customers by payout count
- Payout method breakdown (PayId vs Bank Account)

### Alerts

**Critical (PagerDuty):**
- Payout Handler error rate >10% for 5 minutes
- DLQ depth >10 messages
- Monoova API returning 500 errors

**Warning (Email):**
- Payout Handler error rate >5% for 10 minutes
- Lambda cold start rate >20%
- DynamoDB consumed capacity >80%

---

## Cost Summary

### Monthly Cost Breakdown (200 payouts/day)

| Service | Usage | Unit Cost | Monthly Cost |
|---------|-------|-----------|--------------|
| **Lambda (Payout Handler)** | 6,000 invocations × 2s × 512MB | $0.0000138/invocation | $8.28 |
| **Lambda (Webhook Handler)** | 6,000 invocations × 0.5s × 256MB | $0.0000017/invocation | $0.10 |
| **API Gateway** | 12,000 requests | $3.50/million | $0.04 |
| **DynamoDB (Transactions)** | 12,000 writes + 6,000 reads | $1.25/million writes | $2.00 |
| **DynamoDB (Customers)** | Minimal usage | On-demand | $0.50 |
| **Secrets Manager** | 1 secret + 6,000 API calls | $0.40/secret | $0.45 |
| **SQS DLQ** | <10 messages/month | $0.40/million | $0.01 |
| **CloudWatch Logs** | 1 GB ingestion | $0.50/GB | $0.50 |
| **CloudWatch Alarms** | 5 alarms | $0.10/alarm | $0.50 |
| **Data Transfer** | 10 GB outbound (Monoova API) | $0.09/GB | $0.90 |
| **Total** | | | **$13.28** |

**With AWS Free Tier:**
- Lambda: 1M requests/month + 400,000 GB-seconds free
- API Gateway: 1M requests/month free (first 12 months)
- DynamoDB: 25 GB storage + 25 RCU/WCU free
- CloudWatch: 10 custom metrics + 5 GB logs free

**Estimated Cost: $10-15/month** (with free tier benefits)

### Cost Comparison: Serverless vs Container-based

**Alternative: Lightsail Container (512 MB, $7/month):**
- Fixed cost: $7/month (running 24/7)
- Data transfer: Same as Lambda
- No API Gateway needed (direct HTTPS)
- **Total: $8-9/month**

**Analysis:**
- Lightsail is slightly cheaper at current volume
- Lambda scales better (auto-scaling, no maintenance)
- Lambda provides better resilience (automatic retries, DLQ)
- **Recommendation: Use Lambda for production-grade requirements**

---

## Deployment Architecture

### Environment Strategy

**Development:**
- Sandbox Monoova API (api.m-pay.com.au)
- Separate AWS account or namespace prefix (dev-)
- Test data only
- No customer PII

**Production:**
- Production Monoova API (api.mpay.com.au)
- Separate AWS account with strict IAM
- Real customer data
- Compliance monitoring enabled

### CI/CD Pipeline

**Tools:**
- AWS SAM or Terraform for infrastructure
- GitHub Actions or AWS CodePipeline
- Automated testing (unit + integration)

**Stages:**
1. **Build:** Package Lambda functions
2. **Test:** Run unit tests + integration tests against sandbox
3. **Deploy Dev:** Deploy to dev environment
4. **Manual Approval:** Operations team approves
5. **Deploy Prod:** Blue/green deployment to production

---

## API Gateway Configuration

### Request Validation Schema

```json
{
  "type": "object",
  "required": ["customer_id", "amount", "payout_method"],
  "properties": {
    "customer_id": {
      "type": "string",
      "pattern": "^[a-zA-Z0-9-]+$"
    },
    "amount": {
      "type": "number",
      "minimum": 0.01,
      "maximum": 1000
    },
    "payout_method": {
      "type": "string",
      "enum": ["PayId", "BankAccount"]
    }
  }
}
```

### Response Schemas

**Success (202 Accepted):**
```json
{
  "transaction_id": "txn-123",
  "status": "Pending",
  "message": "Payout initiated successfully",
  "created_at": "2025-11-09T10:30:00Z"
}
```

**Error (400 Bad Request):**
```json
{
  "error": "ValidationError",
  "message": "Amount exceeds maximum limit of $1000",
  "timestamp": "2025-11-09T10:30:00Z"
}
```

**Error (500 Internal Server Error):**
```json
{
  "error": "InternalError",
  "message": "Failed to process payout request",
  "transaction_id": "txn-123",
  "timestamp": "2025-11-09T10:30:00Z"
}
```

---

## Compliance & Governance

### Australian Privacy Act Compliance

**Data Minimization:**
- Only store necessary customer information
- Encrypt PII (bank accounts, PayIDs) at rest
- Delete customer data on request (GDPR-style right to erasure)

**Data Retention:**
- Transaction records: 7 years (financial compliance)
- CloudWatch logs: 7 days (operational needs)
- DLQ messages: 14 days (error investigation)

**Access Control:**
- Admin web app: Role-based access (RBAC)
- AWS resources: Least privilege IAM
- Audit logs: CloudTrail enabled (90-day retention)

### PCI DSS

**Assessment:** Not applicable (no card data handling)
- Fiserv handles all card transactions
- Only bank account/PayID data stored
- Not considered cardholder data

### NPP Compliance

**Managed by Monoova:**
- Monoova is licensed payment provider
- Handles NPP scheme compliance
- Your responsibility: Data accuracy and security

---

## Next Steps

### Phase 1: Infrastructure Setup (Week 1)
1. Create AWS accounts (dev + prod)
2. Deploy DynamoDB tables via Terraform
3. Create Secrets Manager secret for Monoova API key
4. Deploy Lambda functions (initial version)
5. Configure API Gateway routes

### Phase 2: Integration Testing (Week 2)
1. Test payout flow with Monoova sandbox
2. Verify webhook processing
3. Load testing (simulate 1,000 payouts/hour)
4. Security testing (penetration test)

### Phase 3: Production Deployment (Week 3)
1. Deploy to production environment
2. Migrate customer data (if applicable)
3. Configure CloudWatch alarms
4. Enable CloudTrail audit logging
5. Go-live with limited rollout (10% traffic)

### Phase 4: Monitoring & Optimization (Ongoing)
1. Monitor metrics for 2 weeks
2. Optimize Lambda memory allocation
3. Tune DynamoDB capacity (if needed)
4. Review and optimize costs

---

## Conclusion

This serverless architecture provides a cost-effective, scalable, and secure solution for processing Monoova payouts. The pay-per-use model ensures zero idle costs while maintaining production-grade resilience and observability.

**Key Benefits:**
- **Cost:** $10-15/month for 6,000 transactions (vs $50-100/month for EC2)
- **Scalability:** Auto-scales from 0 to thousands of requests
- **Resilience:** Built-in retries, DLQ, and error handling
- **Security:** Encryption at rest/transit, secrets management, least privilege IAM
- **Operational Excellence:** CloudWatch monitoring, alarms, and dashboards

**Trade-offs:**
- Cold start latency (mitigated by reserved concurrency)
- Vendor lock-in to AWS (mitigated by clean architecture)
- Debugging complexity (mitigated by structured logging)

This architecture is ready for implementation and production deployment.
