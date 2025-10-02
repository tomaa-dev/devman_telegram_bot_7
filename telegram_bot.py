import ptbot
import random
import os
from pytimeparse import parse
from decouple import config


TG_TOKEN = config('TELEGRAM_TOKEN')
TG_CHAT_ID = config('TELEGRAM_ID')


def notify_progress(chat_id, question, bot):
    time_in_seconds = parse(question)
    message_id = bot.send_message(chat_id, "Запускаю таймер...")
    bot.create_countdown(time_in_seconds, reply, chat_id=chat_id, message_id=message_id, total_time=time_in_seconds, bot=bot)
    bot.create_timer(time_in_seconds, timer_reply, chat_id=chat_id, bot=bot)


def reply(secs_left, chat_id, message_id, total_time, bot):
    progress_bar = render_progressbar(total_time, total_time - secs_left)
    bot_message = "Осталось секунд: {}\n{}".format(secs_left, progress_bar)
    bot.update_message(chat_id, message_id, bot_message)


def timer_reply(bot, chat_id):
    bot_message = "Время вышло"
    bot.send_message(chat_id, bot_message)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def main():
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(notify_progress, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()