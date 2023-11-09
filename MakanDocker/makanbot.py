#   ∧,,,∧
#  (• ⩊ •) ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊
# |￣U U￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣|
# |       WELCOME TO DIEU'S CODE!      |
# |           DON'T GET LOST           |
# |                                    |
# ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣

import logging
import boto3

### For Windows Client ###
# session = boto3.Session(profile_name='makaning-2')
# ddb = session.resource('dynamodb', region_name='ap-southeast-1')

### For Mac Client / AWS ###
ddb = boto3.resource('dynamodb', region_name='ap-southeast-1')
SessionTable = ddb.Table('SessionTable')

from GetRestaurantcopy import *
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
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
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

LOCATION, SELECTION_1, SELECTION_2, SELECTION_3, SELECTION_4, RANDOM = range(6)

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

next_reply = ("Here are more options!")

back_reply = ("Let's backtrack.")

surprise_reply = ("Don't worry, I'll look for something delicious for you! \n\n"
                          + "Send me your current location so that I can look for some makan spots nearby (ﾉ´ヮ`)ﾉ*: ･ﾟ")

back_to_food_categories_reply = ("Sure! Let's pick something else.")

# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼


# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
# Sends messages for /start command; bot will ask user what they feel like eating
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    print('User in /start')
    user = update.effective_user
    first_name = user.first_name
    start_reply = ("Hi " + first_name + "! " + "I'm the Makan-ing bot. I can help find some makan spots near you! \n\n"
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
    print(user.first_name + "'s user choice = " + user_food_choice)
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
        location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)], [KeyboardButton(text="Back to food categories 🥢")]]
        print('User clicked "IDK, surprise me!" in /start or selection_1')

        await update.message.reply_text (
            surprise_reply,
            reply_markup=ReplyKeyboardMarkup(
                location_keyboard, one_time_keyboard=True, input_field_placeholder="Send me your location! (Stalker vibes, jk)"
            )
        )
        return LOCATION

# IF user clicks on any food categories from selection_1, this flow will happen:
    else:
        user_food_choice_reply = ("Ooh, that sounds delicious! \n\n"
                       + "Send me your current location so that I can look for some " + lower_user_food_choice + " makan spots nearby 🍽️")
        if user_food_choice == 'Cafes':
            user_food_choice = 'Cafes & Coffee'
        SessionTable.put_item(
            Item =
            {
            'chatID': chatid,
            'food_choice' : user_food_choice
            }
            )
        location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)], [KeyboardButton(text="Back to food categories 🥢")]]
        print('User clicked any food category from selection_1 in /start or selection_1')

        await update.message.reply_text (
            user_food_choice_reply,
            reply_markup=ReplyKeyboardMarkup(
                location_keyboard, one_time_keyboard=True, input_field_placeholder="Send me your location! (Stalker vibes, jk)"
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
            location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True), [KeyboardButton(text="Back to food categories 🥢")]], [KeyboardButton(text="Back to food categories 🥢")]]
            print('User clicked "IDK, surprise me!" in /start or selection_2')
            SessionTable.put_item(
            Item =
            {
            'chatID': chatid,
            'food_choice' : 'IDK, surprise me!'
            }
            )

            await update.message.reply_text (
                surprise_reply,
                reply_markup=ReplyKeyboardMarkup(
                    location_keyboard, one_time_keyboard=True, input_field_placeholder="Send me your location! (Stalker vibes, jk)"
                )
            )
            return LOCATION

# IF user clicks on any food categories from selection_2, this flow will happen:
    else:
        user_food_choice_reply = ("Ooh, that sounds delicious! \n\n"
                       + "Send me your current location so that I can look for some " + lower_user_food_choice + " makan spots nearby 🍽️")
        location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)], [KeyboardButton(text="Back to food categories 🥢")]]
        print('User clicked any food category from selection_1 in /start or selection_2')
        SessionTable.put_item(
            Item =
            {
            'chatID': chatid,
            'food_choice' : user_food_choice
            }
            )

        await update.message.reply_text (
            user_food_choice_reply,
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
            location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)], [KeyboardButton(text="Back to food categories 🥢")]]
            print('User clicked "IDK, surprise me!" in /start or selection_2')
            SessionTable.put_item(
            Item =
            {
            'chatID': chatid,
            'food_choice' : 'IDK, surprise me!'
            }
            )

            await update.message.reply_text (
                surprise_reply,
                reply_markup=ReplyKeyboardMarkup(
                    location_keyboard, one_time_keyboard=True, input_field_placeholder="Send me your location! (Stalker vibes, jk)"
                )
            )
            return LOCATION

