clone repo

cd mlx_parallm

uv venv .venv

uv pip install -e .

source .venv/bin/activate && test_mcp_server.py

results will be stored on an sqlite db in mlx_results.db on the mcp root dir