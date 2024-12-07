# EXIF Manager Pro

A professional EXIF metadata management and optimization tool for images, built with Python and Flask.

## Features

- User authentication system
- Project-based image organization
- EXIF metadata editing and management
- Batch processing capabilities
- Image preview and download
- Secure file handling

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Copy .env.example to .env and configure:
   ```bash
   cp .env.example .env
   ```
6. Initialize the database:
   ```bash
   python scripts/init_db.py
   ```
7. Run the development server:
   ```bash
   python run_dev.py
   ```

## Usage

1. Register a new account or use the test account:
   - Email: test@example.com
   - Password: password123
2. Create a new project
3. Upload images and manage their EXIF metadata
4. Export modified images individually or in batch

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.