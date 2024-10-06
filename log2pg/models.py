from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class LogEntry(Base):
    """
    Represents a single log entry in the database.

    This model corresponds to the 'log_entries' table and stores information
    about individual API requests, including timestamp, customer ID, request details,
    and performance metrics.
    """
    __tablename__ = "log_entries"

    # Table columns
    id: Mapped[int] = mapped_column(primary_key=True, 
                                    doc="Unique identifier for each log entry")
    timestamp: Mapped[datetime] = mapped_column(index=True, 
                                                doc="Timestamp of when the request was made")
    customer_id: Mapped[str] = mapped_column(index=True, 
                                             doc="Identifier for the customer who made the request")
    request_path: Mapped[str] = mapped_column(
        doc="The path of the API request (e.g., '/api/v1/users')")
    status_code: Mapped[int] = mapped_column(
        doc="HTTP status code of the response")
    duration: Mapped[float] = mapped_column(
        doc="Duration of the request in milliseconds")

    def __repr__(self) -> str:
        """
        Provide a string representation of the LogEntry instance.

        Returns:
            str: A string representation of the LogEntry.
        """
        return (f"<LogEntry(id={self.id}, timestamp={self.timestamp}, "
                f"customer_id='{self.customer_id}', request_path='{self.request_path}', "
                f"status_code={self.status_code}, duration={self.duration})>")