import os
from cloudlink import CloudLink

if __name__ == "__main__":
    # Render passes the port as an environment variable
    port = int(os.environ.get("PORT", 10000))
    
    print(f"Starting Cloudlink server on port {port}...")
    
    # Initialize the correct capital CloudLink engine wrapper
    cl = CloudLink()
    
    # Start the server listening routine
    cl.server(host="0.0.0.0", port=port)
