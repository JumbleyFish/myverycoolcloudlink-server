import os
import asyncio
from cloudlink import server

if __name__ == "__main__":
    # Render automatically passes the web port via environment variables
    port = int(os.environ.get("PORT", 10000))
    
    print(f"Starting official Cloudlink v4 engine on port {port}...")
    
    # Step 1: Initialize the core server template framework with zero arguments
    cl_instance = server()
    
    # Step 2: Configure the target host and port definitions natively
    cl_instance.host = "0.0.0.0"
    cl_instance.port = port
    
    # Step 3: Run the internal server socket routine using asyncio loop rules
    asyncio.run(cl_instance.run())
