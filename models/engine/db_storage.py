#!/usr/bin/python3
"""This module defines the DBStorage class for database interaction"""
from os import getenv
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

logging.basicConfig(level=logging.DEBUG)

class DBStorage:
    """DBStorage class for database interaction"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage instance"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)
        
        print("db url: {}".format(self.__engine))

    def all(self, cls=None):
        """Query objects from the database"""
        obj_dict = {}
        if cls is None:
            cls_list = [User, State, City, Amenity, Place, Review]
        else:
            cls_list = [cls]
        for cl in cls_list:
            objs = self.__session.query(cl).all()
            for obj in objs:
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add an object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        logging.dubug("Saving data to db: %s", self)
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create a new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = session(session_factory)
    def do_all(self, args):
        from models import classes
        from models import storage
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in classes:
                print("** class doesn't exist **")
                return
            obj_dict = storage.all(classes[args])
            for k, v in obj_dict.items():
                print_list.append(str(v))
        else:
            obj_dict = storage.all()
            for k, v in obj_dict.items():
                print_list.append(str(v))

        print(print_list)
    

    def new(self, obj):
        self.__session.add(obj)
        print("calling new function.... ")
        logging.debug("Data being saved: %s", obj)

    def save(self):
        print("saving from db side... ")
        self.__session.commit()


    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = Session()
