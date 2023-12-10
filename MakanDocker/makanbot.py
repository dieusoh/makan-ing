#   ∧,,,∧
#  (• ⩊ •) ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊
# |￣U U￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣|
# |       WELCOME TO DIEU'S CODE!      |
# |           DON'T GET LOST           |
# |                                    |
# ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣

import logging
import boto3
import requests
import traceback
import html
import json

### Comment this out if not Windows Client
# boto3.setup_default_session(profile_name='makaning-2')

ddb = boto3.resource('dynamodb', region_name='ap-southeast-1')
SessionTable = ddb.Table('SessionTable')
MRT_table = ddb.Table('MRT')
ssm = boto3.client('ssm')

#### This section sets whether the prod or staging API is selected
stage = 'prod'
# stage = 'test'

if stage == 'prod':
    bot_token = ssm.get_parameter(Name='/telegram/prod-token', WithDecryption=True)['Parameter']['Value']

else:
    bot_token = ssm.get_parameter(Name='/telegram/test-token', WithDecryption=True)['Parameter']['Value']

from GetRestaurant import *
from telegram import __version__ as TG_VER
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Message
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)

# Enables logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Sets higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

LOCATION, SELECTION_1, SELECTION_2, SELECTION_3, SELECTION_4, RANDOM, GET_MRT = range(7)

# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
# Define keyboards for food categories
reply_keyboard_1 = [
["IDK, surprise me!"],
["Burgers", "Cafes", "Chinese"],
["French","Halal", "Hawker Food"],
["Next"],
]

reply_keyboard_2 = [
["IDK, surprise me!"], 
["Indian", "Italian", "Japanese"],
["Korean", "Malay", "Mediterranean"],
["Back", "Next"],
]

reply_keyboard_3 = [
["IDK, surprise me!"], 
["Mexican", "Pasta", "Pizza"],
["Ramen", "Salads", "Spanish"],
["Back", "Next"],
]

reply_keyboard_4 = [
["IDK, surprise me!"], 
["Sushi", "Thai", "Turkish"],
["Vegan", "Vegetarian", "Western"],
["Back", "Next"],
]

random_keyboard = [[KeyboardButton(text="More options please! 🥠")], [KeyboardButton(text="🥢 Back to food categories")]]

back_to_food_categories_keyboard = [[KeyboardButton(text="🥢 Back to food categories")]]

next_reply = ("Here are more options!")

back_reply = ("Let's backtrack.")

surprise_reply = ("Don't worry, I'll look for something delicious for you! (ﾉ´ヮ`)ﾉ*: ･ﾟ\n\n"
                  + "Send me your <u>current location</u> or the <u>nearest MRT station</u> to where you are planning to go, and I can look for some makan spots nearby.")

back_to_food_categories_reply = ("Sure! Let's pick something else.")

mrt_reply = ("Type in the nearest MRT station to where you currently are, or where you're planning to go!")

mrt_error_reply = ("Oops, so sorry! I didn't quite understand that. Could you try typing it again or choosing another location?")

# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼


# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
# Sends messages for /start command; bot will ask user what they feel like eating
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    print('User in /start')
    user = update.effective_user
    first_name = user.first_name
    start_reply = ("Hi " + first_name + "! ✨ " + "I'm the Makan-ing bot. I can help find some makan spots near you or where you're planning to go! \n\n"
                   + "What do you feel like eating today?")

# 1st set of food categories; functionally the same as selection_1
    await update.message.reply_text (
        start_reply,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_1, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
        )  
    )

    return SELECTION_2

# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼


# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
async def selection_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('User in selection_2')
    user = update.message.from_user
    chatid = user.id
    user_food_choice = update.message.text
    lower_user_food_choice = str.lower(user_food_choice)
    logger.info("User chose %s", user_food_choice)

# IF user clicks on "Next" in selection_1, this flow will happen:
# 2nd set of food categories
    if user_food_choice == "Next":
        print('User clicked "Next" in /start or selection_1')
        
        await update.message.reply_text (
            next_reply,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_2, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
            )
        )
        return SELECTION_3

