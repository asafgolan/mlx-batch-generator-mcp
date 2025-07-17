# MLX Batch Generator MCP Setup

## Prerequisites
- Python 3.11+
- uv (Python package manager)

## Bootstrap Guide

### 1. Clone Repository
```bash
clone repo
cd mlx-batch-generator-mcp
```

### 2. Run Setup Script
```bash
uv run python scripts/setup.py
```

### 3. Configure Jupyter (One-time setup)
```bash
uv run nbstripout --install
```

### 4. Start Development Environment
```bash
uv run jupyter lab
```

### 5. Test MCP Server
Run the `test_mcp_server.py` to test persistence in SQLite database `mlx_results.db` in the root directory:
```bash
uv run python test_mcp_server.py
```

This will verify the MCP server functionality and database persistence.

### 6. Test MCP Server with Inspector
```bash
# run mcp server with inspector (specify server command directly)
npx @modelcontextprotocol/inspector uv run mcp_server.py
```

This will:
- Start the MCP inspector at `http://localhost:6274`
- Connect your MLX batch server to the inspector
- Show available tools for batch text generation
- Display the authentication token for secure access

**Alternative if above doesn't work:**
```bash
# Run server separately, then connect inspector
uv run mcp_server.py &
npx @modelcontextprotocol/inspector
```

### 7. Connect to MCP Client (Claude/Cursor)
refer to [mcp_config_example.json](mcp_config_example.json) for configuration