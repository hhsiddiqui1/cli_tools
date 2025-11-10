# Implementation Phases - Monoova Payments Integration

## Overview

This document outlines the step-by-step implementation plan for deploying the AWS serverless Monoova payments integration. The implementation is structured into 5 phases spanning approximately 4-5 weeks from initial setup to production deployment.

---

## Phase 1: Infrastructure Foundation (Week 1)

### Objectives
- Set up AWS accounts and environments
- Deploy core infrastructure using Terraform
- Configure security and access controls

### Tasks

#### 1.1 AWS Account Setup
**Duration:** 1 day

**Steps:**
1. Create separate AWS accounts (or use account prefixes):
   - Development environment (`monoova-dev`)
   - Production environment (`monoova-prod`)
2. Enable AWS Organizations (if multi-account)
3. Configure billing alerts:
   - Alert at $10, $25, $50 thresholds
   - SNS notification to finance team
4. Enable AWS CloudTrail for audit logging
5. Set up AWS Config for compliance monitoring

**Dependencies:** AWS account admin access

**Validation:**
- Can log in to both dev and prod accounts
- Billing alerts configured and tested
- CloudTrail logging active

---

#### 1.2 DynamoDB Tables
**Duration:** 1 day

**Tables to Create:**

**1. Transactions Table**
```hcl
# Terraform configuration
resource "aws_dynamodb_table" "transactions" {
  name         = "monoova-transactions"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "transaction_id"

  attribute {
    name = "transaction_id"
    type = "S"
  }

  attribute {
    name = "uniqueReference"
    type = "S"
  }

  attribute {
    name = "customer_id"
    type = "S"
  }

  global_secondary_index {
    name            = "UniqueReferenceIndex"
    hash_key        = "uniqueReference"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "CustomerIndex"
    hash_key        = "customer_id"
    range_key       = "created_at"
    projection_type = "ALL"
  }

  server_side_encryption {
    enabled = true
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Environment = "production"
    Application = "monoova-payouts"
  }
}
```

**2. Customers Table**
```hcl
resource "aws_dynamodb_table" "customers" {
  name         = "monoova-customers"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "customer_id"

  attribute {
    name = "customer_id"
    type = "S"
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.customer_data.arn
  }

  point_in_time_recovery {
    enabled = true
  }
}
```

**Dependencies:** AWS account setup complete

**Validation:**
```bash
aws dynamodb describe-table --table-name monoova-transactions
aws dynamodb describe-table --table-name monoova-customers
# Verify encryption and PITR enabled
```

---

#### 1.3 AWS Secrets Manager
**Duration:** 0.5 days

**Steps:**
1. Create KMS key for Secrets Manager encryption:
   ```hcl
   resource "aws_kms_key" "secrets" {
     description = "KMS key for Monoova API secrets"
     enable_key_rotation = true
   }
   ```

2. Create secret for Monoova API key:
   ```hcl
   resource "aws_secretsmanager_secret" "monoova_api_key" {
     name        = "monoova/api-key"
     description = "Monoova Payments API Key"
     kms_key_id  = aws_kms_key.secrets.id
   }
   ```

3. Manually populate secret value via AWS Console:
   ```json
   {
     "apiKey": "your-sandbox-api-key",
     "environment": "sandbox",
     "baseUrl": "https://api.m-pay.com.au"
   }
   ```

**Dependencies:** DynamoDB tables created

**Validation:**
```bash
aws secretsmanager describe-secret --secret-id monoova/api-key
aws secretsmanager get-secret-value --secret-id monoova/api-key
```

---

#### 1.4 IAM Roles for Lambda
**Duration:** 0.5 days

**Roles to Create:**

**1. Payout Handler Lambda Role**
```hcl
resource "aws_iam_role" "payout_handler" {
  name = "monoova-payout-handler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "payout_handler_policy" {
  name = "monoova-payout-handler-policy"
  role = aws_iam_role.payout_handler.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["secretsmanager:GetSecretValue"]
        Resource = aws_secretsmanager_secret.monoova_api_key.arn
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem"
        ]
        Resource = [
          aws_dynamodb_table.customers.arn,
          aws_dynamodb_table.transactions.arn
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt"
        ]
        Resource = aws_kms_key.customer_data.arn
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:log-group:/aws/lambda/monoova-payout-handler:*"
      }
    ]
  })
}
```

**2. Webhook Handler Lambda Role**
```hcl
resource "aws_iam_role" "webhook_handler" {
  name = "monoova-webhook-handler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "webhook_handler_policy" {
  name = "monoova-webhook-handler-policy"
  role = aws_iam_role.webhook_handler.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:Query",
          "dynamodb:UpdateItem"
        ]
        Resource = [
          aws_dynamodb_table.transactions.arn,
          "${aws_dynamodb_table.transactions.arn}/index/UniqueReferenceIndex"
        ]
      },
      {
        Effect = "Allow"
        Action = ["sqs:SendMessage"]
        Resource = aws_sqs_queue.webhook_dlq.arn
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:log-group:/aws/lambda/monoova-webhook-handler:*"
      }
    ]
  })
}
```

**Dependencies:** DynamoDB and Secrets Manager created

**Validation:**
```bash
aws iam get-role --role-name monoova-payout-handler-role
aws iam get-role-policy --role-name monoova-payout-handler-role --policy-name monoova-payout-handler-policy
```

