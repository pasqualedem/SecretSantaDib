import random

GAME_TXT = "res/game.txt"
RULES_TXT = "res/rules.txt"
INFO_TXT = "res/info.txt"


def get_messages():
    with open(GAME_TXT, 'r') as msgtxt:
        game = msgtxt.read()
    with open(RULES_TXT, 'r') as msgtxt:
        rules = msgtxt.read()
    with open(INFO_TXT, 'r') as msgtxt:
        info = msgtxt.read()
    return game, rules, info


def generate_message(santa, child):
    game, rules, info = get_messages()
    spaces = random.randint(300, 500)
    msg = f"Hi {santa},\n" \
          f"If you don't know how the game works:\n" \
          f"{game}" \
          f"READ THE RULES\nREAD THE RULES\nREAD THE RULES\nREAD THE RULES\nREAD THE RULES\nREAD THE RULES\n\n" \
          f"{rules}\n\n" \
          f"Here some info:\n" \
          f"{info}\n" \
          f"OK, now make sure that no one can see your screen now.\n" \
          f"This year your gift goes to ...\n"
    msg += "  |  \n" * (spaces // 2)
    msg += f"Just scroll another {spaces // 2} lines, be patient (HAVE YOU READ THE RULES?)\n"
    msg += "  |  \n" * (spaces // 2)
    msg += "  V  \n"
    msg += f"{child}!!!\n" \
           f"I HOPE THAT YOU RED THE RULES\n"
    msg += f"Good luck!"
    return msg


def get_email():
    game, rules, info = get_messages()
    msg = f"Hi,\n" \
          f"If you don't know how the game works:\n" \
          f"{game}" \
          f"READ THE RULES\nREAD THE RULES\nREAD THE RULES\nREAD THE RULES\nREAD THE RULES\nREAD THE RULES\n" \
          f"{rules}\n\n" \
          f"Here some info:\n" \
          f"{info}\n" \
          f"OK, now make sure that no one can see your screen now.\n" \
          f"This year your gift goes to ...\n\n\n" \
          f"OK, now you are ready to know the name of your child. Just check the ZIP file."
    return msg
