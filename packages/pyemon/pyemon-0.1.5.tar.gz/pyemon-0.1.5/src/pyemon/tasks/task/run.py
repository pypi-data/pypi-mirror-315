from ...task import *
from ...directory import *
import glob
import importlib

class TaskRunTask(Task):
  def run(self, argv):
    builtinTaskNames = list(map(lambda task: task.Name, Task.tasks()))
    sys.path.append(os.getcwd())
    tasks = {}
    for path in glob.glob("**/pyetask.py", recursive = True):
      names = Directory.split(path)
      names[-1] = os.path.splitext(names[-1])[0]
      for task in importlib.import_module(".".join(names)).Task.tasks():
        if task.Name not in builtinTaskNames:
          tasks[task.Name] = task
    if len(argv) == 0:
      strings = ["<Tasks>"]
      for task in tasks.values():
        strings.append(task.to_string("  "))
        strings.append("")
      sys.exit("\n".join(strings))
    else:
      name = List.shift(argv)
      if name in tasks:
        tasks[name].run(argv)
      else:
        sys.exit(String.to_undefined_string(name))
Task.parse_if_main(__name__, TaskRunTask("<task args>"))
