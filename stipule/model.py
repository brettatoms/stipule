import sqlalchemy as sa
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

# TODO: use ConfigParser to read uri from stipule.config
uri = 'sqlite:///:memory:'
engine = sa.create_engine(uri, echo=True)

Base = declarative_base()

class Accession(Base):
    __tablename__ = 'accession'
    acc_num = Column(String, primary_key=True)
    genus = Column(String)
    name = Column(String)
    range = Column(String)
    common_name = Column(String)
    misc_notes = Column(String)
    recd_dt = Column(String)
    recd_dt = Column(String)
    recd_amt = Column(String)
    recd_as = Column(String)
    recd_size = Column(String)
    recd_notes = Column(String)

    psource_current = Column(String)
    psource_acc_num = Column(String)
    psource_acc_dt = Column(String)
    psource_misc = Column(String)

class Plant(Base):
    __tablename__ = 'plant'
    acc_num_qual = Column(String, primary_key=True)
    acc_num = Column(String)
