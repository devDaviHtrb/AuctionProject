# Auction Project

  This repository is an **academic project** focused on the **integration of database concepts**, **front-end** and **back-end web development**, and **design**, using technologies such as **HTML**, **CSS**, **Python**, **JavaScript**, and **PostgreSQL**, which are used to develop a **fictitious auction website**.

<!--
SignUp
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

## Introduction

  The group hereby documents the process of creating an **auction website** based on **Python, HTML, CSS, and JavaScript**. Through **websockets**, **dynamic rendering**, a blend of **single-page** and **multiple-page applications**, and modern **design concepts**, this website aims to provide a pleasant customer experience while maintaining **scalability**, **good programming practices**, and **resource efficiency**.

  The objective of this project is to develop a **functional online auction website** capable of:

  - Managing **real-time bids**
  - Integrating with a **secure payment API**
  - Providing a **complete user experience**, from creating listings to completing transactions

  The platform is designed to be **broad and inclusive**, allowing any user, whether **individual** or **legal entity**, to:

  - Participate in auctions
  - Create rooms to advertise products

  To ensure **security and traceability**:

  - Only **registered and authenticated users** can participate in auctions
  - The system offers **anonymity options**, a **light/dark theme**, and **accessibility mode** for a **personalized experience**

  The platform supports:

  - **Product listings without category restrictions**
  - A **dynamic database** capable of storing an **unlimited number of categories and attributes**, ensuring **flexibility** and **scalability**

  To optimize the user experience, the site uses a combination of rendering techniques:

  - **Multiple Page Application (MPA)**
  - **Server-Side Rendering (SSR)**
  - **Client-Side Rendering (CSR)**

  This approach allows **HTML blocks to be loaded only when necessary**, reducing computational resource usage and improving performance.

  The system follows the **MVC (Model-View-Controller)** standard, promoting:

  - **Separation of concerns** between data, business logic, and interface
  - Easier **maintenance**
  - Facilitation of **unit testing**
  - Improved **future scalability**

  The project is modularized, with:

  - **Routes and endpoints**
  - **Services**
  - **Real-time events**

  All components are managed automatically, ensuring **code organization** and **readability**.

  The technology stack was **strategically chosen**:

  - **Backend & Route Management**: Flask
  - **Relational Database**: PostgreSQL
  - **User Authentication & Sessions**: Flask-Login
  - **Real-Time Bidding**: Flask-SocketIO
  - **Frontend**: JavaScript / CSS / HTML

  This combination ensures **scalability, security, and performance**, allowing the system to support a **large number of users** and **concurrent auctions**.

  With this structure, the project also allows for future enhancements, such as:

  - **Notifications**
  - **Advanced filters**
  - **Sales reports**
  - **Integration with other service APIs**

## Project Architecture

  The project’s architecture is based on the **MVC (Model–View–Controller)** pattern.

  However, due to the project’s scope and complexity, using a **pure MVC** approach would lead to **disorganization**, **low modularity**, and **future difficulties** with **maintenance**, **scalability**, **unit testing**, and **legacy evolution**.

  Therefore, the final architecture is a **variation of MVC**, preserving its main principles but adding extra layers and abstractions to ensure greater organization and clear separation of concerns.

  The MVC pattern divides the application into three main layers:

  | Layer          | Responsibility                                                                                                     |
  | -------------- | ------------------------------------------------------------------------------------------------------------------ |
  | **Model**      | Handles **data**, **business logic**, and **database interactions**.                                               |
  | **View**       | Represents the **user interface** and **data presentation**.                                                       |
  | **Controller** | Acts as the **intermediary between Model and View**, receiving requests, processing data, and returning responses. |

  In this project, the MVC pattern has been **extended and modularized** to include:

  - A **service layer** (isolated and reusable business logic)
  - A **setup layer** (centralized configuration of extensions, sockets, and ORM)
  - **Context-based routing layers** (`public`, `common`, `admin`)
  - A **utilities layer** (helpers and validation scripts)

  ```bash

  app.py
  ├── config.py
  ├── database.sql
  ├── dockerfile
  ├── myapp
  │   ├── extensions.py
  │   ├── initExtensions.py
  │   ├── __init__.py
  │   ├── models/
  │   ├── repositories/
  │   ├── routes/
  │   ├── services/
  │   ├── setup/
  │   ├── sockets/
  │   ├── static/
  │   ├── templates/
  │   └── utils/
  ├── requirements.txt
  └── README.md
  ```
