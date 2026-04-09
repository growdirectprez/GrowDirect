-- =============================================================================
-- GrowDirect Platform — Memory Database Initialization
-- =============================================================================
-- Platform-level knowledge store. Used by the memory-bus MCP server.
--
-- Tables are managed by Alembic (services/memory-bus/migrations/)
-- Run: cd services/memory-bus && alembic upgrade head
--
-- Runs after 01-create-databases.sql.
-- =============================================================================

\c growdirect_memory;

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

GRANT ALL ON ALL TABLES IN SCHEMA public TO growdirect;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO growdirect;

-- =============================================================================
-- Test database — extensions only (schema managed by Alembic)
-- =============================================================================

\c growdirect_memory_test;

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

GRANT ALL ON ALL TABLES IN SCHEMA public TO growdirect;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO growdirect;
