import pyperclip

copied_text = pyperclip.paste()
try:
    print(copied_text.split("\n")[1])
except IndexError:
    pass


