# Media Vault Application

A web application for managing and browsing media collections (anime, movies, series) with filtering and search capabilities.

## Prerequisites

- Ubuntu 20.04/22.04 LTS
- Docker and Docker Compose
- Git (optional, if cloning the repository)

## Setup Instructions

1. **Clone the repository (if not already done):**
   ```bash
   git clone <repository-url>
   cd media-vault
   ```

2. **Make the setup script executable and run it:**
   ```bash
   chmod +x setup_ubuntu.sh
   ./setup_ubuntu.sh
   ```
   
   This script will:
   - Install Docker and Docker Compose if not already installed
   - Set up proper permissions
   - Build and start the application containers

3. **Access the application:**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:5000

## Project Structure

```
.
├── backend/           # Backend Flask application
│   ├── app.py         # Main application file
│   └── Dockerfile     # Backend Docker configuration
├── db/                # Database files
│   └── data.sql       # Database schema and initial data
├── frontend/          # Frontend files
│   ├── static/        # Static assets (CSS, JS, images)
│   └── templates/     # HTML templates
├── docker-compose.yml  # Docker Compose configuration
└── setup_ubuntu.sh    # Ubuntu setup script
```

## Managing the Application

- **Start the application:**
  ```bash
  docker-compose up -d
  ```

- **Stop the application:**
  ```bash
  docker-compose down
  ```

- **View logs:**
  ```bash
  docker-compose logs -f
  ```

- **Rebuild the application (after code changes):**
  ```bash
  docker-compose up -d --build
  ```

## Troubleshooting

- If you encounter permission issues, try running:
  ```bash
  sudo chown -R $USER:$USER .
  ```

- If the database doesn't initialize properly, try:
  ```bash
  docker-compose down -v
  docker-compose up -d --build
  ```

## License

This project is licensed under the MIT License.
