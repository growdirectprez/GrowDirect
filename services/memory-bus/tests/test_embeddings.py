# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
from unittest.mock import patch, MagicMock
from memory_bus.embeddings import get_embedding
from memory_bus.config import Config


class TestGetEmbedding:
    def test_returns_list_of_floats_on_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "embedding": [0.1] * 1024
        }
        with patch("memory_bus.embeddings.httpx.post", return_value=mock_response):
            config = Config()
            result = get_embedding("test text", config)
            assert result is not None
            assert len(result) == 1024
            assert all(isinstance(v, float) for v in result)

    def test_returns_none_on_connection_error(self):
        with patch("memory_bus.embeddings.httpx.post", side_effect=Exception("connection refused")):
            config = Config()
            result = get_embedding("test text", config)
            assert result is None

    def test_truncates_long_text(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"embedding": [0.1] * 1024}
        with patch("memory_bus.embeddings.httpx.post", return_value=mock_response) as mock_post:
            config = Config()
            long_text = "x" * 10000
            get_embedding(long_text, config)
            call_args = mock_post.call_args
            sent_text = call_args[1]["json"]["input"]
            assert len(sent_text) <= config.max_text_length

    def test_truncates_to_1024_dimensions(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "embedding": [0.1] * 4096  # native dimension
        }
        with patch("memory_bus.embeddings.httpx.post", return_value=mock_response):
            config = Config()
            result = get_embedding("test text", config)
            assert len(result) == 1024
