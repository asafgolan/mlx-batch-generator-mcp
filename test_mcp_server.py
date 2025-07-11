#!/usr/bin/env python3
"""
Test the new FastMCP-based MLX server implementation
"""

import asyncio
import json
import subprocess
import sys

async def test_fastmcp_mlx_server():
    """Test the FastMCP MLX server"""
    print("🚀 Testing MLX MCP Server")
    print("=" * 50)
    
    # Start MLX MCP server
    cmd = [sys.executable, "mcp_server.py"]
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0
    )
    
    try:
        await asyncio.sleep(2)  # Give server time to start
        
        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        }
        
        print("📤 Sending initialize request...")
        request_json = json.dumps(init_request) + "\n"
        process.stdin.write(request_json)
        process.stdin.flush()
        
        # Read response
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            if "error" in response:
                print(f"❌ Initialize error: {response['error']}")
                return False
            else:
                print(f"✅ Initialize success: {response['result']['serverInfo']['name']}")
        else:
            print("❌ No response to initialize")
            return False
        
        # Send initialized notification
        init_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        
        notification_json = json.dumps(init_notification) + "\n"
        process.stdin.write(notification_json)
        process.stdin.flush()
        
        # Test list tools
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        print("📤 Sending list tools request...")
        request_json = json.dumps(list_tools_request) + "\n"
        process.stdin.write(request_json)
        process.stdin.flush()
        
        # Read response
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            if "error" in response:
                print(f"❌ List tools error: {response['error']}")
                return False
            else:
                tools = response['result']['tools']
                print(f"✅ List tools success: Found {len(tools)} tools")
                for tool in tools:
                    print(f"  - {tool['name']}: {tool['description']}")
        else:
            print("❌ No response to list tools")
            return False
        
        # Test model info tool
        model_info_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "get_model_info",
                "arguments": {}
            }
        }
        
        print("📤 Sending model info request...")
        request_json = json.dumps(model_info_request) + "\n"
        process.stdin.write(request_json)
        process.stdin.flush()
        
        # Read response
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            if "error" in response:
                print(f"❌ Model info error: {response['error']}")
                return False
            else:
                result = response['result']
                if result.get('isError'):
                    print(f"❌ Model info returned error: {result['content'][0]['text']}")
                else:
                    print(f"✅ Model info success: {result['content'][0]['text'][:100]}...")
        else:
            print("❌ No response to model info")
            return False
        
        # Test single generation (with small token limit to speed up test)
        single_gen_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "single_generate_text",
                "arguments": {
                    "prompt": "Hello, my name is",
                    "max_tokens": 5,
                    "temperature": 0.7
                }
            }
        }
        
        print("📤 Sending single generation request...")
        request_json = json.dumps(single_gen_request) + "\n"
        process.stdin.write(request_json)
        process.stdin.flush()
        
        # Read response (this might take a while for model loading)
        print("⏳ Waiting for generation response (this may take time for model loading)...")
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            if "error" in response:
                print(f"❌ Single generation error: {response['error']}")
                return False
            else:
                result = response['result']
                if result.get('isError'):
                    print(f"❌ Single generation returned error: {result['content'][0]['text']}")
                else:
                    print(f"✅ Single generation success: {result['content'][0]['text'][:200]}...")
        else:
            print("❌ No response to single generation")
            return False
        
        # Test batch generation
        batch_gen_request = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "batch_generate_text",
                "arguments": {
                    "prompts": [
                        "Hello, my name is",
                        "The weather today is",
                        "I like to code in"
                    ],
                    "max_tokens": 5,
                    "temperature": 0.7,
                    "verbose": True
                }
            }
        }
        
        print("📤 Sending batch generation request...")
        request_json = json.dumps(batch_gen_request) + "\n"
        process.stdin.write(request_json)
        process.stdin.flush()
        
        # Read response (this might take a while for batch processing)
        print("⏳ Waiting for batch generation response (this may take time for batch processing)...")
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            if "error" in response:
                print(f"❌ Batch generation error: {response['error']}")
                return False
            else:
                result = response['result']
                if result.get('isError'):
                    print(f"❌ Batch generation returned error: {result['content'][0]['text']}")
                else:
                    print(f"✅ Batch generation success: {result['content'][0]['text'][:300]}...")
        else:
            print("❌ No response to batch generation")
            return False
        
        print("\n🎉 MLX MCP server works correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        return False
    finally:
        process.terminate()
        process.wait()
        print("🛑 MLX MCP server terminated")

if __name__ == "__main__":
    asyncio.run(test_fastmcp_mlx_server())
