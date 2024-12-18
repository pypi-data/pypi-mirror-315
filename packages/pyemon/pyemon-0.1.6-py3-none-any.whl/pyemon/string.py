from .command import *

class String:
  @classmethod
  def to_undefined_string(self, name):
    return """{} is undefined.""".format(Command.to_error_string(name))
