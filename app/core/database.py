from sqlmodel import SQLModel, create_engine, Session

# Configuration for SQLite database file
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False is needed for SQLite when using worker threads
# because the connection is created in one thread but used in another.
connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    """
    Creates the database file and all tables defined in SQLModel models.
    Should be called on application startup.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Dependency generator that yields a database session.
    Used by FastAPI endpoints to interact with the DB.
    """
    with Session(engine) as session:
        yield session