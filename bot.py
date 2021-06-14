import threading
from datetime import datetime, timedelta

import flask
import telebot
from flask import Flask
from telebot.apihelper import ApiTelegramException
from timeloop import Timeloop

from constants import *

from rest import *
from user_dao import *
from format_util import *
from utils import validate_dist, validate_pin, validate_input, create_reply_keyboard, get_dist_for_state, isCancel

my_secret = os.environ['API_KEY']
app = Flask(__name__)
bot = telebot.TeleBot(my_secret)

WEBHOOK_URL = cons.HOST_URL + my_secret
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

tl = Timeloop()


@bot.message_handler(commands=['help'])
def help_menu(message):
    bot.send_message(message.chat.id, show_help_message())


@bot.message_handler(commands=['lookup'])
def start(message):
    sent_msg = bot.send_message(message.chat.id, "Enter your age, district, dose number (1 or 2) separated by comma")
    bot.register_next_step_handler(sent_msg, dist_handler, False)


# @bot.message_handler(commands=['update'])
# def update_user_config(message):
#     sent_msg = bot.send_message(message.chat.id, "Enter your age, district, dose number (1 or 2) separated by comma")
#     bot.register_next_step_handler(sent_msg, dist_handler, True)


@bot.message_handler(commands=['delete'])
def delete_user_config(message):
    sent_msg = bot.send_message(message.chat.id, "Are you sure you want to delete your data : (yes/no)")
    bot.register_next_step_handler(sent_msg, delete_user_handle)


@bot.message_handler(commands=['add'])
def add_dist_input(message):
    if get_user(message.chat.id):
        send_stepper_msg(message.chat.id, state_text, all_states, add_to_user_dists)
    else:
        bot.send_message(message.chat.id, "User not found, please register using /start")


@bot.message_handler(commands=['remove'])
def add_dist_input(message):
    user = get_user(message.chat.id)
    if user:
        dists = map_reverse(cons.district_map, user['dist_id'])
        send_stepper_msg(message.chat.id, "Select the entry which you want to remove", dists, remove_from_user_dists, dists)


@bot.message_handler(commands=['details'])
def get_user_saved_details(message):
    user = get_user(message.chat.id)
    if user is not None:
        user['dist_id'] = map_reverse(cons.district_map, user['dist_id'])
        bot.send_message(message.chat.id, format_user_details(user), parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "Your preference not saved, use /start to save")


@bot.message_handler(commands=['slots'])
def get_slots(message):
    date_c = date.today().strftime("%d-%m-%Y")
    print('Getting slots.........')
    user = get_user(message.chat.id)
    if user is not None:
        get_available_slots(message.chat.id, user, date_c)
    else:
        bot.send_message(message.chat.id, "User not found, please register using /start")


@bot.message_handler(commands=['subscribe'])
def start_user_thread(message):
    user = get_user(message.chat.id)
    if user is not None:
        if not user['notify']:
            user['notify'] = True
            save_user(message.chat.id, user)
        else:
            bot.send_message(message.chat.id, "You already have an active subscription")
            return
    else:
        bot.send_message(message.chat.id, "Your Preference not found, please register using /start")
        return

    print('Subscription success for ', message.chat.id)
    bot.send_message(message.chat.id, "Subscription successful, you will be notified for slots when available")


@bot.message_handler(commands=['unsubscribe'])
def pause_notifier(message):
    user = get_user(message.chat.id)
    if user is not None:
        if user['notify']:
            user['notify'] = False
            save_user(message.chat.id, user)
            print('Subscription removed for user ', message.chat.id)
            bot.send_message(message.chat.id, 'Subscription notification removed')
        else:
            bot.send_message(message.chat.id, "You don't have any active Subscription")
    else:
        bot.send_message(message.chat.id, "Your Preference not found, please register using /start")
        return


@bot.message_handler(commands=['find_by_pin'])
def get_slot_for_pin(message):
    sent_msg = bot.send_message(message.chat.id, "Enter your age, pincode, dose number (1 or 2) separated by comma")
    bot.register_next_step_handler(sent_msg, pincode_handler)


def pincode_handler(message):
    user_details = [x.strip() for x in message.text.split(',')]
    if len(user_details) < 3:
        bot.send_message(message.chat.id, "Invalid Entry, /find_by_pin again")
    else:
        age, pin, dose_type, check_date = populate_user_details(user_details)

        if not validate_pin(pin):
            bot.send_message(message.chat.id, "Invalid pincode")
            return

        # save/update user
        # save_user_details(message.chat.id, dist, age, dose_type, isUpdate)
        # if not isUpdate:
        user = populate_pref_fields()
        user['pincodes'].append(pin)
        user['dose_type'] = dose_type
        user['age'] = age
        get_available_pincode_slots(message.chat.id, user, check_date)
        # else:
        #     bot.send_message(message.chat.id, "Your preference have been updated - check /my_details")


