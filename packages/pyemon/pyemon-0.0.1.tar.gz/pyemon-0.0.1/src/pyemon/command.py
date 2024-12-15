import subprocess
import datetime as dt

class Command:
  def __init__(self, args = []):
    self.Args = args

  def run(self):
    Command.print_command("""[{}] $ {}""".format(dt.datetime.now().strftime("%y/%m/%d %H:%M:%S"), " ".join(self.Args)))
    return subprocess.run(self.Args)

  @classmethod
  def print_command(cls, msg):
    print("""\033[40m\033[32m{}\033[0m""".format(msg))

  @classmethod
  def print_error(cls, msg):
    print("""\033[40m\033[31m{}\033[0m""".format(msg))
