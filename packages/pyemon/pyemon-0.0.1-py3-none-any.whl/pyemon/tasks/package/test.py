from ...option import *
from ...command import *

def task_package_test(argv):
  Command(["pipenv", "run", "pytest", "-s"] + argv).run()

if __name__ == "__main__":
  task_package_test(sys.argv[1:])
