from sqlalchemy import Engine
from sqlalchemy.orm import Session

from belial_db.models import AssetFileModel


class AssetFileRepo:
    """
    Repository for managing asset files in the database.
    """

    def __init__(self, engine: Engine):
        """
        Initializes the AssetFileRepo with a database engine.

        :param engine: SQLAlchemy Engine instance for database connection.
        """
        self._engine = engine

    def create_asset_file(self, asset_file: AssetFileModel) -> AssetFileModel:
        """
        Creates a new asset file in the database.

        :param asset_file: The AssetFileModel instance to create.
        :return: The created AssetFileModel instance.
        """
        with Session(self._engine) as session:
            session.add(asset_file)
            session.commit()
            return asset_file

    def update_asset_file(self, asset_file: AssetFileModel) -> AssetFileModel:
        """
        Updates an existing asset file in the database.

        :param asset_file: The AssetFileModel instance to update.
        :return: The updated AssetFileModel instance.
        """
        with Session(self._engine) as session:
            session.merge(asset_file)
            session.commit()
            return asset_file

    def delete_asset_file(self, id: int) -> None:
        """
        Deletes an asset file by its ID.

        :param id: The ID of the asset file to delete.
        """
        with Session(self._engine) as session:
            asset_file = session.query(AssetFileModel).filter(AssetFileModel.Id == id).first()
            if asset_file:
                session.delete(asset_file)
                session.commit()
