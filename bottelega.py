import telebot
import requests
import sql
import newspik as na
from api_keys import api_key_telegram

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

bot = telebot.TeleBot(api_key_telegram,parse_mode=None)
selc_cat = False
sett_cat = False
selc_kw = False
sett_kw = False
dict_cat = {'Бизнес':'business', 'Развлечение':'entertainment', 'Здоровье':'health', 'Наука':'science', 'Спорт':'sports', 'Технологии':'technology'}

@bot.message_handler(commands=['start'])
def handle_start_help(message):
    user_id = message.from_user.id
    if(sql.check_sub(user_id)):
        bot.send_message(user_id,"Вы уже подписаны")
    else:
        sql.add_sub(user_id)
        bot.send_message(user_id,"Привет. Мы вас добавили в список подписчиков нашего бота.\n Команды ищите в readme или в списке команд бота")

@bot.message_handler(commands=['categorys'])
def handle_categ(message):
    global selc_cat
    global sett_cat
    user_id = message.from_user.id
    if(not sql.check_cat(user_id)):
        markup_reply = telebot.types.ReplyKeyboardMarkup(row_width=3)
        itembtn1 = telebot.types.KeyboardButton('Бизнес')
        itembtn2 = telebot.types.KeyboardButton('Развлечение')
        itembtn3 = telebot.types.KeyboardButton('Здоровье')
        itembtn4 = telebot.types.KeyboardButton('Наука')
        itembtn5 = telebot.types.KeyboardButton('Спорт')
        itembtn6 = telebot.types.KeyboardButton('Технологии')
        markup_reply.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)
        bot.send_message(user_id,"Выберете категорию",reply_markup=markup_reply)
        selc_cat = True
    else:
        markup_reply = telebot.types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = telebot.types.KeyboardButton('Удалить категорию')
        itembtn2 = telebot.types.KeyboardButton('Отмена')
        markup_reply.add(itembtn1, itembtn2)
        bot.send_message(user_id,f"Ваша категория - {get_key(dict_cat,sql.ret_cat(user_id))}",reply_markup=markup_reply)
        sett_cat = True

@bot.message_handler(commands=['keywords'])
def handle_kw(message):
    global selc_kw
    global sett_kw
    user_id = message.from_user.id
    if(not sql.check_kw(user_id)):
        bot.send_message(user_id,"Введите ключевое слово")
        selc_kw = True
    else:
        markup_reply = telebot.types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = telebot.types.KeyboardButton('Удалить ключевое слово')
        itembtn2 = telebot.types.KeyboardButton('Отмена')
        markup_reply.add(itembtn1, itembtn2)
        bot.send_message(user_id,f"Ваше ключевое слово - {sql.ret_kw(user_id)}",reply_markup=markup_reply)
        sett_kw = True

@bot.message_handler(commands=['news'])
def handle_news(message):
    user_id = message.from_user.id
    if(not sql.check_cat(user_id) and not sql.check_kw(user_id)):
        for i,j in zip(na.ret_news(),na.ret_news_url()):
            bot.send_message(user_id,f"{i} \n {j}")
    elif(sql.check_cat(user_id) and not sql.check_kw(user_id)):
        for i,j in zip(na.ret_news(cat=sql.ret_cat(user_id)),na.ret_news_url(cat=sql.ret_cat(user_id))):
            bot.send_message(user_id,f"{i} \n {j}")
    elif(not sql.check_cat(user_id) and sql.check_kw(user_id)):
        for i,j in zip(na.ret_news(kw=sql.ret_kw(user_id)),na.ret_news_url(kw=sql.ret_kw(user_id))):
            bot.send_message(user_id,f"{i} \n {j}")
    else:
        for i,j in zip(na.ret_news(kw=sql.ret_kw(user_id),cat=sql.ret_cat(user_id)),na.ret_news_url(kw=sql.ret_kw(user_id),cat=sql.ret_cat(user_id))):
            bot.send_message(user_id,f"{i} \n {j}")


@bot.message_handler(func=lambda message: True)
def answer_to_message(message):
    global selc_cat
    global sett_cat
    global selc_kw
    global sett_kw
    user_id = message.from_user.id
    if (message.text in dict_cat and selc_cat):
        sql.add_cat(user_id,dict_cat.get(message.text))
        bot.send_message(user_id,"Категория добавлена успешно", reply_markup=telebot.types.ReplyKeyboardRemove())
        selc_cat = False
    elif (message.text == "Удалить категорию" and sett_cat):
        sql.del_cat(user_id)
        bot.send_message(user_id,"Категория удалена",reply_markup=telebot.types.ReplyKeyboardRemove())
        sett_cat = False
    elif (message.text == "Отмена" and (sett_cat or sett_kw)):
        bot.send_message(user_id,"Отмена",reply_markup=telebot.types.ReplyKeyboardRemove())
        sett_cat = False
    elif (selc_kw):
        sql.add_kw(user_id,message.text)
        bot.send_message(user_id,"Ключевое слово добавлено успешно")
        selc_kw = False
    elif (message.text == "Удалить ключевое слово" and sett_kw):
        sql.del_kw(user_id)
        bot.send_message(user_id,"Ключевое слово удалено",reply_markup=telebot.types.ReplyKeyboardRemove())
        sett_cat = False
    else:
        bot.send_message(user_id,"Что-то полшло не так. Попробуйте ещё раз")
 
    


bot.polling()