---

#### 1.5 SQS Dead Letter Queue
**Duration:** 0.5 days

**Steps:**
```hcl
resource "aws_sqs_queue" "webhook_dlq" {
  name                       = "monoova-webhook-dlq"
  message_retention_seconds  = 1209600  # 14 days
  visibility_timeout_seconds = 30

  sqs_managed_sse_enabled = true

  tags = {
    Environment = "production"
    Purpose     = "Webhook failure capture"
  }
}
```

**Dependencies:** None

**Validation:**
```bash
aws sqs get-queue-attributes --queue-url <queue-url> --attribute-names All
```

---

#### 1.6 CloudWatch Log Groups and Alarms
**Duration:** 0.5 days

**Log Groups:**
```hcl
resource "aws_cloudwatch_log_group" "payout_handler" {
  name              = "/aws/lambda/monoova-payout-handler"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_group" "webhook_handler" {
  name              = "/aws/lambda/monoova-webhook-handler"
  retention_in_days = 7
}
```

**Alarms:**
```hcl
# Alarm 1: Payout Handler Error Rate
resource "aws_cloudwatch_metric_alarm" "payout_handler_errors" {
  alarm_name          = "monoova-payout-handler-high-error-rate"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300  # 5 minutes
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "Payout handler error rate exceeded threshold"

  dimensions = {
    FunctionName = "monoova-payout-handler"
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
}

# Alarm 2: DLQ Depth
resource "aws_cloudwatch_metric_alarm" "dlq_depth" {
  alarm_name          = "monoova-webhook-dlq-not-empty"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "ApproximateNumberOfMessagesVisible"
  namespace           = "AWS/SQS"
  period              = 60
  statistic           = "Sum"
  threshold           = 0
  alarm_description   = "Webhook DLQ has messages - requires investigation"

  dimensions = {
    QueueName = aws_sqs_queue.webhook_dlq.name
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
}
```

**SNS Topic for Alerts:**
```hcl
resource "aws_sns_topic" "alerts" {
  name = "monoova-alerts"
}

resource "aws_sns_topic_subscription" "alerts_email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = "ops-team@yourcompany.com"
}
```

**Dependencies:** Lambda functions (will be created in Phase 2)

**Validation:**
```bash
aws cloudwatch describe-alarms --alarm-names monoova-payout-handler-high-error-rate
aws sns list-subscriptions-by-topic --topic-arn <topic-arn>
```

---

### Phase 1 Deliverables

- [ ] AWS accounts configured with billing alerts
- [ ] DynamoDB tables deployed (transactions, customers)
- [ ] Secrets Manager secret created (Monoova API key)
- [ ] IAM roles created for Lambda functions
- [ ] SQS DLQ deployed
- [ ] CloudWatch log groups and alarms configured
- [ ] SNS topic for alerts with email subscription
- [ ] All infrastructure deployed via Terraform (version controlled)

### Phase 1 Sign-off Criteria

1. All Terraform applies successfully without errors
2. DynamoDB tables are accessible and encrypted
3. Secrets Manager secret can be retrieved by IAM role
4. CloudWatch alarms can be triggered manually (test alarm)
5. SNS alert email received successfully

---

## Phase 2: Lambda Function Development (Week 2-3)

### Objectives
- Develop and unit test Lambda functions
- Integrate with Monoova sandbox API
- Implement error handling and retry logic

### Tasks

#### 2.1 Payout Handler Lambda Development
**Duration:** 3 days

**File Structure:**
```
lambda/payout_handler/
   handler.py           # Main Lambda handler
   monoova_client.py    # Monoova API client with retry logic
   validators.py        # Input validation functions
   requirements.txt     # Python dependencies
   tests/
       test_handler.py
       test_monoova_client.py
```

**Key Implementation Details:**

**1. Requirements (`requirements.txt`):**
```
boto3==1.34.0
requests==2.31.0
aws-encryption-sdk==3.1.1
```

**2. Main Handler (`handler.py`):**
- Input validation (amount, customer_id, payout_method)
- Retrieve customer from DynamoDB
- Decrypt payout destination (PayID or bank account)
- Generate UUID v4 for uniqueReference
- Call Monoova API via client
- Store transaction in DynamoDB
- Return 202 Accepted response

**3. Monoova Client (`monoova_client.py`):**
- HTTP client with retry logic (exponential backoff)
- Correct API payload structure (from validation_report.md)
- Error handling for 4xx and 5xx responses
- Idempotency support (same uniqueReference on retry)

**Dependencies:** Phase 1 infrastructure complete

**Validation:**
```bash
# Unit tests
cd lambda/payout_handler
python -m pytest tests/ -v

# Integration test with Monoova sandbox
python -m pytest tests/integration/ -v
```

**Acceptance Criteria:**
- Unit tests pass with >90% code coverage
- Successfully calls Monoova sandbox API
- Handles API errors gracefully
- Stores transaction in DynamoDB correctly
- Completes in <5 seconds (excluding Monoova API latency)

---

#### 2.2 Webhook Handler Lambda Development
**Duration:** 2 days

**File Structure:**
```
lambda/webhook_handler/
   handler.py           # Main Lambda handler
   validators.py        # Webhook signature validation
   requirements.txt     # Python dependencies
   tests/
       test_handler.py
```

