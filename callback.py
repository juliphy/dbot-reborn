from db import exist_user, update_user,find_user,delete_user
from markup import Markup
from telebot import formatting

def process_callback(call,bot):
    message = call.message.message_id
    id = call.from_user.id

    match (call.data):
        case "settings": 
            bot.edit_message_text('Settings', id, message_id=message)
            bot.edit_message_reply_markup(id, message, reply_markup=Markup('settings').markup)

        case "back_start":
            if exist_user(id,bot):

                bot.edit_message_text('Start',id, message_id=message)
                bot.edit_message_reply_markup(id, message, reply_markup=Markup('start',True).markup)
            
            else:
                bot.edit_message_text('Start',id, message_id=message)
                bot.send_message(id, 'Ви можете зареєструватися знову.', reply_markup=Markup('start', False).markup)
                

        case "info":
            user = find_user(id,bot)
            bot.edit_message_text("Ім'я: " + user["name"] + "\nДата народження: " + user["birthdate"] + "\nID для входу: " + formatting.hcode(user['id']), id,message_id=message)
            bot.edit_message_reply_markup(id, message, reply_markup=Markup('only_back').markup)
        
        case "delete":
            delete_user(id,bot)
            bot.edit_message_text('Профіль видалено. Щоб знову зробити профіль, натисніть кнопку Назад або пропишіть /start.',id, message)
            bot.edit_message_reply_markup(id, message,reply_markup=Markup('only_back', False).markup)

    if call.data.startswith('update'):
            bot.edit_message_text('Якщо ви вже не хочете змінювати, то натисніть кнопку снизу.', id,message)
            bot.edit_message_reply_markup(id, message, reply_markup=Markup('only_back').markup)

            if call.data.endswith('name'):
                msg = bot.send_message(id, 'Відправте бажаний ПІБ')

                bot.register_next_step_handler(msg, update_user, bot, 'name')
            elif call.data.endswith('date'):
                msg = bot.send_message(id, 'Відправте бажану дату народження')

                bot.register_next_step_handler(msg, update_user, bot, 'birthdate')

            elif call.data.endswith('photo'):
                msg = bot.send_message(id, 'Відправте бажене фото. Тільки 3x4 фото підтримуются.')

                bot.register_next_step_handler(msg, update_user, bot, 'photo')