# IF user clicks on "IDK, surprise me!" in selection_1, this flow will happen:
    elif user_food_choice == "IDK, surprise me!":
        SessionTable.put_item(
            Item =
            {
            'chatID': chatid,
            'food_choice' : 'IDK, surprise me!'
            }
            )
        location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)], [KeyboardButton(text="🚆 Send the closest MRT station")], [KeyboardButton(text="🥢 Back to food categories")]]
        print('User clicked "IDK, surprise me!" in /start or selection_1')

        await update.message.reply_text (
            surprise_reply, parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(
                location_keyboard, one_time_keyboard=True, input_field_placeholder="Send me your location! (Stalker vibes, jk)"
            )
        )
        return LOCATION

# IF user clicks on any food categories from selection_1, this flow will happen:
    else:
        user_food_choice_reply = ("Ooh, that sounds delicious! (*• ڡ •*) I'll look for some " + lower_user_food_choice + " makan spots for you 🍽️ \n\n"
                                  + "Send me your <u>current location</u> or the <u>closest MRT station</u> to where you are planning to go.")
        if user_food_choice == 'Cafes':
            user_food_choice = 'Cafes & Coffee'
        SessionTable.put_item(
            Item =
            {
            'chatID': chatid,
            'food_choice' : user_food_choice
            }
            )
        location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)], [KeyboardButton(text="🚆 Send the closest MRT station")], [KeyboardButton(text="🥢 Back to food categories")]]
        print('User clicked any food category from selection_1 in /start or selection_1')

        await update.message.reply_text (
            user_food_choice_reply, parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True, input_field_placeholder="Send me your location! (Stalker vibes, jk)"
            )
        )
        return LOCATION
    

# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼


# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
async def selection_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('User in selection_3')
    user = update.message.from_user
    chatid = user.id
    user_food_choice = update.message.text
    lower_user_food_choice = str.lower(user_food_choice)
    print(user.first_name + "'s user choice = " + user_food_choice)

# IF user clicks on "Next" in selection_2, this flow will happen:
# 3rd set of food categories
    if user_food_choice == "Next":
        print('User clicked "Next" in selection_2')
        
        await update.message.reply_text (
            next_reply,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_3, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
            )
        )
        return SELECTION_4

# IF user clicks on "Back" in selection_2, this flow will happen:
    elif user_food_choice == "Back":
        print('User clicked "Back" in selection_2')

        await update.message.reply_text (
            back_reply,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_1, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
            )
        )
        
        return SELECTION_2

# If user clicks on "IDK, surprise me!" in selection_2, this flow will happen:
    elif user_food_choice == "IDK, surprise me!":
        SessionTable.put_item(
        Item =
        {
        'chatID': chatid,
        'food_choice' : 'IDK, surprise me!'
        }
        )
        location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)], [KeyboardButton(text="🚆 Send the closest MRT station")], [KeyboardButton(text="🥢 Back to food categories")]]
        print('User clicked "IDK, surprise me!" in /start or selection_2')

        await update.message.reply_text (
            surprise_reply, parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(
                location_keyboard, one_time_keyboard=True, input_field_placeholder="Send me your location! (Stalker vibes, jk)"
            )
        )
        return LOCATION

# IF user clicks on any food categories from selection_2, this flow will happen:
    else:
        user_food_choice_reply = ("Ooh, that sounds delicious! (*• ڡ •*) I'll look for some " + lower_user_food_choice + " makan spots for you 🍽️ \n\n"
                                  + "Send me your <u>current location</u> or the <u>closest MRT station</u> to where you are planning to go.")
        location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)], [KeyboardButton(text="🚆 Send the closest MRT station")], [KeyboardButton(text="🥢 Back to food categories")]]
        print('User clicked any food category from selection_1 in /start or selection_2')
        SessionTable.put_item(
            Item =
            {
            'chatID': chatid,
            'food_choice' : user_food_choice
            }
            )

        await update.message.reply_text (
            user_food_choice_reply, parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(
                location_keyboard, one_time_keyboard=True, input_field_placeholder="Send me your location! (Stalker vibes, jk)"
            )
        )
        return LOCATION


# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼


# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
async def selection_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('User in selection_4')
    user = update.message.from_user
    chatid = user.id
    user_food_choice = update.message.text
    lower_user_food_choice = str.lower(user_food_choice)
    print(user.first_name + "'s user choice = " + user_food_choice)

# IF user clicks on "Next" in selection_4, this flow will happen:
# 4th set of food categories
    if user_food_choice == "Next":
        print('User clicked "Next" in selection_4')
        
        await update.message.reply_text (
            next_reply,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_4, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
            )
        )
        return SELECTION_1

# IF user clicks on "Back" in selection_3, this flow will happen:
    elif user_food_choice == "Back":
        print('User clicked "Back" in selection_3')

        await update.message.reply_text (
            back_reply,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_2, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
            )
        )
        
        return SELECTION_3

# If user clicks on "IDK, surprise me!" in selection_2, this flow will happen:
    elif user_food_choice == "IDK, surprise me!":
            location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)], [KeyboardButton(text="🚆 Send the closest MRT station")], [KeyboardButton(text="🥢 Back to food categories")]]
            print('User clicked "IDK, surprise me!" in /start or selection_2')
            SessionTable.put_item(
            Item =
            {
            'chatID': chatid,
            'food_choice' : 'IDK, surprise me!'
            }
            )

            await update.message.reply_text (
                surprise_reply, parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardMarkup(
                    location_keyboard, one_time_keyboard=True, input_field_placeholder="Send me your location! (Stalker vibes, jk)"
                )
            )
            return LOCATION

# IF user clicks on any food categories from selection_2, this flow will happen:
    else:
        user_food_choice_reply = ("Ooh, that sounds delicious! (*• ڡ •*) I'll look for some " + lower_user_food_choice + " makan spots for you 🍽️ \n\n"
                                  + "Send me your <u>current location</u> or the <u>closest MRT station</u> to where you are planning to go.")
        location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)], [KeyboardButton(text="🚆 Send the closest MRT station")], [KeyboardButton(text="🥢 Back to food categories")]]
        print('User clicked any food category from selection_1 in /start or selection_2')
        SessionTable.put_item(
            Item =
            {
            'chatID': chatid,
            'food_choice' : user_food_choice
            }
            )

        await update.message.reply_text (
            user_food_choice_reply, parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(
                location_keyboard, one_time_keyboard=True, input_field_placeholder="Send me your location! (Stalker vibes, jk)"
            )
        )
        return LOCATION


# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼



# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
async def selection_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('User in selection 1')
    user = update.message.from_user
    chatid = user.id
    user_food_choice = update.message.text
    lower_user_food_choice = str.lower(user_food_choice)
    print(user.first_name + "'s user choice = " + user_food_choice)

# IF user clicks "Next" on selection_4, this flow will happen:
# Return to 1st set of food categories
    if user_food_choice == "Next":
        print('User clicked "Next" from selection_3')

        await update.message.reply_text (
            next_reply,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_1, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
            )
        )
        return SELECTION_2

# IF user clicks on "Back" from selection_4, this flow will happen:
    elif user_food_choice == "Back":
        print('User clicked "Back" from selection_3')

        await update.message.reply_text (
            back_reply,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_3, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
            )
        )
        
        return SELECTION_4

# If user clicks on "IDK, surprise me!" in selection_3, this flow will happen:
    elif user_food_choice == "IDK, surprise me!":
            location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)], [KeyboardButton(text="🚆 Send the closest MRT station")], [KeyboardButton(text="🥢 Back to food categories")]]
            print('User clicked "IDK, surprise me!" in /start or selection_3')
            SessionTable.put_item(
            Item =
            {
            'chatID': chatid,
            'food_choice' : 'IDK, surprise me!'
            }
            )

            await update.message.reply_text (
                surprise_reply, parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardMarkup(
                    location_keyboard, one_time_keyboard=True, input_field_placeholder="Send me your location! (Stalker vibes, jk)"
                )
            )
            return LOCATION