**Key Implementation Details:**

**1. Main Handler (`handler.py`):**
- Parse webhook payload
- Validate webhook authenticity (Authorization header)
- Query DynamoDB by uniqueReference (using GSI)
- Update transaction status
- Handle duplicate webhooks (idempotency)
- Return 200 OK within 3 seconds

**2. Error Handling:**
- DynamoDB query failures ’ Retry 3 times
- Update failures ’ Send to DLQ
- Unknown webhook events ’ Log and return 200

**Dependencies:** Phase 1 infrastructure complete

**Validation:**
```bash
# Unit tests
cd lambda/webhook_handler
python -m pytest tests/ -v

# Simulate webhook locally
curl -X POST http://localhost:9000/2015-03-31/functions/function/invocations \
  -d '{"eventName": "NppPaymentStatus", "uniqueReference": "test-uuid", "status": "Payment Successful"}'
```

**Acceptance Criteria:**
- Unit tests pass with >90% code coverage
- Correctly updates transaction status
- Handles duplicate webhooks without error
- Completes in <3 seconds
- Failed events sent to DLQ

---

#### 2.3 Shared Utilities Development
**Duration:** 1 day

**File Structure:**
```
lambda/shared/
   crypto.py            # Encryption/decryption utilities
   models.py            # Data models (Pydantic)
   exceptions.py        # Custom exceptions
   tests/
       test_crypto.py
       test_models.py
```

**Key Utilities:**

**1. Encryption (`crypto.py`):**
```python
# AWS Encryption SDK wrapper
from aws_encryption_sdk import EncryptionSDKClient, CommitmentPolicy
from aws_encryption_sdk.keyrings.aws_kms import AwsKmsKeyring

def encrypt_field(plaintext: str, kms_key_id: str) -> str:
    """Encrypt sensitive field using AWS KMS"""
    pass

def decrypt_field(ciphertext: str, kms_key_id: str) -> str:
    """Decrypt sensitive field using AWS KMS"""
    pass
```

**2. Data Models (`models.py`):**
```python
from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime

class PayoutRequest(BaseModel):
    customer_id: str = Field(..., pattern=r'^cust-[a-f0-9-]+$')
    amount: float = Field(..., gt=0.01, le=1000.0)
    payout_method: Literal["PayId", "BankAccount"]
    description: Optional[str] = Field(None, max_length=200)

class Transaction(BaseModel):
    transaction_id: str
    uniqueReference: str
    customer_id: str
    amount: float
    status: Literal["Pending", "Completed", "Rejected", "Failed"]
    created_at: datetime
```

**Dependencies:** None (can be developed in parallel)

**Validation:**
```bash
cd lambda/shared
python -m pytest tests/ -v
```

---

#### 2.4 Lambda Deployment Packages
**Duration:** 1 day

**Steps:**

1. **Package Lambda functions:**
```bash
# Payout Handler
cd lambda/payout_handler
pip install -r requirements.txt -t .
zip -r payout_handler.zip . -x "tests/*" "__pycache__/*" "*.pyc"

# Webhook Handler
cd lambda/webhook_handler
pip install -r requirements.txt -t .
zip -r webhook_handler.zip . -x "tests/*" "__pycache__/*" "*.pyc"
```

2. **Deploy via Terraform:**
```hcl
resource "aws_lambda_function" "payout_handler" {
  filename         = "lambda/payout_handler/payout_handler.zip"
  function_name    = "monoova-payout-handler"
  role             = aws_iam_role.payout_handler.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  architectures    = ["arm64"]
  memory_size      = 512
  timeout          = 30
  source_code_hash = filebase64sha256("lambda/payout_handler/payout_handler.zip")

  environment {
    variables = {
      MONOOVA_API_SECRET_ARN = aws_secretsmanager_secret.monoova_api_key.arn
      DYNAMODB_TABLE_TRANSACTIONS = aws_dynamodb_table.transactions.name
      DYNAMODB_TABLE_CUSTOMERS = aws_dynamodb_table.customers.name
      MONOOVA_MACCOUNT_TOKEN = "6279059726039800"  # Your mAccount number
      MONOOVA_SOURCE_BSB = "802-985"
      MONOOVA_SOURCE_ACCOUNT = "654378888"
      REMITTER_NAME = "Your Business Name"
    }
  }

  dead_letter_config {
    target_arn = aws_sqs_queue.webhook_dlq.arn
  }
}
```

3. **Test deployed functions:**
```bash
aws lambda invoke --function-name monoova-payout-handler \
  --payload '{"customer_id":"test-cust","amount":100}' \
  response.json

cat response.json
```

**Dependencies:** Lambda code developed and tested locally

**Validation:**
- Lambda functions deploy without errors
- Environment variables set correctly
- IAM roles attached successfully
- Test invocations return expected responses

---

### Phase 2 Deliverables

- [ ] Payout handler Lambda function developed and tested
- [ ] Webhook handler Lambda function developed and tested
- [ ] Shared utilities library created
- [ ] Unit test coverage >90%
- [ ] Integration tests pass with Monoova sandbox
- [ ] Lambda deployment packages created
- [ ] Functions deployed to AWS dev environment
- [ ] Manual smoke tests pass

