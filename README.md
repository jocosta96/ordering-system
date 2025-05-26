# ordering-system
A fast food self-service system designed for Software Architecture Postgraduate coursework.

## System Architecture
[View the system architecture diagram on Miro](https://miro.com/app/board/uXjVIDKgo30=/?share_link_id=192061516718)

## Features
- Customer self-service ordering
- Product and ingredient management
- Order processing and tracking
- Modular, layered architecture (Domain, Adapter, Application)
- RESTful API endpoints

## Technologies Used
- Python 3.10+
- FastAPI
- SQLAlchemy
- Alembic (for migrations)
- Docker (for containerization)

## Project Structure
```
app/
  main.py            # Application entrypoint
  adapter/           # Inbound/Outbound adapters (REST, repositories)
  domain/            # Domain entities, use cases, value objects
alembic/             # Database migrations
requirements.txt     # Python dependencies
Dockerfile           # Containerization
compose.yaml         # Docker Compose setup
```

## Setup & Installation
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd ordering-system
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure the .env like this sample:
   
    POSTGRES_USER=""
    POSTGRES_PASSWORD=""
    POSTGRES_DB=""
    PGADMIN_MAIL=""
    PGADMIN_PW=""
    POSTGRES_HOST='postgres'
    HOST='localhost'
    DRIVER_NAME = 'postgresql'

3. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```
4. ** with Docker:
   ```bash
   docker compose up --build
   ```

## Usage
- Access the API at `http://localhost:8000` (or the port specified in your config).
- Use tools like Postman or curl to interact with the endpoints
 - Using Swagger is highly encouraged.
 check at `http://127.0.0.1:8080/redoc` or `http://127.0.0.1:8080/docs`

## Running Tests
```bash
pytest
```

## Contributing
This project has educational purposes, which means that PR's will be done only by the project members

## License
This project is licensed under the MIT License.
