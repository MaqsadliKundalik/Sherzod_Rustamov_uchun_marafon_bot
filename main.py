from telebot import TeleBot, types

import db

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL = "Your_channel"
admin = "Admin_id"
bot = TeleBot(BOT_TOKEN)
bot.send_message(admin, 'Bot ishga tushdi!')

# Keyboard Markups
checksub_KM = types.InlineKeyboardMarkup(row_width=1).add(
                             types.InlineKeyboardButton(text='Kanalga kirish', url='https://t.me/' + CHANNEL),
                             types.InlineKeyboardButton(text="Tekshirish", callback_data="checksub")
                         )

checksub_KM2 = types.InlineKeyboardMarkup(row_width=1).add(
                             types.InlineKeyboardButton(text='Kanalga kirish', url='https://t.me/' + CHANNEL),
                             types.InlineKeyboardButton(text="Tekshirish", callback_data="checksub2")
                         )

main_KM = types.ReplyKeyboardMarkup(row_width=2).add(
    "Referal havola", "Ballim", "Reyting"
)

# nested functions

def check_sub_channel(message):
    status = bot.get_chat_member("@" + CHANNEL, message.from_user.id).status
    if status in ['member', 'creator', "administrator"]: return True
    else: return False

def nested_start_reply(message: types.Message):
    if len(message.text) > 100:
        bot.send_message(message.from_user.id, f'Men {len(message.text)} ta belgili ism-familya mavjudligiga ishonmayman. Iltimos haqiqiy ism-familyangizni yuboring.')
        bot.register_next_step_handler(message, nested_start_reply)
    elif message.text.count(" ") > 2:
        bot.send_message(message.from_user.id, "Menga faqat ism familyangizni yuboring.")
        bot.register_next_step_handler(message, nested_start_reply)
    else:
        db.add_user('name', message.text, message.from_user.id)
        user = db.get_user(message.from_user.id)
        if check_sub_channel(message):
            db.add_user('subs', '1', message.from_user.id)
            if user[2]:
                bot.send_message(user[2], "Sizga 1 ball qo'shildi!")
            bot.send_message(message.from_user.id, "Nima qilamiz?", reply_markup=main_KM)
        else:
            bot.send_message(message.from_user.id, "Siz quydagi kanal obunachisi bo'lishingiz lozim.",
                             reply_markup=checksub_KM)

def nested_send_message_for_users(message: types.Message):
    users = db.get_users()
    a, b = 0, 0
    for i in users:
        try:
            bot.copy_message(i[0], message.from_user.id, message.message_id, reply_markup=message.reply_markup)
            a += 1
        except:
            b += 1
            continue
    bot.send_message(message.from_user.id, f"Xabar yuborilganlar: {a} ta\nXabar yuborilmaganlar: {b} ta")

@bot.message_handler(commands=['start'], chat_types=['private'])
def start_reply(message:types.Message):
    bot.delete_message(message.from_user.id, message.message_id)
    if not db.get_user(message.from_user.id):
            db.add_user('id', message.from_user.id, message.from_user.id)
            if message.text[7:].isdigit():
                db.add_user('reffer', message.text[7:], message.from_user.id)
                reffer = db.get_user(message.text[7:])
                bot.send_message(reffer[0], f"{message.from_user.full_name} do'stingiz botga tashrif buyurdi! Endi do'stingiz ism-familyasini yuborishi va kanal obunachisi ekanligini tasdiqlatishi kerak.")
            bot.send_message(message.from_user.id, "Assalomu alaykum, menga ism familyangizni yuboring.")
            bot.register_next_step_handler(message, nested_start_reply)

    elif not db.get_user(message.from_user.id)[1]:
            db.add_user('id', message.from_user.id, message.from_user.id)
            if message.text[7:].isdigit():
                db.add_user('reffer', message.text[7:], message.from_user.id)
                reffer = db.get_user(message.text[7:])
                bot.send_message(reffer[0], f"{message.from_user.full_name} do'stingiz botga tashrif buyurdi! Endi do'stingiz ism-familyasini yuborishi va kanal obunachisi ekanligini tasdiqlatishi kerak.")
            bot.send_message(message.from_user.id, "Assalomu alaykum, menga ism familyangizni yuboring.")
            bot.register_next_step_handler(message, nested_start_reply)

    else:
        if check_sub_channel(message):
            db.add_user('subs', '1', message.from_user.id)
            bot.send_message(message.from_user.id, "Nima qilamiz?", reply_markup=main_KM)
        else:
            db.add_user('subs', '0', message.from_user.id)
            bot.send_message(message.from_user.id, "Siz quydagi kanal obunachisi bo'lishingiz lozim.",
                             reply_markup=checksub_KM)

