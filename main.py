import os
from cloudlink import server

if __name__ == "__main__":
    # Render passes the port as an environment variable
    port = int(os.environ.get("PORT", 10000))
    
    print(f"Starting Cloudlink server on port {port}...")
    
    # Initialize the server on Render's specified port and host
    cl = server(port=port, host="0.0.0.0")

