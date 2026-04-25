# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from memory_bus.config import Config
from memory_bus.embeddings import get_embedding

logger = logging.getLogger(__name__)

VALID_MEMORY_TYPES = frozenset([
    "decision", "finding", "context", "architecture",
    "session_summary", "procedure", "context_block",
    "work_product", "team_profile", "foundation",
])

VALID_LAYERS = frozenset(["corp", "canary", "shared"])

VALID_DOMAINS = frozenset([
    "identity", "tsp", "chirp", "alert", "owl",
    "fox", "analytics", "alx", "raas", "ops", "ui_bff",
])

VALID_BLOCK_TYPES = frozenset([
    "domain_overview", "workflow", "data_model", "api_contract",
])


class MemoryStore:
    """Core storage and retrieval operations for the memory bus."""

    def __init__(self, config: Config):
        self._config = config
        self._engine = create_engine(
            config.database_url,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
        )
        self._session_factory = sessionmaker(bind=self._engine)

    def _session(self) -> Session:
        return self._session_factory()

    def healthy(self) -> bool:
        """Check database connectivity."""
        try:
            with self._session() as session:
                session.execute(text("SELECT 1"))
                return True
        except Exception:
            return False

    # -----------------------------------------------------------------
    # Session lifecycle
    # -----------------------------------------------------------------

    def session_start(
        self, gro_issues: Optional[list[str]] = None
    ) -> dict[str, Any]:
        """Create a new session and assemble startup context."""
        session_id = f"alx-{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc)
        gro_list = gro_issues or []

        with self._session() as db:
            db.execute(
                text("""
                    INSERT INTO alx_sessions
                        (id, session_id, started_at, status, gro_issues, created_at)
                    VALUES
                        (:id, :sid, :now, 'active', :gro, :now)
                """),
                {
                    "id": str(uuid.uuid4()),
                    "sid": session_id,
                    "now": now,
                    "gro": json.dumps(gro_list),
                },
            )
            db.commit()

        context = self._assemble_startup_context(gro_list)
        return {
            "session_id": session_id,
            "status": "active",
            "started_at": now.isoformat(),
            "gro_issues": gro_list,
            "startup_context": context,
        }

    def session_close(
        self,
        session_id: str,
        summary: str,
        decisions: Optional[list[str]] = None,
        unresolved: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """Close a session with summary and decisions."""
        now = datetime.now(timezone.utc)

        with self._session() as db:
            result = db.execute(
                text("""
                    UPDATE alx_sessions
                    SET status = 'closed',
                        closed_at = :now,
                        summary = :summary,
                        decisions = :decisions,
                        unresolved = :unresolved,
                        updated_at = :now
                    WHERE session_id = :sid AND status = 'active'
                    RETURNING session_id
                """),
                {
                    "sid": session_id,
                    "now": now,
                    "summary": summary,
                    "decisions": json.dumps(decisions or []),
                    "unresolved": json.dumps(unresolved or []),
                },
            )
            row = result.fetchone()
            db.commit()

            if not row:
                return {"error": f"No active session found: {session_id}"}

        # Store summary as memory
        self.memory_store(
            session_id=session_id,
            content=summary,
            memory_type="session_summary",
        )

        return {
            "session_id": session_id,
            "status": "closed",
            "closed_at": now.isoformat(),
            "summary": summary,
        }

    def _assemble_startup_context(self, gro_issues: list[str]) -> str:
        """Build startup context from recent memories and decisions."""
        parts = []
        with self._session() as db:
            rows = db.execute(
                text("""
                    SELECT content, created_at
                    FROM alx_memories
                    WHERE memory_type = 'decision'
                    ORDER BY created_at DESC LIMIT 5
                """)
            ).fetchall()
            if rows:
                parts.append("## Recent Decisions")
                for row in rows:
                    parts.append(f"- {row[0]}")

            for gro in gro_issues:
                gro_rows = db.execute(
                    text("""
                        SELECT content, memory_type
                        FROM alx_memories
                        WHERE content ILIKE :pattern
                        ORDER BY created_at DESC LIMIT 3
                    """),
                    {"pattern": f"%{gro}%"},
                ).fetchall()
                if gro_rows:
                    parts.append(f"\n## Context for {gro}")
                    for row in gro_rows:
                        parts.append(f"- [{row[1]}] {row[0][:200]}")

        return "\n".join(parts) if parts else "No prior context found."

    # -----------------------------------------------------------------
    # Memory operations
    # -----------------------------------------------------------------

    def memory_store(
        self,
        session_id: str,
        content: str,
        memory_type: str = "context",
        metadata: Optional[dict[str, Any]] = None,
        layer: str = "shared",
    ) -> dict[str, Any]:
        """Persist a memory with optional embedding and layer tag."""
        if memory_type not in VALID_MEMORY_TYPES:
            return {"error": f"Invalid memory_type: {memory_type}. Valid: {sorted(VALID_MEMORY_TYPES)}"}
        if layer not in VALID_LAYERS:
            return {"error": f"Invalid layer: {layer}. Valid: {sorted(VALID_LAYERS)}"}

        memory_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        embedding = get_embedding(content, self._config)

        with self._session() as db:
            # Validate session exists (enforces FK integrity at application level)
            session_check = db.execute(
                text("SELECT 1 FROM alx_sessions WHERE session_id = :sid"),
                {"sid": session_id},
            ).fetchone()
            if not session_check:
                return {"error": f"Session '{session_id}' does not exist — call session_start first"}

            if embedding:
                db.execute(
                    text("""
                        INSERT INTO alx_memories
                            (id, session_id, memory_type, content, metadata,
                             embedding, layer, created_at, updated_at)
                        VALUES
                            (:id, :sid, :mtype, :content, :meta,
                             :embedding, :layer, :now, :now)
                    """),
                    {
                        "id": memory_id,
                        "sid": session_id,
                        "mtype": memory_type,
                        "content": content,
                        "meta": json.dumps(metadata or {}),
                        "embedding": str(embedding),
                        "layer": layer,
                        "now": now,
                    },
                )
            else:
                db.execute(
                    text("""
                        INSERT INTO alx_memories
                            (id, session_id, memory_type, content, metadata,
                             layer, created_at, updated_at)
                        VALUES
                            (:id, :sid, :mtype, :content, :meta,
                             :layer, :now, :now)
                    """),
                    {
                        "id": memory_id,
                        "sid": session_id,
                        "mtype": memory_type,
                        "content": content,
                        "meta": json.dumps(metadata or {}),
                        "layer": layer,
                        "now": now,
                    },
                )
            db.commit()

        return {
            "memory_id": memory_id,
            "memory_type": memory_type,
            "layer": layer,
            "has_embedding": embedding is not None,
            "created_at": now.isoformat(),
        }

    def memory_recall(
        self,
        query: str,
        limit: int = 10,
        memory_type: Optional[str] = None,
        layer: Optional[str] = None,
    ) -> dict[str, Any]:
        """Semantic search with fallback chain: vector -> full-text -> ILIKE.

        Args:
            layer: Filter by memory layer (corp/canary/shared).
                   None returns all layers.
        """
        embedding = get_embedding(query, self._config)

        # Build optional filters
        filters = []
        filter_params: dict[str, Any] = {}
        if memory_type:
            filters.append("AND memory_type = :mtype")
            filter_params["mtype"] = memory_type
        if layer:
            filters.append("AND layer = :layer")
            filter_params["layer"] = layer
        extra_where = " ".join(filters)

        with self._session() as db:
            # Tier 1: pgvector cosine similarity
            if embedding:
                rows = db.execute(
                    text(f"""
                        SELECT id, session_id, memory_type, content, metadata,
                               layer, created_at,
                               1 - (embedding <=> :embedding::vector) AS similarity
                        FROM alx_memories
                        WHERE embedding IS NOT NULL {extra_where}
                        ORDER BY embedding <=> :embedding::vector
                        LIMIT :limit
                    """),
                    {"embedding": str(embedding), "limit": limit, **filter_params},
                ).fetchall()

                if rows:
                    return self._format_recall_results(rows, "vector", query)

            # Tier 2: Full-text search
            rows = db.execute(
                text(f"""
                    SELECT id, session_id, memory_type, content, metadata,
                           layer, created_at,
                           ts_rank(to_tsvector('english', content),
                                   plainto_tsquery('english', :query)) AS similarity
                    FROM alx_memories
                    WHERE to_tsvector('english', content) @@
                          plainto_tsquery('english', :query) {extra_where}
                    ORDER BY similarity DESC
                    LIMIT :limit
                """),
                {"query": query, "limit": limit, **filter_params},
            ).fetchall()

            if rows:
                return self._format_recall_results(rows, "fulltext", query)

            # Tier 3: ILIKE fallback
            rows = db.execute(
                text(f"""
                    SELECT id, session_id, memory_type, content, metadata,
                           layer, created_at, 0.0 AS similarity
                    FROM alx_memories
                    WHERE content ILIKE :pattern {extra_where}
                    ORDER BY created_at DESC
                    LIMIT :limit
                """),
                {"pattern": f"%{query}%", "limit": limit, **filter_params},
            ).fetchall()

            return self._format_recall_results(rows, "ilike", query)

    def _format_recall_results(
        self, rows: list, source: str, query: str
    ) -> dict[str, Any]:
        """Format recall results into standard response dict."""
        matches = []
        for row in rows:
            matches.append({
                "memory_id": str(row[0]),
                "session_id": row[1],
                "memory_type": row[2],
                "content": row[3],
                "metadata": row[4] if row[4] else {},
                "layer": row[5],
                "created_at": row[6].isoformat() if row[6] else None,
                "similarity": float(row[7]) if row[7] else 0.0,
            })
        return {
            "query": query,
            "matches": matches,
            "count": len(matches),
            "source": source,
        }

    def memory_search(
        self,
        session_id: Optional[str] = None,
        memory_type: Optional[str] = None,
        since: Optional[str] = None,
        layer: Optional[str] = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Structured search by session, type, date, or layer."""
        with self._session() as db:
            conditions = []
            params: dict[str, Any] = {"limit": limit}

            if session_id:
                conditions.append("session_id = :sid")
                params["sid"] = session_id
            if memory_type:
                conditions.append("memory_type = :mtype")
                params["mtype"] = memory_type
            if since:
                conditions.append("created_at >= :since")
                params["since"] = since
            if layer:
                conditions.append("layer = :layer")
                params["layer"] = layer

            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

            rows = db.execute(
                text(f"""
                    SELECT id, session_id, memory_type, content, metadata,
                           layer, created_at
                    FROM alx_memories
                    {where_clause}
                    ORDER BY created_at DESC
                    LIMIT :limit
                """),
                params,
            ).fetchall()

            memories = [
                {
                    "memory_id": str(r[0]),
                    "session_id": r[1],
                    "memory_type": r[2],
                    "content": r[3],
                    "metadata": r[4] if isinstance(r[4], dict) else (json.loads(r[4]) if r[4] else {}),
                    "layer": r[5],
                    "created_at": r[6].isoformat() if r[6] else None,
                }
                for r in rows
            ]

            return {
                "memories": memories,
                "count": len(memories),
                "filters": {
                    "session_id": session_id,
                    "memory_type": memory_type,
                    "since": since,
                    "layer": layer,
                },
            }

    def context_assemble(
        self,
        topic: Optional[str] = None,
        gro_issue: Optional[str] = None,
        limit: int = 15,
    ) -> dict[str, Any]:
        """Assemble a context window for a topic or GRO issue."""
        memories = []

        if gro_issue:
            result = self.memory_recall(gro_issue, limit=limit)
            memories.extend(result.get("matches", []))

        if topic and topic != gro_issue:
            result = self.memory_recall(topic, limit=limit)
            memories.extend(result.get("matches", []))

        decisions = self.memory_search(memory_type="decision", limit=5)
        memories.extend(decisions.get("memories", []))

        summaries = self.memory_search(memory_type="session_summary", limit=1)
        memories.extend(summaries.get("memories", []))

        # Deduplicate
        seen: set[str] = set()
        unique = []
        for m in memories:
            mid = m.get("memory_id")
            if mid and mid not in seen:
                seen.add(mid)
                unique.append(m)

        context_lines = ["## ALX Memory Context", ""]

        summaries_list = summaries.get("memories", [])
        if summaries_list:
            last = summaries_list[0]
            context_lines.append(f"### Last Session ({last.get('created_at', 'unknown')})")
            context_lines.append(last.get("content", ""))
            context_lines.append("")

        decision_mems = [m for m in unique if m.get("memory_type") == "decision"]
        if decision_mems:
            context_lines.append("### Recent Decisions")
            for d in decision_mems[:5]:
                context_lines.append(f"- {d.get('content', '')}")
            context_lines.append("")

        other_mems = [m for m in unique if m.get("memory_type") not in ("decision", "session_summary")]
        if other_mems:
            context_lines.append("### Related Context")
            for m in other_mems[:10]:
                context_lines.append(f"- [{m.get('memory_type', 'context')}] {m.get('content', '')}")
            context_lines.append("")

        return {
            "context": "\n".join(context_lines),
            "memory_count": len(unique),
            "topic": topic,
            "gro_issue": gro_issue,
            "sources": [m.get("memory_id") for m in unique],
        }

    def domain_context(
        self,
        domain: str,
        topic: Optional[str] = None,
        token_budget: int = 4000,
    ) -> dict[str, Any]:
        """Full domain context assembly with token budget."""
        if domain not in VALID_DOMAINS:
            return {"error": f"Unknown domain: {domain}. Must be one of: {sorted(VALID_DOMAINS)}"}

        char_budget = token_budget * 4
        sections: list[tuple[str, str]] = []
        blocks_used: list[str] = []
        total_chars = 0

        overviews = self._recall_context_blocks(domain, "domain_overview")
        if overviews:
            block = overviews[0]
            sections.append(("Overview", block["content"]))
            blocks_used.append("domain_overview")
            total_chars += len(block["content"])

        contracts = self._recall_context_blocks(domain, "api_contract")
        if contracts:
            block = contracts[0]
            sections.append(("API Contract", block["content"]))
            blocks_used.append("api_contract")
            total_chars += len(block["content"])

        if topic:
            workflows = self._recall_context_blocks(domain, "workflow")
            if workflows:
                best = self._pick_best_workflow(workflows, topic)
                if best and total_chars + len(best["content"]) <= char_budget:
                    sections.append(("Workflow", best["content"]))
                    blocks_used.append("workflow")
                    total_chars += len(best["content"])
                elif best:
                    remaining = char_budget - total_chars
                    if remaining > 200:
                        truncated = best["content"][:remaining] + "\n\n[...truncated to fit token budget]"
                        sections.append(("Workflow", truncated))
                        blocks_used.append("workflow (truncated)")
                        total_chars += remaining

        if total_chars < char_budget - 400:
            data_models = self._recall_context_blocks(domain, "data_model")
            if data_models:
                block = data_models[0]
                remaining = char_budget - total_chars
                content = block["content"]
                if len(content) <= remaining:
                    sections.append(("Data Model", content))
                    blocks_used.append("data_model")
                elif remaining > 200:
                    sections.append(("Data Model", content[:remaining] + "\n\n[...truncated]"))
                    blocks_used.append("data_model (truncated)")

        lines = [f"## {domain.replace('_', ' ').title()} Domain Context", ""]
        for heading, content in sections:
            lines.append(f"### {heading}")
            lines.append(content)
            lines.append("")

        if not sections:
            lines.append("_No context blocks found for this domain. Run seed_context_blocks.py to populate._")
            lines.append("")

        context_text = "\n".join(lines)

        return {
            "context": context_text,
            "domain": domain,
            "topic": topic,
            "blocks_used": blocks_used,
            "token_estimate": len(context_text) // 4,
        }

    def _recall_context_blocks(
        self,
        domain: str,
        block_type: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """Retrieve context blocks for a service domain."""
        with self._session() as db:
            type_filter = ""
            params: dict[str, Any] = {"domain": domain}

            if block_type:
                type_filter = "AND metadata->>'block_type' = :block_type"
                params["block_type"] = block_type

            params["domain_jsonb"] = json.dumps(domain)

            rows = db.execute(
                text(f"""
                    SELECT id, memory_type, content, metadata, created_at
                    FROM alx_memories
                    WHERE memory_type = 'context_block'
                        AND (
                            metadata->>'domain' = :domain
                            OR metadata->'domains' @> CAST(:domain_jsonb AS jsonb)
                        )
                        {type_filter}
                    ORDER BY created_at DESC
                """),
                params,
            ).fetchall()

            return [
                {
                    "memory_id": str(r[0]),
                    "memory_type": r[1],
                    "content": r[2],
                    "metadata": json.loads(r[3]) if isinstance(r[3], str) else (r[3] or {}),
                    "created_at": r[4].isoformat() if r[4] else None,
                }
                for r in rows
            ]

    def _pick_best_workflow(
        self,
        workflows: list[dict[str, Any]],
        topic: str,
    ) -> Optional[dict[str, Any]]:
        """Pick the workflow block most relevant to the given topic."""
        topic_words = set(topic.lower().split())
        if not topic_words:
            return workflows[0] if workflows else None

        best_score = 0
        best_block = None
        for wf in workflows:
            content_lower = wf.get("content", "").lower()
            score = sum(1 for w in topic_words if w in content_lower)
            if score > best_score:
                best_score = score
                best_block = wf

        return best_block or (workflows[0] if workflows else None)
