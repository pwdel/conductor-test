ARG BASE_IMAGE=valencia-mcp-base:latest
FROM ${BASE_IMAGE}

WORKDIR /workspace

COPY pyproject.toml README.md ./
COPY src ./src
COPY docs ./docs

RUN uv pip install --python /opt/venv/bin/python -e .

EXPOSE 8005

CMD ["fastmcp", "run", "src/mcp_doc_server/server.py", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8005"]
