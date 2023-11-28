import functions_framework
from parsons import VAN

@functions_framework.http
def lawn_sign(request):
    request_json = request.get_json(silent=True)

    van_key = '<VAN KEY>'
    s_question = request_json.get('v_sq')
    s_response = request_json.get('v_sr')

    try:
        van = VAN(api_key=van_key, db='MyVoters')

        resp = van.find_person(
            first_name=request_json.get('fname'),
            last_name=request_json.get('lname'),
            street_number=request_json.get('hno'),
            street_name=request_json.get('street'),
            zip=request_json.get('zip'))

        # UNCOMMENT TO ACTIVATE ENTIRE SCRIPT
        van_id = resp['vanId']
        van.apply_survey_response(van_id, s_question, s_response, contact_type_id='75', input_type_id='11')
        
        return str(van_id)
    except:
        van = VAN(api_key=van_key, db='MyCampaign')

        # update person if exists. else create person
        # matching is... weird sometimes
        resp = van.upsert_person_json({
            "firstName": request_json.get('fname'),
            "lastName": request_json.get('lname'),
            "addresses": [{
                "addressLine1": request_json.get('hno') + " " + request_json.get('street'),
                "zipOrPostalCode": request_json.get('zip')
            }],
            "phones": [{
                "phoneNumber": request_json.get('phone')
            }],
            "surveyQuestionResponses": [{
                'surveyQuestionId': s_question,
                'type': 'Volunteer',
                'cycle': 2022,
                'name': 'FSA Lawn Sign',
                'mediumName': 'Lawn',
                'shortName': 'Lawn',
                'scriptQuestion': 'Would you like a lawn sign to show your support for the campaign?',
                'status': 'Active', 
                'responses': [{
                    'surveyResponseId': s_response, 'name': 'Wants Sign', 'mediumName': 'Wan', 'shortName': 'W'
                }]
            }]
        })

        van_id = resp['vanId']
        
        return str(van_id)