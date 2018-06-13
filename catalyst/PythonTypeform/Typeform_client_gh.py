"""Documentation found at: https://www.typeform.com/help/data-api/"""
import requests
import json
import csv


fieldnames = ['Survey Name', 'Survey ID', 'ID', 'Field ID', 'Question', 'Response ID', 'Response']
writer = csv.DictWriter(open('multicare.csv', 'w'), fieldnames=fieldnames, lineterminator='\n')
writer.writeheader()

key = '9723283d7a8815c61c212b4c4643610181aa8e12'
UID = 'BtfwWY'
survey_list_request_url = 'https://api.typeform.com/v1/forms?key={0}'.format(key)
survey_list_request = requests.get(survey_list_request_url)
survey_list_response = json.loads(survey_list_request.text)
typeform_request_url = 'https://api.typeform.com/v1/form/{0}?key={1}&completed=true&order_by=completed'.format(UID, key)
typeform_request = requests.get(typeform_request_url)
typeform_response = json.loads(typeform_request.text)
data = {}
questions = {}
answers = {}
for resp in survey_list_response:
    if resp['id'] == UID:
        survey_id = resp['id']
        survey_nm = resp['name']
for q in typeform_response["questions"]:
    if q['id'] != 'hidden_client':
        questions[q['id']] = q["question"].replace('<strong>', '').replace('</strong>', '')
print(questions)
# for s in typeform_response["questions"]:
#     if s["id"] != 'hidden_client':
#         data['Survey Name'] = survey_nm
#         data['Survey ID'] = survey_id
#         data['ID'] = s["id"]
#         data['Field ID'] = s["field_id"]
#         data['Question'] = s["question"].replace('<strong>', '').replace('</strong>', '')
for r in typeform_response["responses"]:
    rx = r["answers"]
    print(rx)
    # answers[r['id']] = r["answers"]
# for key in rx.keys():
#     data['Response ID'] = key
# for value in rx.values():
#     data['Response'] = value
dicts = questions, answers
writer.writerow({'Survey Name': survey_nm, 'Question': questions})
