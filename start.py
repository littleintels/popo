


from telegram.ext import *
from telegram import *
import telegram
import telegram
import logging,json
from callbacks import *
from app import *
from keys import *
from inlines import *
from pagin import *
from delete import *


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)



logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#Start of function definitions
def start(update,context) -> None:
    user = int(update.effective_chat.id)
    with open("./jsons/stats.json") as bot_status:
        status_bot = json.load(bot_status)
    keyee =[["Products","PGP Key"],["📦 Orders (0)","📊Feedback 98.97%","💵 Payments"],["🛒 Cart","✉️ Chat"]]
    keyboard = ReplyKeyboardMarkup(keyee,one_time_keyboard=False,resize_keyboard=True)
    if update.message.chat['type'] == "private":
        with open("./jsons/keys.json", 'r') as fp:
            keys = json.load(fp)
        admin = keys['admins']
        if user in admin:
            keye =[["🟢 Add Product"],["Customer's view"]]
            keyboar = ReplyKeyboardMarkup(keye,one_time_keyboard=False,resize_keyboard=True)
            text = f"<b>Welcome to moderator panel {update.message.from_user.first_name}</b>\n" \
                   f"1. ℹ️ Add Product - adding new goods to list\n" \
                   f"2. 🟢 Activate/Deactivate - activating bot so user can access store\n" \
                   f"3. Customer's view - view store as user"            
            context.bot.send_message(chat_id=user,text=text,reply_markup=keyboar,parse_mode="html")
        else:
            with open("./jsons/users.json") as fps:
                users = json.load(fps)
            with open("./jsons/users_order.json") as fp:
                orders = json.load(fp)
            
            with open("./jsons/keys.json", 'r') as fp:
                keys = json.load(fp)
            pgp = keys['start']
            if user not in users['user']:
                orders.append({
                    "id": user,
                    "orders": [],
                    "totallist": 0,
                    "topay": 0,
                    "successorderandpaid": [],
                    "payments": [],
                    "key": "Products",
                    "del":  0,
                    "del2":0,
                    "shipmethod": "",
                    "paytype": "",
                    "extra": "",
                    "extra2": "",
                    "extra3": ""
                })
                with open("./jsons/users_order.json", 'w') as json_fil:
                    json.dump(orders, json_fil, 
                            indent=3,  
                            separators=(',',': '))
        
                users['user'].append(int(user))
                with open("./jsons/users.json", 'w') as json_file:
                    json.dump(users, json_file)
        
                update.message.reply_text(pgp,parse_mode="html",reply_markup=keyboard)
            else:
                update.message.reply_text(pgp,parse_mode="html",reply_markup=keyboard)
        
    
def stats(update,context) -> None:
    user = int(update.effective_chat.id)
    context.bot.deleteMessage (message_id = update.message.message_id,
                           chat_id = user)
    if update.message.chat['type'] == "private": 
        if user == 1185692914:
            keymap = [
                       [InlineKeyboardButton("Activate 🟢", callback_data=f"activate"),
                       InlineKeyboardButton("Deactivate 🔴",callback_data=f"deactivate")],
                       [InlineKeyboardButton("Close", callback_data=f"close")]
                       
                     ]
            inline = InlineKeyboardMarkup(keymap)
            context.bot.send_message(chat_id=user,text="Choose bot status",reply_markup=inline)
    
    
    
def relogin(update,context) -> None:
    user = int(update.effective_chat.id)
    if update.message.chat['type'] == "private":
        with open("./jsons/keys.json", 'r') as fp:
            keys = json.load(fp)
            
        admin = keys['admin']
        if user in admin:
            keys['admins'].append(user)
            with open("./jsons/keys.json", 'w') as json_file:
                    json.dump(keys, json_file)
            keye =[["🟢 Add Product"],["Activate&Deactivate","Customer's view"]]
            keyboar = ReplyKeyboardMarkup(keye,one_time_keyboard=False,resize_keyboard=True)
            text = f"<b>Welcome to moderator panel {update.message.from_user.first_name}</b>\n" \
                   f"1. ℹ️ Add Product - adding new goods to list\n" \
                   f"2. 🟢 Activate/Deactivate - activating bot so user can access store\n" \
                   f"3. Customer's view - view store as user"            
            context.bot.send_message(chat_id=user,text=text,reply_markup=keyboar,parse_mode="html")
    
def logout(update,context) -> None:
    user = int(update.effective_chat.id)
    with open("./jsons/keys.json", 'r') as fp:
            keys = json.load(fp)
    admin = keys['admins']
    if user in admin:
        print("yes")
        admin_postion = int(admin.index(user))
        del admin[admin_postion]
        with open("./jsons/keys.json", 'w') as json_file:
                    json.dump(keys, json_file)
        keyee =[["Products","PGP Key"],["📦 Orders (0)","📊Feedback 98.97%","💵 Payments"],["🛒 Cart","✉️ Chat"]]
        keyboard = ReplyKeyboardMarkup(keyee,one_time_keyboard=False,resize_keyboard=True)
        context.bot.send_message(chat_id=user,text="Logged successfully as customer\nUse /login to become bot admin again only bot owner can do this",reply_markup=keyboard)


