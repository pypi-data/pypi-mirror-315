from sqlalchemy import create_engine

from belial_db.models.relationships import Base


def create_connection(db_url: str, echo: bool = False):
    """
    Create a database connection and initialize the database schema.

    Args:
        db_url (str): The database URL to connect to.
        echo (bool): If True, the engine will log all statements. Default is False.

    Returns:
        Engine: A SQLAlchemy Engine instance connected to the specified database.
    """
    engine = create_engine(db_url, echo=echo)
    Base.metadata.create_all(engine)
    return engine
