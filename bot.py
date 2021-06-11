import os
import threading
from datetime import date, datetime, timedelta

import flask
import telebot
from flask import Flask
from timeloop import Timeloop

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


@bot.message_handler(commands=['start'])
def start(message):
    sent_msg = bot.send_message(message.chat.id, "Enter your age, district, dose number(1 or 2) separated by space")
    bot.register_next_step_handler(sent_msg, dist_handler)


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
    subs = {v: k for k, v in cons.district_map.items()}
    user['dist_id'] = [subs.get(item) for item in user['dist_id']]
    bot.send_message(message.chat.id, format_user_details(user), parse_mode="HTML")


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
    if user is not None and not user['notify']:
        user['notify'] = True
        save_user(message.chat.id, user)
    else:
        bot.send_message(message.chat.id, "You already have an active subscription")
        return

    print('Subscription success for ', message.chat.id)
    bot.send_message(message.chat.id, "Subscription successful, you will be notified for slots when available")


@bot.message_handler(commands=['unsubscribe'])
def pause_notifier(message):
    user = get_user(message.chat.id)
    if user is not None and user['notify']:
        user['notify'] = False
        save_user(message.chat.id, user)
        print('Subscription removed for user ', message.chat.id)
        bot.send_message(message.chat.id, 'Subscription notification removed')
    else:
        bot.send_message(message.chat.id, "You don't have any active Subscription")


def add_to_user_dists(message):
    user = get_user(message.chat.id)
    if user is not None:
        try:
            new_dist_id = cons.district_map[message.text.lower()]
        except:
            print("Invalid district entered")
            bot.send_message(message.chat.id, "Invalid district name")
            return

        if new_dist_id not in user['dist_id']:
            user['dist_id'].append(new_dist_id)
            save_user(message.chat.id, user)
            bot.send_message(message.chat.id, "Saved to your list")
        else:
            bot.send_message(message.chat.id, "District already saved in your list")


def remove_from_user_dists(message):
    user = get_user(message.chat.id)
    if user is not None:
        try:
            new_dist_id = cons.district_map[message.text.lower()]
        except:
            print("Invalid district entered")
            bot.send_message(message.chat.id, "Invalid district name")
            return

        if new_dist_id not in user['dist_id']:
            bot.send_message(message.chat.id, "District not in your saved list")
        else:
            user['dist_id'].remove(new_dist_id)
            save_user(message.chat.id, user)
            bot.send_message(message.chat.id, "Removed from your list")


def dist_handler(message):
    user_details = message.text.split()
    if len(user_details) < 3:
        bot.send_message(message.chat.id, "Invalid Entry, /start again")
    else:
        age, dist, dose_type, check_date = populate_user_details(user_details)
        dist_id = validate_dist(dist)
        if not dist_id:
            bot.send_message(message.chat.id, "Invalid district")
            return

        # save user
        save_user_details(message.chat.id, dist, age, dose_type)
        get_available_slots(message.chat.id, [dist_id], dose_type, age, check_date)


def get_available_slots(chat_id, dist_id, dose_type, age, check_date):
    data = get_next7days_by_district(dist_id, check_date)
    resp = None
    if data is not None:
        resp = get_availability_from_data(data, dose_type, age)
    # print(resp)
    if resp is not None and len(resp) > 0:
        print('Slots found for ', chat_id)
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


# Threads to check and notify every minute for slots
def start_threads():
    with open('users.json', 'r') as f:
        try:
            users = json.loads(f.read())
        except:
            users = {}

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
    tl.start()
    print("Slot notifier started.............!!!")
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
