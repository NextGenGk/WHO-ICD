# NAMASTE v2 UI

A FastAPI-based web interface for interacting with the WHO ICD (International Classification of Diseases) API.

## Features

- User-friendly web interface for ICD code lookup
- Support for various ICD API endpoints
- OAuth2 authentication with WHO ICD API
- Environment-based configuration
- Responsive design

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- WHO ICD API credentials (Client ID and Client Secret)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd NAMASTE-v2-UI
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your WHO ICD API credentials:
   ```
   WHO_CLIENT_ID=your_client_id
   WHO_CLIENT_SECRET=your_client_secret
   WHO_TOKEN_URL=token_url_from_who
   WHO_BASE_URL=base_api_url_from_who
   ```

## Usage

1. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

3. Use the web form to make API requests to the WHO ICD API.

## Project Structure

- `main.py` - Main FastAPI application and route handlers
- `templates/` - HTML templates
  - `form.html` - Main web interface
- `.env` - Environment variables (not version controlled)
- `requirements.txt` - Python dependencies

## API Endpoints

- `GET /` - Main page with the ICD API query form
- `POST /` - Handles form submission and makes requests to WHO ICD API

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| WHO_CLIENT_ID | WHO ICD API Client ID | Yes |
| WHO_CLIENT_SECRET | WHO ICD API Client Secret | Yes |
| WHO_TOKEN_URL | WHO OAuth2 Token URL | Yes |
| WHO_BASE_URL | WHO ICD API Base URL | Yes |

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
- [WHO ICD API](https://icd.who.int/icdapi) - The ICD API service