- ### Simplified Flow
    ```mermaid
    flowchart TB
        %% ===== USERS =====
        subgraph USERS["👥 Users"]
            IU["Individual User"]
            LEU["Legal Entity User"]
            ADM["Administrator"]
        end

        %% ===== AUTH =====
        subgraph AUTH["🔐 Authentication"]
            SU["Sign Up"]
            LG["Login / Google OAuth"]
            EP["Edit Profile"]
        end

        %% ===== AUCTION =====
        subgraph AUCTION["🏷️ Auction System"]
            CREATE["Create Auction"]
            JOIN["Join Auction Room"]
            BID["Place Bid"]
            CLOSE["Close Auction / Set Winner"]
        end

        %% ===== PAYMENT =====
        subgraph PAYMENT["💳 Payments"]
            PROCESS["Process Payment"]
            NOTIFY["Send Notification"]
        end

        %% ===== DATABASE =====
        subgraph DB["🗄️ Database"]
            USERS_DB["Users"]
            AUCTIONS_DB["Auctions & Bids"]
            PAYMENTS_DB["Payments"]
        end

        %% ===== FLOWS =====
        IU --> SU --> LG --> EP
        LEU --> SU --> LG --> EP
        ADM --> AUCTION

        IU --> JOIN --> BID --> CLOSE --> PROCESS --> NOTIFY
        LEU --> CREATE --> CLOSE --> PROCESS --> NOTIFY

        SU --> USERS_DB
        EP --> USERS_DB
        CREATE --> AUCTIONS_DB
        BID --> AUCTIONS_DB
        CLOSE --> AUCTIONS_DB
        PROCESS --> PAYMENTS_DB
    ```

## Models

- ### Settings
  <details>
    <summary>View Setting Model</summary>
  
  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |setting_id|INT|None|N|P.K.|Integer and auto-increment primary key of the settings table|
  |anonymous_mode|BOOLEAN|None|N|None|"Display of the user's personal information in an auction bid|default false"|
  |two_factor_auth|BOOLEAN|None|N|None|"Enabling or disabling two-factor authentication|default false"|
  |user_id|INT|None|N|FK|Foreign key originating from the users table|

  </details>

- ### Users
  <details>
    <summary>View User Model</summary>

  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |user_id|INT|None|N|P.K.|Integer and auto-increment primary key of the users table|
  |name|VARCHAR|255|N|None|User's full name|
  |username|VARCHAR|50|N|None|Fictitious user name or name used on the website by the company|
  |password|VARCHAR|500|N|None|User password stored in varchar greater than 255 for encryption|
  |e-mail|VARCHAR|255|N|None|User email|
  |cpf|CHAR|14|N|None|CPF (with mask) of the individual or legal representative in the case of a company account|
  |photo|VARCHAR|255|S|None|Profile photo link displayed on the website|
  |cellphone1|CHAR|14|N|None|User's main cell phone (with area code and mask Ex.: (00)00000-0000)|
  |cellphone2|CHAR|14|S|None|Secondary cell phone (with area code and mask Ex.: (00)00000-0000)|
  |landline|CHAR|13|S|None|Landline (with area code and mask Ex.: (00)0000-0000)|
  |wallet|DECIMAL|"(12|2)"|N|None|"Stores the user's balance|can be added to the payment method and debited when purchasing an item or redeemed from the wallet"|
  |admin_user|BOOLEAN|None|N|None|If the user has system administrator permissions|
  |active_auction_number|TINYINT|1|N|None|"Number of advertised products active in auction to control maximum advertising value|default 0"|
  |password_token_expiration_datetime|DATETIME|None|S|None|"Token expiration date and time for password change|if it exists"|
  |api_token|VARCHAR|255|S|None|Token used in the external payments API that may not exist at first will be null|
  |password_token|VARCHAR|255|S|None|Token for changing the password| 
  </details>

- ### Physical_persons
  <details>
    <summary>View Physycal Person Model</summary>

  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |user_id|INT|None|N|PK FK|Foreign key originating from the users table key that plays the role of primary key in the physical_persons table|
  |rg|VARCHAR|12|N|None|ID number (with mask Ex.: 00.000.000-0)|      
  |birth_date|DATE|None|N|None|Date of birth|
  |gender|VARCHAR|20|N|None|User gender|
  </details>

- ### Legal_persons
  <details>
    <summary>View Legal Person Model</summary>

  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |user_id|INT|None|N|PK FK|Foreign key originating from the users table key that plays the role of primary key in the legal_persons table|
  |cnpj|CHAR|18|N|None|Company CNPJ (with mask)|
  |state_tax_registration|CHAR|17|S|None|State Registration (I.E.) of the company (with mask) considering the state with the most digits in the I.E. with 13 digits and 4 mask spaces|
  |legal_business_name|VARCHAR|255|N|None|Company name|
  |trade_name|VARCHAR|255|N|None|Business name of the company|        
  |scrap_purchase_authorization|BOOLEAN|None|N|None|Authorization to purchase scrap|
  </details>

