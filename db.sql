CREATE DATABASE roulete;

CREATE USER roulete_admin WITH PASSWORD '1234abcd';

ALTER ROLE roulete_admin SET client_encoding TO 'utf8';
ALTER ROLE roulete_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE roulete_admin SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE Roulete TO roulete_admin;