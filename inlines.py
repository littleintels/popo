
from telegram.ext import *
from telegram import *
import telegram
import telegram
import json
from app import *


def inlines(update,context) -> None:
    keyboard = update.message.text.split()
    user = int(update.effective_chat.id)
    print(keyboard)
    
    if update.message.chat['type'] == "private":
        with open("./jsons/keys.json", 'r') as fps:
            admi = json.load(fps)
            
        
           
        
        admin = admi['admins']
        if user in admin:
            if len(keyboard) >= 2:
                keyboard_name = keyboard[1].replace("#", " ")
                
                inline_keyboards = keyboard[2:]
                koko = " ".join(inline_keyboards)
                
                with open("./jsons/new_keys.json", 'r') as fp:
                    keys = json.load(fp)
                for i in keys:
                    
                    if i['name'] == f"{keyboard_name}":
                        print("yes")
                        
                        if i["keys"] == ["Back"]:
                            print("nothing in keyboard")
                            i['inline'].append(koko)
                        
                            with open("./jsons/new_keys.json", 'w') as json_file:
                                json.dump(keys, json_file,
                                          ensure_ascii=False,  
                                          indent=4    ,
                                          separators=(',',': '))
                        
                            button_list = []
                            idx = 1
                            for ad in i['inline']:
                                idx+=1
                                button_list.append(InlineKeyboardButton(f"{ad} ❌", callback_data =f"removeinline {idx-2} {keyboard_name}"))
                            print(keyboard_name)
                            reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
                            context.bot.send_message(chat_id=user,text="Keyboard Added",reply_markup=reply_markup)
                            break
                        else:
                            context.bot.send_message(chat_id=user,text="can't add inline keyboard here because button keyboard exist")
                        
                else:
                    context.bot.send_message(chat_id=user,text="Please use correct keyboard names\n/inline [keyboard name] [your goods seperated with comma's]")
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
def keyboa(update,context) -> None:
    keyboard = update.message.text.split()
    user = int(update.effective_chat.id)
 
    
    if update.message.chat['type'] == "private":
        with open("./jsons/keys.json", 'r') as fps:
            admi = json.load(fps)
            
        admin = admi['admins']
        if user in admin:
            
            if len(keyboard) >= 2:
                keyboard_name = keyboard[1].replace("#", " ")
                
                
                if "€" in keyboard[2:]:
                    inline_keyboards = keyboard[2:].replace("€" , "$")
                else:
                    inline_keyboards = keyboard[2:]
                
                koko = " ".join(inline_keyboards)
                
                with open("./jsons/new_keys.json", 'r') as fp:
                    keys = json.load(fp)
                for i in keys:
                    
                    if i['name'] == f"{keyboard_name}":
                        
                        
                        i['keys'][-1] = koko
                        i['keys'].append("Back")
                        
                        keys.append({
                            "name": koko,
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
                        context.bot.send_message(chat_id=user,text="Keyboard Added",reply_markup=reply_markup)
                      
                        break
                     
                    
                    
                else:
                    context.bot.send_message(chat_id=user,text="Please use correct keyboard names\n/key [keyboard name] [your goods seperated with comma's]")
        else:
            context.bot.send_message(user,"Usage /key [Sub-Keyboard name]")
                    
                    
                    
                    
                    
                    
                    
def desc(update,context) -> None:
    keyboard = update.message.text.split()
    user = int(update.effective_chat.id)
    print(keyboard)
    
    if update.message.chat['type'] == "private":
        with open("./jsons/keys.json", 'r') as fps:
            admi = json.load(fps)
            
        admin = admi['admins']
        if user in admin:
           
            if len(keyboard) >= 2:
                if "#" in keyboard[1]:
                    keyboard_name = keyboard[1].replace("#", " ")
                else:
                    keyboard_name = keyboard[1]
                print(keyboard_name)                
                
                inline_keyboards = keyboard[2:]
                koko = " ".join(inline_keyboards)
                print(koko)
                
                
                with open("./jsons/new_keys.json", 'r') as fp:
                    keys = json.load(fp)
                for i in keys:
                    
                    if i['name'] == keyboard_name:
                        print("yes")
                        i['desc'] = koko
                        print(koko)
                        with open("./jsons/new_keys.json", 'w') as json_file:
                            json.dump(keys, json_file, 
                               ensure_ascii=False,  
                               indent=4    ,
                               separators=(',',': '))
                        context.bot.send_message(chat_id=user,text="Settings done")
                        break
                
                else:
                    context.bot.send_message(chat_id=user,text="Please use correct keyboard names\n/desc [keyboard name] [message]")
                    