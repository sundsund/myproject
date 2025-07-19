import json
from fhir.resources.questionnaire import Questionnaire

with open('data/questionnaire.json', 'r') as f:
    questionnaire_data = json.load(f)

for entry in questionnaire_data.get('entry', []):
    resource = entry.get('resource')
    if resource and resource.get('resourceType') == 'Questionnaire':
        questionnaire = Questionnaire(resource)
        print(f"Questionnaire Title: {questionnaire.title}")
        for item in questionnaire.item:
            print(f"  Question: {item.text}")
