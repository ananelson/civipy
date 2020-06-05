import json

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

def mocked_contact_get_responses(params):
    if params.get('email') == "validunique@example.com":
        data = {'is_error': 0, 'version': 3, 'count': 1, 'id': 3, 'values': [{
            'contact_id' : '10', 'contact_type' : 'Individual', 
            'display_name' : "Valid Unique", 'email' : 'validunique@example.com'
                }]}
        return MockResponse(data, 200)
    else:
        raise Exception("not imeplemnted")

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
