import chatbot

bot = chatbot.Chatbot()

bot.openBrowser()

while True:
    bot.cekAndSendMessage()