from pymongo import MongoClient
from telebot import formatting

from .markup import Markup
from .get_link import get_image_link

uri = "mongodb+srv://juliphyy:l7jOBx88bEV9kvw5@cluster0.vpa0axs.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
collection = client.magicdocs.data


def exist_user(id, bot):
    try:
        x = collection.find_one({"chatID": id})
        if x is not None:
            return True
        else:
            return False

    except:
        bot.send_message(id,
                         'Вибачте! Щось трапилось з базою данних. Спробуйте ще раз пізніше чи напишіть до підтримки.')


def find_user(id, bot):
    try:
        x = collection.find_one({"chatID": id})

        if x:
            return x
        else:
            raise ValueError("ID не найден.")
    except:
        bot.send_message(id,
                         'Вибачте! Щось трапилось з базою данних. Спробуйте ще раз пізніше чи напишіть до підтримки.')


def create_user(user, bot):
    try:
        collection.insert_one(user)
    except:
        bot.send_message(user.id,
                         'Вибачте! Щось трапилось з базою данних. Спробуйте ще раз пізніше чи напишіть до підтримки.')


def delete_user(id, bot):
    try:
        collection.delete_one({"chatID": id})
    except:
        bot.send_message(id,
                         'Вибачте! Щось трапилось з базою данних. Спробуйте ще раз пізніше чи напишіть до підтримки.')


def update_user(msg, bot, change_type):
    try:
        if change_type == 'name' or change_type == 'birthdate':
            collection.update_one({"chatID": int(msg.chat.id)}, {"$set": {change_type: msg.text}})

            if change_type == 'name':
                change_type = "Ім'я"
                text1 = ' було змінено на '
            else:
                change_type = "Дата народження"
                text1 = ' була змінена '

            bot.send_message(msg.chat.id, formatting.hitalic(change_type) + text1 + formatting.hbold(msg.text),
                             reply_markup=Markup('only_back').markup)
        else:
            image = get_image_link(msg, bot)

            collection.update_one({"chatID": int(msg.chat.id)}, {"$set": {"urlFace": image}})

            bot.send_message(msg.chat.id, 'Фото змінено.', reply_markup=Markup('only_back').markup)
    except Exception as e:
        bot.send_message(msg.chat.id,
                         'Вибачте! Щось трапилось з базою данних. Спробуйте ще раз пізніше чи напишіть до підтримки.')
        print("Something went wrong. chatID: " + str(msg.chat.id) + ". Error:")
        print(e)
