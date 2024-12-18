from typing import Any
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from .relationships import Base, MapAssetAssociation, MapAssetFileAssociation
from .asset import Asset
from .asset_file import AssetFile


class Map(Base):
    """Represents a map in the database.

    Attributes:
        Id (int): The primary key for the map.
        Name (str): The name of the map.
        Assets (list[AssetModel]): A list of assets associated with the map.
        AssetFiles (list[AssetFileModel]): A list of asset files associated with the map.
    """

    __tablename__ = "maps"

    Id = Column(Integer, primary_key=True, nullable=False)
    Name = Column(String, nullable=False)

    Assets: Mapped[list[Asset]] = relationship("Asset", secondary=MapAssetAssociation, back_populates="Maps")
    AssetFiles: Mapped[list[AssetFile]] = relationship(
        "AssetFile", secondary=MapAssetFileAssociation, back_populates="Maps"
    )

    def __eq__(self, other: Any):
        if not isinstance(other, Map):
            return NotImplemented
        return self.Id == other.Id

    def __hash__(self):
        return hash(self.Id)

    def __repr__(self):
        return f"<Map(Id={self.Id}, Name='{self.Name}')>"
