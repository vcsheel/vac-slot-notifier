import json
from datetime import date
from json import JSONDecodeError
import constants as cons


def save_user_details(chat_id, dist, age, dose_type):
    data = get_user(chat_id)
    if data is None:
        user_details = dict()
        user_details['dist_id'] = [cons.district_map[dist.lower()]]
        user_details['age'] = int(age)
        user_details['dose_type'] = int(dose_type)

        print('Saving user details....')
        save_user(chat_id, user_details)

    else:
        print('User details found in db')


def save_user(chat_id, user_details):
    with open('users.json', 'r+') as out:
        try:
            data = json.loads(out.read())
        except JSONDecodeError:
            data = {}

        # print("all users: ", data)
        data[str(chat_id)] = user_details
        out.seek(0)
        out.truncate()
        # print('saving: ', data)
        out.write(json.dumps(data))
    print("User details saved....")


def get_user(chat_id):
    with open('users.json', 'r') as f:
        try:
            data = json.loads(f.read())
        except JSONDecodeError:
            data = {}

        if str(chat_id) in data:
            print('User found...')
            return data[str(chat_id)]
        else:
            print('User not found...')
            return None


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
