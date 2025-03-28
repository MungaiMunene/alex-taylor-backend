from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Use the PORT environment variable for dynamic port (on Render or similar platforms)
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if no port is provided (local)
    
    # Run the app with the specified host and port
    app.run(host='0.0.0.0', port=port, debug=True)