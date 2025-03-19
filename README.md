# FastAPI Order Management Microservice

This project converts a PHP-based monolithic Order Management API to a modern Python FastAPI microservice architecture with PostgreSQL database.

## Project Overview

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)
- Git

## Project Structure

```
shiplee_assignment/
├── main.py               # FastAPI application code
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── .env                  # Environment variables (not committed to version control)
└── README.md             # This file
```

## Setup & Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd shiplee_assignment
```

### 2. Create .env file

Create a `.env` file in the project root with the following content:

```
DATABASE_URL=postgresql://user:password@db:5432/orders_db
```

### 3. Build and run with Docker Compose

```bash
docker-compose up -d
```

This command will:
- Build the Docker image for the API
- Start the PostgreSQL database
- Connect the services together
- Make the API available on port 8000

### 4. Verify the installation

Open your browser and navigate to:
- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## API Endpoints

### Create Order

```
POST /orders/
```

Request body:
```json
{
  "customer_name": "John Doe",
  "product_name": "Smartphone",
  "price": 499.99
}
```

Response:
```json
{
  "status": "success",
  "order_id": 1
}
```

### Health Check

```
GET /health
```

Response:
```json
{
  "status": "healthy"
}
```

## Development

### Local Development (without Docker)

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload
```

### Running Tests

```bash
pytest
```

## Troubleshooting

### Permission Denied Error

If you encounter a "Permission denied" error when running Docker commands:

```bash
# Add your user to the docker group
sudo usermod -aG docker $USER

# Apply the changes (requires logging out and back in)
newgrp docker
```

### Database Connection Issues

If the service can't connect to the database:

1. Check if the PostgreSQL container is running:
```bash
docker-compose ps
```

2. Check the logs:
```bash
docker-compose logs db
docker-compose logs app
```

3. Verify the DATABASE_URL in the .env file matches the configuration in docker-compose.yml
