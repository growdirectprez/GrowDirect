-- GrowDirect Shared Database Initialization
-- Runs once on first postgres container boot (idempotent — safe to re-run)
-- All app databases land in a single PostgreSQL 17 + pgvector instance.

-- Create app databases (idempotent — safe to re-run)
SELECT 'CREATE DATABASE canary OWNER growdirect'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'canary')\gexec

SELECT 'CREATE DATABASE canary_test OWNER growdirect'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'canary_test')\gexec

SELECT 'CREATE DATABASE canary_memory OWNER growdirect'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'canary_memory')\gexec

SELECT 'CREATE DATABASE cove OWNER growdirect'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'cove')\gexec

SELECT 'CREATE DATABASE cove_test OWNER growdirect'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'cove_test')\gexec

-- Enable pgvector on all databases
\c canary
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS sales;
CREATE SCHEMA IF NOT EXISTS metrics;

-- RLS helper functions
CREATE OR REPLACE FUNCTION set_current_merchant(mid TEXT) RETURNS VOID AS $$
BEGIN PERFORM set_config('canary.current_merchant_id', mid, true); END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_current_merchant() RETURNS TEXT AS $$
BEGIN RETURN current_setting('canary.current_merchant_id', true); END;
$$ LANGUAGE plpgsql;

-- Canary app roles (SOX compliance — write-path isolation)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'canary_app') THEN
        CREATE ROLE canary_app WITH LOGIN PASSWORD 'canary_app_dev_2026';
    END IF;
END
$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'canary_tsp') THEN
        CREATE ROLE canary_tsp WITH LOGIN PASSWORD 'canary_tsp_dev_2026';
    END IF;
END
$$;

GRANT ALL ON SCHEMA app TO growdirect;
GRANT ALL ON SCHEMA sales TO growdirect;
GRANT ALL ON SCHEMA metrics TO growdirect;

-- canary_app: full access to app/metrics, read-only on sales
GRANT USAGE ON SCHEMA app TO canary_app;
GRANT USAGE ON SCHEMA sales TO canary_app;
GRANT USAGE ON SCHEMA metrics TO canary_app;
GRANT USAGE ON SCHEMA public TO canary_app;
-- canary_app: full DML on app and metrics schemas
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA app
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO canary_app;
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA metrics
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO canary_app;
-- canary_app: read-only on sales
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA sales
  GRANT SELECT ON TABLES TO canary_app;
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO canary_app;
ALTER ROLE canary_app SET search_path TO app, sales, metrics, public;

-- canary_tsp: full access to sales, read-only on app
GRANT USAGE ON SCHEMA sales TO canary_tsp;
GRANT USAGE ON SCHEMA app TO canary_tsp;
GRANT USAGE ON SCHEMA public TO canary_tsp;
ALTER ROLE canary_tsp SET search_path TO sales, app, public;
-- canary_tsp: full DML on sales
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA sales
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO canary_tsp;
-- canary_tsp: read-only on app
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA app
  GRANT SELECT ON TABLES TO canary_tsp;

\c canary_test
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS sales;
CREATE SCHEMA IF NOT EXISTS metrics;

-- Grant canary_app and canary_tsp access to test database too
GRANT USAGE ON SCHEMA app TO canary_app;
GRANT USAGE ON SCHEMA sales TO canary_app;
GRANT USAGE ON SCHEMA metrics TO canary_app;
GRANT USAGE ON SCHEMA app TO canary_tsp;
GRANT USAGE ON SCHEMA sales TO canary_tsp;
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA app
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO canary_app;
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA metrics
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO canary_app;
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA sales
  GRANT SELECT ON TABLES TO canary_app;
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA sales
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO canary_tsp;
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA app
  GRANT SELECT ON TABLES TO canary_tsp;

\c canary_memory
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ALX Memory Tables (GRO-165)
CREATE TABLE IF NOT EXISTS alx_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      TEXT NOT NULL UNIQUE,
    started_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    closed_at       TIMESTAMPTZ,
    status          TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'closed', 'abandoned')),
    gro_issues      TEXT[],
    summary         TEXT,
    decisions       JSONB,
    unresolved      JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_alx_sessions_status ON alx_sessions(status);
CREATE INDEX IF NOT EXISTS idx_alx_sessions_started ON alx_sessions(started_at DESC);

CREATE TABLE IF NOT EXISTS alx_memories (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      TEXT NOT NULL,
    memory_type     TEXT NOT NULL CHECK (memory_type IN ('decision', 'finding', 'context', 'architecture', 'session_summary', 'procedure')),
    content         TEXT NOT NULL,
    metadata        JSONB,
    embedding       vector(1024),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_alx_memories_session ON alx_memories(session_id);
CREATE INDEX IF NOT EXISTS idx_alx_memories_type ON alx_memories(memory_type);
CREATE INDEX IF NOT EXISTS idx_alx_memories_created ON alx_memories(created_at DESC);

CREATE TABLE IF NOT EXISTS seed_embeddings (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_file     TEXT NOT NULL,
    section_path    TEXT NOT NULL,
    content         TEXT NOT NULL,
    embedding       vector(1024) NOT NULL,
    metadata        JSONB,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_seed_embeddings_vector
    ON seed_embeddings USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_seed_embeddings_source
    ON seed_embeddings(source_file);

GRANT ALL ON ALL TABLES IN SCHEMA public TO growdirect;
GRANT ALL ON ALL TABLES IN SCHEMA public TO canary_app;
GRANT USAGE ON SCHEMA public TO canary_app;
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO canary_app;

\c cove
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

\c cove_test
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
