
from telegram.ext import *
from telegram import *
import telegram
import json
from app import *
from pay import *

import time


def refresh(update,context) -> None:
    query : CallbackQuery = update.callback_query
    user = int(query.message.chat.id)
    text = update.callback_query.data
    texty = text.split()
    print(texty)
    keyee =[["Checkout"],["Back to store"]]
    keyboardd = ReplyKeyboardMarkup(keyee,one_time_keyboard=False,resize_keyboard=True)

    if len(texty)==1:
        #print(texty)
        with open("./jsons/stats.json") as bot_status:
            status_bot = json.load(bot_status)
        if text == "deactivate":
            status_bot['status'] = False
            with open("./jsons/stats.json", 'w') as json_file:
                json.dump(status_bot, json_file)
            context.bot.deleteMessage (message_id = query.message.message_id,
                           chat_id = user)
            query.answer("Bot off 🔴")
        elif text == "activate":
            status_bot['status'] = True
            with open("./jsons/stats.json", 'w') as json_file:
                json.dump(status_bot, json_file)
            context.bot.deleteMessage (message_id = query.message.message_id,
                           chat_id = user)
            query.answer("Bot activated 🟢")
        elif text == "close":
            query.answer("Closed success")
            context.bot.deleteMessage (message_id = query.message.message_id,
                           chat_id = user)
       
        elif text == "menu":
            context.bot.deleteMessage (message_id = query.message.message_id,
                           chat_id = user)
            with open("./jsons/keys.json", 'r') as fp:
                keys = json.load(fp)
            pgp = keys['start']
            keyee =[["Products","PGP Key"],["📦 Orders (0)","📊Feedback 98.97%","💵 Payments"],["🛒 Cart","✉️ Chat"]]
            keyboardj = ReplyKeyboardMarkup(keyee,one_time_keyboard=False,resize_keyboard=True)
            context.bot.send_message(user,pgp,parse_mode="html",disable_web_page_preview=True,reply_markup=keyboardj)
        elif text == "pgpkey":
            context.bot.send_document(user, document=open('./PGP.txt', 'rb'), filename="Please encrypt your sensitive data with key")
        elif text == "check":
            context.bot.deleteMessage (message_id = query.message.message_id,
                           chat_id = user)
            ioi =  context.bot.send_message(chat_id=user,text="❗️❗️❗️New bot link for checking the legitimacy of bots",parse_mode="html",reply_markup=keyboardd)
            with open("./jsons/users_order.json", "r") as fp:
                orders = json.load(fp)
            for i in orders:
                if i['id'] == user:
                    have_ordered = i['totallist']
                    ads_list = i['orders']
                    tot = "${0:,}".format(int(i['topay']))
                    text =f"You can proceed to checkout or apply a discount or return to the store.\n\n"
                    button_list = []
                    idx = 1
                    for ad in ads_list:
                        text += f"<b>{idx}. {ad}</b>\n"
                        idx+=1
                        button_list.append(InlineKeyboardButton(f"{ad} ❌", callback_data =f"cancelorder {idx-2} {ad}"))
                    reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
                    tyu = context.bot.send_message(chat_id=user,text=f"{text}\nTotal: {tot}", parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True,reply_markup=reply_markup)
                    
                    print(tyu.message_id)
                    with open("./jsons/users_order.json", "r") as fpx:
                        ordersx = json.load(fpx)
                    for ix in ordersx:
                        if ix['id'] == user:  
                            ix['del']= tyu.message_id
                            ix['del2'] = ioi.message_id
                            with open("./jsons/users_order.json", "w" ) as poi:
                                json.dump(ordersx,poi,
                                        ensure_ascii=False,  
                                        indent=3,  
                                       separators=(',',': '))
                    break
        elif text == "final":
            with open("./jsons/users_order.json","r" ) as fifi:
                ids = json.load(fifi)
            for idf in ids:
                if idf['id'] == user:
                    currency = idf['paytype']
                    ship_method = idf['shipmethod']
                    total = idf['topay']
                    amo = ship_method.split()
                    acc = int(float(amo[0].replace("$","")))+int(float(total))
                    Pay = NowPayments()
                    n = Pay.createPayment(price_amount=acc, price_currency='usd', pay_currency= currency )
                    id = 1
                    for basket in idf['orders']:
                        bas = f"*{id}.* {basket}\n"
                    message =  f"✅Payment for *Order {n['payment_id']}*\n\n" \
                                       f"*Your Basket*\n" \
                                       f"{bas}\n\n" \
                                       f"Delivery:\n*{ship_method}*\n\n" \
                                       f"Transfer {n['pay_amount']} {n['pay_currency'].upper()} to\n*{n['pay_address']}*\n\n" \
                                       f"Please send *EXACT* amount shown above within 120 minutes or your payment will not be recognised by the bot and may experience delays! As soon as the payment appears on the blockchain and the bot detect your payment, your order will not be automatically canceled.\n\n" \
                                       f"*Attention!* The average commission fee for sending coins is *~6.0E-5 BTC.* If your wallet sets the commission fee itself, please add the average commission to the amount to avoid further problems."
                    keyboarde =  [
                                       [  InlineKeyboardButton("Show QR Code", callback_data="qr")],
                                       [  InlineKeyboardButton("Payment Details",callback_data=f"det {n['pay_address']} {n['pay_amount']} ")]
                                  ]
                    yeye = InlineKeyboardMarkup(keyboarde)
                    boi = query.edit_message_text(message,parse_mode="markdown",reply_markup=yeye)
                    context.bot.pin_chat_message(chat_id=user, message_id=boi.message_id, disable_notification=False, timeout=None)
                    with open("./jsons/users_order.json") as fp:
                        orders = json.load(fp)
                    for ie in orders:
                        if ie['id'] == user:
                            ie['orders']=[]
                            ie['topay']=0
                            ie['totallist']=0
                    
                    with open("./jsons/users_order.json", 'w') as json_file:
                        json.dump(orders, json_file, 
                               ensure_ascii=False,  
                               indent=3,  
                               separators=(',',': '))
                    time.sleep(60)
                    Pay = NowPayments()
                    n = Pay.getPaymentStatus(5016641558)
                    if n['payment_status'] == "waiting":
                        text = f"Payment for *Order {n['payment_id']}* has not yet been received\n\nPlease note 100 minutes remain untill the order is automatically cancelled"
                        context.bot.send_message(user,text)
                    elif n['payment_status'] == "finished":
                        text = f"Payment for Order {n['payment_id']} has been received"
                        context.bot.send_message(user,text)
                    time.sleep(60)
                    mes = f"Payment for Order {n['payment_id']} is automatically cancelled. System did not received correct payment amount within 120 minutes after placing the order.\n\n"  \
                               f"Why did this happen?\n1. Your payment did not appear on time in the blockchain: this happens when your exchange service or software application send funds with a delay.\n2. You have not sent enough coins for your order.\n3. You didn't send the payment at all.\n\n" \
                               f"How can I solve this problem?\nClick on Check transaction so that I will check the payment automatically again.\nShare your order number - {n['payment_id']} and the transaction hash (TXID) via Chat Support. We will do our best to resolve your problem as soon as possible. Thank you!"
                    bi =context.bot.send_message(user,mes)
                    context.bot.pin_chat_message(chat_id=user, message_id=bi.message_id, disable_notification=False, timeout=None)
                    break
            
    elif len(texty)>=2:
       
        funct = texty[0]
        if len(texty) == 2:
            print("yes")
            keyboard = texty[1]
        else:
            print("no")
            keyboard = "#".join(texty[1:])
        
        
        if funct == "addbutton":
            print("he needs to add button")
            context.bot.send_message(chat_id=user,text=f"Use\n`/key {keyboard}` [your keyboards]\n/key Dissociatives help,Coine\n",parse_mode="markdown")
        elif funct == "addinline":
            print("he needs inline button")
            context.bot.send_message(chat_id=user,text=f"Use\n`/inline {keyboard}` [your goods]\n/key Dissociatives 10GR KETAMINE,28GR KETAMINE\n",parse_mode="markdown")
        elif funct == "desc":
            print("he needs to change description")
            context.bot.send_message(chat_id=user,text=f"Use\n`/desc {keyboard}` [your message]\n/key Dissociatives There are currently one item in store\n",parse_mode="markdown")
        elif funct == "addcart":
            amount = int(float(texty[-1].replace("$","")))
            goods = texty[1:]
            keyboard = " ".join(goods)
            print(keyboard)
            print(amount)
            with open("./jsons/users_order.json") as fp:
                orders = json.load(fp)
            for i in orders:
                if i['id'] == user:
                    i['orders'].append(keyboard)
                    i["totallist"] += 1
                    i['topay'] += amount
                    
                with open("./jsons/users_order.json", 'w') as json_file:
                    json.dump(orders, json_file, 
                               ensure_ascii=False,  
                               indent=3,  
                               separators=(',',': '))
                
            with open("./jsons/users_order.json") as fp:
                orders = json.load(fp)
            for i in orders:
                if i['id'] == user:
                    items = i['totallist']
                    price_all = "${0:,}".format(int(i['topay']))
                    keyboarde =  [[InlineKeyboardButton("Checkout", callback_data="check")]]
                    inline = InlineKeyboardMarkup(keyboarde)
                    message = f"You've added <b>{keyboard} ${amount}</b> to your cart!\n\n" \
                                f"<code>There are currently {items} items in the cart priced at {price_all}</code>"
                    query.answer("Thanks for shopping ✅")
                    context.bot.send_message(chat_id=user,text=message,parse_mode="html",reply_markup=inline)
                    break
                        
        elif funct == "cancelorder":
            amount = int(float(texty[-1].replace("$","")))
            order_id = int(texty[1])
            print(f"Amount: {amount}\nId: {order_id}")
            query.answer("Item removed ✅")
            with open("./jsons/users_order.json") as fp:
                listObj = json.load(fp)
            for i in listObj:
               
                if i['id'] == user:
                    del i['orders'][order_id]
                    i['totallist'] -= 1
                    i['topay'] -= amount
                    with open("./jsons/users_order.json", 'w') as json_file:
                        json.dump(listObj, json_file, 
                                 indent=3,  
                               separators=(',',': '))
                    with open("./jsons/users_order.json") as fp:
                        orders = json.load(fp)
                    for i in orders:
                        if i['id'] == user:
                            have_ordered = i['totallist']
                            ads_list = i['orders']
                            tot = "${0:,}".format(int(i['topay']))
                            if have_ordered == 0:
                                query.edit_message_text("<code>Your basket is empty.Go to the Products section and select the desired product.</code>",parse_mode="html")
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
                                query.edit_message_text(text=f"{text}\nTotal: {tot}", parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True,reply_markup=reply_markup)
                                break
                                
        elif funct == "removeinline":
            keyboard_id = int(texty[1])
            goods = texty[2:]
            keyboardq = " ".join(goods)
            print(keyboardq, keyboard_id)
            query.answer("Item removed ✅")
            with open("./jsons/new_keys.json") as fp:
                inline_keyboard = json.load(fp)
                
            for i in inline_keyboard:
                if i['name'] == f"{keyboardq}":
                    del i['inline'][keyboard_id]
                    with open("./jsons/new_keys.json", 'w') as json_file:
                        json.dump(inline_keyboard, json_file, 
                                 indent=3,  
                               separators=(',',': '))
                        
                    with open("./jsons/new_keys.json") as fp:
                        orders = json.load(fp)
                    for io in orders:
                        if io['name'] == f"{keyboardq}":
                            have_inline = io['inline']
                            if have_inline == []:
                                msg = f"No items in this product"
                                query.edit_message_text(text=msg)
                                break
                            else:
                                text =f"item deleted you can add or remove items\n\n"
                                button_list = []
                                idx = 1
                                for ad in have_inline:
                                    text += f"<b>{idx}. {ad}</b>\n"
                                    idx+=1
                                    button_list.append(InlineKeyboardButton(f"{ad} ❌", callback_data =f"removeinline {idx-2} {keyboardq}"))
                                reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
                                query.edit_message_text(text=text, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True,reply_markup=reply_markup)
                                break
        
        
        elif funct == "removeship":
            keyboard_id = int(texty[1])
            
            query.answer("shipping method removed ✅")
            with open("./jsons/ship.json") as fp:
                inline_keyboard = json.load(fp)
                
            del inline_keyboard[keyboard_id]
            with open("./jsons/ship.json", 'w') as json_file:
                json.dump(inline_keyboard, json_file, )
                        
            with open("./jsons/ship.json") as fp:
                orders = json.load(fp)
            
            
            if orders == []:
                msg = f"No Shipping Method"
                query.edit_message_text(text=msg)
                
            else:
                text =f"Remove shipping method by clicking inline keyboard\n\n"
                button_list = []
                idx = 1
                for ad in orders:
                    text += f"<b>{idx}. {ad}</b>\n"
                    idx+=1
                    button_list.append(InlineKeyboardButton(f"{ad} ❌", callback_data =f"removeship {idx-2}"))
                reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
                query.edit_message_text(text=text, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True,reply_markup=reply_markup)
                
        elif funct == "removepay":
            keyboard_id = int(texty[1])
            
            query.answer("Payment method removed ✅")
            with open("./jsons/paymethod.json") as fp:
                inline_keyboard = json.load(fp)
                
            del inline_keyboard[keyboard_id]
            with open("./jsons/paymethod.json", 'w') as json_file:
                json.dump(inline_keyboard, json_file, )
                        
            with open("./jsons/paymethod.json") as fp:
                orders = json.load(fp)
            
            
            if orders == []:
                msg = f"No Payment Method"
                query.edit_message_text(text=msg)
                
            else:
                text =f"Remove Payment method by clicking inline keyboard\n\n"
                button_list = []
                idx = 1
                for ad in orders:
                    text += f"<b>{idx}. {ad}</b>\n"
                    idx+=1
                    button_list.append(InlineKeyboardButton(f"{ad} ❌", callback_data =f"removepay {idx-2}"))
                reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
                query.edit_message_text(text=text, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True,reply_markup=reply_markup)
                
        elif funct == "shipping":
            ship_method = " ".join(texty[1:])
            amo = texty[1].replace("$","")
            print(ship_method ,  amo)
            with open("./jsons/paymethod.json","r") as payments:
                pays = json.load(payments)
            
            if pays == []:
                query.edit_message_text(text="No payment method available now. Check back later", parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
            else:
                button_list = []
                idx = 1
                for ad in pays:
                    idx+=1
                    button_list.append(InlineKeyboardButton(f"{ad}", callback_data =f"payments  {ad}"))
                reply_markups=InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
                query.edit_message_text(text="Choose your payment method", parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True,reply_markup=reply_markups)
                with open("./jsons/users_order.json") as fpp:
                    porders = json.load(fpp)
                for i in porders:
                    if i['id'] == user:
                        i['shipmethod'] = ship_method
                with open("./jsons/users_order.json", 'w') as json_file:
                    json.dump(porders, json_file, 
                               ensure_ascii=False,  
                               indent=3,  
                               separators=(',',': '))
                
                
                
        elif funct == "payments":
            pay_method = " ".join(texty[1:])
            print(pay_method)
            keyboarde =  [
                                       [  InlineKeyboardButton("Sellers's PGP Key", callback_data="pgpkey")],
                                       [  InlineKeyboardButton("Cancel",callback_data="menu")]
                                  ]
            yeye = InlineKeyboardMarkup(keyboarde)
            tes ="Please reply to this message with your delivery address ensuring it follows the format shown below.\n\n *PGP encryption allowed through the bot*\n\n`Mr First Name Surname\n1 London Street\nWestminster\nLONDON\nW1 1AA\nUnited Kingdom`\n\nIf you have entered your information successfully a confirmation message will appear then follow the instructions to complete order."
            
            bolo = query.edit_message_text(tes,parse_mode="markdown",reply_markup= yeye)
            with open("./jsons/users_order.json") as fpp:
                porders = json.load(fpp)
            for i in porders:
                if i['id'] == user:
                    i['paytype'] = pay_method
                    i['extra'] = "useraddress"
                    i['extra2']=bolo.message_id
            with open("./jsons/users_order.json", 'w') as json_file:
                json.dump(porders, json_file, 
                               ensure_ascii=False,  
                               indent=3,  
                               separators=(',',': '))
                
                
        elif funct == "det":
            address = texty[1]
            amount = texty[2]
            context.bot.send_message(user,text=f"`{address}`",parse_mode="markdown")
            context.bot.send_message(user,text=f"`{amount}`",parse_mode="markdown")
            
            
            
                
            
            
                   
    
            
            