- ### Addresses
  <details>
    <summary>View Address Model</summary>

  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |address_id|INT|None|N|P.K.|Integer and auto-incrementing primary key of the addresses table|
  |street_name|VARCHAR|255|N|None|Street Name|
  |street_number|VARCHAR|6|N|None|Residence number|
  |apt|VARCHAR|80|S|None|Complement|
  |zip_code|CHAR|9|N|None|CEP (with mask)|
  |district|VARCHAR|80|N|None|Neighborhood|
  |city|VARCHAR|80|N|None|City|
  |state|CHAR|2|N|None|State (U.F. acronym)|
  |principal_address|BOOLEAN|None|N|None|"If the registered address is the user's main address|default false"|
  |user_id|INT|None|N|FK|Foreign key originating from the primary key of the users table|
  </details>

- ### Payments
  <details>
    <summary>View Payment Model</summary>
    
  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |payment_id|INT|None|N|P.K.|Integer and auto-increment primary key of the payments table|
  |amount|DECIMAL|"(12|2)"|N|None|Value moved|
  |payer|VARCHAR|255|N|None|The one who sends the payment|
  |payee|VARCHAR|255|N|None|The one who receives the payment|
  |opening_datetime|DATETIME|None|N|None|Payment opening date and time|
  |due_datetime|DATETIME|None|N|None|Payment expiry date and time|    
  |confirmation_datetime|DATETIME|None|S|None|Payment completion date and time|
  |user_id|INT|None|N|FK|Foreign key originating from the primary key of the users table|
  |payment_method_id|INT|None|N|FK|Foreign key originating from the primary key of the payment_methods table|
  |payment_status_id|INT|None|N|FK|Foreign key originating from the primary key of the payment_statuses table|
  </details>

- ### Payment_methods
  <details>
    <summary>View Payment Method Model</summary>
    
  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |payment_method_id|INT|None|N|P.K.|Integer and auto-increment primary key of the payment_methods table|
  |payment_method_name|VARCHAR|20|N|None|"Payment method name (debit card|ticket|pix|etc)"|
  </details>

- ### Payment_statuses
  <details>
    <summary>View Payment Status Model</summary>
    
  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |payment_status_id|INT|None|N|P.K.|Integer and auto-increment primary key of the payment_statuses table|
  |payment_status_name|VARCHAR|20|N|None|"Payment status method name (pending|paid|failed|reversed|canceled)"|
  </details>

- ### Bids
  <details>
    <summary>View Bid Model</summary>
    
  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |bid_id|INT|None|N|P.K.|Integer and auto-incrementing primary key of the bids table|
  |bid_value|DECIMAL|"(12|2)"|N|None|Bid value executed|
  |bid_datetime|DATETIME|None|N|None|Date and time of bid execution|  
  |winner|BOOLEAN|None|N|None|"If the bid is the winning bid of the auction|default false"|
  |user_id|INT|None|N|FK|Foreign key originating from the primary key of the users table|
  </details>

- ### Products
  <details>
    <summary>View Product Model</summary>
    
  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |product_id|INT|None|N|P.K.|Integer and auto-increment primary key of the products table|
  |product_name|VARCHAR|255|N|None|Full product name|
  |dispription|TEXT|None|S|None|Open product description in prose text format|
  |min_bid|DECIMAL|"(12|2)"|N|None|Minimum product value|
  |start_datetime|DATETIME|None|N|None|Auction start date and time|   
  |street_name|VARCHAR|255|S|None|Street name (part of the address where the product is located)|
  |street_number|VARCHAR|6|S|None|House number (part of the address where the product is located)|
  |apt|VARCHAR|80|S|None|Complement (part of the address where the product is located)|
  |zip_code|CHAR|9|S|None|ZIP code (with mask) (part of the address where the product is located)|
  |district|VARCHAR|80|S|None|Neighborhood (part of the address where the product is located)|
  |city|VARCHAR|80|S|None|City (part of the address where the product is located)|
  |state|CHAR|2|S|None|State (U.F.) (part of the address where the product is located)|
  |user_id|INT|None|N|FK|Foreign key originating from the primary key of the users table|
  |category_id|INT|None|N|FK|Foreign key originating from the primary key of the categories table|
  |product_status_id|INT|None|N|FK|Foreign key originating from the primary key of the product_statuses table|
  </details>

- ### Product_statuses
  <details>
    <summary>View Product Status Model</summary>
    
  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |product_status_id|INT|None|N|P.K.|Integer and auto-increment primary key of the product_statuses table|
  |product_status_name|VARCHAR|20|N|None|"Auction status name (not started|in occurrence|finished|canceled)"|
  </details>

- ### Categories
  <details>
    <summary>View Category Model</summary>
    
  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |category_id|INT|None|N|P.K.|Integer and auto-increment primary key of the categories table|
  |category_name|VARCHAR|80|N|None|Category name|
  </details>

