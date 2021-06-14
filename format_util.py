import constants as cons
from utils import get_age_group_from_age


def format_message(resp):
    message = "\n<strong>Slots Found</strong>\n"
    message += "------------\n"
    for key_date, centers in resp.items():
        message += "\n<b><ins>" + key_date + "</ins></b>\n"
        for center in centers:
            message += "\n<pre><code>"
            message += center['center_name'] + '\n'
            message += center['district'] + " - "
            message += str(center['pincode']) + '\n'
            message += center['vaccine'] + " - " + center['fee_type'] + '\n'
            message += "Dose 1" + " : " + str(center[cons.doses[1]])
            message += " | "
            message += "Dose 2" + " : " + str(center[cons.doses[2]])
            message += "</code></pre>\n"

    message += '\n <b>Visit</b> <a href="' + cons.cowin_register_url + '"> CoWIN </a> <b>portal to register</b>'
    return message


def safe_str_conversion(text):
    return str(text if text else 'Any')


## {"dist_id": ["hyderabad", "rangareddy"], "age": 23, "dose_type": 2}
def format_user_details(user):
    message = "<b> Your saved choice: </b>\n\n"
    message += "- Age Group: " + get_age_group_from_age(user['age']) + '\n'
    message += "- Vaccine: " + safe_str_conversion(user['vaccine']) + '\n'
    message += "- Fee: " + safe_str_conversion(user['fee_type']) + '\n'
    message += "- Dose : " + safe_str_conversion(user['dose_type']) + '\n'
    message += "- Notify for slots : " + str(user['notify']) + '\n'
    message += "- District(s) : "
    dists = ", ".join(user['dist_id'])
    message += dists

    return message


def show_help_message():
    message = "Hi, I can help you look for a  slot and notify you whenever it's available\n"
    message += "You can use following commands - \n\n"

    for cmd in cons.command_list:
        message += '/' + cmd + '\n'
    return message
