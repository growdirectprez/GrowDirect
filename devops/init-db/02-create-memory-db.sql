-- =============================================================================
-- GrowDirect Platform — Memory Database Initialization (GRO-172)
-- =============================================================================
-- Platform-level knowledge store. Replaces canary_memory (GRO-165).
-- Used by the memory-bus MCP server for all GrowDirect apps.
--
-- Tables:
--   alx_sessions     — session lifecycle tracking
--   alx_memories     — memories with pgvector embeddings + layer tagging
--   seed_embeddings  — curated knowledge base
--
-- Runs after 01-create-databases.sql.
-- =============================================================================

\c growdirect_memory;

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ----- alx_sessions -----

CREATE TABLE IF NOT EXISTS alx_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      TEXT NOT NULL UNIQUE,
    started_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    closed_at       TIMESTAMPTZ,
    status          TEXT NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'closed', 'abandoned')),
    gro_issues      JSONB,
    summary         TEXT,
    decisions       JSONB,
    unresolved      JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_alx_sessions_status ON alx_sessions(status);
CREATE INDEX IF NOT EXISTS idx_alx_sessions_started ON alx_sessions(started_at DESC);

-- ----- alx_memories -----

CREATE TABLE IF NOT EXISTS alx_memories (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      TEXT NOT NULL,
    memory_type     TEXT NOT NULL
                    CHECK (memory_type IN (
                        'decision', 'finding', 'context', 'architecture',
                        'session_summary', 'procedure', 'context_block',
                        'work_product', 'team_profile', 'foundation'
                    )),
    content         TEXT NOT NULL,
    metadata        JSONB,
    embedding       vector(1024),
    layer           TEXT NOT NULL DEFAULT 'shared'
                    CHECK (layer IN ('corp', 'canary', 'cove', 'shared')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_alx_memories_session ON alx_memories(session_id);
CREATE INDEX IF NOT EXISTS idx_alx_memories_type ON alx_memories(memory_type);
CREATE INDEX IF NOT EXISTS idx_alx_memories_created ON alx_memories(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_alx_memories_layer ON alx_memories(layer);

-- ----- seed_embeddings -----

CREATE TABLE IF NOT EXISTS seed_embeddings (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_file     TEXT NOT NULL,
    section_path    TEXT NOT NULL,
    content         TEXT NOT NULL,
    embedding       vector(1024) NOT NULL,
    metadata        JSONB,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_seed_embeddings_vector
    ON seed_embeddings USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_seed_embeddings_source
    ON seed_embeddings(source_file);

-- ----- updated_at trigger -----

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_alx_sessions_updated_at
    BEFORE UPDATE ON alx_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_alx_memories_updated_at
    BEFORE UPDATE ON alx_memories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_seed_embeddings_updated_at
    BEFORE UPDATE ON seed_embeddings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

GRANT ALL ON ALL TABLES IN SCHEMA public TO growdirect;

-- =============================================================================
-- Test database — identical schema
-- =============================================================================

\c growdirect_memory_test;

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS alx_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      TEXT NOT NULL UNIQUE,
    started_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    closed_at       TIMESTAMPTZ,
    status          TEXT NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'closed', 'abandoned')),
    gro_issues      JSONB,
    summary         TEXT,
    decisions       JSONB,
    unresolved      JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_alx_sessions_status ON alx_sessions(status);
CREATE INDEX IF NOT EXISTS idx_alx_sessions_started ON alx_sessions(started_at DESC);

CREATE TABLE IF NOT EXISTS alx_memories (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      TEXT NOT NULL,
    memory_type     TEXT NOT NULL
                    CHECK (memory_type IN (
                        'decision', 'finding', 'context', 'architecture',
                        'session_summary', 'procedure', 'context_block',
                        'work_product', 'team_profile', 'foundation'
                    )),
    content         TEXT NOT NULL,
    metadata        JSONB,
    embedding       vector(1024),
    layer           TEXT NOT NULL DEFAULT 'shared'
                    CHECK (layer IN ('corp', 'canary', 'cove', 'shared')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_alx_memories_session ON alx_memories(session_id);
CREATE INDEX IF NOT EXISTS idx_alx_memories_type ON alx_memories(memory_type);
CREATE INDEX IF NOT EXISTS idx_alx_memories_created ON alx_memories(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_alx_memories_layer ON alx_memories(layer);

CREATE TABLE IF NOT EXISTS seed_embeddings (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_file     TEXT NOT NULL,
    section_path    TEXT NOT NULL,
    content         TEXT NOT NULL,
    embedding       vector(1024) NOT NULL,
    metadata        JSONB,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_seed_embeddings_vector
    ON seed_embeddings USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_seed_embeddings_source
    ON seed_embeddings(source_file);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_alx_sessions_updated_at
    BEFORE UPDATE ON alx_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_alx_memories_updated_at
    BEFORE UPDATE ON alx_memories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_seed_embeddings_updated_at
    BEFORE UPDATE ON seed_embeddings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

GRANT ALL ON ALL TABLES IN SCHEMA public TO growdirect;
