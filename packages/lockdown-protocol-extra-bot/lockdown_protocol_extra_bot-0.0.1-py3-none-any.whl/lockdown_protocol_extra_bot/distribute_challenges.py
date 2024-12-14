# coding: utf-8

from ksupk import ProbabilityBag
import random


def distribute_challenges(players: dict, challenges: dict) -> dict:
    ch = {}
    res = {}
    for k_i in challenges:
        if is_adding_challenge(challenges[k_i]["apper_chance"]):
            ch[k_i] = challenges[k_i]["weight"]
    pb = ProbabilityBag(ch)

    c = 1
    for player_i in players:
        chosen_challenge = pb.pop()
        # if chosen_challenge == "0" and c > 0:
        #     c -= 1
        #     pb.add("0", 40)
        res[player_i] = postprocess_challenge(challenges[chosen_challenge]["describe"],
                                              list(players.values()), players[player_i])
        res[player_i] = ("Правила: \n"
                         "1) Никому нельзя рассказывать про это твоё доп. задание. \n"
                         "2) Выполнять его нужно всеми силами и честно (оно обязательное). \n"
                         "3) Оно в приоритете над основным. \n"
                         "\n"
                         "Твоё задание: \n"
                         "🙈🙈🙈🙈🙈🙈🙈🙈🙈🙈\n"
                         f"{res[player_i]}\n"
                         "🐵🐵🐵🐵🐵🐵🐵🐵🐵🐵\n")
    return res


def is_adding_challenge(prob: float | int) -> bool:
    return random.uniform(0, 100) < prob


def postprocess_challenge(text: str, colors: list, cur_color: str) -> str:
    if "{rnd_player}" in text:
        if len(colors) < 2:
            return text
        while True:
            chosen_color = random.choice(colors)
            if chosen_color != cur_color:
                break
        return text.replace("{rnd_player}", f"\"{chosen_color}\"")
    else:
        return text
