#!/usr/bin/env python3
"""Batch ingest all Tier 1 memories into Cognee Tier 2.

Reads all alx_memories from PostgreSQL and submits them to Cognee
for entity extraction, vector embedding, and knowledge graph enrichment.

Processes in batches to avoid overwhelming Ollama (qwen3:14b).
Each batch: cognee.add() → cognee.cognify()

Run inside container:
    python3 devops/scripts/ingest_tier2_batch.py [--batch-size 50] [--dry-run]
"""
import argparse
import asyncio
import importlib
import os
import sys
import time

sys.path.insert(0, "/app")


def patch_cognee_edge_model():
    """Runtime monkey-patch Cognee's Edge model for qwen3:14b compatibility.

    qwen3:14b generates edges as {"from": ..., "to": ...} but Cognee 0.5.3
    expects {"source_node_id": ..., "target_node_id": ...}. This creates
    patched Edge + KnowledgeGraph classes with a model_validator that remaps
    the keys, then replaces them in all Cognee modules that use them.

    Must run AFTER importing cognee but BEFORE calling cognify().
    """
    from pydantic import BaseModel, Field, model_validator
    from typing import List

    import cognee.shared.data_models as dm

    if hasattr(dm.Edge, "__validators__") or hasattr(dm.Edge, "normalize_edge_keys"):
        print("  Cognee Edge model already patched")
        return

    OrigNode = dm.Node

    class PatchedEdge(BaseModel):
        """Edge in a knowledge graph."""
        source_node_id: str
        target_node_id: str
        relationship_name: str

        @model_validator(mode="before")
        @classmethod
        def normalize_edge_keys(cls, data):
            if isinstance(data, dict):
                if "from" in data and "source_node_id" not in data:
                    data["source_node_id"] = data.pop("from")
                if "to" in data and "target_node_id" not in data:
                    data["target_node_id"] = data.pop("to")
                if "source" in data and "source_node_id" not in data:
                    data["source_node_id"] = data.pop("source")
                if "target" in data and "target_node_id" not in data:
                    data["target_node_id"] = data.pop("target")
            return data

    class PatchedKnowledgeGraph(BaseModel):
        """Knowledge graph."""
        nodes: List[OrigNode] = Field(..., default_factory=list)
        edges: List[PatchedEdge] = Field(..., default_factory=list)

    class PatchedMemorySummary(BaseModel):
        """Memory summary."""
        nodes: List[OrigNode] = Field(..., default_factory=list)
        edges: List[PatchedEdge] = Field(..., default_factory=list)

    # Replace in the data_models module
    dm.Edge = PatchedEdge
    dm.KnowledgeGraph = PatchedKnowledgeGraph
    dm.MemorySummary = PatchedMemorySummary

    # Patch all modules that import KnowledgeGraph directly
    modules_to_patch = [
        "cognee.tasks.graph.extract_graph_from_data",
        "cognee.tasks.graph.extract_graph_from_data_v2",
        "cognee.tasks.graph.cascade_extract.utils.extract_edge_triplets",
        "cognee.modules.graph.utils.expand_with_nodes_and_edges",
        "cognee.modules.graph.utils.retrieve_existing_edges",
        "cognee.api.v1.cognify.cognify",
        "cognee.api.v1.cognify.routers.get_cognify_router",
        "cognee.infrastructure.databases.graph.config",
    ]

    patched_count = 0
    for mod_name in modules_to_patch:
        try:
            mod = importlib.import_module(mod_name)
            if hasattr(mod, "KnowledgeGraph"):
                mod.KnowledgeGraph = PatchedKnowledgeGraph
                patched_count += 1
        except ImportError:
            pass

    print(f"  Cognee Edge model patched ({patched_count} modules updated)")


def init_cognee():
    """Initialize Cognee using the same config as canary.services.alx.memory."""
    from canary.services.alx.memory import _init_cognee
    _init_cognee()
    print("Cognee initialized via ALX memory layer")


