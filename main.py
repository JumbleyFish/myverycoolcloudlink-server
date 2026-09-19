import os
import asyncio
from cloudlink import server

# Setup an HTTP health check for cron-job.org manually alongside Cloudlink
async def cron_ping_middleware(ready_event):
    await ready_event.wait()
    print("Cloudlink background check running...")

if __name__ == "__main__":
    # Render passes the listening port via environment variables
    port = int(os.environ.get("PORT", 10000))
    
    print(f"Starting official Cloudlink v4 engine on port {port}...")
    
    # Initialize the server cleanly using the direct v4 library class structure
    cl_server = server(
        port=port, 
        host="0.0.0.0"
    )
