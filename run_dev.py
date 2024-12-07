import os
from app import create_app
from flask import cli

# Désactiver le mode debug de Flask en production
cli.show_server_banner = lambda *args: None

def run_dev_server():
    app = create_app()
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run the development server
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
        use_reloader=True
    )

if __name__ == '__main__':
    run_dev_server()