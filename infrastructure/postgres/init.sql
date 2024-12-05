-- Check if the database exists and create it if not
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = current_setting('POSTGRES_DB')) THEN
        EXECUTE format('CREATE DATABASE %I', current_setting('POSTGRES_DB'));
    END IF;
END $$;

-- Check if the user exists and create it if not
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = current_setting('POSTGRES_USER')) THEN
        EXECUTE format('CREATE USER %I WITH PASSWORD %L', current_setting('POSTGRES_USER'), current_setting('POSTGRES_PASSWORD'));
    END IF;
END $$;

-- Set role settings for the user
DO $$
BEGIN
    EXECUTE format('ALTER ROLE %I SET client_encoding TO ''utf8''', current_setting('POSTGRES_USER'));
    EXECUTE format('ALTER ROLE %I SET default_transaction_isolation TO ''read committed''', current_setting('POSTGRES_USER'));
    EXECUTE format('ALTER ROLE %I SET timezone TO ''UTC''', current_setting('POSTGRES_USER'));
END $$;

-- Grant all privileges on the database to the user
DO $$
BEGIN
    EXECUTE format('GRANT ALL PRIVILEGES ON DATABASE %I TO %I', current_setting('POSTGRES_DB'), current_setting('POSTGRES_USER'));
END $$;
