import os
import json
import redis
from datetime import date
from json import JSONDecodeError
import constants as cons

REDIS_URL = os.environ['REDIS_URL']
redis_handle = redis.Redis(REDIS_URL)


def get_user(chat_id):
    user = redis_handle.get(chat_id)
    if user:
        return json.loads(user)
    return user


def save_user(chat_id, user_details):
    print("Saving user details .... ", chat_id)
    if user_details:
        return redis_handle.set(chat_id, json.dumps(user_details))
    return False


def delete_user(chat_id):
    print("Deleting user ",chat_id)
    resp = redis_handle.delete(chat_id)
    if resp == 0:
        print("no such user found")
    else:
        print("User Delete op is successful")


def save_user_details(chat_id, dist, age, dose_type, isUpdate):
    data = get_user(chat_id)
    if data is None or isUpdate:
        user_details = dict()
        user_details['dist_id'] = [validate_dist(dist)]
        user_details['age'] = int(age)
        user_details['dose_type'] = int(dose_type)

        try:
            user_details['notify'] = data['notify']
        except:
            user_details['notify'] = False

        print('Saving user details.... ', chat_id)
        save_user(chat_id, user_details)

    else:
        print('User details found in db')


def validate_dist(dist_name):
    try:
        return cons.district_map[dist_name.lower()]
    except:
        return False


def get_date():
    return date.today().strftime("%d-%m-%Y")


def populate_user_details(user_details):
    age = int(user_details[0])
    dist = user_details[1]
    dose_type = int(user_details[2])
    check_date = get_date()
    if len(user_details) == 4:
        check_date = user_details[3]
    return age, dist, dose_type, check_date
