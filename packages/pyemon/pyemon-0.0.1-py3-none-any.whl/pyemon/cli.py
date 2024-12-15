import sys
import os
import glob
from .option import *
from .directory import *
from .tasks.package.build import *
from .tasks.package.test import *

def main():
  argv = ListHelper(sys.argv[1:])
  for path in glob.glob("**/*.py", root_dir = os.path.dirname(__file__) + "/tasks", recursive = True):
    splitedPath = Directory.split(path)
    splitedPath[-1] = os.path.splitext(splitedPath[-1])[0]
    count = len(splitedPath)
    if splitedPath == argv.slice(0, count):
      for _ in range(count):
        argv.shift()
      methodName = "_".join(["task"] + splitedPath)
      globals()[methodName](argv.List)
      break

if __name__ == "__main__":
  main()
