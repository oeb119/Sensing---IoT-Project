import asyncio
import csv
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, JobQueue
import logging
import pull_thingspeak_data as pu
import gmail as gm
import graph as gr
import edit_eurostar1 as eu

# Enable logging to help debug
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Initializing some access credentials
bot_id = ""
chat_id = ""
text = 'hooplyhoopla'

eu_channel = '2363580'
fl_channel = '2367228'
eu_api_read = 'I0TX348P2XLD2V55'
fl_api_read = '5DMSQSY2KYNGH5ZD'


### Functions to enable travel price checking and alerts every 4 hours ###
# Function defining job that will be scheduled to check and alert every 4 hours
async def send_periodic_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    # if planes are cheaper than trains
    if float(pu.get_latest_price(eu_channel, 1, eu_api_read)) > float(pu.get_latest_price(fl_channel, 1, fl_api_read)):
        print('IF')
        try:
            print('TRY')
            # Send a message if conditions are met
            train_price = pu.get_latest_price(eu_channel, 1, eu_api_read)
            plane_price = pu.get_latest_price(fl_channel, 1, fl_api_read)
            await context.bot.send_message(job.chat_id, text=
f'''HEY HEY!! Crazy stuff is happening!

On December 20th, PLANES from London to Paris are CHEAPER than TRAINS! 
Planes: £{plane_price}
Trains: £{train_price}

Send your MP an email ASAP with "/email 20"''')    
        except Exception as e:
            logging.error(f"An error occurred while sending a message: {e}")
    else:
        try:
            await context.bot.send_message(job.chat_id, text=f'''All is well, trains for December 20th are cheaper than planes.''')
        except Exception as e:
            logging.error(f"An error occurred while sending a message: {e}") 

# Function adding the send_periodic_message function to the job queue
async def set(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    context.job_queue.run_repeating(send_periodic_message, interval = 60, chat_id=chat_id, name=str(chat_id))
    await update.effective_message.reply_text("Dec 20th travel checker initiated")

# Function that removes jobs from the job queue if called
def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

# Function calling the job removing function
async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Travel checker successfully cancelled!" if job_removed else "There is no active travel checking going on"
    await update.message.reply_text(text)


### Function to track user engagement with bot functions (email sent and tickets bot) in a csv file ###

def add_to_csv(command_type, day):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [timestamp, command_type, day]

    with open('user_traction.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)


### Functions to check ticket prices ###

# Function to convert desired travel day to corresponding field number in thingspeak data
def day_to_field(day):
    corresp = ['20', '21', '22', '23', '24', '25', '26', '27']
    field = corresp.index(str(day)) + 1
    return field

# Function to get lowest train and plane prices for the requested day
async def min_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # if planes are cheaper than trains
    if float(pu.get_latest_price(eu_channel, day_to_field(update.message.text), eu_api_read)) > float(pu.get_latest_price(fl_channel, day_to_field(update.message.text), fl_api_read)):
        # Send a message if conditions are met
        day = update.message.text
        train_price = pu.get_latest_price(eu_channel, day_to_field(update.message.text), eu_api_read)
        plane_price = pu.get_latest_price(fl_channel, day_to_field(update.message.text), fl_api_read)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=
        f'''On Dec {day}: 
        Planes are cheaper! 
        Planes: £{plane_price}
        Trains: £{train_price}''')
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'If you want to protest, type "/email {day}", and your MP will get an email demanding greener travel.')
    
    elif float(pu.get_latest_price(eu_channel, day_to_field(update.message.text), eu_api_read)) == False:
        day = update.message.text
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'There are no trains on Dec {day}!')
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'If you want to protest, type "/email {day}", and your MP will get an email demanding greener travel.')

    # if trains are chepaer than planes
    else:
        day = update.message.text
        train_price = pu.get_latest_price(eu_channel, day_to_field(update.message.text), eu_api_read)
        plane_price = pu.get_latest_price(fl_channel, day_to_field(update.message.text), fl_api_read)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=
        f'''On Dec {day}: 
        Trains are cheaper 
        Planes: £{plane_price}
        Trains: £{train_price}!''')
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"If you want to buy the train ticket, type '/buy {day}', and I'll send you the url.")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"If you want to see a graph of how the ticket prices have evolved, type '/graph {day}'")

