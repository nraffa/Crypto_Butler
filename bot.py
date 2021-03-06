import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
import requests

def get_prices():
    coins = ["BTC", "ETH", "ETC", "ADA", "DOGE", "XRP"]

    crypto_data = requests.get(
        "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=USD".format(",".join(coins))).json()["RAW"]

    data = {}
    for i in crypto_data:
        data[i] = {
            "coin": i,
            "price": crypto_data[i]["USD"]["PRICE"],
            "change_day": crypto_data[i]["USD"]["CHANGEPCT24HOUR"],
            "change_hour": crypto_data[i]["USD"]["CHANGEPCTHOUR"]
        }

    return data

if __name__ == "__main__":
    print(get_prices())

#We first import os, and then set the port number to listen in for the webhook.
import os
PORT = int(os.environ.get('PORT', 88))


telegram_bot_token = '1859659731:AAE548d5qWjZQtTSL4aWzFUvKc0eyTH0lYE'

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    chat_id = update.effective_chat.id
    message = "I'm your go-to crypto bot, please talk to me!\nPress /prices so I can give you last updates on cryptocurrencies."
    context.bot.send_message(chat_id=chat_id, text=message)

def prices(update, context):
    chat_id_prices = update.effective_chat.id
    message_prices = "This are the latest updates on the prices of Bitcoin, Ethereum, Cardano and others.\nIf you have any feedback for me, press on /feedback."

    crypto_data = get_prices()
    for i in crypto_data:
        coin = crypto_data[i]["coin"]
        price = crypto_data[i]["price"]
        change_day = crypto_data[i]["change_day"]
        change_hour = crypto_data[i]["change_hour"]
        message_prices += f"Coin: {coin}\nPrice: ${price:,.2f}\nHour Change: {change_hour:.3f}%\nDay Change: {change_day:.3f}%\n\n"

    context.bot.send_message(chat_id=chat_id_prices, text=message_prices)

def feedback(update, context):
    chat_id_feedback = update.effective_chat.id
    message_feedback = "Please send me your feedback!\nPress /start to go back to the main menu."
    context.bot.send_message(chat_id=chat_id_feedback, text=message_feedback)
    


#The goal is to have this function called every time the Bot receives a Telegram message that 
#contains the /start command. To accomplish that, you can use a CommandHandler 
#(one of the provided Handler subclasses) and register it in the dispatcher:
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

price_handler = CommandHandler('prices', prices)
dispatcher.add_handler(price_handler)

feedback_handler = CommandHandler('feedback', feedback)
dispatcher.add_handler(feedback_handler)

#Next, we modify the following line from to
#updater.start_polling()

updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=telegram_bot_token,
                          webhook_url = 'https://crypto-mayordomo-botv2.herokuapp.com/' + telegram_bot_token )
#updater.bot.setWebhook('https://crypto-mayordomo-bot.herokuapp.com/' + telegram_bot_token)

updater.idle()

#What this is doing is that it changes the polling method to webhook, listening in to 0.0.0.0 with
#the port you specified above with the PORT variable. The token refers to the API token of your telegram
#bot, which should be defined at the top of the code. The next line is to set the Webhook with the link
#to your heroku app, which we will get to next.

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.

