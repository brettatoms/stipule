import ConfigParser
import os

import sqlalchemy as sa
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import config

uri = config.get('database_url')
engine = sa.create_engine(uri, echo=True)
Session = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

class Accession(Base):
    __tablename__ = 'accession'
    acc_num = Column(String, primary_key=True)
    genus = Column(String, index=True)
    name = Column(String)
    common_name = Column(String, index=True)

    range = Column(String)
    misc_notes = Column(String)
    recd_dt = Column(String)
    recd_amt = Column(String)
    recd_as = Column(String)
    recd_size = Column(String)
    recd_notes = Column(String)

    psource_current = Column(String, index=True)
    psource_acc_num = Column(String)
    psource_acc_dt = Column(String)
    psource_misc = Column(String)

    plants = relationship("Plant", backref="accession",
                          order_by="Plant.qualifier")


class Plant(Base):
    __tablename__ = 'plant'
    acc_num = Column(String, ForeignKey('accession.acc_num'), primary_key=True)
    qualifier = Column(String, primary_key=True)

    sex = Column(String)

    loc_name = Column(String, index=True)
    loc_code = Column(String, index=True)
    loc_change_type = Column(String)
    loc_date = Column(String)
    loc_nplants = Column(String)

    # TODO: need full condition instead of code, e.g. Alive instead of A
    condition = Column(String)
    checked_date = Column(String)
    checked_note = Column(String)
    checked_by = Column(String)

