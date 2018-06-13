__author__ = 'Kevin Wood'
## Documentation found at: https://www.typeform.com/help/data-api/ ##
import requests
import json
import datetime

from datetime import timedelta, date

class TypeformClient:
    api_key = '9723283d7a8815c61c212b4c4643610181aa8e12'
    typeform_UID = 'BtfwWY'
    FilePrefix = "C:/SourceFiles/Typeform/"
    now = datetime.datetime.now()
    Date_as_of = str(date.today() - timedelta(days=1))
    survey_filename = '{0}Survey_asof-{1}.csv'.format(FilePrefix, Date_as_of)
    answer_filename = '{0}QuestionResponse_asof-{1}.csv'.format(FilePrefix, Date_as_of)
    survey_submission_filename = '{0}SurveySubmission_asof-{1}.csv'.format(FilePrefix, Date_as_of)
    question_filename = '{0}Question_asof-{1}.csv'.format(FilePrefix, Date_as_of)


    def get_surveys(self, api_key):
        # Set up API connection for fetching the list of Typeform UID's
        survey_list_request_url = 'https://api.typeform.com/v1/forms?key={0}'.format(api_key)
        survey_list_request = requests.get(survey_list_request_url)
        survey_list_response = json.loads(survey_list_request.text)

        return survey_list_response

    def get_typeforms(self, api_key):
        typeform_request_url = 'https://api.typeform.com/v1/forms?key={0}'.format(api_key)
        typeform_request = requests.get(typeform_request_url)
        typeform_response = json.loads(typeform_request.text)
        return typeform_response