def add_to_user_dists(message):
    if isCancel(message.text):
        handle_cancel(message)
        return
    state = message.text
    if validate_input(state, all_states):
        dists = get_dist_for_state(state)
        send_stepper_msg(message.chat.id, dist_text, dists, dist_add_handler, dists)

    else:
        wrong_input_message(message.chat.id)
        send_stepper_msg(message.chat.id, state_text, all_states, add_to_user_dists)


def dist_add_handler(message, dists):
    if isCancel(message.text):
        handle_cancel(message)
        return
    dist = message.text

    if validate_input(dist, dists):
        ## add dist to user dist
        user = get_user(message.chat.id)
        if user is not None:
            new_dist_id = validate_dist(dist)

            if len(user['dist_id']) >= 2:
                bot.send_message(message.chat.id, "You can add only 2 district max", reply_markup=types.ReplyKeyboardRemove())
                return

            if new_dist_id not in user['dist_id']:
                user['dist_id'].append(new_dist_id)
                save_user(message.chat.id, user)
                bot.send_message(message.chat.id, "Saved to your list", reply_markup=types.ReplyKeyboardRemove())
            else:
                bot.send_message(message.chat.id, "District already saved in your list", reply_markup=types.ReplyKeyboardRemove())
        else:
            bot.send_message(message.chat.id, "User not found, please register using /start", reply_markup=types.ReplyKeyboardRemove())
    else:
        wrong_input_message(message.chat.id)
        send_stepper_msg(message.chat.id, dist_text, dists, dist_add_handler, dists)


def remove_from_user_dists(message, dists):
    user = get_user(message.chat.id)
    if user is not None:
        selected_item = message.text

        if selected_item not in dists:
            bot.send_message(message.chat.id, "District not in your saved list", reply_markup=types.ReplyKeyboardRemove())
        else:
            user['dist_id'].remove(validate_dist(selected_item))
            save_user(message.chat.id, user)
            bot.send_message(message.chat.id, "Removed from your list", reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, "User not found, please register using /start", reply_markup=types.ReplyKeyboardRemove())


def delete_user_handle(message):
    res = message.text.lower()
    if res == 'yes':
        print('deleting user ', message.chat.id, '.....')
        is_del = delete_user(message.chat.id)
        if is_del:
            bot.send_message(message.chat.id, "Your preference data has been removed")
        else:
            bot.send_message(message.chat.id, "No preference data found")


def dist_handler(message, isUpdate):
    user_details = [x.strip() for x in message.text.split(',')]
    if len(user_details) < 3:
        bot.send_message(message.chat.id, "Invalid Entry, /start again")
    else:
        age, dist, dose_type, check_date = populate_user_details(user_details)
        dist_id = validate_dist(dist)
        if not dist_id:
            bot.send_message(message.chat.id, "Invalid district")
            return

        # save/update user
        user = save_user_details(message.chat.id, dist, age, dose_type, isUpdate)
        if not isUpdate:
            user = populate_pref_fields()
            user['dist_id'] = [dist_id]
            user['age'] = age
            user['dose_type'] = dose_type
            get_available_slots(message.chat.id, user, check_date)
        else:
            bot.send_message(message.chat.id, "Your preference have been updated - check /my_details")


def get_available_pincode_slots(chat_id, user, check_date):
    data = get_next7days_by_pin(user['pincodes'], check_date)
    resp = None
    if data is not None:
        resp = get_availability_from_data(data, user)
    # print(resp)
    if resp is not None and len(resp) > 0:
        print('Slots found for ', chat_id, ' for total ', len(resp), ' days')
        bot.send_message(chat_id, text=format_message(resp), parse_mode="HTML")
    else:
        print('No slots found for ', chat_id, "on next 7 days of ", check_date)
        bot.send_message(chat_id, "No slots found")


def process_error(error, chat_id):
    if error['error_code'] == 403 and error['description'] == blocker_user_error:
        print(error['description'], chat_id)
        delete_user(chat_id)


def get_available_slots(chat_id, user, check_date, isThreaded=False):
    data = get_next7days_by_district(user['dist_id'], check_date)
    resp = None
    if data is not None:
        resp = get_availability_from_data(data, user)
    # print(resp)
    if resp is not None and len(resp) > 0:
        print('Slots found for ', chat_id, ' for total ', len(resp), ' days')
        response_text = format_message(resp)
        split_text = telebot.util.split_string(response_text, 3000)
        for text in split_text:
            try:
                bot.send_message(chat_id, text=text, parse_mode="HTML")
            except ApiTelegramException as e:
                print("User...exception while sending message", chat_id, " -- ", e)
                process_error(e.result_json, chat_id)

    else:
        print('No slots found for ', chat_id, "on next 7 days of ", check_date)
        if not isThreaded:
            try:
                bot.send_message(chat_id, "No slots found")
            except ApiTelegramException as e:
                print("User...exception while sending message", chat_id, " -- ", e)
                process_error(e.result_json, chat_id)


#################################


def wrong_input_message(chat_id):
    bot.send_message(chat_id, 'Wrong input..., Try again or /cancel to abort')


def send_stepper_msg(chat_id, text, keyboard, state_handler, *arg):
    sent_msg = bot.send_message(chat_id, text, reply_markup=create_reply_keyboard(keyboard))
    bot.register_next_step_handler(sent_msg, state_handler, *arg)


