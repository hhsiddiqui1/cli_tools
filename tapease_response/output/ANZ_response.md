# Responses to ANZ

This document provides the information requested by ANZ in the email with reference C25101056246.

## 1. Visual Diagram of End-to-End Payment Flow

The payment flow is detailed in the attached `payment_flow.puml` file, which is a PlantUML sequence diagram. This diagram can be converted to a visual image using online tools like the official PlantUML web server.

Here is a text-based description of the flow:
1. A customer pays the taxi driver using a Clover Terminal.
2. The Clover Terminal sends the transaction details to Fiserv for processing.
3. Fiserv processes the transaction, debits the Customer's Bank, and returns the result to the Clover Terminal.
4. At the end of each day, Fiserv provides Tapease with a report of all transactions or via real-time APIs.
5. Fiserv transfers the total funds from the day's transactions to Tapease's ANZ account (Payin).
6. Tapease's system calculates the amount to be paid to each merchant after deducting service fees.
7. Tapease then initiates the payout to the merchants using one of the following methods:
    - Electronic Funds Transfer (EFT) via ANZ.
    - Cash payment, where Tapease withdraws cash from its ANZ account.

## 2. List of Entities Receiving Cash Payments

TODO: Please provide a list of all entities that receive cash payments, including the corresponding disbursed amounts.

Example:
- Merchant A: $500
- Merchant B: $300

## 3. Approximate Total Amount of Monthly Cash Withdrawals

TODO: Please advise the approximate total amount of monthly cash withdrawals in the future.

## 4. Transition to a Fully Electronic Disbursement Method

TODO: Please advise if you are considering transitioning to a fully electronic disbursement method (EFT only), thereby eliminating cash disbursements.

## 5. AML/CTF Compliance Program

TODO: Please attach a copy of your AML/CTF compliance program.

## 6. Independent Review for AML/CTF Compliance Program

TODO: Please attach a copy of the Independent Review for your AML/CTF compliance program if it is available.
