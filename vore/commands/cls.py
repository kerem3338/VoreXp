import os
def command(args):
  if os.name == "nt":
    os.system("cls")
  else:
    os.system("clear")
