import os

def command(args):
  try:
    os.mkdir(str(args[0]))
  except FileExistsError:
    print("Klasör Zaten Var")