from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database.connector import Connector


db_connector = Connector.get_instance()
db_base = db_connector.get_base()


class ActiveCompany(db_base):
    __tablename__ = "active_companies"

    id = Column(Integer, primary_key=True, index=True)
    hash_key = Column(String(255), unique=True, nullable=False, index=True)
    size = Column(String(255), nullable=False)
    nature_type_code = Column(String(255), nullable=False)
    nature_type_descr = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    is_branch = Column(Boolean, nullable=False)
    amount = Column(Integer, nullable=False)

    def __init__(self, hash_key, size, nature_type_code, nature_type_descr, city, is_branch, amount):
        self.hash_key = hash_key
        self.size = size
        self.nature_type_code = nature_type_code
        self.nature_type_descr = nature_type_descr
        self.city = city
        self.is_branch = True if is_branch == "Sim" else False
        self.amount = amount

class ActiveCompanyActivities(db_base):
    __tablename__ = "active_companies_activities"

    id = Column(Integer, primary_key=True, index=True)
    hash_key = Column(String(255), ForeignKey("active_companies.hash_key"), nullable=False)
    cnae = Column(String(255), nullable=False)
    cnae_descr = Column(String(255), nullable=False)
    is_main_cnae = Column(Boolean, nullable=False)
    segment = Column(String(255), nullable=False)
    amount = Column(Integer, nullable=False)

    company = relationship("ActiveCompany", backref="activities")

    def __init__(self, hash_key, cnae, cnae_descr, is_main_cnae, segment, amount):
        self.hash_key = hash_key
        self.cnae = cnae
        self.cnae_descr = cnae_descr
        self.is_main_cnae = True if is_main_cnae == "Sim" else False
        self.segment = segment
        self.amount = amount


ACTIVE_COMPANIES_DICTIONARY = {
    "empresas-ativas": {
        "schema": ActiveCompany,
        "dict": {
            "hash_key": "hash_chave",
            "size": "porte",
            "nature_type_code": "cod_natureza",
            "nature_type_descr": "natureza",
            "city": "municipio",
            "is_branch": "filial",
            "amount": "qtd",
        }
    },
    "empresas-ativas-atividades": {
        "schema": ActiveCompanyActivities,
        "dict": {
            "hash_key": "hash_chave",
            "cnae": "cod_atividade",
            "cnae_descr": "descr_atividade",
            "is_main_cnae": "principal",
            "segment": "seguimento",
            "amount": "qtd",
        }
    }
}