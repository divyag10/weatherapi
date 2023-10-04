from .db import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean, Integer, Float
from sqlalchemy.sql import func
# from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE


class ActivityData(Base):
	__tablename__ = 'activity_data'
	id = Column(Integer, primary_key=True, nullable=False)
	temperature = Column(Float, nullable=False)
	humidity = Column(Float, nullable=False)
	wind = Column(Float, nullable=False)
	recommendation = Column(String, nullable=False)
	weather = Column(String)
	humidity_val = Column(String)
	wind_val = Column(String)
