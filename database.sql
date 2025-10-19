
-- === SQL CREATE TABLES ===

CREATE TABLE case_types (
	case_type_id SERIAL NOT NULL, 
	case_type_name VARCHAR(10) NOT NULL, 
	PRIMARY KEY (case_type_id)
)



CREATE TABLE categories (
	category_id SERIAL NOT NULL, 
	category_name VARCHAR(80) NOT NULL, 
	PRIMARY KEY (category_id)
)



CREATE TABLE payment_methods (
	payment_method_id SERIAL NOT NULL, 
	payment_method VARCHAR(20) NOT NULL, 
	PRIMARY KEY (payment_method_id)
)



CREATE TABLE payment_statuses (
	payment_status_id SERIAL NOT NULL, 
	payment_status VARCHAR(20) NOT NULL, 
	PRIMARY KEY (payment_status_id)
)



CREATE TABLE product_statuses (
	product_status_id SERIAL NOT NULL, 
	product_status VARCHAR(20) NOT NULL, 
	PRIMARY KEY (product_status_id)
)



CREATE TABLE technical_features (
	technical_feature_id SERIAL NOT NULL, 
	technical_feature_name VARCHAR(80) NOT NULL, 
	PRIMARY KEY (technical_feature_id)
)



CREATE TABLE users (
	user_id SERIAL NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	username VARCHAR(50) NOT NULL, 
	password VARCHAR(400) NOT NULL, 
	email VARCHAR(255) NOT NULL, 
	cpf CHAR(11), 
	photo VARCHAR(255), 
	cellphone1 CHAR(14), 
	cellphone2 CHAR(14), 
	landline CHAR(13), 
	wallet DECIMAL(10, 2) NOT NULL, 
	admin_user BOOLEAN NOT NULL, 
	active_auction_number SMALLINT NOT NULL, 
	password_token_expiration_datetime TIMESTAMP WITHOUT TIME ZONE, 
	api_token VARCHAR(255), 
	password_token VARCHAR(255), 
	PRIMARY KEY (user_id)
)



CREATE TABLE addresses (
	address_id SERIAL NOT NULL, 
	street_name VARCHAR(255) NOT NULL, 
	street_number VARCHAR(6) NOT NULL, 
	apt VARCHAR(80), 
	zip_code CHAR(9) NOT NULL, 
	district VARCHAR(80) NOT NULL, 
	city VARCHAR(80) NOT NULL, 
	state CHAR(2) NOT NULL, 
	principal_address BOOLEAN NOT NULL, 
	user_id INTEGER, 
	PRIMARY KEY (address_id), 
	FOREIGN KEY(user_id) REFERENCES users (user_id)
)



CREATE TABLE category_technical_features (
	technical_feature_id INTEGER NOT NULL, 
	category_id INTEGER NOT NULL, 
	PRIMARY KEY (technical_feature_id, category_id), 
	FOREIGN KEY(technical_feature_id) REFERENCES technical_features (technical_feature_id), 
	FOREIGN KEY(category_id) REFERENCES categories (category_id)
)