- ### Technical_features
  <details>
    <summary>View Technical Feature Model</summary>
    
  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |technical_feature_id|INT|None|N|P.K.|Integer and auto-increment primary key of the technical_features table|
  |technical_feature_name|VARCHAR|80|N|None|Name of the technical characteristic|
  </details>

- ### Category_technical_features
  <details>
    <summary>View Category Technical Feature Model</summary>
    
  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |technical_feature_id|INT|None|N|PK FK|Foreign key originating from the primary key of the technical_features table that plays the role of primary key in the category_technical_features table|
  |category_id|INT|None|N|PK FK|Foreign key originating from the primary key of the categories table that plays the role of primary key in the category_technical_features table|
  </details>

- ### Technical_features_values
  <details>
    <summary>View Technical Feature Value Model</summary>
    
  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |category_id|INT|None|N|PK FK|Foreign key originating from the primary key of the categories table that plays the role of primary key in the technical_features_valeus table|
  |technical_features_id|INT|None|N|PK FK|Foreign key originating from the primary key of the technical_features table that plays the role of primary key in the technical_features_valeus table|
  |value|VARCHAR|255|N|None|Value/Description given to a given technical specification|
  |product_id|INT|None|N|PK FK|Foreign key originating from the primary key of the products table, which plays the role of a foreign key in the technical_features_valeus table and also a primary key to guarantee the integrity and functioning of the system|
  </details>

- ### Images
  <details>
    <summary>View Image Model</summary>
    
  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |image_id|INT|None|N|P.K.|Integer and auto-increment primary key of the images table|
  |image|VARCHAR|255|N|None|Product image link|
  |principal_image|BOOLEAN|None|N|None|If the image is the main photo to be displayed of the product|
  |product_id|INT|None|N|FK|Foreign key originating from the primary key of the products table|
  </details>

- ### Legal_infos
  <details>
    <summary>View Legal Info Model</summary>
    
  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |legal_infos_id|INT|None|N|P.K.|Integer and auto-increment primary key of the legal_infos table|
  |process_number|CHAR|25|N|None|Process number (with mask)|
  |court|VARCHAR|255|N|None|Judicial court|
  |plaintiff|VARCHAR|255|N|None|Name of the creditor|
  |defendant|VARCHAR|255|N|None|Name of the executed|
  |judge_name|VARCHAR|255|N|None|Name of the judge responsible for the legal process|
  |extra_notes|TEXT|None|S|None|Additional descriptions in prose text format|
  |product_id|INT|None|N|FK|Foreign key originating from the primary key of the products table|
  |case_type_id|INT|None|N|FK|Foreign key originating from the primary key of the case_types table|
  </details>

- ### Case_types
  <details>
    <summary>View Case Type Model</summary>
    
  | Atributte | Type | Size | Nullable | Key | Description|
  |-----------|------|------|----------|-----|------------|
  |case_type_id|INT|None|N|P.K.|Integer and auto-increment primary key of the case_types table|
  |case_type_name|VARCHAR|10|N|None|"Name of the type of legal execution (tax|judicial)"|
  </details>


![DATABASE](https://res.cloudinary.com/dnet6nodm/image/upload/v1761767967/Users_photos/swmczrsjmmszfnfkwmjv.jpg)


## Setup

file: createSocketEvents.py
Purpose: Dynamically imports all socket event modules from the myapp/sockets folder.

Usage:

from myapp.setup.create_SocketEvents import create_SocketEvents
create_SocketEvents()

Description:

Uses pkgutil to iterate over all modules in the folder.

Imports each module using importlib.import_module.

Ensures all socket events are automatically registered without manual imports.

File: createTables.py
Purpose: Handles database creation and schema export for PostgreSQL.

Usage:

from myapp.setup.create_tables import create_tables
create_tables(app, db)

Description:

Iterates over all model modules in myapp/models.

Creates tables using SQLAlchemy within the Flask app context.

Exports DDL statements to database.sql file.

Optionally drops all existing tables with drop_all_tables(db).

Dependencies:

Flask

Flask-SQLAlchemy

SQLAlchemy

postgresql dialect

3. myapp/utils/File - File Utilities

Functions:

erase_file(file_path) – clears the content of a file.

write_file(file_path, content) – appends content to a file.

Usage:
Used internally by create_tables.py to export DDL to database.sql.

4. Cloudinary Integration

File: cloudinary_setup.py
Purpose: Configures Cloudinary API credentials for media storage.

Setup:

import cloudinary
from config import Config

cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET
)

Description:

Sets up secure access to Cloudinary.

Credentials are imported from a Config class.

5. myapp/setup/InitSocket.py - Flask-SocketIO Initialization

Purpose: Initializes SocketIO in a Flask application.

Usage:

