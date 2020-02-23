import telebot
import pobedaMovies

bot = telebot.TeleBot('942385623:AAHC1o_C2r1Bm1kpwqW9hlt-vA3Ak9NMBTQ')

jsonData = pobedaMovies.reloadData()

@bot.message_handler(commands=['help','start'])
def start_message(message):
    bot.send_message(message.chat.id, '/update - reload movies data\n/all - show all movie titles\n/date - show all movie sessions for the date\n/date_with_subs - show all movie sessions for the date that have subtitles')

@bot.message_handler(commands=['date'])
def userInputRequest(message):
    bot.send_message(message.chat.id, 'Input date as dd.mm')
    bot.register_next_step_handler(message, process_date)

@bot.message_handler(commands=['date_with_subs'])
def userInputRequestWithSubs(message):
    bot.send_message(message.chat.id, 'Input date as dd.mm')
    bot.register_next_step_handler(message, process_date_with_subs)  

@bot.message_handler(commands=['update'])
def update_data(message):
    jsonData = pobedaMovies.reloadData()
    bot.send_message(message.chat.id, 'Updated.')

@bot.message_handler(commands=['all'])
def showAll(message):
        separator = '\n'
        allNames = pobedaMovies.getMovieNames(jsonData)
        botResponse = separator.join(allNames)
        bot.send_message(message.chat.id, botResponse)

def process_date(message, subs = False):
    try:
        inputDate = message.text
        namesByDate = pobedaMovies.getNamesByDate(jsonData, inputDate, subs)
        separator = '\n'
        botResponse = separator.join(namesByDate)
        bot.send_message(message.chat.id, 'your results:\n' + botResponse)
    except Exception as e:
        bot.reply_to(message, 'oops: ' + e)

def process_date_with_subs(message):
    process_date(message, True)


bot.polling()
