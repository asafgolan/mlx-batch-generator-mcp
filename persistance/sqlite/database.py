#!/usr/bin/env python3
"""
Database module for MLX MCP Server
Handles SQLite database operations for storing generation results
"""

import sqlite3
import logging
from datetime import datetime
from typing import Optional
from pathlib import Path
import os

logger = logging.getLogger(__name__)

# Database configuration - use absolute path
SCRIPT_DIR = Path(__file__).parent.absolute()
DB_PATH = os.path.join(SCRIPT_DIR, "mlx_results.db")

def init_database():
    """Initialize SQLite database with results table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS generation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            model_name TEXT NOT NULL,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            max_tokens INTEGER,
            temperature REAL,
            prompt_index INTEGER,
            batch_id TEXT,
            is_batch BOOLEAN DEFAULT FALSE
        )
    """)
    
    conn.commit()
    conn.close()
    logger.info(f"Database initialized at {DB_PATH}")

def save_generation_result(model_name: str, prompt: str, response: str, 
                         max_tokens: int, temperature: float, 
                         prompt_index: Optional[int] = None, 
                         batch_id: Optional[str] = None, 
                         is_batch: bool = False):
    """Save a generation result to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO generation_results 
        (model_name, prompt, response, max_tokens, temperature, prompt_index, batch_id, is_batch)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (model_name, prompt, response, max_tokens, temperature, prompt_index, batch_id, is_batch))
    
    conn.commit()
    conn.close()
    logger.info(f"Generation result saved to database")

def get_batch_results(batch_id: str):
    """Get all results for a specific batch_id"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, timestamp, model_name, prompt, response, max_tokens, temperature, prompt_index, batch_id
        FROM generation_results 
        WHERE batch_id = ?
        ORDER BY prompt_index
    """, (batch_id,))
    
    results = cursor.fetchall()
    conn.close()
    
    return [{
        "id": row[0],
        "timestamp": row[1],
        "model_name": row[2],
        "prompt": row[3],
        "response": row[4],
        "max_tokens": row[5],
        "temperature": row[6],
        "prompt_index": row[7],
        "batch_id": row[8]
    } for row in results]

def get_recent_results(limit: int = 10):
    """Get recent generation results"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, timestamp, model_name, prompt, response, max_tokens, temperature, prompt_index, batch_id
        FROM generation_results 
        ORDER BY timestamp DESC 
        LIMIT ?
    """, (limit,))
    
    results = cursor.fetchall()
    conn.close()
    
    return [{
        "id": row[0],
        "timestamp": row[1],
        "model_name": row[2],
        "prompt": row[3],
        "response": row[4],
        "max_tokens": row[5],
        "temperature": row[6],
        "prompt_index": row[7],
        "batch_id": row[8]
    } for row in results]

def get_results_by_model(model_name: str, limit: int = 10):
    """Get recent results for a specific model"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, timestamp, model_name, prompt, response, max_tokens, temperature, prompt_index, batch_id
        FROM generation_results 
        WHERE model_name = ?
        ORDER BY timestamp DESC 
        LIMIT ?
    """, (model_name, limit))
    
    results = cursor.fetchall()
    conn.close()
    
    return [{
        "id": row[0],
        "timestamp": row[1],
        "model_name": row[2],
        "prompt": row[3],
        "response": row[4],
        "max_tokens": row[5],
        "temperature": row[6],
        "prompt_index": row[7],
        "batch_id": row[8]
    } for row in results]
