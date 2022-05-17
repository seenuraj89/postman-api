#Description - Create parallel responses for surveys
#seenu
#new
#Steps- 1. Get survey token corresponding to Survey
#       2. Get Question structure for the survey
#       3. Prepare random answers for questions based on the type
#       4. Post responses to survey
#new changes
import json
import random
import requests
from datetime import datetime
from locust import HttpLocust, TaskSet, task
import time
import logging
import uuid

#FILE_NAME = 'logs_locust_run.txt'

#API endpoint to which the requests should be posted
#For LA Game, changing demo.dt to app.dt
#post_endpoint = "https://demo.dropthought.com/"
post_endpoint = "https://app.dropthought.com/"

#Token that changes based on the user login
#tibcodt acct
#bearer_token = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0aWJjb2R0QGRyb3B0aG91Z2h0LmNvbSIsInJvbGUiOiJST0xFX1VTRVIiLCJleHAiOjE1OTQyNDgyMzUsImlzcyI6IkRyb3BUaG91Z2h0LCBJbmMifQ.6bPtIoLbcdmuR_FKl8IzGUJD_M9oNw4mbhLlnsjxSSm8Myq2QkIS-vFhCB_nxFOvb_0sX8W9f0OpbOMGa0Y-mg'
#richard acct
#bearer_token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJyaWNoYXJkQGRyb3B0aG91Z2h0LmNvbSIsInJvbGUiOiJST0xFX1VTRVIiLCJleHAiOjE1OTQyNDgxNzAsImlzcyI6IkRyb3BUaG91Z2h0LCBJbmMifQ.CKTc63Mbz_J9xBwLDj1IxspjXZPRLDgRfcvffJsqvwIB1YY4AAaqxgN78k9dwpdUcy3GhxLj7_hPQtfenUhPpw"
#fanx airislabs acct
#bearer_token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhaXJpc2xhYnMuZmFueEBnbWFpbC5jb20iLCJyb2xlIjoiUk9MRV9VU0VSIiwiZXhwIjoxNTk3MTg1ODM0LCJpc3MiOiJEcm9wVGhvdWdodCwgSW5jIn0.BBl8elP-6tEqaVA3-eSajgDL1ff0uWuY9nIwltM6oUMkNRhlUW7bNWWoOvnIDAXBL6cOeZ18UJh8DtnCVSDYdQ"

#app DT anirudh account
bearer_token='eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhbmlydWRoQGJhaHdhbmN5YmVydGVrLmNvbSIsInJvbGUiOiJST0xFX1VTRVIiLCJleHAiOjE2MTI0MzgzMzEsImlzcyI6IkRyb3BUaG91Z2h0LCBJbmMifQ.xeQADa3EeRxKH2ZHXKW-Mn_b4GEiCHQkfujXCati5m25pK6kzEGyCESsfbWAYMI9HrY9nxD7KxgqNQn2jp0bRw'

#To get Token corresponding to survey Id
#For LA Game, changing demo.dt to app.dt
#survey_token_url = "https://demo.dropthought.com/dtapp/api/dtsurvey/generateToken/surveyuuid/"
survey_token_url = "https://app.dropthought.com/dtapp/api/dtsurvey/generateToken/surveyuuid/"
#
#Get the question structure for URL
#For LA Game, changing demo.dt to app.dt
#survey_structure_url = "https://demo.dropthought.com/dtapp/api/surveys/"
survey_structure_url = "https://app.dropthought.com/dtapp/api/surveys/"
#

#Get survey token corresponding to survey
def get_survey_token(survey_id):
    req_get = requests.get(url= survey_token_url + survey_id + "?cc=DT", headers={'Authorization': bearer_token})
    response_dict = req_get.json()
    response = response_dict['result'][0]['token']
    survey_token = response.split("$")[0]
    if not survey_token:
        print ("survey token is empty")
    return survey_token