# IF user clicks on any food categories from selection_2, this flow will happen:
    else:
        user_food_choice_reply = ("Ooh, that sounds delicious! \n\n"
                       + "Send me your current location so that I can look for some " + lower_user_food_choice + " makan spots nearby 🍽️")
        location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)], [KeyboardButton(text="Back to food categories 🥢")]]
        print('User clicked any food category from selection_1 in /start or selection_2')
        SessionTable.put_item(
            Item =
            {
            'chatID': chatid,
            'food_choice' : user_food_choice
            }
            )

        await update.message.reply_text (
            user_food_choice_reply,
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
            location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)], [KeyboardButton(text="Back to food categories 🥢")]]
            print('User clicked "IDK, surprise me!" in /start or selection_3')
            SessionTable.put_item(
            Item =
            {
            'chatID': chatid,
            'food_choice' : 'IDK, surprise me!'
            }
            )

            await update.message.reply_text (
                surprise_reply,
                reply_markup=ReplyKeyboardMarkup(
                    location_keyboard, one_time_keyboard=True, input_field_placeholder="Send me your location! (Stalker vibes, jk)"
                )
            )
            return LOCATION

# IF user clicks on any food categories from selection_3, this flow will happen:
    else:
        user_food_choice_reply = ("Ooh, that sounds delicious! \n\n"
                       + "Send me your current location so that I can look for some " + lower_user_food_choice + " makan spots nearby 🍽️")
        location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)], [KeyboardButton(text="Back to food categories 🥢")]]
        print('User clicked any food category from selection_1 in /start or selection_1')
        SessionTable.put_item(
            Item =
            {
            'chatID': chatid,
            'food_choice' : user_food_choice
            }
            )

        await update.message.reply_text (
            user_food_choice_reply,
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

    if user_location_choice == "Back to food categories 🥢":
        print('User chose to go back to food categories')
        await update.message.reply_text(
        back_to_food_categories_reply,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_1, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
            )
        )
        return SELECTION_2
    
    else:
        print ('Searching for food')
        logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude)
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
        logger.info('User is at %s, user looking for %s', user_geohash, user_food_choice)
        food_options = find_food(user_geohash, user_food_choice, user_latitude, user_longitude)
        random_keyboard = [[KeyboardButton(text="More options please! 🥠")], [KeyboardButton(text="Back to food categories 🥢")]]

        await update.message.reply_text(
        food_options,
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

    if user_location_choice == "Back to food categories 🥢":
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
        user_food_choice = user_info['Item']['food_choice']
        print (user_food_choice)
        user_geohash = user_info['Item']['Geohash']
        user_latitude = float(user_info['Item']['Latitude'])
        user_longitude = float(user_info['Item']['Longitude'])
        logger.info('User is at %s, user looking for &f', user_geohash, user_food_choice)
        food_options = find_food(user_geohash, user_food_choice, user_latitude, user_longitude)
        random_keyboard = [[KeyboardButton(text="More options please! 🥠")], [KeyboardButton(text="Back to food categories 🥢")]]

        await update.message.reply_text(
        food_options,
            reply_markup=ReplyKeyboardMarkup(
                random_keyboard, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
            )
        )
        return RANDOM

# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼


# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
# When user sends /about, this message will trigger:
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("User is in /about")
    ### !!! REWORK THIS MESSAGE IN THE FUTURE. Make it more concise. 
    about_text = ("Hi, I'm the Makan-ing bot! 😄 I'm here to answer life's most difficult (and most frequently asked) question: <u><b>What should I eat today?</b></u> \n\n"
                  + "I can help: \n"
                  + "📍 <u>Find makan spots</u> based on your preferred cuisine and current location \n"
                  + "🍙 <u>Provide food recommendations</u> if you can't decide on what to eat \n\n"
                  + "Just type /start or select it from the menu bar, and I'll help you discover your next delicious meal! \n\n"

    )
    await update.message.reply_text(
        about_text, parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼


# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
# Cancels and ends the conversation when user uses /cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye, it was nice talking to you!", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼


# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
def main() -> None:
    """Run the bot."""
# Prod env token
    application = Application.builder().token("6243320723:AAE6Bip1fb8ltmhUbFyWXE7tdrxdZ9GgDBo").build()
        # TO DO:
        #     If there's an error in prod env being set up, wait 20s then try again
        #     Need to plan for a graceful failure

# # Test env token
    # application = Application.builder().token("6374507603:AAFmHROHbX3Y2vTtm_dFp6rBkl1iKy0CBVk").build()

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
            ]
        },
        # Will probably not need the /cancel fallback command
        # fallbacks=[CommandHandler("cancel", cancel)],
        fallbacks=[CommandHandler("start", start)]
    )

# Add commands to the telegram bot
    # application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("about", about))
    # application.add_handler(CommandHandler("feedback", feedback))

    application.add_handler(conv_handler)

# Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼
