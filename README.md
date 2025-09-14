# AuctionProject
This repository is an academic project focused on the integration of database concepts, front and back-end web development and design, using technologies such as HTML, CSS, Python, JavaScript and MariaDB, which we will use to develop a fictitious auction website.

## Models

## Notification

## Asaas
- ### Customer ```/services/CreateAsaasCustomer```
  To make payments, a customer is required within the Asaas payment API. The ```create_asaas_customer(id_user)``` function creates a customer on the Asaas server and adds it to the database.
  
  It returns the status code and description and receives the id of user who earns the id_asaas as a parameter.
  
- ### PaymentLink
  pass
- ### Webhook ```/routes/actions/Webhook```
  Whenever a change occurs in any of the payment processes, this route receives information about the process movement from the payment API. For security reasons, this route receives a key (password) in the header so that only authorized users can move these processes.
  
  This function operates through the ```"/payment/webhook"``` route and receives a JSON POST with information, including the most important ```EVENT```, which contains the information code. Below are the possible codes that can be received:

  ```PAYMENT_AUTHORIZED```
    - Card payment that has been authorized and needs to be captured.

    ```PAYMENT_APPROVED_BY_RISK_ANALYSIS```
    - Card payment approved by manual risk analysis.

    ```PAYMENT_CREATED```
    - Generation of new charge.

    ```PAYMENT_CONFIRMED```
    - Charge confirmed (payment made, but the balance has not yet been made available).

    ```PAYMENT_ANTICIPATED```
    - Advance payment.

    ```PAYMENT_DELETED```
    - Charge removed.

    ```PAYMENT_REFUNDED```
    - Charge reversed.

    ```PAYMENT_REFUND_DENIED```
    - Refund denied.

    ```PAYMENT_CHARGEBACK_REQUESTED```
    - Received chargeback.

    ```PAYMENT_AWAITING_CHARGEBACK_REVERSAL```
    - Dispute won, awaiting transfer from the acquirer.

    ```PAYMENT_DUNNING_REQUESTED```
    - Request for negative listing.

    ```PAYMENT_CHECKOUT_VIEWED```
    - Billing invoice viewed by the customer.

    ```PAYMENT_PARTIALLY_REFUNDED```
    - Charge partially reversed.

    ```PAYMENT_SPLIT_DIVERGENCE_BLOCK```
    - Billing amount blocked due to split discrepancy.

    ```PAYMENT_AWAITING_RISK_ANALYSIS```
    - Card payment awaiting approval by manual risk analysis.

    ```PAYMENT_REPROVED_BY_RISK_ANALYSIS```
    - Card payment rejected by manual risk analysis.

    ```PAYMENT_UPDATED```
    - Change in due date or existing billing amount.

    ```PAYMENT_RECEIVED```
    - Collection received.

    ```PAYMENT_OVERDUE```
    - Overdue billing.

    ```PAYMENT_RESTORED```
    - Payment restored.

    ```PAYMENT_REFUND_IN_PROGRESS```
    - Refund in process (settlement is already scheduled, charge will be refunded after settlement is executed).

    ```PAYMENT_RECEIVED_IN_CASH_UNDONE```
    - Cash receipt undone.

    ```PAYMENT_CHARGEBACK_DISPUTE```
    - In chargeback dispute (if documents are presented for dispute).

    ```PAYMENT_DUNNING_RECEIVED```
    - Receipt of negative rating.

    ```PAYMENT_BANK_SLIP_VIEWED```
    - Billing slip viewed by the customer.

    ```PAYMENT_CREDIT_CARD_CAPTURE_REFUSED```
    - Card capture declined

    ```PAYMENT_SPLIT_CANCELLED```
    - Billing had a split canceled.

    ```PAYMENT_SPLIT_DIVERGENCE_BLOCK_FINISHED```
    - Blocking of the charge amount due to split discrepancy has been finalized.

## Socket
- ### Join Room ```/sockets/Room```
    Whenever a user joins an auction, all participants in that auction should be notified.

    This notification will be sent via Socket.IO, using the ```"join_room"``` event.

    When a user connects to the auction, the server will send a message to all clients:

    In the ```"server_content"``` event

    And specifically in the room corresponding to the auction the user joined.

    This way, the frontend can display updated information in real time.

    The only required parameter is the auction ID,which will be in a json.

    will return a JSON:
    ```js
    {
        type: "entry",
        room_id: INT,
        user_id: INT
        username: STR
        product_id: INT
        product_name: STR
    }
    ```

    Here's a JavaScript example:
    ```html
      <script src="/socket.io/socket.io.js"></script>
      <script>

        const socket = io();

        function joinAuctionRoom(id_auction) {
          socket.emit("join_room", {
            id_auction = id_auction
          });
        }

        socket.on("server_content", (data) => {
          const response = data.response;
          if (response.type === "entry") {
            alert(`usr: ${response.username} \n room: ${response.room_id}`);
          }
        });

      </script>
    ```

- ### Bid ```/socket/Room```
  Whenever a user bids in an auction, all participants in that auction should be notified.

  This notification will be sent by Socket.IO using the ```"bid_content"``` event.

  When a user bids, the server will send a message to all clients:

  In the ```"server_content"``` event

  And specifically in the room corresponding to the auction the user is in (placed the bid).

  This way, the frontend will be able to display updated information in real time.

  The required parameters will be the auction ID, the ID of the user who placed the bid, and the bid amount,which will be in a json.

  will return a JSON:
    ```js
    {
        type: "bid",
        room_id: INT,
        user_id: INT,
        username: STR,
        value: FLT/DBL,
        product_id: INT,
        product_name: STR
    }
    ```
  Here's a JavaScript example:
  ```html
      <script src="/socket.io/socket.io.js"></script>
      <script>

        const socket = io();

        function sendBid(id_auction, id_user, value) {
          socket.emit("bid_content", {
            id_auction = id_auction,
            id_user = id_user,
            value = value
          });
        }

        socket.on("server_content", (data) => {
          const response = data.response;
          if (response.type === "bid") {
            alert(`usr: ${response.username} \n room: ${response.room_id}\n val: ${response.value}`);
          }
        });

      </script>
    ```
  

- ### Close Auction ```/sockets/CloseRoom```
  Whenever an auction is created, it will have a predetermined time limit to close. However, it could happen that a user makes a bid in the last minute. So whenever a user makes a bid in the last 2 minutes, the time limit resets to 2 minutes.

  The ```close_auction(id_auction)``` function removes all participants from the socket room, deletes the auction, and changes its status.

  To time it, there is the function ```start_auction_timer(auction_id, seconds)``` which calls the function ```close_auction()``` after giving the time, for the occasion in which a bid is made in the final minutes the function ```add_time_to_action(id_auction, seconds)``` will be called. In extreme cases or exceptions, for example a server crash, the function ```start()``` must be called in this case putting all the auctions in the database on timer again.


