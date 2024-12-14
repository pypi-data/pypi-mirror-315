# coding: utf-8

"""
Step 1. Find telegram bot named "@BotFather".
Step 2. To create a new bot type “/newbot” or click on it.
Step 3. Follow instructions.
Step 4. See a new API token generated for it. Like this: 270485614:AAHfiqksKZ8WmR2zSjiQ7_v4TMAKdiHm9T0
"""

from lockdown_protocol_extra_bot.settings_handler import SettingsHandler
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
import io
import time
from ksupk import singleton_decorator, get_time_str, ProbabilityBag
from lockdown_protocol_extra_bot.gen_challenges import get_challenges
from lockdown_protocol_extra_bot.distribute_challenges import distribute_challenges


@singleton_decorator
class GameBot:

    def __init__(self, token: str, password: str):

        self.available_nicknames_cls = ["🟥 red", "🍊 orange", "🟨 yellow",
                                        "🟩 green", "🐬 cyan", "🟦 blue",
                                        "😈 purple", "🦄 pink", "⬜️ white"]  # 🟪 -- purple square

        self.bot = telebot.TeleBot(token)
        self.password = password
        self.current_players = {}
        self.available_nicknames = self.available_nicknames_cls.copy()

        self.bot.message_handler(commands=['join'])(self.join)
        self.bot.message_handler(commands=['leave'])(self.leave)
        self.bot.message_handler(commands=['start_round'])(self.start_round)
        self.bot.message_handler(commands=['reset'])(self.reset)
        self.bot.message_handler(commands=['help'])(self.help)
        self.bot.message_handler(func=lambda message: True)(self.handle_message)

    def handle_message(self, message):
        user_id = message.from_user.id
        self.bot.reply_to(message, "🌰 Нечего ответить. ")

    def help(self, message):
        help_txt = ("❔\n "
                    "/join -- присоединиться к игре\n "
                    "/leave -- ливнуть\n "
                    "/start_round -- запустить раунд\n "
                    "/reset -- перезапустить всё\n "
                    "/help -- показать это сообщение\n ")
        self.bot.reply_to(message, help_txt)

    def join(self, message):
        user_id = message.from_user.id
        if user_id in self.current_players:
            self.bot.reply_to(message, "🫵 Вы уже присоединились к игре.")
            return

        if not self.available_nicknames:
            self.bot.reply_to(message, "❌ Мест нет.")
            return

        markup = InlineKeyboardMarkup()
        for nickname in self.available_nicknames:
            markup.add(InlineKeyboardButton(nickname, callback_data=f"nickname_{nickname}"))

        self.bot.send_message(
            message.chat.id,
            "Цвет?",
            reply_markup=markup
        )

    def leave(self, message):
        user_id = message.from_user.id
        if user_id not in self.current_players:
            self.bot.reply_to(message, "❌ Вы и так не играете. ")
            return

        nickname = self.current_players.pop(user_id)
        self.available_nicknames.append(nickname)

        self.notify_all(f"🚪 {nickname} покинул игру.")
        self.bot.reply_to(message, "🫵 Вы покинули игру.")

    def start_round(self, message):
        if not self.current_players:
            self.bot.reply_to(message, "❌ Нет игроков для начала раунда.")
            return
        if len(self.current_players) < 1:  # 3
            self.notify_all("❌ Нужно хотя бы 3 игрока! ")
        else:
            player_challenges = distribute_challenges(self.current_players, get_challenges())
            for player_i in player_challenges:
                self.bot.send_message(player_i, player_challenges[player_i])
            self.notify_all("🔊 Раунд начался! ")

    def reset(self, message):
        def ask_password(message):
            self.bot.send_message(message.chat.id, "🔐 Введите пароль для сброса: ")
            self.bot.register_next_step_handler(message, check_password)

        def check_password(message):
            if message.text == self.password:
                self.available_nicknames = self.available_nicknames_cls.copy()
                self.notify_all("🔔 Игра была сброшена. ")
                # self.bot.reply_to(message, "Игра успешно сброшена.")
                self.current_players.clear()
            else:
                self.bot.reply_to(message, "❌ Неверный пароль.")

        ask_password(message)

    def notify_all(self, text):
        for user_id in self.current_players:
            self.bot.send_message(user_id, text)

    def run(self):
        @self.bot.callback_query_handler(func=lambda call: call.data.startswith("nickname_"))
        def handle_nickname_selection(call):
            user_id = call.from_user.id
            if user_id in self.current_players:
                self.bot.answer_callback_query(call.id, "❌ Вы уже выбрали псевдоним. Если надо поменять, то leaveните.")
                return

            nickname = call.data.split("_")[1]
            if nickname not in self.available_nicknames:
                self.bot.answer_callback_query(call.id, "❌ Этот псевдоним уже занят. Слишком долго выбирал. ")
                return

            self.current_players[user_id] = nickname
            self.available_nicknames.remove(nickname)

            # self.bot.answer_callback_query(call.id, f"Вы выбрали псевдоним: {nickname}")
            # self.bot.send_message(call.message.chat.id, f"Вы успешно присоединились к игре как {nickname}.")
            self.notify_all(f"🔔 Новый игрок присоединился: {nickname}")

        self.bot.polling()


def start_telegram_bot():
    sh = SettingsHandler()

    bot_instance = GameBot(sh.tele_token(), sh.tele_password())
    bot_instance.run()
    #
    # c = 0
    # while c < 1:
    #     try:
    #         c += 1
    #         bot_instance = GameBot(sh.tele_token(), sh.tele_password())
    #         bot_instance.run()
    #     except Exception as e:
    #         kek = f"e"
