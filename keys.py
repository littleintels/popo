from telegram.ext import *
from telegram import *
import telegram


import os
import time
import sys
import json
from app import *

from telegram_bot_pagination import InlineKeyboardPaginator

sys.path.append('..')

from common import get_logger, log_func, reply_error
from utils import is_equal_inline_keyboards
from data import *
log = get_logger(__file__)




run_async
log_func(log)
def keyboards(update: Update, context: CallbackContext) -> None:
    keyboard = update.message.text
    user = int(update.effective_chat.id)
    
    
    if update.message.chat['type'] == "private":
        with open("./jsons/keys.json", 'r') as fps:
            admi = json.load(fps)
            
        admin = admi['admins']
        if user in admin:
           
            with open("./jsons/new_keys.json", 'r') as fp:
                keys = json.load(fp)
            for i in keys:
                if i['name'] == f"{keyboard}":
                    
                    if i['inline'] == [] and i['keys'] == []:
                        msg = f"1. Add button keyboard\n2. Add inline keyboard\n"
                        keymap = [
                                   [InlineKeyboardButton("Button", callback_data=f"addbutton {keyboard}"),
                                    InlineKeyboardButton("Inline",callback_data=f"addinline {keyboard}")],
                                   [InlineKeyboardButton("Change description text",callback_data=f"desc {keyboard}")],
                                   [InlineKeyboardButton("Close", callback_data=f"close")] 
                        ]
                        inline = InlineKeyboardMarkup(keymap)
                        context.bot.send_message(chat_id=user,text=msg,reply_markup=inline)
                        break
                    
                    elif i['inline'] != [] and i['keys'] == []:
                        
                        keymap = [
                                 
                                    [InlineKeyboardButton("Inline",callback_data=f"addinline {keyboard}")],
                                    [InlineKeyboardButton("Change description text",callback_data=f"desc {keyboard}")],
                                   [InlineKeyboardButton("Close", callback_data=f"close")] 
                        ]
                        inline = InlineKeyboardMarkup(keymap)
                        context.bot.send_message(chat_id=user,text="You can add more items to this list\n",reply_markup=inline)
                        break
                    
                    elif i['inline'] == [] and i['keys'] != []:
                        msg = f"1. Add button keyboard\n2. Add inline keyboard\n"
                        keymap = [
                                   [InlineKeyboardButton("Button", callback_data=f"addbutton {keyboard}"),
                                    InlineKeyboardButton("Inline",callback_data=f"addinline {keyboard}")],
                                   [InlineKeyboardButton("Change description text",callback_data=f"desc {keyboard}")],
                                   [InlineKeyboardButton("Close", callback_data=f"close")] 
                        ]
                        inline = InlineKeyboardMarkup(keymap)
                        button_list = []
                        for ad in i['keys']:
                            button_list.append(ad)
                        reply_markup=ReplyKeyboardMarkup(build_menu(button_list,n_cols=1),one_time_keyboard=False,resize_keyboard=True)
                        context.bot.send_message(chat_id=user,text="...",reply_markup=reply_markup)
                        context.bot.send_message(chat_id=user,text=msg,reply_markup=inline)
                        break
                    elif i["inline"]!= []:
                        msg = f"1. Add more inline keyboards\nClick any inline here to delete\n\n"
                        keymap = [
                                   [InlineKeyboardButton("Button", callback_data=f"addbutton {keyboard}"),
                                    InlineKeyboardButton("Inline",callback_data=f"addinline {keyboard}")],
                                   [InlineKeyboardButton("Change description text",callback_data=f"desc {keyboard}")],
                                   [InlineKeyboardButton("Close", callback_data=f"close")] 
                        ]
                        inline = InlineKeyboardMarkup(keymap)
                        button_list = []
                        idx = 1
                        for ad in i['inline']:
                            idx+=1
                            button_list.append(InlineKeyboardButton(f"{ad} ❌", callback_data =f"removeinline {idx-2} {keyboard}"))
                        
                        if i['desc'] == "no":
                            velo = "please change goods discription with\n/desc (keyboard name) (your text)\nfor next line use (\\n)\nfor bold use (*)\n for mono use (`)"
                        else:
                            velo = i["desc"]
                            
                        reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
                        context.bot.send_message(chat_id=user,text=velo,reply_markup=reply_markup,parse_mode="html")
                        context.bot.send_message(chat_id=user,text=msg,reply_markup=inline)
                        break
                        print("no")
                        break 
                
                
                elif keyboard == "Add more shipping method":
                    print("shipping")
                    admi['set'] = "shipping"
                    with open("./jsons/keys.json", 'w') as json_file:
                        json.dump(admi, json_file)
                    context.bot.send_message(chat_id=user,text="Please reply to this message with name of the shipping method\ne.g - `$0.00 Royal Mail First Class (UK Only)`",parse_mode='markdown')
                    break
                elif keyboard == "Add more payment method":
                    print("pays")
                    admi['set'] = "pays"
                    with open("./jsons/keys.json", 'w') as json_file:
                        json.dump(admi, json_file)
                    context.bot.send_message(chat_id=user,text="Please reply to this message with name of the payment method\ne.g - `BTC`",parse_mode='markdown')
                    break    
                else:
                    if admi['set'] == "shipping":
                        print('yes')
                        admi['set']=" "
                        with open("./jsons/keys.json","w")as pol:
                            json.dump(admi,pol)
                        with open("./jsons/ship.json","r") as u_file:
                            address = json.load(u_file)
                        add = keyboard.split()
                        if len(add) == 1:
                            ship = add[0]
                        else:
                            ship = " ".join(add[0:])
                        address.append(ship)
                        with open("./jsons/ship.json", "w") as a_file:
                            json.dump(address,a_file)
                        with open("./jsons/ship.json","r") as u_file:
                            shipping = json.load(u_file)
                        
                        button_list = []
                        idx = 1
                        for ad in shipping:
                            idx+=1
                            button_list.append(InlineKeyboardButton(f"{ad} ❌", callback_data =f"removeship {idx-2}"))
                        
                        reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
                        context.bot.send_message(chat_id=user,text="Shipping Method added",reply_markup=reply_markup)
                    elif admi['set'] == "pays":
                        print('yes')
                        admi['set']=" "
                        with open("./jsons/keys.json","w")as pol:
                            json.dump(admi,pol)
                        with open("./jsons/paymethod.json","r") as u_file:
                            address = json.load(u_file)
                        add = keyboard.split()
                        if len(add) == 1:
                            ship = add[0]
                        else:
                            ship = " ".join(add[0:])
                        address.append(ship)
                        with open("./jsons/paymethod.json", "w") as a_file:
                            json.dump(address,a_file)
                        with open("./jsons/paymethod.json","r") as u_file:
                            shipping = json.load(u_file)
                        
                        button_list = []
                        idx = 1
                        for ad in shipping:
                            idx+=1
                            button_list.append(InlineKeyboardButton(f"{ad} ❌", callback_data =f"removepay {idx-2}"))
                        
                        reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
                        context.bot.send_message(chat_id=user,text="Payment Method added",reply_markup=reply_markup)
                
        # here to display to user's keyboards and inlines
        else:
            print("am here")
            with open("./jsons/new_keys.json", 'r') as fp:
                keys = json.load(fp)
            for i in keys:
                if i['name'] == f"{keyboard}":
                    if i['keys'] == ["Back"] and i['inline'] == []:
                        context.bot.send_message(chat_id=user,text="Sorry there's no item here\nprobably it might be added soon")
                        break
                    elif i['keys'] == ["Back"] and i["inline"] != []:
                        if i['desc'] == "no":
                            desc = keyboard
                        else:
                            desc = i['desc']
                            
                        button_list = []
                       
                        for ad in i['inline']:
                            button_list.append(InlineKeyboardButton(ad, callback_data =f"addcart {ad}"))
                            
                        reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
                        context.bot.send_message(chat_id=user,text=desc,reply_markup=reply_markup,parse_mode="html")
                        break
                    elif i['keys'] != ['Back'] and i['inline'] == []:
                        if i['desc'] == "no":
                            desc = keyboard
                        else:
                            desc = i['desc']
                            
                        button_list = []
                        for ad in i['keys']:
                            button_list.append(ad)
                        reply_markup=ReplyKeyboardMarkup(build_menu(button_list,n_cols=1),one_time_keyboard=False,resize_keyboard=True)
                        context.bot.send_message(chat_id=user,text=desc,reply_markup=reply_markup,parse_mode="markdown")
                        check_position(user=user,keyboard=keyboard)
                        break
                        
                elif f"{keyboard}" == "🛒 Cart":
                    keyee =[["Checkout"],["Back to store"]]
                    keyboard = ReplyKeyboardMarkup(keyee,one_time_keyboard=False,resize_keyboard=True)
                    with open("./jsons/users_order.json") as fp:
                        orders = json.load(fp)
                    for i in orders:
                        if i['id'] == user:
                            have_ordered = i['totallist']
                            ads_list = i['orders']
                            tot = "€{0:,}".format(int(i['topay']))
                           
                            if have_ordered == 0 or ads_list == []:
                                kesyee =[["Back to store"]]
                                skeyboard = ReplyKeyboardMarkup(kesyee,one_time_keyboard=False,resize_keyboard=True)
                                update.message.reply_text("<code>Your basket is empty.Go to the Products section and select the desired product.</code>",parse_mode="html",reply_markup=skeyboard)
                                break
                            else:
                                text =f"You can proceed to checkout or return to the store.\n\n"
                                button_list = []
                                idx = 1
                                for ad in ads_list:
                                    text += f"<b>{idx}. {ad}</b>\n"
                                    idx+=1
                                    button_list.append(InlineKeyboardButton(f"{ad} ❌", callback_data =f"cancelorder {idx-2} {ad}"))
                                reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
                                ioi = update.message.reply_text("❗️❗️❗️New bot link for checking the legitimacy of bots",parse_mode="html",reply_markup=keyboard)
                                tyu = update.message.reply_text(text=f"{text}\nTotal: {tot} ", parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True,reply_markup=reply_markup)
                                i['del']=tyu.message_id
                                i['del2'] = ioi.message_id
                                with open("./jsons/users_order.json", "w" ) as poi:
                                    json.dump(orders,poi,
                                        ensure_ascii=False,  
                                        indent=3,  
                                       separators=(',',': '))
                                break
                    
                
                elif f"{keyboard}" == "PGP Key":
                    with open("./jsons/keys.json", 'r') as fp:
                        keys = json.load(fp)
                    pgp = keys['pgp']
                    context.bot.send_message(chat_id=user,text=pgp)
                    break
                
                elif f"{keyboard}" == "📊Feedback 98.97%":
                    message = update.message

                    paginator = InlineKeyboardPaginator(
                        page_count=len(character_pages),
                        current_page=1,
                        data_pattern='character#{page}'
                    )
                    paginator.add_before(
                        InlineKeyboardButton('All', callback_data='character#1'),
                        InlineKeyboardButton('Positive', callback_data='positive#1'),
                        InlineKeyboardButton('Neutral', callback_data='neutral#1'),
                        InlineKeyboardButton('Negative', callback_data='negative#1')
                    )  
    
                    character = character_pages[0]

                    message.reply_text(
                        text='{title}'.format(**character),
                        reply_markup=paginator.markup,
                        parse_mode=ParseMode.MARKDOWN
                    )
                    break
                elif f"{keyboard}" == "Checkout":
                    with open("./jsons/users_order.json","r" ) as fifi:
                        ids = json.load(fifi)
                        for idf in ids:
                            if idf['id'] == user:
                                dele = idf['del'] 
                                print(dele)
                                dle = idf['del2']
                                context.bot.deleteMessage (message_id = dele,chat_id = user)
                                context.bot.deleteMessage (message_id = dle,chat_id = user)
                                
                                
                    with open("./jsons/ship.json","r") as shipping:
                        shipped = json.load(shipping)
                    
                    if  shipped == []:
                        keyee =[["Checkout"],["Back to store"]]
                        keyboardd = ReplyKeyboardMarkup(keyee,one_time_keyboard=False,resize_keyboard=True)
                        update.message.reply_text("No shipping method available now",reply_markup=keyboardd)
                    else:
                        button_list = []
                        idx = 1
                       
                        for ad in shipped:
                            amount = keyboard[0]
                            goods = keyboard[0:]
                            keyboards = " ".join(goods)
                            print(goods, keyboards)
                            idx+=1
                            button_list.append(InlineKeyboardButton(f"{ad}", callback_data =f"shipping  {ad}"))
                        reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
                        update.message.reply_text("Choose a shipping method",reply_markup=reply_markup)
                        
                else:
                    with open("./jsons/users_order.json","r" ) as fifi:
                        ids = json.load(fifi)
                        for idf in ids:
                            if idf['id'] == user:
                                if idf['extra']=="useraddress":
                                    user_address = update.message.text
                                    context.bot.deleteMessage (message_id = update.message.message_id,chat_id = user)
                                    text = "*Great, almost done!*\n\nPlease check the items, payment method, address and shipping method.\n\n"
                                    
                                    ship_add = idf['shipmethod']
                                    pay_met = idf['paytype']
                                    total = idf['topay']
                                    amo = ship_add.split()
                                    acc = int(float(amo[0].replace("$","")))+int(float(total))
                                
                                    idx = 1
                                    for adx in idf['orders']:
                                        text += f"*{idx}. {adx}*\n"
                                        idx += 1
                                    boko = f"{text}\n\n" \
                                                 f"`{user_address}`\n\n" \
                                                 f"*{ship_add}*\n" \
                                                 f"Payment Method: *{pay_met}*\n" \
                                                 f"Total: *${acc}*"
                                    keyboarde =  [
                                       [  InlineKeyboardButton("Checkout", callback_data="final"),
                                         InlineKeyboardButton("Cancel",callback_data="menu")]
                                        ]
                                    yeye = InlineKeyboardMarkup(keyboarde)
                                    with open("./jsons/users_order.json") as fpp:
                                        porders = json.load(fpp)
                                    for i in porders:
                                        if i['id'] == user:
                                            i['extra'] = ""
                                            
                                    with open("./jsons/users_order.json", 'w') as json_file:
                                        json.dump(porders, json_file, 
                                                       ensure_ascii=False,  
                                                       indent=3,  
                                                       separators=(',',': '))
                                    context.bot.editMessageText(chat_id=update.message.chat_id,message_id=int(idf['extra2']),text=boko,parse_mode="markdown",reply_markup=yeye)
                                    break
                    


                    
def check_position(user,keyboard):
    user = user
    print(user, keyboard)
    with open("./jsons/users_order.json") as fp:
        orders = json.load(fp)
    for i in orders:
        if i['id'] == user:
            i['key'] = keyboard
            with open("./jsons/users_order.json", 'w') as json_fil:
                json.dump(orders, json_fil, 
                          indent=3,  
                        separators=(',',': '))   
                
                
        else:
            print("error")    
                        
                        