@bot.message_handler(commands=['users'], func=lambda message: message.from_user.id == admin)
def send_users_list(message: types.Message):
    with open("users.doc", "w") as doc:
        result = ""
        users = db.get_users()
        j = 0
        for i in users:
            j += 1
            result += (f"{j}-Foydalanuvchi:\n"
                       f"\tIsm-familya: {i[1]}\n"
                       f"\tID: {i[0]}\n"
                       f"\tKanalga obuna bo'l{'' if int(i[3]) else 'ma'}gan\n\n")
        doc.write(result)
    with open('users.doc', "r") as doc: bot.send_document(message.from_user.id, document=doc)

@bot.message_handler(commands=['send'], func=lambda message: message.from_user.id == admin)
def send_message_for_users(message: types.Message):
    bot.send_message(message.from_user.id, "Menga foydalanuvchilarga yuboriladigan xabarni tashlang.")
    bot.register_next_step_handler(message, nested_send_message_for_users)
@bot.message_handler(chat_types=['private'])
def replier(message: types.Message):
    match message.text:
        case "Referal havola":
            bot.send_message(message.from_user.id, "https://t.me/onlaynonatiliuz_bot?start=" + str(message.from_user.id))
        case "Ballim":
            user = db.get_user(message.from_user.id)
            ball = 0
            for i in db.get_users():
                if user[0] == i[3]: ball += 1
            bot.send_message(user[0], f"Sizning ma'lumotlaringiz:\n\nIsm-familya: {user[1]}\nBall: {ball}")
        case 'Reyting':
            reyting = db.get_res(message.from_user.id)
            n = reyting[1]
            reyting = reyting[0]
            result = "Reyting:\n"
            j = 1
            for i in reyting:
                result += f"{j}. {i[1]} - {i[2]}\n"
                j += 1
                if j > 20: break
            result += f"\nSiz {n}-o'rinsiz.\n"
            result += f"Jami qatnashchilar {len(reyting)} ta"
            bot.send_message(message.from_user.id, result)



@bot.callback_query_handler(lambda x: x.data)
def cbd_query_reply(cbq: types.CallbackQuery):
    bot.delete_message(cbq.from_user.id, cbq.message.id)
    match cbq.data:
        case "checksub2":
                if check_sub_channel(cbq):
                    db.add_user('subs', '1', cbq.from_user.id)
                    user = db.get_user(cbq.from_user.id)
                    if user[2].isdigit():
                        bot.send_message(user[2], "Sizga 1 ball qo'shildi!")
                    bot.send_message(cbq.from_user.id, "Nima qilamiz?", reply_markup=main_KM)
                else:
                    bot.send_message(cbq.from_user.id, "Siz quydagi kanal obunachisi bo'lishingiz lozim.",
                                     reply_markup=checksub_KM)
        case "checksub":
                if check_sub_channel(cbq):
                    db.add_user('subs', '1', cbq.from_user.id)
                    bot.send_message(cbq.from_user.id, "Nima qilamiz?", reply_markup=main_KM)
                else:
                    bot.send_message(cbq.from_user.id, "Siz quydagi kanal obunachisi bo'lishingiz lozim.",
                                     reply_markup=checksub_KM)
bot.polling()