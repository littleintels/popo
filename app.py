
from telegram.ext import *
from telegram import *
import telegram
import telegram
import json





def products(update,context) -> None:
    user = int(update.effective_chat.id)
    if update.message.chat['type'] == "private": 
        with open("./jsons/keys.json", 'r') as fp:
            keys = json.load(fp)
        keyboard = keys['keys']
    
        
        button_list = []
        for ad in keyboard:
            button_list.append(ad)
        reply_markup=ReplyKeyboardMarkup(build_menu(button_list,n_cols=1),one_time_keyboard=False,resize_keyboard=True)
        admin = keys['admins']
        if user in admin:
            context.bot.send_message(chat_id=user,text="Click view to see items in product list",reply_markup=reply_markup)
  
def add_products(update,context) -> None:
    user = int(update.effective_chat.id)
    if update.message.chat['type'] == "private": 
        with open("./jsons/new_keys.json", 'r') as fp:
            keys = json.load(fp)
        with open("./jsons/keys.json", 'r') as fps:
            admi = json.load(fps)
            
        
        admins = admi['admins']
        if user in admins:
            for i in keys:
                if i['name'] == 'Products':
                    if i['keys']== ["Back"]:
                        context.bot.send_message(chat_id=user,text="no items in products\nyou can add one with /new [Product Name]")
                        break
                    else:
                        button_list = []
                        for ad in i['keys']:
                            button_list.append(ad)
                        reply_markup=ReplyKeyboardMarkup(build_menu(button_list,n_cols=1),one_time_keyboard=False,resize_keyboard=True)
                        context.bot.send_message(chat_id=user,text="List of items in products\n\nyou can add new product with /new [product name]\n",reply_markup=reply_markup)
                        break
                    
            
def new_product(update,context) -> None:
    user = int(update.effective_chat.id)
    text = update.message.text.split()
   
    if update.message.chat['type'] == "private":
        with open("./jsons/keys.json", 'r') as fps:
            admi = json.load(fps)
            
       
        
        texts = text[1:]
        texty = " ".join(texts)
        admin = admi['admins']
        if user in admin:
            with open("./jsons/new_keys.json", 'r') as fp:
                keys = json.load(fp)
            for i in keys:
                print("here")
                if i['name'] == 'Products':
                   
                    i['keys'][-1] = texty
                    i['keys'].append("Back")
                    
                    
                    
                    keys.append({
                        "name": texty,
                        "inline": [],
                        "keys": ["Back"],
                        "desc": "no"
                    })
                    
                    with open("./jsons/new_keys.json", 'w') as json_file:
                        json.dump(keys, json_file, 
                           ensure_ascii=False,  
                           indent=4    ,
                           separators=(',',': '))
                        button_list = []
                        for ad in i['keys']:
                            button_list.append(ad)
                    reply_markup=ReplyKeyboardMarkup(build_menu(button_list,n_cols=1),one_time_keyboard=False,resize_keyboard=True)
                        
                    context.bot.send_message(chat_id=user,text="Added new product",reply_markup=reply_markup)
    



           
def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu