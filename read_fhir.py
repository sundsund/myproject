import json
from fhir.resources.patient import Patient

with open('data/patient.json', 'r') as f:
    patient_data = json.load(f)

for entry in patient_data.get('entry', []):
    resource = entry.get('resource')
    if resource and resource.get('resourceType') == 'Patient':
        patient = Patient(resource)
        print(f"Patient ID: {patient.id}")
        for name in patient.name:
            print(f"  Name: {' '.join(name.given)} {name.family}")
