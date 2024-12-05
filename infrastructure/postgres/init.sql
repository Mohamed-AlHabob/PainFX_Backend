-- Check if the database exists and create it if not
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'authen_db') THEN
        CREATE DATABASE authen_db;
    END IF;
END
$$;

-- Connect to the new database
\c authen_db;

-- Check if the user exists and create it if not
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'authen_user') THEN
        CREATE USER authen_user WITH PASSWORD 'mohamed';
    END IF;
END
$$;

-- Set role settings for the user
ALTER ROLE authen_user SET client_encoding TO 'utf8';
ALTER ROLE authen_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE authen_user SET timezone TO 'UTC';

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON DATABASE authen_db TO authen_user;
