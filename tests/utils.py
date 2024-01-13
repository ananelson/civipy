import json

AUTH_ERROR_TEXT = {"error_message": "Failed to authenticate key", "is_error": 1}


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        self.url = "http://civipy/tests"

    def json(self):
        return self.json_data


def mocked_contact_create_responses(params):
    if params.get("contact_id") == "10":
        data = {
            "is_error": 0,
            "version": 3,
            "count": 1,
            "id": 3,
            "values": {
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
                    "modified_date": "2020-06-05 21:40:53",
                }
            },
        }
        return MockResponse(data, 200)
    else:
        raise Exception(str(params))


def mocked_contact_get_responses(params):
    if params.get("email") == "validunique@example.com":
        data = {
            "is_error": 0,
            "version": 3,
            "count": 1,
            "id": 3,
            "values": [
                {
                    "contact_id": "10",
                    "contact_type": "Individual",
                    "display_name": "Valid Unique",
                    "email": "validunique@example.com",
                }
            ],
        }
        return MockResponse(data, 200)
    elif params.get("email") == "unknown@example.com":
        data = {"is_error": 0, "version": 3, "count": 0, "values": []}
        return MockResponse(data, 200)
    else:
        raise Exception("not implemented")


def mocked_contribution_get_response(params):
    if params.get("trxn_id") == "12345":
        data = {
            "is_error": 0,
            "undefined_fields": ["contribution_test", "trxn_id"],
            "version": 3,
            "count": 1,
            "id": 55,
            "values": [
                {
                    "contact_id": "154",
                    "contact_type": "Individual",
                    "contact_sub_type": "",
                    "sort_name": "Donor, Sample",
                    "display_name": "Sample Donor",
                    "contribution_id": "55",
                    "currency": "USD",
                    "receive_date": "2020-09-03 12:40:59",
                    "non_deductible_amount": "",
                    "total_amount": "200.00",
                    "fee_amount": "4.70",
                    "net_amount": "195.30",
                    "trxn_id": "12345",
                    "invoice_id": "",
                    "cancel_date": "",
                    "cancel_reason": "0",
                    "receipt_date": "2020-09-03 16:41:27",
                    "thankyou_date": "",
                    "contribution_source": "Online Contribution",
                    "amount_level": "",
                    "is_test": "0",
                    "is_pay_later": "0",
                    "contribution_status_id": "1",
                    "check_number": "",
                    "contribution_campaign_id": "",
                    "financial_type_id": "1",
                    "financial_type": "Donation",
                    "product_id": "",
                    "product_name": "",
                    "sku": "",
                    "contribution_product_id": "",
                    "product_option": "",
                    "fulfilled_date": "",
                    "contribution_start_date": "",
                    "contribution_end_date": "",
                    "contribution_recur_id": "",
                    "financial_account_id": "1",
                    "accounting_code": "",
                    "contribution_note": "",
                    "contribution_batch": "",
                    "contribution_status": "Completed",
                    "payment_instrument": "Credit Card",
                    "payment_instrument_id": "1",
                    "instrument_id": "1",
                    "contribution_check_number": "",
                    "contribution_campaign_title": "",
                    "id": "55",
                    "contribution_type_id": "1",
                }
            ],
        }
        return MockResponse(data, 200)
    elif params.get("trxn_id") == "00000":
        data = {"is_error": 0, "version": 3, "count": 0, "values": []}
        return MockResponse(data, 200)
    else:
        raise Exception("not implemented")


def mocked_requests_get(*args, **kwargs):
    entity, action, json_params = deconstruct_params(kwargs["params"])

    if entity == "Contact":
        if action == "get":
            return mocked_contact_get_responses(json_params)
        else:
            raise Exception("action %s not implemented for %s" % (action, entity))
    elif entity == "Contribution":
        if action == "get":
            return mocked_contribution_get_response(json_params)
        else:
            raise Exception("action %s not implemented for %s" % (action, entity))
    else:
        raise Exception("entity %s not implemented" % entity)

    return MockResponse(None, 404)


def mocked_requests_post(*args, **kwargs):
    entity, action, json_params = deconstruct_params(kwargs["params"])

    if entity == "Contact":
        if action == "create":
            return mocked_contact_create_responses(json_params)
        else:
            raise Exception("action %s not implemented for %s" % (action, entity))
    else:
        raise Exception("entity %s not implemented" % (entity))

    return MockResponse(None, 404)


def deconstruct_params(params):
    excluded_keys = {"api_key", "debug", "key", "json", "sequential"}
    json_params = {k: v for k, v in params.items() if k not in excluded_keys}
    entity = json_params.pop("entity")
    action = json_params.pop("action")
    return entity, action, json_params
