# MLX MCP Server Persistence Layer

This folder contains the persistence implementations for the MLX MCP Server batch processing system.

## Current Structure

```
persistance/
├── docker-compose.yml          # Docker services for persistence
├── sqlite/
│   └── database.py            # Current SQLite implementation (working)
├── neo4j/
│   └── neo4j_database.py      # Neo4j implementation (stub)
└── README.md                  # This file
```

## Available Persistence Options

### 1. SQLite (Current - Working)
- **Location**: `sqlite/database.py`
- **Status**: ✅ **Fully implemented and working**
- **Use Case**: Current production implementation
- **Features**:
  - Batch result storage
  - Query by batch_id, model, or recent results
  - Lightweight, file-based storage

### 2. Neo4j (Future - Stub)
- **Location**: `neo4j/neo4j_database.py`
- **Status**: 🚧 **Stub implementation**
- **Use Case**: Graph-based storage for complex relationships
- **Features** (planned):
  - Batch → Result relationships
  - Model → Batch relationships
  - Complex query capabilities
  - Graph-based analytics

## Docker Services

### Running the Services
```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d neo4j
docker-compose up -d redis

# Stop services
docker-compose down
```

### Available Services
- **Neo4j**: `localhost:7474` (HTTP), `localhost:7687` (Bolt)
  - Username: `neo4j`
  - Password: `mlx_password`
- **Redis**: `localhost:6379`

## Usage

### Current (SQLite)
```python
from sqlite.database import get_batch_results, save_generation_result

# Save result
save_generation_result(model_name, prompt, response, ...)

# Query results
results = get_batch_results(batch_id)
```

### Future (Neo4j - When Implemented)
```python
from neo4j.neo4j_database import Neo4jDatabase

db = Neo4jDatabase()
db.connect()
db.save_batch_result(batch_id, model_name, processing_type, ...)
results = db.get_batch_results(batch_id)
```

## Next Steps

1. **Decide persistence schema** for specialized processing types (NER, semantic, etc.)
2. **Implement Neo4j integration** when graph relationships are needed
3. **Add migration utilities** to move from SQLite to Neo4j when required
