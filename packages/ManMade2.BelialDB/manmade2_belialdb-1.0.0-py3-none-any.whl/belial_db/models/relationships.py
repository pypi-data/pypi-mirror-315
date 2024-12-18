"""
This module defines the relationships between different database models
using SQLAlchemy. It includes associations for maps, assets, and asset files.
"""

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base

Base = declarative_base()

MapAssetAssociation = Table(
    "map_asset_association",
    Base.metadata,
    Column("MapId", Integer, ForeignKey("maps.Id"), primary_key=True),
    Column("AssetId", Integer, ForeignKey("assets.Id"), primary_key=True),
    __doc__="Association table linking maps to assets.",
)

MapAssetFileAssociation = Table(
    "map_assetfile_association",
    Base.metadata,
    Column("MapId", Integer, ForeignKey("maps.Id"), primary_key=True),
    Column("AssetFileId", Integer, ForeignKey("asset_files.Id"), primary_key=True),
    __doc__="Association table linking maps to asset files.",
)
