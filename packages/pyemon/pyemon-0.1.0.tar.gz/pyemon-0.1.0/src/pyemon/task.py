from .option import *
from .command import *
import sys
import inflection
import copy

class Task:
  __Tasks = {}

  def __init__(self, caption = ""):
    name = inflection.underscore(self.__class__.__name__)
    if name.endswith("_task"):
      name = name[:-5]
    self.__Name = name.replace("_", ".")
    self.Caption = caption
    self.OptionParser = OptionParser()

  @property
  def Name(self):
    return self.__Name

  def run(self, argv):
    pass

  def to_string(self, indent = ""):
    strings = []
    if len(self.Caption) == 0:
      strings.append("""{}{}""".format(indent, self.__Name))
    else:
      strings.append("""{}{} # {}""".format(indent, self.__Name, self.Caption))
    string = self.OptionParser.to_string("""{}  """.format(indent))
    if 0 < len(string):
      strings.append(string)
    return "\n".join(strings)

  def __str__(self):
    return self.to_string()

  @classmethod
  def set(cls, task):
    Task.__Tasks[task.Name] = task
    return task

  @classmethod
  def get(cls, name):
    if name in Task.__Tasks:
      return Task.__Tasks[name]
    else:
      return None

  @classmethod
  def tasks(cls):
    return tuple(Task.__Tasks.values())

  @classmethod
  def parse(cls, argv):
    if 0 < len(argv):
      newArgv = copy.deepcopy(argv)
      name = List.shift(newArgv)
      if name in Task.__Tasks:
        Task.__Tasks[name].run(newArgv)
      else:
        sys.exit(Task.to_undefined_string(name))

  @classmethod
  def parse_if_main(cls, name, task = None):
    if task is not None:
      Task.set(task)
    if name == "__main__" or name == "pyemon.cli":
      argv = copy.deepcopy(sys.argv[1:])
      if task is not None:
        argv.insert(0, task.Name)
      Task.parse(argv)

  @classmethod
  def to_undefined_string(self, name):
    return """{} task is undefined.""".format(Command.to_error_string(name))
