from SleePyPhases.recordloaders.MedicalDB import MedicalDB
from SleepHarmonizer import RecordLoaderAlice


class RecordLoaderTSM(RecordLoaderAlice):
    config = {}

    def getMetaData(self, recordName):
        metadata = super().getMetaData(recordName)
        del metadata["patientName"]
        del metadata["patientCode"]
        del metadata["patientAdd"]
        del metadata["technician"]

        db = MedicalDB.get()
        row = db.getRecordData(recordName)
        diagnoses = db.getDiagnoses(recordName)
        metadata["psg_type"] = db.getPSGType(recordName)

        if row is not None:
            patient_id, case_id, recordDate, patientAge, gender = row

            metadata["patient"] = patient_id
            metadata["case"] = case_id
            metadata["age"] = patientAge
            metadata["gender"] = gender
            metadata["startRecord"] = recordDate

        if diagnoses is not None:
            metadata.update(diagnoses)
        
        db.close()

        return metadata
