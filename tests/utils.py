import json

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

def mocked_contact_create_responses(params):
    if params.get('contact_id') == "10":
        data = { "is_error": 0, "version": 3, "count": 1, "id": 3, "values": {
            "10": {
                "id": "10",
                "contact_type": "Individual",
                "contact_sub_type": "",
                "do_not_email": "0",
                "do_not_phone": "0",
                "do_not_mail": "0",
                "do_not_sms": "0",
                "do_not_trade": "0",
                "is_opt_out": "0",
                "legal_identifier": "",
                "display_name": "Updated Name",
                "legal_name": "",
                "image_URL": "",
                "preferred_communication_method": "",
                "preferred_language": "en_US",
                "preferred_mail_format": "Both",
                "prefix_id": "",
                "suffix_id": "",
                "formal_title": "",
                "communication_style_id": "1",
                "job_title": "",
                "gender_id": "",
                "birth_date": "",
                "is_deceased": "0",
                "deceased_date": "",
                "household_name": "",
                "primary_contact_id": "",
                "organization_name": "",
                "sic_code": "",
                "user_unique_id": "",
                "created_date": "2017-12-15 15:55:09",
                "modified_date": "2020-06-05 21:40:53"
        } } }
        return MockResponse(data, 200)
    else:
        raise Exception(str(params))

def mocked_contact_get_responses(params):
    if params.get('email') == "validunique@example.com":
        data = {'is_error': 0, 'version': 3, 'count': 1, 'id': 3, 'values': [{
            'contact_id' : '10', 'contact_type' : 'Individual', 
            'display_name' : "Valid Unique", 'email' : 'validunique@example.com'
                }]}
        return MockResponse(data, 200)
    elif params.get('email') == "unknown@example.com":
        data = { "is_error": 0, "version": 3, "count": 0, "values": [] }
        return MockResponse(data, 200)
    else:
        raise Exception("not implemented")

def mocked_requests_get(*args, **kwargs):
    entity = kwargs['params']['entity']
    action = kwargs['params']['action']
    json_params = json.loads(kwargs['params']['json'])
    del json_params['sequential']

    if entity == 'Contact':
        if action == 'get':
            return mocked_contact_get_responses(json_params)
        else:
            raise Exception("action %s not implemented for %s" % (action, entity))
    else:
        raise Exception("entity %s not implemented" % (entity))

    return MockResponse(None, 404)

def mocked_requests_post(*args, **kwargs):
    entity = kwargs['params']['entity']
    action = kwargs['params']['action']
    json_params = json.loads(kwargs['params']['json'])
    del json_params['sequential']

    if entity == 'Contact':
        if action == 'create':
            return mocked_contact_create_responses(json_params)
        else:
            raise Exception("action %s not implemented for %s" % (action, entity))
    else:
        raise Exception("entity %s not implemented" % (entity))

    return MockResponse(None, 404)
