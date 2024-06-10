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


class Opening(db_base):
    __tablename__ = "openings"
    id = Column(Integer, primary_key=True, index=True)
    hash_key = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    size = Column(String(255), nullable=False)
    nature_type_code = Column(String(255), nullable=False)
    nature_type_descr = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    is_branch = Column(Boolean, nullable=False)
    amount_x = Column(Integer, nullable=False)
    cnae = Column(String(255), nullable=False)
    cnae_descr = Column(String(255), nullable=False)
    segment = Column(String(255), nullable=False)
    amount_y = Column(Integer, nullable=False)

    def __init__(self, hash_key, year, month, size, nature_type_code, nature_type_descr, city, is_branch, amount_x, cnae, cnae_descr, segment, amount_y):
        self.hash_key = hash_key
        self.year = year
        self.month = months[month]
        self.size = size
        self.nature_type_code = nature_type_code
        self.nature_type_descr = nature_type_descr
        self.city = city
        self.is_branch = True if is_branch == "Sim" else False
        self.amount_x = amount_x
        self.cnae = cnae
        self.cnae_descr = cnae_descr
        self.segment = segment
        self.amount_y = amount_y


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

    def __init__(self, year, month, serial_identifier, nature_type_code, nature_type_descr, city, cp_name, cp_address, cp_total, register_hours_duration):
        self.year = year
        self.month = month
        self.serial_identifier = serial_identifier
        self.nature_type_code = nature_type_code
        self.nature_type_descr = nature_type_descr
        self.city = city
        self.register_hours_duration = register_hours_duration


OPENING_COMPANIES_DICTIONARY = {
    "aberturas": {
        "schema": OpeningCompany,
        "dict": {
            "hash_key": "hash_chave_abertura",
            "year": "ano",
            "month": "mês",
            "size": "porte",
            "nature_type_code": "cod_natureza",
            "nature_type_descr": "descr_natureza",
            "city": "municipio",
            "is_branch": "filial",
            "amount": "qtd",
        }
    },
    "atividades-aberturas": {
        "schema": OpeningCompanyActivities,
        "dict": {
            "hash_key": "hash_chave_abertura",
            "cnae": "cod_atividade",
            "cnae_descr": "descr_atividade",
            "segment": "seguimento",
            "amount": "qtd",
        }
    },
    "tempo-aberturas": {
        "schema": OpeningCompanyTimeSeries,
        "dict": {
            "year": "ano",
            "month": "mês",
            "serial_identifier": "serial",
            "nature_type_code": "cod_natureza",
            "nature_type_descr": "natureza",
            "city": "municipio",
            "cp_name": "cp_nome",
            "cp_address": "cp_endereco",
            "cp_total": "cp_total",
            "register_hours_duration": "registro",
        }
    },
    "opening": {
        "schema": Opening,
        "dict": {
            "hash_key": "hash_chave_abertura",
            "year": "ano",
            "month": "mês",
            "size": "porte",
            "nature_type_code": "cod_natureza",
            "nature_type_descr": "descr_natureza",
            "city": "municipio",
            "is_branch": "filial",
            "amount_x": "qtd_x",
            "cnae": "cod_atividade",
            "cnae_descr": "descr_atividade",
            "segment": "seguimento",
            "amount_y": "qtd_y",
        }
    }
}