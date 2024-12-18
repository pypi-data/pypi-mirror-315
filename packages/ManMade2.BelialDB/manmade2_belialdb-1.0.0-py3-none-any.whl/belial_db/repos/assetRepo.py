from sqlalchemy import Engine
from sqlalchemy.orm import Session

from belial_db.models import AssetModel


class AssetRepo:
    """
    Repository for managing assets in the database.
    """

    def __init__(self, engine: Engine):
        """
        Initializes the AssetRepo with a database engine.

        :param engine: SQLAlchemy Engine instance for database connection.
        """
        self._engine = engine

    def get_asset(self, id: int) -> AssetModel | None:
        """
        Retrieves an asset by its ID.

        :param id: The ID of the asset to retrieve.
        :return: The AssetModel instance if found, otherwise None.
        """
        with Session(self._engine) as session:
            return session.query(AssetModel).filter(AssetModel.Id == id).first()

    def create_asset(self, asset: AssetModel) -> AssetModel:
        """
        Creates a new asset in the database.

        :param asset: The AssetModel instance to create.
        :return: The created AssetModel instance.
        """
        with Session(self._engine) as session:
            session.add(asset)
            session.commit()
            return asset

    def update_asset(self, asset: AssetModel) -> AssetModel:
        """
        Updates an existing asset in the database.

        :param asset: The AssetModel instance to update.
        :return: The updated AssetModel instance.
        """
        with Session(self._engine) as session:
            session.merge(asset)
            session.commit()
            return asset

    def delete_asset(self, id: int) -> None:
        """
        Deletes an asset by its ID.

        :param id: The ID of the asset to delete.
        """
        with Session(self._engine) as session:
            asset = session.query(AssetModel).filter(AssetModel.Id == id).first()
            if asset:
                session.delete(asset)
                session.commit()