# IF user clicks on any food categories from selection_3, this flow will happen:
    else:
        user_food_choice_reply = ("Ooh, that sounds delicious! (*• ڡ •*) I'll look for some " + lower_user_food_choice + " makan spots for you 🍽️ \n\n"
                                  + "Send me your <u>current location</u> or the <u>closest MRT station</u> to where you are planning to go.")
        location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)], [KeyboardButton(text="🚆 Send the closest MRT station")], [KeyboardButton(text="🥢 Back to food categories")]]
        print('User clicked any food category from selection_1 in /start or selection_1')
        SessionTable.put_item(
            Item =
            {
            'chatID': chatid,
            'food_choice' : user_food_choice
            }
            )

        await update.message.reply_text (
            user_food_choice_reply, parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(
                location_keyboard, one_time_keyboard=True, input_field_placeholder="Send me your location! (Stalker vibes, jk)"
            )
        )
        return LOCATION
        

# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼


# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
# Stores the location of the user when user clicks "Send current location" button
async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print ('In Location')
    print ('------------')
    user = update.message.from_user
    user_location = update.message.location
    user_location_choice = update.message.text
    chatid = user.id

    if user_location_choice == "🥢 Back to food categories":
        print('User chose to go back to food categories')
        await update.message.reply_text(
        back_to_food_categories_reply,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_1, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
            )
        )
        return SELECTION_2
    
    elif user_location_choice == "🚆 Send the closest MRT station":
        print('User is sending the closest MRT station')
        await update.message.reply_text(
        mrt_reply,
            )
        return GET_MRT


    else:
        print ('Searching for food')
        logger.info("Location of %s: %f / %f", chatid, user_location.latitude, user_location.longitude)
        message = 'Looking for some delicious makan spots now 🍣\n\nHow about...'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(chatid) + '&parse_mode=Markdown&text=' + message
        requests.get(send_text)

        user_latitude = (user_location.latitude)
        user_longitude = (user_location.longitude)
        user_geohash = get_geohash(user_latitude, user_longitude)
        user_food_choice = ''
        user_food_choice = SessionTable.get_item(
            Key = {
                'chatID':chatid
            }
        )
        user_food_choice = user_food_choice['Item']['food_choice']
        SessionTable.put_item(
            Item =
            {
            'chatID': chatid,
            'food_choice' : user_food_choice,
            'Latitude':str(user_latitude),
            'Longitude':str(user_longitude),
            'Geohash':user_geohash
            }
            )
        logger.info('User session %s is at %s, user looking for %s', chatid,user_geohash, user_food_choice)
        restaurant_options = find_food(user_geohash, user_food_choice, user_latitude, user_longitude)
        number_of_restaurants = restaurant_options[1]
        print (number_of_restaurants)
        food_options = restaurant_options[0]
        if number_of_restaurants < 5 and number_of_restaurants > 0:
            message = "Sorry, these were all the makan places that we could find near you that fit the category, please try a different category for more options"
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(chatid) + '&parse_mode=Markdown&text=' + message
            requests.get(send_text)
                
            await update.message.reply_text(
            food_options, parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardMarkup(
                    back_to_food_categories_keyboard, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
                )
            )
            return RANDOM
        
        else:
            await update.message.reply_text(
                food_options, parse_mode=ParseMode.HTML,
                    reply_markup=ReplyKeyboardMarkup(
                        random_keyboard, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
                    )
                )
            return RANDOM



# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼


# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
async def random(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print ('In random')
    user = update.message.from_user
    user_location = update.message.location
    user_location_choice = update.message.text
    chatid = user.id

    if user_location_choice == "🥢 Back to food categories":
        print('User chose to go back to food categories')

        await update.message.reply_text(
        back_to_food_categories_reply,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_1, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
            )
        )
        return SELECTION_2

    else:
        print ('Searching for food2')
        user_info = ''
        user_info = SessionTable.get_item(
            Key = {
                'chatID':chatid
            }
        )
        message = 'Looking for some delicious makan spots now 🍣\n\nHow about...'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(chatid) + '&parse_mode=Markdown&text=' + message
        requests.get(send_text)
        user_food_choice = user_info['Item']['food_choice']
        print (user_food_choice)
        user_geohash = user_info['Item']['Geohash']
        user_latitude = float(user_info['Item']['Latitude'])
        user_longitude = float(user_info['Item']['Longitude'])
        restaurant_options = find_food(user_geohash, user_food_choice, user_latitude, user_longitude)
        number_of_restaurants = restaurant_options[1]
        food_options = restaurant_options[0]
        random_keyboard = [[KeyboardButton(text="More options please! 🥠")], [KeyboardButton(text="🥢 Back to food categories")]]

        if number_of_restaurants < 5 and number_of_restaurants > 0:
            message = "Sorry, these were all the makan places that we could find near you that fit the category, please try a different category for more options"
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(chatid) + '&parse_mode=Markdown&text=' + message
            requests.get(send_text)
                
            await update.message.reply_text(
            food_options, parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardMarkup(
                    back_to_food_categories_keyboard, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
                )
            )
            return RANDOM
        
        else:
            await update.message.reply_text(
                food_options, parse_mode=ParseMode.HTML,
                    reply_markup=ReplyKeyboardMarkup(
                        random_keyboard, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
                    )
                )
            return RANDOM

# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼

# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
async def get_mrt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    print("User is in get_mrt")
    chatid = user.id
    user_mrt_choice = update.message.text
    user_mrt_choice = user_mrt_choice.lower()
    random_keyboard = [[KeyboardButton(text="More options please! 🥠")], [KeyboardButton(text="🥢 Back to food categories")]]
    # Get geohash of MRT
    try: 
        mrt_info = MRT_table.query(
            KeyConditionExpression = Key('MRT-name').eq(user_mrt_choice)
        )
        user_geohash = mrt_info['Items'][0]['Geohash']
        user_latitude = float(mrt_info['Items'][0]['Latitude'])
        user_longitude = float(mrt_info['Items'][0]['Longitude'])
        message = 'Looking for some delicious makan spots now 🍣\n\nHow about...'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(chatid) + '&parse_mode=Markdown&text=' + message
        requests.get(send_text)
        user_food_choice = ''
        user_food_choice = SessionTable.get_item(
            Key = {
                'chatID':chatid
            }
        )
        user_food_choice = ''
        user_food_choice = SessionTable.get_item(
            Key = {
                'chatID':chatid
            }
        )
        user_food_choice = user_food_choice['Item']['food_choice']
        SessionTable.put_item(
            Item =
            {
            'chatID': chatid,
            'food_choice' : user_food_choice,
            'Latitude':str(user_latitude),
            'Longitude':str(user_longitude),
            'Geohash':user_geohash
            }
            )
        logger.info('User session %s is at %s, user looking for %s', chatid,user_geohash, user_food_choice)
        restaurant_options = find_food(user_geohash, user_food_choice, user_latitude, user_longitude)
        number_of_restaurants = restaurant_options[1]
        food_options = restaurant_options[0]

        if number_of_restaurants < 5 and number_of_restaurants > 0:
            message = "Sorry, these were all the makan places that we could find near you that fit the category, please try a different category for more options"
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(chatid) + '&parse_mode=Markdown&text=' + message
            requests.get(send_text)
                
            await update.message.reply_text(
            food_options, parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardMarkup(
                    back_to_food_categories_keyboard, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
                )
            )
            return RANDOM
        
        else:
            await update.message.reply_text(
                food_options, parse_mode=ParseMode.HTML,
                    reply_markup=ReplyKeyboardMarkup(
                        random_keyboard, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
                    )
                )
            return RANDOM
    
    except:
        # add some error handling logic here when they input an mrt station that is wrong
        print ('Error in get_mrt')
        await update.message.reply_text(
        mrt_error_reply, parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(
                random_keyboard, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
            )
        )
        return GET_MRT  



# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
# When user sends /about, this message will trigger:
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("User is in /about")
    ### !!! REWORK THIS MESSAGE IN THE FUTURE. Make it more concise. 
    about_text = ("Hi, I'm the Makan-ing bot! 😄 I'm here to answer life's most difficult (and most frequently asked) question: <u><b>What should I eat today?</b></u> \n\n"
                  + "I can help: \n"
                  + "📍 <u>Find makan spots</u> based on your preferred cuisine and location \n"
                  + "🍙 <u>Provide food recommendations</u> if you can't decide on what to eat \n\n"
                  + "Just type /start or select it from the menu bar, and I'll help you discover your next delicious meal! \n\n"

    )
    await update.message.reply_text(
        about_text, parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼

# # ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
# # When user sends /feedback, this message will trigger:
# async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     print("User is in /feedback")
#     ### !!! REWORK THIS MESSAGE IN THE FUTURE. Make it more concise. 
#     feedback_text = ("Makan-ing is built for the everyday Singaporean! We are always looking for ways to improve our app and make it better. \n\n"
#                      + "You can email us at hello@makaning.com if you:\n"
#                      + "- Have any feedback (good or bad)\n"
#                      + "- Have a makan spots you would like to recommend\n"
#                      + "- Are interested in any partnerships or collaboration\n"
#                      + "- Or just want to say hi!\n\n"
#                      + "We read every email! ヽ(*⌒▽⌒*)ﾉ"
#     )

#     await update.message.reply_text(
#         feedback_text, parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove()
#     )
    
#     return ConversationHandler.END

# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼

# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
# When user sends /feedback, this message will trigger:
async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("User is in /feedback")
    ### !!! REWORK THIS MESSAGE IN THE FUTURE. Make it more concise. 
    feedback_text = ("Makan-ing is built for the everyday Singaporean! We are always looking for ways to improve our app and make it better. \n\n"
                     + "You can email us at hello@makaning.com if you:\n"
                     + "- Have any feedback (good or bad)\n"
                     + "- Have a makan spot you would like to recommend\n"
                     + "- Are interested in any partnerships or collaboration\n"
                     + "- Just want to say hi!\n\n"
                     + "We read every email! ╰(*´︶`*)╯♡"
    )

    await update.message.reply_text(
        feedback_text, parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove()
    )
    
    return ConversationHandler.END

# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:    
    user = update.message.from_user
    chatid = user.id
    
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(
        chat_id=chatid, text=message, parse_mode=ParseMode.HTML
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:    
    user = update.message.from_user
    chatid = user.id
    
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "Sorry, we encountered an error. Please enter '/start' to try using the bot again"
    )

    # Finally, send the message
    await context.bot.send_message(
        chat_id=chatid, text=message, parse_mode=ParseMode.HTML
    )

    return ConversationHandler.END

# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
# Cancels and ends the conversation when user uses /cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    chatid = user.id
    logger.info("ChatID %s canceled the conversation.", chatid)
    await update.message.reply_text(
        "Bye, it was nice talking to you!", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼


# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
def main() -> None:
    """Run the bot."""
    application = Application.builder().token(bot_token).build()

# Add conversation handler with the states
    conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
        states={
            LOCATION: [
                MessageHandler(filters.LOCATION & ~filters.COMMAND, location),
                MessageHandler(filters.TEXT & ~filters.COMMAND, location),
            ],
            SELECTION_1: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, selection_1),
            ],
            SELECTION_2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, selection_2),
            ],
            SELECTION_3: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, selection_3),
            ],
            SELECTION_4: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, selection_4),
            ],
            RANDOM: [
                MessageHandler(filters.LOCATION & ~filters.COMMAND, random),
                MessageHandler(filters.TEXT & ~filters.COMMAND, random),
            ],
            GET_MRT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_mrt),
            ]
        },
        # Will probably not need the /cancel fallback command
        fallbacks=[CommandHandler("start", start)]
    )

# Add commands to the telegram bot
    # application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("feedback", feedback))
    application.add_error_handler(error_handler)
    application.add_handler(conv_handler)

# Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼
