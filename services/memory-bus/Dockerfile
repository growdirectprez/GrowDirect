FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# growdirect-mcp is a local sibling package required by memory-bus
COPY growdirect-mcp/pyproject.toml /tmp/growdirect-mcp/pyproject.toml
COPY growdirect-mcp/growdirect_mcp/ /tmp/growdirect-mcp/growdirect_mcp/
RUN pip install --no-cache-dir /tmp/growdirect-mcp

COPY memory-bus/pyproject.toml .
COPY memory-bus/memory_bus/ memory_bus/

RUN pip install --no-cache-dir .

EXPOSE 8003

CMD ["python3", "-m", "memory_bus.server"]