CREATE TABLE legal_persons (
	user_id INTEGER NOT NULL, 
	cnpj VARCHAR(70) NOT NULL, 
	state_tax_registration CHAR(17), 
	legal_business_name VARCHAR(255) NOT NULL, 
	trade_name VARCHAR(255) NOT NULL, 
	scrap_purchase_authorization BOOLEAN NOT NULL, 
	PRIMARY KEY (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (user_id) ON DELETE CASCADE
)



CREATE TABLE payments (
	payment_id SERIAL NOT NULL, 
	amount DECIMAL(10, 2) NOT NULL, 
	payment_method INTEGER, 
	payment_status INTEGER, 
	payer VARCHAR(255) NOT NULL, 
	payee VARCHAR(255) NOT NULL, 
	opening_datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	due_datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	confirmation_datetime TIMESTAMP WITHOUT TIME ZONE, 
	user_id INTEGER, 
	PRIMARY KEY (payment_id), 
	FOREIGN KEY(payment_method) REFERENCES payment_methods (payment_method_id), 
	FOREIGN KEY(payment_status) REFERENCES payment_statuses (payment_status_id), 
	FOREIGN KEY(user_id) REFERENCES users (user_id)
)



CREATE TABLE physical_persons (
	user_id INTEGER NOT NULL, 
	rg VARCHAR(12), 
	birth_date DATE, 
	gender VARCHAR(20), 
	PRIMARY KEY (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (user_id) ON DELETE CASCADE
)



CREATE TABLE settings (
	setting_id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	anonymous_mode BOOLEAN NOT NULL, 
	two_factor_auth BOOLEAN NOT NULL, 
	PRIMARY KEY (setting_id), 
	FOREIGN KEY(user_id) REFERENCES users (user_id) ON DELETE CASCADE
)



CREATE TABLE products (
	product_id SERIAL NOT NULL, 
	product_name VARCHAR(255) NOT NULL, 
	product_room VARCHAR(64) NOT NULL, 
	description TEXT, 
	min_bid DECIMAL(12, 2) NOT NULL, 
	start_datetime TIMESTAMP WITHOUT TIME ZONE, 
	product_status INTEGER, 
	street_name VARCHAR(255), 
	street_number VARCHAR(6), 
	apt VARCHAR(80), 
	zip_code CHAR(9), 
	district VARCHAR(80), 
	city VARCHAR(80), 
	state CHAR(2), 
	user_id INTEGER, 
	category_technical_feature_id INTEGER, 
	category INTEGER, 
	end_datetime TIMESTAMP WITHOUT TIME ZONE, 
	duration INTEGER NOT NULL, 
	PRIMARY KEY (product_id), 
	UNIQUE (product_room), 
	FOREIGN KEY(product_status) REFERENCES product_statuses (product_status_id), 
	FOREIGN KEY(user_id) REFERENCES users (user_id), 
	FOREIGN KEY(category_technical_feature_id) REFERENCES category_technical_features (technical_feature_id), 
	FOREIGN KEY(category) REFERENCES categories (category_id)
)



CREATE TABLE bids (
	bid_id SERIAL NOT NULL, 
	bid_value DECIMAL(12, 2) NOT NULL, 
	bid_datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	winner BOOLEAN NOT NULL, 
	user_id INTEGER, 
	product_id INTEGER, 
	PRIMARY KEY (bid_id), 
	FOREIGN KEY(user_id) REFERENCES users (user_id), 
	FOREIGN KEY(product_id) REFERENCES products (product_id)
)



CREATE TABLE images (
	image_id SERIAL NOT NULL, 
	image VARCHAR(255) NOT NULL, 
	principal_image BOOLEAN NOT NULL, 
	product_id INTEGER, 
	PRIMARY KEY (image_id), 
	FOREIGN KEY(product_id) REFERENCES products (product_id)
)



CREATE TABLE legal_infos (
	legal_infos_id SERIAL NOT NULL, 
	process_number CHAR(25) NOT NULL, 
	court VARCHAR(255) NOT NULL, 
	case_type INTEGER, 
	plaintiff VARCHAR(255) NOT NULL, 
	defendant VARCHAR(255) NOT NULL, 
	judge_name VARCHAR(255) NOT NULL, 
	extra_notes TEXT, 
	product_id INTEGER, 
	PRIMARY KEY (legal_infos_id), 
	FOREIGN KEY(case_type) REFERENCES case_types (case_type_id), 
	FOREIGN KEY(product_id) REFERENCES products (product_id)
)



CREATE TABLE technical_features_values (
	technical_feature_id INTEGER NOT NULL, 
	category_id INTEGER NOT NULL, 
	value VARCHAR(255) NOT NULL, 
	product_id INTEGER NOT NULL, 
	PRIMARY KEY (technical_feature_id, category_id, product_id), 
	FOREIGN KEY(technical_feature_id) REFERENCES technical_features (technical_feature_id), 
	FOREIGN KEY(category_id) REFERENCES categories (category_id), 
	FOREIGN KEY(product_id) REFERENCES products (product_id)
)


