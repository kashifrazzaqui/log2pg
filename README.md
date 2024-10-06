# log2pg: Log Processing and API Project

This project processes log data, populates a PostgreSQL database, and provides an API endpoint for retrieving customer statistics.

## Prerequisites

- Docker
- Docker Compose
- Python 3.9+

## Setup and Running

1. Clone this repository:
   ```
   git clone kashifrazzaqui/log2pg
   cd log2pg
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install the project in editable mode:
   ```
   pip install -e .
   ```

5. Generate the log file:
   ```
   python scripts/generator.py
   ```

6. Build and run the services:
   ```
   docker-compose up --build
   ```

The API will be available at `http://localhost:8000`.

## Running Tests

To run the tests, make sure you're in the project root directory and your virtual environment is activated, then run:

```
pytest
```

## API Usage

To get statistics for a specific customer:

Note: that I use `from_date` and not `from`, I find this clarifies the meaning and avoid using a keyword

```
GET /customers/{customer_id}/stats?from_date=YYYY-MM-DD
```

Example:
```
http://localhost:8000/customers/cust_1/stats?from_date=2024-10-01
```

cURL Example:
```
curl "http://localhost:8000/customers/cust_1/stats?from_date=2024-09-01"
```

This will return daily statistics for the specified customer starting from the given date.

## Troubleshooting

If you encounter any issues, please ensure that:
- All required ports are available (8000 for the API, 5432 for PostgreSQL)
- You have the latest version of Docker and Docker Compose installed
- You have generated the `api_requests.log` file before running `docker-compose up`
- Your virtual environment is activated and all dependencies are installed
