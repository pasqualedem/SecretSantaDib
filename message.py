import random


def generate_message(santa, child):
    spaces = random.randint(300, 500)
    msg = f"Hi {santa},\n" \
          f"make sure that no one can see your screen now.\n" \
          f"This year your gift goes to ...\n"
    msg += "  |  \n" * (spaces // 2)
    msg += f"Just scroll another {spaces // 2} lines, be patient\n"
    msg += "  |  \n" * (spaces // 2)
    msg += "  V  \n"
    msg += f"{child}!!!\n"
    msg += f"Good luck!"
    return msg
