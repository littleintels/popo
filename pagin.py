

import os
import time
import sys

# pip install python-telegram-bot
from telegram import Update, ParseMode
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram.ext.dispatcher import run_async
from telegram import *
from telegram.ext import *
# pip install python-telegram-bot-pagination
from telegram_bot_pagination import InlineKeyboardPaginator

sys.path.append('..')

from common import get_logger, log_func, reply_error
from utils import is_equal_inline_keyboards
from data import *


log = get_logger(__file__)


run_async
log_func(log)
def startkjgg(update: Update, context: CallbackContext):
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

run_async
log_func(log)
def on_callback_query(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    source, page = query.data.split('#', 1)
    know_which =query.data.split()
   
    print(page)
    page = int(page)

    paginator = InlineKeyboardPaginator(
        page_count=len(character_pages),
        current_page=page,
        data_pattern=source + '#{page}'
    )
    paginator.add_before(
        
        InlineKeyboardButton('All', callback_data='character#1'),
        InlineKeyboardButton('Positive', callback_data='positive#1'),
        InlineKeyboardButton('Neutral', callback_data='neutral#1'),
        InlineKeyboardButton('Negative', callback_data='negative#1')
    )              
    
    

    # Fix error: "telegram.error.BadRequest: Message is not modified"
    if is_equal_inline_keyboards(paginator, query.message.reply_markup):
        return

    character = character_pages[page - 1]

    query.message.edit_text(
        text='{title}'.format(**character),
        reply_markup=paginator.markup,
        parse_mode=ParseMode.MARKDOWN
    )

run_async
log_func(log)
def neutral(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    source, page = query.data.split('#', 1)
    know_which =query.data.split()
   
    print(page)

    page = int(page)

    paginator = InlineKeyboardPaginator(
        page_count=len(Neutral),
        current_page=page,
        data_pattern=source + '#{page}'
    )
    paginator.add_before(
        InlineKeyboardButton('All', callback_data='character#{}'.format(page)),
        InlineKeyboardButton('Positive', callback_data='positive#1'),
        InlineKeyboardButton('Neutral', callback_data='neutral#1'),
        InlineKeyboardButton('Negative', callback_data='negative#1')
    )              
    
    

    # Fix error: "telegram.error.BadRequest: Message is not modified"
    if is_equal_inline_keyboards(paginator, query.message.reply_markup):
        return

    character = Neutral[page - 1]

    query.message.edit_text(
        text='{title}'.format(**character),
        reply_markup=paginator.markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    
    
run_async
log_func(log)
def negative(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    source, page = query.data.split('#', 1)
    know_which =query.data.split()
   
    print(page)

    page = int(page)

    paginator = InlineKeyboardPaginator(
        page_count=len(Negative),
        current_page=page,
        data_pattern=source + '#{page}'
    )
    paginator.add_before(
        InlineKeyboardButton('All', callback_data='character#{}'.format(page)),
        InlineKeyboardButton('Positive', callback_data='positive#1'),
        InlineKeyboardButton('Neutral', callback_data='neutral#1'),
        InlineKeyboardButton('Negative', callback_data='negative#1')
    )           
    
    

    # Fix error: "telegram.error.BadRequest: Message is not modified"
    if is_equal_inline_keyboards(paginator, query.message.reply_markup):
        return

    character = Negative[page - 1]

    query.message.edit_text(
        text='{title}'.format(**character),
        reply_markup=paginator.markup,
        parse_mode=ParseMode.MARKDOWN
    )


run_async
log_func(log)
def positive(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    source, page = query.data.split('#', 1)
    know_which =query.data.split()
   
    print(page)

    page = int(page)

    paginator = InlineKeyboardPaginator(
        page_count=len(Positive),
        current_page=page,
        data_pattern=source + '#{page}'
    )
    paginator.add_before(
        InlineKeyboardButton('All', callback_data='character#{}'.format(page)),
        InlineKeyboardButton('Positive', callback_data='positive#1'),
        InlineKeyboardButton('Neutral', callback_data='neutral#1'),
        InlineKeyboardButton('Negative', callback_data='negative#1')
    )              
    
    

    # Fix error: "telegram.error.BadRequest: Message is not modified"
    if is_equal_inline_keyboards(paginator, query.message.reply_markup):
        return

    character = Positive[page - 1]

    query.message.edit_text(
        text='{title}'.format(**character),
        reply_markup=paginator.markup,
        parse_mode=ParseMode.MARKDOWN
    )

