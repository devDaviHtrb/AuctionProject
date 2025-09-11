# AuctionProject
This repository is an academic project focused on the integration of database concepts, front and back-end web development and design, using technologies such as HTML, CSS, Python, JavaScript and MariaDB, which we will use to develop a fictitious auction website.

## Models

## Notification

## Asaas
- ### Customer
  To make payments, a customer is required within the Asaas payment API. The create_asaas_customer() function creates a customer on the Asaas server and adds it to the database. It returns the status code and description and receives the user who earns the id_asaas as a parameter.
- ### PaymentLink
  pass
- ### Webhook
  Whenever a change occurs in any of the payment processes, this route receives information about the process movement from the payment API. For security reasons, this route receives a key (password) in the header so that only authorized users can move these processes. This function operates through the "/payment/webhook" route and receives a JSON POST with information, including the most important EVENT, which contains the information code. Below are the possible codes that can be received:

  PAYMENT_AUTHORIZED
    - Card payment that has been authorized and needs to be captured.

    PAYMENT_APPROVED_BY_RISK_ANALYSIS
    - Card payment approved by manual risk analysis.

    PAYMENT_CREATED
    - Generation of new charge.

    PAYMENT_CONFIRMED
    - Charge confirmed (payment made, but the balance has not yet been made available).

    PAYMENT_ANTICIPATED
    - Advance payment.

    PAYMENT_DELETED
    - Charge removed.

    PAYMENT_REFUNDED
    - Charge reversed.

    PAYMENT_REFUND_DENIED
    - Refund denied.

    PAYMENT_CHARGEBACK_REQUESTED
    - Received chargeback.

    PAYMENT_AWAITING_CHARGEBACK_REVERSAL
    - Dispute won, awaiting transfer from the acquirer.

    PAYMENT_DUNNING_REQUESTED
    - Request for negative listing.

    PAYMENT_CHECKOUT_VIEWED
    - Billing invoice viewed by the customer.

    PAYMENT_PARTIALLY_REFUNDED
    - Charge partially reversed.

    PAYMENT_SPLIT_DIVERGENCE_BLOCK
    - Billing amount blocked due to split discrepancy.

    PAYMENT_AWAITING_RISK_ANALYSIS
    - Card payment awaiting approval by manual risk analysis.

    PAYMENT_REPROVED_BY_RISK_ANALYSIS
    - Card payment rejected by manual risk analysis.

    PAYMENT_UPDATED
    - Change in due date or existing billing amount.

    PAYMENT_RECEIVED
    - Collection received.

    PAYMENT_OVERDUE
    - Overdue billing.

    PAYMENT_RESTORED
    - Payment restored.

    PAYMENT_REFUND_IN_PROGRESS
    - Refund in process (settlement is already scheduled, charge will be refunded after settlement is executed).

    PAYMENT_RECEIVED_IN_CASH_UNDONE
    - Cash receipt undone.

    PAYMENT_CHARGEBACK_DISPUTE
    - In chargeback dispute (if documents are presented for dispute).

    PAYMENT_DUNNING_RECEIVED
    - Receipt of negative rating.

    PAYMENT_BANK_SLIP_VIEWED
    - Billing slip viewed by the customer.

    PAYMENT_CREDIT_CARD_CAPTURE_REFUSED
    - Card capture declined

    PAYMENT_SPLIT_CANCELLED
    - Billing had a split canceled.

    PAYMENT_SPLIT_DIVERGENCE_BLOCK_FINISHED
    - Blocking of the charge amount due to split discrepancy has been finalized.

## Socket
- ### Bid
- ### Finish Auction
- ### Win
- ### Add Money

