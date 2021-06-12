import os
import threading
from datetime import date, datetime, timedelta

import flask
import telebot
from flask import Flask
from timeloop import Timeloop
from states import states
from telebot import types

from utils import *
from users import *
from format_util import *

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


@bot.message_handler(commands=['/check'])
def start(message):
    sent_msg = bot.send_message(message.chat.id, "Enter your age, district, dose number (1 or 2) separated by comma")
    bot.register_next_step_handler(sent_msg, dist_handler, False)


@bot.message_handler(commands=['update'])
def update_user_config(message):
    sent_msg = bot.send_message(message.chat.id, "Enter your age, district, dose number (1 or 2) separated by comma")
    bot.register_next_step_handler(sent_msg, dist_handler, True)


@bot.message_handler(commands=['delete'])
def delete_user_config(message):
    sent_msg = bot.send_message(message.chat.id, "Are you sure you want to delete your data : (yes/no)")
    bot.register_next_step_handler(sent_msg, delete_user_handle)


@bot.message_handler(commands=['add_district'])
def add_dist_input(message):
    sent_msg = bot.send_message(message.chat.id, "Enter district name")
    bot.register_next_step_handler(sent_msg, add_to_user_dists)


@bot.message_handler(commands=['remove_district'])
def add_dist_input(message):
    sent_msg = bot.send_message(message.chat.id, "Enter district name")
    bot.register_next_step_handler(sent_msg, remove_from_user_dists)


@bot.message_handler(commands=['my_details'])
def get_user_saved_details(message):
    user = get_user(message.chat.id)
    if user is not None:
        subs = {v: k for k, v in cons.district_map.items()}
        user['dist_id'] = [subs.get(item) for item in user['dist_id']]
        bot.send_message(message.chat.id, format_user_details(user), parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "Your preference not saved, use /start to save")


@bot.message_handler(commands=['slots'])
def get_slots(message):
    date_c = date.today().strftime("%d-%m-%Y")
    print('Getting slots.........')
    user = get_user(message.chat.id)
    if user is not None:
        get_available_slots(message.chat.id, user['dist_id'], user['dose_type'], user['age'], date_c)
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


def add_to_user_dists(message):
    user = get_user(message.chat.id)
    if user is not None:
        new_dist_id = validate_dist(message.text)
        if not new_dist_id:
            print("Invalid district entered")
            bot.send_message(message.chat.id, "Invalid district name")
            return

        if len(user['dist_id']) >= 2:
            bot.send_message(message.chat.id, "You can add only 2 district max")
            return

        if new_dist_id not in user['dist_id']:
            user['dist_id'].append(new_dist_id)
            save_user(message.chat.id, user)
            bot.send_message(message.chat.id, "Saved to your list")
        else:
            bot.send_message(message.chat.id, "District already saved in your list")
    else:
        bot.send_message(message.chat.id, "User not found, please register using /start")


def remove_from_user_dists(message):
    user = get_user(message.chat.id)
    if user is not None:
        new_dist_id = validate_dist(message.text)
        if not new_dist_id:
            print("Invalid district entered")
            bot.send_message(message.chat.id, "Invalid district name")
            return

        if new_dist_id not in user['dist_id']:
            bot.send_message(message.chat.id, "District not in your saved list")
        else:
            user['dist_id'].remove(new_dist_id)
            save_user(message.chat.id, user)
            bot.send_message(message.chat.id, "Removed from your list")
    else:
        bot.send_message(message.chat.id, "User not found, please register using /start")


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
        save_user_details(message.chat.id, dist, age, dose_type, isUpdate)
        if not isUpdate:
            get_available_slots(message.chat.id, [dist_id], dose_type, age, check_date)
        else:
            bot.send_message(message.chat.id, "Your preference have been updated - check /my_details")


