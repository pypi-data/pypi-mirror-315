from typing import Any
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from .relationships import Base, MapAssetAssociation
from .vector3_type import Vector3Type
from .vector4_type import Vector4Type


class Asset(Base):
    """Represents an asset in the game.

    Attributes:
        Id (int): The primary key for the asset.
        AssetFileId (int): The ID of the associated asset file.
        Path (str): The file path of the asset.
        Type (str): The type of the asset (e.g., model, texture).
        ScaleFactor (float): The scale factor for the asset.
        Position (Vector3Type): The 3D position of the asset in the game world.
        Rotation (Vector4Type): The rotation of the asset represented as a quaternion.
        MapId (int): The ID of the map where the asset is located.
        Map (MapModel): The map model associated with this asset.
    """

    __tablename__ = "assets"

    Id = Column(Integer, primary_key=True)
    AssetFileId = Column(Integer, nullable=False)
    Path = Column(String, nullable=False)
    Type = Column(String, nullable=False)
    ScaleFactor = Column(Float(), nullable=False)
    Position = Column(Vector3Type, nullable=False)
    Rotation = Column(Vector4Type, nullable=False)

    Maps = relationship("Map", secondary=MapAssetAssociation, back_populates="Assets")

    def __eq__(self, other: Any):
        if not isinstance(other, Asset):
            return NotImplemented
        return self.Id == other.Id

    def __hash__(self):
        return hash(self.Id)

    def __repr__(self):
        return (
            f"<Asset(Id={self.Id}, Path='{self.Path}', Type='{self.Type}', ScaleFactor={self.ScaleFactor})>"
        )
