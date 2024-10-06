# log2pg: Log Processing and API Project

This project processes log data, populates a PostgreSQL database, and provides an API endpoint for retrieving customer statistics.

## Prerequisites

- Docker
- Docker Compose
- Python 3.9+

## Configuration

The project uses a configuration file (`log2pg/config.py`) to manage various settings. You can modify this file to change database connection details, API settings, log processing parameters, and more.

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

3. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Install the project in editable mode:
   ```
   pip install -e .
   ```

6. Review and update the configuration in `log2pg/config.py` if necessary.

7. Generate the log file:
   ```
   python scripts/generator.py
   ```

8. Build and run the services:
   ```
   docker-compose up --build
   ```

The API will be available at `http://localhost:8000` (or the host and port specified in your configuration).

## Running Tests

To run the tests, make sure you're in the project root directory and your virtual environment is activated, then run:

```
pytest
```

## API Usage

To get statistics for a specific customer:

Note: that I use `from_date` and not `from`, I find this clarifies the meaning and avoids using a keyword

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