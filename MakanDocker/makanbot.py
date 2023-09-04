# WHY DID I DECIDE TO DO THIS
# THE FOLLY OF MAN
# I AM ICARUS AND I AM PLUMMETING
# WHY DID I THINK I WAS A STRONG, INDEPENDENT WOMEN. TAYLOR SWIFT U OVERSOLD THIS LIFE TO ME.

# DIEU'S TO DO:
    # Make sure it's not stuck on an infinite loop; integrate /cancel command.
    # Find a list of food categories from Burpple


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

GENDER, PHOTO, LOCATION, SELECTION_1, SELECTION_2, SELECTION_3 = range(6)

# Sends messages for /start command; bot will ask user what they feel like eating
# I would name this SELECTION_1 but it breaks the code and I don't want to fix it.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user = update.effective_user
    first_name = user.first_name
    start_reply = ("Hi " + first_name + "! " + "I'm the makan-ing bot. I can help you find some makan spots near you! \n\n"
                   + "What do you feel like eating today?")

# 1st set of food categories
    reply_keyboard_1 = [
        ["IDK, surprise me!"],
        ["Chinese", "Malay", "Indian"],
        ["Cafes","Vegetarian", "Hawker food"],
        ["More options"],
    ]

    await update.message.reply_text (
        start_reply,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_1, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
        )
        
    )

    return SELECTION_2

###!!! 2nd set of food categories IF user clicks on "More options" in start
async def selection_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    first_name = user.first_name
    user_food_choice = update.message.text
    lower_user_food_choice = str.lower(user_food_choice)
    user_location = update.message.location
    print(user.username + "'s user choice = " + user_food_choice)

    if user_food_choice == "More options":
        more_options_reply = ("Here are more options!")
        reply_keyboard_2 = [
        ["IDK, surprise me!"], 
        ["Japanese", "Korean", "Thai"],
        ["Pasta", "Pizza", "Burger"],
        ["More options"],
        ]
        await update.message.reply_text (
            more_options_reply,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_2, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
            )
        )

# IF user clicks on any food categories from selection_2, this flow will happen:
    else:
        user_food_choice_reply = ("Ooh, that sounds delicious! \n\n"
                       + "Send me your current location so that I look for some " + lower_user_food_choice + " makan spots nearby 🍽️")
        await update.message.reply_text (
            user_food_choice_reply
            )
        
    return SELECTION_3

###!!! 3rd set of food categories IF user clicks on "More options" in selection_2
async def selection_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    first_name = user.first_name
    user_food_choice = update.message.text
    lower_user_food_choice = str.lower(user_food_choice)
    user_location = update.message.location
    print(user.username + "'s user choice = " + user_food_choice)

    if user_food_choice == "More options":
        more_options_reply = ("Here are more options!")
        reply_keyboard_3 = [
        ["IDK, surprise me!"], 
        ["Brunch", "Bubble tea", "Dessert"],
        ["Supper", "Hot pot", "Salads"],
        ["More options"],
        ]
        await update.message.reply_text (
            more_options_reply,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_3, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
            )
        )

# IF user clicks on any food categories from selection_3, this flow will happen:
    else:
        user_food_choice_reply = ("Ooh, that sounds delicious! \n\n"
                       + "Send me your current location so that I look for some " + lower_user_food_choice + " makan spots nearby 🍽️")
        await update.message.reply_text (
            user_food_choice_reply
            )
        ### here is where i'll put return LOCATION
        
    return SELECTION_1

###!!! Return to 1st set of food categories IF user clicks on "More options" in selection_3
async def selection_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    first_name = user.first_name
    user_food_choice = update.message.text
    lower_user_food_choice = str.lower(user_food_choice)
    user_location = update.message.location
    print(user.username + "'s user choice = " + user_food_choice)

    if user_food_choice == "More options":
        more_options_reply = ("Here are more options!")
        reply_keyboard_1 = [
        ["IDK, surprise me!"],
        ["Chinese", "Malay", "Indian"],
        ["Cafes","Vegetarian", "Hawker food"],
        ["More options"],
    ]
        await update.message.reply_text (
            more_options_reply,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_1, one_time_keyboard=True, input_field_placeholder="I'm so hungry :("
            )
        )

# IF user clicks on any food categories from selection_1, this flow will happen:
    else:
        user_food_choice_reply = ("Ooh, that sounds delicious! \n\n"
                       + "Send me your current location so that I look for some " + lower_user_food_choice + " makan spots nearby 🍽️")
        await update.message.reply_text (
            user_food_choice_reply
            )
        
    return SELECTION_2





### CLEAN UP THE BELOW FLOW. Once we're done logging the food category from the user, we can work on getting nearby options with that category. ###





# async def selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Reads the option selected by the user or gives more options."""
#     user = update.message.from_user
#     user_food_choice = update.message.text
#     user_location = update.message.location
#     print ("user choice = " + user_food_choice)
#     # logger.info(
#     #     "Message  ", user_food_choice
#     # )

#     if user_food_choice == "More options":


#     await update.message.reply_text(
#         "Thanks! Let me look for some yummy food near you."
#     )

#     return LOCATION

###############################




    # Keyboard for user to send location -> Need to account for typing as well
    reply_keyboard = [[KeyboardButton(text="🍴 Send current location", request_location=True)]]

    start_reply = ("Hi " + first_name + "!"
                   + " Let's look for some makan spots for you. \n\n"
                   + "Send me your current location or where you plan to go."
                   )
    
    await update.message.reply_text (
        start_reply,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Send me your location! (Stalker vibes, jk)"
        )
        
    )

    return LOCATION

# THIS PART IS IMPORTANT. DON'T DELETE!!! #
# async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Stores the location and asks for some info about the user."""
#     user = update.message.from_user
#     user_location = update.message.location
#     logger.info(
#         "Location of %s: %f / %f", user.username, user_location.latitude, user_location.longitude
#     )
#     await update.message.reply_text(
#         "Thanks! Let me look for some yummy food near you."
#     )

#     return

###################

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



    # Test env token
    # application = Application.builder().token("6566523234:AAGGe36r6_Bqis9BdxHHnRua0kSaBEc_OhQ").build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
        states={
            # LOCATION: [
            #     MessageHandler(filters.LOCATION, location),
            # ],
            SELECTION_1: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, selection_1),
            ],
            SELECTION_2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, selection_2),
            ],
            SELECTION_3: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, selection_3),
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()