def get_memories(memory_type=None, limit=None):
    """Fetch all Tier 1 memories from PostgreSQL via raw SQL."""
    from canary.services.alx.memory import _get_session
    from sqlalchemy import text

    session = _get_session()
    try:
        sql = "SELECT id, session_id, memory_type, content FROM alx_memories ORDER BY created_at"
        params = {}
        if memory_type:
            sql = "SELECT id, session_id, memory_type, content FROM alx_memories WHERE memory_type = :mt ORDER BY created_at"
            params["mt"] = memory_type
        if limit:
            sql += " LIMIT :lim"
            params["lim"] = limit

        rows = session.execute(text(sql), params).fetchall()
        return [
            {"id": str(r[0]), "session_id": r[1], "memory_type": r[2], "content": r[3]}
            for r in rows
        ]
    finally:
        session.close()


async def ingest_batch(memories, batch_num, total_batches):
    """Ingest a batch of memories into Cognee.

    Each memory is added as its own dataset to avoid exceeding nomic-embed-text's
    8192 token context window. All datasets in the batch are then cognified together.
    """
    import cognee
    from canary.services.alx.memory import _prepare_cognee_ingest

    print(f"\n  Batch {batch_num}/{total_batches}: {len(memories)} memories")

    dataset_names = []
    t0 = time.time()

    for i, m in enumerate(memories):
        ds = f"alx_t2_{batch_num}_{i}"
        dataset_names.append(ds)
        await cognee.add(m["content"], dataset_name=ds)

    t_add = time.time() - t0
    print(f"  add() completed in {t_add:.1f}s ({len(memories)} datasets)")

    print(f"  Running cognify (entity extraction + graph)...")
    _prepare_cognee_ingest()  # Clear stale Kuzu locks
    t0 = time.time()
    await cognee.cognify(dataset_names)
    t_cognify = time.time() - t0
    print(f"  cognify() completed in {t_cognify:.1f}s")

    return {"batch": batch_num, "memories": len(memories), "add_time": t_add, "cognify_time": t_cognify}


async def main_async(args):
    """Main async entry point."""
    import cognee

    # Apply monkey-patch AFTER cognee is imported but BEFORE cognify
    print("Patching Cognee for qwen3 compatibility...")
    patch_cognee_edge_model()

    init_cognee()

    memories = get_memories(memory_type=args.type, limit=args.limit)
    print(f"\nTotal memories to ingest: {len(memories)}")

    if args.dry_run:
        print("DRY RUN — would ingest these memories:")
        for mt in set(m["memory_type"] for m in memories):
            count = sum(1 for m in memories if m["memory_type"] == mt)
            print(f"  {mt}: {count}")
        return

    # Process in batches
    batch_size = args.batch_size
    batches = [memories[i:i + batch_size] for i in range(0, len(memories), batch_size)]
    total_batches = len(batches)
    print(f"Processing {total_batches} batches of ~{batch_size} memories each")

    results = []
    overall_start = time.time()

    for i, batch in enumerate(batches, 1):
        try:
            result = await ingest_batch(batch, i, total_batches)
            results.append(result)
        except Exception as e:
            print(f"  ERROR in batch {i}: {e}")
            results.append({"batch": i, "error": str(e)})

    overall_time = time.time() - overall_start

    print(f"\n{'='*60}")
    print(f"COMPLETE: {len(memories)} memories ingested in {overall_time:.0f}s ({overall_time/60:.1f} min)")
    print(f"Batches: {len(results)} ({sum(1 for r in results if 'error' not in r)} succeeded)")

    # Verify
    print("\nVerifying knowledge graph...")
    try:
        from cognee.api.v1.search import search as cognee_search
        from cognee.modules.search.types import SearchType
        test_result = await cognee_search(SearchType.CHUNKS, "Chirp rule engine", None)
        print(f"  Search test: {len(test_result)} results for 'Chirp rule engine'")
    except Exception as e:
        print(f"  Search test failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Batch ingest Tier 1 → Cognee Tier 2")
    parser.add_argument("--batch-size", type=int, default=50, help="Memories per batch (default: 50)")
    parser.add_argument("--type", type=str, default=None, help="Filter by memory_type")
    parser.add_argument("--limit", type=int, default=None, help="Max memories to process")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be ingested")
    args = parser.parse_args()

    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
