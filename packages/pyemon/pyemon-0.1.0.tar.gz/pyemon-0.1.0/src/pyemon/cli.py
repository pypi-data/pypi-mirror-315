from .tasks.package.build import *
from .tasks.package.init import *
from .tasks.package.install import *
from .tasks.package.test import *
from .tasks.package.upload import *
from .tasks.task.run import *

class HelpTask(Task):
  def run(self, argv):
    if len(argv) == 0:
      strings = ["<Tasks>"]
      for task in Task.tasks():
        strings.append(task.to_string("  "))
        strings.append("")
      sys.exit("\n".join(strings))
    if argv[0] == "help":
      newArgv = copy.deepcopy(argv)
      newArgv.pop(0)
      if len(newArgv) == 0:
        taskNames = []
        for task in Task.tasks():
          if task.Name != "help":
            taskNames.append(task.Name)
        print("""{}""".format(" ".join(taskNames)))
      else:
        print("<Tasks>")
        for name in newArgv:
          task = Task.get(name)
          if task is None:
            sys.exit(Task.to_undefined_string(name))
          else:
            print(task.to_string("  "))
            print("")
    else:
      Task.parse(argv)
Task.parse_if_main(__name__, HelpTask("<task names>"))

def main():
  pass
