from icecream import ic
from sqlalchemy.exc import IntegrityError
import logging
import pandas as pd
import os

from schemas.active_companies import ACTIVE_COMPANIES_DICTIONARY


class DatabaseFileIngester:
    def __init__(self, db, filename: str, default_base_path: str = 'datasets/final/', default_extension: str = '-final.csv', csv_separator: str = ";", csv_decimal: str = ",", csv_encoding: str = "utf-8"):
        self.db = db
        self.filename = filename
        self.default_base_path = default_base_path
        self.default_extension = default_extension
        self.filepath = f'{self.default_base_path}{self.filename}{self.default_extension}'
        self.csv_separator = csv_separator
        self.csv_decimal = csv_decimal
        self.csv_encoding = csv_encoding

        # create log file and configure loggers
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler(f'logs/{self.filename}.log')
        self.handler.setLevel(logging.DEBUG)

        self.integrity_errors_count = 0
        self.hashs_with_integrity_errors = set()
        self.successful_insertions_count = 0
        
    def _verify_existence(self):
        ic(f"Verifying existence of file {self.filepath}")
        #ic(os.listdir(self.default_base_path))
        return os.path.exists(self.filepath)
    
    def _read_csv(self):
        if self._verify_existence():
            ic(f"Reading file {self.filename}")
            return pd.read_csv(
                self.filepath,
                sep=self.csv_separator,
                decimal=self.csv_decimal,
                encoding=self.csv_encoding)
        raise FileNotFoundError(f"File {self.filepath} not found")

    def ingest_into_db(self):
        for index, row in self._read_csv().iterrows():
            if self.filename in list(ACTIVE_COMPANIES_DICTIONARY.keys()):
                schema = ACTIVE_COMPANIES_DICTIONARY[self.filename]["schema"]
                schema_dict = ACTIVE_COMPANIES_DICTIONARY[self.filename]["dict"]
                table_record = schema(**{key: row[value] for key, value in schema_dict.items()})
            else:
                # [TODO: add opening companies]
                raise NotImplementedError("Opening companies ingestion not implemented")
            try:
                self.db.add(table_record)
                self.db.commit()
                self.db.refresh(table_record)
                self.successful_insertions_count += 1
                continue
            except IntegrityError as e:
                self.db.rollback()
                self.integrity_errors_count += 1
                self.hashs_with_integrity_errors.add(table_record.hash_key)
                continue
            except Exception as e:
                ic(f"Error: {e}")
                self.db.rollback()
                self.logger.error(f"Error: {e}")
                raise Exception(f"Error: {e}")
        ic(f"Ingestion of {self.filename} finished")
        return {"successful_insertions": self.successful_insertions_count, "integrity_errors": self.integrity_errors_count}
    
    def generate_insertion_report(self):
        self.logger.addHandler(self.handler)

        ic(f"File: {self.filename}")
        self.logger.info(f"File: {self.filename}")

        ic(f"Successful insertions: {self.successful_insertions_count}")
        self.logger.info(f"Successful insertions: {self.successful_insertions_count}")

        ic(f"Integrity errors: {self.integrity_errors_count}")
        self.logger.info(f"Integrity errors: {self.integrity_errors_count}")

        ic(f"Hashs with integrity errors: {self.hashs_with_integrity_errors}")

        with open(f'logs/{self.filename}-integrity_errors.txt', 'w') as f:
            for hash_key in self.hashs_with_integrity_errors:
                f.write(f"{hash_key}\n")

        self.logger.removeHandler(self.handler)
