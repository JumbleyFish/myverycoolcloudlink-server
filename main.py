import os
from cloudlink import CloudLink

if __name__ == "__main__":
    # Render and Hugging Face pass the port as an environment variable
    port = int(os.environ.get("PORT", 3000))
    
    print(f"Starting Cloudlink server on port {port}...")
    
    # Initialize Cloudlink Server
    cl = CloudLink(debug=True)
    cl.server(host="0.0.0.0", port=port)
