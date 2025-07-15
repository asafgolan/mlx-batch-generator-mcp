#!/usr/bin/env python3
"""
Database module for MLX MCP Server
Handles SQLite database operations for storing generation results
"""

import sqlite3
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

# Database configuration
DB_PATH = "mlx_results.db"

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
    logger.info(f"Saved generation result to database (batch: {is_batch})")