### Phase 2 Sign-off Criteria

1. All unit tests pass
2. Integration tests successfully call Monoova sandbox API
3. Lambda functions deploy without errors
4. Test payout completes end-to-end in dev environment
5. Webhook processing updates DynamoDB correctly

---

## Phase 3: API Gateway Configuration (Week 3)

### Objectives
- Configure API Gateway REST API
- Set up authentication and authorization
- Enable CORS for web application
- Deploy API to dev and prod stages

### Tasks

#### 3.1 API Gateway REST API Creation
**Duration:** 1 day

**Terraform Configuration:**
```hcl
resource "aws_api_gateway_rest_api" "monoova_api" {
  name        = "monoova-payouts-api"
  description = "API for Monoova payment processing"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

# /payouts resource
resource "aws_api_gateway_resource" "payouts" {
  rest_api_id = aws_api_gateway_rest_api.monoova_api.id
  parent_id   = aws_api_gateway_rest_api.monoova_api.root_resource_id
  path_part   = "payouts"
}

# POST /payouts method
resource "aws_api_gateway_method" "create_payout" {
  rest_api_id   = aws_api_gateway_rest_api.monoova_api.id
  resource_id   = aws_api_gateway_resource.payouts.id
  http_method   = "POST"
  authorization = "AWS_IAM"  # Or "COGNITO_USER_POOLS"

  request_validator_id = aws_api_gateway_request_validator.body_validator.id
}

# Request validator
resource "aws_api_gateway_request_validator" "body_validator" {
  name                        = "body-validator"
  rest_api_id                 = aws_api_gateway_rest_api.monoova_api.id
  validate_request_body       = true
  validate_request_parameters = false
}

# Lambda integration
resource "aws_api_gateway_integration" "payout_handler_integration" {
  rest_api_id             = aws_api_gateway_rest_api.monoova_api.id
  resource_id             = aws_api_gateway_resource.payouts.id
  http_method             = aws_api_gateway_method.create_payout.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.payout_handler.invoke_arn
}

# Lambda permission for API Gateway
resource "aws_lambda_permission" "api_gateway_invoke_payout" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.payout_handler.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.monoova_api.execution_arn}/*"
}
```

**Dependencies:** Lambda functions deployed

**Validation:**
```bash
aws apigateway get-rest-apis
aws apigateway get-resources --rest-api-id <api-id>
```

---

#### 3.2 Webhook Endpoint Configuration
**Duration:** 0.5 days

**Steps:**
```hcl
# /webhooks resource
resource "aws_api_gateway_resource" "webhooks" {
  rest_api_id = aws_api_gateway_rest_api.monoova_api.id
  parent_id   = aws_api_gateway_rest_api.monoova_api.root_resource_id
  path_part   = "webhooks"
}

# /webhooks/monoova resource
resource "aws_api_gateway_resource" "monoova_webhook" {
  rest_api_id = aws_api_gateway_rest_api.monoova_api.id
  parent_id   = aws_api_gateway_resource.webhooks.id
  path_part   = "monoova"
}

# POST /webhooks/monoova method
resource "aws_api_gateway_method" "receive_webhook" {
  rest_api_id   = aws_api_gateway_rest_api.monoova_api.id
  resource_id   = aws_api_gateway_resource.monoova_webhook.id
  http_method   = "POST"
  authorization = "NONE"  # Validate in Lambda using Authorization header

  request_parameters = {
    "method.request.header.Authorization" = true
  }
}

# Lambda integration
resource "aws_api_gateway_integration" "webhook_handler_integration" {
  rest_api_id             = aws_api_gateway_rest_api.monoova_api.id
  resource_id             = aws_api_gateway_resource.monoova_webhook.id
  http_method             = aws_api_gateway_method.receive_webhook.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.webhook_handler.invoke_arn
}
```

**Dependencies:** API Gateway created, webhook handler Lambda deployed

**Validation:**
```bash
# Test webhook endpoint
curl -X POST https://<api-id>.execute-api.ap-southeast-2.amazonaws.com/dev/webhooks/monoova \
  -H "Authorization: Bearer test-secret" \
  -H "Content-Type: application/json" \
  -d '{"eventName":"NppPaymentStatus","uniqueReference":"test","status":"Payment Successful"}'
```

---

#### 3.3 CORS Configuration
**Duration:** 0.5 days

**Steps:**
```hcl
# Enable CORS for /payouts endpoint
resource "aws_api_gateway_method" "payouts_options" {
  rest_api_id   = aws_api_gateway_rest_api.monoova_api.id
  resource_id   = aws_api_gateway_resource.payouts.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "payouts_options" {
  rest_api_id = aws_api_gateway_rest_api.monoova_api.id
  resource_id = aws_api_gateway_resource.payouts.id
  http_method = aws_api_gateway_method.payouts_options.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "payouts_options_response" {
  rest_api_id = aws_api_gateway_rest_api.monoova_api.id
  resource_id = aws_api_gateway_resource.payouts.id
  http_method = aws_api_gateway_method.payouts_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "payouts_options_response" {
  rest_api_id = aws_api_gateway_rest_api.monoova_api.id
  resource_id = aws_api_gateway_resource.payouts.id
  http_method = aws_api_gateway_method.payouts_options.http_method
  status_code = aws_api_gateway_method_response.payouts_options_response.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,Authorization'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,POST,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"  # Change to your domain in production
  }
}
```

