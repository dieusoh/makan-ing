# WHY DID I DECIDE TO DO THIS
# THE FOLLY OF MAN
# I AM ICARUS AND I AM PLUMMETING
# WHY DID I THINK I WAS A STRONG, INDEPENDENT WOMEN. TAYLOR SWIFT U OVERSOLD THIS LIFE TO ME.

# DIEU'S TO DO:
    # Make sure it's not stuck on an infinite loop; integrate /cancel command.
    # Find a list of food categories from Burpple


#   ∧,,,∧
#  (• ⩊ •) ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊
# |￣U U￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣|
# |       WELCOME TO DIEU'S CODE!      |
# |           DON'T GET LOST           |
# |                                    |
# ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣

import logging

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

GENDER, SURPRISE_ME_REPLY, LOCATION, SELECTION_1, SELECTION_2, SELECTION_3 = range(6)

# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
# Define keyboards for food categories
reply_keyboard_1 = [
["IDK, surprise me!"],
["Chinese", "Malay", "Indian"],
["Cafes","Vegetarian", "Hawker food"],
["Next"],
]

reply_keyboard_2 = [
["IDK, surprise me!"], 
["Japanese", "Korean", "Thai"],
["Pasta", "Pizza", "Burger"],
["Back", "Next"],
]

reply_keyboard_3 = [
["IDK, surprise me!"], 
["Brunch", "Bubble tea", "Dessert"],
["Supper", "Hot pot", "Salads"],
["Back", "Next"],
]

next_reply = ("Here are more options!")

back_reply = ("Let's backtrack.")

surprise_reply = ("Don't worry, I'll look for something delicious for you! \n\n"
                          + "Send me your current location so that I look for some makan spots nearby (ﾉ´ヮ`)ﾉ*: ･ﾟ")

# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼


# ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
# Sends messages for /start command; bot will ask user what they feel like eating
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    print('User in /start')
    user = update.effective_user
    first_name = user.first_name
    start_reply = ("Hi " + first_name + "! " + "I'm the makan-ing bot. I can help you find some makan spots near you! \n\n"
                   + "What do you feel like eating today?")

# 1st set of food categories
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
    user_food_choice = update.message.text
    lower_user_food_choice = str.lower(user_food_choice)
    # user_location = update.message.location
    print(user.first_name + "'s user choice = " + user_food_choice)
    logger.info("User %s chose %s", user.first_name, user_food_choice)

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
        location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)]]
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
                       + "Send me your current location so that I look for some " + lower_user_food_choice + " makan spots nearby 🍽️")
        location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)]]
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
        return SELECTION_1

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
            location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)]]
            print('User clicked "IDK, surprise me!" in /start or selection_2')

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
                       + "Send me your current location so that I look for some " + lower_user_food_choice + " makan spots nearby 🍽️")
        location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)]]
        print('User clicked any food category from selection_1 in /start or selection_2')

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
    user_food_choice = update.message.text
    lower_user_food_choice = str.lower(user_food_choice)
    print(user.first_name + "'s user choice = " + user_food_choice)

# IF user clicks "Next" on selection_3, this flow will happen:
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

# IF user clicks on "Back" from selection_3, this flow will happen:
    elif user_food_choice == "Back":
        print('User clicked "Back" from selection_3')

        await update.message.reply_text (
            back_reply,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_2, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
            )
        )
        
        return SELECTION_3

# If user clicks on "IDK, surprise me!" in selection_3, this flow will happen:
    elif user_food_choice == "IDK, surprise me!":
            location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)]]
            print('User clicked "IDK, surprise me!" in /start or selection_3')

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
                       + "Send me your current location so that I look for some " + lower_user_food_choice + " makan spots nearby 🍽️")
        location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)]]
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
# Stores the location of the user when user clicks "Send current location" button
async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude)
    print("User's latitude = " + str(user_location.latitude))
    print("User's longitude = " + str(user_location.longitude))
    
    await update.message.reply_text(
        "Thanks! Searching for some yummy food near you now."
    )

# 𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼𓍊𓋼




# # ଘ(੭ˊ꒳​ˋ)੭✧ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ ⋆｡°✩ ⋆⁺｡˚⋆˙‧₊✩₊‧˙⋆˚｡⁺⋆ ✩°｡⋆ 
# async def surprise_me_reply(update: Update,context: ContextTypes.DEFAULT_TYPE) -> int:
#     print('User in surprise_me_reply')
#     user = update.message.from_user
#     surprise_me_reply = ("How about...")
#     location_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)]]

#     await update.message.reply_text (
#         surprise_me_reply,
#         reply_markup=ReplyKeyboardMarkup(
#             location_keyboard, one_time_keyboard=True, input_field_placeholder="Send me your location! (Stalker vibes, jk)"
#         )
#     )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Prod env token
    application = Application.builder().token("6243320723:AAE6Bip1fb8ltmhUbFyWXE7tdrxdZ9GgDBo").build()
        # TO DO:
            # If there's an error in prod env being set up, wait 20s then try again
            # Need to plan for a graceful failure

    # Test env token
    # application = Application.builder().token("6566523234:AAGGe36r6_Bqis9BdxHHnRua0kSaBEc_OhQ").build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
        states={
            LOCATION: [
                MessageHandler(filters.LOCATION, location),
            ],
            SELECTION_1: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, selection_1),
            ],
            SELECTION_2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, selection_2),
            ],
            SELECTION_3: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, selection_3),
            ]
            # SURPRISE_ME_REPLY: [
            #     MessageHandler(filters.TEXT & ~filters.COMMAND, surprise_me_reply),
            # ]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()