def pgp(update,context) -> None:
    text = update.message.text.split()[1:]
    user = int(update.effective_chat.id)
    texty = str(" ".join(text))
    
    print(texty)
    context.bot.send_message(chat_id=user,text=texty,parse_mode="markdown")
    
    
   
    with open("./pagi/neutral.json", 'r') as fp:
        keys = json.load(fp)
    neutral = keys['neutral']
    neutral.append(texty)
    with open("./pagi/neutral.json", 'w') as json_fil:
        json.dump(keys, json_fil, 
                    indent=3,  
                    separators=(',',': '))
        
        
        
        
        
def backs(update,context) -> None:
    keyboard = update.message.text
    user = int(update.effective_chat.id)
    
    
    if update.message.chat['type'] == "private":
        with open("./jsons/users_order.json") as fp:
            orders = json.load(fp)
        
        with open("./jsons/keys.json", 'r') as fp:
            keys = json.load(fp)
        admin = keys['admins']
        if user in admin:
        
            keye =[["🟢 Add Product"],["Customer's view"]]
            keyboar = ReplyKeyboardMarkup(keye,one_time_keyboard=False,resize_keyboard=True)
            text = f"<b>Welcome to moderator panel {update.message.from_user.first_name}</b>\n" \
                   f"1. ℹ️ Add Product - adding new goods to list\n" \
                   f"2. 🟢 Activate/Deactivate - activating bot so user can access store\n" \
                   f"3. Customer's view - view store as user"            
            context.bot.send_message(chat_id=user,text=text,reply_markup=keyboar,parse_mode="html")
        else:
            
            for i in orders:
                if i['id'] == user:
                    position = i["key"]
                    if position == "Products":
                        with open("./jsons/keys.json", 'r') as fp:
                            keyss = json.load(fp)
                        pgp = keyss['start']
                        keyee =[["Products","PGP Key"],["📦 Orders (0)","📊Feedback 98.97%","💵 Payments"],["🛒 Cart","✉️ Chat"]]
                        keyboardo = ReplyKeyboardMarkup(keyee,one_time_keyboard=False,resize_keyboard=True)
                        context.bot.send_message(user,pgp,reply_markup=keyboardo,parse_mode="html")
                        break
                    else:
                        with open("./jsons/new_keys.json", 'r') as fp:
                            keys = json.load(fp)
                        for it in keys:
                            if position in it["keys"]:
                                keybod = it['name']
                                for iu in keys:
                                    if iu['name'] == keybod:
                        
                                        if iu['desc'] == "no":
                                            desc = keyboard
                                        else:
                                            desc = iu['desc']
                            
                                        button_list = []
                                        for ad in iu['keys']:
                                            button_list.append(ad)
                                        reply_markup=ReplyKeyboardMarkup(build_menu(button_list,n_cols=1),one_time_keyboard=False,resize_keyboard=True)
                                        context.bot.send_message(chat_id=user,text=desc,reply_markup=reply_markup,parse_mode="markdown")
                                        check_position(user=user,keyboard=keybod)
                                        break
     
               
def main() -> None:
    # Create the Updater and pass it your bot's token.
    token = "2025749575:AAEg4tp3e0u6jQoHk2VeRlcHPEOcvY4Ejxk"
    
    updater = Updater(token,use_context=True)
    dp = updater.dispatcher
   
    print('started bot')
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('login', relogin))
    updater.dispatcher.add_handler(CommandHandler('delete', delete))
    updater.dispatcher.add_handler(CommandHandler('logout', logout))
    updater.dispatcher.add_handler(CommandHandler('pgp', pgp))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex("^Customer's view"),logout))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex("^Back to store"),start))
    dp.add_handler(CallbackQueryHandler(on_callback_query, pattern='^character#'))
    dp.add_handler(CallbackQueryHandler(neutral, pattern='^neutral#'))
    dp.add_handler(CallbackQueryHandler(negative, pattern='^negative#'))
    dp.add_handler(CallbackQueryHandler(positive, pattern='^positive#'))
    
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^Activate&Deactivate'),stats))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^View Products'),add_products))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^Back'),backs))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^Main Menu'),start))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^🟢 Add Product'),products))
    updater.dispatcher.add_handler(CallbackQueryHandler(refresh))
    updater.dispatcher.add_handler(CommandHandler('new', new_product))
    updater.dispatcher.add_handler(CommandHandler('key', keyboa))
    updater.dispatcher.add_handler(CommandHandler('inline', inlines))
    updater.dispatcher.add_handler(CommandHandler('desc', desc))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, keyboards))
    
   
   
    updater.start_polling()
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
    
    
if __name__ == '__main__':
    main()