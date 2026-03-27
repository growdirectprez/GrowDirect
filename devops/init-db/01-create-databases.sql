-- GrowDirect Shared Database Initialization
-- Runs once on first postgres container boot (idempotent via IF NOT EXISTS)
-- All app databases land in a single PostgreSQL 17 + pgvector instance.

-- Create app databases
CREATE DATABASE canary OWNER growdirect;
CREATE DATABASE canary_test OWNER growdirect;
CREATE DATABASE cove OWNER growdirect;
CREATE DATABASE cove_test OWNER growdirect;

-- Enable pgvector on all databases
\c canary
CREATE EXTENSION IF NOT EXISTS vector;

\c canary_test
CREATE EXTENSION IF NOT EXISTS vector;

\c cove
CREATE EXTENSION IF NOT EXISTS vector;

\c cove_test
CREATE EXTENSION IF NOT EXISTS vector;
