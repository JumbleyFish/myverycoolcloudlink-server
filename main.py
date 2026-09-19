import os
import cloudlink

if __name__ == "__main__":
    # Render passes the port as an environment variable
    port = int(os.environ.get("PORT", 3000))
    
    print(f"Starting Cloudlink server on port {port}...")
    
    # Initialize Cloudlink Server (v0.2 uses lowercase 'l')
    cl = cloudlink.cloudlink(debug=True)
    cl.server(host="0.0.0.0", port=port)

