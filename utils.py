from telebot import types

import constants as cons
from datetime import date

from states import states


def filter_by_age(age, session_min_age_limit):
    if age is None:
        return True
    elif 18 <= int(age) < 45 and session_min_age_limit == 18:
        return True
    elif int(age) >= 45 and session_min_age_limit == 45:
        return True
    else:
        return False


def filter_by_fee(fee, session_fee):
    if fee is None:
        return True
    else:
        return fee == session_fee


def filter_by_dose(dose_type, session, min_available=1):
    if dose_type is None:
        return session['available_capacity'] >= min_available
    else:
        return int(session[cons.doses[dose_type]]) >= min_available


def filter_by_vaccine(vaccine, session_vaccine):
    if vaccine is None:
        return True
    else:
        return vaccine == session_vaccine


def filter_user_pref(user, fee_type, session):
    return filter_by_dose(user['dose_type'], session, user['min_slots']) and filter_by_age(user['age'], session[
        "min_age_limit"]) and filter_by_fee(user['fee_type'], fee_type) and filter_by_vaccine(user['vaccine'],
                                                                                              session['vaccine'])


def map_reverse(obj, org_list: list):
    sub = {v: k for k, v in obj.items()}
    return [sub.get(item) for item in org_list]


def get_age_group_from_age(age):
    try:
        if age >= 45:
            return '45+'
        elif 18 <= age < 45:
            return '18-44'
        else:
            return 'Any'
    except:
        return 'Any'


def get_date():
    return date.today().strftime("%d-%m-%Y")


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


def validate_input(user_input, expected):
    if user_input not in expected:
        return False
    else:
        return True


def create_reply_keyboard(data):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = []
    for key in data:
        buttons.append(types.KeyboardButton(text=key))
    keyboard.add(*buttons)
    return keyboard


def get_dist_for_state(state):
    dists = []
    for i in states:
        if i['state_name'] == state:
            dists.append(i['district_name'])
    return sorted(dists)


def isCancel(msg):
    if msg == '/cancel':
        return True
    else:
        return False
