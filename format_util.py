def format_message(resp, dose_type):
    message = "\n<strong>Slots Found</strong>\n"
    for key_date, centers in resp.items():
        message += "\n<b><ins>" + key_date + "</ins></b>\n"
        for center in centers:
            message += "\n<pre><code>"
            message += center['center_name'] + ", " + center['district'] + " -- Dose " + str(dose_type) + " : " + str(
                center[cons.doses[dose_type]])
            message += "</code></pre>\n"
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
