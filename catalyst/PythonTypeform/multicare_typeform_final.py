"""Documentation found at: https://www.typeform.com/help/data-api/"""
import requests
import csv


client_name = 'MultiCare'
print('Retrieving the %s survey(s)' % client_name)

fieldnames = ['SurveyName', 'SurveyID', 'SurveySubmissionID', 'StartDTS', 'QuestionID', 'QuestionTXT', 'QResponseVAL',
              'ServiceName']
writer = csv.DictWriter(open('multicare.csv', 'w'), fieldnames=fieldnames, lineterminator='\n')
writer.writeheader()

key = '9723283d7a8815c61c212b4c4643610181aa8e12'
# UID = ['BtfwWY', 'H2IWBR']
UID = []

survey_list_request_url = 'https://api.typeform.com/v1/forms?key={}'.format(key)
survey_list_request = requests.get(survey_list_request_url)
survey_list_response = survey_list_request.json()
for s in survey_list_response:
    if client_name in s["name"]:
        UID.append(s["id"])
        print(s["name"])
for u in UID:
    typeform_request_url = 'https://api.typeform.com/v1/form/{}?key={}&completed=true&order_by=completed'.format(u, key)
    typeform_request = requests.get(typeform_request_url)
    typeform_response = typeform_request.json()
    survey_id = u
    survey_ids_to_names = {d['id']: d['name'] for d in survey_list_response}
    survey_name = survey_ids_to_names[survey_id]
    question_ids_to_text = {d['id']: d['question'].replace('<strong>', '').replace('</strong>', '')
                            for d in typeform_response['questions']}

    # for m in typeform_response["responses"]:
        # print(m["token"]) #Survey submission ID
        # print(m["metadata"].get("date_land", [])) #Start DTS
        # print(m["metadata"].get("date_submit", []))
        # print(m["metadata"].get("network_id", []))

    for response in typeform_response['responses']:
        for response_id, answer in response['answers'].items():
            writer.writerow({
                        'SurveyName': survey_name,
                        'SurveyID': u,
                        'SurveySubmissionID': response["token"],
                        'StartDTS': response["metadata"].get("date_land", []),
                        'QuestionID': response_id,
                        'QuestionTXT': question_ids_to_text[response_id],  # Answer IDs and Question IDs are the same.
                        'QResponseVAL': answer,
                        'ServiceName': response["hidden"].get("servicename")})
