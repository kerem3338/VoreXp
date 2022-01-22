import os

def command(args):
  if os.path.isdir(args[0]):
    os.chdir(args[0])