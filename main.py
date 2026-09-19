import os
import cloudlink

if __name__ == "__main__":
    # Render passes the port as an environment variable
    port = int(os.environ.get("PORT", 10000))
    
    print(f"Starting Cloudlink server on port {port}...")
    
    # Initialize the core cloudlink object framework
    cl = cloudlink.cloudlink()
    
    # Run the server using its built-in method
    cl.server(host="0.0.0.0", port=port)
