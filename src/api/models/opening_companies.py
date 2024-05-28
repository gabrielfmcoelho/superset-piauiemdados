from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

from database.connector import Connector


months = {
    "jan": 1,
    "fev": 2,
    "mar": 3,
    "abr": 4,
    "mai": 5,
    "jun": 6,
    "jul": 7,
    "ago": 8,
    "set": 9,
    "out": 10,
    "nov": 11,
    "dez": 12
}

db_connector = Connector.get_instance()
db_base = db_connector.get_base()


class OpeningCompany(db_base):
    __tablename__ = "opening_companies"

    id = Column(Integer, primary_key=True, index=True)
    hash_key = Column(String(255), unique=True, nullable=False, index=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    size = Column(String(255), nullable=False)
    nature_type_code = Column(String(255), nullable=False)
    nature_type_descr = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    is_branch = Column(Boolean, nullable=False)
    amount = Column(Integer, nullable=False)

    def __init__(self, hash_key, year, month, size, nature_type_code, nature_type_descr, city, is_branch, amount):
        self.hash_key = hash_key
        self.year = year
        self.month = months[month]
        self.size = size
        self.nature_type_code = nature_type_code
        self.nature_type_descr = nature_type_descr
        self.city = city
        self.is_branch = True if is_branch == "Sim" else False
        self.amount = amount

class OpeningCompanyActivities(db_base):
    __tablename__ = "opening_companies_activities"

    id = Column(Integer, primary_key=True, index=True)
    hash_key = Column(String(255), ForeignKey("opening_companies.hash_key"), nullable=False)
    cnae = Column(String(255), nullable=False)
    cnae_descr = Column(String(255), nullable=False)
    segment = Column(String(255), nullable=False)
    amount = Column(Integer, nullable=False)

    company = relationship("OpeningCompany", backref="activities")

    def __init__(self, hash_key, cnae, cnae_descr, segment, amount):
        self.hash_key = hash_key
        self.cnae = cnae
        self.cnae_descr = cnae_descr
        self.segment = segment
        self.amount = amount

class OpeningCompanyTimeSeries(db_base):
    __tablename__ = "opening_companies_time_series"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    serial_identifier = Column(String(255), nullable=False)
    nature_type_code = Column(String(255), nullable=False)
    nature_type_descr = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    register_hours_duration = Column(Float, nullable=False)

    def __init__(self, year, month, serial_identifier, nature_type_code, nature_type_descr, city, cp_name, cp_address, cp_total, register, hh, mm, ss, register_hours_duration, register_minutes_duration):
        self.year = year
        self.month = month
        self.serial_identifier = serial_identifier
        self.nature_type_code = nature_type_code
        self.nature_type_descr = nature_type_descr
        self.city = city
        self.register_hours_duration = register_hours_duration