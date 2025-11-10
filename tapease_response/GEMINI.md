# Project Overview

This project is for **Tapease**, a service operated by **A2 Square Pty Ltd**. Tapease functions as an Independent Selling Organization (ISO), providing payment terminal services to taxi operators in Sydney, Australia.

The core business model involves:
- Onboarding taxi drivers as merchants, including full Know Your Customer (KYC) verification.
- Deploying Fiserv's Clover payment terminals to these merchants.
- Receiving bulk daily settlements from Fiserv for all transactions processed through these terminals.
- Calculating and distributing individual merchant earnings via various payout methods (EFT, PayID, and cash).

A key aspect of Tapease's operation is that it does **not** process, store, or transmit any cardholder data. All payment processing is handled by Fiserv, a PCI Level 1 compliant payment processor. This significantly reduces Tapease's PCI DSS scope.

## Current Project Goal

The immediate goal of this project is to provide a comprehensive response to a review request from **ANZ Bank** (Case Reference: C25101056246). The response focuses on demonstrating compliance with financial regulations, particularly in the areas of Anti-Money Laundering/Counter-Terrorism Financing (AML/CTF) and payment flow transparency.

## Key Components

The repository contains the following key components:

- `tapease-openapi.json`: The OpenAPI specification for the Tapease backend system. This API, built with FastAPI (Python), provides the technical infrastructure for merchant onboarding, transaction tracking, payout management, and compliance auditing.

- `output/`: This directory contains the full response package for ANZ, including:
    - `ANZ_Response_Complete.md`: The main response document.
    - `AML_CTF_Compliance_Framework.md`: A detailed outline of the company's AML/CTF policies and procedures.
    - `PCI_DSS_Scope_Statement.md`: A document clarifying the minimal PCI DSS scope of the business.
    - `comprehensive_payment_flow.puml`: A PlantUML diagram detailing the end-to-end payment flow.
    - `EXECUTIVE_SUMMARY.md`: A high-level overview of the response to ANZ.

- `ANZ_Requests.txt`: The original request letter from ANZ, outlining the information required.

## Technical Stack

- **Backend:** The `tapease-openapi.json` file indicates the backend is built using **Python** with the **FastAPI** framework.
- **Diagrams:** **PlantUML** is used for generating payment flow diagrams.

# Building and Running

TODO: Add instructions on how to set up the development environment, build the project, and run the backend service. This would likely involve:
1. Setting up a Python virtual environment.
2. Installing dependencies from a `requirements.txt` file (not currently present).
3. Running the FastAPI application using a server like Uvicorn.

# Development Conventions

Development should follow the conventions and standards established in the existing documentation. Key considerations include:
- **Compliance by Design:** All new features must be built with AML/CTF and data security requirements in mind.
- **API Standards:** The API should adhere to the structure and style defined in `tapease-openapi.json`.
- **Auditability:** All significant actions within the system must be logged in the audit trail.
- **Documentation:** Diagrams and technical documentation should be kept up-to-date.