#!/usr/bin/python3
"""Defines the State class."""
import models
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.city import City
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """
    Represents a state for a MySQL database.
    Inherits from SQLAlchemy Base and links to the MySQL table states.
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City",  backref="state", cascade="delete")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """list of all related City objects."""
            city_list = []
            for c in list(models.storage.all(City).values()):
                if c.state_id == self.id:
                    city_list.append(c)
            return city_list