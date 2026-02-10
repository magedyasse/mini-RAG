from .minirag_base import SQLALchemy_Base
from sqlalchemy import Column, Integer, String, func, ForeignKey , String , DateTime
from sqlalchemy.dialects.postgresql import UUID , JSONB 
from sqlalchemy.orm import relationship
from sqlalchemy import Index
import uuid

class Asset(SQLALchemy_Base):
    
    __tablename__ = "assets"
    
    asset_id = Column(Integer, primary_key=True , autoincrement=True)
    asset_uuid = Column(UUID(as_uuid=True),default=uuid.uuid4, unique=True, nullable=False)
    
    asset_type = Column(String, nullable=False)
    asset_name = Column(String, nullable=False)
    
    asset_size = Column(Integer, nullable=True)  
    
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now() )
    updated_at = Column(DateTime(timezone=True), nullable=True,  onupdate=func.now() )
    
    asset_config = Column(JSONB, nullable=False)
    
    asset_project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    
    project  = relationship("Project", back_populates="assets")
    chunks = relationship("Chunk", back_populates="asset")
    
    __table_args__ = (
        
        Index('ix_asset_project_id', asset_project_id),
        Index('ix_asset_type', asset_type),
        
    )