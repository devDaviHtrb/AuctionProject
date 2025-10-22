# AuctionProject
This repository is an academic project focused on the integration of database concepts, front and back-end web development and design, using technologies such as HTML, CSS, Python, JavaScript and MariaDB, which we will use to develop a fictitious auction website.

<!--
SingUp
	validação das entradas
		general_validations
	validação  por email
	via api do google
	associacao ao tipo de pessoa
	create no DATABASE
	hash de senha
Login
	autenticação de 2 fatores
	via api do google
criptofrafia do user_id no cookies
	puxar dados
Profile
Create Auction
	validação
	relacionamento com categorias e caracteristcica
	create no DATABASE
listagem de Liloes
Entrar Leilao
Emitir lance
Encerramento e Ganhador
Pagamento
Logout
Modulos
-->

## Sumary

## Project Architecture

## Models

## SingUp
```/myapp/routes/actions/public/SingUp```

The ```/signUp``` route is a **POST** endpoint that receives the following form values:

```js
{
  username:       SRT,
  password:       SRT,
  email:          STR,
  cpf:            STR   | null,
  name:           STR,
  userType:       STR,
  cellphone1:     STR   | null,
  cellphone2:     STR   | null,
  landline:       STR   | null,
  photo:          IMAGE | null,
  street_name:    STR   | null,  
  street_number:  INT   | null,
  apt:            STR   | null,
  zip_code:       STR   | null,
  district:       SRT   | null,
  city:           STR   | null,
  stat:           STR   | null
}
```
### Physical Person
If **userType** is ```physical_person```, the following additional fields are required:
```js
{
  rg:         STR   | null,
  birth_date: DATE  | null,
  gender:     STR  
}

```
### Legal Person
If **userType** is ```legal_person```, the following additional fields are required:
```js
{
  state_tax_registration:       STR | null,
  legal_business_name:          STR,
  trade_name:                   STR
  scrap_purchase_authorization: STR,
  cnpj:                         STR
}
```

After the data validation performed by ```/myapp/util/GeneralUserValidation```, an authentication token is sent to the provided email.
Once the user verifies their email, the account is created in the database, and the user is redirected to the login page.

Alternatively, users can sign up using the **Google API**.
In this case, the user will not have a password but will be able to log in normally via the **Google API**.
An email will be sent to the linked account explaining that they can set a password at any time, or immediately, through a token generated for password setup.

All passwords are stored as **HASHES** in the database.
Every authentication or password verification process is performed using **HASH** comparison.
## Login
```/myapp/routes/public/Login```

The ``/login`` route is a public **POST** endpoint that accepts the following form values:

```js
{
  username: STR,
  password: STR
}
```
The password is converted into a **HASH**, and authentication is performed using this hash.
Users can also log in using the **Google API**.

If two-factor authentication (**2FA**) is enabled, a token will be sent to the user’s registered email to complete the login process.

If the user forgets their password, it can be reset through the password recovery process.

## Auth
```/myapp/routes/actions/public/Auth```

These routes handle **Google API authentication, token validation, password resets**, and **user creation**.

- ### Google Redirect
  Route: ```/auth/google/redirect```

  Redirects the user to the Google login page and requests an authentication link from the **Google API**.

- ### Google Validate
  Route:  ```/auth/google/validate```
  
  Validates the received authentication link and data.
  If valid, the system either creates a new user account or logs in the existing user.

- ### Auth
  Route: ```/auth/confirm/<string:token>```

  Receives a token, identifies its type, and performs the corresponding action:

  - If *type* = ``login`` → logs in the user

  - If *type* = ```create``` → creates the user

  - If *type* = ``reset`` → resets the password

  In the case of a password reset, a POST request with the new password must be sent:
  ```js
  {
    new_password: STR
  }
  ```

- ### Resend
  Route: ```/auth/resend/<string:email>```
  
  This route may or may not receive an email parameter.
  If no email is provided, it redirects to the SignUp page.
  If an email is provided, it resends the token to that email.

- ### Change Password
  Route: ```/auth/change/<string:email>```
  
  Generates a password reset token (if a user with the given email exists) and sends it to the provided email address.

## Notification 
- ### Send
  ```/myapp/services/routes```

  The function ```send_email(email, subject ,content)``` receives as parameters the user's email, subject and content of the message, and sends it to the user, notification management is done by 


## Asaas
- ### Customer
  ```/services/CreateAsaasCustomer```

  To make payments, a customer is required within the Asaas payment API. The ```create_asaas_customer(id_user)``` function creates a customer on the Asaas server and adds it to the database.
  
  It returns the status code and description and receives the id of user who earns the id_asaas as a parameter.
  
- ### Webhook
  ```/routes/actions/Webhook```

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
- ### Join Room
  ```/sockets/Room```
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
        type:         "entry",
        room_id:      INT,
        username:     STR
    }
    ```

    Here's a JavaScript example:
    ```html
      <script src="/socket.io/socket.io.js"></script>
      <script>

        const socket = io();

        function joinAuctionRoom(room_id) {
          socket.emit("join_room", {
            room_id = room_id
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

  This notification will be sent by Socket.IO using the ```"emit_bid"``` event.

  When a user bids, the server will send a message to all clients:

  In the ```"server_content"``` event

  And specifically in the room corresponding to the auction the user is in (placed the bid).

  This way, the frontend will be able to display updated information in real time.

  The required parameters will be the auction ID, the ID of the user who placed the bid, and the bid amount,which will be in a json.

  will return a JSON:
    ```js
    {
        type:           "bid",
        room_id:        INT,
        username:       STR,
        value:          FLT | DBL
    }
    ```
  Here's a JavaScript example:
  ```html
      <script src="/socket.io/socket.io.js"></script>
      <script>

        const socket = io();

        function sendBid(room_id, value) {
          socket.emit("bid_content", {
            room_id = room_id,
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

## Configuration and Deployment

## Security

## The Team
