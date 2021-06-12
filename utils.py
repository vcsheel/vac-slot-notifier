import requests
import json
import constants


def get_next7days_by_district(dist_ids, date):
    url = constants.calendarByDistrict_url
    # headers = {'Origin': 'https://apisetu.gov.in'}
    data = {}

    for dist_id in dist_ids:
        payload = {'district_id': dist_id, 'date': date}
        response = requests.get(url, headers=constants.headers, params=payload)
        # print(response.request.headers)
        print(response.url)
        if response.status_code == 200:
            try:
                data['centers'].extend(response.json()['centers'])
            except:
                data = response.json()
        else:
            print(response.json())

    return data


def get_next7days_by_pin(pincodes, date):
    url = constants.calendarByPin_url
    # headers = {'Origin': 'https://apisetu.gov.in'}
    data = {}

    for pin in pincodes:
        payload = {'pincode': pin, 'date': date}
        response = requests.get(url, headers=constants.headers, params=payload)
        # print(response.request.headers)
        print(response.url)
        if response.status_code == 200:
            try:
                data['centers'].extend(response.json()['centers'])
            except:
                data = response.json()
        else:
            print(response.json())

    return data


# get_next7days_by_district(581, "12-06-2021")
def create_resp_session(session, center):
    resp = dict()
    resp['center_name'] = center['name']
    resp['fee_type'] = center['fee_type']
    resp['district'] = center['district_name']
    # resp['min_age_limit'] = session['min_age_limit']
    resp['vaccine'] = session['vaccine']
    resp['available_capacity_dose1'] = session['available_capacity_dose1']
    resp['available_capacity_dose2'] = session['available_capacity_dose2']
    return resp


def get_availability_from_data(data, dose_type, age):
    response = {}
    if data:
        for center in data['centers']:
            for session in center['sessions']:
                if int(session[constants.doses[dose_type]]) > 0 and age >= int(session["min_age_limit"]):
                    # print(session[doses[dose_type]])
                    date = session['date']
                    resp = create_resp_session(session, center)
                    if date not in response:
                        response[date] = [resp]
                    else:
                        response[date].append(resp)
    else:
        print("Received empty data")
    # print(response)
    return response
