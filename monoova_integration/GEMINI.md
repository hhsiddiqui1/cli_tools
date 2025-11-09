# Project: Monoova Payout Integration

## Project Overview

This project aims to build a Python-based service to integrate with the Monoova Payments API for automating customer payouts. The system is designed to be secure, scalable, and reliable, with the intention of deploying it on AWS as a serverless application.

The core functionality involves:
1.  **Funding:** Receiving settlement funds from Fiserv into a dedicated Monoova Automatcher account.
2.  **User Management:** Securely storing customer payout details (Bank Accounts and PayIDs).
3.  **Payouts:** Executing payouts to customers via the Monoova API, triggered by an internal web application.

The architecture is event-driven, relying on webhooks for asynchronous status updates on payments.

**Key Technologies:**
*   **Backend:** Python
*   **API Provider:** Monoova (Payments API v5.29)
*   **Target Infrastructure:** AWS Lambda, API Gateway, S3, DynamoDB, Secrets Manager, SQS, CloudWatch.

## Project Structure

The project is organized into the following files and directories:

*   `GEMINI.md`: This file. A living document providing an overview of the project.
*   `requirements.md`: Details the functional requirements, user flows, and compliance analysis.
*   `analysis.md`: Details the non-functional requirements (Security, Scalability, Reliability, etc.).
*   `docs/`: Contains all documentation, including PlantUML source diagrams and their rendered PNG versions.
*   `*.yaml`: The OpenAPI specifications for the Monoova APIs.

## Building and Running

### Dependencies

The project uses Python. Install the required packages using pip:

```bash
pip install -r requirements.txt
```

### Generating Diagrams

To convert the PlantUML source files (`.plantuml`) in the `docs/` directory into PNG images, run the following Python script:

```bash
python render_diagrams.py
```

### Running the Application

```bash
# TODO: Add command to run the application locally.
# This will likely involve running a local Flask/FastAPI server
# to simulate the AWS Lambda and API Gateway environment.
python payout_service.py
```

### Running Tests

```bash
# TODO: Add command to run tests.
# We will use Python's `unittest` or `pytest` framework.
python -m unittest discover
```

## Development Conventions

### Security
*   **API Keys:** The Monoova API key must be stored securely in **AWS Secrets Manager** and retrieved at runtime. It must not be hardcoded.
*   **Data at Rest:** All sensitive customer data, especially bank account and PayID details, must be encrypted in the database.
*   **Data in Transit:** All communication must use HTTPS/TLS.

### Reliability
*   **Idempotency:** All payout requests to Monoova must use a unique `callerUniqueReference`. This allows for safe retries on network failures without the risk of duplicate payments.
*   **Asynchronous Updates:** The final status of a payment is handled via webhooks. This is critical for reliability as some payment methods are not instantaneous.
*   **Error Handling:** Failed webhook events or critical processing errors should be sent to a Dead-Letter Queue (DLQ) in AWS SQS for manual inspection and reprocessing.

### Code Style
*   The project will follow the [PEP 8 -- Style Guide for Python Code](https://peps.python.org/pep-0008/).
*   Use type hints for function signatures to improve code clarity and maintainability.
