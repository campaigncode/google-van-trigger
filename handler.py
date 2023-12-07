import functions_framework
from parsons import VAN

@functions_framework.http
def handler(request):
    request_json = request.get_json(silent=True)

    van_key = request_json.get('van_key')
    s_question = request_json.get('van_sq')
    s_response = request_json.get('van_sr')
    contact_type_id = request_json.get('van_ct')
    input_type_id = request_json.get('van_it')

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
        van.apply_survey_response(van_id, s_question, s_response, contact_type_id, input_type_id)
        
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
            }]
        })

        van_id = resp['vanId']
        van.apply_survey_response(van_id, s_question, s_response, contact_type_id, input_type_id)
        
        return str(van_id)