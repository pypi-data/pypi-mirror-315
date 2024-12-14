import sys

from pyPhases.util.Logger import classLogger
from pypika import Table, PostgreSQLQuery as Query
from pypika.queries import QueryBuilder


@classLogger
class MedicalDB:
    connection = None
    client = None
    assocCursor = None
    _instance = None

    config = {
        "user": "root",
        "password": "example",
        "host": "localhost",
        "port": 5432,
        "database": "data",
    }

    @classmethod
    def get(cls) -> "MedicalDB":
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.connect()
        return cls._instance

    def connect(self):

        import psycopg2

        try:
            c = MedicalDB.config
            conn = psycopg2.connect(
                "host=%s port=%i dbname=%s user=%s password=%s"
                % (
                    c["host"],
                    c["port"],
                    c["database"],
                    c["user"],
                    c["password"],
                )
            )

        except psycopg2.Error as e:
            self.logError(f"Error connecting to Postgres Platform: {e}")
            sys.exit(1)
        self.conn = conn
        self.cursor = conn.cursor()

    def execute(self, sql, **vars):
        if isinstance(sql, QueryBuilder):
            sql = sql.get_sql()
        return self.cursor.execute(sql, **vars)

    def executeAndFetch(self, sql, **vars):
        self.execute(sql, **vars)
        return self.cursor.fetchall()

    def commit(self):
        self.conn.commit()
    
    def executeAndFetchOne(self, sql, **vars):
        self.execute(sql, **vars)
        return self.cursor.fetchone()

    def close(self):
        if self.connection is not None:
            self.connection.close()

    def fillRecordId(self, id):
        return id

    def getRecordData(self, recordId):
        record = Table("record", schema=self.config["schema"])
        patient = Table("patient", schema=self.config["schema"])
        medCase = Table("medical_case", schema=self.config["schema"])
        q = (
            Query.from_(record)
            .select(patient.id_patient, record.id_medical_case, record.start, patient.date_of_birth, patient.gender)
            .join(medCase).on(record.id_medical_case == medCase.id_medical_case)
            .join(patient).on(patient.id_patient == medCase.id_patient)
            .where(record.id_record == recordId)
        )
        row = self.executeAndFetchOne(q)

        if row is None:
            return None
        
        row = list(row)
        age = None if row[2] or row[3] is None else row[2] - row[3]
        row[3] = age

        return row

    def getDiagnoses(self, recordId):
        diag = Table("diagnosis", schema=self.config["schema"])
        record = Table("record", schema=self.config["schema"])
        medCase = Table("medical_case", schema=self.config["schema"])
        q = Query.from_(diag)\
            .select("diagnosis_category_id", "diagnosis")\
            .join(medCase).on(diag.id_medical_case == medCase.id_medical_case)\
            .join(record).on(medCase.id_medical_case == record.id_medical_case)\
            .where(record.id_record == recordId)\
            .get_sql()
        
        diagnoses = self.executeAndFetch(q)

        diagnoseCats = {d[0]: d[1] for d in diagnoses}
        return diagnoseCats

    def getPSGType(self, recordId):

        record = Table("record", schema=self.config["schema"])
        q = (
            Query.from_(record)
            .select("psg_config")
            .where(record.id_record == recordId)
        )
        r = self.executeAndFetchOne(q)

        return r[0] if bool(r) else ""