from myapp.setup.socket import init_socket
socket_io = init_socket(app)

Description:

Creates a SocketIO instance.

Attaches it to the Flask app using init_app.

6. myapp/setup/InitSqlAlchemy.py - SQLAlchemy Initialization

Purpose: Initializes the SQLAlchemy instance for Flask.

Usage:

from myapp.setup.database import init_db
db = init_db(app)

Description:

Configures the SQLAlchemy ORM with Flask.

Returns the database instance for further usage.

7. myapp/setup/PermissionRequire.py - Authentication Decorator

Purpose: Provides authentication and permission checks for routes.

Usage:

from myapp.setup.PermissionRequire import init_authDecorator
init_authDecorator(app)

Description:

Defines public, common, and admin routes.

Checks user sessions and cookies for authentication.

Redirects unauthorized users to login or returns 403 Forbidden.

Initializes session data with init_session when a valid user is found.

8. myapp/setup/registerHandlers.py - Error Handlers

Purpose: Registers custom error pages for the Flask application.

Usage:

from myapp.setup.register_handlers import register_handlers
register_handlers(app)

Description:

Supports error codes: 403, 404.

Maps error codes to HTML templates (403.html, 404.html).

Uses closures to remember error templates when handling exceptions.

9. myapp/setup/registerRoutes.py - Route Registration

Purpose: Dynamically registers all Flask Blueprints from the myapp/routes folder.

Usage:

from myapp.setup.register_routes import register_routes
register_routes(app)

Description:

Recursively scans myapp/routes for Python modules.

Imports modules and registers any Blueprint objects.

Updates route permissions lists (publicRoutes, commonRoutes, adminRoutes).

Provides helper functions to extract endpoints from Blueprints.

## SignUp

  `/myapp/routes/actions/public/SignUp`

  The `/signUp` route is a **POST** endpoint that receives the following form values:

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

  - ### Physical Person

    If **userType** is `physical_person`, the following additional fields are required:

    ```js
    {
      rg:         STR   | null,
      birth_date: DATE  | null,
      gender:     STR
    }

    ```

  - ### Legal Person

    If **userType** is `legal_person`, the following additional fields are required:

    ```js
    {
      state_tax_registration:       STR | null,
      legal_business_name:          STR,
      trade_name:                   STR,
      scrap_purchase_authorization: STR,
      cnpj:                         STR
    }
    ```

  After the **data validation** performed by `/myapp/util/GeneralUserValidation`, an **authentication token** is sent to the provided **email**.  
  Once the user verifies their email, the **account** is created in the **database**, and the user is redirected to the **login page**.

  Alternatively, users can **sign up using the Google API**.  
  In this case, the user will **not have a password**, but will be able to **log in normally** via the **Google API**.  
  An **email** will be sent to the linked account explaining that they can **set a password** at any time, or immediately, through a **token generated for password setup**.

  All **passwords** are stored as **HASHES** in the **database**.  
  Every **authentication** or **password verification** process is performed using **HASH comparison**.

## Login

  `/myapp/routes/public/Login`

  The `/login` route is a public **POST** endpoint that accepts the following form values:

  ```js
  {
    username: STR,
    password: STR
  }
  ```

  After the **data validation** performed by `/myapp/util/GeneralUserValidation`, an **authentication token** is sent to the provided **email**.  
  Once the user verifies their **email**, the **account** is created in the **database**, and the user is redirected to the **login page**.

  Alternatively, users can **sign up using the Google API**.  
  In this case, the user will **not have a password**, but will be able to **log in normally** via the **Google API**.  
  An **email** will be sent to the linked account explaining that they can **set a password** at any time, or immediately, through a **token generated for password setup**.

  All **passwords** are stored as **HASHES** in the **database**.  
  Every **authentication** or **password verification** process is performed using **HASH comparison**.

## Auth

  `/myapp/routes/actions/public/Auth`

  These routes handle **Google API authentication, token validation, password resets**, and **user creation**.

  - ### Google Redirect

    Route: `/auth/google/redirect`

    Redirects the user to the Google login page and requests an authentication link from the **Google API**.

  - ### Google Validate

    Route: `/auth/google/validate`

    Validates the received authentication link and data.
    If valid, the system either creates a new user account or logs in the existing user.

  - ### Auth

    Route: `/auth/confirm/<string:token>`

    Receives a **token**, identifies its **type**, and performs the corresponding action:

    - If **type** = `login` → **logs in** the **user**
    - If **type** = `create` → **creates** the **user**
    - If **type** = `reset` → **resets the password**

    In the case of a **password reset**, a **POST request** with the **new password** must be sent.


    ```js
    {
      new_password: STR
    }
    ```

  - ### Resend

    Route: `/auth/resend/<string:email>`

    This **route** may or may not receive an **email parameter**.  
  - If **no email** is provided, it **redirects** to the **SignUp page**.  
  - If an **email** is provided, it **resends the token** to that **email**.

  - ### Change Password

    Route: `/auth/change`

    It's a **POST** endpoint that receives the following form values:
    ```js
    {
      email:  STR
    }
    ```
    
    Generates a **password reset token** (if a **user** with the given **email** exists) and sends it to the provided **email address**.

