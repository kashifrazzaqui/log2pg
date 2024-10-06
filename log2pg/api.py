from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from .database import get_db
from .models import LogEntry
from datetime import datetime

app = FastAPI()

def get_stats_from_db(db: Session, customer_id: str, from_date: datetime):
    """
    Retrieve aggregated statistics from the database for a specific customer and date range.

    Args:
        db (Session): The database session.
        customer_id (str): The ID of the customer to retrieve stats for.
        from_date (datetime): The start date for the statistics.

    Returns:
        SQLAlchemy Result: An object containing aggregated statistics including total requests,
        successful requests, failed requests, average latency, median latency, and 99th percentile latency.
    """
    # Aggregate log data for a specific customer since a given date
    return db.query(
        func.count(LogEntry.id).label("total_requests"),
        func.sum(case((LogEntry.status_code < 400, 1), else_=0)).label("successful_requests"),
        func.sum(case((LogEntry.status_code >= 400, 1), else_=0)).label("failed_requests"),
        func.avg(LogEntry.duration).label("avg_latency"),
        func.percentile_cont(0.5).within_group(LogEntry.duration.desc()).label("median_latency"),
        func.percentile_cont(0.99).within_group(LogEntry.duration.desc()).label("p99_latency")
    ).filter(
        LogEntry.customer_id == customer_id,
        LogEntry.timestamp >= from_date
    ).first()

@app.get("/customers/{customer_id}/stats")
def get_customer_stats(customer_id: str, from_date: str, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve customer statistics.

    Args:
        customer_id (str): The ID of the customer to retrieve stats for.
        from_date (str): The start date for the statistics in YYYY-MM-DD format.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing the following statistics:
            - total_requests: Total number of requests.
            - successful_requests: Number of successful requests (status code < 400).
            - failed_requests: Number of failed requests (status code >= 400).
            - uptime: Percentage of successful requests.
            - avg_latency: Average latency in milliseconds.
            - median_latency: Median latency in milliseconds.
            - p99_latency: 99th percentile latency in milliseconds.

    Raises:
        HTTPException: 400 error if the date format is invalid.
        HTTPException: 404 error if no data is found for the given customer and date range.
    """
    try:
        # Convert string date to datetime object
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    stats = get_stats_from_db(db, customer_id, from_date)

    if not stats or not stats.total_requests:
        raise HTTPException(status_code=404, detail="No data found for the given customer and date range")

    # Calculate uptime percentage
    uptime = (stats.successful_requests / stats.total_requests) * 100 if stats.total_requests > 0 else 0

    # Format and return the statistics
    return {
        "total_requests": stats.total_requests,
        "successful_requests": stats.successful_requests,
        "failed_requests": stats.failed_requests,
        "uptime": f"{uptime:.2f}%",
        "avg_latency": f"{stats.avg_latency:.2f}ms" if stats.avg_latency else None,
        "median_latency": f"{stats.median_latency:.2f}ms" if stats.median_latency else None,
        "p99_latency": f"{stats.p99_latency:.2f}ms" if stats.p99_latency else None
    }