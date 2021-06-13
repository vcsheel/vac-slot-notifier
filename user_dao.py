import json
import os
from datetime import date

import redis

import constants as cons

REDIS_URL = os.environ['REDIS_URL']
redis_handle = redis.from_url(url=REDIS_URL)


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
    print("Deleting user ", chat_id)
    resp = redis_handle.delete(chat_id)
    if resp == 0:
        print("no such user found")
        return False
    else:
        print("User Delete op is successful")
        return True


def get_all_user():
    print("Get all users....")
    keys = redis_handle.keys()
    keys = [json.loads(x) for x in keys]

    val = redis_handle.mget(keys)
    val = [json.loads(x) for x in val]

    return dict(zip(keys, val))


# def migrate_db():
#     print("------------------------------------------")
#     print("Starting migration....")
#     print("------------------------------------------")
#     keys = redis_handle.keys()
#     keys = [json.loads(x) for x in keys]
#
#     for i in keys:
#         print("Migrating user ----------- ", i)
#         user = get_user(i)
#         print("Before migration: ", user)
#
#         user['pincodes'] = []
#         user['fee_type'] = None
#         user['vaccine'] = None
#         user['min_slots'] = 1
#         user['check_date'] = None
#
#         redis_handle.set(i, json.dumps(user))
#         print("Migration complete for user.... ", i)
#         print("After migrating: ", get_user(i))
#     print("------------------------------------------")
#     print("Migration completed for all")
#     print("------------------------------------------")


def populate_pref_fields():
    user = dict()
    user['pincodes'] = []
    user['vaccine'] = None
    user['fee_type'] = None
    user['check_date'] = None
    user['min_slots'] = 1
    user['notify'] = False

    return user


def save_user_details(chat_id, dist, age, dose_type, isUpdate):
    user = get_user(chat_id)

    if user and not isUpdate:
        print('User details found in db')
        return

    if not user:
        user = populate_pref_fields()

    user['dist_id'] = [validate_dist(dist)]
    user['age'] = int(age)
    user['dose_type'] = int(dose_type)
    save_user(chat_id, user)
    print('Saving user details - ', chat_id, ' - ', user)
    return user


def save_user_pref(chat_id, age, vaccine, dose, fee_type):
    user = get_user(chat_id)
    if user is None:
        user = {'dist_id': [], 'pincodes': [], 'notify': True}

    user['age'] = int(age) if age else None
    user['dose_type'] = int(dose) if dose else None
    user['vaccine'] = vaccine
    user['fee_type'] = fee_type
    user['check_date'] = None
    user['min_slots'] = 1
    print('Updating filters for user ', chat_id)
    save_user(chat_id, user)


def validate_dist(dist_name):
    try:
        return cons.district_map[dist_name.strip().lower()]
    except:
        return False


def validate_pin(pin):
    if len(pin) == 6:
        return True
    else:
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