**Dependencies:** API Gateway endpoints created

**Validation:**
```bash
# Test OPTIONS preflight
curl -X OPTIONS https://<api-id>.execute-api.ap-southeast-2.amazonaws.com/dev/payouts \
  -H "Origin: https://yourapp.com" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

---

#### 3.4 API Deployment to Dev and Prod Stages
**Duration:** 0.5 days

**Steps:**
```hcl
# Dev stage
resource "aws_api_gateway_deployment" "dev" {
  rest_api_id = aws_api_gateway_rest_api.monoova_api.id
  stage_name  = "dev"

  depends_on = [
    aws_api_gateway_integration.payout_handler_integration,
    aws_api_gateway_integration.webhook_handler_integration
  ]
}

# Prod stage
resource "aws_api_gateway_deployment" "prod" {
  rest_api_id = aws_api_gateway_rest_api.monoova_api.id
  stage_name  = "prod"

  depends_on = [
    aws_api_gateway_integration.payout_handler_integration,
    aws_api_gateway_integration.webhook_handler_integration
  ]
}

# CloudWatch logging for prod
resource "aws_api_gateway_method_settings" "prod_logging" {
  rest_api_id = aws_api_gateway_rest_api.monoova_api.id
  stage_name  = aws_api_gateway_deployment.prod.stage_name
  method_path = "*/*"

  settings {
    logging_level      = "INFO"
    data_trace_enabled = false
    metrics_enabled    = true
  }
}
```

**Dependencies:** All API Gateway resources configured

**Validation:**
```bash
# Get deployment URLs
aws apigateway get-stages --rest-api-id <api-id>

# Test dev endpoint
curl -X POST https://<api-id>.execute-api.ap-southeast-2.amazonaws.com/dev/payouts \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"test","amount":100,"payout_method":"PayId"}'

# Test prod endpoint (after phase 5)
curl -X POST https://<api-id>.execute-api.ap-southeast-2.amazonaws.com/prod/payouts \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"test","amount":100,"payout_method":"PayId"}'
```

---

### Phase 3 Deliverables

- [ ] API Gateway REST API created
- [ ] POST /payouts endpoint configured
- [ ] POST /webhooks/monoova endpoint configured
- [ ] CORS enabled for web app
- [ ] Request validation configured
- [ ] CloudWatch logging enabled
- [ ] Dev and prod stages deployed
- [ ] API documentation generated (Swagger/OpenAPI)

### Phase 3 Sign-off Criteria

1. API endpoints accessible via HTTPS
2. Lambda functions invoked successfully via API Gateway
3. CORS preflight requests work correctly
4. Request validation rejects invalid payloads
5. CloudWatch logs show API Gateway activity

---

## Phase 4: Testing & Validation (Week 4)

### Objectives
- End-to-end testing with Monoova sandbox
- Load testing and performance validation
- Security testing
- Webhook delivery testing

### Tasks

#### 4.1 End-to-End Testing
**Duration:** 2 days

**Test Scenarios:**

**1. Successful Payout Flow:**
```python
# Test script: tests/e2e/test_payout_flow.py
import requests
import time

# Step 1: Create payout
response = requests.post(
    "https://<api-id>.execute-api.ap-southeast-2.amazonaws.com/dev/payouts",
    json={
        "customer_id": "test-cust-001",
        "amount": 100.00,
        "payout_method": "PayId"
    }
)
assert response.status_code == 202
transaction_id = response.json()["transaction_id"]

# Step 2: Wait for webhook (simulate)
time.sleep(10)

# Step 3: Check status
status_response = requests.get(
    f"https://<api-id>.execute-api.ap-southeast-2.amazonaws.com/dev/payouts/{transaction_id}"
)
assert status_response.json()["status"] == "Completed"
```

**2. Failed Payout (Insufficient Balance):**
- Test with invalid customer_id
- Verify error response
- Confirm no transaction recorded

**3. Webhook Processing:**
- Manually trigger webhook to dev endpoint
- Verify DynamoDB update
- Check CloudWatch logs

**4. Idempotency:**
- Submit same payout request twice with identical data
- Verify only one Monoova transaction created
- Test retry with same uniqueReference

**Dependencies:** All Phase 1-3 infrastructure deployed

**Validation:**
```bash
cd tests/e2e
python -m pytest test_payout_flow.py -v -s
```

---

#### 4.2 Load Testing
**Duration:** 1 day

**Tool:** Locust or Apache JMeter

**Test Configuration:**
```python
# locustfile.py
from locust import HttpUser, task, between

class PayoutUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def create_payout(self):
        self.client.post("/payouts", json={
            "customer_id": f"test-cust-{self.environment.stats.num_requests % 100}",
            "amount": 50.00,
            "payout_method": "PayId"
        })