## Address

## Notification

- ### Send

  `/myapp/services/routes`

  The function `send_email(email, subject ,content)` receives as parameters the user's email, subject and content of the message, and sends it to the user, notification management is done by

## Profile

## Auction

`/myapp/model/Products`

- ### Create Auction
  `/myapp/routes/common/NewAuction`

  Route: `/new/auction`

  The `/login` route is a common **POST** endpoint that accepts the following form values:

  ```js
  {
    product_name:   STR,
    description:    STR | null,
    min_bid:        FLT | DBL,
    start_datetime: STR | null,
    product_status: STR[FK],
    street_name:    STR | null,
    street_number:  STR | null,
    apt:            STR | null,
    zip_code:       STR | null,
    district:       STR | null,
    city:           STR | null,
    state:          STR | null,
    user_id:        INT,
    category:       STR[FK],
    end_datetime:   DATETIME | null,
    duration:       INT,
    photos:         LIST[PHOTO],
  }
  ```

  This **route** creates a new **`auction|product`** in the **database** and **application**.

  This **route** can also receive **legal information**, which will be accepted if the **request** includes the following information:

  ```js
  {
    process_number: STR,
    court:          STR,
    case_type:      STR[FK],
    plaintiff:      STR,
    defendant:      STR,
    judge_name:     STR,
    extra_notes:    STR | null
  }
  ```

- ### Technical Features
  
  Every **product** belongs to a **category**, and each **category** defines which **technical features** are applicable to it.  
  This relationship of possibility is represented by the table:

  `category_technical_features(category_id, technical_feature_id)`

  To assign actual **values** to those features, the table below is used:

  `technical_features_values(product_id, technical_feature_id, category_id, value)`

  This table links the **product** to its corresponding **technical features** and stores the assigned **content/value**, while also maintaining the **category relationship** to facilitate specific queries.

  The **back-end** must ensure **data integrity** by preventing invalid or inconsistent relationships between these entities.  
  The available **technical features** for a given **product** are obtained through the function:

  ```product_repository.get_technical_feature_id(product)```

