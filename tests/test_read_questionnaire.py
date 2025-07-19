import unittest
import json
from fhir.resources.questionnaire import Questionnaire

class TestReadQuestionnaire(unittest.TestCase):

    def test_read_questionnaire(self):
        with open('data/questionnaire.json', 'r') as f:
            questionnaire_data = json.load(f)

        for entry in questionnaire_data.get('entry', []):
            resource = entry.get('resource')
            if resource and resource.get('resourceType') == 'Questionnaire':
                questionnaire = Questionnaire(resource)
                self.assertIsNotNone(questionnaire.title)
                self.assertGreater(len(questionnaire.item), 0)

if __name__ == '__main__':
    unittest.main()
