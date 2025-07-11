#!/usr/bin/env python3
"""
MLX MCP Server using FastMCP API - Robust Implementation
Provides batch and single text generation using MLX models
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from mcp.server import FastMCP
from utils import load, generate, batch_generate

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP app
app = FastMCP("mlx-batch-generator")

# Global model cache
model_cache = {
    "model": None,
    "tokenizer": None,
    "current_model_name": None
}

def load_model_if_needed(model_name: str):
    """Load model if not already loaded or if different model requested"""
    if model_cache["model"] is None or model_cache["current_model_name"] != model_name:
        logger.info(f"Loading model: {model_name}")
        try:
            model_cache["model"], model_cache["tokenizer"] = load(model_name)
            model_cache["current_model_name"] = model_name
            logger.info(f"Model loaded successfully: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            raise

@app.tool()
def batch_generate_text(
    prompts: List[str],
    model_name: str = "microsoft/Phi-3-mini-4k-instruct",
    max_tokens: int = 100,
    temperature: float = 0.7,
    verbose: bool = False,
    format_prompts: bool = False
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
        # Load model if needed
        load_model_if_needed(model_name)
        
        # Generate responses
        responses = batch_generate(
            model_cache["model"],
            model_cache["tokenizer"],
            prompts=prompts,
            max_tokens=max_tokens,
            verbose=verbose,
            temp=temperature,
            format_prompts=format_prompts
        )
        
        # Format results
        results = []
        for i, (prompt, response) in enumerate(zip(prompts, responses)):
            results.append({
                "prompt_index": i,
                "prompt": prompt,
                "response": response
            })
        
        return json.dumps({
            "model": model_name,
            "total_prompts": len(prompts),
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
def single_generate_text(
    prompt: str,
    model_name: str = "microsoft/Phi-3-mini-4k-instruct",
    max_tokens: int = 100,
    temperature: float = 0.7,
    verbose: bool = False
) -> str:
    """
    Generate text from a single prompt using MLX models.
    
    Args:
        prompt: Prompt to generate from
        model_name: Model to use for generation
        max_tokens: Maximum tokens to generate
        temperature: Temperature for generation
        verbose: Enable verbose output
    
    Returns:
        JSON string containing the generation result
    """
    try:
        # Load model if needed
        load_model_if_needed(model_name)
        
        # Generate response
        response = generate(
            model_cache["model"],
            model_cache["tokenizer"],
            prompt=prompt,
            max_tokens=max_tokens,
            verbose=verbose,
            temp=temperature
        )
        
        return json.dumps({
            "model": model_name,
            "prompt": prompt,
            "response": response
        }, indent=2)
        
    except Exception as e:
        logger.error(f"Error in single_generate_text: {e}")
        return json.dumps({
            "error": str(e),
            "model": model_name,
            "prompt": prompt
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
    app.run()
