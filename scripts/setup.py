#!/usr/bin/env python3
"""
Environment setup script for MLX Batch Generator MCP project.
This script sets up the development environment so that code editors 
and JupyterLab automatically detect the correct Python environment.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Main setup function"""
    print("🚀 Setting up MLX Batch Generator MCP development environment...")
    
    # Get project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("📦 Installing dependencies with uv...")
    result = subprocess.run([
        "uv", "sync", "--extra", "dev"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Failed to install dependencies: {result.stderr}")
        sys.exit(1)
    
    print("✅ Dependencies installed successfully!")
    
    # Register Jupyter kernel
    print("🔧 Registering Jupyter kernel...")
    result = subprocess.run([
        "uv", "run", "python", "-m", "ipykernel", "install", 
        "--user", "--name=mlx-batch-generator", "--display-name=MLX Batch Generator (uv)"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"⚠️  Warning: Failed to register Jupyter kernel: {result.stderr}")
    else:
        print("✅ Jupyter kernel registered successfully!")
    
    # Create .python-version file for editor detection
    python_version = sys.version.split()[0]
    with open(".python-version", "w") as f:
        f.write(python_version)
    print(f"✅ Created .python-version file: {python_version}")
    
    # Verify environment
    print("\n🔍 Environment verification:")
    print(f"Python executable: {sys.executable}")
    print(f"Project root: {project_root}")
    print(f"Virtual environment: {project_root / '.venv'}")
    
    # Check key packages
    try:
        import mlx
        print(f"✅ mlx available")
    except ImportError:
        print("❌ mlx not found")
    
    try:
        import mlx_lm
        print(f"✅ mlx-lm available")
    except ImportError:
        print("❌ mlx-lm not found")
    
    try:
        import mcp
        print(f"✅ mcp available")
    except ImportError:
        print("❌ mcp not found")
    
    try:
        import jupyterlab
        print("✅ JupyterLab available")
    except ImportError:
        print("❌ JupyterLab not found")
    
    print("\n🎉 Environment setup complete!")
    print("\n📝 Next steps:")
    print("1. Configure nbstripout: uv run nbstripout --install")
    print("2. Restart your code editor")
    print("3. Select the Python interpreter: .venv/bin/python")
    print("4. Run JupyterLab: uv run jupyter lab")
    print("5. Test MCP server: uv run python test_mcp_server.py")

if __name__ == "__main__":
    main()
