import os,json
import telebot
import threading
import constants as cons
from timeloop import Timeloop
from json import JSONDecodeError
from utils import get_next7days_by_district, get_availability_from_data
from datetime import date, datetime, timedelta
from flask import Flask
import flask


my_secret = os.environ['API_KEY']
app = Flask(__name__)
bot = telebot.TeleBot(my_secret)
# bot.remove_webhook()
bot.set_webhook(url=cons.HOST_URL + my_secret)

@bot.message_handler(commands=['greet'])
def greet(message):
  bot.send_message(my_id, "Hey! Hows it going?")

@bot.message_handler(commands=['start'])
def start(message):
  sent_msg = bot.send_message(message.chat.id, "Enter your age, district, dose number(1 or 2) separated by space")
  bot.register_next_step_handler(sent_msg, dist_handler)

@bot.message_handler(commands=['add_district'])
def add_dist_input(message):
  sent_msg = bot.send_message(message.chat.id, "Enter district name")
  bot.register_next_step_handler(sent_msg, add_dist_to_user_list)

@bot.message_handler(commands=['my_details'])
def get_user_saved_details(message):
  user = get_user(message.chat.id)
  subs = {v:k for k, v in cons.district_map.items()}
  user['dist_id'] = [subs.get(item) for item in user['dist_id']]
  bot.send_message(message.chat.id, format_user_details(user), parse_mode="HTML")

def add_dist_to_user_list(message):
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


def dist_handler(message):
  user_details = message.text.split()
  if len(user_details) < 3:
    sent_msg = bot.send_message(message.chat.id, "You have entered wrong value, please enter your age, district, dose number(1 or 2) and date(dd-mm-yyyy)")
    bot.register_next_step_handler(sent_msg, dist_handler)
  else:
    age = int(user_details[0])
    dist = user_details[1]
    dose_type = int(user_details[2])
    check_date = date.today().strftime("%d-%m-%Y")
    if len(user_details) == 4:
      check_date = user_details[3]
    try:
      dist_id = cons.district_map[dist.lower()]
    except:
      bot.send_message(message.chat.id, "Invalid district")
      return

    # save user
    save_user_details(message.chat.id, dist, age, dose_type)
    get_available_slots(message.chat.id, [dist_id], dose_type, age, check_date)


@bot.message_handler(commands=['slots'])
def get_slots(message):
  date_c = date.today().strftime("%d-%m-%Y")
  print('Getting slots.........')
  user = get_user(message.chat.id)
  if user is not None:
    get_available_slots(message.chat.id, user['dist_id'], user['dose_type'], user['age'], date_c)
  else:
    bot.send_message(message.chat.id, "User not found, please register using /start")

@bot.message_handler(commands=['thread'])
def get_thread(message):
  print(threading.active_count())
  for thread in threading.enumerate():
    print(thread.name)

            
@bot.message_handler(commands=['subscribe'])
def start_user_thread(message):
  user = get_user(message.chat.id)
  if user is not None and not user['notify']:
    user['notify'] = True
    save_user(message.chat.id, user)
  else:
    bot.send_message(message.chat.id, "You already have an active subsctiption")
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


def save_user_details(id, dist, age, dose_type):
  data = get_user(id)
  if data is None:
    user_details = {}
    user_details['dist_id'] = [cons.district_map[dist.lower()]]
    user_details['age'] = int(age)
    user_details['dose_type'] = int(dose_type)
    
    print('Saving user details....')
    save_user(id, user_details)

  else:
    print('User details found in db')

def save_user(id, user_details):
  with open('users.json', 'r+') as out:
    try:
      data = json.loads(out.read())
    except JSONDecodeError:
      data = {}

    # print("all users: ", data)
    data[str(id)] = user_details
    out.seek(0)
    out.truncate()
    # print('saving: ', data)
    out.write(json.dumps(data))
  print("User details saved....")

def get_user(id):
  with open('users.json', 'r') as f:
    try:
      data = json.loads(f.read())
    except JSONDecodeError:
      data = {}

    if str(id) in data:
      print('User found...')
      return data[str(id)]
    else:
      print('User not found...')
      return None

def get_available_slots(id, dist_id, dose_type, age, check_date):
  data = get_next7days_by_district(dist_id, check_date)
  resp = None
  if data is not None:
    resp = get_availability_from_data(data, dose_type, age)
  # print(resp)
  if resp is not None and len(resp)>0:
    print('Slots found for ', id)
    bot.send_message(id, text=format_message(resp, dose_type), parse_mode="HTML")
  else:
    print('No slots found for ', id, "on next 7 days of ",check_date)
    bot.send_message(id, "No slots found")


def get_available_slots_for_thread(id, dist_id, dose_type, age, check_date):
  print('Checking availabilty for user ', id)
  data = get_next7days_by_district(dist_id, check_date)
  resp = None
  if data is not None:
    resp = get_availability_from_data(data, dose_type, age)
  # print(resp)
  if resp is not None and len(resp)>0:
    print('Slots found for ', id)
    bot.send_message(id, format_message(resp, dose_type), parse_mode= "HTML")
  else:
    print('No slots found for ', id, "on next 7 days of ",check_date)
    # bot.send_message(id, "No slots found")


def format_message(resp, dose_type):
  message = "\n<strong>Slots Found</strong>\n"
  for key_date,centers in resp.items():
    message += "\n<b><ins>" + key_date + "</ins></b>\n"
    for center in centers:
      message += "\n<pre><code>"
      message += center['center_name'] + ", " + center['district'] + " -- Dose " + str(dose_type) + " : " + str(center[cons.doses[dose_type]])
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

# Threads to check and notify every minute for slots
def start_threads():
  with open('users.json', 'r') as f:
    try:
      users = json.loads(f.read())
    except:
      users = {}

  check_date = date.today().strftime("%d-%m-%Y")
  threads = [threading.Thread(target=get_available_slots_for_thread, args=(id,user['dist_id'], user['dose_type'], user['age'], check_date,)) for id,user in users.items() if user['notify']]
  for thread in threads:
      thread.start()
  for thread in threads:
      thread.join()

tl = Timeloop()

@tl.job(interval=timedelta(seconds=60))
def check_every_minute():
  print('Starting new slot check at : ', datetime.now())
  start_threads()


# print('starting Timeloop...')
# tl.start()
# print("Slot notifier started.............!!!")
# bot.polling()

@app.route('/' + my_secret, methods=['POST'])
def getMessage():
    json_string = flask.request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


# @app.route("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url='https://LiveVioletredFlashmemory.vsheel.repl.co/' + my_secret)
#     return "!", 200


if __name__ == "__main__":
  tl.start()
  print("Slot notifier started.............!!!")
  app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
