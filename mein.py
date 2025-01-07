import os

from pytimeparse import parse

from dotenv import load_dotenv
import ptbot


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)

def notify_progress(secs_left,chat_id,message_id,question):
    progress= parse(question)-secs_left
    progres_bar=render_progressbar(parse(question),progress)
    message_time='Осталось секунд:{}'.format(secs_left)
    bar=message_time+progres_bar
    bot.update_message(
        chat_id, 
        message_id, 
        bar,
        )
        
def wait(chat_id, question):
    message_id=bot.send_message(chat_id,'Таймер запущен')  
    bot.create_countdown(
        parse(question), 
        notify_progress,
        question=question, 
        chat_id=chat_id, 
        message_id=message_id,
        )
    bot.create_timer(
        parse(question), 
        choose, 
        author_id=chat_id, 
        message=question
        )   
       
def choose(author_id, message):    
    bot.send_message(author_id, 'Время вышло')


if __name__ == '__main__':
    load_dotenv()
    tg_token = os.environ['TELEGRAM_TOKEN']
    tg_chat_id = os.environ['TG_ID'] 
    bot = ptbot.Bot(tg_token)
    bot.send_message(tg_chat_id, 'Привет!')
    bot.reply_on_message(wait)
    bot.reply_on_message(notify_progress)
    bot.run_bot()