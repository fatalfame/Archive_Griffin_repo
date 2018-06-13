import requests
import json


api_key = '9723283d7a8815c61c212b4c4643610181aa8e12'
typeform_UID = 'BtfwWY'
survey_list_request_url = 'https://api.typeform.com/v1/form/{0}?key={1}'.format(typeform_UID, api_key)
survey_list_request = requests.get(survey_list_request_url)
survey_list_response = json.loads(survey_list_request.text)
r = requests.get('https://api.typeform.com/v1/form/BtfwWY?key=9723283d7a8815c61c212b4c4643610181aa8e12')
typeform_response = json.loads(r.text)
for t in survey_list_response["stats"]:
    print(t)
for t in typeform_response["questions"]:
    print(t)
for t in typeform_response["responses"]:
    print(t["answers"])