# Function that sends an email complaining to London Hammersmith MP about expensive trains and cheap flights
async def email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with the arguments passed by the user, when the command /email is issued."""
    # if planes are cheaper than trains
    input_message = update.message.text
    day = input_message.split('/email ')[1]
    if float(pu.get_latest_price(eu_channel, day_to_field(day), eu_api_read)) > float(pu.get_latest_price(fl_channel, day_to_field(day), fl_api_read)):
        print(str(day) + " " + str(pu.get_latest_price(eu_channel, day_to_field(day), eu_api_read)) + " " + str(pu.get_latest_price(fl_channel, day_to_field(day), fl_api_read)))
        gm.send_email(day, pu.get_latest_price(eu_channel, day_to_field(day), eu_api_read), pu.get_latest_price(fl_channel, day_to_field(day), fl_api_read))
        add_to_csv("email", day)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Email sent to Andy Slaughter")

    elif float(pu.get_latest_price(eu_channel, day_to_field(day), eu_api_read)) == False:
        gm.send_email(day, pu.get_latest_price(eu_channel, day_to_field(day), eu_api_read), pu.get_latest_price(fl_channel, day_to_field(day), fl_api_read))
        add_to_csv("email", day)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Email sent to Andy Slaughter")
    
    # if trains are chepaer than planes
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, it doesn't make all that much sense to protest if trains are indeed cheaper than planes...")

# Function to provide user with url of train website to buy ticket
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with the arguments passed by the user, when the command /buy is issued."""
    input_message = update.message.text
    day = input_message.split('/buy ')[1]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Here's the url. Please let me know '/bought {day}' after you buy your ticket.")
    await (context.bot.send_message(chat_id=update.effective_chat.id, text=str(eu.get_url("7015400", "8727100", "2023-12-", str(day)))))

# Function to track user purchase conversion and add it to the csv file
async def bought(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with the arguments passed by the user, when the command /bought is issued."""
    input_message = update.message.text
    day = input_message.split('/bought ')[1]
    add_to_csv("ticket", day)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Thanks for letting me know. Safe travels!")

# Function to provide user with a graph of how train and plane prices have evolved over past few days for requested travel date
async def graph(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with the arguments passed by the user, when the command /graph is issued."""
    input_message = update.message.text
    day = input_message.split('/graph ')[1]
    gr.plot_save_name(str(day), day_to_field(str(day)))
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Here's how the prices have varied recently")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('plot_dec_{}.png'.format(str(day)), 'rb'))

# Function to redirect invalid user messages
async def stray_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please type a valid message or command :)")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Type /help for guidance")

# Function to provide a guide of the bot's purpose and commands
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="""Hey hey! I am GroundTravel, a green travel bot who informs you about travel prices from London to Paris between Dec 20 and Dec 27th. Here are a few commands:

- Type "/set" for me to check every 2 hours if flight prices are cheaper than train prices. Type "/unset" to end it.

- Current fares: type the day of travel between dec 20-27th (ex. 22)
                                   
- Graph of flight and train prices for a travel date evolution: type "/graph" followed by travel day (ex. /graph 22)

- Buy train ticket: type "/buy" followed by travel day (ex. /buy 22). Please notify me if you bought it with "/bought 22"

- Activist complain to local MP about expensive flights: type "/email" followed by day of travel (ex. /email 22)""")

if __name__ == '__main__':
    application = ApplicationBuilder().token('6633365284:AAEryJOWdvrXIQNQiWHJKLQKA0B2UVQStPA').build()
    
    #associates the user message with the function to respond
    email_handler = CommandHandler('email', email)
    graph_handler = CommandHandler('graph', graph)
    help_handler = CommandHandler(['help', 'start'], help)
    buy_handler = CommandHandler('buy', buy)
    bought_handler = CommandHandler('bought', bought)
    min_price_handler = MessageHandler(filters.Text(["20", "21", "22", "23", "24", "25", "26", "27"]), min_price)
    stray_text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), stray_text)

    #adds the command and message handlers to bot application
    application.add_handler(CommandHandler("set", set))
    application.add_handler(CommandHandler("unset", unset))

    application.add_handler(email_handler)
    application.add_handler(graph_handler)
    application.add_handler(help_handler)
    application.add_handler(buy_handler)
    application.add_handler(bought_handler)
    application.add_handler(min_price_handler)
    application.add_handler(stray_text_handler)
    
    print(application.bot)
    
    #starts the bot application and sets it ot continuously poll for new updates
    #when an update is received, the corresponding event handler will be called
    application.run_polling()