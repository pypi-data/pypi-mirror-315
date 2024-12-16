import subprocess
import datetime as dt

class Command:
  def __init__(self, args = []):
    self.Args = args

  def run(self, **kwargs):
    print(Command.to_command_string("""[{}] $ {}""".format(dt.datetime.now().strftime("%y/%m/%d %H:%M:%S"), self.to_string())))
    return subprocess.run(self.Args, **kwargs)

  def to_string(self):
    return " ".join(self.Args)

  def __str__(self):
    return self.to_string()

  @classmethod
  def to_command_string(cls, value):
    return """\033[40m\033[32m{}\033[0m""".format(value)

  @classmethod
  def to_error_string(cls, value):
    return """\033[40m\033[31m{}\033[0m""".format(value)