def get_available_slots(chat_id, dist_id, dose_type, age, check_date):
    data = get_next7days_by_district(dist_id, check_date)
    resp = None
    if data is not None:
        resp = get_availability_from_data(data, dose_type, age)
    # print(resp)
    if resp is not None and len(resp) > 0:
        print('Slots found for ', chat_id, ' for total ', len(resp), ' days')
        bot.send_message(chat_id, text=format_message(resp, dose_type), parse_mode="HTML")
    else:
        print('No slots found for ', chat_id, "on next 7 days of ", check_date)
        bot.send_message(chat_id, "No slots found")


def get_available_slots_for_thread(chat_id, dist_id, dose_type, age, check_date):
    print('Checking availability for user ', chat_id)
    data = get_next7days_by_district(dist_id, check_date)
    resp = None
    if data is not None:
        resp = get_availability_from_data(data, dose_type, age)
    # print(resp)
    if resp is not None and len(resp) > 0:
        print('Slots found for ', chat_id)
        bot.send_message(chat_id, format_message(resp, dose_type), parse_mode="HTML")
    else:
        print('No slots found for ', chat_id, "on next 7 days of ", check_date)
        # bot.send_message(id, "No slots found")

#################################


def create_reply_keyboard(data):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = []
    for key in data:
        buttons.append(types.KeyboardButton(text=key))
    keyboard.add(*buttons)
    return keyboard


def validate_input(user_input, expected):
    if user_input not in expected:
        return False
    else:
        return True


def wrong_input_message(chat_id):
    bot.send_message(chat_id, 'Wrong input..., Try again or /cancel to abort')


def get_dist_for_state(state):
    dists = []
    for i in states:
        if i['state_name'] == state:
            dists.append(i['district_name'])
    return sorted(dists)


def send_stepper_msg(chat_id, text, keyboard, state_handler, *arg):
    sent_msg = bot.send_message(chat_id, text, reply_markup=create_reply_keyboard(keyboard))
    bot.register_next_step_handler(sent_msg, state_handler, *arg)


def isCancel(msg):
    if msg == '/cancel':
        return True
    else:
        return False


@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    bot.send_message(message.chat.id, "Operation cancelled", reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['register'])
def handle_start(message):
    send_stepper_msg(message.chat.id, age_group_text, age_groups, some_state_handler)


def some_state_handler(message):
    if isCancel(message.text):
        handle_cancel(message)
        return

    age_group = message.text
    if validate_input(age_group, age_groups):
        send_stepper_msg(message.chat.id, state_text, all_states, some_dist_handler, age_group)
    else:
        wrong_input_message(message.chat.id)
        send_stepper_msg(message.chat.id, age_group_text, age_groups, some_state_handler)


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
    if age_group == age_groups[0]:
        age = 18
    else:
        age = 45

    dist_id = validate_dist(dist)

    if dose_type == dose_types[0]:
        dose_type = 1
    else:
        dose_type = 2

    print("Finally....", age, dose_type, dist_id)
    save_user_details(chat_id, dist, age, dose_type, False)
    get_available_slots(chat_id, [dist_id], dose_type, age, get_date())


my_states = set()
all_states = list()
age_groups = ['18-44', '45+']
dose_types = ['Dose 1', 'Dose 2']
age_group_text = "Select your age group"
state_text = "Select your state"
dist_text = "Select your district"
dose_text = "Select your dose type"


def init_states():
    for i in states:
        my_states.add(i['state_name'])
    global all_states
    all_states = sorted(list(my_states))


#####################################################


# Threads to check and notify every minute for slots
def start_threads():
    users = get_all_user()

    check_date = date.today().strftime("%d-%m-%Y")
    threads = [threading.Thread(target=get_available_slots_for_thread,
                                args=(chat_id, user['dist_id'], user['dose_type'], user['age'], check_date,))
               for chat_id, user in users.items() if user['notify']]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


@tl.job(interval=timedelta(seconds=60))
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
    tl.start()
    print("Slot notifier started.............!!!")
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
