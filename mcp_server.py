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
from database import init_database, save_generation_result, get_batch_results, get_recent_results, get_results_by_model

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP app
app = FastMCP("mlx-batch-generator")

# No model cache - load fresh each time like demo notebook

def _format_prompts_by_type(prompts: List[str], prompt_type: str, max_tokens: int) -> List[str]:
    """
    Format prompts based on the specified prompt type.
    
    Args:
        prompts: List of base prompts
        prompt_type: Type of formatting to apply (currently only "raw" supported)
        max_tokens: Token limit (unused in raw mode)
    
    Returns:
        List of formatted prompts
    """
    # For now, only raw passthrough is supported
    return prompts

@app.tool()
def batch_generate_text(
    prompts: List[str],
    model_name: str = "microsoft/Phi-3-mini-4k-instruct",
    max_tokens: int = 300,
    temperature: float = 0.7,
    verbose: bool = False,
    format_prompts: bool = True,
    prompt_type: str = "raw"
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
        prompt_type: Type of prompt formatting to apply (currently only "raw" supported)
    
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
        
        # Apply prompt type formatting
        formatted_prompts = _format_prompts_by_type(prompts, prompt_type, max_tokens)
        
        # Generate responses
        responses = batch_generate(
            model,
            tokenizer,
            prompts=formatted_prompts,
            max_tokens=max_tokens,
            verbose=verbose,
            temp=temperature,
            format_prompts=format_prompts
        )
        
        # Generate batch ID for this batch
        batch_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Save all results to database (no results in response)
        for i, (prompt, response) in enumerate(zip(prompts, responses)):
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
        
        # Return only batch_id and status for modular processing
        return json.dumps({
            "status": "success",
            "model": model_name,
            "total_prompts": len(prompts),
            "batch_id": batch_id,
            "message": "Batch processing completed. Use read_batch_results to retrieve results."
        }, indent=2)
        
    except Exception as e:
        logger.error(f"Error in batch_generate_text: {e}")
        return json.dumps({
            "status": "error",
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

@app.tool()
def read_batch_results(
    batch_id: str = None,
    model_name: str = None,
    limit: int = 10
) -> str:
    """
    Read batch generation results from SQLite database.
    
    Args:
        batch_id: Specific batch ID to fetch results for
        model_name: Filter results by model name
        limit: Maximum number of results to return (default: 10)
    
    Returns:
        JSON string containing the query results
    """
    try:
        if batch_id:
            # Get results for specific batch
            results = get_batch_results(batch_id)
            return json.dumps({
                "status": "success",
                "query_type": "batch_results",
                "batch_id": batch_id,
                "total_results": len(results),
                "results": results
            }, indent=2)
        
        elif model_name:
            # Get results for specific model
            results = get_results_by_model(model_name, limit)
            return json.dumps({
                "status": "success",
                "query_type": "model_results",
                "model_name": model_name,
                "limit": limit,
                "total_results": len(results),
                "results": results
            }, indent=2)
        
        else:
            # Get recent results
            results = get_recent_results(limit)
            return json.dumps({
                "status": "success",
                "query_type": "recent_results",
                "limit": limit,
                "total_results": len(results),
                "results": results
            }, indent=2)
    
    except Exception as e:
        logger.error(f"Error in read_batch_results: {e}")
        return json.dumps({
            "status": "error",
            "error": str(e)
        }, indent=2)

if __name__ == "__main__":
    logger.info("Starting MLX MCP Server with FastMCP...")
    # Initialize database
    init_database()
    app.run()
