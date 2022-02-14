
from telegram.ext import *
from telegram import *
import telegram
import json



def delete(update,context) -> None:
    user = int(update.effective_chat.id)
    text = update.message.text.split()
    with open("./jsons/keys.json", 'r') as fp:
            keys = json.load(fp)
    admin = keys['admins']
    if user in admin:
        if len(text) == 1:
            context.bot.send_message(chat_id=user,text="you must add parameter of button to delete\n/delete [button name]",parse_mode="html")
            
        else:
            if len(text) == 2:
                keyboard_name = text[1]
            else:
                keyboard_name = " ".join(text[1:])
                
            with open("./jsons/new_keys.json", 'r') as fps:
                button = json.load(fps)
              
            
            for i in range(len(button)):
                if button[i]["name"] == keyboard_name:
                    button.pop(i)
                    for b in button:
                        if b['name'] == "Products":
                            keyss = b['keys']
                            if keyboard_name in keyss:
                                num = int(keyss.index(keyboard_name))
                                del keyss[num]
                            
                                with open("./jsons/new_keys.json", "w") as j_file:
                                     json.dump(button,j_file,
                                         indent=4, 
                                         separators=(',', ': '))
                           
                                context.bot.send_message(chat_id=user,text="Button removed",parse_mode="html")
                                break
                            
                            else:
                                for y in button:
                                    bo = y['keys']
                                    if keyboard_name in bo:
                                       num = int(bo.index(keyboard_name))
                                       del bo[num]
                                       print(num)
                                       
                                with open("./jsons/new_keys.json", "w") as j_file:
                                     json.dump(button,j_file,
                                         indent=4, 
                                         separators=(',', ': '))
                                     
                                context.bot.send_message(chat_id=user,text="Button removed",parse_mode="html")
                                break
                            
                    break
       
       