## Asaas

  ![Flow](https://res.cloudinary.com/dnet6nodm/image/upload/v1761768327/Users_photos/hsjf8keoqguhded6vtme.png)


- ### Customer

  `/services/CreateAsaasCustomer`

  To make **payments**, a **customer** is required within the **Asaas payment API**.  
  The `create_asaas_customer(id_user)` **function** creates a **customer** on the **Asaas server** and adds it to the **database**.

  It **returns** the **status code** and **description**, and receives the **user ID** (who will receive the **id_asaas**) as a **parameter**.

- ### Webhook

  `/routes/actions/Webhook`

  Whenever a **change** occurs in any of the **payment processes**, this **route** receives information about the **process movement** from the **payment API**.  
  For **security reasons**, this **route** requires a **key (password)** in the **header**, so that only **authorized users** can manage these processes.

  This **function** operates through the `"/payment/webhook"` **route** and receives a **JSON POST** with information, including the most important **EVENT**, which contains the **information code**.  
  Below are the possible **codes** that can be received:

  | Status                                   | Description                                                                                  |
  |-----------------------------------------|----------------------------------------------------------------------------------------------|
  | ```PAYMENT_AUTHORIZED```                       | Card payment that has been authorized and needs to be captured.                              |
  | ```PAYMENT_APPROVED_BY_RISK_ANALYSIS```        | Card payment approved by manual risk analysis.                                               |
  | ```PAYMENT_CREATED```                          | Generation of new charge.                                                                    |
  | ```PAYMENT_CONFIRMED```                        | Charge confirmed (payment made, but balance not yet available).                               |
  | ```PAYMENT_ANTICIPATED```                      | Advance payment.                                                                             |
  | ```PAYMENT_DELETED```                          | Charge removed.                                                                              |
  | ```PAYMENT_REFUNDED```                         | Charge reversed.                                                                             |
  | ```PAYMENT_REFUND_DENIED```                     | Refund denied.                                                                               |
  | ```PAYMENT_CHARGEBACK_REQUESTED```             | Received chargeback.                                                                         |
  | ```PAYMENT_AWAITING_CHARGEBACK_REVERSAL```     | Dispute won, awaiting transfer from the acquirer.                                            |
  | ```PAYMENT_DUNNING_REQUESTED```                | Request for negative listing.                                                                |
  | ```PAYMENT_CHECKOUT_VIEWED```                  | Billing invoice viewed by the customer.                                                     |
  | ```PAYMENT_PARTIALLY_REFUNDED```               | Charge partially reversed.                                                                   |
  | ```PAYMENT_SPLIT_DIVERGENCE_BLOCK```           | Billing amount blocked due to split discrepancy.                                             |
  | ```PAYMENT_AWAITING_RISK_ANALYSIS```           | Card payment awaiting approval by manual risk analysis.                                      |
  | ```PAYMENT_REPROVED_BY_RISK_ANALYSIS```        | Card payment rejected by manual risk analysis.                                              |
  | ```PAYMENT_UPDATED```                           | Change in due date or existing billing amount.                                               |
  | ```PAYMENT_RECEIVED```                          | Collection received.                                                                         |
  | ```PAYMENT_OVERDUE```                           | Overdue billing.                                                                             |
  | ```PAYMENT_RESTORED```                          | Payment restored.                                                                            |
  | ```PAYMENT_REFUND_IN_PROGRESS```                | Refund in process (settlement scheduled, will refund after settlement executed).             |
  | ```PAYMENT_RECEIVED_IN_CASH_UNDONE```          | Cash receipt undone.                                                                         |
  | ```PAYMENT_CHARGEBACK_DISPUTE```                | In chargeback dispute (if documents are presented for dispute).                              |
  | ```PAYMENT_DUNNING_RECEIVED```                  | Receipt of negative rating.                                                                  |
  | ```PAYMENT_BANK_SLIP_VIEWED```                  | Billing slip viewed by the customer.                                                         |
  | ```PAYMENT_CREDIT_CARD_CAPTURE_REFUSED```       | Card capture declined.                                                                       |
  | ```PAYMENT_SPLIT_CANCELLED```                   | Billing had a split canceled.                                                                |
  | ```PAYMENT_SPLIT_DIVERGENCE_BLOCK_FINISHED```  | Blocking of the charge amount due to split discrepancy has been finalized.                   |

  
## Socket

- ### Join Room

  `/sockets/Room`

  Whenever a **user** joins an **auction**, all **participants** in that auction should be **notified**.

  This **notification** will be sent via **Socket.IO**, using the `"join_room"` **event**.

  The **event** receives the following **content**:

  ```js
  {
    room_id: INT;
  }
  ```

  When a **user** connects to the **auction**, the **server** will send a **message** to all **clients**:

  - In the `"server_content"` **event**  
  - Specifically in the **room** corresponding to the **auction** the **user** joined

  This allows the **frontend** to display **updated information** in **real time**.

  The only required **parameter** is the **auction ID**, which will be sent in a **JSON** object.

  The **event** receives the following **content** and will return a **JSON**:
  ```js
  {
      type:         "entry",
      room_id:      STR,
      username:     STR
  }
  ```

  Here's a **JavaScript example**:

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


- ### Bid

  `/socket/Room`

  Whenever a **user** **bids** in an **auction**, all **participants** in that **auction** should be **notified**.

  The **event** receives the following **content**:

  ```js
  {
    room_id:    STR
    user_id:    INT,
    value:      FLT | DBL,
    product_id: INT
  }
  ```

  This **notification** will be sent via **Socket.IO** using the `"emit_bid"` **event**.

  When a **user** **bids**, the **server** will send a **message** to all **clients**:

  - In the `"server_content"` **event**  
  - Specifically in the **room** corresponding to the **auction** the **user** is in

  This allows the **frontend** to display **updated information** in **real time**.

  The **event** will return a **JSON** response:

  ```js
  {
      type:           "bid",
      room_id:        STR,
      username:       STR,
      value:          FLT | DBL,

  }
  ```

  Here's a **JavaScript example**:

  ```html
  <script src="/socket.io/socket.io.js"></script>
  <script>

    const socket = io();

    function sendBid(value, product_id) {
      socket.emit("emit_bid", {
        value = value,
        product_id = product_id
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

- ### Make Bid

  `/myapp/services/BidServices`

  After the **validations** of the received **data**, the **function** `make_bid(user_id, product_id, value)` is called.  
  It retrieves the **last bid** and validates it against the **user's account balance** and whether the **value** is greater than the **minimum**.  
  If everything is valid, the **bid** is **sent to the database**.

- ### Close Auction

  `/sockets/CloseRoom`

  Whenever an **auction** is created, it will have a **predetermined time limit** to close.  
  However, if a **user** makes a **bid** in the last minutes, the **time limit** resets:  
  - Whenever a **bid** is made in the last 2 minutes, the **time limit** resets to 2 minutes.

  The **function** `close_auction(id_auction)`:

  - Removes all **participants** from the **socket room**  
  - Deletes the **auction**  
  - Changes its **status**

  To manage the timer, the **function** `start_auction_timer(auction_id, seconds)` calls `close_auction()` after the defined **time**.  
  If a **bid** is made in the final minutes, the **function** `add_time_to_action(id_auction, seconds)` is called.  

  In extreme cases or **exceptions**, such as a **server crash**, the **function** `restart()` must be called, which **resets all auctions in the database** on the **timer**.

  The **function** `close_auction(id_auction)` calls the **function** `set_winner(product)`, which:

  - Retrieves the **last valid bid** made (e.g., in cases of continuous purchases)  
  - Records and adds **discounts** to the **database**  
  - Creates a new **payment**, defining the **item transaction** and **value**

## Logout

## Security

## Modules

| Category       | File                                         | Function                                   |
| -------------- | -------------------------------------------- | ------------------------------------------ |
| Database       | `setup/InitSqlAlchemy.py`                    | Initializes the connection and ORM         |
| Tables         | `setup/createTables.py`                      | Creates the model tables                   |
| Sockets        | `setup/InitSocket.py`                        | Configures the Socket.IO server            |
| Authentication | `setup/PermissionRequire.py`                 | Permission-checking middleware             |
| Initialization | `initExtensions.py`                          | Loads Flask extensions (DB, Login, Socket) |
| HTTP Errors    | `templates/401.html`, `403.html`, `404.html` | Standard HTTP error handling               |

## Configuration and Deployment
  First, you must clone and entry the repository.
  ```bash
  git clone https://github.com/devDaviHtrb/AuctionProject
  cd AuctionProject
  ```

  For any of the following ways to run the project, the following .env file (environment variables) is required:

  ```env
  # -----------------------
  # API LINK (URL)
  # -----------------------
  URL_API =         https://asaas.com/api/v3
  SANDBOX_URL_API = https://api-sandbox.asaas.com/v3
  PAYMENT_LINK =    # YOUR PAYMENT LINK

  # -----------------------
  # API TOKEN
  # -----------------------
  API_TOKEN =         # YOUR ASAAS TOKEN API
  SANDBOX_API_TOKEN = # ONLY DEBUG

  # -----------------------
  #BANK ID
  # -----------------------
  ASAAS_WALLET_ID = # YOUR ASAAS WALLET ID

  # -----------------------
  #TOKEN FOR OUR API
  # -----------------------
  INTERNAL_TOKEN_API =  # A TOKEN FOR WEBHOOK

  # -----------------------
  #DATABASE
  # -----------------------
  SQLALCHEMY_DATABASE_URI = # YOUR DATABSE LINK
  POSTGRES_USER =           # YOUR DATABASE USER
  POSTGRES_PASSWORD =       # YOUR DATABASE PASSWORD
  POSTGRES_DB =             # YOUR DATABASE NAME
  POSTGRES_PORT =           5432
  CLOUDINARY_CLOUD_NAME =   # NAME OF IMAGE API
  CLOUDINARY_API_KEY =      # IMAGE API KEY
  CLOUDINARY_API_SECRET =   # IMAGE API SECRET

  # -----------------------
  # EMAIL
  # -----------------------
  CORPORATION_EMAIL =     # YOUR EMAIL
  CORPORATION_PASSWORD =  # YOUR PASSWORD
  GOOGLE_CLIENT_ID =      # YOUR CLIENT ID OF GOOGLE API
  GOOGLE_SECRECT =        # YOUR SECRETS FOR GOOGLE API
  GOOGLE_PROJECT_ID =     # YOUR PROJECT ID FOR GOOGLE API
  GOOGLE_REDIRECT_URIS =  # YOUR REDIRECT LINK FOR LOGIN WITH GOOGLE API

  # -----------------------
  #FLASK
  # -----------------------
  FLASK_ENV = development
  HOST =      0.0.0.0
  PORT =      5000
  DEBUG =     False
  ```

- ### Python Run
    
    This option is ideal for local development..

    - Python 3.9+ installed
    - `pip` updated
    - PostgreSQL database running

    ```bash
    # Create and activate a virtual environment.
    python3 -m venv venv
    source venv/bin/activate   # (Linux/Mac)
    venv\Scripts\activate      # (Windows)

    # Install the dependencies.
    pip install -r requirements.txt

    # Configure the .env file (see section above)

    # Run the Flask application.
    python3 app.py
    ```

    The application will be available at: http://localhost:5000

- ### Docker Run
    
    You must have Docker installed so you can run it:
    ```bash
    docker-compose build
    #docker-compose down -v #FOR RECREATE DATABASE
    docker-compose up -d
    ```

    If you don't want to build it manually, you can get it from Docker Hub:

    ```bash
    docker pull arturregadas/auctionproject:latest
    docker-compose up -d # FOR POSTGRESQL
    ```

    The application will be available at: http://localhost:5000

## The Team