```

**Load Test Scenarios:**

**1. Normal Load (200 payouts/day):**
- 10 concurrent users
- Duration: 10 minutes
- Expected: 0% error rate, <2s response time

**2. Peak Load (10x normal):**
- 100 concurrent users
- Duration: 5 minutes
- Expected: <5% error rate, <5s response time

**3. Burst Load:**
- 0 ’ 200 users in 1 minute
- Duration: 5 minutes
- Expected: Lambda auto-scales, <10% error rate

**Dependencies:** Dev environment stable

**Validation:**
```bash
locust -f locustfile.py --host https://<api-id>.execute-api.ap-southeast-2.amazonaws.com/dev
# Open http://localhost:8089 for monitoring
```

**Success Criteria:**
- P95 response time <3 seconds
- Error rate <5%
- No Lambda throttling errors
- DynamoDB performance stable

---

#### 4.3 Security Testing
**Duration:** 1 day

**Test Cases:**

**1. Authentication:**
- Test API Gateway without credentials (expect 403)
- Test with invalid API key (expect 401)
- Test with expired token (if using Cognito)

**2. Input Validation:**
- SQL injection attempts in customer_id
- XSS attempts in description field
- Negative amounts
- Amounts exceeding $1000 limit

**3. Webhook Security:**
- Test webhook without Authorization header (expect 401)
- Test with invalid webhook signature
- Test replay attack (same webhook twice)

**4. Data Encryption:**
- Verify DynamoDB data is encrypted at rest
- Verify customer payout destinations are encrypted (base64 check)
- Verify TLS in transit (check certificate)

**Dependencies:** All Phase 1-3 infrastructure deployed

**Validation:**
```bash
# Run security tests
cd tests/security
python -m pytest test_security.py -v
```

**Success Criteria:**
- All authentication tests pass
- Input validation blocks malicious payloads
- Webhook security prevents unauthorized access
- Data encryption verified

---

#### 4.4 Webhook Delivery Testing
**Duration:** 1 day

**Test Scenarios:**

**1. Normal Webhook Delivery:**
- Create payout in Monoova sandbox
- Wait for NppPaymentStatus webhook
- Verify DynamoDB updated correctly

**2. Webhook Retry (Simulate Failure):**
- Configure webhook handler to return 500
- Verify Monoova retries after 30 seconds
- Restore handler, verify update succeeds

**3. Duplicate Webhook:**
- Send same webhook twice
- Verify idempotency (no duplicate updates)

**4. Unknown Webhook Event:**
- Send webhook with unknown eventName
- Verify handler logs and returns 200

**5. DLQ Testing:**
- Force webhook handler to fail (remove DynamoDB table temporarily)
- Verify message sent to DLQ
- Verify CloudWatch alarm triggers

**Dependencies:** Monoova sandbox webhook configured

**Validation:**
```bash
# Manually trigger webhook
curl -X POST https://<api-id>.execute-api.ap-southeast-2.amazonaws.com/dev/webhooks/monoova \
  -H "Authorization: Bearer <webhook-secret>" \
  -H "Content-Type: application/json" \
  -d @tests/fixtures/webhook_successful.json
```

---

### Phase 4 Deliverables

- [ ] End-to-end test suite passing
- [ ] Load test results documented
- [ ] Security test report completed
- [ ] Webhook delivery tests passing
- [ ] Performance baseline established
- [ ] Test coverage report generated

### Phase 4 Sign-off Criteria

1. All E2E tests pass in dev environment
2. Load tests show system can handle 10x current volume
3. Security tests pass with no critical vulnerabilities
4. Webhook processing works reliably
5. DLQ captures failed events correctly

---

## Phase 5: Production Deployment (Week 5)

### Objectives
- Deploy to production environment
- Configure Monoova production webhook URL
- Monitor for 48 hours
- Gradual traffic migration (if applicable)

### Tasks

#### 5.1 Production Environment Setup
**Duration:** 1 day

**Steps:**

1. **Update Secrets Manager:**
```bash
# Replace sandbox API key with production key
aws secretsmanager put-secret-value \
  --secret-id monoova/api-key \
  --secret-string '{"apiKey":"prod-key","environment":"production","baseUrl":"https://api.mpay.com.au"}'
```

2. **Update Environment Variables:**
```hcl
# Update Lambda environment variables in Terraform
environment {
  variables = {
    MONOOVA_API_SECRET_ARN = aws_secretsmanager_secret.monoova_api_key.arn
    MONOOVA_MACCOUNT_TOKEN = "YOUR_PROD_MACCOUNT_TOKEN"
    # ... other variables
  }
}
```

3. **Deploy Production Infrastructure:**
```bash
cd infrastructure/terraform
terraform workspace select prod
terraform plan
terraform apply
```

4. **Verify Production Deployment:**
```bash
# Test health check endpoint (if implemented)
curl https://<prod-api-id>.execute-api.ap-southeast-2.amazonaws.com/prod/health
```

**Dependencies:** Phase 4 testing complete

**Validation:**
- Production Lambda functions deployed
- Production API Gateway accessible
- Secrets Manager contains production credentials
- All CloudWatch alarms active

---

#### 5.2 Monoova Webhook Configuration
**Duration:** 0.5 days

**Steps:**

1. **Register Webhook URL with Monoova:**
   - Contact Monoova support or use Monoova portal
   - Provide production webhook URL:
     ```
     https://<prod-api-id>.execute-api.ap-southeast-2.amazonaws.com/prod/webhooks/monoova
     ```
   - Specify events to receive:
     - `NppPaymentStatus` (required)
     - `NPPReceivePayment` (optional)
     - `DirectEntryDishonour` (optional)

2. **Configure Webhook Authentication:**
   - Generate webhook secret token
   - Store in environment variable: `MONOOVA_WEBHOOK_SECRET`
   - Provide to Monoova for Authorization header

3. **Test Webhook Delivery:**
   - Request test webhook from Monoova
   - Verify received in CloudWatch logs
   - Confirm DynamoDB update (if test transaction provided)

**Dependencies:** Production environment deployed

**Validation:**
```bash
# Check CloudWatch logs for webhook receipt
aws logs filter-log-events \
  --log-group-name /aws/lambda/monoova-webhook-handler \
  --filter-pattern "NppPaymentStatus" \
  --start-time $(date -d '10 minutes ago' +%s)000
