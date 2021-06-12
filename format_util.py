import constants as cons


def format_message(resp, dose_type):
    message = "\n<strong>Slots Found</strong>\n"
    message += "------------\n"
    for key_date, centers in resp.items():
        message += "\n<b><ins>" + key_date + "</ins></b>\n"
        for center in centers:
            message += "\n<pre><code>"
            message += center['center_name'] + ", " + center['district'] + " -- Dose " + str(dose_type) + " : " + str(
                center[cons.doses[dose_type]])
            message += "</code></pre>\n"

    message += '\n <b>Visit</b> <a href="' + cons.cowin_register_url + '"> CoWIN </a> <b>portal to register</b>'
    return message


## {"dist_id": ["hyderabad", "rangareddy"], "age": 23, "dose_type": 2}
def format_user_details(user):
    message = "<b> Your saved choice: </b>\n\n"
    message += "- Age : " + str(user['age']) + '\n'
    message += "- Dose : " + str(user['dose_type']) + '\n'
    message += "- Notify for slots : " + str(user['notify']) + '\n'
    message += "- District(s) : "
    dists = ", ".join(user['dist_id'])
    message += dists

    return message


def show_help_message():
    message = "I can help you look for a  slot and notify you whenever it's available\n"
    message += "You can use following commands - \n"
    message += "/start - Stars your slot checking process\n"
    message += "/update - Update your details\n"
    message += "/slots - Get slots for next 7 days\n"
    message += "/add_district - Add a district to your list\n"
    message += "/remove_district - Remove a district from your list\n"
    message += "/my_details - View your details\n"
    message += "/subscribe - Subscribe for notifications every minute\n"
    message += "/unsubscribe - Stop notifications\n"
    return message