#Create responses based on question type
def create_random_responses(survey_id, survey_token, ans_type):
    #1-negative, 2- neutral , 3-positive
    out_dict = {}
    #{"data": [{},{}]}
    out_dict['data'] = []

    questions = []
    req_get = requests.get(url=survey_structure_url + survey_id, headers={'Authorization': bearer_token})
    output_dictionary = req_get.json()
    #Get question structure
    if output_dictionary['success']:
        #Added below logic to handle multipage surveys 
        pages = output_dictionary['result']['pages']
        for i in range(0,len(pages)):
            questions.extend(pages[i]['questions'])
    #Added below logic to prepare answers for questions based on type
    for i in range(0,len(questions)):
        dic = {}
        dic['dataId'] = questions[i]['questionId']
        dic['dataType'] = questions[i]['type']
        #Rating question or nps question
        if questions[i]['type'] == "rating" or questions[i]['type'] == "nps":
            low_limit = 0
            high_limit = int(questions[i]['scale']) - 1
            middle = (high_limit - low_limit) // 2 
            #Negative
            if ans_type == 1:
                #Below logic is to handle if scale is 2. As per survey creation page, scale should always be more than 1.
                if (middle < 1):
                    middle = 1
                dic['dataValue'] = [random.randint(low_limit,middle-1)]
            #Neutral
            elif ans_type == 2:
                dic['dataValue'] = [middle]
            #Positive
            else:
                dic['dataValue'] = [random.randint(middle+1, high_limit)]
        #Single Choice question
        if questions[i]['type'] == "singleChoice":
            dic['dataValue'] = [random.randint(0,len(questions[i]['options'])-1)]
        #Multiple choice question
        if questions[i]['type'] == "multiChoice":
            options_len = len(questions[i]['options'])-1
            #random.sample would return a list. 
            dic['dataValue'] = random.sample(range(0,options_len),random.randint(0,options_len))
        #Open question
        if questions[i]['type'] == 'open':
            pos_choice = ['eveything was good ', 'Great food options. Really liked the hamburgers ', 'Mind blowing experience', 'Excitement in the air!!!','It was a great game. The number of tackles and shoots was breathtaking. The game was so engaging!','Great food and drinks offered! The employees were very helpful and nice! Would definitely come back !','Man, security and service staff were brisk today.']
            neg_choice = ['Was not happy with the customer service. ', 'I was happy Intil staff was rude to me.','Needs to improve a lot ','Customer service needs to improve. Everything was slow. ']    
            neutral_choice = ['Parking was a big pain. Had an amazing time otherwise.','I did not pay good money for an experience like this','Okay, but customer service could be better. ','Things could have gone better with that guy in security']
            if ans_type == 1:
                dic['dataValue'] = [random.choice(neg_choice)]
            elif ans_type == 2:
                dic['dataValue'] = [random.choice(neutral_choice)]
            else:
                dic['dataValue'] = [random.choice(pos_choice)]

        out_dict['data'].append(dic)
    #SAG-430: Adding metadata as submissionid will not be there during feedback submission
    #out_dict['metaData'] = {}
    unique_id = str(uuid.uuid4())
    out_dict['metaData'] = {"UniqueId":unique_id}
    #
    out_dict['token'] = survey_token
    return out_dict           
#SAG-430 - To have logging saved in a file, use command like 'locust -f locustfile.py --no-web -c 1 -r 1 --run-time 0h1m --logfile=locustfile.log' when running locust in local.
class UserBehavior(TaskSet):

    @task
    def on_start(self):
        #survey_id_list = ["08a7fcc3-463a-4ea8-833b-bf92609da539","55bbf050-ce4f-4107-9929-fb1500f48767","0fc1d2f3-c26e-4806-b461-d29ea350b156"]
        #survey_id_list = ["0fc1d2f3-c26e-4806-b461-d29ea350b156"]
        survey_id_list=['254bf750-d398-4f7e-b12e-86c51d4c9d77']
        for survey_id in survey_id_list:
            survey_token = get_survey_token(survey_id)
            out_dict = create_random_responses(survey_id, survey_token, random.randint(1,3))
            #SAG-430- Saving logs in a file
            logging.info(out_dict)
            response = self.client.post("dtapp/api/event",json = out_dict, headers = {'Authorization': bearer_token, 'content-type': 'application/json'})
            time.sleep(60)

class WebsiteUser(HttpLocust):
    host = post_endpoint
    task_set = UserBehavior
    #stop_timeout=5
