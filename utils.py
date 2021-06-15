from datetime import date

from telebot import types, util

import constants as cons
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


def is_dose_amount_changed(d_type, r, b_in_A):
    if d_type is None:
        return r["available_capacity_dose2"] > b_in_A['available_capacity_dose2'] or r["available_capacity_dose1"] > \
               b_in_A['available_capacity_dose1']
    else:
        return r[d_type] > b_in_A[d_type]


def get_splitted_text(response_text):
    split_text = util.split_string(response_text, 3000)

    resp_list = []
    # print("Split:", len(split_text))
    for i in range(len(split_text)):
        # print(i, "-", len(split_text[i]))
        final_txt = split_text[i]
        if i < len(split_text) - 1:
            part = split_text[i].rpartition('</code></pre>\n')
            # print(len(part[0]),part[1], len(part[2]))
            # print('--------------')
            split_text[i + 1] = part[2] + split_text[i + 1]
            final_txt = part[0] + part[1]
        resp_list.append(final_txt)
    return resp_list


def filter_new_centers(current, prev, user):
    f_resp = {}
    print('----------------------------------------')
    print('----------------------------------------')

    for key, B in current.items():
        if key in prev:
            A = prev[key]

            res = []
            for b in B:
                r = dict(b)
                b_in_A = next(
                    (a for a in A if b["center_name"] == a["center_name"] and b["min_age_limit"] == a["min_age_limit"]),
                    None)
                if b_in_A:
                    print('Found matching center: ', b_in_A['center_name'])

                    user_d_t = cons.doses.get(user['dose_type'])

                    if is_dose_amount_changed(user_d_t, r, b_in_A):
                        print('Diff found in slots... adding to return list')
                        res.append(r)

                else:
                    print('Entry not in prev saved notification...', r['center_name'], " - ", r['min_age_limit'])
                    res.append(r)

            if len(res) > 0:
                f_resp[key] = res

        else:
            print("Date not found in prev")
            f_resp[key] = B
    print('----------------------------------------')
    print('----------------------------------------')
    return f_resp
