import csv
from datetime import datetime
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from .models import LogEntry, Base
from .config import DATE_FORMAT, BATCH_SIZE


def parse_log_line(line: str) -> dict:
    """
    Parse a single log line and return a dictionary of log entry data.

    Args:
        line (str): A single line from the log file.

    Returns:
        dict: A dictionary containing parsed log entry data with keys:
            - timestamp (datetime): The timestamp of the log entry.
            - customer_id (str): The ID of the customer.
            - request_path (str): The path of the request.
            - status_code (int): The HTTP status code of the response.
            - duration (float): The duration of the request in milliseconds.
    """
    parts = line.strip().split(" ")
    return {
        "timestamp": datetime.strptime(f"{parts[0]} {parts[1]}", DATE_FORMAT),
        "customer_id": parts[2],
        "request_path": parts[3],
        "status_code": int(parts[4]),
        "duration": float(parts[5]),
    }


def process_log_file(file_path: str) -> None:
    """
    Process the entire log file and insert entries into the database.

    This function reads the log file, parses each line, creates LogEntry objects,
    and inserts them into the database. It handles the database session and
    commits the changes in batches for better performance.

    Args:
        file_path (str): The path to the log file to be processed.

    Raises:
        Exception: If there's an error while processing the log file or inserting data into the database.
    """

    # Create database tables if they don't exist
    Base.metadata.create_all(bind=engine)

    with open(file_path, "r") as f:
        reader = csv.reader(f, delimiter=" ")
        db = SessionLocal()
        try:
            # Process log entries in batches for better performance
            batch = []
            for row in reader:
                log_entry = LogEntry(
                    timestamp=datetime.strptime(f"{row[0]} {row[1]}", DATE_FORMAT),
                    customer_id=row[2],
                    request_path=row[3],
                    status_code=int(row[4]),
                    duration=float(row[5]),
                )
                batch.append(log_entry)

                if len(batch) >= BATCH_SIZE:
                    db.add_all(batch)
                    db.commit()
                    batch = []

            # Add any remaining entries
            if batch:
                db.add_all(batch)
                db.commit()
        except Exception as e:
            print(f"Error processing log file: {e}")
            db.rollback()
        finally:
            db.close()


if __name__ == "__main__":
    # Process the log file when the script is run directly
    process_log_file("/app/data/api_requests.log")
