#!/usr/bin/env python3
"""
MLX MCP Server using FastMCP API - Robust Implementation
Provides batch and single text generation using MLX models
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from mcp.server import FastMCP
from utils import load, generate, batch_generate
from database import init_database, save_generation_result

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP app
app = FastMCP("mlx-batch-generator")

# No model cache - load fresh each time like demo notebook

@app.tool()
def batch_generate_text(
    prompts: List[str],
    model_name: str = "microsoft/Phi-3-mini-4k-instruct",
    max_tokens: int = 300,
    temperature: float = 0.7,
    verbose: bool = False,
    format_prompts: bool = True
) -> str:
    """
    Generate text from multiple prompts in parallel using MLX models.
    
    Args:
        prompts: List of prompts to generate from
        model_name: Model to use for generation
        max_tokens: Maximum tokens to generate
        temperature: Temperature for generation
        verbose: Enable verbose output
        format_prompts: Format prompts for chat models
    
    Returns:
        JSON string containing the batch generation results
    """
    try:
        # Load model fresh each time (like demo notebook)
        logger.info(f"Loading model: {model_name}")
        model, tokenizer = load(model_name)
        logger.info(f"Model loaded successfully: {model_name}")
        
        # Debug: Log the max_tokens parameter
        logger.info(f"batch_generate_text called with max_tokens: {max_tokens}")
        
        # Generate responses
        responses = batch_generate(
            model,
            tokenizer,
            prompts=prompts,
            max_tokens=max_tokens,
            verbose=verbose,
            temp=temperature,
            format_prompts=format_prompts
        )
        
        # Generate batch ID for this batch
        batch_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Format results and save to database
        results = []
        for i, (prompt, response) in enumerate(zip(prompts, responses)):
            # Save to database
            save_generation_result(
                model_name=model_name,
                prompt=prompt,
                response=response,
                max_tokens=max_tokens,
                temperature=temperature,
                prompt_index=i,
                batch_id=batch_id,
                is_batch=True
            )
            
            results.append({
                "prompt_index": i,
                "prompt": prompt,
                "response": response
            })
        
        return json.dumps({
            "model": model_name,
            "total_prompts": len(prompts),
            "batch_id": batch_id,
            "results": results
        }, indent=2)
        
    except Exception as e:
        logger.error(f"Error in batch_generate_text: {e}")
        return json.dumps({
            "error": str(e),
            "model": model_name,
            "total_prompts": len(prompts)
        }, indent=2)

@app.tool()
def get_model_info() -> str:
    """
    Get information about the currently loaded model.
    
    Returns:
        JSON string containing model information
    """
    try:
        if model_cache["current_model_name"] is None:
            return json.dumps({
                "status": "no_model_loaded",
                "message": "No model is currently loaded"
            }, indent=2)
        
        return json.dumps({
            "status": "model_loaded",
            "model_name": model_cache["current_model_name"],
            "model_loaded": model_cache["model"] is not None,
            "tokenizer_loaded": model_cache["tokenizer"] is not None
        }, indent=2)
        
    except Exception as e:
        logger.error(f"Error in get_model_info: {e}")
        return json.dumps({
            "error": str(e),
            "status": "error"
        }, indent=2)

if __name__ == "__main__":
    logger.info("Starting MLX MCP Server with FastMCP...")
    # Initialize database
    init_database()
    app.run()
