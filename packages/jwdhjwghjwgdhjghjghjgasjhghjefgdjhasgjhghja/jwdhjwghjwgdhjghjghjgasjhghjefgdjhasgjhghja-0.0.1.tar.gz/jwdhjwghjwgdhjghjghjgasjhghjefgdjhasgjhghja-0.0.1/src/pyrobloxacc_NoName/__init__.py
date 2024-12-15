import keyboard

def chat(message):
    if isinstance(message, str):
        keyboard.write(message)
    else:
        raise TypeError(f"{message} is not a string.")