@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    bot.send_message(message.chat.id, "Operation cancelled", reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['start'])
def handle_start(message):
    help_menu(message)
    bot.send_message(message.chat.id, "Please enter your search details to get started!!!")
    send_stepper_msg(message.chat.id, age_group_text, age_groups.keys(), some_state_handler)


def some_state_handler(message):
    if isCancel(message.text):
        handle_cancel(message)
        return

    age_group = message.text
    if validate_input(age_group, age_groups.keys()):
        send_stepper_msg(message.chat.id, state_text, all_states, some_dist_handler, age_group)
    else:
        wrong_input_message(message.chat.id)
        send_stepper_msg(message.chat.id, age_group_text, age_groups.keys(), some_state_handler)


def some_dist_handler(message, age_group):
    if isCancel(message.text):
        handle_cancel(message)
        return
    state = message.text
    if validate_input(state, all_states):
        dists = get_dist_for_state(state)
        send_stepper_msg(message.chat.id, dist_text, dists, dose_handler, age_group, state, dists)

    else:
        wrong_input_message(message.chat.id)
        send_stepper_msg(message.chat.id, state_text, all_states, some_dist_handler, age_group)


def dose_handler(message, age_group, state, dists):
    if isCancel(message.text):
        handle_cancel(message)
        return
    dist = message.text

    if validate_input(dist, dists):
        send_stepper_msg(message.chat.id, dose_text, dose_types, final_handler, age_group, dist)
    else:
        wrong_input_message(message.chat.id)
        send_stepper_msg(message.chat.id, dist_text, dists, dose_handler, age_group, state, dists)


def final_handler(message, age_group, dist):
    if isCancel(message.text):
        handle_cancel(message)
        return

    dose_type = message.text
    if validate_input(dose_type, dose_types):
        print(message.text, age_group, dist)
        bot.send_message(message.chat.id, "Your input saved, checking for slots...",
                         reply_markup=types.ReplyKeyboardRemove())

        new_dist_handler(message.chat.id, age_group, dist, dose_type)
        bot.send_message(message.chat.id, "You can /subscribe for getting slot notification")
    else:
        wrong_input_message(message.chat.id)
        send_stepper_msg(message.chat.id, dose_text, dose_types, final_handler, age_group, dist)


def new_dist_handler(chat_id, age_group, dist, dose_type):
    age = age_groups.get(age_group)

    dist_id = validate_dist(dist)

    dose_type = dose_types.get(dose_type)

    print("Finally....", age, dose_type, dist_id)
    user = save_user_details(chat_id, dist, age, dose_type, False)
    # TODO => Remove with better logic
    user = populate_pref_fields()
    user['dist_id'] = [dist_id]
    user['age'] = age
    user['dose_type'] = dose_type

    get_available_slots(chat_id, user, get_date())


my_states = set()
all_states = list()


def init_states():
    for i in states:
        my_states.add(i['state_name'])
    global all_states
    all_states = sorted(list(my_states))


#####################################################

## Filter section starts

@bot.message_handler(commands=['filter'])
def handler_filter(message):
    send_stepper_msg(message.chat.id, age_group_text, age_groups.keys(), age_filter_handler)


def age_filter_handler(message):
    age = age_groups.get(message.text)
    print("AGe group: ", age)
    send_stepper_msg(message.chat.id, vaccine_text, vaccine_types.keys(), vaccine_filter_handler, age)


def vaccine_filter_handler(message, age):
    vaccine = vaccine_types.get(message.text)
    print('Vaccine: ', vaccine)
    send_stepper_msg(message.chat.id, dose_text, dose_types.keys(), dose_filter_handler, age, vaccine)


def dose_filter_handler(message, age, vaccine):
    dose = dose_types.get(message.text)
    print("Dose: ", dose)
    send_stepper_msg(message.chat.id, fee_type_text, fee_types.keys(), fee_type_filter_handler, age, vaccine, dose)


def fee_type_filter_handler(message, age, vaccine, dose):
    fee_type = fee_types.get(message.text)
    print("Fee_type: ", fee_type)
    print("User pref: ", age, vaccine, dose, fee_type)
    save_user_pref(message.chat.id, age, vaccine, dose, fee_type)
    bot.send_message(message.chat.id, "Your preferences have been saved", reply_markup=types.ReplyKeyboardRemove())


# Filter section ends

##########################################


# Threads to check and notify every minute for slots
def start_threads():
    users = get_all_user()

    check_date = date.today().strftime("%d-%m-%Y")
    threads = [threading.Thread(target=get_available_slots,
                                args=(chat_id, user, check_date, True))
               for chat_id, user in users.items() if user['notify']]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


@tl.job(interval=timedelta(seconds=120))
def check_every_minute():
    print('Starting new slot check at : ', datetime.now())
    start_threads()


@app.route('/' + my_secret, methods=['POST'])
def getMessage():
    json_string = flask.request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


if __name__ == "__main__":
    init_states()
    # migrate_db()
    tl.start()
    print("Slot notifier started.............!!!")
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