```

---

#### 5.3 Smoke Testing in Production
**Duration:** 0.5 days

**Test Cases:**

**1. Test Payout (Small Amount):**
```bash
# Create test payout for $0.01 to internal account
curl -X POST https://<prod-api-id>.execute-api.ap-southeast-2.amazonaws.com/prod/payouts \
  -H "Authorization: Bearer <prod-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "internal-test-account",
    "amount": 0.01,
    "payout_method": "PayId"
  }'
```

**2. Verify Transaction Flow:**
- Check transaction created in DynamoDB
- Monitor CloudWatch logs for Monoova API call
- Wait for webhook (1-2 minutes)
- Verify status updated to "Completed"
- Confirm funds received in test account

**3. Test Error Scenarios:**
- Invalid customer_id (expect 400)
- Excessive amount (expect 400)
- Missing required fields (expect 400)

**Dependencies:** Webhook configured, production access granted

**Validation:**
- All smoke tests pass
- No errors in CloudWatch logs
- Funds received successfully in test account

---

#### 5.4 Monitoring and Observability
**Duration:** 1 day (ongoing)

**Setup CloudWatch Dashboard:**
```hcl
resource "aws_cloudwatch_dashboard" "monoova_prod" {
  dashboard_name = "monoova-production"

  dashboard_body = jsonencode({
    widgets = [
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/Lambda", "Invocations", { stat = "Sum", label = "Payout Handler Invocations" }],
            [".", "Errors", { stat = "Sum", label = "Payout Handler Errors" }],
            [".", "Duration", { stat = "Average", label = "Avg Duration (ms)" }]
          ]
          period = 300
          region = "ap-southeast-2"
          title  = "Payout Handler Metrics"
        }
      },
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/DynamoDB", "ConsumedReadCapacityUnits", { stat = "Sum" }],
            [".", "ConsumedWriteCapacityUnits", { stat = "Sum" }]
          ]
          period = 300
          region = "ap-southeast-2"
          title  = "DynamoDB Capacity"
        }
      },
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/SQS", "ApproximateNumberOfMessagesVisible", { stat = "Average", label = "DLQ Depth" }]
          ]
          period = 60
          region = "ap-southeast-2"
          title  = "Dead Letter Queue"
        }
      }
    ]
  })
}
```

**Configure Additional Alarms:**
```hcl
# Daily payout volume alarm (anomaly detection)
resource "aws_cloudwatch_metric_alarm" "payout_volume_anomaly" {
  alarm_name          = "monoova-payout-volume-anomaly"
  comparison_operator = "LessThanLowerOrGreaterThanUpperThreshold"
  evaluation_periods  = 2
  threshold_metric_id = "ad1"

  metric_query {
    id          = "m1"
    return_data = true

    metric {
      metric_name = "Invocations"
      namespace   = "AWS/Lambda"
      period      = 3600  # 1 hour
      stat        = "Sum"

      dimensions = {
        FunctionName = "monoova-payout-handler"
      }
    }
  }

  metric_query {
    id          = "ad1"
    expression  = "ANOMALY_DETECTION_BAND(m1, 2)"
    label       = "Invocations (expected)"
    return_data = true
  }
}
```

**Dependencies:** Production deployment complete

**Validation:**
- CloudWatch dashboard displays all metrics
- Alarms configured and in "OK" state
- SNS notifications delivered successfully

---

#### 5.5 Runbook and Documentation
**Duration:** 1 day

**Create Operations Runbook:**

**1. Common Issues and Resolutions**

**Issue: High Error Rate in Payout Handler**
- **Symptoms:** CloudWatch alarm "monoova-payout-handler-high-error-rate" triggered
- **Investigation:**
  1. Check CloudWatch logs for error messages
  2. Verify Monoova API status (check Monoova status page)
  3. Check Secrets Manager secret is accessible
  4. Verify DynamoDB tables are available
- **Resolution:**
  - If Monoova API down: Wait for recovery, inform users
  - If secret expired: Rotate API key in Secrets Manager
  - If DynamoDB issue: Check AWS Service Health Dashboard
  - If code bug: Deploy rollback version via Terraform

**Issue: Webhooks Not Processing**
- **Symptoms:** DLQ depth > 0, transactions stuck in "Pending" status
- **Investigation:**
  1. Check CloudWatch logs for webhook handler errors
  2. Verify webhook URL configured correctly in Monoova
  3. Check webhook authentication (Authorization header)
- **Resolution:**
  - Manually process DLQ messages
  - Update transaction statuses from Monoova transaction status API
  - Fix webhook handler bug and redeploy

**Issue: DynamoDB Throttling**
- **Symptoms:** DynamoDB throttle errors in CloudWatch logs
- **Investigation:**
  1. Check DynamoDB consumed capacity metrics
  2. Verify on-demand mode enabled
  3. Check for hot partition key
- **Resolution:**
  - If on-demand throttling: Contact AWS support (unlikely)
  - If provisioned mode: Increase RCU/WCU
  - If hot partition: Redesign partition key strategy

**2. Monitoring Checklist (Daily)**
- [ ] Check CloudWatch dashboard for anomalies
- [ ] Review DLQ for failed events
- [ ] Verify payout success rate >95%
- [ ] Check AWS costs (compare to budget)
- [ ] Review CloudWatch logs for warnings

**3. Emergency Contacts**
- AWS Support: [support link]
- Monoova Support: support@monoova.com
- On-call engineer: [phone/email]
- Operations lead: [phone/email]

**Dependencies:** Production deployment complete

**Validation:**
- Runbook reviewed by operations team
- Emergency contacts verified
- All team members have access to AWS console

---

### Phase 5 Deliverables

- [ ] Production infrastructure deployed
- [ ] Monoova production webhook configured
- [ ] Smoke tests passing in production
- [ ] CloudWatch dashboard and alarms configured
- [ ] Operations runbook created
- [ ] Team trained on monitoring and incident response
- [ ] Production go-live approved

### Phase 5 Sign-off Criteria

1. Production smoke tests pass successfully
2. Webhook delivery confirmed from Monoova
3. CloudWatch dashboard shows healthy metrics
4. All alarms in "OK" state
5. Operations team trained and ready
6. Go-live approval from stakeholders

---

## Post-Deployment (Ongoing)

### Week 1-2 Post-Launch: Intensive Monitoring

**Daily Tasks:**
1. Review CloudWatch metrics and logs
2. Check DLQ for any failed events
3. Verify payout success rate
4. Monitor AWS costs
5. Review customer feedback (if any)

**Weekly Tasks:**
1. Generate payout summary report
2. Review and optimize Lambda memory allocation
3. Analyze DynamoDB performance
4. Review security logs in CloudTrail
5. Update documentation based on lessons learned

---

### Ongoing Maintenance

**Monthly:**
- Review and optimize AWS costs
- Check for AWS service updates/deprecations
- Update Lambda runtime if needed (Python version)
- Review and rotate API keys (quarterly)

**Quarterly:**
- Security audit (IAM policies, encryption)
- Disaster recovery drill (restore from backup)
- Capacity planning (forecast growth)
- Performance optimization review

**Annually:**
- Comprehensive security review
- Compliance audit (Privacy Act, data retention)
- Architecture review (consider new AWS services)
- Cost optimization analysis

---

## Success Metrics

### Technical Metrics
- **Uptime:** >99.9% (measured by CloudWatch alarms)
- **Error Rate:** <1% (failed payouts / total payouts)
- **Response Time:** P95 <3 seconds (API Gateway to response)
- **Webhook Processing:** <5 seconds (webhook receipt to DynamoDB update)

### Business Metrics
- **Cost per Transaction:** <$0.05 (AWS costs / total payouts)
- **Payout Success Rate:** >98% (completed / total initiated)
- **Time to Completion:** <2 minutes average (payout initiated to funds received)

### Operational Metrics
- **Mean Time to Detection (MTTD):** <5 minutes (error to alarm)
- **Mean Time to Resolution (MTTR):** <30 minutes (alarm to fix)
- **False Alarm Rate:** <5% (false alarms / total alarms)

---

## Rollback Plan

### Scenario: Critical Issue in Production

**Steps:**

1. **Immediate:** Disable API Gateway endpoint (set throttle to 0)
2. **Notify:** Send alert to operations team and stakeholders
3. **Investigate:** Review CloudWatch logs to identify root cause
4. **Rollback Lambda Functions:**
   ```bash
   # Revert to previous version
   aws lambda update-function-code \
     --function-name monoova-payout-handler \
     --s3-bucket lambda-deployments \
     --s3-key payout_handler_v1.0.0.zip
   ```
5. **Verify:** Test with smoke tests
6. **Re-enable:** Restore API Gateway throttle limits
7. **Post-Mortem:** Document root cause and prevention measures

### Scenario: Data Corruption in DynamoDB

**Steps:**

1. **Immediate:** Stop all write operations
2. **Backup:** Create on-demand backup of current state
3. **Restore:** Restore from point-in-time recovery (within 35-day window)
4. **Reconcile:** Compare restored data with Monoova transaction status API
5. **Verify:** Test with small transaction volume
6. **Resume:** Gradually restore normal operations

---

## Conclusion

This implementation plan provides a structured approach to deploying the Monoova payments integration. Each phase has clear objectives, tasks, dependencies, and validation criteria to ensure successful delivery.

**Total Timeline:** 4-5 weeks from infrastructure setup to production deployment

**Key Milestones:**
- Week 1: Infrastructure foundation complete
- Week 2-3: Lambda functions developed and tested
- Week 3: API Gateway configured
- Week 4: Testing and validation complete
- Week 5: Production deployment and monitoring

**Next Steps:** Proceed to Phase 1 infrastructure setup after stakeholder approval of this plan.
