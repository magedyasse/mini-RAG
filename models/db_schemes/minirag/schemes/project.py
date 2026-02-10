from .minirag_base import SQLALchemy_Base
from sqlalchemy import Column, Integer, func, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid


class Project(SQLALchemy_Base):
    
    __tablename__ = "projects"
    
    project_id = Column(Integer, primary_key=True , autoincrement=True)
    project_uuid = Column(UUID(as_uuid=True),default=uuid.uuid4, unique=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now() )
    updated_at = Column(DateTime(timezone=True), nullable=True,  onupdate=func.now() )
    
    chunks  = relationship("Chunk", back_populates="project")
    assets = relationship("Asset", back_populates="project")

    
    
    
    
    