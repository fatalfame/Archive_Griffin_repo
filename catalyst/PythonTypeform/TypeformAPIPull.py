from tc_writer import Writer
from formater import DataFormatter
from Typeform_client import TypeformClient

import logging
import collections

__author__ = 'Kevin Wood'
# Documentation found at: https://www.typeform.com/help/data-api/ #

logging.basicConfig(filename="C:\SourceFiles\Typeform\logs\Typeform.log", level=logging.INFO)

# ------------------------------------------------------------------------------------------------#
# ----------------------------------- START PULLING TYPEFORM -------------------------------------#
# ------------------------------------------------------------------------------------------------#

logging.info("Started Pulling Typeform Report(s) at:" + str(TypeformClient.now))

# ------------------------------------------------------------------------------------------------#
# ------------------------------- GET SURVEYS FROM TYPEFORM --------------------------------------#
# ------------------------------------------------------------------------------------------------#

survey_list_response = {}

try:
    survey_list_response = TypeformClient().get_surveys(TypeformClient.api_key)
except Exception, e:
    logging.info("Error in Survey List request to Typeform")
    logging.info("@@Error: " + str(e))

# Loop through each survey belonging to Health Catalyst in order to parse each report into a csv
for survey in range(len(survey_list_response)):
    question_result = []
    question_dict = collections.OrderedDict()
    survey_dict = {}
    survey_result = []

    typeform_UID = survey_list_response[survey]["id"]

    typeform_name = survey_list_response[survey]["name"]
    survey_dict["SurveyNM"] = typeform_name
    survey_dict["SurveyID"] = typeform_UID

    # ------------------------------------------------------------------------------------------------#
    # ------------------------- GET SURVEY SUBMISSIONS FROM TYPEFORM ---------------------------------#
    # ------------------------------------------------------------------------------------------------#
    # Set up API connection for fetching the Typeform JSON data
    try:
        typeform_response = TypeformClient().get_typeforms(TypeformClient.api_key, typeform_UID)

    except Exception, e:
        logging.info("Error in Responses request to Typeform")
        logging.info("@@Error: " + str(e))

    # ------------------------------------------------------------------------------------------------#
    # ----------------------- PARSE TYPEFORM RESPONSE FOR QUESTION RESULT ----------------------------#
    # ------------------------------------------------------------------------------------------------#

    # Loop through JSON response list of "questions" and set id's to questions of those id's as key-value pairs
    # Also create a list with the question_dict and write it to a separate file in order to serve as a table in
    # SMD so that question ID's can be used as column names instead of questions in SMD tables
    for question in typeform_response["questions"]:
        # Question_table_dict is specifically for writing out to the Questions table
        question_table_dict = {}
        question_id = question["id"]
        pre_value = question["question"]
        question_txt = pre_value.replace("<strong>", "").replace("</strong>", "").replace("<br />", "")\
            .encode("ascii", errors="ignore")
        if question_id != "hidden_id" and question_id != "hidden_name":
            question_table_dict["QuestionID"] = question_id
            question_table_dict["QuestionTXT"] = question_txt
            question_table_dict["SurveyID"] = typeform_UID
            # add question_id and txt key-value pair to Question Dict, which will be used to get questions and answers
            # for QuestionResponse table
            question_dict[question_id] = question_txt
            question_result.append(question_table_dict)

    # ------------------------------------------------------------------------------------------------#
    # ----------- PARSE TYPEFORM RESPONSE FOR SURVEY SUBMISSION & QUESTION RESPONSE RESULTS ----------#
    # ------------------------------------------------------------------------------------------------#

    # Create an empty list for survey submission and answer results that will be filled with dictionaries made up of
    # JSON response
    survey_submission_result = []
    answer_result = []

    # Loop through each response in the JSON response list of "responses" and fill a dictionary of "answers"
    # with each survey submission's respective answers
    for response in typeform_response["responses"]:
        # Create an empty dictionary that will be filled with key-value pairs of actual questions
        # (not id's) and each survey submission's respective answers
        survey_submission_dict = {}
        answer_dict = response["answers"]

        # Some reports have a JSON response that has the survey_submission name paired with the "id" key as opposed to
        # the "name" key, so this try-except appropriately handles these differences
        if len(response["hidden"]) != 0:
            try:
                name = response["hidden"]["name"]
                survey_submission_dict["RespondentNameCD"] = name
                # WATCH OUT FOR THIS EXCEPTION BEING TOO BROAD!!!!!!!
            except KeyError:
                name_id = response["hidden"].get("id", [])
                survey_submission_dict["RespondentNameCD"] = name_id
        else:
            survey_submission_dict["RespondentNameCD"] = []
        # Must get each surveysubmission/survey submission's "metadata" as Typeform names it, or just there personal
        # info BEFORE going into the nested loop of their responses
        token = response["token"]
        survey_submission_dict["SurveySubmissionID"] = token

        network_id = response["metadata"].get("network_id", [])
        survey_submission_dict["NetworkID"] = network_id

        start_date = response["metadata"].get("date_land", [])
        survey_submission_dict["StartDTS"] = start_date

        submit_date = response["metadata"].get("date_submit", [])
        survey_submission_dict["SubmitDTS"] = submit_date

        survey_submission_dict["SurveyID"] = typeform_UID
        #print response["hidden"]
        if len(response["hidden"]) !=0:
            try:
                if len(response["hidden"]["servicename"]) !=0:
                    survey_submission_dict["servicename"]=response["hidden"]["servicename"]
                else:
                    survey_submission_dict["servicename"] = None
            except KeyError:
                survey_submission_dict["servicename"] = None
            try:
                if response["hidden"]["client"] != None:
                    if  len(response["hidden"]["client"]) != 0:
                        survey_submission_dict["client"] = response["hidden"]["client"]
                    else:
                        survey_submission_dict["client"] = None
                else:

                    survey_submission_dict["client"] = None
            except KeyError:
                survey_submission_dict["client"] = None

        else:
            survey_submission_dict["servicename"] = None
            survey_submission_dict["client"] = None



        survey_submission_result.append(survey_submission_dict)

        # Find where question_dict keys (e.g. "list_26061842_choice") and answer_dict keys (e.g. "list_26061842_choice)
        # match in order to write the associated values as a key-value pair
        for key in question_dict:

            question_answer_dict = collections.OrderedDict()
            # If the question_dict key is in the answer_dict then create key-value pair unless a
            # respondent/surveysubmission doesn't answer a question
            if key in answer_dict:
                question_answer_dict["QuestionID"] = key
                question_answer_dict["SurveySubmissionID"] = token
                question_answer_dict["SurveyID"] = typeform_UID
                question_answer_dict["SurveyNM"] = typeform_name
                value = answer_dict[key]
                # Strip any text responses of any commas or returns in order to satisfy EDW data requirements
                final_value = value.replace(',', '').replace('\n', '')
                question_answer_dict["QuestionResponseVAL"] = final_value

            else:
                value = None
                question_answer_dict["QuestionID"] = key
                question_answer_dict["SurveySubmissionID"] = token
                question_answer_dict["SurveyID"] = typeform_UID
                question_answer_dict["SurveyNM"] = typeform_name
                question_answer_dict["QuestionResponseVAL"] = value

            answer_result.append(question_answer_dict)

    survey_result.append(survey_dict)

    # DataFormatter ensures that the result data is in the proper format for the EDW
    final_answer_result = DataFormatter().format_data(answer_result)

    final_survey_submission_result = DataFormatter().format_data(survey_submission_result)

    # Try writing each of the lists of dictionaries to csv files and output error message in log file upon failure
    try:
        Writer().write_to_file(survey_result, TypeformClient.survey_filename)
    except Exception, e:
        logging.info("Error: Survey table not able to be written from Typeform response.")
        logging.info("@@Error: " + str(e))

    try:
        Writer().write_to_file(question_result, TypeformClient.question_filename)
    except Exception, e:
        logging.info("Error: Question table not able to be written from Typeform response.")
        logging.info("@@Error: " + str(e))

    # Use IF-ELSE here instead of TRY-EXCEPT because some lines may be null and will throw off the Writer's
    # ability to writer column headers for a column
    if final_answer_result:
        Writer().write_to_file(final_answer_result, TypeformClient.answer_filename)

    if final_survey_submission_result:
        Writer().write_to_file(final_survey_submission_result, TypeformClient.survey_submission_filename)

logging.info("Completed Typeform Report(s) Pull at:" + str(TypeformClient.now))
# ------------------------------------------------------------------------------------------------#
# ----------------------------------- COMPLETED TYPEFORM PULL ------------------------------------#
# ------------------------------------------------------------------------------------------------#
