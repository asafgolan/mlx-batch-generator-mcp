# MLX Parallel Generation MCP Server Setup

This MCP server provides batch text generation capabilities using MLX models for VS Code extensions like Cline or Continue.

## Prerequisites

- Python 3.8+
- MLX framework installed
- VS Code with Cline or Continue extension

## Installation

1. **Install MCP dependencies**:
   ```bash
   pip install mcp pydantic
   ```

2. **Ensure MLX is installed**:
   ```bash
   pip install mlx mlx-lm
   ```

## Configuration

### For Cline Extension

Add this to your Cline settings (`~/.continue/config.json` or similar):

```json
{
  "mcpServers": {
    "mlx-batch-generator": {
      "command": "python",
      "args": ["/Users/asafgolan/Jarvis/mlx_parallm/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/Users/asafgolan/Jarvis/mlx_parallm"
      }
    }
  }
}
```

### For Continue Extension

Add this to your Continue config file:

```json
{
  "mcpServers": {
    "mlx-batch-generator": {
      "command": "python",
      "args": ["/Users/asafgolan/Jarvis/mlx_parallm/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/Users/asafgolan/Jarvis/mlx_parallm"
      }
    }
  }
}
```

## Usage

The MCP server provides two main tools:

### 1. `batch_generate`
Generate text from multiple prompts in parallel:

```json
{
  "tool": "batch_generate",
  "prompts": [
    "Write a short poem about AI",
    "Explain quantum computing",
    "Create a recipe for cookies"
  ],
  "model_name": "mlx-community/Meta-Llama-3-8B-Instruct-4bit",
  "max_tokens": 150,
  "temperature": 0.7
}
```

### 2. `single_generate`
Generate text from a single prompt:

```json
{
  "tool": "single_generate",
  "prompt": "Write a function to calculate fibonacci numbers",
  "model_name": "mlx-community/Meta-Llama-3-8B-Instruct-4bit",
  "max_tokens": 200,
  "temperature": 0.3
}
```

## Available Models

The server supports various MLX models:

- `mlx-community/Meta-Llama-3-8B-Instruct-4bit` (default)
- `meta-llama/Meta-Llama-3-8B-Instruct`
- `microsoft/Phi-3-mini-4k-instruct`
- `mlx-community/Phi-3-mini-4k-instruct-4bit`
- `google/gemma-1.1-2b-it`
- `mlx-community/gemma-1.1-2b-it-4bit`

## Parameters

- `prompts`: List of strings (for batch_generate)
- `prompt`: Single string (for single_generate)
- `model_name`: Model identifier (optional, defaults to Llama-3-8B-Instruct-4bit)
- `max_tokens`: Maximum tokens to generate (default: 100)
- `temperature`: Sampling temperature (default: 0.7)
- `verbose`: Enable verbose output (default: false)
- `format_prompts`: Format prompts for chat models (default: false)

## Testing

Test the server directly:

```bash
cd /Users/asafgolan/Jarvis/mlx_parallm
python mcp_server.py
```

The server will start and listen for MCP protocol messages via stdio.

## Troubleshooting

1. **Model loading issues**: Ensure you have sufficient memory and the model is available
2. **Path issues**: Update the absolute path in the config to match your installation
3. **Permission issues**: Ensure Python has access to the MLX models directory
4. **Extension not recognizing**: Restart VS Code after updating the configuration

## Performance Tips

- Use 4-bit quantized models for better performance
- Adjust `max_tokens` based on your needs
- Enable `verbose=true` for debugging
- Consider model warm-up time for first generation